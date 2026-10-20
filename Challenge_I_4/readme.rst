Challenge I.4 - MACE Examples and Verification
==============================================

Objective
---------
Execute and document the course MACE examples using ASE.

Environment and Method
----------------------
Calculations were executed in the molmatmodel Conda environment
under WSL2 Ubuntu using CPU-based MACE models and ASE.
OpenMP threads were limited to two.

Executed Scripts
----------------

- ``tests/quick_test.py``: log saved.
- ``tests/model_analyzer.py``: log saved.
- ``tests/model_element_detector.py``: log saved.
- ``tests/check_mace_ml_installation.py``: log saved.
- ``simple/water_mace.py``: log saved.
- ``simple/water_mace_emt_01.py``: log saved.

Results
-------
The MACE quick test evaluated H2O, CH4, NH3, CO2, C6H6 and N2.
The water geometry optimization produced an O-H bond length
of 0.9728 Angstrom and a potential energy of -14.1603 eV.

In the water comparison, the mean absolute bond-length errors
were 0.0156 Angstrom (MACE) and 0.1421 Angstrom (EMT).
The bond-angle errors were 0.43 degrees (MACE) and
7.38 degrees (EMT).

Discussion
----------
Both water example scripts exited successfully.
The four installation/model test scripts also exited with code 0.
MACE gave more accurate water geometry than EMT in this example.
The model analyzer's detailed analysis status was not independently
verified beyond successful process termination.
A CUDA driver warning was observed, but CPU calculations succeeded.
Original scripts and individual output logs are retained.
