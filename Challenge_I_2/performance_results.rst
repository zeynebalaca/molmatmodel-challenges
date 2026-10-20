Performance Benchmark Results
=============================

Objective
---------
Measure the computational performance of MOPAC, NWChem and Quantum ESPRESSO on a local WSL2 Ubuntu system and compare selected results with the course reference runs.

Environment
-----------
- Platform: Ubuntu under WSL2, with 4 physical and 8 logical CPU cores detected.
- Conda environment: molmatmodel (Python 3.11).
- Quantum ESPRESSO: PWSCF 7.5.
- MPI: Open MPI 5.0.11.
- Each benchmark configuration was measured once; timings may vary between runs.

MOPAC: Mini-DNA PM7 Single-Point Calculation
---------------------------------------------
System: C40H50N14O26P4 (134 atoms). Method: PM7, NOOPT.

============== ============== ========================
OpenMP threads Wall time (s)  Heat of formation (kcal/mol)
============== ============== ========================
2              17.02          -807.20255
4              17.28          -807.36647
6              15.23          -807.35008
============== ============== ========================

All calculations ended normally. Six threads gave the shortest wall time in this set of single measurements. The maximum variation in heat of formation was 0.16392 kcal/mol.

NWChem: CH3 Radical
-------------------
Calculation: spin-doublet CH3 radical, B3LYP/6-311G with ZORA, followed by magnetic property calculations.

============= ============= =====================
MPI processes Wall time (s) Final DFT energy (Ha)
============= ============= =====================
2             8.30          -39.853430540821
4             6.50          -39.853430540822
6             5.00          -39.853430540826
============= ============= =====================

All three calculations completed successfully, and their final DFT energies agreed within 5e-12 Ha. Reference course times were 12.40, 10.20 and 9.30 s for 2, 4 and 6 MPI processes, respectively. Six MPI processes required Open MPI's --use-hwthread-cpus option in this WSL2 environment. Each run used a separate working directory.

Quantum ESPRESSO: Bulk Thallium
-------------------------------
Calculation: 2-atom HCP Tl cell, spin-orbit-coupled noncollinear DFT, 40 Ry wavefunction cutoff and 8x8x8 k-point sampling.

=========== ============= ================= ==============
MPI x OMP   Wall time (s) Total energy (Ry) SCF iterations
=========== ============= ================= ==============
2 x 1       17.22         -242.12772581     6
4 x 1       10.82         -242.12772581     6
8 x 1       7.24          -242.12772581     6
=========== ============= ================= ==============

All three calculations reached SCF convergence and finished with JOB DONE. The energies agree at the precision printed by Quantum ESPRESSO. Eight MPI processes gave the shortest wall time among the tested configurations, with a 2.38x speedup relative to two MPI processes.

Discussion
----------
For the tested configurations, increasing parallelism improved NWChem and Quantum ESPRESSO wall times, while MOPAC showed a smaller and nonmonotonic response. These are single-run measurements rather than statistically averaged performance results. Comparisons with the instructor's reference timings should be interpreted cautiously because the hardware and software environments differ.
