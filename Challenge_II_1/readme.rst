Challenge II.1 - Silicon Total Energy Calculations
==================================================

Objective
---------
Calculate the total energy of crystalline silicon using
Quantum ESPRESSO directly and through ASE. Investigate
the effect of the plane-wave energy cutoff.

Computational Method
--------------------
The course silicon structure contains two Si atoms in
a primitive unit cell.

Quantum ESPRESSO was used for self-consistent field calculations.
The Brillouin zone was sampled using a 2x2x2 k-point mesh.
Gaussian smearing was used with degauss = 0.01 Ry.
The SCF convergence threshold was 1e-10.
The supplied Si.upf pseudopotential was used.

Energy cutoff values of 30, 50 and 70 Ry were investigated.
An additional calculation was performed through ASE at 30 Ry.

Results
-------
- QE, 30 Ry: -16.73649696 Ry
- QE, 50 Ry: -16.73675970 Ry
- QE, 70 Ry: -16.73677386 Ry
- ASE + QE, 30 Ry: -227.711622 eV
- Direct QE, 30 Ry converted to eV: -227.711642 eV
- Absolute ASE-QE difference at 30 Ry: 0.00001959 eV
- Absolute energy change from 30 to 70 Ry: 0.00027690 Ry

Discussion
----------
All four calculations completed successfully.

The total energy changed only slightly when the cutoff was
increased from 50 to 70 Ry. This indicates improving energy
convergence for the specified structure and k-point mesh.

The ASE-driven and directly executed QE calculations gave
consistent total energies within the precision reported.

The cutoff comparison does not constitute a complete convergence
study of all computational parameters.

Alternative silicon pseudopotentials are available in the
local MatScProjects collection, including Si.pz-vbc.UPF and
Si.pbe-nl-kjpaw_psl.1.0.0.UPF. These alternatives have not
yet been used in the calculations reported here. Different
pseudopotentials can have different total-energy reference
values and should be compared with appropriate validation tests.

Reproducibility
---------------
- run_challenge.py: calculation automation
- QE_30Ry/: direct QE calculation at 30 Ry
- QE_50Ry/: direct QE calculation at 50 Ry
- QE_70Ry/: direct QE calculation at 70 Ry
- ASE_30Ry/: ASE-driven calculation at 30 Ry
- challenge_II_1.log: execution summary
