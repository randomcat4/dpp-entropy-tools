# A2 final v3 independent review

STATUS: CORRECT

## Commit binding

Candidate commit: `5084d3966a3eccc3ad5b497f1da6eab08fe7554a`

All review below is bound to git blob contents read from that commit, not to
mutable working-tree files.

| Role | Commit path | SHA256 |
| --- | --- | --- |
| frozen v3 | `research/A2/frozen_theorem_v3.md` | `0ed19afb8081865a92bfc37de6f333e06b6ac65e0404bee59799ed58f8f7c44c` |
| anonymous proof | `research/A2/proofs/uniform_event_bounds_v3.md` | `77dfde5c594dad6ff0de5159b6d36b5a27082d0713d49178ff6af29ab72d5e50` |
| hazards | `research/A2/hazards.md` | `cf1b4faf792efa054d20312312bc2eb8da8d2631d1bfbdc7dae3557135148440` |

Certification target: Sections 1--4 of the anonymous proof only. Sections
5--7 are treated as context, limitations, and failure ledger, not as certified
claims.

No computation was run for this v3 review.

## Claim 1: zero-safe finite-law and matrix estimates

The finite-law estimate is valid without assuming any positive lower bound on
event probabilities. For `h(p)=-p log p`, the scalar bound

```text
|h(b)-h(a)| <= d(2+log(1/d)),  d=|b-a|, 0<=a,b<=1
```

follows by integrating the upper bound `1-log s` for `|h'(s)|` over the
worst interval of length `d`, with the endpoint `0` handled by improper
integration and continuity. Clipping `q` into `[0,1]` cannot increase its
distance from a genuine probability `p`. Summing over `N=2^n` events and
absolute weights `1/2,1/2,1` gives exactly `2N omega(R)`.

The matrix perturbation estimate is also sound. For each principal minor,
telescoping one column at a time bounds the determinant difference by
`k delta`, because unchanged columns of principal submatrices of contractions
have norm at most `1` and changed columns have norm at most `delta`. Summing
over all supersets in inclusion-exclusion gives event-law error at most
`L_n delta`, with `L_n=n 2^n`. Applying the finite-law estimate yields the
stated `2^(n+1) omega(L_n delta)` bound. The proof uses the full exact-event
law rather than principal minors as probabilities.

No critical gap found for Claim 1.

## Claim 2: bounded moving mixed data

The statement is correctly limited to moving data that remain uniformly bounded
and satisfy the frozen-data Schur residual conditions at each evaluated
epsilon, in addition to actual endpoint feasibility. It does not claim a
universal moving-frame theorem.

The proof freezes the datum at a given epsilon and introduces `x=sqrt(epsilon)`
as the small parameter. The skew generator

```text
J=V B^T U^T - U B V^T
```

gives an orthogonal comparison kernel agreeing with the submitted mixed kernel
through order `x^2`, with a uniform `O(x^3)` matrix error. The Schur residual
conditions make the comparison family feasible for uniformly small `x`, while
the frozen statement separately assumes feasibility of the actual endpoints at
the evaluated epsilon. The matrix error contributes the
`C epsilon^(3/2)(1+log(1/epsilon))` term through Claim 1.

The event classification is adequate. The spectral exact-event formula

```text
p(S)=sum_|J0|=|S| prod_(j in J0) lambda_j
              prod_(j notin J0)(1-lambda_j) det(T_{S,J0})^2
```

is the standard full-event DPP law after eigenstate mixing and
Cauchy--Binet. It covers exact events, not only inclusion minors. For
rank-`r` active events with `a=psi_S^2>0`, the condition
`epsilon<c m` keeps endpoint and midpoint probabilities in a fixed multiple of
`a`; Taylor's formula then gives only
`O(epsilon[1+log(1/a)])`, and summing over active events gives the
`C epsilon(1+log(1/m))` term.

