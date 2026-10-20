from pathlib import Path
from docutils.core import publish_doctree
import csv
import re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path.cwd()
al_dir = root / "electronic"
si_dir = Path.home() / "challenges/Challenge_II_4/baseline"

def get_data(folder):
    log = (folder / (
        "electronic_properties_al.log"
        if folder == al_dir
        else "electronic_properties_si.log"
    )).read_text(errors="replace")

    def number(pattern):
        matches = re.findall(pattern, log, re.I)
        if not matches:
            raise RuntimeError(f"Missing value: {pattern}")
        return float(matches[-1])

    fermi = number(r"Fermi level from NSCF calculation:\s*([-\d.]+)")
    spilling = number(r"Spilling parameter value:\s*([-\d.]+)")
    difference = number(r"Relative difference in integrated DOS:\s*([\d.]+)%")

    dos = np.loadtxt(folder / "total_dos.dat", comments="#")
    return fermi, spilling, difference, dos

ef_al, spilling_al, diff_al, dos_al = get_data(al_dir)
ef_si, spilling_si, diff_si, dos_si = get_data(si_dir)

# Comparison of total densities of states
plt.figure(figsize=(9, 5))
plt.plot(dos_al[:, 0] - ef_al, dos_al[:, 1],
         label="Aluminum (metal)")
plt.plot(dos_si[:, 0] - ef_si, dos_si[:, 1],
         label="Silicon (semiconductor)")
plt.axvline(0, color="black", linestyle="--", linewidth=1)
plt.xlabel("Energy relative to Fermi level (eV)")
plt.ylabel("Total DOS (states/eV/cell)")
plt.xlim(-8, 8)
plt.title("Total Density of States: Aluminum vs Silicon")
plt.legend()
plt.tight_layout()
plt.savefig(root / "Al_vs_Si_TDOS.png", dpi=200)
plt.close()

# Aluminum projected density of states
pdos_dir = al_dir / "pdos_results"
files = {
    "Al s": next(pdos_dir.glob("*atm#1(Al)_wfc#1(s)")),
    "Al p": next(pdos_dir.glob("*atm#1(Al)_wfc#2(p)"))
}

plt.figure(figsize=(9, 5))

for label, filename in files.items():
    values = np.loadtxt(filename, comments="#")
    plt.plot(values[:, 0] - ef_al, values[:, 1],
             label=label)

plt.axvline(0, color="black", linestyle="--", linewidth=1)
plt.xlabel("Energy relative to Fermi level (eV)")
plt.ylabel("Projected DOS (states/eV)")
plt.xlim(-8, 8)
plt.title("Aluminum: s and p Orbital Contributions")
plt.legend()
plt.tight_layout()
plt.savefig(root / "Al_PDOS.png", dpi=200)
plt.close()

with (root / "results.csv").open() as f:
    tests = list(csv.DictReader(f))

with (root / "extended_kpoints.csv").open() as f:
    extended = list(csv.DictReader(f))

if not all(r["success"] == "True" for r in tests + extended):
    raise RuntimeError("Not all convergence calculations succeeded.")

title = "Challenge II.5 - Electronic Properties of Aluminum"

lines = [
    title,
    "=" * len(title),
    "",
    "Objective",
    "---------",
    "Investigate the structure and electronic properties of",
    "FCC aluminum and compare its density of states with silicon.",
    "",
    "Method",
    "------",
    "Quantum ESPRESSO was used for plane-wave DFT calculations.",
    "The supplied Al.upf pseudopotential was employed.",
    "Energy-cutoff and k-point convergence scans preceded",
    "variable-cell structural relaxation.",
    "",
    "The electronic structure calculation used the relaxed",
    "aluminum cell, a 70 Ry wavefunction cutoff,",
    "an 18x18x18 SCF mesh and a 26x26x26 NSCF mesh.",
    "Charge density, Lowdin populations, TDOS and PDOS",
    "were calculated with QE post-processing tools.",
    "",
    "Convergence Tests",
    "-----------------",
    ""
]

for r in tests:
    lines.append(
        f"- {r['test']}: {r['energy_Ry']} Ry "
        f"(success: {r['success']})."
    )

for r in extended:
    k = r["k_grid"]
    lines.append(
        f"- k={k}x{k}x{k}: {r['energy_Ry']} Ry; "
        f"successive energy difference "
        f"{float(r['delta_meV_atom']):.4f} meV/atom."
    )

lines += [
    "",
    "Structural Relaxation",
    "---------------------",
    "The initial FCC lattice parameter was approximately",
    "4.03893 Angstrom. The optimized parameter was approximately",
    "4.03299 Angstrom and the final primitive cell volume",
    "was 16.39911 Angstrom^3.",
    "",
    "Electronic Properties",
    "---------------------",
    f"- Al Fermi energy: {ef_al:.4f} eV",
    f"- Al spilling parameter: {spilling_al:.6f}",
    f"- Al integrated TDOS-PDOS difference: {diff_al:.2f} percent",
    f"- Si Fermi energy: {ef_si:.4f} eV",
    f"- Si spilling parameter: {spilling_si:.6f}",
    f"- Si integrated TDOS-PDOS difference: {diff_si:.2f} percent",
    "",
    "Discussion",
    "----------",
    "Aluminum is metallic, whereas crystalline silicon is",
    "semiconducting. Their TDOS profiles are compared after",
    "shifting each energy axis by its own calculated Fermi level.",
    "",
    "The low spilling parameters indicate reasonably good",
    "orbital projections in these calculations.",
    "",
    "The 26x26x26 k-point mesh gave a successive energy",
    "difference below 1 meV/atom in the preliminary Al scan.",
    "Further k-point testing would strengthen convergence",
    "verification, particularly for metallic aluminum.",
    "",
    "The silicon and aluminum DOS were calculated using",
    "different k-point grids and primitive cells.",
    "Their absolute DOS magnitudes should not be interpreted",
    "as directly normalized per atom without adjustment.",
    "",
    "The supplied course FCC structure was used as the initial",
    "structure. An independently downloaded experimental",
    "crystal structure has not yet been verified.",
    "A separate band-structure path calculation was not performed.",
    "",
    "Outputs",
    "-------",
    "- Al_vs_Si_TDOS.png: silicon-aluminum TDOS comparison",
    "- Al_PDOS.png: aluminum orbital-projected DOS",
    "- results.csv: initial convergence and relaxation tests",
    "- extended_kpoints.csv: additional k-point calculations",
    "- electronic/: QE inputs, output data and post-processing",
    ""
]

report = "\n".join(lines)
(root / "readme.rst").write_text(report)
publish_doctree(report, settings_overrides={"halt_level": 2})

print("SUCCESS: Al vs Si DOS figure created.")
print("SUCCESS: Al orbital PDOS figure created.")
print("SUCCESS: Challenge II.5 README validated.")
print(f"Al Fermi energy: {ef_al:.4f} eV")
print(f"Al spilling: {spilling_al:.6f}")
