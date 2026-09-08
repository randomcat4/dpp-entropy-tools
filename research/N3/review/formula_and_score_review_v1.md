# N3 formula and conditional-score review v1

STATUS: CORRECT for the explicit formula layer checked here.

STATUS: CRITICAL_GAPS for the original global theorem and for any optimizer-direction residual bound.

## Scope

This is a non-author review in `research/N3/review/`. I first checked the frozen N3 definitions against an independent implementation at local baseline `fa504ec74e16843fafc395880d7ba99b4c1d2129`. After that first formula pass, I reviewed the fixed candidate object at commit `424b4efcec0052ad8d79ac71c69b334dcfb03bb8`.

Fixed candidate blobs:

| Object | Blob |
| --- | --- |
| `research/N3/frozen_theorem_v1.md` | `3edfa72b1a5cc11db28e419b70e633b9f683aefa` |
| `research/N3/main/conditional_score_lemma_v1.md` | `7202917271534297bf6ac7527e830e50946f66fd` |
| `research/N3/main/certify_score_obstruction.py` | `b27a15fcff15a98d78b94a9d663f7b512b5bbcf7` |
| `research/N3/main/score_obstruction_certificate.json` | `f51a96cf32faf70a170824e93eeb383e380f5c22` |

I did not review any later author modification, and I did not change the frozen premises.

## Formula Layer

The eight atom formulas are correct for

```text
K = [[x,a,b],[a,y,c],[b,c,z]],
q12=xy-a^2, q13=xz-b^2, q23=yz-c^2,
r=xyz+2abc-xc^2-yb^2-za^2.
```

Independent Mobius inversion gives

```text
p123=r,
p12=q12-r, p13=q13-r, p23=q23-r,
p1=x-q12-q13+r, p2=y-q12-q23+r, p3=z-q13-q23+r,
p0=1-x-y-z+q12+q13+q23-r.
```

The six-coordinate first and second jets check out with the convention
`(11,22,33,12,13,23)`, where an off-diagonal coordinate is the symmetric
direction `Eij+Eji`. The off-diagonal factor is therefore real: for example
`d det(K)[E12+E21]=2(K13 K23-K33 K12)`, not the single-entry cofactor. The
same convention gives

```text
eta_12 = 2 (N^-1)_12, eta_13 = 2 (N^-1)_13, eta_23 = 2 (N^-1)_23.
```

The direct entropy Hessian identity

```text
B = -Hess H = F + sum_S p_S'' log(p_S)
```

matches the structural formula

```text
B(D,D)=F(D,D)-2 tr(N adj D)
```

on all deterministic samples. On connected samples with `N` invertible, it
also matches

```text
B = A - det(N) eta eta^T,
A_ij = F(E_i,E_j)+det(N) tr(N^-1 E_i N^-1 E_j).
```

For the off-diagonal basis vectors, the coordinate diagonal entries satisfy

```text
B(E12+E21,E12+E21)=F(E12+E21,E12+E21)+2N33,
B(E13+E31,E13+E31)=F(E13+E31,E13+E31)+2N22,
B(E23+E32,E23+E32)=F(E23+E32,E23+E32)+2N11.
```

The two conditional covariance square identities are algebraically correct:

```text
p_empty p_ij - p_i p_j = -[(1-K_kk)K_ij + K_ik K_jk]^2,
p_k p_123 - p_ik p_jk = -[K_kk K_ij - K_ik K_jk]^2.
```

I checked 12 exact rational square identities and 24 floating square identities.
The largest direct-vs-structural `B` discrepancy in the formula audit was
`1.2871648191747909e-15`; the largest Schur-form discrepancy on connected
samples was `1.2732870313669764e-15`.

## Boundary Scope

The known dense rank-one boundary result has the stated limited scope: fixed
`theta in (0,1)`, fixed unit `u` with all coordinates nonzero, and equal soft
eigenvalues in

```text
K_epsilon = epsilon I + (theta-epsilon)uu^T.
```

