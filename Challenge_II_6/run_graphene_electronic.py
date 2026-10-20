from pathlib import Path
import os
import re
import shutil
import subprocess
import sys

root = Path.cwd()
work = root / "electronic"
work.mkdir(exist_ok=True)
(work / "tmp").mkdir(exist_ok=True)

source = Path.home() / "Molecular-and-Materials-Modeling-2026-August/materials-modeling/C.upf"
shutil.copy2(source, work / "C.upf")

relax_output = (root / "cell_relax/graphene_relax.out").read_text(errors="replace")

blocks = re.findall(
    r"Begin final coordinates(.*?)End final coordinates",
    relax_output,
    re.S
)
if not blocks:
    raise RuntimeError("Optimized graphene geometry was not found.")

block = blocks[-1]
cell_match = re.search(
    r"CELL_PARAMETERS\s*\(angstrom\)\s*\n((?:[^\n]+\n){3})",
    block
)
positions_match = re.search(
    r"ATOMIC_POSITIONS\s*\(angstrom\)\s*\n((?:[^\n]+\n){2})",
    block
)

if not cell_match or not positions_match:
    raise RuntimeError("Unable to parse final cell or atom positions.")

cell = cell_match.group(1).strip()
positions = positions_match.group(1).strip()

env = os.environ.copy()
env["OMP_NUM_THREADS"] = "1"
env["OPENBLAS_NUM_THREADS"] = "1"

def pw_input(calculation, k):
    nbnd_line = "nbnd = 12," if calculation == "nscf" else ""
    return f"""&CONTROL
 calculation = '{calculation}',
 prefix = 'graphene',
 pseudo_dir = './',
 outdir = './tmp',
 tstress = .true.,
/
&SYSTEM
 ibrav = 0,
 nat = 2,
 ntyp = 1,
 ecutwfc = 90,
 ecutrho = 720,
 occupations = 'smearing',
 smearing = 'gauss',
 degauss = 0.01,
 assume_isolated = '2D',
 {nbnd_line}
/
&ELECTRONS
 conv_thr = 1.0d-9,
 mixing_beta = 0.5,
/
ATOMIC_SPECIES
 C 12.011 C.upf

CELL_PARAMETERS angstrom
{cell}

ATOMIC_POSITIONS angstrom
{positions}

K_POINTS automatic
{k} {k} 1 0 0 0
"""

(work / "scf.in").write_text(pw_input("scf", 18))
(work / "nscf.in").write_text(pw_input("nscf", 24))

(work / "dos.in").write_text("""&DOS
 prefix = 'graphene',
 outdir = './tmp',
 fildos = 'graphene_tdos.dat',
 Emin = -20.0,
 Emax = 20.0,
 DeltaE = 0.02,
/
""")

(work / "projwfc.in").write_text("""&PROJWFC
 prefix = 'graphene',
 outdir = './tmp',
 filpdos = 'graphene_pdos',
 Emin = -20.0,
 Emax = 20.0,
 DeltaE = 0.02,
/
""")

(work / "pp.in").write_text("""&INPUTPP
 prefix = 'graphene',
 outdir = './tmp',
 filplot = 'charge_density',
 plot_num = 0,
/
&PLOT
 nfile = 1,
 filepp(1) = 'charge_density',
 weight(1) = 1.0,
 iflag = 3,
 output_format = 6,
 fileout = 'charge_density.cube',
/
""")

def run(name, executable, input_name, ranks=1, timeout=1200):
    command = (
        ["mpirun", "--use-hwthread-cpus", "-np", str(ranks)]
        if ranks > 1 else []
    )
    command += [executable, "-in", input_name]

    print(f"\n===== RUNNING {name} =====", flush=True)
    output_file = work / f"{name}.out"

    with output_file.open("w") as logfile:
        try:
            result = subprocess.run(
                command,
                cwd=work,
                env=env,
                stdout=logfile,
                stderr=subprocess.STDOUT,
                timeout=timeout
            )
            status = result.returncode
        except subprocess.TimeoutExpired:
            status = 124

    output = output_file.read_text(errors="replace")
    success = status == 0 and "JOB DONE." in output

    print(f"Exit code: {status}")
    print(f"Completed: {success}", flush=True)

    if not success:
        print("Last 25 output lines:")
        print("\n".join(output.splitlines()[-25:]))
        sys.exit(1)

    return output

scf = run("scf", "pw.x", "scf.in", ranks=4)
nscf = run("nscf", "pw.x", "nscf.in", ranks=4)
dos = run("dos", "dos.x", "dos.in")
pdos = run("projwfc", "projwfc.x", "projwfc.in", ranks=2)
charge = run("charge", "pp.x", "pp.in")

fermi_values = re.findall(
    r"the Fermi energy is\s+([-\d.]+)\s+ev",
    nscf,
    re.I
)

print("\n========== ELECTRONIC STRUCTURE RESULTS ==========")

if fermi_values:
    fermi = float(fermi_values[-1])
    (work / "fermi_energy.txt").write_text(f"{fermi:.8f}\n")
    print(f"Fermi energy: {fermi:.6f} eV")
else:
    print("Fermi energy: not found in NSCF output")

spilling = re.findall(
    r"Spilling Parameter:\s*([-\d.]+)",
    pdos,
    re.I
)
if spilling:
    print(f"Spilling parameter: {spilling[-1]}")

print("\nGenerated files:")
for filename in [
    "graphene_tdos.dat",
    "graphene_pdos.pdos_tot",
    "charge_density.cube"
]:
    path = work / filename
    print(f"  {filename}: {'OK' if path.exists() else 'MISSING'}")

print("\nCarbon orbital projection files:")
for path in sorted(work.glob("graphene_pdos.pdos_atm*")):
    print(" ", path.name)

print("\nSaved calculation directory:", work)
