# General family verdict

AUTHOR STATUS: PROVED_FOR_CLOSURE / SCOUT_FOR_GAP.

This is an author/generalizer verdict.  It is not a fresh independent
`CORRECT` verification.

## Strongest result

The previous n=3 and n=4 fixed-beta construction has been promoted to an
arbitrary-dimensional exact theorem.

For every \(n\ge2\), there are rational, connected, heterogeneous, SPD
tridiagonal matrices

\[
L_-,L_0,L_+
\]

such that

\[
\Phi(L_0)=\frac{\Phi(L_-)+\Phi(L_+)}2,
\qquad
\Phi(L)=L(I+L)^{-1}.
\]

Moreover, the construction gives a whole open convex parameter domain

\[
\Omega_\beta=\{\tau>0:R^{-1}\operatorname{diag}(\tau)R^{-T}\prec I\}
\]

on which \(K(\tau)=\Phi(L(\tau))\) is affine in \(\tau\).  The perturbation
rank is exactly the number of changed innovation coordinates:

\[
\operatorname{rank}(K(\tau^+)-K(\tau^-))
=\#\{i:\tau_i^+\ne\tau_i^-\}.
\]

Thus generic chords in this family are full-rank, while one-coordinate
directions are precisely rank-one and fall under the Gu prior-art blocker
recorded by the parent task.

## Files

- `theorem.md`: exact arbitrary-n theorem, proof, rational existence
  corollary, rank formula.
- `derivation.md`: \(\tau\)-coordinate first/second derivative structure and
  the \(O(n^2)\) directional-jet DP interface.
- `search.py`: deterministic finite scout search over n=5..30.
- `search_results.json`: generated finite evidence.
- `verdict.md`: this summary.

## Finite search result

Command:

```text
python search.py --n-min 5 --n-max 30 --trials 160 --seed 20260908 --out search_results.json
```

Exit code: `0`.

The search used three direction buckets for every dimension:

```text
rank1, rank2, full_rank
```

and evaluated `4160` feasible chords in each bucket across n=5..30.  It also
performed an n=5 exact-Möbius reuse smoke through the existing NS-1
`path_schur.py`; mismatch count was `0`, and the float-vs-exact entropy
difference was about `9.99e-16`.

No positive scout gap above `1e-10` was found.

Best finite value:

```text
n = 30
bucket = rank2
Delta = -1.8402479120993576e-05
```

The sign convention is

\[
\Delta=\frac{H(K_-)+H(K_+)}2-H(K_0).
\]

Positive \(\Delta\) would violate concavity.  The finite search did not find
one.

## Mechanism learned

The \(\tau\)-coordinates decompose the K perturbation into rank-one pieces:

\[
\partial_{\tau_i}K=-u_i u_i^T.
\]

Consequently, single-coordinate curvature is nonpositive by the recorded Gu
rank-one blocker.  A positive gap inside this family, if it exists, must come
from mixed Hessian terms involving at least two innovation coordinates.

The derivation file gives the exact atom-level Hessian formula and an
\(O(n^2)\) path-DP route for directional first and second derivatives by
propagating second-order jets through the continuant/run recurrence.

## Nonclaims

- No R3 counterexample is claimed.
- No finite search miss is promoted to a no-go theorem.
- No interval-certified positive gap exists in this output.
- No claim is made that all path-affine innovation chords are concave.
- No claim is made beyond the stated fixed-beta/unit-bidiagonal family.

## Remaining gaps

1. Independent verification of `theorem.md`, especially the arbitrary-n
   rational existence corollary and rank formula.
2. Implement the \(O(n^2)\) second-order jet DP from `derivation.md`; current
   search uses finite chord values, not exact Hessian propagation.
3. If a later search finds positive Decimal/float scout gaps, certify strict
   feasibility and entropy sign by outward-rounded intervals before promoting
   any candidate.
