# D10-U5 run log

Date: 2026-09-08.

No server, no GPU, no dependency installation, no random search, no subagents.
Only this U5 directory was written.

Command from repository root:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research\R3\deepening_10h\dense_hessian\connected_puncture_distance\connected_distance_scout.py
```

Final exit code: 0.

Output:

```text
research/R3/deepening_10h/dense_hessian/connected_puncture_distance/scout_results.json
```

Script SHA256:

```text
6edbc8eb33bee157c1c10c8bf468bba8aabceb4d0d551c630abb19ab3c4afdd6
```

## Exact denominators

- P4 full off-diagonal scaled Hessian:
  - 16 exact atom polynomials.
  - Entropy through total off-diagonal degree 8.
  - 64 retained entropy monomials.
  - The scaled 6 by 6 off-diagonal limit is diagonal and strictly negative.
- n=4 full connected labelled graph scout:
  - all 38 connected labelled graphs on four vertices;
  - one deterministic nonzero rational support-weight assignment per graph;
  - exact fraction LDL check of the negative scaled off-diagonal limiting
    matrix passed for all 38.
- shortest-path diagonal coefficient scout:
  - all 38 connected labelled n=4 graphs;
  - all 6 coordinate pairs per graph, 228 exact two-variable targets;
  - selected n=5 graphs: P5 path, C5 cycle, diameter-3 branched tree, and K2,3;
  - all 10 coordinate pairs per selected n=5 graph, 40 exact two-variable
    targets;
  - each target used exact Möbius atoms: 16 atoms for n=4, 32 atoms for n=5;
  - all targets matched the candidate `epsilon^(2d)` shortest-path coefficient.

## P4 scaled constants

For

```text
x=(1/5,1/3,3/5,3/4),
A12=1/3, A23=-2/5, A34=3/7,
edge order=(12),(13),(14),(23),(24),(34),
```

the scaled off-diagonal limiting diagonal is

```text
(-75/4, -25/2, -600/49, -18, -864/49, -1200/49).
```

These fractions are sanity values.  The P4 proof candidate is stated for
arbitrary strict `x` and nonzero path weights.

## Discarded numerical probe

An initial naive double-precision finite-difference Hessian probe at
`epsilon=0.002` produced small positive maximum eigenvalues for many connected
graphs.  This was discarded as a numerical-method failure: the expected
distance-three and distance-four curvatures are of order `epsilon^6` and
`epsilon^8`, far below the finite-difference/roundoff scale.  No such float
probe is used in the verdict.
