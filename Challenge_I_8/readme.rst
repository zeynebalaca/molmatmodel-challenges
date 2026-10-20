Challenge I.8 - Computational Modeling of UO2I2(H2O)2
=====================================================

Objective
---------
Investigate the molecular structure and electronic energy of
the uranium(VI) complex UO2I2(H2O)2 using MACE and NWChem.

Computational Methods
---------------------
The initial geometry was obtained from the course example
based on the published molecular structure.

MACE calculations used a pretrained MACE-MP medium model
on CPU. Geometry optimization was performed using BFGS
with a maximum force tolerance of 0.05 eV/Angstrom.
The uranium atom was constrained during optimization.

NWChem was used for a B3LYP single-point DFT calculation.
Stuttgart relativistic effective core potentials were used
for uranium and iodine, while 6-31G* basis sets were used
for oxygen and hydrogen.
The NWChem calculation used four MPI processes.

MACE Results
------------
- Initial potential energy: -62.055403 eV
- Final potential energy: -62.442938 eV
- Potential energy change: -0.387535 eV
- Geometry optimization: converged after 14 BFGS steps
- Average optimized U=O bond length: 1.7857 Angstrom
- Average optimized U-I bond length: 3.0280 Angstrom
- Average optimized O-H bond length: 0.9747 Angstrom

NWChem Results
--------------
- Final B3LYP total DFT energy: -377.647069332693 Hartree
- Calculation type: single-point energy
- Execution: completed successfully

Discussion
----------
The optimized MACE geometry remains close to the literature-based
initial structure. However, the initial coordinates were already
derived from published structural parameters. Therefore, agreement
with these reference values does not constitute independent
validation of the pretrained MACE potential for actinide complexes.

The MACE and NWChem total energies are not directly comparable
because the methods use different energy definitions and
electronic-structure approximations.

The NWChem calculation was a single-point calculation on
the geometry specified in its input file, not a geometry
optimization of the final MACE structure.

Reference
---------
Published molecular structure:
https://doi.org/10.1021/ja030260r

Reproducibility
---------------
MACE source script and calculation log are stored in ``mace/``.
NWChem input and calculation log are stored in ``nwchem/``.
The optimized molecular coordinates are retained as XYZ and CIF files.
