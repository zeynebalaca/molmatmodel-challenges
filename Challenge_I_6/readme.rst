Challenge I.6 - Methane C-H Bond Dissociation Energy
====================================================

Objective
---------
Adapt the course ethane C-C bond dissociation example to methane.

Method
------
The reaction CH4 -> CH3 + H was evaluated using ASE.
CH4 and CH3 geometries were optimized with BFGS to a maximum
force tolerance of 0.01 eV/Angstrom.
BDE = E(CH3) + E(H) - E(CH4).
Both EMT and a pretrained MACE-MP medium model were tested.

Results
-------

- EMT: C-H dissociation energy = 3.25386 eV
  (313.95 kJ/mol); CH4 converged:
  True; CH3 converged: True.

- MACE-MP: C-H dissociation energy = 4.31577 eV
  (416.41 kJ/mol); CH4 converged:
  True; CH3 converged: True.

Discussion
----------
The approximate experimental methane C-H bond dissociation
energy is 4.52 eV. The calculated values are
model-dependent electronic energy differences, not
zero-point-corrected thermochemical bond enthalpies.
Neither EMT nor a general-purpose materials MACE potential
guarantees accurate radical or isolated-atom energetics.
See results.csv and methane_CH_bond.log for complete values.
