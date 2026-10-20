import csv
import os
import re
import shutil
import subprocess
from pathlib import Path

root = Path.cwd()
source = Path.home() / "Molecular-and-Materials-Modeling-2026-August/materials-modeling"

shutil.copy2(source / "6_Surfaces_and_2D_Materials/convergence_test_graphene.py",
             root / "convergence_test_graphene_original.py")

pseudo = source / "C.upf"
if not pseudo.exists():
    raise FileNotFoundError(pseudo)

env = os.environ.copy()
env["OMP_NUM_THREADS"] = "1"
env["OPENBLAS_NUM_THREADS"] = "1"

tests = (
    [("cutoff", e, 12) for e in (40, 55, 70)]
    + [("kpoints", 70, k) for k in (6, 12, 18, 24, 20)]
)

results = []

for kind, ecut, k in tests:
    name = f"{kind}_{ecut}Ry_k{k}"
    folder = root / name
    folder.mkdir(exist_ok=True)
    (folder / "tmp").mkdir(exist_ok=True)
    shutil.copy2(pseudo, folder / "C.upf")

    inp = f"""&CONTROL
 calculation = 'scf',
 prefix = 'graphene',
 pseudo_dir = './',
 outdir = './tmp',
/
&SYSTEM
 ibrav = 0,
 nat = 2,
 ntyp = 1,
 ecutwfc = {ecut},
 ecutrho = {8 * ecut},
 occupations = 'smearing',
 smearing = 'gauss',
 degauss = 0.01,
 assume_isolated = '2D',
/
&ELECTRONS
 conv_thr = 1.0d-9,
 mixing_beta = 0.5,
/
ATOMIC_SPECIES
 C 12.011 C.upf

CELL_PARAMETERS angstrom
  2.4560000000  0.0000000000  0.0000000000
 -1.2280000000  2.1269583917  0.0000000000
  0.0000000000  0.0000000000 15.0000000000

ATOMIC_POSITIONS angstrom
 C 0.0000000000 0.0000000000 7.5000000000
 C 0.0000000000 1.4179722611 7.5000000000

K_POINTS automatic
{k} {k} 1 0 0 0
"""
    (folder / "graphene.in").write_text(inp)

    print(f"\nRunning {kind}: ecut={ecut} Ry, k={k}x{k}x1",
          flush=True)

    try:
        with (folder / "graphene.out").open("w") as log:
            proc = subprocess.run(
                ["mpirun", "--use-hwthread-cpus", "-np", "4",
                 "pw.x", "-in", "graphene.in"],
                cwd=folder,
                env=env,
                stdout=log,
                stderr=subprocess.STDOUT,
                timeout=600
            )
        status = proc.returncode
    except subprocess.TimeoutExpired:
        status = 124

    output = (folder / "graphene.out").read_text(errors="replace")
    energies = re.findall(
        r"!\s+total energy\s*=\s*([-\d.]+)\s*Ry",
        output
    )

    energy = float(energies[-1]) if energies else None
    success = (
        status == 0
        and "JOB DONE." in output
        and "convergence has been achieved" in output
        and energy is not None
    )

    result = {
        "test": kind,
        "ecutwfc_Ry": ecut,
        "k_grid": f"{k}x{k}x1",
        "energy_Ry": energy,
        "success": success,
        "exit_code": status
    }
    results.append(result)

    with (root / "results.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(result))
        writer.writeheader()
        writer.writerows(results)

    print(f"Energy: {energy} Ry | success={success}", flush=True)
    if not success:
        print("Last output lines:")
        print("\n".join(output.splitlines()[-8:]))

print("\n========== SUMMARY ==========")
for r in results:
    print(
        f"{r['test']:8s} "
        f"ecut={r['ecutwfc_Ry']:2d} Ry "
        f"k={r['k_grid']:8s} "
        f"E={str(r['energy_Ry']):>15s} Ry "
        f"success={r['success']}"
    )

print("\nSaved results.csv and individual calculation outputs.")
