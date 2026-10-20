Challenge II.6 - Graphene: 2D Convergence, Relaxation and Electronic Properties
===============================================================================

Objective
---------
Study graphene as a two-dimensional material using
Quantum ESPRESSO and ASE-style workflows.
The tasks included convergence testing, constrained
cell relaxation and electronic-structure analysis.

Method
------
A single graphene layer was constructed with a vacuum
spacing of 15 Angstrom along z and with
``assume_isolated = '2D'`` in the electronic workflow.

Convergence tests were performed for three wavefunction
cutoffs and several 2D k-point meshes.
A constrained cell relaxation was then carried out,
allowing only in-plane lattice relaxation.
Electronic properties were analyzed using SCF, NSCF,
DOS, projected DOS and charge-density post-processing.

Convergence Results
-------------------
Wavefunction cutoff scan at 12x12x1:
- 40 Ry: -24.00590210 Ry
- 55 Ry: -24.08273339 Ry
- 70 Ry: -24.09391003 Ry

K-point scan at 70 Ry:
- 6x6x1:  -24.09066159 Ry
- 12x12x1: -24.09391003 Ry
- 18x18x1: -24.09421340 Ry
- 20x20x1: -24.09432343 Ry
- 24x24x1: -24.09427867 Ry

The total energy stabilized as the in-plane k-point
mesh increased. For graphene, meshes divisible by three
are physically preferred because they sample the K point
properly.

Relaxed Geometry
----------------
The constrained QE relaxation converged successfully.

Final lattice vectors:
- a1 = ( 2.466425429,  0.000000000, 0.000000000 ) Angstrom
- a2 = (-1.233212714,  2.135987078, 0.000000000 ) Angstrom
- a3 = ( 0.000000000,  0.000000000, 15.000000000 ) Angstrom

Final atomic positions:
- C1 = (0.0000000000, -0.0000000000, 7.5000000000) Angstrom
- C2 = (0.0000000000,  1.4239913852, 7.5000000000) Angstrom

This gives a C-C bond length of approximately
1.42399 Angstrom.

Electronic-Structure Results
----------------------------
- Fermi energy: -4.2409 eV
- Spilling parameter: 0.0109
- TDOS file: electronic/graphene_tdos.dat
- PDOS total file: electronic/graphene_pdos.pdos_tot
- Charge density: electronic/charge_density.cube

Orbital Analysis Near the Fermi Level
-------------------------------------
Integrated carbon p-orbital contributions within
E_F +/- 1 eV:

Graphene:
- pz: 0.058815 states (100.00%)
- px: 0.000000 states (0.00%)
- py: 0.000000 states (0.00%)

Silicon:
- pz: 0.048108 states (33.33%)
- px: 0.048108 states (33.33%)
- py: 0.048108 states (33.33%)

Discussion
----------
For graphene, the states near the Fermi level are
entirely dominated by the out-of-plane pz orbital.
This is the expected signature of the pi and pi-star
electronic states that form the Dirac-cone physics.

In contrast, silicon does not show an isolated pz-only
dominance near the Fermi level. Its bonding is three-
dimensional and sp3-like, so the p contributions are
distributed more isotropically.

Therefore, the graphene PDOS confirms the expected
two-dimensional electronic character, whereas silicon
shows a very different bonding and orbital picture.

Outputs
-------
- graphene_p_orbitals.png
- graphene_tdos.png
- graphene_vs_si_p_orbitals.png
- graphene_vs_si_tdos.png
- electronic/charge_density.cube
- electronic/lowdin.out
- electronic/graphene_tdos.dat
- electronic/graphene_pdos.pdos_tot

Reproducibility
---------------
The convergence calculations are stored in results.csv.
The relaxation outputs are stored under cell_relax/.
The electronic-structure outputs are stored under
electronic/.


Graphene DOS: k-point grid comparison
-------------------------------------

The total electronic density of states (DOS) of graphene was
calculated using four k-point grids: 12x12x1, 18x18x1,
20x20x1 and 24x24x1.

For the first three grids, separate Quantum ESPRESSO SCF,
NSCF and DOS calculations were completed. The previously
calculated 24x24x1 DOS was used as an additional reference.

The calculations use the same graphene geometry and
electronic-structure settings apart from the k-point grids.

The resulting DOS curves are compared over the full
energy range and in a narrower energy window.

The comparison is intended to illustrate the effect of
Brillouin-zone sampling on the computed DOS, especially
near the Fermi level.

See DOS_kgrid_comparison/graphene_DOS_kgrid_comparison.png
and DOS_kgrid_comparison/DOS_kgrid_summary.csv.

The results are subject to the chosen smearing and
computational parameters and are not presented as a
fully converged reference DOS.
