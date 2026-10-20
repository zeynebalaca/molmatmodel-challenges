import csv
import os
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path.cwd()
SOURCE = Path.home() / "Molecular-and-Materials-Modeling-2026-August"
ALTERNATIVE = Path.home() / "MatScProjects/Materials_Modeling_School/Aug2025"

potentials = {
    "course_Si": SOURCE / "materials-modeling/Si.upf",
    "alternative_PBE_PAW": ALTERNATIVE / "Si.pbe-nl-kjpaw_psl.1.0.0.UPF",
}

for name, path in potentials.items():
    if not path.is_file():
        raise FileNotFoundError(f"{name}: {path}")

original = (SOURCE / "materials-modeling/1_Energy_Calculation/Si.in").read_text()

results = []
env = os.environ.copy()
env["OMP_NUM_THREADS"] = "1"
env["OPENBLAS_NUM_THREADS"] = "1"

tests = (
    [("cutoff", e, 4) for e in (30, 50, 70)]
    + [("kpoints", 70, k) for k in (2, 4, 6)]
)

for potential_name, potential_path in potentials.items():
    for test_type, cutoff, k in tests:
        folder = ROOT / potential_name / f"{test_type}_{cutoff}Ry_k{k}"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "tmp").mkdir(exist_ok=True)

        shutil.copy2(potential_path, folder / "Si.upf")

        content = re.sub(
            r"ecutwfc\s*=\s*[\d.]+",
            f"ecutwfc = {cutoff}",
            original,
            count=1
        )

        content = re.sub(
            r"pseudo_dir\s*=\s*'[^']*'",
            "pseudo_dir = './'",
            content
        )

        content = content.replace(
            "calculation      = 'scf'",
            "calculation = 'scf'\n   outdir = './tmp'"
        )

        content = re.sub(
            r"K_POINTS automatic\s*\n\s*\d+\s+\d+\s+\d+\s+0\s+0\s+0",
            f"K_POINTS automatic\n{k} {k} {k} 0 0 0",
            content
        )

        content = re.sub(
            r"(ecutwfc\s*=\s*\d+)",
            rf"\1\n   ecutrho = {cutoff * 8}",
            content,
            count=1
        )

        (folder / "Si.in").write_text(content)

        print(
            f"Running {potential_name} | {test_type} | "
            f"ecut={cutoff} Ry | k={k}x{k}x{k}",
            flush=True
        )

        with (folder / "Si.out").open("w") as log:
            try:
                proc = subprocess.run(
                    ["mpirun", "--use-hwthread-cpus", "-np", "4",
                     "pw.x", "-in", "Si.in"],
                    cwd=folder,
                    env=env,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    timeout=600
                )
                status = proc.returncode
            except subprocess.TimeoutExpired:
                status = 124

        output = (folder / "Si.out").read_text(errors="replace")

        matches = re.findall(
            r"!\s+total energy\s*=\s*([-\d.]+)\s*Ry",
            output
        )

        energy = float(matches[-1]) if matches else None
        success = (
            status == 0
            and "JOB DONE." in output
            and energy is not None
        )

        result = {
            "pseudopotential": potential_name,
            "test": test_type,
            "ecutwfc_Ry": cutoff,
            "k_grid": k,
            "energy_Ry": energy,
            "energy_eV": energy * 13.605693122994 if energy is not None else None,
            "success": success,
            "exit_code": status,
        }

        results.append(result)
        print(
            f"  Energy: {energy} Ry | success={success}",
            flush=True
        )

        with (ROOT / "results.csv").open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(result))
            writer.writeheader()
            writer.writerows(results)

print("\n========== FINAL RESULTS ==========")
for r in results:
    print(
        f"{r['pseudopotential']:22s} "
        f"{r['test']:8s} "
        f"ecut={r['ecutwfc_Ry']:3d} "
        f"k={r['k_grid']:2d} "
        f"E={str(r['energy_Ry']):>15s} Ry "
        f"success={r['success']}"
    )

print("\nSaved results.csv and individual QE inputs/outputs.")
