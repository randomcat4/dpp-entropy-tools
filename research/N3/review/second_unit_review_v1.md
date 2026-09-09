# N3 second review unit v1

STATUS: CORRECT for the fixed local obstruction certificates and the finite
Sherman-Morrison optimizer lemma checked here.

STATUS: CRITICAL_GAPS for the frozen N3 entropy theorem, the global scalar
bound `rho<=1`, and any DPP alignment lower bound strong enough to prove it.

## Scope

This review covers three fixed objects only:

1. Main stationary obstruction commit
   `449221bc3639c2de1239707f15dd938d6e230b9d`.
2. Falsification rank-two boundary obstruction commit
   `f8a75e077c4ca449307e251ceef5f5c2bb6d218c`.
3. Inequality Sherman-Morrison note commit
   `c0964be794705bc89e6b3ba6ecdc98afa6c81e32`.

I did not edit any author object. I used a review-owned script,
`verify_second_unit.py`, and fixed Git objects as read-only inputs.

## Stationary Obstruction

The stationary obstruction at commit `449221b` is correct as a strict
counterexample to the proposed sufficient condition

```text
max_k Q_k(D_*) >= C(D_*)
```

at the true trace-constrained `A`-optimizer. It is not an entropy-concavity
counterexample.

Checked blobs:

| Object | Blob |
| --- | --- |
| `research/N3/main/stationary_obstruction_v1.md` | `cc55d5ab4a43ef373789b6fcd195dd117b1bdeb3` |
| `research/N3/main/pair_score_identity_v1.md` | `8dd133e448974338c4c038ea1ffc2c6f945c766e` |
| `research/N3/main/certify_stationary_obstruction.py` | `1a5003eb9b565e65bb897cead9c81df6d22a43b2` |
| `research/N3/main/stationary_obstruction_certificate.json` | `c919239301a6c3755dad6d7a6da00688310442ff` |

For

```text
K=(1/100) [[51,24,-24],[24,48,-24],[-24,-24,52]],
d=A^-1 eta,
```

the independent 180-bit dyadic interval recomputation exactly matches the
fixed JSON certificate. The script rebuilt event gradients, Fisher `F`,
`N`, `N^-1`, `eta`, and

```text
A = F + det(N) G_N
```

from the event formulas. It explicitly checked that `A` is not just `F`:
the `(11,11)` correction interval is
`[3.502632235885, 3.502632235886]`.

The interval Gaussian eliminations used positive enclosed pivots for `N^-1`
and for the six-by-six `A d = eta` solve, so the computed box encloses the
exact stationary vector produced by that elimination formula. The trace
normalizer `eta^T d` is strictly positive, so replacing `d` by
`d_*=d/(eta^T d)` multiplies every quadratic gap by a positive square and
does not change signs. The script also checked the normalized gaps directly.

The certified ratios are:

```text
(Q_1(d)-C(d))/A(d,d) in [-0.101833309756, -0.101833309755],
(Q_2(d)-C(d))/A(d,d) in [-0.101569942472, -0.101569942471],
(Q_3(d)-C(d))/A(d,d) in [-0.101967455682, -0.101967455681],
(F(d)-C(d))/A(d,d)   in [ 0.547561495186,  0.547561495187],
rho                  in [ 0.452438504813,  0.452438504814].
```

Thus every individual `Q_k` and every convex combination of the three fails
to dominate `C` at the true `A`-optimizer, while the real entropy Hessian
quantity remains positive.

## Pair-Score Identity

The identity in `pair_score_identity_v1.md` is correct for strictly positive
three-bit laws. In the `p`-weighted space, the vector

```text
h_S = (-1)^(3-|S|)/p_S
```

is orthogonal to constants and all degree-at-most-two monomials, since the
corresponding alternating sums vanish. Its squared norm is
`Z=sum_S 1/p_S`, and for a mass-preserving score `p'/p` the missing component
is `(Lambda')^2/Z`. The variational form

```text
F_pair = min_c sum_S (p'_S-c epsilon_S)^2/p_S
```

has minimizer `c=Lambda'/Z` and equals `F-(Lambda')^2/Z`. The review script
checked these orthogonality and minimization identities exactly on a rational
positive law with a rational mass-preserving score.

