# Independent SECOND review: PR58 joint-additive addendum

Overall verdict:

- Analytic joint-additive proof units: `CORRECT`.
- Static code interface for the finite witness: `CORRECT` as interface inspection only.
- Numerical strict witness claims at `s=9/10`: `INCOMPLETE` in this review by frozen scope, because I did not independently run or reconstruct the rational/log certificate.
- Original `[3,15]` corridor and `s=10` computation: `INCOMPLETE` in this review by explicit exclusion.
- Formal proof and novelty: `INCOMPLETE` / not certified.

No `CRITICAL_GAPS` were found in the analytic Hilbert-projection proof, normal equations, rank-four reduction, or abstract dual lower-bound argument.

## Sources and binding

`input_binding.json` binds the packet to PR 58 head `5ab3cae1c49da8334057596f46a4bd8fc449b98c` under `research/I05-23-middle-20260909/`. I recomputed SHA-256 hashes for all seven frozen files and they match the binding; see `source_binding.json`.

I used the accepted PR54 local scope only for the rank-two outer-wedge identity. The accepted record states the formula for `q_s=1-sa+s^2b`, `u=q_s-1`, `y=s^2b`, and

`t^2 I''(t)=E[Phi(u)+4y^2/(1+u)+y psi(u)]`

with the named `Phi` and `psi` functions (`accepted_pr54.md` lines 45-51; linked source `ADDENDUM_OUTER_WEDGE_FLOW_RATE.md` lines 23-95). I do not import the earlier PR54 claims beyond that accepted scope.

## Unit 1: two-margin Hilbert projection and factor `1/2` bound

Verdict: `CORRECT`.

Relevant lines:

- `ADDENDUM_JOINT_ADDITIVE.md` lines 21-63.
- `ADDENDUM_CONDITIONAL_CENTERING.md` lines 15-42 and 93-123.
- `RESULT.md` lines 22-44 and 84-104.

The proof defines `h=y/q_s` and uses the fixed left and right DPP marginals to get

`E_{P_s}[h|S]=sum_T p_C(T)y(S,T)=0`

and symmetrically in `T` (`ADDENDUM_JOINT_ADDITIVE.md` lines 21-33). Therefore `h` is orthogonal in `L^2(P_s)` to every additive function `f(S)+g(T)`, because multiplying by the conditional law cancels `q_s` and leaves the product-law fiber sums of `y`.

The Cauchy step has the right denominator and the right factor:

- `E_{P_s} h^2 = E_mu[y^2/q_s] = A_2/4`.
- `R_add` is the squared `L^2(P_s)` distance from `psi(u_s)` to the additive subspace.
- Thus `|E_mu[y psi]| <= (1/2) sqrt(A_2 R_add)`, giving line 59 from the accepted outer-wedge identity.

This is a sufficient lower bound only. The text states that correctly at lines 132 and 247-251.

## Unit 2: relation to one-sided residuals

Verdict: `CORRECT`.

Relevant lines:

- `ADDENDUM_JOINT_ADDITIVE.md` lines 49-63.
- `ADDENDUM_CONDITIONAL_CENTERING.md` lines 59-91.

The additive subspace contains left-only functions, right-only functions, and constants. Therefore its squared projection residual is at most each one-sided residual from the previous conditional-centering addendum. Because the lower bound worsens monotonically with the residual inside the negative square-root term, the joint-additive lower bound is no weaker than either one-sided bound.

## Unit 3: zero-mean gauge, normal equations, strict contraction, inverse, and residual formula

Verdict: `CORRECT`.

Relevant lines:

- `ADDENDUM_JOINT_ADDITIVE.md` lines 65-105.

After removing the constant `c=E_{P_s} psi`, the minimization can be written over the zero-mean spaces `U=L^2_0(p_A)` and `V=L^2_0(p_C)`. This fixes the `f -> f+c0`, `g -> g-c0` gauge. The original `R_add` in line 52 is unchanged by this centering because constants belong to the additive subspace.

