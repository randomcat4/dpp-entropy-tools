# C1 formula audit

Reviewer: C1 independent non-author formula checker.
Scope: frozen B0 definitions in `runs/C1/repo/research/C1/frozen_statement.md`, N3 round2 sources, and C1 `main/reconstruction.md`.

STATUS: CORRECT within the formula-reconstruction scope below.

This is not a proof of B0. The implication `beta(K)=0 => det(N) alpha(K)<=1` remains INCOMPLETE unless a separate proof or certified violating exact beta-zero kernel is supplied.

## Sources read

- `tasks/C1/PROMPT.md`
- `runs/C1/repo/AGENTS.md`
- `runs/C1/repo/research/C1/frozen_statement.md`
- `runs/C1/repo/research/C1/main/reconstruction.md`
- `runs/C1/repo/research/C1/main/core.py`, `precheck.json`, `tilt_probe.json`
- `runs/C1/repo/research/N3/round2/frozen_theorem_v1.md`
- `runs/C1/repo/research/N3/round2/verdict.md`, `checkpoint.json`, `provenance.md`
- `runs/C1/repo/research/N3/round2/verifications/index.md`
- `runs/C1/repo/research/N3/round2/review/round2_review_v1.md`, `round2_final_review_v2.md`
- Directly relevant old proof notes: `beta_zero_existence.md`, `rayleigh_beta_zero_obstruction.md`, `dense_weak_edge_beta_v1.md`, `lambda_tangent_locked_odds_lemma.md`, `locked_odds_degeneracy_addendum.md`

The path `research/C1/frozen_statement.md` named in the task was absent under the root. The matching frozen file used here is `runs/C1/repo/research/C1/frozen_statement.md`.

## Formula reconstruction verdict

The eight exact atoms are correctly reconstructed from

```text
q12=xy-a^2, q13=xz-b^2, q23=yz-c^2,
r=xyz+2abc-xc^2-yb^2-za^2,
p123=r, pij=qij-r, pi=Kii-qij-qik+r, p0=1-x-y-z+q12+q13+q23-r.
```

The one- and two-derivative formulas in `main/reconstruction.md` are consistent with differentiating these polynomials in the six symmetric coordinates `(x,y,z,a,b,c)`. In particular the off-diagonal basis is `Eij+Eji`, so first derivatives of `qij` contain `-2 Kij Dij`, second derivatives contain `-2 Dij^2`, and `eta_ij=2(N^-1)_ij` for off-diagonal coordinates. I found no missing factor of two.

The log-second-derivative term satisfies

```text
sum_S pS'' log pS = ell12 q12'' + ell13 q13'' + ell23 q23'' + Lambda r''
                 = d G - d eta eta^T,
```

with `N=-diag(ell23,ell13,ell12)-Lambda K`, `d=det N`, `G(D,E)=tr(N^-1 D N^-1 E)`, and `eta(D)=tr(N^-1 D)`. Hence

```text
B=-Hess H = F+dG-d eta eta^T
```

is correct in the frozen six-coordinate convention.

## Positivity and rank conditions

For the conditional two-by-two odds, direct Rayleigh square identities give

```text
ell_ij <= 0,        ell_ij + Lambda <= 0.
```

Therefore:

- If `Lambda<0`, then `N=diag(-ell)+(-Lambda)K>0`.
- If `Lambda>0`, then `N=diag(-ell-Lambda)+Lambda(I-K)>0`.
- If `Lambda=0`, then `ell_ij=0` would force both conditioned Rayleigh squares for edge `ij` to vanish. Their unsquared equations imply `Kij=0` and `Kik Kjk=0`, which disconnects the three-vertex graph. Thus every diagonal entry of `N=diag(-ell)` is strictly positive on the connected frozen domain.

This covers connected domains with exactly one zero edge; no division by an edge, by `T=2abc`, or by `uvw` is needed.

`Cov(Tstat)` is positive definite because all eight atom probabilities are positive and no nonzero multilinear polynomial of degree at most two can be constant on all cube vertices. The moment Jacobian

```text
J = d(x,y,z,q12,q13,q23)/d(x,y,z,a,b,c)
```

has determinant `-8abc`, so it can lose rank at a zero edge. At a connected one-zero-edge point it has rank five. This does not invalidate `F_pair=J^T Cov^-1 J`, but it does mean `F_pair` must not be inverted there. The matrix `M=F_pair+dG` is still positive definite because `d>0` and `G(D,D)=||N^-1/2 D N^-1/2||_F^2`.

