# NS-1 sparse Schur evidence

Status: DEEP for path-sparse `L` entropy recursion; no counterexample
candidate.

## Files in this directory

```text
path_schur.py
validation.json
route_note.md
evidence.md
verdict.md
```

All are under:

```text
C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo\research\R3\next_structures\sparse_schur
```

No other directory was modified by this work unit.

## Prototype

`path_schur.py` is a dependency-free standard-library prototype.  It supports:

* exact rational positive-definiteness certificate for tridiagonal path `L`
  via leading continuants;
* construction of the dense marginal kernel `K=L(I+L)^(-1)` for `n<=8`
  validation;
* direct Mobius atom probabilities from marginal `K`;
* independent L-ensemble path-run atom probabilities;
* `O(n^2)` path entropy dynamic programming using interval/run determinants;
* reduced-only `n=12` smoke test.

It uses Decimal logarithms for diagnostics.  It does not provide directed
rounding or final sign certificates.

## Command run

Python executable:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
```

Command:

```text
& 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo\research\R3\next_structures\sparse_schur\path_schur.py' `
  --self-test `
  --out 'C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo\research\R3\next_structures\sparse_schur\validation.json'
```

Exit code: `0`.

No remote command was run.  No GPU, BLAS, OpenMP, NumPy, or SciPy was used.

## Validation summary

The generated [validation.json](validation.json) reports:

```text
status = PASS
```

Direct validation 1:

```text
name = heterogeneous_path_n6
n = 6
events_checked = 64
mobius_sum = 1
l_ensemble_sum = 1
mismatch_count = 0
min_atom = 20003760/9294488377
entropy_abs_diff = 4E-89
Z = 9294488377/20003760
```

Direct validation 2:

```text
name = heterogeneous_path_n8
n = 8
events_checked = 256
mobius_sum = 1
l_ensemble_sum = 1
mismatch_count = 0
min_atom = 3077443495526400/7139781485523238273
entropy_abs_diff = 2E-89
Z = 7139781485523238273/3077443495526400
```

Reduced-only smoke:

```text
n = 12
state_count = 78
full_events = 4096
Z = det(I+L)
entropy = 8.016446877766049101192628361605617771518371554317588584839654406297372
```

The equality `Z=det(I+L)` is exact in the JSON:

```text
59244255080670167824998909954413/851312961027809280000000000
```

## What the validation proves

For the two `n<=8` cases, every exact atom probability agrees as a rational
number between:

```text
1. direct Mobius inversion from marginal K;
2. direct L-ensemble formula det(L_S)/det(I+L);
3. path run factorization of det(L_S).
```

This catches the main semantic failure mode: using inclusion determinants
`det K_S` as exact event probabilities.

The `n=12` smoke test demonstrates the intended complexity reduction:

```text
78 path interval determinants instead of 4096 event atoms.
```

It is not a gap certificate and not a theorem about all low-treewidth kernels.

## Failed or held branches

Attempt denominator for this work unit:

```text
path-sparse L             -> DEEP
generic sparse marginal K -> HOLD
generic tree-sparse L     -> HOLD
arbitrary arrowhead L     -> HOLD
```

Blockers:

* Sparse marginal `K` path keeps off-diagonal couplings in
  `det(K-I_{S^c})`; generic prefix continuant states do not collapse to a
  finite alphabet.
* Generic tree-sparse `L` requires messages carrying effective Schur
  complements; no polynomial exact entropy state space was proved here.
* Arbitrary arrowhead `L` reduces to subset-sum logarithms unless extra
  repeated or discrete weight structure is imposed.
* Marginal-kernel affine chords are not closed under path-sparse `L`.

## Reproducibility and safety notes

No `C:\canglan\` path was accessed.  No sub-agent was spawned.  No process was
started or stopped on the remote server.  No search was expanded beyond the
self-test cases above.

Finite validation is implementation evidence only.  It is not a certification
of real DPP entropy concavity or nonconcavity.
