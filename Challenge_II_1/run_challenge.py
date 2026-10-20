import os
import re
import shutil
import subprocess
from pathlib import Path

root = Path.cwd()
base = (root / "Si.in").read_text()

env = os.environ.copy()
env["OMP_NUM_THREADS"] = "1"
env["OPENBLAS_NUM_THREADS"] = "1"

results = []

def run(command, folder, logname):
    folder.mkdir(exist_ok=True)
    shutil.copy2(root / "Si.upf", folder / "Si.upf")
    with (folder / logname).open("w") as logfile:
        try:
            process = subprocess.run(
                command,
                cwd=folder,
                env=env,
                stdout=logfile,
                stderr=subprocess.STDOUT,
                timeout=600,
            )
            return process.returncode
        except subprocess.TimeoutExpired:
            return 124

for cutoff in [30, 50, 70]:
    folder = root / f"QE_{cutoff}Ry"
    folder.mkdir(exist_ok=True)

    modified = re.sub(
        r"ecutwfc\s*=\s*[\d.]+",
        f"ecutwfc = {cutoff}",
        base,
        count=1,
    )
    modified = modified.replace(
        "pseudo_dir       = '.././'",
        "pseudo_dir       = './'",
    )
    modified = modified.replace(
        "calculation      = 'scf'",
        "calculation      = 'scf'\n   outdir = './tmp'",
    )

    (folder / "Si.in").write_text(modified)
    (folder / "tmp").mkdir(exist_ok=True)

    print(f"\nRunning Quantum ESPRESSO: {cutoff} Ry", flush=True)

    status = run(
        ["mpirun", "--use-hwthread-cpus", "-np", "4",
         "pw.x", "-in", "Si.in"],
        folder,
        "Si.out",
    )

    output = (folder / "Si.out").read_text(errors="replace")
    match = re.findall(
        r"!\s+total energy\s*=\s*([-\d.]+)\s*Ry",
        output,
    )
    energy = float(match[-1]) if match else None
    success = (
        status == 0
        and "JOB DONE." in output
        and "convergence has been achieved" in output
        and energy is not None
    )

    results.append((f"QE {cutoff} Ry", energy, success))
    print(f"Exit code: {status}")
    print(f"Converged: {success}")
    print(f"Total energy: {energy} Ry", flush=True)

print("\nRunning ASE + Quantum ESPRESSO: 30 Ry", flush=True)

ase_folder = root / "ASE_30Ry"
ase_folder.mkdir(exist_ok=True)

script = (root / "si_ase.py").read_text()
script = re.sub(
    r'qe_bin = "/path/to/quantum-espresso/bin"',
    'qe_bin = str(Path.home() / "miniforge3/envs/molmatmodel/bin")',
    script,
)
script = "from pathlib import Path\n" + script
script = script.replace(
    "pw_command = f'mpirun -np 4 {qe_bin}/pw.x'",
    "pw_command = f'mpirun --use-hwthread-cpus -np 4 {qe_bin}/pw.x'",
)

(ase_folder / "si_ase.py").write_text(script)

status = run(
    ["python", "-u", "si_ase.py"],
    ase_folder,
    "si_ase.out",
)

ase_output = (ase_folder / "si_ase.out").read_text(errors="replace")
matches = re.findall(r"Total energy:\s*([-\d.]+)\s*eV", ase_output)
ase_energy = float(matches[-1]) if matches else None

print(f"Exit code: {status}")
print(f"ASE total energy: {ase_energy} eV")

print("\n========== SUMMARY ==========")
for name, energy, success in results:
    print(f"{name}: {energy} Ry | converged={success}")
print(f"ASE 30 Ry: {ase_energy} eV | success={status == 0}")

print("\nCalculation logs saved in separate folders.")
