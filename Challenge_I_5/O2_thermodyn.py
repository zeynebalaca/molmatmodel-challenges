from pathlib import Path
from ase.build import molecule
from ase.calculators.emt import EMT
from ase.optimize import QuasiNewton
from ase.thermochemistry import IdealGasThermo
from ase.vibrations import Vibrations

atoms = molecule('O2')
atoms.calc = EMT()

opt = QuasiNewton(atoms, logfile='O2_optimization.log')
converged = opt.run(fmax=0.01, steps=200)

energy = atoms.get_potential_energy()
bond_length = atoms.get_distance(0, 1)

vib = Vibrations(atoms, name='O2_vib')
vib.run()
vib_energies = vib.get_energies()
vib.summary(log='O2_vibrations.log')

thermo = IdealGasThermo(
    vib_energies=vib_energies,
    potentialenergy=energy,
    atoms=atoms,
    geometry='linear',
    symmetrynumber=2,
    spin=1
)

T = 298.15
P = 101325.0

H = thermo.get_enthalpy(temperature=T, verbose=False)
S = thermo.get_entropy(temperature=T, pressure=P, verbose=False)
G = H - T*S

print(f"Optimization converged: {converged}")
print(f"Optimized O-O distance: {bond_length:.6f} Angstrom")
print(f"Potential energy: {energy:.6f} eV")
print(f"Enthalpy H: {H:.6f} eV")
print(f"Entropy S: {S:.9f} eV/K")
print(f"Gibbs energy G: {G:.6f} eV")

results = f"""Challenge I.5 - Oxygen Molecule Thermochemistry
================================================

Objective
---------
Adapt the original N2 thermochemistry example to O2.

Method
------
ASE with the EMT calculator was used for O2 geometry optimization,
finite-difference vibrations and ideal-gas thermochemistry.
The electronic spin was set to 1 (triplet oxygen) and the
rotational symmetry number to 2.
Temperature: {T} K. Pressure: {P} Pa.

Results
-------
- Optimization converged: {converged}
- Optimized O-O bond length: {bond_length:.6f} Angstrom
- Potential energy: {energy:.6f} eV
- Enthalpy H: {H:.6f} eV
- Entropy S: {S:.9f} eV/K
- Gibbs energy G = H - TS: {G:.6f} eV

Discussion
----------
These are model-dependent thermochemical estimates.
The calculated enthalpy is not the standard enthalpy of formation.
EMT is a simplified empirical potential and may not accurately
describe the electronic structure and vibrations of triplet O2.
Original N2 input and calculation logs are retained.
"""
Path('readme.rst').write_text(results)

from docutils.core import publish_doctree
publish_doctree(results, settings_overrides={'halt_level': 2})
print("SUCCESS: Challenge I.5 README validated.")