The formula audit only rechecked six floating probes in that family, all with
`rho<1`. These probes support the recorded asymptotic behavior but do not prove
it, and they do not cover unequal soft-eigenvalue rates, `theta -> 0`, `theta -> 1`,
vanishing coordinates of `u`, or general interior kernels. The asymptotic
`rho -> 1` from below rules out a uniform bound `rho<=c<1`; it does not prove
the global target `rho<=1`.

Disconnected strict kernels may be reached by continuity for `B>=0` if the
connected global result is proved, but the inverse-`N` Schur formula itself
must not be used at singular `N`. The diagonal disconnected sample in the
formula audit was used only to check this non-application.

## Conditional-Score Candidate

For the fixed candidate at commit `424b4efcec0052ad8d79ac71c69b334dcfb03bb8`,
the score projection lemma is correct as an exact identity/inequality for
positive two-by-two tables.

For one table `(a,b,c,d)`, with `m=a+b+c+d`, `delta=ad-bc`, score `s=p'/p`,
`h=(d,-c,-b,a)`, and `h0=h-2delta/m`, direct expansion gives

```text
sum p h = 2delta,
sum p h0 = 0,
sum p h0^2 = ad(a+d)+bc(b+c)-4delta^2/m,
sum p h0(s-m'/m) = delta' - 2delta m'/m.
```

Weighted Cauchy gives the stated lower bound. The Fisher chain rule over the
conditioning bit gives

```text
F >= Q_k = (m_1')^2/(m_0 m_1) + sum_two_tables u^2/V.       (L1)
```

Completing the square gives the exact omitted-information identity

```text
F-Q_k = sum_two_tables sum_table p
        (s-m'/m-(u/V)h0)^2.                                (L2)
```

For DPP paths, the specialization `delta=-w^2` is correct for both conditioning
layers, and differentiating it gives

```text
u = -2w(w' - w m'/m),
```

with no division by `w`. I checked these identities exactly on three rational
DPP samples and all three conditioning coordinates.

## Shortcut Obstruction

The displayed rational object is a strict DPP kernel and the small chord is
strictly feasible:

```text
K = (1/100) [[30,29,15],[29,33,10],[15,10,16]],
D = diag(1,1,1/3),
t = 1/100000.
```

Independent exact recomputation gives the same atoms in bitmask order:

```text
(292541,260259,272959,14241,92359,24841,42141,659)/1000000.
```

The recomputed certificate matches the fixed JSON exactly. With 70 log-series
terms and the stated positive remainder,

```text
max_k Q_k(D) - C(D) in [-1.911698525970, -1.911698525969],
B(D,D)=F(D,D)-C(D) in [30.995287355311, 30.995287355312].
```

The log enclosure is used within its stated range: after dyadic scaling every
log argument lies in `[1,2]`, and the largest transformed `|z|=(y-1)/(y+1)` is
`12857/44107 < 1/3`.

Thus `max_k Q_k(D) >= C(D)` is false, and every convex combination of the
three `Q_k` fails at this same direction. Since the true `B(D,D)` is strictly
positive, this is not an entropy-concavity counterexample. It is only a
counterexample to that sufficient Fisher shortcut.

The author text correctly separates this direction from the trace-constrained
optimizer `d_*`. I found no proof here of `max_k Q_k(d_*) >= C(d_*)`, nor a
proof that the residual score components in L2 are controlled by the stationarity
condition.

## Critical Gaps And Non-Coverage

1. The global N3 theorem remains unproved. This review does not prove
   `rho(K)<=1` for all connected strict real kernels.
2. The constrained inequality
   `F(D,D)+det(N)tr(N^-1DN^-1D)>=det(N)` under `tr(N^-1D)=1` remains open.
3. The conditional-score candidate proves a lower bound and a shortcut
   obstruction; it does not certify the optimizer-direction bound needed for
   the main theorem.
4. No Lean, interval-global, or all-domain certificate is included here.
5. Finite deterministic probes and one exact rational obstruction must remain
   SCOUT/local evidence, not a global proof.
6. I did not audit later author drafts or any object outside the fixed commit
   listed above.
