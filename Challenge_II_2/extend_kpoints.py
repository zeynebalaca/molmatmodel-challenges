import csv
import os
import re
import shutil
import subprocess
from pathlib import Path

root = Path.cwd()
env = os.environ.copy()
env["OMP_NUM_THREADS"] = "1"
env["OPENBLAS_NUM_THREADS"] = "1"

original_rows = list(csv.DictReader(open("results.csv")))
rows = []

for potential in ("course_Si", "alternative_PBE_PAW"):
    previous = next(
        float(r["energy_Ry"])
        for r in original_rows
        if r["pseudopotential"] == potential
        and r["test"] == "kpoints"
        and int(r["k_grid"]) == 6
    )

    source = root / potential / "kpoints_70Ry_k6"

    for k in (8, 10, 12, 16):
        folder = root / potential / f"kpoints_70Ry_k{k}"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "tmp").mkdir(exist_ok=True)

        shutil.copy2(source / "Si.upf", folder / "Si.upf")

        text = (source / "Si.in").read_text()
        text = re.sub(
            r"(K_POINTS automatic\s*\n)\s*\d+\s+\d+\s+\d+\s+0\s+0\s+0",
            rf"\g<1>{k} {k} {k} 0 0 0",
            text
        )
        (folder / "Si.in").write_text(text)

        print(f"Running {potential}: {k}x{k}x{k}", flush=True)

        with (folder / "Si.out").open("w") as log:
            try:
                process = subprocess.run(
                    ["mpirun", "--use-hwthread-cpus", "-np", "4",
                     "pw.x", "-in", "Si.in"],
                    cwd=folder, env=env,
                    stdout=log, stderr=subprocess.STDOUT,
                    timeout=600
                )
                status = process.returncode
            except subprocess.TimeoutExpired:
                status = 124

        output = (folder / "Si.out").read_text(errors="replace")
        values = re.findall(
            r"!\s+total energy\s*=\s*([-\d.]+)\s*Ry",
            output
        )

        success = status == 0 and "JOB DONE." in output and bool(values)
        energy = float(values[-1]) if values else None

        delta = (
            abs(energy - previous) * 13605.693122994 / 2
            if success else None
        )

        rows.append({
            "pseudopotential": potential,
            "k_grid": k,
            "ecutwfc_Ry": 70,
            "energy_Ry": energy,
            "delta_meV_atom": delta,
            "success": success
        })

        print(
            f"Energy: {energy} Ry | "
            f"Delta: {delta} meV/atom | success={success}",
            flush=True
        )

        if success:
            previous = energy

        with open("extended_kpoints.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

print("\nSUCCESS: Extended k-point scan finished.")
print("Results saved to extended_kpoints.csv")
