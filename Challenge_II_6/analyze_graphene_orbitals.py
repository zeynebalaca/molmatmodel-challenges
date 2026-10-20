from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path.cwd()
folder = root / "electronic"
fermi = float((folder / "fermi_energy.txt").read_text().strip())

pfiles = sorted(folder.glob("graphene_pdos.pdos_atm*_*wfc#2(p)"))
if len(pfiles) != 2:
    raise RuntimeError(f"Expected 2 carbon p-PDOS files; found {len(pfiles)}")

total = None

for f in pfiles:
    data = np.loadtxt(f, comments="#")
    if data.ndim != 2 or data.shape[1] < 5:
        raise RuntimeError(f"Unexpected PDOS columns: {f.name}")
    if total is None:
        total = data.copy()
    else:
        if not np.allclose(data[:, 0], total[:, 0]):
            raise RuntimeError("PDOS energy grids do not match.")
        total[:, 1:] += data[:, 1:]

energy = total[:, 0] - fermi

# QE p-orbital ordering for the non-spin-polarized case:
# column 0: energy, 1: total p, 2: pz, 3: px, 4: py.
pz, px, py = total[:, 2], total[:, 3], total[:, 4]

plt.figure(figsize=(9, 5))
plt.plot(energy, pz, label="pz (out-of-plane)")
plt.plot(energy, px, label="px (in-plane)")
plt.plot(energy, py, label="py (in-plane)")
plt.axvline(0, color="black", linestyle="--", linewidth=1)
plt.xlabel("Energy relative to Fermi level (eV)")
plt.ylabel("PDOS (states/eV/cell)")
plt.title("Graphene: Carbon p-Orbital Contributions")
plt.xlim(-6, 6)
plt.legend()
plt.tight_layout()
plt.savefig(root / "graphene_p_orbitals.png", dpi=200)
plt.close()

tdos = np.loadtxt(folder / "graphene_tdos.dat", comments="#")
plt.figure(figsize=(9, 5))
plt.plot(tdos[:, 0] - fermi, tdos[:, 1], label="Graphene TDOS")
plt.axvline(0, color="black", linestyle="--", linewidth=1)
plt.xlabel("Energy relative to Fermi level (eV)")
plt.ylabel("TDOS (states/eV/cell)")
plt.title("Graphene Total Density of States")
plt.xlim(-6, 6)
plt.legend()
plt.tight_layout()
plt.savefig(root / "graphene_tdos.png", dpi=200)
plt.close()

mask = (energy >= -1.0) & (energy <= 1.0)
weights = {
    "pz": float(np.trapezoid(pz[mask], energy[mask])),
    "px": float(np.trapezoid(px[mask], energy[mask])),
    "py": float(np.trapezoid(py[mask], energy[mask]))
}
summed = sum(weights.values())

print("===== GRAPHENE ORBITAL ANALYSIS =====")
print(f"Fermi energy: {fermi:.4f} eV")
print("Integrated p-orbital contributions within EF +/- 1 eV:")

for orbital, value in weights.items():
    percentage = 100 * value / summed if summed > 0 else float("nan")
    print(f"{orbital}: {value:.6f} states ({percentage:.2f}%)")

print("\n===== GENERATED PLOTS =====")
for f in ("graphene_p_orbitals.png", "graphene_tdos.png"):
    print(f, "OK" if (root / f).exists() else "MISSING")

print("\n===== AVAILABLE SILICON PDOS FILES =====")
si = Path.home() / "challenges/Challenge_II_4"
matches = list(si.rglob("*pdos_atm*"))
for f in matches[:10]:
    print(f)
if not matches:
    print("No silicon atom-projected PDOS files found under Challenge_II_4.")
