Challenge II.8 - Hydrogen Adsorption on Graphene
================================================

Objective
---------
Investigate the adsorption of one hydrogen atom on periodic
graphene supercells containing 8 and 18 carbon atoms.
Assess the influence of wavefunction cutoff and supercell size.

Computational Method
--------------------
Quantum ESPRESSO plane-wave DFT calculations were performed
through ASE, using the supplied C and H pseudopotentials.
The original course geometry files were used to initialize
the C8, H@C8 and C18 configurations.

Spin-polarized calculations were employed, with the
DFT-D3 dispersion correction and a 1x1x1 k-point grid.
The charge-density cutoffs were set to eight times
the corresponding wavefunction cutoffs.

Atomic positions of clean slabs and hydrogen-adsorbed
slabs were optimized with BFGS, using a maximum force
criterion of 0.01 eV/Angstrom.
The isolated H atom was evaluated separately by SCF.

The positive binding-energy convention was:

E_binding = E(clean slab) + E(H) - E(H on slab).

Results
-------
- H@C8 at 80 Ry: 2.86389992 eV
- H@C8 at 100 Ry: 2.86385284 eV
- H@C18 at 100 Ry: 3.58213147 eV

- Binding-energy change from 80 to 100 Ry for C8: -0.00004708 eV
- Binding-energy change from C8 to C18 at 100 Ry: 0.71827863 eV

Optimized Bond Distances
------------------------
- H@C8 at 100 Ry: nearest C-H distance = 1.10165 Angstrom
- H@C18 at 100 Ry: nearest C-H distance = 1.11112 Angstrom

Discussion
----------
The binding energies at 80 and 100 Ry are nearly
identical for the C8 system, suggesting limited
wavefunction-cutoff sensitivity over this tested interval.

Increasing the graphene supercell from C8 to C18
changes the calculated binding energy significantly.
This indicates an important supercell-size effect.
Neither a complete k-point convergence test nor a
supercell-size extrapolation was performed.

The initial adsorption geometry used one H atom
placed 1.20 Angstrom above a carbon site.
The optimized H@C18 calculation represents one
local adsorption configuration, not a systematic
search over every possible adsorption site.

The agreement of the C8/80 Ry binding energy with
the course reference is a numerical reproduction
of that calculation, not experimental validation.

Outputs
-------
- adsorption_summary.csv: binding-energy comparison
- adsorption_energy_comparison.png: summary plot
- binding_energy_80Ry.json: C8 at 80 Ry
- cutoff_100Ry/: C8 and H calculations at 100 Ry
- C18_100Ry/: C18 and H@C18 structures and results
- run_adsorption.py: baseline calculation script
- run_adsorption_100Ry.py: cutoff comparison
- run_c18_adsorption.py: enlarged-supercell study


Hg adsorption on C18: three-site comparison
-------------------------------------------

The course challenge requests Hg adsorption calculations at three
different C18 sites: on-top, on-bridge and on-hollow.

Quantum ESPRESSO calculations used a plane-wave cutoff of 80 Ry,
a 1x1x1 k-point grid and DFT-D3 dispersion corrections.

For a consistent site-specific comparison, the carbon slab was held
fixed and the Hg lateral coordinates were constrained. The Hg vertical
position was optimized with BFGS to a constrained maximum force below
0.01 eV/Angstrom.

Adsorption energy was calculated as:

    E_ads = E(Hg@C18) - E(C18) - E(Hg)

The resulting adsorption energies are:

* On-top:   -0.237229 eV
* On-bridge: -0.237522 eV
* On-hollow: -0.239897 eV

All three constrained calculations met the specified force criterion.
The hollow site gave the lowest calculated energy under these
constraints, but the energy differences are small.

These results are constrained site optimizations, not fully relaxed
unconstrained site minima. An earlier unconstrained bridge-start
calculation did not meet the force convergence criterion and is
not used as a converged adsorption result.

See Hg_on_C18_constrained/adsorption_site_comparison.csv and
Hg_on_C18_constrained/adsorption_site_comparison.png.
