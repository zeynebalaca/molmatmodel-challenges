Challenge I.1 - Basic Software Functionality Tests
==================================================

Task
----
Run the basic software functionality test scripts independently.

Files
-----
* ``ase_tests-pyscf_mopac.py`` - H2O energy calculations with PySCF and MOPAC.
* ``ase_tests-pyscf-mopac-xtb-crest-nwchem-qe.py`` - Six software functionality checks.
* ``ase-test2.py`` - PySCF and MOPAC calculations for H2O and CH4.
* ``*.py.log`` - Saved output from each test script.
* ``*_logfileSAVED`` - Reference outputs provided with the course.
* ``qe/`` - Original course input files for Quantum ESPRESSO.

Method
------
Calculations were run under Ubuntu WSL2 using the ``molmatmodel`` Conda environment, with ASE 3.29.0 and PySCF 2.14.0. The original scripts were run without modification. PySCF used RHF/6-31G, MOPAC used PM7, and xTB used GFN2-xTB.

Results
-------
All three Python scripts completed. The PySCF, MOPAC and xTB values agree with the available course reference logs to the displayed precision.

::

   H2O PySCF (RHF/6-31G):  -2067.6141 eV
   H2O MOPAC (PM7):           -2.5019 eV
   H2O xTB (GFN2-xTB):      -137.9678 eV
   CH4 PySCF (RHF/6-31G):  -1093.3644 eV
   CH4 MOPAC (PM7):           -0.6235 eV

CREST reported a successful version check. NWChem and Quantum ESPRESSO produced successful binary-check messages; those messages alone do not establish convergence of a physical calculation.

Discussion
----------
The tests confirm that the main molecular modeling tools can be invoked in the installed environment. PySCF total energies and MOPAC heats of formation use different energy conventions and must not be compared directly. Additional DFT calculations are required to verify full NWChem and Quantum ESPRESSO functionality.
