# P1 signed-cycle pilot

Status: `SCOUT_COMPLETE`; finite numerical evidence only.
Compute process 157823 exited 0, Python 3.12.3, NumPy 2.5.3, one thread.
Full hashes, command and timing: [manifest](pilot_results/manifest.json).

At diagonal `(0.13,0.37,0.63,0.86)`, fix positive edges 01,02,03 as
a spanning-tree gauge. Enumerate all signs of the remaining three K4
edges, or two diamond edges. This covers 8 and 4 gauge classes respectively
for these fixed labeled edge magnitudes. It does not quotient vertex
permutations because their unequal diagonals and edge magnitudes are fixed.
Each has radial off-diagonal fractions 0.2,0.7,0.97 of the maximal symmetric
strict-contraction radius about its diagonal midpoint.

For each of 36 midpoints, compute the entire Hessian in a Frobenius-orthonormal
symmetric basis. Record the top direction, its endpoint feasibility radius,
three affine chords at 0.1,0.5,0.9 of that radius, all 16 event jets and eight
complementary event pairs. Also record a separately Fisher-whitened direction.
Coverage: 36 study Hessians + one smoke Hessian, 108 study chords, 576 event
rows. The smoke determinant/Mobius event discrepancy is 5.56e-17; its
directional Hessian agrees with finite differences to 4.16e-8.

- Largest Frobenius-normalized curvature: -0.0003775804243707932.
- Largest supported Fisher/acceleration ratio: 0.26671853457306155.
- Largest chord gap: -0.00000469876908670841.
- Positive curvature candidates above 1e-9: zero.

The least-negative direction almost entirely fills the missing diamond edge
23. Its Fisher and acceleration contributions are both negative, approximately
-0.0002517245 and -0.0001258559. Thus its small curvature is not evidence that
positive event acceleration nearly dominates Fisher. This distinction matters
when choosing a refinement objective.

The Fisher ratio uses a numerical support threshold and is not a rigorous
full-space bound. The pilot does not cover unequal spectral disappearance
rates. The next adaptive unit changes eigenvalue scales and moving frames;
independent exact arithmetic reviews selected frozen fixtures.
