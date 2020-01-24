import quantum_program as qp

electron = []
electrons = []
ev = qp.electron_volt
h = qp.planks_constant
c = qp.speed_of_light


def setup():
    electron = [1, 0, 0, -1]
    electrons = [electron]


def test_get_energy_level():
    particle = [1, 'absouletly nothing no one cares about']

    n = qp.get_energy_level(particle)

    assert n >= 1


def test_which_element():
    atom = [1, 0, electrons]

    element = qp.get_element_name_given_configuration(atom)

    assert element == 'Hydrogen'


def test_which_element_deuteron():
    atom = [1, 1, electrons]

    element = qp.get_element_name_given_configuration(atom)

    assert element == 'Deuteron'


def test_which_element_carbon():
    atom = [6, 6, electrons]

    element = qp.get_element_name_given_configuration(atom)

    assert element == 'Carbon'


def test_which_element_carbon_14():
    atom = [6, 8, electrons]

    element = qp.get_element_name_given_configuration(atom)

    assert element == 'Carbon-14'


def test_which_configuration_carbon():
    element = 'Carbon'

    configuration = qp.get_atomic_configuration_given_name(element)

    assert configuration == [6, 6, 6]


def test_aufbau_principle_hydrogen():
    atom = [1, 0, 1]

    configuration = qp.aufbau_principle(atom)

    assert configuration == [1, 0, [[1, 0, 0, -1]]]


def test_aufbau_principle_carbon():
    atom = [6, 6, 6]

    configuration = qp.aufbau_principle(atom)

    assert configuration == [6, 6, [[1, 0, 0, -1],
                                    [1, 0, 0, 1],
                                    [2, 0, 0, -1],
                                    [2, 0, 0, 1],
                                    [2, 1, -1, -1],
                                    [2, 1, -1, 1],
                                    ]]


# Get basic properties


def test_electron_spin():
    electron = [1, 0, 0, 1]

    s = qp.get_spin(electron)

    assert s == 1


def test_total_atomic_spin():
    atom_electrons = [[1, 0, 0, -1], [1, 0, 0, 1], [2, 0, 0,  1]]

    S = qp.get_spin(atom_electrons)

    assert S == 1


# Get all states


def test_get_highest_ground_state_energy():
    """
    The information about the electrons should be redundent
    if anything this method would be used to additavely built
    up the number of electrons.
    """
    atom = [1, 0, 1]

    highest_energy_level = qp.get_highest_energy_level(atom)

    assert highest_energy_level == 1


def test_get_highest_ground_state_energy_2():
    atom = [6, 6, 6]

    highest_energy_level = qp.get_highest_energy_level(atom)

    assert highest_energy_level == 2


def test_get_highest_ground_state_energy_3():
    atom = [10, 10, 10]

    highest_energy_level = qp.get_highest_energy_level(atom)

    assert highest_energy_level == 2


def test_get_highest_ground_state_energy_4():
    atom = [12, 12, 12]

    highest_energy_level = qp.get_highest_energy_level(atom)

    assert highest_energy_level == 3


# emission


def test_photon_emission_rydberg_2_1():
    """
    Rounding is necessary as the given anwser is itself rounded
    """
    atom = [1, 1, 1]
    transition = [2, 1]

    frequency = qp.rydberg_transition_formula(
        atom,
        transition[0],
        transition[1]
    )
    energy = round(h * c / frequency, 2)
    actual_emmitted = round(10.2 * ev, 2)

    assert energy == actual_emmitted


def test_photon_emission_rydberg_3_1():
    atom = [1, 1, 1]
    transition = [3, 1]

    wavelength = qp.rydberg_transition_formula(
        atom,
        transition[0],
        transition[1]
    )
    energy = round(h * c / wavelength, 2)
    actual_emmitted = round(12.09 * ev, 2)

    assert energy == actual_emmitted


# absorption


def test_atom_shell_full_helium():
    helium_shells = [[1, 0, 0, 1], [1, 0, 0, -1]]

    is_full = qp.is_shell_full(helium_shells)

    assert is_full


def test_atom_shell_full_lithium():
    lithium_shells = [[1, 0, 0, 1], [1, 0, 0, -1], [2, 0, 0, 1]]

    is_full = qp.is_shell_full(lithium_shells)

    assert not is_full


def test_photon_absorbed_basic_simple_configuration():
    """
    More to this as a incoming photon could energise any applicable electron
    which changes the total number of photons emitted.
    """
    atom_before_absorption = [1, 0, 1]
    photon_energy = 10.1 * ev

    atom_after_absorption, photon = qp.absorption(atom_before_absorption,
                                                  photon_energy)

    assert atom_after_absorption == atom_before_absorption


def test_photon_absorbed_basic():
    """
    More to this as a incoming photon could energise any applicable electron
    which changes the total number of photons emitted.
    """
    atom_before_absorption = [1, 0, [[1, 0, 0, 1]]]
    photon_energy = 10.1 * ev

    atom_after_absorption, photon = qp.absorption(atom_before_absorption,
                                                  photon_energy)

    assert atom_after_absorption == atom_before_absorption


def test_photon_absorbed_equivalent_energy():
    photon_energy = 10.2 * ev
    atom_before_absorption = [1, 0, [[1, 0, 0, 1]]]

    atom_after_absorption, emitted_photon = qp.absorption(
        atom_before_absorption,
        photon_energy)
    
    assert atom_after_absorption != atom_before_absorption
    assert round(emitted_photon, 1) == 0


def test_photon_absorbed_leftover():
    photon_freq = 10.3 * ev
    atom_before_absorption = [1, 0, [[1, 0, 0, -1]]]

    atom_after_absorption, photon_leftover = qp.absorption(
        atom_before_absorption,
        photon_freq)

    assert atom_after_absorption != atom_before_absorption
    assert atom_after_absorption == [1, 0, [[2, 0, 0, -1]]]
    assert photon_leftover <= photon_freq
