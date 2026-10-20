Challenge I.5 - Oxygen Molecule Thermochemistry
================================================

Objective
---------
Adapt the original N2 thermochemistry example to O2.

Method
------
ASE with the EMT calculator was used for O2 geometry optimization,
finite-difference vibrations and ideal-gas thermochemistry.
The electronic spin was set to 1 (triplet oxygen) and the
rotational symmetry number to 2.
Temperature: 298.15 K. Pressure: 101325.0 Pa.

Results
-------
- Optimization converged: True
- Optimized O-O bond length: 1.100464 Angstrom
- Potential energy: 0.624750 eV
- Enthalpy H: 0.782058 eV
- Entropy S: 0.002111047 eV/K
- Gibbs energy G = H - TS: 0.152649 eV

Discussion
----------
These are model-dependent thermochemical estimates.
The calculated enthalpy is not the standard enthalpy of formation.
EMT is a simplified empirical potential and may not accurately
describe the electronic structure and vibrations of triplet O2.
Original N2 input and calculation logs are retained.
