from pathlib import Path
import os
import csv
import re
import shutil
import subprocess

root = Path.cwd()
source = Path.home() / "Molecular-and-Materials-Modeling-2026-August/materials-modeling"
pseudo = source / "Al.upf"

if not pseudo.exists():
    raise FileNotFoundError(pseudo)

env = os.environ.copy()
env["OMP_NUM_THREADS"] = "1"
env["OPENBLAS_NUM_THREADS"] = "1"

a = 2.019464845

def prepare_input(cutoff, k, calculation="scf"):
    ion_cell = """
&IONS
 ion_dynamics = 'bfgs',
/
&CELL
 cell_dynamics = 'bfgs',
 press = 0.0,
 press_conv_thr = 0.5,
/
""" if calculation == "vc-relax" else ""

    return f"""&CONTROL
 calculation = '{calculation}',
 prefix = 'Al',
 pseudo_dir = './',
 outdir = './tmp',
 tstress = .true.,
 tprnfor = .true.,
 etot_conv_thr = 1.0d-5,
 forc_conv_thr = 1.0d-3,
/
&SYSTEM
 ibrav = 0,
 nat = 1,
 ntyp = 1,
 ecutwfc = {cutoff},
 ecutrho = {cutoff * 8},
 occupations = 'smearing',
 smearing = 'gauss',
 degauss = 0.01,
/
&ELECTRONS
 conv_thr = 1.0d-9,
 mixing_beta = 0.5,
/
{ion_cell}
ATOMIC_SPECIES
 Al 26.9815385 Al.upf

CELL_PARAMETERS angstrom
 0.0 {a} {a}
 {a} 0.0 {a}
 {a} {a} 0.0

ATOMIC_POSITIONS angstrom
 Al 0.0 0.0 0.0

K_POINTS automatic
{k} {k} {k} 0 0 0
"""

tests = [
    ("cutoff_40Ry", 40, 12, "scf"),
    ("cutoff_55Ry", 55, 12, "scf"),
    ("cutoff_70Ry", 70, 12, "scf"),
    ("kpoints_6", 70, 6, "scf"),
    ("kpoints_10", 70, 10, "scf"),
    ("kpoints_14", 70, 14, "scf"),
    ("cell_relax", 70, 14, "vc-relax"),
]

results = []

for name, cutoff, k, calculation in tests:
    folder = root / name
    folder.mkdir(exist_ok=True)
    (folder / "tmp").mkdir(exist_ok=True)

    shutil.copy2(pseudo, folder / "Al.upf")
    (folder / "Al.in").write_text(
        prepare_input(cutoff, k, calculation)
    )

    print(f"\n===== {name} =====", flush=True)

    with (folder / "Al.out").open("w") as log:
        try:
            proc = subprocess.run(
                [
                    "mpirun", "--use-hwthread-cpus",
                    "-np", "4", "pw.x",
                    "-in", "Al.in"
                ],
                cwd=folder,
                env=env,
                stdout=log,
                stderr=subprocess.STDOUT,
                timeout=900
            )
            status = proc.returncode
        except subprocess.TimeoutExpired:
            status = 124

    output = (folder / "Al.out").read_text(errors="replace")

    energies = re.findall(
        r"!\s+total energy\s*=\s*([-\d.]+)\s*Ry",
        output
    )

    energy = float(energies[-1]) if energies else None

    success = (
        status == 0
        and "JOB DONE." in output
        and energy is not None
    )

    if calculation == "vc-relax":
        success = success and "bfgs converged" in output

    result = {
        "test": name,
        "calculation": calculation,
        "ecutwfc_Ry": cutoff,
        "k_grid": k,
        "energy_Ry": energy,
        "success": success,
        "exit_code": status
    }

    results.append(result)

    with (root / "results.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(result))
        writer.writeheader()
        writer.writerows(results)

    print(f"Exit code: {status}")
    print(f"Energy: {energy} Ry")
    print(f"Success: {success}", flush=True)

    if calculation == "vc-relax" and success:
        blocks = re.findall(
            r"Begin final coordinates(.*?)End final coordinates",
            output, re.S
        )
        if blocks:
            final = blocks[-1].strip()
            (root / "relaxed_geometry.txt").write_text(final)
            print("\nFinal optimized geometry:")
            print(final[:1600])

print("\n========== SUMMARY ==========")
for r in results:
    print(
        f"{r['test']:16s} "
        f"E={str(r['energy_Ry']):>16s} Ry "
        f"success={r['success']}"
    )

print("\nResults saved to results.csv")