The normal equations in lines 85-89 are the orthogonality equations for the residual against all zero-mean left and right functions:

`f+K_sg=m`, `g+K_s^*f=n`.

Substitution gives the inverse equations in lines 91-97. The strict contraction claim in line 99 is valid under full Cartesian support: equality in conditional expectation contraction would force a zero-mean function of `T` to agree almost surely with a function of `S`; positive mass on every `(S,T)` atom forces both functions to be constant, hence zero. In finite dimension this gives `||K_s||<1`, so `I-K_sK_s^*` and `I-K_s^*K_s` are invertible.

The value formula in lines 101-105 follows from Pythagoras at the optimum:

`R_add = ||psi_0||^2 - <psi_0,f+g> = E[psi_0^2] - <m,f> - <n,g>`.

## Unit 4: DPP rank-at-most-four reduction

Verdict: `CORRECT`.

Relevant lines:

- `ADDENDUM_JOINT_ADDITIVE.md` lines 107-132.
- `ADDENDUM_OUTER_WEDGE_FLOW_RATE.md` lines 7-17 for the accepted rank-two feature form.

For centered `g`, the constant part of `q_s` drops out. The rank-two DPP likelihood gives

`(K_sg)(S) = -s tr(G_A(S) E_{p_C}[G_C g]) + s^2 det(G_A(S)) E_{p_C}[det(G_C)g]`

as in lines 116-122. Since a real symmetric `2 x 2` matrix has three independent entries, the range is contained in the span of those three `G_A` coordinate functions plus `det G_A`; hence rank at most four. The same argument applies on the right. The statement that components of `m` orthogonal to `Ran K_s` pass through unchanged is also correct, since `K_sK_s^*` vanishes on `Ran(K_s)^\perp`.

Minor wording note: the four features should be understood as their induced centered feature coordinates inside `L^2_0(p_A)` or `L^2_0(p_C)` when solving the zero-mean normal equations. This is implicit in the surrounding gauge setup and is not a mathematical gap.

## Unit 5: analytic dual lower bound for zero-row/column interaction tables

Verdict: `CORRECT` for the abstract dual argument.

Relevant lines:

- `ADDENDUM_JOINT_ADDITIVE.md` lines 171-197.
- `input/code/verify_joint_additive_failure.py` lines 70-103 for static interface only.

For any table `c_{ST}` with zero row and column sums, `sum c_{ST}(f(S)+g(T))=0` for every additive `f+g`. For the projection residual `r=psi-f-g`,

`sum c psi = sum c r`.

Using the atom probabilities `P_s(S,T)=mu(S,T)q_s(S,T)` as the weights gives

`(sum c r)^2 <= (sum c^2/P_s(S,T)) * R_add`,

which is exactly the displayed denominator in line 196. The code statically contains the displayed integer table and row/column zero assertions at lines 70-72, then uses `Patom=mu*q` in the denominator at lines 94-97.

The independent certification of the concrete lower bound in lines 199-208 is excluded from this review.

Actionable note for publication-quality readability: state the row/column enumeration of the `8 x 8` witness table in the prose. The code uses subset-mask order through `subs(3)` at lines 14-15 and 76-79, but the markdown table itself does not name that order.

## Unit 6: finite strict witness and static code inspection

Verdict: `INCOMPLETE` for the strict numerical witness; `CORRECT` as static interface inspection.

Relevant lines:

- `ADDENDUM_JOINT_ADDITIVE.md` lines 134-231.
- `input/code/verify_joint_additive_failure.py` lines 1-117.

The script interface matches the witness narrative:

- rational matrices are encoded at lines 6-12;
- rank, density, and strict block legality assertions appear at lines 33-39;
- complete-event product atoms are built at lines 41-44 and 76-97;
- outward logarithm interval helpers appear at lines 46-68;
- the dual lower-bound comparison and true-curvature assertions appear at lines 99-105.

