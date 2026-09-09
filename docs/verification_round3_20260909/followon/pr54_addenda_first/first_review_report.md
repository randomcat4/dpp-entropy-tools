# PR54 addenda FIRST review, head-bound to `c3b9e968c0b4557546c7b10137ef4fff295338b4`

Verdict: `ACCEPTED_SCOPED` for the three new addenda and for the endpoint-discriminant/root-separation portion of the fixture at this frozen head.

Scope reviewed:

| Unit | Status | Exact scope |
|---|---:|---|
| `research/I05-23-20260909/ADDENDUM_ARBITRARY_RANK.md` | `ACCEPTED_SCOPED` | Arbitrary-rank local strict radial curvature near decoupling, including complete likelihood, score lower bound, explicit radius, and true `t`-curvature conversion. |
| `research/I05-23-20260909/ADDENDUM_ENDPOINT_RARE_EVENT.md` | `ACCEPTED_SCOPED` | Simple legal endpoint rare-event lemma/theorem, including analytic finite atom orders, full Fisher term, full/empty atom Schur complements, and both endpoint signs. |
| `research/I05-23-20260909/ADDENDUM_RANK2_ENDPOINT_SPECTRUM.md` | `ACCEPTED_SCOPED` | Rank-two endpoint simplicity test via active generalized eigenvalue multiplicity/discriminant and exact arithmetic interface. |
| `research/I05-23-20260909/code/verify_local_and_matching.py:148-172` and `research/I05-23-20260909/output/verify_local_and_matching.txt:12-14` | `ACCEPTED_SCOPED` | Endpoint discriminants and root-separation inequalities only. I did not certify the original matching/global entropy-deficit fixture lines. |

## Findings

### A. Arbitrary-rank local curvature

The complete likelihood formula is mathematically valid under the stated strict assumptions. For each complete configuration, the event matrices `X_S=A-E_{S^c}` and `Y_T=C-E_{T^c}` are invertible in the strict finite DPP setting, and the Schur complement gives the full-law likelihood polynomial in `s=t^2` with no dropped configurations (`ADDENDUM_ARBITRARY_RANK.md:43-65`). The rank bound follows from the rank of the cross perturbation (`ADDENDUM_ARBITRARY_RANK.md:61-65`).

The score lower bound is sound and uses the complete Fisher term. The inclusion statistic identity
`E_{p_s} Z_ij=A_ii C_jj-sB_ij^2` gives `E_mu[Z_ij w_1]=-B_ij^2`, and Cauchy--Schwarz under the product law yields
`sigma^2 >= B_ij^4/(A_ii C_jj(1-A_ii C_jj))>0` (`ADDENDUM_ARBITRARY_RANK.md:75-101`). This is not an entrywise-Hessian shortcut; it is a full-law Fisher lower bound obtained from one observable statistic.

The explicit radius and constants are finite and correctly keep every coefficient bound. The definitions of `C_0,C_1,C_2,C_3`, `delta_0`, `L_3`, and `delta` are enough to ensure `1/2 <= q_s <= 3/2`, bounded logarithmic derivatives, and a positive `L_3` (`ADDENDUM_ARBITRARY_RANK.md:103-156`). The entropy derivative identities retain the full Fisher term (`ADDENDUM_ARBITRARY_RANK.md:158-190`). The conversion from `s` to `t` is correct: `J(s)=2I'(s)+4sI''(s)=-H''(sqrt(s))`, and the estimate `J'(s) >= 3 sigma_*^2` on the certified interval gives `H''(t) <= -3 sigma_*^2 t^2 < 0` for `0<|t|<=sqrt(delta)` (`ADDENDUM_ARBITRARY_RANK.md:192-215`). The Weyl bound also correctly gives strictness of both `K(t)` and `I-K(t)` on that interval (`ADDENDUM_ARBITRARY_RANK.md:213-215`).

### B. Simple endpoint rare-event dominance

Lemma B.1 correctly separates finite analytic atoms into positive-limit atoms and finite-order vanishing atoms (`ADDENDUM_ENDPOINT_RARE_EVENT.md:31-40`). A simple zero contributes `-a/x+O(1)` through the Fisher term, while all acceleration terms and all higher-order vanishing atoms are at most logarithmic or bounded (`ADDENDUM_ENDPOINT_RARE_EVENT.md:41-76`). The entropy second derivative identity explicitly sums over all atoms and uses only `sum p_omega''=0` (`ADDENDUM_ENDPOINT_RARE_EVENT.md:62-69`).

