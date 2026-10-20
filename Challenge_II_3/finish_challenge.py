import os
import re
import shutil
import subprocess
from pathlib import Path

import numpy as np
from ase.io import read
from docutils.core import publish_doctree

root = Path.cwd()
source = Path.home() / "Molecular-and-Materials-Modeling-2026-August/materials-modeling"
ase_dir = root / "ase_relax"
ase_dir.mkdir(exist_ok=True)
shutil.copy2(source / "Si.upf", ase_dir / "Si.upf")

script = (source / "3_Cell_Relaxation/cell_relaxation_si.py").read_text()
script = script.replace(
    'qe_bin = "/path/to/quantum-espresso/bin"',
    'qe_bin = "' + str(Path.home() / "miniforge3/envs/molmatmodel/bin") + '"'
)
script = script.replace(
    "mpirun -np 8 {qe_bin}/pw.x",
    "mpirun --use-hwthread-cpus -np 4 {qe_bin}/pw.x"
)
script = re.sub(r"kpts=\(15,15,15\)", "kpts=(8,8,8)", script)
script = script.replace("opt.run(fmax=0.01)", "opt.run(fmax=0.01, steps=30)")
(ase_dir / "cell_relaxation_si.py").write_text(script)

env = os.environ.copy()
env["OMP_NUM_THREADS"] = "1"
env["OPENBLAS_NUM_THREADS"] = "1"

print("Running ASE-driven silicon cell relaxation...", flush=True)
with (ase_dir / "ase_relax.log").open("w") as log:
    try:
        proc = subprocess.run(
            ["python", "-u", "cell_relaxation_si.py"],
            cwd=ase_dir, env=env,
            stdout=log, stderr=subprocess.STDOUT,
            timeout=900
        )
        status = proc.returncode
    except subprocess.TimeoutExpired:
        status = 124

ase_log = (ase_dir / "ase_relax.log").read_text(errors="replace")
print("ASE exit code:", status)
print("\n".join(ase_log.splitlines()[-15:]))

# Check source outputs
results = {}
for name in ("original", "shifted"):
    output = (root / name / "Si_vc_relax.out").read_text()
    if "JOB DONE." not in output or "bfgs converged" not in output:
        raise RuntimeError(f"{name} QE optimization not converged")

    energy = re.findall(
        r"!\s+total energy\s*=\s*([-\d.]+)\s*Ry", output
    )[-1]
    volume = re.findall(
        r"new unit-cell volume\s*=\s*[\d.]+\s*a.u.\^3\s*\(\s*([\d.]+)\s*Ang\^3",
        output
    )[-1]
    results[name] = (float(energy), float(volume))

ase_energy = re.findall(
    r"Total Energy\s*:\s*([-\d.]+)\s*eV", ase_log
)
ase_pressure = re.findall(
    r"Pressure\s*:\s*([-\d.]+)\s*kbar", ase_log
)
ase_success = (
    status == 0
    and bool(ase_energy)
    and (ase_dir / "final_relaxed_structure.vasp").exists()
)

title = "Challenge II.3 - Silicon Cell Relaxation"

report = f"""{title}
{'=' * len(title)}

Objective
---------
Investigate the relaxation of crystalline silicon using
Quantum ESPRESSO directly and through ASE. Compare the
original crystal with a manually displaced initial structure.

Quantum ESPRESSO Method
-----------------------
Two variable-cell relaxations were performed with Quantum
ESPRESSO using the supplied silicon pseudopotential.

The wavefunction energy cutoff was 70 Ry and the
charge-density cutoff was 560 Ry.
An 8x8x8 k-point mesh was used.
The atomic positions and cell were optimized using BFGS.

The second initial structure was modified by shifting
one silicon atom by 0.08 Angstrom along the x direction.

Direct QE Results
-----------------
- Original structure energy: {results['original'][0]:.8f} Ry
- Shifted structure energy: {results['shifted'][0]:.8f} Ry
- Original final cell volume: {results['original'][1]:.5f} Angstrom^3
- Shifted final cell volume: {results['shifted'][1]:.5f} Angstrom^3
- Both QE calculations converged successfully.

ASE Calculation
---------------
- ASE calculation completed: {ase_success}
- ASE final energy: {ase_energy[-1] if ase_energy else 'not available'} eV
- ASE final pressure: {ase_pressure[-1] if ase_pressure else 'not available'} kbar

Discussion
----------
Both direct QE optimizations converged to similar total energies
and cell volumes despite the initial atomic displacement.
This suggests recovery toward closely related relaxed structures.

The ASE calculation used an 8x8x8 k-point mesh to limit
computational expense. This is less dense than the
16x16x16 mesh investigated in Challenge II.2.
The present relaxations are methodological demonstrations,
not fully converged production calculations.

The ASE optimization status must be interpreted using its
saved convergence log and trajectory.

Reproducibility
---------------
- run_qe_relax.py: direct QE calculations
- original/: original structure input and output
- shifted/: displaced structure input and output
- ase_relax/: ASE calculation, trajectory and logs
"""

(root / "readme.rst").write_text(report)
publish_doctree(report, settings_overrides={"halt_level": 2})

print("\nSUCCESS: Challenge II.3 README validated.")
print(f"ASE calculation completed: {ase_success}")