I did not run the script or independently reconstruct the rational/log certificate. Therefore I do not certify:

- `R_add > 192.456...`;
- the threshold `< 166.441...`;
- `W(9/10)<0`;
- `t^2 I''(t)>4.653...`;
- the resulting strict separation between true curvature and failure of the joint-additive sufficient criterion.

Those are precisely the claims requiring the separate independent certificate assigned outside this review.

## Unit 7: limited Erbar-Maas comparison

Verdict: `CORRECT`.

Relevant lines:

- `ADDENDUM_JOINT_ADDITIVE.md` lines 233-245.
- Erbar-Maas arXiv page and article text: arXiv records the 2012 v2 and abstract, and the article setup states an irreducible finite Markov kernel with reversible stationary measure and detailed balance in its main-results section.

The comparison is limited and correctly non-importing. Erbar-Maas works with an irreducible reversible finite Markov kernel and a nonlocal transport metric whose geodesics define the entropy-convexity notion. This does not identify the DPP radial parameter `t` or `tau=-log s` with an Erbar-Maas transport geodesic, and it does not cover a generally nonreversible directed visible generator. The addendum therefore correctly treats this route as structurally distinct rather than as a black-box curvature proof.

External source used: https://arxiv.org/abs/1111.2687, especially the abstract and main-results setup.

## Unit 8: remaining whole-chord boundary

Verdict: `CORRECT` as a status limitation; theorem remains `INCOMPLETE`.

Relevant lines:

- `ADDENDUM_JOINT_ADDITIVE.md` lines 247-251.
- `RESULT.md` lines 295-307.
- `accepted_pr54.md` lines 17, 29, and 71.

The addendum does not claim to prove dense correlated rank-two whole-chord entropy concavity. It explicitly leaves the general dense correlated rank-two whole chord incomplete and identifies the remaining target as a complete-event, exact projection problem over the whole legal chord. This is consistent with the accepted PR54 scope, which accepted local-center, endpoint, matching-deficit, and outer-wedge units without closing the general whole-chord theorem.

## Final classification by unit

| Unit | Classification |
| --- | --- |
| Source binding and frozen packet | `CORRECT` |
| Accepted outer-wedge dependency, limited to PR54 accepted scope | `CORRECT` |
| Two-margin projection and factor `1/2` Cauchy bound | `CORRECT` |
| Relation to one-sided residuals | `CORRECT` |
| Gauge, normal equations, strict contraction, inverse, residual formula | `CORRECT` |
| DPP rank-at-most-four reduction | `CORRECT` |
| Abstract zero-row/column dual lower bound | `CORRECT` |
| Static code interface for finite witness | `CORRECT` |
| Concrete `s=9/10` numerical strict witness | `INCOMPLETE` |
| Original `[3,15]` / `s=10` computation | `INCOMPLETE` |
| Erbar-Maas comparison | `CORRECT` |
| Whole dense correlated legal chord | `INCOMPLETE` |
| Formal verification | `INCOMPLETE` |
| Novelty / priority | `INCOMPLETE` |

## Actionable gaps

1. Obtain the separate independent rational/log certificate for the concrete `s=9/10` strict witness before promoting lines 199-231 of `ADDENDUM_JOINT_ADDITIVE.md` from author computation to accepted theorem.
2. In `ADDENDUM_JOINT_ADDITIVE.md`, specify the subset ordering used by the displayed `8 x 8` interaction table, matching the code's mask order, so the finite witness is self-contained.
3. Keep the whole legal chord marked `INCOMPLETE` unless a new proof or full exact certificate closes the complete projection problem stated in lines 247-251.

## Execution and certification limits

I performed no arithmetic, SymPy, interval, entropy, remote, or formal execution. I ran only static file reads and SHA-256 hash checks. I made no GitHub mutations and did not inspect PR comments, FIRST reports, original PR58 SECOND material, independent C2 artifacts, or `[excluded private directory]`.
