Challenge II.2 - Silicon Convergence Tests
==========================================

Objective
---------
Investigate plane-wave cutoff and k-point convergence for
crystalline silicon using two pseudopotentials.

Computational Method
--------------------
Self-consistent calculations were performed with Quantum
ESPRESSO for the two-atom silicon primitive cell.
Cutoff energies of 30, 50 and 70 Ry were tested at 4x4x4
k-points. K-point meshes of 2x2x2, 4x4x4 and 6x6x6
were tested at 70 Ry. Charge-density cutoffs were set
to eight times the wavefunction cutoff.

Results
-------

course_Si
~~~~~~~~~

- cutoff: ecutwfc=30 Ry, k=4x4x4, energy=-16.91076906 Ry.
- cutoff: ecutwfc=50 Ry, k=4x4x4, energy=-16.91101110 Ry.
- cutoff: ecutwfc=70 Ry, k=4x4x4, energy=-16.91102440 Ry.
- kpoints: ecutwfc=70 Ry, k=2x2x2, energy=-16.73677386 Ry.
- kpoints: ecutwfc=70 Ry, k=4x4x4, energy=-16.91102440 Ry.
- kpoints: ecutwfc=70 Ry, k=6x6x6, energy=-16.92311814 Ry.

- Energy difference, 50-70 Ry: 0.0905 meV/atom.
- Energy difference, k=4 to k=6: 82.2719 meV/atom.

alternative_PBE_PAW
~~~~~~~~~~~~~~~~~~~

- cutoff: ecutwfc=30 Ry, k=4x4x4, energy=-93.43892062 Ry.
- cutoff: ecutwfc=50 Ry, k=4x4x4, energy=-93.43971276 Ry.
- cutoff: ecutwfc=70 Ry, k=4x4x4, energy=-93.43973980 Ry.
- kpoints: ecutwfc=70 Ry, k=2x2x2, energy=-93.26568279 Ry.
- kpoints: ecutwfc=70 Ry, k=4x4x4, energy=-93.43973980 Ry.
- kpoints: ecutwfc=70 Ry, k=6x6x6, energy=-93.45180863 Ry.

- Energy difference, 50-70 Ry: 0.1839 meV/atom.
- Energy difference, k=4 to k=6: 82.1024 meV/atom.

Discussion
----------
Both pseudopotentials showed decreasing energy changes
as the wavefunction cutoff increased.

However, the energy differences between 4x4x4 and 6x6x6
k-point meshes were still substantial. Therefore,
k-point convergence was not established in this scan.

Different pseudopotentials have different absolute
total-energy references. Their raw total energies
must not be interpreted as a direct accuracy ranking.

This study is a preliminary convergence comparison.
A denser k-point scan is required before selecting
fully converged production parameters.

Reproducibility
---------------
The complete numerical results are stored in results.csv.
Individual Quantum ESPRESSO input and output files
are retained in pseudopotential-specific directories.
The original calculation workflow is run_convergence.py.

Extended K-point Convergence
----------------------------

Additional k-point meshes were tested at 70 Ry.
The energy differences below are relative to the
previously tested k-point mesh and are expressed
in meV per atom.

course_Si:

- 8x8x8: E = -16.92459923 Ry, delta = 10.0756 meV/atom.
- 10x10x10: E = -16.92483327 Ry, delta = 1.5921 meV/atom.
- 12x12x12: E = -16.92487625 Ry, delta = 0.2924 meV/atom.
- 16x16x16: E = -16.92488690 Ry, delta = 0.0725 meV/atom.

alternative_PBE_PAW:

- 8x8x8: E = -93.45328451 Ry, delta = 10.0402 meV/atom.
- 10x10x10: E = -93.45351730 Ry, delta = 1.5836 meV/atom.
- 12x12x12: E = -93.45355993 Ry, delta = 0.2900 meV/atom.
- 16x16x16: E = -93.45357049 Ry, delta = 0.0718 meV/atom.

For both pseudopotentials, the energy difference
between successive sampled meshes fell below
1 meV/atom at 12x12x12.
At 16x16x16, the difference was approximately
0.07 meV/atom.

These results support the use of a 16x16x16
k-point mesh at 70 Ry for the tested system.
No denser-mesh verification was performed.

The additional calculations are documented in
extended_kpoints.csv and extended_kpoints.log.
