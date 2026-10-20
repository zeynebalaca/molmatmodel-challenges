from pathlib import Path
import shutil
import subprocess
import os
import re

root = Path.cwd()
source = Path.home() / "Molecular-and-Materials-Modeling-2026-August/materials-modeling/Si.upf"

env = os.environ.copy()
env["OMP_NUM_THREADS"] = "1"
env["OPENBLAS_NUM_THREADS"] = "1"

structures = {
    "original": 0.0,
    "shifted": 0.08
}

for name, shift in structures.items():
    folder = root / name
    folder.mkdir(exist_ok=True)
    (folder / "tmp").mkdir(exist_ok=True)
    shutil.copy2(source, folder / "Si.upf")

    input_text = f"""&CONTROL
 calculation = 'vc-relax',
 prefix = 'si_{name}',
 pseudo_dir = './',
 outdir = './tmp',
 etot_conv_thr = 1.0d-5,
 forc_conv_thr = 1.0d-3,
/
&SYSTEM
 ibrav = 0,
 nat = 2,
 ntyp = 1,
 ecutwfc = 70,
 ecutrho = 560,
 occupations = 'smearing',
 smearing = 'gauss',
 degauss = 0.01,
/
&ELECTRONS
 conv_thr = 1.0d-9,
 mixing_beta = 0.5,
/
&IONS
 ion_dynamics = 'bfgs',
/
&CELL
 cell_dynamics = 'bfgs',
 press = 0.0,
 press_conv_thr = 0.5,
/
ATOMIC_SPECIES
 Si 28.085 Si.upf

CELL_PARAMETERS angstrom
 0.000000 2.714900 2.714900
 2.714900 0.000000 2.714900
 2.714900 2.714900 0.000000

ATOMIC_POSITIONS angstrom
 Si {1.35745 + shift:.6f} 4.072350 4.072350
 Si 0.000000 0.000000 0.000000

K_POINTS automatic
8 8 8 0 0 0
"""

    (folder / "Si_vc_relax.in").write_text(input_text)

    print(f"\n===== Running {name} structure =====", flush=True)

    with (folder / "Si_vc_relax.out").open("w") as log:
        try:
            process = subprocess.run(
                ["mpirun", "--use-hwthread-cpus", "-np", "4",
                 "pw.x", "-in", "Si_vc_relax.in"],
                cwd=folder,
                env=env,
                stdout=log,
                stderr=subprocess.STDOUT,
                timeout=900
            )
            status = process.returncode
        except subprocess.TimeoutExpired:
            status = 124

    output = (folder / "Si_vc_relax.out").read_text(errors="replace")

    values = re.findall(
        r"!\s+total energy\s*=\s*([-\d.]+)\s*Ry",
        output
    )

    converged = (
        status == 0
        and "JOB DONE." in output
        and "bfgs converged" in output
    )

    print(f"Exit code: {status}")
    print(f"Geometry converged: {converged}")
    print(f"Last SCF energy: {values[-1] if values else 'N/A'} Ry")

    final = re.findall(
        r"Begin final coordinates(.*?)End final coordinates",
        output,
        re.S
    )

    if final:
        print("Final coordinates and cell:")
        print(final[-1].strip()[:1800])

print("\nQE relaxation runs finished. Outputs saved in original/ and shifted/.")
