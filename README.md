# Molecular and Materials Modeling — Computational Exercises

This repository contains 16 computational exercises completed as part of
a molecular and materials modeling learning project, based on the
*Molecular and Materials Modeling — August 2026* course materials.

The exercises cover electronic-structure calculations, molecular
simulation, geometry optimization, convergence testing, density of
states, work functions, and surface adsorption.

## Computational Tools

- Quantum ESPRESSO 7.5
- Atomic Simulation Environment (ASE)
- Python, NumPy, Matplotlib
- MACE machine-learning interatomic potentials
- NWChem
- MOPAC
- Additional tools used in individual exercises

Calculations were performed in a Linux environment using WSL2.
Each challenge directory includes its own README and relevant
scripts, inputs, results, and/or figures.

## Part I — Molecular Modeling

| Exercise | Topic |
|---|---|
| [I.1](Challenge_I_1/) | Software installation and initial tests |
| [I.2](Challenge_I_2/) | Computational performance comparisons |
| [I.3](Challenge_I_3/) | Diatomic molecules with MACE |
| [I.4](Challenge_I_4/) | Interatomic potentials and molecular geometry |
| [I.5](Challenge_I_5/) | Molecular thermochemistry |
| [I.6](Challenge_I_6/) | Methane C–H bond dissociation |
| [I.7](Challenge_I_7/) | Methane geometry optimization with Quantum ESPRESSO |
| [I.8](Challenge_I_8/) | Uranium-containing molecular complex |

## Part II — Materials Modeling

| Exercise | Topic |
|---|---|
| [II.1](Challenge_II_1/) | Silicon total-energy calculations |
| [II.2](Challenge_II_2/) | Silicon convergence testing |
| [II.3](Challenge_II_3/) | Silicon structure and cell relaxation |
| [II.4](Challenge_II_4/) | Silicon electronic properties and DOS |
| [II.5](Challenge_II_5/) | Aluminum electronic properties and DOS |
| [II.6](Challenge_II_6/) | Graphene and two-dimensional materials |
| [II.7](Challenge_II_7/) | Graphene work-function calculations |
| [II.8](Challenge_II_8/) | Hydrogen adsorption on graphene |

## Selected Results

### Silicon and Aluminum

Silicon convergence, cell-relaxation and electronic-property
calculations were performed using Quantum ESPRESSO.

For aluminum, an FCC structure was optimized and its electronic
density of states was compared with that of silicon.

### Graphene

Graphene convergence tests and constrained in-plane relaxation
were performed. Orbital-projected DOS analysis showed that
carbon pz orbitals dominate the electronic states near the
Fermi level in the calculated graphene system.

### Graphene Work Function

Two electrostatic-potential calculations were compared:

| Setting | Calculated work function |
|---|---:|
| With 2D isolation | 4.2872 eV |
| Without 2D isolation | 4.2403 eV |

The calculation without 2D isolation produced a flatter
vacuum-potential plateau in the investigated geometry.

### Hydrogen Adsorption

Spin-polarized DFT-D3 calculations were performed for
hydrogen adsorption on graphene supercells.

| System | Cutoff | Binding energy |
|---|---:|---:|
| H@C8 | 80 Ry | 2.863900 eV |
| H@C8 | 100 Ry | 2.863853 eV |
| H@C18 | 100 Ry | 3.582131 eV |

The binding-energy difference between the two supercell
sizes indicates that supercell-size effects remain important.


### Graphene DOS k-Point Comparison

Additional SCF, NSCF, and DOS calculations were completed
for 12x12x1, 18x18x1, and 20x20x1 k-point grids and
compared against the previously calculated 24x24x1 grid.

The DOS curves, Fermi-energy alignment, numerical summary,
and computational inputs are provided in `Challenge_II_6`.

### Mercury Adsorption on Graphene

Hg adsorption on C18 was evaluated at three adsorption sites
using Quantum ESPRESSO with DFT-D3 dispersion corrections.

| Adsorption site | Adsorption energy |
|---|---:|
| On-top | -0.237229 eV |
| On-bridge | -0.237522 eV |
| On-hollow | -0.239897 eV |

For these site-specific comparisons, the carbon geometry and
Hg lateral coordinates were held fixed while the Hg height
was optimized. All three constrained optimizations converged.

The hollow site yielded the lowest calculated adsorption
energy under these constraints. The small energy differences
should not be interpreted as a definitive site preference
without further convergence testing.

## Reproducibility

The computational procedures are documented in the
corresponding challenge directories.

Large temporary simulation files, wavefunction files,
and Quantum ESPRESSO restart data are excluded from
this repository to reduce storage requirements.

Pseudopotential files are required to reproduce the
Quantum ESPRESSO calculations. Users should obtain
the relevant compatible pseudopotentials and adjust
their local executable and pseudopotential paths
before running the scripts.

Some scripts preserve machine-specific executable
paths from the original computational environment
and may require adaptation.

## Limitations and Further Work

These exercises demonstrate computational workflows
rather than fully converged, publication-ready studies.

Further validation may include:

- Additional k-point and cutoff convergence testing.
- Independent verification of experimental crystal structures.
- Additional adsorption geometries and larger supercells.
- More extensive comparison with published reference data.

Calculated values should therefore be interpreted within
the stated computational approximations.

## Acknowledgment

The exercises are based on the educational materials of
the Molecular and Materials Modeling course (August 2026).

For details of each calculation, consult the README
inside the corresponding challenge directory.
