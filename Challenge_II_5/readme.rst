Challenge II.5 - Electronic Properties of Aluminum
==================================================

Objective
---------
Investigate the structure and electronic properties of
FCC aluminum and compare its density of states with silicon.

Method
------
Quantum ESPRESSO was used for plane-wave DFT calculations.
The supplied Al.upf pseudopotential was employed.
Energy-cutoff and k-point convergence scans preceded
variable-cell structural relaxation.

The electronic structure calculation used the relaxed
aluminum cell, a 70 Ry wavefunction cutoff,
an 18x18x18 SCF mesh and a 26x26x26 NSCF mesh.
Charge density, Lowdin populations, TDOS and PDOS
were calculated with QE post-processing tools.

Convergence Tests
-----------------

- cutoff_40Ry: -4.63586655 Ry (success: True).
- cutoff_55Ry: -4.63588452 Ry (success: True).
- cutoff_70Ry: -4.63589274 Ry (success: True).
- kpoints_6: -4.6401888 Ry (success: True).
- kpoints_10: -4.63404066 Ry (success: True).
- kpoints_14: -4.63481792 Ry (success: True).
- cell_relax: -4.63482356 Ry (success: True).
- k=18x18x18: -4.63519831 Ry; successive energy difference 5.1755 meV/atom.
- k=22x22x22: -4.63545761 Ry; successive energy difference 3.5280 meV/atom.
- k=26x26x26: -4.63543846 Ry; successive energy difference 0.2605 meV/atom.

Structural Relaxation
---------------------
The initial FCC lattice parameter was approximately
4.03893 Angstrom. The optimized parameter was approximately
4.03299 Angstrom and the final primitive cell volume
was 16.39911 Angstrom^3.

Electronic Properties
---------------------
- Al Fermi energy: 8.0045 eV
- Al spilling parameter: 0.014700
- Al integrated TDOS-PDOS difference: 1.47 percent
- Si Fermi energy: 6.3118 eV
- Si spilling parameter: 0.008900
- Si integrated TDOS-PDOS difference: 0.89 percent

Discussion
----------
Aluminum is metallic, whereas crystalline silicon is
semiconducting. Their TDOS profiles are compared after
shifting each energy axis by its own calculated Fermi level.

The low spilling parameters indicate reasonably good
orbital projections in these calculations.

The 26x26x26 k-point mesh gave a successive energy
difference below 1 meV/atom in the preliminary Al scan.
Further k-point testing would strengthen convergence
verification, particularly for metallic aluminum.

The silicon and aluminum DOS were calculated using
different k-point grids and primitive cells.
Their absolute DOS magnitudes should not be interpreted
as directly normalized per atom without adjustment.

The supplied course FCC structure was used as the initial
structure. An independently downloaded experimental
crystal structure has not yet been verified.
A separate band-structure path calculation was not performed.

Outputs
-------
- Al_vs_Si_TDOS.png: silicon-aluminum TDOS comparison
- Al_PDOS.png: aluminum orbital-projected DOS
- results.csv: initial convergence and relaxation tests
- extended_kpoints.csv: additional k-point calculations
- electronic/: QE inputs, output data and post-processing
