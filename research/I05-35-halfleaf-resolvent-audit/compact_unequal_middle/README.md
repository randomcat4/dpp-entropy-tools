# I05-35 continuation: exact compact unequal-strength middle

Status: **PROVED BY AUTHOR WITH AN EXACT CONTINUUM CERTIFICATE / PENDING INDEPENDENT REVIEW**. This continuation is new relative to PR120/PR124 and is not covered by PR132. It does not repeat the equal-strength theorem or the punctured small-edge theorem.

The authoritative reading order for the duplicate predecessor packets is `../AUTHORITY_ORDER_PR120_PR124.md`. Current `main` controls the accepted pointwise-resolvent obstruction; PR132 is the open analytic FIRST for the predecessor positive units. The present compact-middle result starts only after those boundaries.

## New theorem

Normalize the occupied rare corner of a strict half-leaf and put

```text
a=A/q, b=B/q.
```

For every

```text
1/4 <= a <= 4, 1/4 <= b <= 4,
```

the exact integrated occupied-side complete-event Hessian `G1''` is positive definite in all six real-symmetric physical directions. No pointwise-in-`r` resolvent assertion is used.

Consequently, for every strict physical half-leaf with

```text
1/4 <= A/q, B/q, A/qbar, B/qbar <= 4,
qbar=1-A-B-q,
```

both integrated one-sided forms are positive definite and the full eight-event Shannon Hessian is strictly negative in every nonzero physical direction. This is a genuine compact unequal-strength region; for example `A=3/20`, `B=1/4`, `q=qbar=3/10` lies in it and has `A!=B`.

## Certificate

The proof uses the exact six-dimensional block

```text
M(a,b)=[[Y,C^T],[C,L]],
E(a,b)=L-C Y^(-1) C^T.
```

It maps `r=a/(1+a)` and `s=b/(1+b)` to `[1/5,4/5]^2`, partitions each axis into 32 rational intervals, and covers all 1024 boxes. On every box all logarithms and matrix entries are enclosed by exact outward interval arithmetic. A rational triangular preconditioner is then checked to make the whole interval family strictly diagonally dominant with positive diagonal. Gershgorin therefore proves `M(a,b)>0` at every point of every box, hence `E(a,b)>0`.

The fixed logarithm enclosure uses 56 positive atanh terms and its exact geometric tail; arithmetic is rounded outward after every operation to a `2^-140` lattice. The smallest certified preconditioned Gershgorin margin is the positive exact fraction printed in the retained output.

## Evidence boundary

- `proof.md`: self-contained reduction, continuum certificate, physical full-Shannon corollary, and scope.
- `code/verify_compact_unequal_middle.py`: standard-library-only certificate generator/checker.
- `output/verify_compact_unequal_middle.txt`: literal final fixed-input output.
- `failure_ledger.md`: method, computation, and quantifier boundaries.

Recorded final run: Python 3.13.5, Linux x86_64, one process, no GPU; script wall time about 3.26 seconds, external user+system CPU about 4.26 seconds, peak RSS below 95 MiB. No previous PR checker or computation budget was reused. The floating midpoint Cholesky only proposes a dyadic rational preconditioner; every accepted inequality is subsequently checked by exact integer interval arithmetic.

No novelty or formal-verification claim is made. The all-positive-strength quadrant, unequal leaf diagonals beyond already reviewed local persistence, general missing-edge concavity, and general real three-point concavity remain open.
