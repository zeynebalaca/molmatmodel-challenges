from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from docutils.core import publish_doctree

root = Path.cwd()
elec = root / "electronic"
si_root = Path.home() / "challenges" / "Challenge_II_4" / "baseline"

# -------------------------------
# Helpers
# -------------------------------
def load_average_pdos(files):
    total = None
    for f in files:
        data = np.loadtxt(f, comments="#")
        if total is None:
            total = data.copy()
        else:
            total[:, 1:] += data[:, 1:]
    total[:, 1:] /= len(files)
    return total

# -------------------------------
# Graphene data
# -------------------------------
fermi_g = float((elec / "fermi_energy.txt").read_text().strip())

g_p_files = sorted(elec.glob("graphene_pdos.pdos_atm#*(C)_wfc#2(p)"))
if len(g_p_files) < 2:
    raise RuntimeError("Graphene p-PDOS files not found.")

g_data = load_average_pdos(g_p_files)
g_E = g_data[:, 0] - fermi_g
g_pz = g_data[:, 2]
g_px = g_data[:, 3]
g_py = g_data[:, 4]

g_tdos = np.loadtxt(elec / "graphene_tdos.dat", comments="#")
g_tE = g_tdos[:, 0] - fermi_g
g_tY = g_tdos[:, 1]

mask_g = (g_E >= -1.0) & (g_E <= 1.0)
g_int_pz = float(np.trapezoid(g_pz[mask_g], g_E[mask_g]))
g_int_px = float(np.trapezoid(g_px[mask_g], g_E[mask_g]))
g_int_py = float(np.trapezoid(g_py[mask_g], g_E[mask_g]))
g_sum = g_int_pz + g_int_px + g_int_py

# -------------------------------
# Silicon data
# -------------------------------
# Fallback from previously verified output
fermi_si = 6.3118

si_p_files = sorted((si_root / "pdos_results").glob("pdos.pdos_atm#*(Si)_wfc#2(p)"))
if len(si_p_files) < 2:
    raise RuntimeError("Silicon p-PDOS files not found.")

si_data = load_average_pdos(si_p_files)
si_E = si_data[:, 0] - fermi_si
si_pz = si_data[:, 2]
si_px = si_data[:, 3]
si_py = si_data[:, 4]

si_tdos = np.loadtxt(si_root / "total_dos.dat", comments="#")
si_tE = si_tdos[:, 0] - fermi_si
si_tY = si_tdos[:, 1]

mask_si = (si_E >= -1.0) & (si_E <= 1.0)
si_int_pz = float(np.trapezoid(si_pz[mask_si], si_E[mask_si]))
si_int_px = float(np.trapezoid(si_px[mask_si], si_E[mask_si]))
si_int_py = float(np.trapezoid(si_py[mask_si], si_E[mask_si]))
si_sum = si_int_pz + si_int_px + si_int_py

# -------------------------------
# Plot 1: orbital comparison
# -------------------------------
fig, axes = plt.subplots(2, 1, figsize=(9, 8), sharex=True)

axes[0].plot(g_E, g_pz, label="pz")
axes[0].plot(g_E, g_px, label="px")
axes[0].plot(g_E, g_py, label="py")
axes[0].axvline(0, linestyle="--", linewidth=1)
axes[0].set_title("Graphene: Carbon p-orbital PDOS")
axes[0].set_ylabel("PDOS (states/eV/atom)")
axes[0].set_xlim(-6, 6)
axes[0].legend()

axes[1].plot(si_E, si_pz, label="pz")
axes[1].plot(si_E, si_px, label="px")
axes[1].plot(si_E, si_py, label="py")
axes[1].axvline(0, linestyle="--", linewidth=1)
axes[1].set_title("Silicon: Si p-orbital PDOS")
axes[1].set_xlabel("Energy relative to Fermi level (eV)")
axes[1].set_ylabel("PDOS (states/eV/atom)")
axes[1].set_xlim(-6, 6)
axes[1].legend()

plt.tight_layout()
plt.savefig(root / "graphene_vs_si_p_orbitals.png", dpi=200)
plt.close()

# -------------------------------
# Plot 2: TDOS comparison
# -------------------------------
plt.figure(figsize=(9, 5))
plt.plot(g_tE, g_tY, label="Graphene TDOS")
plt.plot(si_tE, si_tY, label="Silicon TDOS")
plt.axvline(0, linestyle="--", linewidth=1)
plt.xlim(-6, 6)
plt.xlabel("Energy relative to Fermi level (eV)")
plt.ylabel("DOS (states/eV/cell)")
plt.title("Graphene vs Silicon TDOS")
plt.legend()
plt.tight_layout()
plt.savefig(root / "graphene_vs_si_tdos.png", dpi=200)
plt.close()

# -------------------------------
# Build README
# -------------------------------
title = "Challenge II.6 - Graphene: 2D Convergence, Relaxation and Electronic Properties"

