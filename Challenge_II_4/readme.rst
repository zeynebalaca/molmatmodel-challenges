Challenge II.4 - Electronic Properties of Silicon
=================================================

Objective
---------
Investigate silicon charge density, Lowdin partial charges,
total density of states (TDOS), projected density of states
(PDOS), and the effect of Gaussian DOS broadening.

Computational Method
--------------------
Quantum ESPRESSO was used through ASE for SCF and NSCF
calculations of crystalline silicon.

Wavefunction cutoff: 65 Ry.
SCF k-point mesh: 8x8x8.
NSCF k-point mesh: 12x12x12.
Baseline electronic smearing: degauss = 0.01 Ry.

Charge density was obtained with pp.x.
Lowdin population analysis and PDOS were obtained with projwfc.x.
TDOS was obtained with dos.x.

DOS broadening was compared at 0.005, 0.010, and 0.020 Ry
using the SAME previously computed NSCF electronic states.
The SCF and NSCF calculations were not repeated for each
broadening value.

Results
-------
- Fermi energy: 6.3118 eV
- Spilling parameter: 0.008900
- Integrated TDOS: 7.9999 states
- Integrated summed PDOS: 7.9290 states
- Integrated TDOS-PDOS relative difference: 0.89 percent
- Maximum pointwise TDOS-PDOS difference: 2.54 percent
- Charge density: charge_density.cube
- Lowdin population analysis: lowdin.out
- Broadening comparison: dos_broadening_comparison.png

Discussion
----------
The low spilling parameter and small integrated TDOS-PDOS
difference indicate good projection quality for the
occupied electronic states examined.

Gaussian broadening affects the smoothness and apparent
width of spectral features in the DOS.

The plotted comparison isolates the DOS post-processing
broadening effect. It does not establish how changing SCF
smearing would affect the self-consistent charge density.

A DOS plot based on finite k-point sampling and Gaussian
broadening is not sufficient by itself to determine a
precise indirect silicon band gap.

Semilocal DFT methods commonly underestimate experimental
semiconductor band gaps. Reliable gap evaluation also
requires adequate Brillouin-zone sampling and appropriate
band-edge analysis.

The results use reduced k-point meshes for computational
efficiency and are not presented as fully converged
production electronic-structure calculations.

Reproducibility
---------------
The original ASE workflow, charge density, Lowdin results,
TDOS and PDOS data are stored in baseline/.
The DOS-broadening data and logs are also retained there.
The comparison plot is dos_broadening_comparison.png.
The summary table is broadening_results.csv.
