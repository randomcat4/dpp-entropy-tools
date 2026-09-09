# N3 round2 review v1

STATUS: CORRECT for the round2 definition rebuild, the exact real principal
minor constraints checked here, and the fixed dense weak-edge beta candidate
at commit `3087eb189237ec0a2d60127d0c35128f0cbcd91c`.

STATUS: CRITICAL_GAPS for the full beta-zero implication `beta(K)=0 =>
det(N) alpha(K)<=1`, and for the original global N3 entropy Hessian theorem.

## Scope

I reviewed the round2 frozen beta-zero slice as an independent non-author
checker. I did not participate in authoring the weak-edge candidate and did
not read the other children drafts. I only wrote files under
`research/N3/round2/review/`.

The frozen subproblem is:

```text
beta(K)=0 implies det(N) alpha(K)<=1
```

with the exact round2 definitions

```text
F_pair = F - v_score v_score^T,
H = F_pair + det(N) G,
alpha = c^T H^-1 c,
beta = v_score^T H^-1 c,
gamma = v_score^T H^-1 v_score.
```

This is a strict slice of the original problem, not a replacement for the
global `rho<=1` target.

## Definition Rebuild

The script `verify_round2_definitions.py` rebuilt the eight event probabilities
by Mobius inversion, the full event Fisher matrix `F`, the richer pair-statistic
projection `F_pair`, `v_score`, `H`, and the scalars `alpha,beta,gamma`.

The pair projection was checked two ways:

1. `F_pair = F - grad(Lambda) grad(Lambda)^T / Z`, where `Z=sum_S 1/p_S`.
2. Direct covariance projection onto
   `(X1,X2,X3,X1X2,X1X3,X2X3)`.

The maximum discrepancy over three deterministic strict kernels was
`1.7763568394002505e-15`.

The exact meaning of beta zero is:

```text
beta = grad(Lambda)^T H^-1 c / sqrt(Z),
Z > 0.
```

Thus `beta=0` is exactly the equation
`grad(Lambda)^T H^-1 c=0`. Numerical smallness is not an exact beta zero.
This unit certified no exact beta-zero point.

## Principal Minor Constraint

For

```text
K=[[x,a,b],[a,y,c],[b,c,z]],
u=xy-q12, v=xz-q13, w=yz-q23,
T=r-xyz+xw+yv+zu,
```

the review script checked exactly that

```text
u=a^2, v=b^2, w=c^2, T=2abc, T^2=4uvw.
```

Along genuinely affine `K+tD`, it also checked the first and second derivative
identities for `q12,q13,q23,r,u,v,w,T`, including the differentiated
constraint `T^2=4uvw`. In the nonzero-edge branch it checked

```text
T'/T = (u'/u + v'/v + w'/w)/2.
```

For the zero-edge connected sample it did not divide by `T,u,v,w`; it used
the polynomial identities directly.

The full Rayleigh polynomial was checked as a square. For pair `ij` and
remaining coordinate `k`,

```text
Delta_ij(tau) = (K_ij tau + K_ij K_kk - K_ik K_jk)^2.
```

The leading coefficient and constant term are nonnegative and the discriminant
is zero. In the zero-edge case the leading coefficient vanishes, but the
polynomial square identity still holds. This is the real principal-minor
structure referred to in the round2 source notes; I used direct expansion for
the actual checks.

## Weak-Edge Candidate

The fixed candidate object is
`3087eb189237ec0a2d60127d0c35128f0cbcd91c:research/N3/round2/main/dense_weak_edge_beta_v1.md`
with blob `6a69ce2ba0ecc0f0826489501f126356708778f5`.

For fixed `x_i in (0,1)` and fixed nonzero real `a,b,c`,

```text
K(t) = [[x1,ta,tb],[ta,x2,tc],[tb,tc,x3]]
```

the density identity checks exactly:

```text
p/mu = 1 - t^2(a^2 chi1 chi2 + b^2 chi1 chi3 + c^2 chi2 chi3)
         + 2t^3abc chi1 chi2 chi3.
```

This also keeps `u=t^2a^2`, `v=t^2b^2`, `w=t^2c^2`,
`T=2t^3abc`, hence `T^2=4uvw`.

I checked two fixed parameter cases, one with `abc>0` and one with `abc<0`,
at `t=1/100,1/200,1/400`. The probes support the author asymptotics:

```text
beta(K(t)) = 4 sqrt(s1 s2 s3) + O(t),
det(N) alpha =
  t^2 [a^2 b^2/(s1 c^2) + a^2 c^2/(s2 b^2) + b^2 c^2/(s3 a^2)] + O(t^3).
```

For the positive `abc` case, the beta values were
`0.47826331213687223`, `0.48008649424796235`, `0.48098356646684304`,
with limit `0.48187088154946733`. The values of
`det(N)alpha/t^2` were `1.2717093626040754`,
`1.2717759873072503`, `1.2717926373258568`, with coefficient
`1.271798185941043`.

For the negative `abc` case, the beta values were
`0.4790222079877592`, `0.4776663483718563`, `0.47698060361456335`,
with limit `0.4762896722078402`. The values of `det(N)alpha/t^2`
were `0.6920255424443245`, `0.692036308451563`, `0.6920390076521677`,
with coefficient `0.6920399088669247`.

The sign of `abc` changes the leading sign of `Lambda`, but not the leading
positive beta limit.

## Fragile Terms Checked

The diagonal/off-diagonal Fisher block behaved as claimed. In the positive
case, `||F_do||/t^3` stayed around `1.05025`; in the negative case it stayed
around `0.41097`. Thus the suspected `O(t)` and `O(t^2)` cross terms are not
present in the checked expansions.

The corresponding `H_do` block also stayed bounded after division by `t^3`.
The off/off block matched the `t^2` leading diagonal with the expected
`dG` contribution:

```text
H_oo = t^2 diag(6a^2/(s1s2), 6b^2/(s1s3), 6c^2/(s2s3)) + O(t^3).
```

The off-coordinate trace covector used the required factor two:

```text
eta_12 = 2(N^-1)_12,
eta_13 = 2(N^-1)_13,
eta_23 = 2(N^-1)_23.
```

The maximum factor-two discrepancy in the weak-edge probes was
`2.220446049250313e-16`.

The degenerating block solve `H h = eta` was checked directly. The leading
off-coordinate limit

```text
t^2 h_o -> (2S/3)(1/(bc),1/(ac),1/(ab))
```

matched the probes, and the residual `||Hh-eta||_infty` stayed below the
recorded tolerance.

## Critical Gaps And Non-Coverage

1. The weak-edge result proves a beta nonzero mechanism near fixed dense
   weak-edge rays. It does not prove the beta-zero implication B0.
2. The proof assumes fixed nonzero `a,b,c` and fixed interior means. It does
   not cover edge constants tending to zero, means tending to `0` or `1`, or
   joint degenerations.
3. This unit found no exact beta-zero root and certified no counterexample
   with `beta=0` and `det(N)alpha>1`.
4. The full score residual is retained in the definitions; no old shortcut
   that deletes it is revived.
5. No Lean proof, global interval certificate, or all-domain proof was run.

## Source Note

The round2 source note points to Al Ahmadieh--Vinzant's real principal-minor
square structure. For this audit, the load-bearing identities were also
verified by direct expansion in the reviewed scripts, so no unproved external
theorem is needed for the finite checks.

