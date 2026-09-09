Historical first report, superseded by review_report_v2.md for the H correlation descriptor. Do not use this file as the current aggregate verdict.

# PR43 rank-two continuation verification report

Reviewer: `C1 rank-two first reviewer`

Current source binding: PR43 commit `7bd5962bbb2020ce47fbe286adda7dfe02f9645d`, with historical source `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78` read first.

Scope: `continuation/frozen_statement_v3.md` clauses E--H only. Clauses I--N, nested v3 channel work, general dense arbitrary rank-two cross-block concavity, and novelty are out of scope.

## Overall verdict

STATUS: CORRECT

Repository status: ACCEPTED_SCOPED for clauses E--H.

Critical gaps found: none.

This is a first non-author review pass, not a final self-certification of a major new theorem. The result should remain scoped to the frozen clauses and the imported C3 diagonal-anchor theorem.

## Dependency interface

The imported C3 finite theorem states that for any strict diagonal finite Hermitian contraction `B=diag(b_i)` and any fixed Hermitian direction `A`, `t -> H(B+tA)` is concave on the entire feasible interval; see `sources/dependency_c3/frozen_statement_v2.md:8-15`. Its proof claims the whole finite ray through an interior diagonal kernel, including both signs and feasible boundary, in `sources/dependency_c3/proof.md:114-141`.

I did not re-certify C3, but its actual hypotheses match the PR43 uses in the one-side diagonal theorem and the empty/full conditional lines in the `3+3` family.

## Clause E: three-point indefinite rank-two directions

STATUS: CORRECT

The frozen claim is at `sources/pr43_7bd5962/continuation/frozen_statement_v3.md:20-43`; the proof is `sources/pr43_7bd5962/proof/04_three_point_indefinite_rank2.md`.

I verified the proof chain:

- The complete-event probabilities have degree at most two because `rank(D)=2`; the direct coefficient setup is at `proof/04_three_point_indefinite_rank2.md:20-31`.
- For a symmetric rank-two direction with null vector `n`, `adj(D)=gamma nn^T`, `gamma<0`, and pair coefficients `delta_ij=gamma n_k^2`; see `proof/04_three_point_indefinite_rank2.md:41-57`.
- The eight atoms of `c` are recovered by the two conditional four-cycles for each of the three coordinate pairs; the Mobius-injectivity closure is at `proof/04_three_point_indefinite_rank2.md:61-84`.
- The conditional two-point odds have the required sign because a two-coordinate conditional DPP has covariance `-offdiag^2`; see `proof/04_three_point_indefinite_rank2.md:91-123`.
- The full entropy Hessian keeps the complete Fisher term and the second event-coefficient term; the interior and boundary extension are at `proof/04_three_point_indefinite_rank2.md:128-136`.

The boundary argument is sufficient: concavity is proved on the strict legal interior and extends to feasible endpoints by continuity of `-x log x`. Semidefinite rank-two directions are explicitly excluded.

## Clause F: exterior sufficient statistics and compressed Hessian

STATUS: CORRECT

The frozen claim is at `sources/pr43_7bd5962/continuation/frozen_statement_v3.md:45-88`.

The exact likelihood ratio follows from the complete-event Schur formula and Sylvester determinant identity in `sources/pr43_7bd5962/proof/03_lifting_and_exterior.md:89-121`. The cancellation identities for the exterior degrees are at `proof/03_lifting_and_exterior.md:129-142`.

The KL and mutual-information compression in `sources/pr43_7bd5962/proof/05_diagonal_and_feature_routes.md:46-73` is valid: the likelihood ratio is measurable with respect to `(G_A,G_C)`, so conditioning on a feature fiber leaves the baseline product fiber law unchanged. This preserves KL to `p_A otimes p_C`; since the block marginals are fixed, it also preserves mutual information.

The Hessian formula at `proof/05_diagonal_and_feature_routes.md:75-120` is correct on the strict interior where every `ell_T(Z)>0`. The formula should be read as a differential identity there; it is not a boundary derivative statement.

## Clause G: three-point conditional direction criterion

STATUS: CORRECT

The frozen claim is at `sources/pr43_7bd5962/continuation/frozen_statement_v3.md:90-112`; proof source is `sources/pr43_7bd5962/proof/06_correlated_3plus3_family.md:3-27`.

The criterion correctly combines three valid cases for each conditional direction `M_S`:

- `rank(M_S)<=1`: complete-event probabilities along `C-rM_S` are affine, so entropy is concave on the legal segment.
- `M_S` indefinite rank two: clause E applies in the original coordinates.
- The line through `C` and `M_S` contains a strict diagonal kernel: the imported C3 theorem applies.

The Schur conditioning identity in `sources/pr43_7bd5962/proof/01_conditioning.md:27-67` and radial lifting in `sources/pr43_7bd5962/proof/03_lifting_and_exterior.md:3-51` then give whole-interval concavity in `t`; strictness for `B != 0` follows from nonzero cross-block covariance and positive mutual information.

## Clause H: correlated non-coordinate `3+3` family

STATUS: CORRECT

The frozen claim is at `sources/pr43_7bd5962/continuation/frozen_statement_v3.md:114-168`; proof source is `sources/pr43_7bd5962/proof/06_correlated_3plus3_family.md:29-149`.

The structural proof checks out. For the empty and full left configurations, `M_S` is a scalar multiple of `M_0`, so the conditional line contains the strict diagonal anchor `D_0`; see `proof/06_correlated_3plus3_family.md:87-105`. For the six middle configurations, the event matrix inertia and Jacobi complementary-minor identity give `det G_S<0`; see `proof/06_correlated_3plus3_family.md:113-147`. Full row rank of `R` then transfers indefiniteness and rank two from `G_S` to `M_S`. Thus all eight left configurations satisfy the clause G criterion.

The explicit rational fixture at `proof/06_correlated_3plus3_family.md:151-236` also checks exactly: the left and right rank-two singular planes are non-coordinate, `A` and `C` are strict correlated kernels, the six middle `M_S` are indefinite rank two, and the stated legal radius is the active Schur-complement bound.

## Independent computation

I wrote and ran an independent exact script:

- Local script: `children/pr43_rank2/independent_pr43_rank2_check.py`
- Exact input: `children/pr43_rank2/continuation_fixture.json`
- Server output: `children/pr43_rank2/exact_check_output.txt`
- Verified exit status: `children/pr43_rank2/exact_check_verified_exit.txt`

The check used `/opt/venv/bin/python` 3.12.3, SymPy 1.13.3, NumPy 2.1.2, and mpmath 1.3.0. It passed:

- symbolic three-point four-cycle and two-point odds identities;
- exact `3+3` fixture structure and radius;
- exact rank-two exterior likelihood, KL compression, and moment cancellations;
- all 64 events positive at `t=1/100` and `t=1/50`;
- high-precision diagnostic curvatures `H''(1/100)=-134.5977301346...` and `H''(1/50)=-584.1036922572...`.

The curvature values are consistency diagnostics only; the universal claims above are accepted from the proof-level arguments.

## Limits

No result here certifies arbitrary dense two-sided rank-two cross-block concavity, high-dimensional exterior scalar positivity, semidefinite rank-two directions, nested v3 clauses I--N, or novelty.