Theorem B.2 correctly turns a one-dimensional spectral endpoint kernel into a simple zero of a complete atom. If `ker K(t_*)` is one-dimensional, the full atom `det K(t)` is handled by Schur complementation through `A`; if `ker(I-K(t_*))` is one-dimensional, the empty atom `det(I-K(t))` is handled through `I-A` (`ADDENDUM_ENDPOINT_RARE_EVENT.md:78-166`). The crossing derivative is strictly negative because `s_* v^T M v=v^T C v>0` in the `K` case, with the same argument for `I-K` (`ADDENDUM_ENDPOINT_RARE_EVENT.md:141-166`). Since `t_*>0`, a simple zero in `s=t^2` is simple in `t`. The negative endpoint statement follows from evenness of the complete law under block sign conjugation (`ADDENDUM_ENDPOINT_RARE_EVENT.md:111-112`). The proof properly excludes multiple spectral endpoints and explains why a quadratic vanishing atom cannot be covered by the simple-root argument (`ADDENDUM_ENDPOINT_RARE_EVENT.md:177-181`).

### C. Rank-two endpoint spectrum

The rank-two endpoint test is correct. Schur complements reduce legality to `I-sR_0 >= 0` and `I-sR_1 >= 0`, so the positive squared endpoint is `s_*=1/max(rho_0,rho_1)` (`ADDENDUM_RANK2_ENDPOINT_SPECTRUM.md:8-47`). Congruence preserves nullity, so the endpoint kernel dimension is the multiplicity of the active top eigenvalue (`ADDENDUM_RANK2_ENDPOINT_SPECTRUM.md:49-54`, `84-99`). For a rank-two positive semidefinite operator, `Delta(R)=2tr(R^2)-tr(R)^2=(lambda_1-lambda_2)^2`, so `Delta>0` is exactly the simple-active-root condition (`ADDENDUM_RANK2_ENDPOINT_SPECTRUM.md:55-82`). The generalized-eigenvalue formulation is a valid exact rational interface and does not require choosing matrix square roots (`ADDENDUM_RANK2_ENDPOINT_SPECTRUM.md:101-113`).

### Endpoint fixture arithmetic

The author code computes the two endpoint generalized-eigenvalue discriminants and the rational square comparisons at `verify_local_and_matching.py:148-172`, with the corresponding output at `output/verify_local_and_matching.txt:12-14`. I independently recomputed these quantities from the fixture matrices in `verify_local_and_matching.py:15-29`, using only exact rational arithmetic and no import from the author verifier.

Independent exact values:

| Quantity | Value | Consequence |
|---|---:|---|
| `Delta_K` | `3710825577769541084161/4104054745543938939062500` | matches output and is positive |
| `[2*(1/25)-tr_K]^2-Delta_K` | `39286478142/25323083421875` | positive, so `rho_K < 1/25` |
| `Delta_I-K` | `16227278265011862790681/6214062013120963640250000` | matches output and is positive |
| `Delta_I-K-[2*(1/20)-tr_IK]^2` | `767487943/3116002550625` | positive, so `rho_I-K > 1/20` |

Thus the stated separation `rho_K < 1/25 < 1/20 < rho_I-K` is exactly certified. The positive legal endpoint for the fixture is governed by `I-K`, and `Delta_I-K>0` makes the active endpoint simple. This supports the claimed endpoint conclusion in the scope of addenda B/C and the fixture endpoint lines.

Reviewer artifacts:

- `frozen_scope.md`
- `fixture_arithmetic_plan.md`
- `check_endpoint_roots.py`
- `fixture_endpoint_root_check.txt`

## Dependencies and limitations

This acceptance depends on the standard finite DPP complete-atom formula and the strict-kernel convention used by `RESULT.md`, but it does not certify the original `RESULT.md` theorem, the original fixture, the matching entropy-gap argument, or any PR54 content outside the three addenda and endpoint root checks named above.

This review does not settle whole-chord concavity. The compact middle interval and multiple/isotropic endpoint cases remain outside the accepted scope, exactly as the addenda state (`ADDENDUM_ARBITRARY_RANK.md:217-224`, `ADDENDUM_ENDPOINT_RARE_EVENT.md:177-181`, `ADDENDUM_RANK2_ENDPOINT_SPECTRUM.md:115-116`).

This review is bound only to PR54 frozen head `c3b9e968c0b4557546c7b10137ef4fff295338b4`. The local `SOURCE.json` records a newer observed live head, which I did not review.
