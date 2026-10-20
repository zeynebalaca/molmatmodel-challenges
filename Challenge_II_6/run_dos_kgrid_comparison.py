from pathlib import Path
import os
import re
import shutil
import subprocess
import time

root = Path.cwd()
source = root / "electronic"
target = root / "DOS_kgrid_comparison"
target.mkdir(exist_ok=True)

pw = shutil.which("pw.x")
dos = shutil.which("dos.x")

if not pw or not dos:
    raise RuntimeError("pw.x or dos.x not found in PATH")

scf_template = (source / "scf.in").read_text()
nscf_template = (source / "nscf.in").read_text()
dos_template = (source / "dos.in").read_text()

if not (source / "C.upf").exists():
    raise RuntimeError("C.upf not found")

def change_grid(content, n):
    pattern = (
        r"(?im)(K_POINTS\s+automatic\s*\n)"
        r"\s*\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+"
    )
    updated, count = re.subn(
        pattern,
        lambda m: m.group(1) + f"{n} {n} 1 0 0 0",
        content
    )
    if count != 1:
        raise RuntimeError("Could not identify the automatic k-point grid")
    return updated

def change_outdir(content):
    updated, count = re.subn(
        r"(?i)(outdir\s*=\s*)['\"][^'\"]+['\"]",
        r"\1'./tmp'",
        content
    )
    if count != 1:
        raise RuntimeError("Could not identify outdir")
    return updated

env = os.environ.copy()
env["OMP_NUM_THREADS"] = "1"
env["OPENBLAS_NUM_THREADS"] = "1"

for n in (12, 18, 20):
    folder = target / f"k{n}"
    folder.mkdir(exist_ok=True)
    (folder / "tmp").mkdir(exist_ok=True)

    shutil.copy2(source / "C.upf", folder / "C.upf")

    inputs = {
        "scf.in": change_outdir(change_grid(scf_template, n)),
        "nscf.in": change_outdir(change_grid(nscf_template, n)),
        "dos.in": change_outdir(dos_template)
    }

    for name, content in inputs.items():
        (folder / name).write_text(content)

    print(f"\n===== {n}x{n}x1 K-POINT GRID =====", flush=True)

    for stage, program, input_name in [
        ("SCF", pw, "scf.in"),
        ("NSCF", pw, "nscf.in"),
        ("DOS", dos, "dos.in")
    ]:
        print(f"Starting {stage}...", flush=True)
        started = time.time()

        command = [
            "mpirun", "--use-hwthread-cpus", "-np", "4",
            program, "-in", input_name
        ]

        output_file = folder / f"{stage.lower()}.out"

        with output_file.open("w") as output:
            result = subprocess.run(
                command,
                cwd=folder,
                stdout=output,
                stderr=subprocess.STDOUT,
                env=env
            )

        if result.returncode != 0:
            print(output_file.read_text(errors="replace")[-3000:])
            raise RuntimeError(
                f"{n}x{n}x1 {stage} failed; see {output_file}"
            )

        output = output_file.read_text(errors="replace")
        if stage in ("SCF", "NSCF") and "JOB DONE." not in output:
            raise RuntimeError(
                f"{stage} did not finish normally: {output_file}"
            )

        if stage == "DOS":
            data_file = folder / "graphene_tdos.dat"
            if not data_file.exists() or data_file.stat().st_size == 0:
                raise RuntimeError("DOS data file missing or empty")

        print(
            f"{stage} completed in "
            f"{(time.time()-started)/60:.1f} minutes",
            flush=True
        )

    print(
        f"SUCCESS: {n}x{n}x1 DOS data saved",
        flush=True
    )

print("\nSUCCESS: ALL THREE DOS CALCULATIONS COMPLETED")
print("Results:", target)
