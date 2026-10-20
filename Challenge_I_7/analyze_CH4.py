import re
import numpy as np
from itertools import combinations
from pathlib import Path
from docutils.core import publish_doctree

output = Path("CH4_relax.out").read_text()

if "JOB DONE." not in output or "bfgs converged" not in output:
    raise RuntimeError("QE calculation did not finish successfully.")

blocks = re.findall(
    r"Begin final coordinates.*?ATOMIC_POSITIONS\s*\(angstrom\)\s*(.*?)\s*End final coordinates",
    output, re.S
)
if not blocks:
    raise RuntimeError("Final atomic coordinates not found.")

lines = [line.split() for line in blocks[-1].strip().splitlines()]
symbols = [line[0] for line in lines]
positions = np.array([[float(x) for x in line[1:4]] for line in lines])

if symbols != ["C", "H", "H", "H", "H"]:
    raise RuntimeError(f"Unexpected atoms: {symbols}")

c = positions[0]
vectors = positions[1:] - c
bonds = np.linalg.norm(vectors, axis=1)

angles = []
for i, j in combinations(range(4), 2):
    cosine = np.dot(vectors[i], vectors[j]) / (bonds[i] * bonds[j])
    angle = np.degrees(np.arccos(np.clip(cosine, -1, 1)))
    angles.append(angle)

energy = re.findall(r"Final energy\s*=\s*([-\d.]+)\s*Ry", output)
if not energy:
    raise RuntimeError("Final energy not found.")
energy = float(energy[-1])

print("===== CH4 GEOMETRY =====")
for i, bond in enumerate(bonds, 1):
    print(f"C-H{i}: {bond:.6f} Angstrom")

for i, angle in enumerate(angles, 1):
    print(f"H-C-H angle {i}: {angle:.4f} degrees")

print(f"Average C-H bond: {np.mean(bonds):.6f} Angstrom")
print(f"Average H-C-H angle: {np.mean(angles):.4f} degrees")
print(f"Final energy: {energy:.10f} Ry")

title = "Challenge I.7 - Methane Geometry Optimization with Quantum ESPRESSO"

report = f"""{title}
{'=' * len(title)}

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
- Final total energy: {energy:.10f} Ry
- Mean C-H bond length: {np.mean(bonds):.6f} Angstrom
- Minimum C-H bond length: {np.min(bonds):.6f} Angstrom
- Maximum C-H bond length: {np.max(bonds):.6f} Angstrom
- Mean H-C-H bond angle: {np.mean(angles):.4f} degrees
- Minimum H-C-H bond angle: {np.min(angles):.4f} degrees
- Maximum H-C-H bond angle: {np.max(angles):.4f} degrees
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
"""

Path("readme.rst").write_text(report)
publish_doctree(report, settings_overrides={"halt_level": 2})

print("\nSUCCESS: Challenge I.7 README validated.")
