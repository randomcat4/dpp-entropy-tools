# D10-B verdict

Status: `DEEP`.

FT-B's existence side is resolved in this work unit by explicit exact rational
triples for `n=3` and `n=4`.  This is a closure result for path-sparse
`L`-ensemble entropy evaluation along a genuine affine chord in marginal
kernel `K` space.  It is not an R3 entropy nonconcavity counterexample.

## Main conclusion

Let

```text
Phi(L)=L(I+L)^(-1).
```

The directory contains an exact construction of non-all-identical, connected,
heterogeneous, SPD tridiagonal matrices

```text
L_-, L_0, L_+
```

such that

```text
Phi(L_0) = (Phi(L_-) + Phi(L_+))/2.
```

The proof uses `S=(I+L)^(-1)`, where `Phi(L)=I-S`.  A fixed path Markov
precision factorization makes `S` affine while `S^(-1)-I` remains
tridiagonal.

## Evidence files

- `approach.md`: derivation, proof boundaries, complexity, and prior-art
  blocker.
- `search_or_algebra.py`: reproducible exact rational construction and checks.
- `evidence.json`: generated check output.

All files are under the assigned route directory only.

## Certificate summary

From `evidence.json`:

```text
overall status = PASS
n=3 K midpoint exact = true
n=4 K midpoint exact = true
n=3 L0 is endpoint-average L = false
n=4 L0 is endpoint-average L = false
n=3 rank(K_+ - K_-) = 3
n=4 rank(K_+ - K_-) = 4
all direct Mobius validations pass = true
```

Every FT-B shape condition is checked exactly:

```text
tridiagonal = true
connected nonzero adjacent edges = true
heterogeneous diagonal = true
L SPD by exact leading continuants = true
Phi(L)=I-(I+L)^(-1) cross-check = true
```

## Entropy gap result

Using the existing NS-1 path entropy recurrence after the triples were found,
the Decimal scout gaps are:

```text
n=3 Delta = -0.00045556980402948637966202904966273876636359662215010218795433969502053929872088544141161521326441
n=4 Delta = -0.00084150938797292809775272697635216508407540691808349059968484019798488667772598963986582249100154
```

The sign convention is `Delta = endpoint average - midpoint`.  These values
are negative, so they support concavity along these two chords and give no
R3 counterexample candidate.  Since no positive scout gap was found, no
outward-rounded interval sign certificate was attempted.

## Relation to the Gu blocker

The parent task supplied the prior-art blocker:

```text
Yuzhou Gu, Entropy of Determinantal Point Processes,
Theorem 7 / Corollary 6:
rank-one K-space directions and chords from 0 to K are concavity directions.
```

This work does not reprove or rely on that theorem as a black box.  It only
records the obstruction.  The constructed D10-B perturbations are full-rank in
the tested dimensions, not rank-one, and are not chords from the origin.

## Nonclaims

- No strict positive entropy gap is claimed.
- No finite numerical check is promoted to a global theorem.
- No claim is made about all path-sparse `L` chords having negative gap.
- No claim is made about all real symmetric DPP entropy.
- No exhaustive search or nonexistence theorem is claimed.

## Minimum remaining obligations

1. Fresh non-author verification of the algebraic construction and the exact
   certificates in `evidence.json`.
2. If future search finds a positive scout gap in this family, add
   outward-rounded logarithm intervals before calling it a strict gap.
3. If this route is scaled to larger n, keep recording perturbation rank so
   rank-one prior-art blockers are not accidentally retested.