This identity exposes the one Fisher score component discarded by the
one/two-point projection. It does not by itself imply `F_pair>=C`.

## Rank-Two Boundary Obstruction

The falsification object at commit `f8a75e0` is correct as a rank-two boundary
obstruction to the pair-score sufficient inequality `F_pair>=C`. It is not an
N3 entropy counterexample and makes no claim about the actual `A`-optimizer.

Checked blobs:

| Object | Blob |
| --- | --- |
| `research/N3/falsification/rank2_projection_obstruction.md` | `32e9b69ab4d0af2b13f14d4efc3887c97cb15d85` |
| `research/N3/falsification/rank2_projection_check.py` | `f7bfb2a20461c9449a222ff48bc08a98351db276` |
| `research/N3/falsification/rank2_projection_check.json` | `e524b3d0edc2a2956564fe26d95375858e58e8b7` |

The analytic mechanism checks out for

```text
u=(1,2,3)/sqrt(14),
K_epsilon=(I-uu^T)/2 + epsilon uu^T,
D=I.
```

The event formulas and direction derivatives are consistent with changing
both `theta` and `epsilon` along `tI`, not with differentiating only in
`epsilon`. The finite projection limit is

```text
13 + sum_i 1/u_i^2 = 577/18.
```

The cofactor constant uses

```text
prod_i(1-u_i^2)=325/1372,
```

so `C(I)=2log(1/epsilon)+2log(325/1372)+O(epsilon log(1/epsilon))`.

At `epsilon=10^-12`, independent exact recomputation matches the fixed JSON:

```text
F_pair-C in [-20.326087425095389917440103297042,
             -20.326087425095389917440103297041],
B=F-C    in [249999999964.951476678055395201064953440915,
             249999999964.951476678055395201064953440916].
```

So dropping the missing Lambda-score component can remove the rare-event
Fisher pole, but the full `B` is positive on this direction.

## Sherman-Morrison Optimizer Lemma

The finite-dimensional optimizer lemma at commit `c0964be` is correct as
ordinary algebra.

Checked blob:

| Object | Blob |
| --- | --- |
| `research/N3/inequality/optimizer_sherman_morrison_lemma.md` | `ebd8a7c3da419233ed134f3a3efeba173fae1924` |

For

```text
A = H + v v^T,
alpha=c(H^-1c), beta=v(H^-1c), gamma=v(H^-1v),
s=alpha-beta^2/(1+gamma),
```

Sherman-Morrison gives

```text
D_A = (H^-1 c - (beta/(1+gamma))H^-1 v)/s.
```

The review script checked this formula against a direct rational solve of
`A^-1 c`, verified `c(D_A)=1`, `A(D_A,D_A)=1/s`, and
`v(D_A)=beta/((1+gamma)s)`. It also checked the suppression

```text
|v(D_A)| <= |v(H^-1 c/alpha)|
```

from `beta^2<=alpha gamma`.

The two scalar equivalences also check:

```text
A(D_A,D_A)>=d    iff    s<=1/d,
beta^2/(1+gamma)>=alpha-1/d    iff    s<=1/d,
```

and the `F2`-at-`D_A` condition is equivalent to

```text
alpha - ((2+gamma) beta^2)/(1+gamma)^2
  >= d (alpha - beta^2/(1+gamma))^2.
```

This lemma does not supply the missing DPP alignment lower bound for
`beta^2/(1+gamma)`. Treating `s<=1/d` as the conclusion would only restate
the old `rho`-equivalent target.

## Critical Gaps And Non-Coverage

1. None of these objects proves the frozen N3 full-domain theorem.
2. The stationary obstruction refutes a proposed sufficient condition at the
   true `A`-optimizer; it does not refute entropy concavity.
3. The rank-two boundary object refutes `F_pair>=C` near one boundary family;
   it does not address the true `A`-optimizer or the global target.
4. The Sherman-Morrison lemma is finite-dimensional algebra only. The DPP
   alignment lower bound remains open.
5. No Lean proof, global interval certificate, or parameter-space proof was
   performed in this review unit.

