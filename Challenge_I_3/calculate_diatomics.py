import csv
from pathlib import Path
from ase import Atoms
from ase.optimize import BFGS
from mace.calculators import mace_mp

systems = {'O2': ('O', 1.21, 5.17), 'F2': ('F', 1.42, 1.60), 'H2': ('H', 0.74, 4.52)}
print('Loading MACE-MP medium model...', flush=True)
calc = mace_mp(model='medium', device='cpu', default_dtype='float64')
rows = []

for name, (element, distance, reference) in systems.items():
    print(f'\nCalculating {name}...', flush=True)
    try:
        atom = Atoms(element, calculator=calc)
        e_atom = atom.get_potential_energy()
        molecule = Atoms(element * 2, positions=[(0, 0, 0), (0, 0, distance)], calculator=calc)
        optimizer = BFGS(molecule, logfile=None)
        converged = optimizer.run(fmax=0.05, steps=100)
        bond = molecule.get_distance(0, 1)
        e_molecule = molecule.get_potential_energy()
        e_atomization = 2 * e_atom - e_molecule
        row = {'molecule': name, 'bond_length_A': f'{bond:.5f}', 'atomization_eV': f'{e_atomization:.5f}', 'reference_eV': reference, 'converged': converged, 'steps': optimizer.nsteps}
        rows.append(row)
        print(row, flush=True)
    except Exception as exc:
        print(f'FAILED {name}: {exc}', flush=True)

if rows:
    with open('results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

lines = ['Challenge I.3 - Atomization Energies of Diatomic Molecules', '==========================================================', '', 'Objective', '---------', 'Extend the course N2 atomization-energy example to O2, F2, and H2.', '', 'Method', '------', 'ASE geometry optimization using the pretrained MACE-MP medium model on CPU.', 'The atomization energy is E_atomization = 2*E_atom - E_molecule.', 'BFGS convergence criterion: maximum force below 0.05 eV/Angstrom.', '', 'Results', '-------', '']
for r in rows:
    lines.append(f"- {r['molecule']}: bond length {r['bond_length_A']} Angstrom; atomization energy {r['atomization_eV']} eV; reference approximately {r['reference_eV']} eV; converged: {r['converged']}.")

lines += ['', 'Discussion', '----------', 'The computed values are model predictions and may differ from experimental dissociation energies. Spin states and isolated-atom reference energies require care for quantitative benchmarking. See results.csv and calculate_diatomics.log for full records.', '']
Path('readme.rst').write_text('\n'.join(lines))
print('\nSaved results.csv and readme.rst', flush=True)
