Challenge II.7 - Graphene Work Function
=======================================

Objective
---------
Calculate the graphene work function from the vacuum level
and the Fermi energy, and compare calculations performed
with and without the 2D isolation setting.

Method
------
A graphene slab was treated with Quantum ESPRESSO.
The electrostatic potential was extracted using pp.x,
and the planar/macroscopic averages were obtained using
average.x. The work function was computed as

Work Function = Vacuum Level - Fermi Level.

The vacuum level was estimated from the macroscopic
average potential using left and right vacuum windows
at 2-4 Å and 11-13 Å along the z direction.

Results
-------
- with_2D:
  - Fermi energy = -4.2405 eV
  - Left vacuum level = 0.0467 eV
  - Right vacuum level = 0.0467 eV
  - Average vacuum level = 0.0467 eV
  - Left vacuum range = 0.2920 eV
  - Right vacuum range = 0.2920 eV
  - Work function = 4.2872 eV

- without_2D:
  - Fermi energy = -1.7174 eV
  - Left vacuum level = 2.5229 eV
  - Right vacuum level = 2.5229 eV
  - Average vacuum level = 2.5229 eV
  - Left vacuum range = 0.0017 eV
  - Right vacuum range = 0.0017 eV
  - Work function = 4.2403 eV

Discussion
----------
The calculation without the 2D isolation setting produced
a much flatter vacuum plateau than the calculation with
the 2D setting.

The recommended value is therefore the result from ``without_2D``, giving a work function of 4.2403 eV.

Both calculated work functions are consistent with the
expected literature range for graphene, approximately
4.2-4.6 eV.

The result with 2D isolation still gives a similar work
function, but its vacuum region is visibly distorted,
which makes it less reliable for vacuum-level analysis.

Outputs
-------
- work_function_results.csv: numerical summary
- work_function_comparison.png: electrostatic potential comparison
- with_2D/: calculation files with 2D isolation
- without_2D/: calculation files without 2D isolation
