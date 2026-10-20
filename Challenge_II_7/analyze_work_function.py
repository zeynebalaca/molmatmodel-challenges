import re
import csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from docutils.core import publish_doctree

root = Path(".").resolve()

cases = [
    ("with_2D", "with_2D"),
    ("without_2D", "without_2D"),
]

results = []

plt.figure(figsize=(10, 6))

for label, folder in cases:
    avg_path = root / folder / "potential_results" / "avg.dat"
    log_path = root / folder / "run.log"

    data = np.loadtxt(avg_path)
    z = data[:, 0] * 0.529177          # bohr -> angstrom
    planar = data[:, 1] * 13.6058      # Ry -> eV
    macro = data[:, 2] * 13.6058       # Ry -> eV

    text = log_path.read_text(errors="replace")
    m = re.search(r"Fermi level:\s*([-\d\.]+)\s*eV", text)
    if not m:
        raise RuntimeError(f"Fermi level not found in {log_path}")
    fermi = float(m.group(1))

    zmax = float(np.max(z))

    # Vakum pencereleri: hücrenin sol ve sağ tarafındaki düz bölgeler
    left_mask = (z > 0.10 * zmax) & (z < 0.30 * zmax)
    right_mask = (z > 0.70 * zmax) & (z < 0.90 * zmax)

    vac_left = float(np.mean(macro[left_mask]))
    vac_right = float(np.mean(macro[right_mask]))
    vac_avg = 0.5 * (vac_left + vac_right)
    work_function = vac_avg - fermi

    results.append({
        "case": label,
        "fermi_eV": fermi,
        "vacuum_left_eV": vac_left,
        "vacuum_right_eV": vac_right,
        "vacuum_avg_eV": vac_avg,
        "work_function_eV": work_function,
    })

    plt.plot(z, macro, label=f"{label} macroscopic average")
    plt.axhline(fermi, linestyle="--", linewidth=1)

plt.xlabel("z (Å)")
plt.ylabel("Electrostatic potential (eV)")
plt.title("Graphene work-function comparison")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(root / "work_function_comparison.png", dpi=200)
plt.close()

# CSV
with open(root / "work_function_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "case",
            "fermi_eV",
            "vacuum_left_eV",
            "vacuum_right_eV",
            "vacuum_avg_eV",
            "work_function_eV",
        ],
    )
    writer.writeheader()
    writer.writerows(results)

r2d = next(r for r in results if r["case"] == "with_2D")
rno = next(r for r in results if r["case"] == "without_2D")

title = "Challenge II.7 - Graphene Work Function"

lines = [
    title,
    "=" * len(title),
    "",
    "Objective",
    "---------",
    "Calculate the graphene work function from the planar/macroscopic",
    "electrostatic potential and compare calculations performed",
    "with and without the assume_isolated = '2D' setting.",
    "",
    "Method",
    "------",
    "The Quantum ESPRESSO work-function workflow was executed in two",
    "separate directories:",
    "",
    "- with_2D: calculation including assume_isolated = '2D'.",
    "- without_2D: calculation with that flag removed.",
    "",
    "The work function was evaluated as:",
    "",
    "Work Function = Vacuum Level - Fermi Level",
    "",
    "The vacuum level was estimated from the macroscopic average",
    "electrostatic potential in the left and right vacuum regions.",
    "",
    "Results",
    "-------",
    f"- With 2D correction: Fermi level = {r2d['fermi_eV']:.4f} eV,",
    f"  average vacuum level = {r2d['vacuum_avg_eV']:.4f} eV,",
    f"  work function = {r2d['work_function_eV']:.4f} eV.",
    "",
    f"- Without 2D correction: Fermi level = {rno['fermi_eV']:.4f} eV,",
    f"  average vacuum level = {rno['vacuum_avg_eV']:.4f} eV,",
    f"  work function = {rno['work_function_eV']:.4f} eV.",
    "",
    "Discussion",
    "----------",
    "The profile obtained with assume_isolated = '2D' is expected to show",
    "edge distortions near the cell boundaries due to the electrostatic",
    "treatment of the slab geometry.",
    "",
    "When the 2D isolation flag is removed, the potential profile is",
    "usually smoother in the vacuum region and can be easier to interpret",
    "for a simple symmetric graphene slab.",
    "",
    "Reported graphene work functions are commonly around 4.5-4.7 eV,",
    "although the exact value depends on the functional, slab setup,",
    "vacuum spacing, k-point sampling and numerical settings.",
    "",
    "Outputs",
    "-------",
    "- work_function_results.csv: numerical summary.",
    "- work_function_comparison.png: comparison of macroscopic potentials.",
    "- with_2D/: calculation files with 2D isolation.",
    "- without_2D/: calculation files without 2D isolation.",
    "",
]

report = "\n".join(lines)
(root / "readme.rst").write_text(report)
publish_doctree(report, settings_overrides={"halt_level": 2})

print("===== WORK FUNCTION RESULTS =====")
for r in results:
    print(
        f"{r['case']}: "
        f"EF={r['fermi_eV']:.4f} eV | "
        f"Vac={r['vacuum_avg_eV']:.4f} eV | "
        f"WF={r['work_function_eV']:.4f} eV"
    )

print()
print("Generated files:")
for name in ["work_function_results.csv", "work_function_comparison.png", "readme.rst"]:
    p = root / name
    print(f"  - {name}: {'OK' if p.exists() else 'MISSING'}")

print()
print("SUCCESS: Challenge II.7 README validated.")
