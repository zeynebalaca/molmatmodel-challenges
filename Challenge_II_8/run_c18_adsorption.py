from pathlib import Path
from ase.io import read, write
from ase.calculators.espresso import Espresso, EspressoProfile
from ase.optimize import BFGS
import numpy as np
import shutil
import json
import os
import traceback
import sys

ROOT = Path.cwd()
WORK = ROOT / "C18_100Ry"
WORK.mkdir(exist_ok=True)

SOURCE = Path.home() / "Molecular-and-Materials-Modeling-2026-August/materials-modeling"
STRUCTURE = SOURCE / "8_Adsorption/Hg_on_C18/c18.vasp"

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

pw = shutil.which("pw.x")
if not pw:
    raise RuntimeError("Quantum ESPRESSO pw.x not found.")

c18 = read(STRUCTURE)
if len(c18) != 18 or set(c18.get_chemical_symbols()) != {"C"}:
    raise RuntimeError("Unexpected C18 structure.")

# Select the C atom nearest to the in-plane geometric center.
xy_center = c18.positions[:, :2].mean(axis=0)
distances = np.linalg.norm(
    c18.positions[:, :2] - xy_center,
    axis=1
)
target = int(np.argmin(distances))

h_on_c18 = c18.copy()
h_position = c18.positions[target].copy()
h_position[2] += 1.20
h_on_c18 += read(SOURCE / "8_Adsorption/h.vasp")[0]
h_on_c18.positions[-1] = h_position

print("===== H@C18 STARTING STRUCTURE =====", flush=True)
print("Target carbon index:", target, flush=True)
print("Target carbon position:", c18.positions[target], flush=True)
print("Initial H position:", h_position, flush=True)
print("Initial C-H distance: 1.20 Å", flush=True)

write(WORK / "initial_H_on_C18.vasp",
      h_on_c18, format="vasp", direct=False)

def calculate(name, atoms):
    folder = WORK / name
    folder.mkdir(exist_ok=True)
    (folder / "tmp").mkdir(exist_ok=True)

    elements = sorted(set(atoms.get_chemical_symbols()))

    for element in elements:
        shutil.copy2(
            SOURCE / f"{element}.upf",
            folder / f"{element}.upf"
        )

    profile = EspressoProfile(
        command=f"mpirun --use-hwthread-cpus -np 4 {pw}",
        pseudo_dir=str(folder)
    )

    calc = Espresso(
        profile=profile,
        pseudopotentials={
            element: f"{element}.upf"
            for element in elements
        },
        input_data={
            "control": {
                "calculation": "scf",
                "prefix": name.lower(),
                "outdir": "./tmp",
                "tstress": True,
                "tprnfor": True,
            },
            "system": {
                "ibrav": 0,
                "ecutwfc": 100,
                "ecutrho": 800,
                "occupations": "smearing",
                "smearing": "gauss",
                "degauss": 0.01,
                "vdw_corr": "DFT-D3",
                "dftd3_version": 4,
                "nspin": 2,
            },
            "electrons": {
                "conv_thr": 1e-9,
                "mixing_beta": 0.5,
            }
        },
        kpts=(1, 1, 1),
        directory=str(folder)
    )

    atoms.calc = calc

    print(f"\n===== RUNNING {name} =====", flush=True)

    opt = BFGS(
        atoms,
        trajectory=str(folder / "relaxation.traj"),
        logfile=str(folder / "relaxation.log")
    )

    opt.run(fmax=0.01, steps=100)
    converged = bool(opt.converged())

    energy = float(atoms.get_potential_energy())
    forces = atoms.get_forces()
    max_force = float(np.linalg.norm(forces, axis=1).max())

    write(folder / "final_structure.vasp",
          atoms, format="vasp", direct=False)

    result = {
        "system": name,
        "formula": atoms.get_chemical_formula(),
        "energy_eV": energy,
        "converged": converged,
        "max_force_eV_A": max_force,
        "cutoff_Ry": 100,
        "kpoints": [1, 1, 1]
    }

    (folder / "result.json").write_text(
        json.dumps(result, indent=2)
    )

    print(f"Energy: {energy:.8f} eV", flush=True)
    print(f"Maximum force: {max_force:.6f} eV/Å", flush=True)
    print(f"Converged: {converged}", flush=True)

    if not converged:
        raise RuntimeError(f"{name}: relaxation not converged.")

    return energy

try:
    e_c18 = calculate("C18", c18)
    e_hc18 = calculate("H_on_C18", h_on_c18)

    h_ref = json.loads(
        (ROOT / "cutoff_100Ry/H/result.json").read_text()
    )
    e_h = float(h_ref["energy_eV"])

    binding = e_c18 + e_h - e_hc18

    summary = {
        "E_C18_eV": e_c18,
        "E_H_eV": e_h,
        "E_H_on_C18_eV": e_hc18,
        "binding_energy_eV": binding,
        "cutoff_Ry": 100,
        "kpoints": [1, 1, 1],
        "initial_adsorption_carbon_index": target
    }

    (WORK / "binding_energy_C18.json").write_text(
        json.dumps(summary, indent=2)
    )

    print("\n========== C18 RESULTS ==========", flush=True)
    print(f"E(C18)   = {e_c18:.8f} eV")
    print(f"E(H)     = {e_h:.8f} eV")
    print(f"E(H@C18) = {e_hc18:.8f} eV")
    print(f"Binding energy = {binding:.8f} eV")
    print("SUCCESS: H@C18 adsorption completed.")

except Exception:
    traceback.print_exc()
    print("Calculation stopped; completed outputs preserved.")
    sys.exit(1)