## Fisher decomposition and beta meaning

In the atom Fisher inner product, `h_S=(-1)^(3-|S|)/p_S` is orthogonal to constants and all degree-at-most-two statistics. Its squared norm is `Z=sum_S 1/p_S`, and pairing any K-affine score with `h` gives `Lambda'`. Hence

```text
F = F_pair + grad(Lambda) grad(Lambda)^T / Z.
```

The exact meaning of beta zero is

```text
beta=0 <=> grad(Lambda)^T M^-1 eta = 0
       <=> Lambda'[D_M] = 0,
D_M = M^-1 eta / alpha, alpha=eta^T M^-1 eta.
```

`D_M` is the unique minimizer of `M(D,D)` under `eta(D)=1`. An arbitrary direction with `Lambda'[D]=0` is not interchangeable with this optimizer. At beta zero,

```text
B(D_M,D_M)=1/alpha-det(N),
```

so `det(N) alpha<=1` is exactly the missing optimized Fisher/cofactor inequality, not a consequence of tangentness alone.

For the full rank-one correction, Sherman-Morrison gives

```text
rho = d[alpha - beta^2/(1+gamma)].
```

At an approximate beta zero, dropping the correction is not licensed.

## C1 tilt stationarity check

The new tilt identities in `main/reconstruction.md` are formula-correct. For diagonal `A`, the exponential L-tilt has K-tangent

```text
Q_A = AK+KA-2KAK,
```

score `2 sum_i A_ii (1_{i in S}-K_ii)`, and therefore

```text
Lambda'[Q_A]=0,             F_pair(Q_A,D)=F(Q_A,D)=2 tr(A D).
```

Substituting `h=M^-1 eta`, `W=N^-1`, and `R=W h W` into `M(h,Q_A)=eta(Q_A)` yields, for all diagonal `A`, the displayed component identity

```text
diag(2h+d[KR+RK-2KRK]) = diag(KW+WK-2KWK).       (T)
```

I found no factor, transpose, or missing full-score term error in `(T)`. The identity is only a stationarity test; it does not determine all six entries of `h` or prove the sign of `1/alpha-d`.

## Independent server run

Script: `runs/C1/children/audit/formula_rebuild_audit.py`.

Output: `runs/C1/children/audit/formula_rebuild_audit.remote.json`.

Exit file: `runs/C1/children/audit/formula_rebuild_audit.exit`.

Remote work directory: `/root/i05-seven-fronts-20260909/C1/audit`.

Interpreter: `/opt/venv/bin/python`.

Final run:

```text
status PASS
pid 164000
exit 0
python 3.12.3
numpy 2.1.2
threads OMP/OPENBLAS/MKL/NUMEXPR = 1
```

The script rebuilt the atoms by explicit formulas and by Mobius inclusion minors; rebuilt first and second derivatives; compared `F_pair=F-vv^T` against `J^T Cov^-1 J`; compared `B` from `sum p'' log p` against `F+dG-d eta eta^T`; checked the off-diagonal `eta` factor two; checked the optimizer identities for `D_M`; checked `(T)` on three diagonal tilt directions; and included a strict connected one-zero-edge sample with `J_rank=5` and `Cov_min_eigenvalue>0`.

Representative maximum residuals from the final run:

```text
explicit atoms vs Mobius atoms:          8.33e-17
analytic dp vs centered finite dp:       5.49e-11
Fpair score form vs covariance form:     7.11e-15
B second-derivative vs N formula:        8.88e-16
off-diagonal eta factor-two residual:    1.39e-17
tilt (T) diagonal residual:              below 1e-14 in all recorded samples
```

The run also records the near certified beta-root midpoint as calibration only: `beta` is about `-1.4e-16` and `det(N) alpha` is about `0.6615279259892364`, matching the known safe bracket scale but not proving any global statement.

## Remaining critical gap

No gap was found in the formula package above. The mathematical gap is exactly the already stated one: prove a DPP-specific lower bound at the actual `M`-stationary trace-normalized direction on exact beta-zero kernels, or certify an exact beta-zero violation. Finite diagnostics, exact tangent directions, and the tilt stationarity equations do not close that gap.
