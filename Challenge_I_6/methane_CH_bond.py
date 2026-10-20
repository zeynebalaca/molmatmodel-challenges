import csv
from pathlib import Path
from ase import Atoms
from ase.build import molecule
from ase.calculators.emt import EMT
from ase.optimize import BFGS
from docutils.core import publish_doctree

results = []
reference = 4.52  # Approximate experimental CH4 -> CH3 + H BDE, eV

def calculate(name, factory):
    print(f"\n===== {name} =====", flush=True)

    ch4 = molecule("CH4")
    ch4.calc = factory()
    opt4 = BFGS(ch4, logfile=None)
    ok4 = opt4.run(fmax=0.01, steps=200)
    e4 = ch4.get_potential_energy()

    ch3 = molecule("CH3")
    ch3.calc = factory()
    opt3 = BFGS(ch3, logfile=None)
    ok3 = opt3.run(fmax=0.01, steps=200)
    e3 = ch3.get_potential_energy()

    h = Atoms("H", calculator=factory())
    eh = h.get_potential_energy()

    bde = e3 + eh - e4
    result = dict(
        method=name,
        E_CH4_eV=e4,
        E_CH3_eV=e3,
        E_H_eV=eh,
        BDE_eV=bde,
        BDE_kJ_mol=bde * 96.485,
        reference_eV=reference,
        CH4_converged=bool(ok4),
        CH3_converged=bool(ok3),
    )
    results.append(result)

    for key, value in result.items():
        print(f"{key}: {value}", flush=True)
    return result

calculate("EMT", lambda: EMT())

try:
    from mace.calculators import mace_mp
    print("\nLoading MACE-MP medium model...", flush=True)
    mace = mace_mp(model="medium", device="cpu", default_dtype="float64")
    calculate("MACE-MP", lambda: mace)
except Exception as exc:
    print(f"MACE FAILED: {type(exc).__name__}: {exc}", flush=True)

with open("results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(results[0]))
    writer.writeheader()
    writer.writerows(results)

lines = [
    "Challenge I.6 - Methane C-H Bond Dissociation Energy",
    "===================================================",
    "",
    "Objective",
    "---------",
    "Adapt the course ethane C-C bond dissociation example to methane.",
    "",
    "Method",
    "------",
    "The reaction CH4 -> CH3 + H was evaluated using ASE.",
    "CH4 and CH3 geometries were optimized with BFGS to a maximum",
    "force tolerance of 0.01 eV/Angstrom.",
    "BDE = E(CH3) + E(H) - E(CH4).",
    "Both EMT and a pretrained MACE-MP medium model were tested.",
    "",
    "Results",
    "-------",
    "",
]
for r in results:
    lines.extend([
        f"- {r['method']}: C-H dissociation energy = {r['BDE_eV']:.5f} eV",
        f"  ({r['BDE_kJ_mol']:.2f} kJ/mol); CH4 converged:",
        f"  {r['CH4_converged']}; CH3 converged: {r['CH3_converged']}.",
        "",
    ])

lines.extend([
    "Discussion",
    "----------",
    "The approximate experimental methane C-H bond dissociation",
    f"energy is {reference:.2f} eV. The calculated values are",
    "model-dependent electronic energy differences, not",
    "zero-point-corrected thermochemical bond enthalpies.",
    "Neither EMT nor a general-purpose materials MACE potential",
    "guarantees accurate radical or isolated-atom energetics.",
    "See results.csv and methane_CH_bond.log for complete values.",
    "",
])

report = "\n".join(lines)
Path("readme.rst").write_text(report)
publish_doctree(report, settings_overrides={"halt_level": 2})
print("\nSUCCESS: Challenge I.6 results saved and README validated.", flush=True)