report = f"""{title}
{'=' * len(title)}

Objective
---------
Study graphene as a two-dimensional material using
Quantum ESPRESSO and ASE-style workflows.
The tasks included convergence testing, constrained
cell relaxation and electronic-structure analysis.

Method
------
A single graphene layer was constructed with a vacuum
spacing of 15 Angstrom along z and with
``assume_isolated = '2D'`` in the electronic workflow.

Convergence tests were performed for three wavefunction
cutoffs and several 2D k-point meshes.
A constrained cell relaxation was then carried out,
allowing only in-plane lattice relaxation.
Electronic properties were analyzed using SCF, NSCF,
DOS, projected DOS and charge-density post-processing.

Convergence Results
-------------------
Wavefunction cutoff scan at 12x12x1:
- 40 Ry: -24.00590210 Ry
- 55 Ry: -24.08273339 Ry
- 70 Ry: -24.09391003 Ry

K-point scan at 70 Ry:
- 6x6x1:  -24.09066159 Ry
- 12x12x1: -24.09391003 Ry
- 18x18x1: -24.09421340 Ry
- 20x20x1: -24.09432343 Ry
- 24x24x1: -24.09427867 Ry

The total energy stabilized as the in-plane k-point
mesh increased. For graphene, meshes divisible by three
are physically preferred because they sample the K point
properly.

Relaxed Geometry
----------------
The constrained QE relaxation converged successfully.

Final lattice vectors:
- a1 = ( 2.466425429,  0.000000000, 0.000000000 ) Angstrom
- a2 = (-1.233212714,  2.135987078, 0.000000000 ) Angstrom
- a3 = ( 0.000000000,  0.000000000, 15.000000000 ) Angstrom

Final atomic positions:
- C1 = (0.0000000000, -0.0000000000, 7.5000000000) Angstrom
- C2 = (0.0000000000,  1.4239913852, 7.5000000000) Angstrom

This gives a C-C bond length of approximately
1.42399 Angstrom.

Electronic-Structure Results
----------------------------
- Fermi energy: {fermi_g:.4f} eV
- Spilling parameter: 0.0109
- TDOS file: electronic/graphene_tdos.dat
- PDOS total file: electronic/graphene_pdos.pdos_tot
- Charge density: electronic/charge_density.cube

Orbital Analysis Near the Fermi Level
-------------------------------------
Integrated carbon p-orbital contributions within
E_F +/- 1 eV:

Graphene:
- pz: {g_int_pz:.6f} states ({100*g_int_pz/g_sum if g_sum > 0 else 0:.2f}%)
- px: {g_int_px:.6f} states ({100*g_int_px/g_sum if g_sum > 0 else 0:.2f}%)
- py: {g_int_py:.6f} states ({100*g_int_py/g_sum if g_sum > 0 else 0:.2f}%)

Silicon:
- pz: {si_int_pz:.6f} states ({100*si_int_pz/si_sum if si_sum > 0 else 0:.2f}%)
- px: {si_int_px:.6f} states ({100*si_int_px/si_sum if si_sum > 0 else 0:.2f}%)
- py: {si_int_py:.6f} states ({100*si_int_py/si_sum if si_sum > 0 else 0:.2f}%)

Discussion
----------
For graphene, the states near the Fermi level are
entirely dominated by the out-of-plane pz orbital.
This is the expected signature of the pi and pi-star
electronic states that form the Dirac-cone physics.

In contrast, silicon does not show an isolated pz-only
dominance near the Fermi level. Its bonding is three-
dimensional and sp3-like, so the p contributions are
distributed more isotropically.

Therefore, the graphene PDOS confirms the expected
two-dimensional electronic character, whereas silicon
shows a very different bonding and orbital picture.

Outputs
-------
- graphene_p_orbitals.png
- graphene_tdos.png
- graphene_vs_si_p_orbitals.png
- graphene_vs_si_tdos.png
- electronic/charge_density.cube
- electronic/lowdin.out
- electronic/graphene_tdos.dat
- electronic/graphene_pdos.pdos_tot

Reproducibility
---------------
The convergence calculations are stored in results.csv.
The relaxation outputs are stored under cell_relax/.
The electronic-structure outputs are stored under
electronic/.
"""

(root / "readme.rst").write_text(report)
publish_doctree(report, settings_overrides={"halt_level": 2})

print("===== FINAL GRAPHENE SUMMARY =====")
print(f"Graphene Fermi energy: {fermi_g:.4f} eV")
print(f"Graphene pz contribution near EF: {100*g_int_pz/g_sum if g_sum > 0 else 0:.2f}%")
print(f"Silicon pz contribution near EF: {100*si_int_pz/si_sum if si_sum > 0 else 0:.2f}%")
print()
print("Generated files:")
for name in [
    "graphene_vs_si_p_orbitals.png",
    "graphene_vs_si_tdos.png",
    "readme.rst"
]:
    print(f"  - {name}: {'OK' if (root / name).exists() else 'MISSING'}")
print()
print("SUCCESS: Challenge II.6 README validated.")
print("SUCCESS: Graphene vs Si comparison plots created.")
