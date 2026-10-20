Challenge I.3 - Atomization Energies of Diatomic Molecules
==========================================================

Objective
---------
Extend the course N2 atomization-energy example to O2, F2, and H2.

Method
------
ASE geometry optimization using the pretrained MACE-MP medium model on CPU.
The atomization energy is E_atomization = 2*E_atom - E_molecule.
BFGS convergence criterion: maximum force below 0.05 eV/Angstrom.

Results
-------

- O2: bond length 1.23606 Angstrom; atomization energy 5.52635 eV; reference approximately 5.17 eV; converged: True.
- F2: bond length 1.45326 Angstrom; atomization energy -0.58251 eV; reference approximately 1.6 eV; converged: True.
- H2: bond length 0.74783 Angstrom; atomization energy 4.20651 eV; reference approximately 4.52 eV; converged: True.

Discussion
----------
The computed values are model predictions and may differ from experimental dissociation energies. Spin states and isolated-atom reference energies require care for quantitative benchmarking. See results.csv and calculate_diatomics.log for full records.

Model Limitation
----------------
The F2 calculation converged geometrically but predicted a negative atomization energy (-0.58251 eV), whereas the approximate experimental reference is +1.60 eV. This is a significant failure of the selected pretrained MACE potential for the F2 dissociation-energy benchmark. The result is retained without alteration.