For rank-`r` zero events, the first endpoint coefficient is `phi_S^2`, while
the midpoint is `O(epsilon^2)`, contributing `Z epsilon log(1/epsilon)`.
For cardinalities `r-1` and `r+1`, the cardinality generating polynomial gives
endpoint coefficient sum

```text
tr H_sigma + tr L_sigma - 2F,
```

and midpoint coefficient sum `tr A + tr C`; endpoint averaging therefore
contributes `-2F epsilon log(1/epsilon)`. All other cardinalities are
controlled at `O(epsilon^2 log(1/epsilon))`. The proof treats vanishing
coefficients by the zero-safe scalar estimate instead of assigning illegal
logarithms to zero rates.

Thus the stated bound

```text
|Delta-(Z-2F)epsilon log(1/epsilon)|
 <= C epsilon(1+log(1/m))
    + C epsilon^(3/2)(1+log(1/epsilon))
```

is supported. Since `0<=Z<=F`, the leading term is at most
`-F epsilon log(1/epsilon)`. The two sufficient domination conditions in the
frozen statement correctly include the extra requirement `epsilon<c m`; in the
case `log(1/m)=o(log(1/epsilon))`, this requirement follows eventually because
`epsilon/m -> 0`.

No critical gap found for Claim 2.

## Claim 3: exact shrinking-direction crossover

For the two-coordinate family, the endpoints have determinant
`epsilon(1-epsilon)(1-b^2)>0`, their complements have the same determinant,
and the midpoint is the true arithmetic midpoint. The four exact-event
probabilities

```text
endpoint: (u-delta, v+delta, w+delta, u-delta)
midpoint: (u,       v,       w,       u)
```

follow directly from the two-by-two full DPP law, with
`u=epsilon(1-epsilon)`, `v=(1-epsilon)^2`, `w=epsilon^2`, and
`delta=b^2 u`.

The entropy difference is reduced to the one-variable expression

```text
D(d)=2h(u-d)+h(v+d)+h(w+d)-2h(u)-h(v)-h(w).
```

Using `u^2=vw`, differentiation gives

```text
D'(d)=2log(1-d/u)-log(1+d/v)-log(1+d/w).
```

Integrating from `0` to `delta` isolates the `{2}` event contribution

```text
-[(w+delta)log(1+delta/w)-delta]
```

and leaves an error `E<=0` with the stated explicit bound

```text
|E| <= delta^2/[u(1-b^2)] + delta^2/(2v).
```

The three regimes then follow from the size of `delta/w`:

- `0<kappa<1/2`: `delta/w -> infinity`, giving the
  `-(1-2kappa)epsilon^(1+2kappa)log(1/epsilon)` term.
- `kappa=1/2`: `delta/w -> 1`, giving
  `-(2log 2-1)epsilon^2+o(epsilon^2)`.
- `kappa>1/2`: `delta/w -> 0`, giving
  `-(1/2)epsilon^(4kappa)(1+o(1))`.

The result is correctly framed as an obstruction to informally substituting a
shrinking `B` into a fixed-data leading term. It does not contradict the old
fixed-data theorem and does not claim a positive entropy gap.

No critical gap found for Claim 3.

## Hazard review

The proof uses full event probabilities throughout, keeps the midpoint as the
actual arithmetic midpoint, avoids arbitrary orthogonal entropy invariance, and
does not use finite non-hits or floating signs. It explicitly handles zero
probabilities, shrinking coefficients, and the failure of fixed-data uniformity
near zero directions. The moving mixed-data lemma is stated as a sufficient
condition with bounded data and `epsilon<c m`; it does not silently extend to
all A2 moving paths.

## Verdict

Sections 1--4 prove the three frozen v3 auxiliary claims within their stated
scope. I found no critical gap in the zero-safe entropy modulus, matrix
perturbation transfer, bounded moving mixed-data asymptotic estimate, or the
two-coordinate shrinking-direction crossover.
