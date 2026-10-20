from pathlib import Path
from ase.io import read, write
from ase.calculators.espresso import Espresso, EspressoProfile
from ase.optimize import BFGS
import shutil
import json
import os
import sys
import traceback

ROOT = Path.cwd()
SOURCE = Path.home() / "Molecular-and-Materials-Modeling-2026-August/materials-modeling"
STRUCTURES = SOURCE / "8_Adsorption"

PW = shutil.which("pw.x")
if not PW:
    raise RuntimeError("pw.x not found in the active environment.")

for symbol in ("C", "H"):
    if not (SOURCE / f"{symbol}.upf").exists():
        raise FileNotFoundError(SOURCE / f"{symbol}.upf")

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

def run_case(name, structure_name, relax):
    work = ROOT / name
    work.mkdir(exist_ok=True)
    (work / "tmp").mkdir(exist_ok=True)

    atoms = read(STRUCTURES / structure_name, format="vasp")

    symbols = set(atoms.get_chemical_symbols())
    for element in symbols:
        shutil.copy2(SOURCE / f"{element}.upf",
                     work / f"{element}.upf")

    print(f"\n========== {name} ==========", flush=True)
    print("Formula:", atoms.get_chemical_formula(), flush=True)
    print("Number of atoms:", len(atoms), flush=True)

    system = {
        "ibrav": 0,
        "ecutwfc": 80,
        "ecutrho": 640,
        "occupations": "smearing",
        "smearing": "gauss",
        "degauss": 0.01,
        "vdw_corr": "DFT-D3",
        "dftd3_version": 4,
        "nspin": 2,
    }

    # Spin-polarized isolated H atom.
    if name == "H":
        system["starting_magnetization(1)"] = 1.0

    profile = EspressoProfile(
        command=f"mpirun --use-hwthread-cpus -np 4 {PW}",
        pseudo_dir=str(work)
    )

    calc = Espresso(
        profile=profile,
        pseudopotentials={
            element: f"{element}.upf"
            for element in sorted(symbols)
        },
        input_data={
            "control": {
                "calculation": "scf",
                "prefix": name.lower(),
                "outdir": "./tmp",
                "tstress": True,
                "tprnfor": True,
            },
            "system": system,
            "electrons": {
                "conv_thr": 1e-9,
                "mixing_beta": 0.5,
            }
        },
        kpts=(1, 1, 1),
        directory=str(work)
    )

    atoms.calc = calc
    converged = True

    if relax:
        print("Starting BFGS relaxation...", flush=True)

        opt = BFGS(
            atoms,
            trajectory=str(work / "relaxation.traj"),
            logfile=str(work / "relaxation.log")
        )
        opt.run(fmax=0.01, steps=80)
        converged = bool(opt.converged())

        print("Geometry optimization converged:",
              converged, flush=True)

    energy = float(atoms.get_potential_energy())

    max_force = (
        float((atoms.get_forces() ** 2).sum(axis=1).max() ** 0.5)
        if relax else None
    )

    write(work / "final_structure.vasp",
          atoms, format="vasp", direct=False)

    result = {
        "system": name,
        "formula": atoms.get_chemical_formula(),
        "n_atoms": len(atoms),
        "cutoff_Ry": 80,
        "kpoints": [1, 1, 1],
        "energy_eV": energy,
        "relaxed": relax,
        "converged": converged,
        "max_force_eV_A": max_force
    }

    (work / "result.json").write_text(
        json.dumps(result, indent=2)
    )

    print(f"Final energy: {energy:.8f} eV", flush=True)
    if max_force is not None:
        print(f"Maximum force: {max_force:.6f} eV/Å",
              flush=True)

    if not converged:
        raise RuntimeError(f"{name}: BFGS did not converge.")

    return energy

try:
    e_ch = run_case("H_on_C8", "ch.vasp", True)
    e_c = run_case("C8", "c.vasp", True)
    e_h = run_case("H", "h.vasp", False)

    binding = e_c + e_h - e_ch

    summary = {
        "E_H_on_C8_eV": e_ch,
        "E_C8_eV": e_c,
        "E_H_eV": e_h,
        "binding_energy_eV": binding,
        "cutoff_Ry": 80
    }

    (ROOT / "binding_energy_80Ry.json").write_text(
        json.dumps(summary, indent=2)
    )

    print("\n========== FINAL RESULTS ==========")
    print(f"E(H@C8) = {e_ch:.8f} eV")
    print(f"E(C8)   = {e_c:.8f} eV")
    print(f"E(H)    = {e_h:.8f} eV")
    print(f"Binding energy = {binding:.8f} eV")
    print("SUCCESS: 80 Ry baseline completed.")

except Exception:
    traceback.print_exc()
    print("\nCalculation stopped. Completed results are preserved.")
    sys.exit(1)
