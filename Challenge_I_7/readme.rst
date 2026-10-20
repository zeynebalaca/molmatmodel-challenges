Challenge I.7 - Methane Geometry Optimization with Quantum ESPRESSO
===================================================================

Objective
---------
Optimize the molecular geometry of methane (CH4) using
Quantum ESPRESSO and evaluate its C-H bond lengths and H-C-H angles.

Computational Method
--------------------
Software: Quantum ESPRESSO 7.5.
Exchange-correlation functional: PBE.
Plane-wave kinetic-energy cutoff: 50 Ry.
Charge-density cutoff: 400 Ry.
Simulation cell: cubic, approximately 15 Angstrom.
Brillouin-zone sampling: Gamma point.
Geometry optimization: BFGS.
Parallel execution: four MPI processes.

Results
-------
- Final total energy: -16.7915086849 Ry
- Mean C-H bond length: 1.094828 Angstrom
- Minimum C-H bond length: 1.094787 Angstrom
- Maximum C-H bond length: 1.094848 Angstrom
- Mean H-C-H bond angle: 109.4712 degrees
- Minimum H-C-H bond angle: 109.4684 degrees
- Maximum H-C-H bond angle: 109.4741 degrees
- Geometry optimization: converged in 2 BFGS steps.

Discussion
----------
The optimized methane geometry is compared with the expected
tetrahedral structure, which has an ideal bond angle of
approximately 109.47 degrees. These results are specific to
the chosen PBE pseudopotentials, plane-wave cutoffs and cell size.
Systematic convergence tests were not performed in this challenge.

Reproducibility
---------------
Input: CH4_relax.in
Output: CH4_relax.out
Analysis: analyze_CH4.py
Pseudopotentials: C.upf and H.upf
