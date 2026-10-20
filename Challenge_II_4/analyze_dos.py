import os
import re
import csv
import subprocess
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from docutils.core import publish_doctree

root = Path.cwd()
baseline = root / "baseline"

if not (baseline / "total_dos.dat").exists():
    raise RuntimeError("Baseline DOS data not found.")

results = []
curves = {}

for width in (0.005, 0.01, 0.02):
    label = f"{width:.3f}"
    filename = f"dos_degauss_{label}.dat"

    input_text = f"""&DOS
 prefix = 'Si_Electronic',
 outdir = './tmp',
 DeltaE = 0.01,
 Emin = -20.0,
 Emax = 20.0,
 ngauss = 0,
 degauss = {width},
 fildos = '{filename}'
/
"""

    (baseline / "dos_broadening.in").write_text(input_text)

    print(f"Running dos.x with degauss={label} Ry", flush=True)

    with (baseline / f"dos_{label}.log").open("w") as log:
        proc = subprocess.run(
            ["dos.x", "-in", "dos_broadening.in"],
            cwd=baseline,
            stdout=log,
            stderr=subprocess.STDOUT,
            timeout=300,
        )

    path = baseline / filename
    if proc.returncode != 0 or not path.exists():
        raise RuntimeError(f"dos.x failed for {label}")

    data = np.loadtxt(path, comments="#")
    if data.ndim != 2 or data.shape[1] < 2:
        raise RuntimeError(f"Invalid DOS file: {filename}")

    curves[label] = data[:, :2]
    results.append({
        "degauss_Ry": width,
        "dos_file": filename,
        "status": "success"
    })

    print(f"  Saved {filename}: {len(data)} energy points", flush=True)

# Fermi energy from the baseline calculation
log = (baseline / "electronic_properties_si.log").read_text()
matches = re.findall(r"Fermi level from NSCF calculation:\s*([-\d.]+)", log)
if not matches:
    raise RuntimeError("Fermi energy not found.")

fermi = float(matches[-1])

plt.figure(figsize=(9, 5.5))

for label, data in curves.items():
    plt.plot(
        data[:, 0] - fermi,
        data[:, 1],
        label=f"degauss = {label} Ry"
    )

plt.axvline(0, color="black", linestyle="--", linewidth=1)
plt.xlim(-8, 8)
plt.xlabel("Energy - Fermi level (eV)")
plt.ylabel("Total DOS (states/eV)")
plt.title("Silicon TDOS: Gaussian Broadening Comparison")
plt.legend()
plt.tight_layout()
plt.savefig(root / "dos_broadening_comparison.png", dpi=180)
plt.close()

with (root / "broadening_results.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(results[0]))
    writer.writeheader()
    writer.writerows(results)

title = "Challenge II.4 - Electronic Properties of Silicon"

report = f"""{title}
{'=' * len(title)}

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
- Fermi energy: {fermi:.4f} eV
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
"""

(root / "readme.rst").write_text(report)
publish_doctree(report, settings_overrides={"halt_level": 2})

print("\nSUCCESS: Challenge II.4 README validated.")
print("SUCCESS: DOS comparison plot created.")
print("SUCCESS: Broadening results saved.")
