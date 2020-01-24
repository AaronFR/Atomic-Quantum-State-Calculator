# Possible Future Features
- Coding standards here are below par now, specifically removing comments and proper spacing
- Structural changes: more robust class structure, move explanation comments from methods. If not a interactive element then examples.
- make atomic dictionary versatile and usable by both get_confic and get_name
- update is_shell_full to calculate all possible shells
- edit shell-generator to implement the aufbau principle properly so that shells are filled diagonally
    ( add fun caveat that due to relativistic effects the aufbau principle is EXPECTED to break down past element 120 ) 
- edit rydberg calculator to have a "force mono-electron" defualt variable
- Lyman, Balmer, etc series for hydrogen
- Chemical bonding given 2 atoms
- gui showing atoms (really simple, just dots)
- Add a isinstance list method for determining if a list is a simple configuration

## Note 24/08/2019
I think I'll leave this project for now.
I was hugely motivated to study coding standards but I'm covering that in spades @ OS right now.
Leaving to do a more interesting project.

## 0.1.0
- ability to generate all configurations for all possible atoms
- getting basic atom properties(number of electrons, energylevel, spin)
- Attributes about atom and shell(highest energy, is shell full)
- rydberg transition calculation (Hydrogen only)
- naming atom given configuration(Very Basic)
- ability to excite electron with a photon(E1 to E2 ONLY)
- tests and functionality for slit experiment diffraction scrapped
- look into applications of your system
    maybe moddeling atom/photon momentum,
    the colour of a simple object(coal/diamond or gold)
