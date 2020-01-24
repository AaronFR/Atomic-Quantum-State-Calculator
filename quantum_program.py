# Standard Physics
electron_volt = 1.602176487 * 10 ** -19  # joules
planks_constant = 6.62607004 * 10 ** -34
speed_of_light = 2.99792458 * 10 ** 8


def energy_given_wavelength_of_particle(wavelength):
    return planks_constant * speed_of_light / wavelength


# Quantum State


def get_energy_level(particle):
    return particle[0]


def get_number_of_electrons(atom):
    if isinstance(atom[2], list):
        number_of_electrons = len(atom[2])
    else:
        number_of_electrons = atom[2]
    
    return number_of_electrons


def get_spin(particle):
    """
    returns individual as well as atomic spin
    """
    total_spin = 0
    if any(isinstance(el, list) for el in particle):
        for electron in particle:
            total_spin += electron[3]
    else:
        total_spin = particle[3]
    return total_spin


def get_highest_energy_level(atom):
    """
    Takes in a simple atomic configuration
    """

    highest_energy_level = 0
    atomic_config = aufbau_principle(atom)
    for electron in atomic_config[2]:
        if highest_energy_level < electron[0]:
            highest_energy_level = electron[0]
    return highest_energy_level


def is_shell_full(atom_electrons, excluding_first_shell=False):
    """
    Takes a full atomic configuration and states whether or not
    its shell if full
    """

    if isinstance(atom_electrons, list):
        number_of_electrons = len(atom_electrons)
    else:
        number_of_electrons = atom_electrons

    full_shells = [2, 10, 18]

    if excluding_first_shell:
        full_shells.pop(0)

    is_full = False
    for valid_full_shell in full_shells:
        if number_of_electrons == valid_full_shell:
            is_full = True

    return is_full


def generator_for_shell(energy_level):
    """
    n is an integer more than or equal to 1
    """
    ang_l = []
    ml = []
    s = [-1, 1]

    n = energy_level
    for index in range(0, energy_level):
        ang_l = index
        for index in range(-ang_l, ang_l + 1):
            ml = index
            for spin in range(-1, 1 + 1, 2):
                s = spin
                yield [n, ang_l, ml, s]


def generate_shell(energy_level):
    """
    n is an integer more than or equal to 1
    """

    gen = generator_for_shell(energy_level)
    shell = []
    while True:
        try:
            shell.append(next(gen))
        except StopIteration:
            break

    return shell

# Describing Atoms


def get_element_name_given_configuration(atom):
    """
    Takes an atomic configuration and strips the spin state information
    Returning the name of the element/ion

    Please use a dictionary
    stored externally
    """
    protons = atom[0]
    neutrons = atom[1]
    electrons = len(atom[2])
    print(len(atom[2]))
    # This should really be a dictionary somehow
    if protons == 1:
        if neutrons == 0:
            return 'Hydrogen'
        if neutrons == 1:
            return 'Deuteron'
    if protons == 6:
        if neutrons == 6:
            return 'Carbon'
        if neutrons == 8:
            return 'Carbon-14'


atom_dict = {"name": "Carbon",
             "protons": 6,
             "neutrons": 6,
             "electrons": 6}


def get_atomic_configuration_given_name(name):
    """
    Takes the name of an element and returns its configuration.
    ELECTRON SPINS NOT ACCOUNTED FOR
    """
    if name == atom_dict["name"]:
        return [atom_dict["protons"],
                atom_dict["neutrons"],
                atom_dict["electrons"]]


# Quantum Methods


def aufbau_principle(atom):
    """
    Could include Madelung's rule,
    but for atomic numbers 12 and below you don't need to care

    Compatible with simple and full atomic configurations
    recommend additional configuration: one where each shell is represented
    """

    number_of_electrons = get_number_of_electrons(atom)

    shell = []
    index = 1

    while len(shell) < number_of_electrons:
        shell += generate_shell(index)
        index += 1
        
    electron_configuration = shell[:number_of_electrons]

    return [atom[0], atom[1], electron_configuration]


def rydberg_transition_formula(atom, transition_from, transition_to):
    """
    Only works for 'hydrogen like' atoms, ones with only a single
    electron

    Returns wavelength of emitted photon
    """

    number_of_electrons = get_number_of_electrons(atom)

    if number_of_electrons != 1:
        raise Exception(
            "Rydberg Equation invalid for non hydrogen-like atoms")
    else:
        rydberg_constant_hydrogen = 1.09677583 * (10 ** 7)
        n1_minus_n2 = (1/(transition_to ** 2) - 1/(transition_from ** 2))

        rydberg = rydberg_constant_hydrogen * (atom[0] ** 2) * (n1_minus_n2)
        wavelength_emitted = 1/(rydberg)

        return wavelength_emitted


def absorption(atom, photon_energy):
    """
    Outputs the new atomic configuration and a photon energy
    if there was remaining energy leftover

    currently the lowest level in the transition is always defined to
    be 1, but this could be variable
    """
    lowest_transition_energy = 1
    highest_energy = get_highest_energy_level(atom)

    full_shell = is_shell_full(atom[2], excluding_first_shell=True)
    higher_trainsition_energy = 2
    if full_shell:
        higher_trainsition_energy = highest_energy + 1
    else:
        higher_trainsition_energy = highest_energy + 1

    wavelength = rydberg_transition_formula(
        atom,
        higher_trainsition_energy,
        lowest_transition_energy
    )
    min_energy_for_transition = energy_given_wavelength_of_particle(wavelength)

    electron_after_change = [generate_shell(higher_trainsition_energy)[0]]
    atom_after_change = [1, 0, electron_after_change]

    if photon_energy < min_energy_for_transition:
        return (atom, photon_energy)
    if photon_energy >= min_energy_for_transition:
        return (atom_after_change, photon_energy)
