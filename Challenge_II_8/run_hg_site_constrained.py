import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

from pathlib import Path
import shutil
import json
import numpy as np
from ase import Atom
from ase.io import read, write
from ase.constraints import FixAtoms, FixCartesian
from ase.optimize import BFGS
from ase.calculators.espresso import Espresso, EspressoProfile

root = Path.cwd() / "Hg_on_C18_constrained"
root.mkdir(exist_ok=True)

src = (Path.home() /
       "Molecular-and-Materials-Modeling-2026-August/"
       "materials-modeling/8_Adsorption/Hg_on_C18")

previous = Path.cwd() / "Hg_on_C18_three_sites"

pw = shutil.which("pw.x")
if pw is None:
    raise RuntimeError("Quantum ESPRESSO pw.x not found")

c18 = read(src / "c18.vasp")

# Sites identified in the previous geometric analysis.
top = c18.positions[7].copy()

bridge_vector = c18.get_distance(
    7, 15, mic=True, vector=True
)
bridge = top + 0.5 * bridge_vector

ring = (3, 12, 7, 15, 6, 14)
anchor = ring[0]
ring_points = [c18.positions[anchor]]

for idx in ring[1:]:
    displacement = c18.get_distance(
        anchor, idx, mic=True, vector=True
    )
    ring_points.append(c18.positions[anchor] + displacement)

hollow = np.mean(ring_points, axis=0)

sites = {
    "on_top": top,
    "on_bridge": bridge,
    "on_hollow": hollow
}

e_c18 = json.loads(
    (previous / "clean_C18/result.json").read_text()
)["energy_eV"]

e_hg = json.loads(
    (previous / "isolated_Hg/result.json").read_text()
)["energy_eV"]

results = {}

print("Reference C18 energy:", e_c18, flush=True)
print("Reference Hg energy:", e_hg, flush=True)

for name, position in sites.items():
    directory = root / name
    directory.mkdir(exist_ok=True)
    (directory / "tmp").mkdir(exist_ok=True)

    atoms = c18.copy()

    hg_position = np.array(position, dtype=float)
    hg_position[2] = np.mean(c18.positions[:, 2]) + 3.4
    atoms.append(Atom("Hg", position=hg_position))

    # Freeze all carbon atoms and Hg's lateral coordinates.
    atoms.set_constraint([
        FixAtoms(indices=list(range(18))),
        FixCartesian(18, mask=(True, True, False))
    ])

    profile = EspressoProfile(
        command=f"mpirun --use-hwthread-cpus -np 4 {pw}",
        pseudo_dir=str(src)
    )

    atoms.calc = Espresso(
        profile=profile,
        pseudopotentials={
            "C": "C.upf",
            "Hg": "Hg.upf"
        },
        input_data={
            "control": {
                "calculation": "scf",
                "prefix": "hg_constrained",
                "outdir": "./tmp",
                "tstress": True,
                "tprnfor": True
            },
            "system": {
                "ecutwfc": 80,
                "occupations": "smearing",
                "smearing": "gauss",
                "degauss": 0.01,
                "vdw_corr": "DFT-D3",
                "dftd3_version": 4
            },
            "electrons": {
                "conv_thr": 1e-9,
                "mixing_beta": 0.5
            }
        },
        kpts=(1, 1, 1),
        directory=str(directory)
    )

    write(directory / "initial.vasp", atoms, format="vasp")

    print(f"\n===== {name} =====", flush=True)

    opt = BFGS(
        atoms,
        logfile=str(directory / "relaxation.log"),
        trajectory=str(directory / "relaxation.traj")
    )

    opt.run(fmax=0.01, steps=60)

    converged = bool(opt.converged())
    energy = float(atoms.get_potential_energy())
    fmax = float(np.linalg.norm(atoms.get_forces(), axis=1).max())
    e_ads = energy - e_c18 - e_hg

    result = {
        "site": name,
        "converged": converged,
        "total_energy_eV": energy,
        "adsorption_energy_eV": e_ads,
        "constrained_max_force_eV_A": fmax,
        "Hg_height_A": float(
            atoms.positions[18, 2] -
            np.mean(atoms.positions[:18, 2])
        ),
        "method": "Fixed carbon slab, fixed Hg x/y, optimized Hg z"
    }

    write(directory / "final.vasp", atoms, format="vasp")
    (directory / "result.json").write_text(
        json.dumps(result, indent=2)
    )

    results[name] = result

    print("Converged:", converged, flush=True)
    print("Constrained Fmax:", fmax, "eV/A", flush=True)
    print("Adsorption energy:", e_ads, "eV", flush=True)

    if not converged:
        raise RuntimeError(f"{name} did not converge")

(root / "comparison.json").write_text(
    json.dumps(results, indent=2)
)

print("\n===== FINAL COMPARISON =====")
for name, result in results.items():
    print(
        f"{name}: "
        f"{result['adsorption_energy_eV']:.8f} eV"
    )

print("SUCCESS: Three constrained site calculations completed.")
