import csv
import os
import re
import shutil
import subprocess
from pathlib import Path

root = Path.cwd()
source = root / "kpoints_14"

with (root / "results.csv").open() as f:
    original = list(csv.DictReader(f))

previous = float(next(
    r["energy_Ry"] for r in original
    if r["test"] == "kpoints_14"
))

env = os.environ.copy()
env["OMP_NUM_THREADS"] = "1"
env["OPENBLAS_NUM_THREADS"] = "1"

results = []

for k in (18, 22, 26):
    folder = root / f"kpoints_{k}"
    folder.mkdir(exist_ok=True)
    (folder / "tmp").mkdir(exist_ok=True)

    shutil.copy2(source / "Al.upf", folder / "Al.upf")

    text = (source / "Al.in").read_text()
    text = re.sub(
        r"(K_POINTS automatic\s*\n)\s*\d+\s+\d+\s+\d+\s+0\s+0\s+0",
        rf"\g<1>{k} {k} {k} 0 0 0",
        text
    )
    (folder / "Al.in").write_text(text)

    print(f"\nRunning {k}x{k}x{k} k-points...", flush=True)

    with (folder / "Al.out").open("w") as log:
        try:
            proc = subprocess.run(
                ["mpirun", "--use-hwthread-cpus", "-np", "4",
                 "pw.x", "-in", "Al.in"],
                cwd=folder,
                env=env,
                stdout=log,
                stderr=subprocess.STDOUT,
                timeout=600
            )
            status = proc.returncode
        except subprocess.TimeoutExpired:
            status = 124

    output = (folder / "Al.out").read_text(errors="replace")
    values = re.findall(
        r"!\s+total energy\s*=\s*([-\d.]+)\s*Ry",
        output
    )

    energy = float(values[-1]) if values else None
    success = (
        status == 0
        and "JOB DONE." in output
        and "convergence has been achieved" in output
        and energy is not None
    )

    delta = (
        abs(energy - previous) * 13605.693122994
        if success else None
    )

    results.append({
        "k_grid": k,
        "ecutwfc_Ry": 70,
        "energy_Ry": energy,
        "delta_meV_atom": delta,
        "success": success
    })

    with (root / "extended_kpoints.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)

    print(f"Energy: {energy} Ry")
    print(f"Difference: {delta} meV/atom")
    print(f"Success: {success}", flush=True)

    if success:
        previous = energy

print("\nExtended Al k-point scan finished.")
print("Results saved to extended_kpoints.csv")
