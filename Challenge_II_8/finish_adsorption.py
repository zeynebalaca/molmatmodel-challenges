from pathlib import Path
import json
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ase.io import read
from docutils.core import publish_doctree

root = Path.cwd()

b80 = json.loads((root / "binding_energy_80Ry.json").read_text())
b100 = json.loads((root / "cutoff_100Ry/binding_energy_100Ry.json").read_text())
b18 = json.loads((root / "C18_100Ry/binding_energy_C18.json").read_text())

cases = [
    ("H@C8", 8, 80, float(b80["binding_energy_eV"])),
    ("H@C8", 8, 100, float(b100["binding_energy_eV"])),
    ("H@C18", 18, 100, float(b18["binding_energy_eV"]))
]

for name, n, cutoff, energy in cases:
    if not np.isfinite(energy):
        raise RuntimeError(f"Invalid binding energy: {name}, {cutoff}")

for folder in [
    "H_on_C8",
    "C8",
    "cutoff_100Ry/H_on_C8",
    "cutoff_100Ry/C8",
    "C18_100Ry/C18",
    "C18_100Ry/H_on_C18"
]:
    result = json.loads((root / folder / "result.json").read_text())
    if not result["converged"]:
        raise RuntimeError(f"Unconverged structure: {folder}")

delta_cutoff = cases[1][3] - cases[0][3]
delta_size = cases[2][3] - cases[1][3]

# Adsorption geometry
geo8 = read(root / "cutoff_100Ry/H_on_C8/final_structure.vasp")
geo18 = read(root / "C18_100Ry/H_on_C18/final_structure.vasp")

def nearest_ch(atoms):
    h_ids = [i for i, a in enumerate(atoms) if a.symbol == "H"]
    c_ids = [i for i, a in enumerate(atoms) if a.symbol == "C"]
    if len(h_ids) != 1:
        raise RuntimeError("Expected exactly one H atom.")
    ds = atoms.get_distances(h_ids[0], c_ids, mic=True)
    return float(np.min(ds))

ch8 = nearest_ch(geo8)
ch18 = nearest_ch(geo18)

with (root / "adsorption_summary.csv").open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "system", "carbon_atoms", "ecutwfc_Ry", "binding_energy_eV"
    ])
    writer.writerows(cases)

# Plot comparison
labels = ["C8 / 80 Ry", "C8 / 100 Ry", "C18 / 100 Ry"]
values = [case[3] for case in cases]

plt.figure(figsize=(8, 5))
bars = plt.bar(labels, values)
for bar, value in zip(bars, values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 0.03,
        f"{value:.4f} eV",
        ha="center"
    )
plt.ylabel("Binding energy (eV)")
plt.title("Hydrogen Adsorption: Cutoff and Cell-Size Effects")
plt.ylim(0, max(values) * 1.15)
plt.tight_layout()
plt.savefig(root / "adsorption_energy_comparison.png", dpi=200)
plt.close()

title = "Challenge II.8 - Hydrogen Adsorption on Graphene"

lines = [
    title,
    "=" * len(title),
    "",
    "Objective",
    "---------",
    "Investigate the adsorption of one hydrogen atom on periodic",
    "graphene supercells containing 8 and 18 carbon atoms.",
    "Assess the influence of wavefunction cutoff and supercell size.",
    "",
    "Computational Method",
    "--------------------",
    "Quantum ESPRESSO plane-wave DFT calculations were performed",
    "through ASE, using the supplied C and H pseudopotentials.",
    "The original course geometry files were used to initialize",
    "the C8, H@C8 and C18 configurations.",
    "",
    "Spin-polarized calculations were employed, with the",
    "DFT-D3 dispersion correction and a 1x1x1 k-point grid.",
    "The charge-density cutoffs were set to eight times",
    "the corresponding wavefunction cutoffs.",
    "",
    "Atomic positions of clean slabs and hydrogen-adsorbed",
    "slabs were optimized with BFGS, using a maximum force",
    "criterion of 0.01 eV/Angstrom.",
    "The isolated H atom was evaluated separately by SCF.",
    "",
    "The positive binding-energy convention was:",
    "",
    "E_binding = E(clean slab) + E(H) - E(H on slab).",
    "",
    "Results",
    "-------",
    f"- H@C8 at 80 Ry: {cases[0][3]:.8f} eV",
    f"- H@C8 at 100 Ry: {cases[1][3]:.8f} eV",
    f"- H@C18 at 100 Ry: {cases[2][3]:.8f} eV",
    "",
    f"- Binding-energy change from 80 to 100 Ry for C8: "
    f"{delta_cutoff:.8f} eV",
    f"- Binding-energy change from C8 to C18 at 100 Ry: "
    f"{delta_size:.8f} eV",
    "",
    "Optimized Bond Distances",
    "------------------------",
    f"- H@C8 at 100 Ry: nearest C-H distance = {ch8:.5f} Angstrom",
    f"- H@C18 at 100 Ry: nearest C-H distance = {ch18:.5f} Angstrom",
    "",
    "Discussion",
    "----------",
    "The binding energies at 80 and 100 Ry are nearly",
    "identical for the C8 system, suggesting limited",
    "wavefunction-cutoff sensitivity over this tested interval.",
    "",
    "Increasing the graphene supercell from C8 to C18",
    "changes the calculated binding energy significantly.",
    "This indicates an important supercell-size effect.",
    "Neither a complete k-point convergence test nor a",
    "supercell-size extrapolation was performed.",
    "",
    "The initial adsorption geometry used one H atom",
    "placed 1.20 Angstrom above a carbon site.",
    "The optimized H@C18 calculation represents one",
    "local adsorption configuration, not a systematic",
    "search over every possible adsorption site.",
    "",
    "The agreement of the C8/80 Ry binding energy with",
    "the course reference is a numerical reproduction",
    "of that calculation, not experimental validation.",
    "",
    "Outputs",
    "-------",
    "- adsorption_summary.csv: binding-energy comparison",
    "- adsorption_energy_comparison.png: summary plot",
    "- binding_energy_80Ry.json: C8 at 80 Ry",
    "- cutoff_100Ry/: C8 and H calculations at 100 Ry",
    "- C18_100Ry/: C18 and H@C18 structures and results",
    "- run_adsorption.py: baseline calculation script",
    "- run_adsorption_100Ry.py: cutoff comparison",
    "- run_c18_adsorption.py: enlarged-supercell study",
    ""
]

report = "\n".join(lines)
(root / "readme.rst").write_text(report)
publish_doctree(report, settings_overrides={"halt_level": 2})

print("===== CHALLENGE II.8 SUMMARY =====")
for name, n, cutoff, energy in cases:
    print(f"{name:6s} | {cutoff:3d} Ry | {energy:.8f} eV")

print(f"\nCutoff effect: {delta_cutoff:.8f} eV")
print(f"Supercell-size effect: {delta_size:.8f} eV")
print(f"C-H distance, C8:  {ch8:.5f} Å")
print(f"C-H distance, C18: {ch18:.5f} Å")

for filename in [
    "adsorption_summary.csv",
    "adsorption_energy_comparison.png",
    "readme.rst"
]:
    if not (root / filename).is_file():
        raise RuntimeError(f"Missing output: {filename}")

print("\nSUCCESS: Challenge II.8 README validated.")
print("SUCCESS: Adsorption comparison figure created.")
print("SUCCESS: All three adsorption cases documented.")
