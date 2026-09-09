# PR54 first-pass proof review

Reviewer role: fresh non-author first proof review for PR54 only.

Reviewed source object: immutable PR54 commit `203f7044815faac9a2de7bc8dbc5bfe249026b1f`, three-file bundle `sources/pr54`.

Not reviewed: later `pr54_daf9c31` addenda, PR51, issue 52, current remote-head changes, broad novelty/priority.

Overall verdict: **ACCEPTED_SCOPED with localized NEEDS_FIX items in Section 5 wording**. I found no critical gap in the main finite local rank-two curvature theorem, the matching entropy-deficit theorem, or the stationary two-layer entropy-rate deficit. The imset, flow, MLSI, and uniform third-derivative parts are correctly presented as interfaces or incomplete obligations. Two statement-level repairs are needed in Proposition 5.2/boundary-remainder text: explicitly include the `I_n'(0)=0` hypothesis used in the proof, and weaken the sentence saying the matching construction realizes the concave-approximant principle.

No new computation was run. The saved exact fixture output was read and checked against the script structure as a consistency artifact; it is not used as a substitute for any general proof.

## C1. Strict local radial curvature for arbitrary rank-two cross block

Proof status: **CORRECT**.

Review verdict: **ACCEPTED_SCOPED**.

Relevant source lines: statement at `RESULT.md` lines 107-188, proof at lines 190-321, scope at lines 323-328.

Proof chain checked:

- The complete-event determinant formula and Schur-complement reduction give the exact likelihood
  `q_s(S,T)=1+s u(S,T)+s^2 v(S,T)` with `s=t^2`; see lines 194-205.
- Normalization of the full complete law gives `E_mu u=E_mu v=0`; see lines 206-209.
- The block marginals remain `A` and `C`, so the entropy loss is the full mutual information `D(p_s||mu)`, not a projected-event entropy; see lines 211-220.
- The nonzero first-score lower bound is valid. For a nonzero entry `B_ij`, the two-point inclusion identity gives `E_mu[Z_ij u]=-B_ij^2`; Cauchy-Schwarz yields
  `sigma^2 >= B_ij^4/(A_ii C_jj(1-A_ii C_jj)) > 0`; see lines 222-252.
- The derivative identities for `I(s)` retain the complete Fisher term `(q_s')^2/q_s`; see lines 258-276.
- The `I'''` bound follows from `q_s >= 1/2`, `|q_s'| <= M_1`, and `|q_s''| <= 2V_0`, giving `L_3=12M_1V_0+4M_1^3`; see lines 278-289.
- The conversion from `s` to the true radial parameter `t` is correct:
  `H''(t)=-(2I'(s)+4sI''(s))`, with `s=t^2`; see lines 291-321.
- The legal radius is in the correct variable: `delta_leg` is an `s`-radius because `|t| <= epsilon/(2 beta)` is equivalent to `s <= (epsilon/(2 beta))^2`; see lines 164-177 and 319-320.

Boundary checks:

- Rank two is used exactly in the determinant lemma producing a quadratic likelihood in `s`.
- `B != 0` supplies a nonzero entry and hence a nonzero score.
- Strictness of `A` and `C` gives full support for the product complete law and invertibility of every `X_S,Y_T`.
- The theorem proves only a certified neighborhood of `t=0`; it does not imply whole-chord concavity.

## C2. Exact rational fixture

Proof status: **CORRECT as a fixture**.

Review verdict: **ACCEPTED_SCOPED**.

Relevant source lines: `RESULT.md` lines 82-101; `code/verify_local_and_matching.py`; `output/verify_local_and_matching.txt`.

The script uses rational matrices, asserts `rank(B)=2`, checks strictness of `A,C,I-A,I-C`, enumerates all 64 complete configurations for a `3+3` example, verifies the likelihood identity against exact event determinants at `t=1/10`, checks `E u=E v=0`, verifies the pair-score identity, and computes an exact local radius and matching coefficient. The saved output reports all assertions passed.

This supports arithmetic consistency of the displayed formulas. It does not prove generic local curvature or global chord claims by enumeration, and PR54 does not use it that way.

## C3. Strong-Rayleigh/SCP martingale moment bound

Proof status: **CORRECT**.

Review verdict: **ACCEPTED_SCOPED**.

Relevant source lines: `RESULT.md` lines 340-375.

The martingale proof has the right orientation and constants. Conditional stochastic covering gives a coupling of the two conditional remainders differing in at most one bit; including the revealed coordinate makes the two full configurations differ in at most two bits. A 1-Lipschitz `F` therefore gives martingale conditional values in an interval of length at most two, and Hoeffding's lemma contributes `exp(lambda^2/2)` per coordinate. Iterating over `N` coordinates gives the claimed `N lambda^2/2`.

The law used later is the baseline product law `mu=P_0`, not the joint law `P_t`; this is correct because the variational argument tests `P_t` against concentration under `mu`.

## C4. Entropy variational inequality

Proof status: **CORRECT**.

Review verdict: **ACCEPTED_SCOPED**.

Relevant source lines: `RESULT.md` lines 377-392.

This is the standard entropy duality inequality obtained by tilting `mu` by `exp(lambda(F-E_mu F))` and using nonnegativity of relative entropy. No extra boundedness hypothesis on `F` is needed in the finite setting.

## C5. Finite cross-matching entropy deficit

Proof status: **CORRECT**.

Review verdict: **ACCEPTED_SCOPED**.

Relevant source lines: `RESULT.md` lines 394-454.

Proof chain checked:

- The fixed block marginals give `H(K(0))-H(K(t))=D(P_t||p_A \otimes p_C)`; see lines 416-424.
- The baseline product of two DPP laws is strong Rayleigh, so Lemma 2.1 applies to the baseline law; see lines 425-426.
- Because `M` is a matching, changing one occupancy bit changes `Z_M` by at most one; see lines 428-434.
- The exact two-point inclusion shift is
  `E_{P_t} X_i X_j - E_mu X_i X_j = -t^2 B_ij^2`; see lines 435-443.
- Applying the variational inequality with `lambda=-t^2 W_M/N` gives
  `D(P_t||mu) >= t^4 W_M^2/(2N)`; see lines 444-454.

Boundary checks:

- If `B != 0`, a one-edge matching has `W_M>0`; the lower bound is strict for every legal `t != 0`.
- The complete law is retained. The matching statistic is only a test function in the full relative entropy.
- No rank-two assumption is needed here; the statement is correctly more general in `B`.

## C6. Two-layer stationary entropy-rate deficit

Proof status: **CORRECT**.

Review verdict: **ACCEPTED_SCOPED**.

Relevant source lines: `RESULT.md` lines 456-510.

For a fixed offset `d`, the window `1,...,n` contains exactly `q_n=n-|d|` matched left-right pairs once `n>|d|`. The finite theorem uses `W_n=(n-|d|)|b_d|^2` and `N_n=2n`, so after dividing by `n` the lower bound is
`t^4 (n-|d|)^2 |b_d|^4/(4 n^2)`. Taking `n -> infinity` gives the constant `1/4`; see lines 481-498.

The boundary normalization is correct: the lost pairs are exactly the `|d|` boundary cells, and the proof keeps their contribution visible before passing to the limit. If the Toeplitz cross block is nonzero, some offset has `b_d != 0`, giving strict rate deficit for every legal `t != 0`.

This remains a global quartic deficit from `t=0`. Lines 500-510 correctly do not promote it to chord concavity or a second-derivative sign.

## C7. Elementary-imset four-cycle certificate interface

Proof status: **CORRECT as a conditional certificate**.

Review verdict: **ACCEPTED_SCOPED for the interface; INCOMPLETE for the universal cone assertion**.

Relevant source lines: `RESULT.md` lines 514-604.

The sign bookkeeping checks out. For a strict determinantal complete law, conditioning outside `{i,j}` and using two-coordinate negative correlation gives
`p(R)p(Rij) <= p(Ri)p(Rj)`, hence `<e^{ij|R},log p> <= 0`; see lines 533-543. For an indefinite rank-two line `K+z(aa^T-bb^T)`, the positive rectangle coefficient satisfies `c=-m`; see lines 547-568. If `m` lies in the nonnegative cone generated by the elementary imsets, then `<c,log p> >= 0`, and the entropy curvature formula
`H''(0)=-sum r^2/p - 2<c,log p> <= 0` follows with the full Fisher term; see lines 570-586.

The rational feasibility/Farkas interface at lines 588-599 is the right certificate standard. The universal claim that the representation always exists is explicitly marked incomplete at lines 601-603, so no unproved imset theorem is being smuggled into the branch.

## C8. Pairwise stochastic covering does not imply square coupling

Proof status: **CORRECT**.

Review verdict: **ACCEPTED_SCOPED**.

Relevant source lines: `RESULT.md` lines 605-653.

The two-bit example has all four adjacent pairwise covering relations: `{1}` covers `empty` on both lower edges, and `{1,2}` covers `{1}` on both upper edges. A square coupling supported on `(R,Ri,Rj,Rij)` with endpoints forced to `empty` and `{1,2}` would require the two middle sets to be distinct, namely `{1}` and `{2}` in some order. The prescribed middle marginals are both point masses at `{1}`, so no such square coupling exists.

This correctly refutes only the inference from pairwise covering to a common square coupling. It does not refute the DPP-specific cone representation.

## C9. Directed-flow/Farkas and entropy-curvature interface

Proof status: **CORRECT as an interface**.

Review verdict: **ACCEPTED_SCOPED for the interface; INCOMPLETE for existence and Bochner curvature**.

Relevant source lines: `RESULT.md` lines 670-818.

The density-adjoint formula is correct. With `r_xy=mu_x q_xy`, stationarity makes incoming and outgoing flow at each state equal, and the adjoint on densities relative to `mu` is
`(L^dagger f)(y)=mu_y^{-1} sum_{x != y} r_xy(f(x)-f(y))`; see lines 684-699. The exterior scaling equations and their rational linear feasibility/Farkas formulation are also correctly stated at lines 701-727.

The entropy-trajectory calculation has the right signs. If `L^dagger` sends degree-one features to `-1` times themselves and the determinant feature to `-2` times itself, then `f_s=1-sa+s^2b` with `s=s_*e^{-tau}` satisfies `partial_tau f_s=L^dagger f_s`; see lines 734-742. The conversion
`-H''(t)=2I'(s)+4sI''(s)=(2/s)(2 Ical''+Ical')` is algebraically correct; see lines 759-768. Thus the missing condition is genuinely a second-order entropy-production inequality, equivalently `D' <= -D/2`; see lines 771-785.

Lines 787-818 correctly leave nonreversible Bochner descent and hidden-state intertwining as obligations, not completed theorems.

## C10. Curvature-to-rate sufficient criteria and limitations

Proof status: **CRITICAL_GAPS in Proposition 5.2 as written; CORRECT after two explicit statement repairs**.

Review verdict: **NEEDS_FIX for Section 5 wording; ACCEPTED_SCOPED for the intended sufficient criterion and for the extensive `I_n''(0)` lower bound**.

Relevant source lines: `RESULT.md` lines 822-939.

What checks out:

- Proposition 5.1 is correct: pointwise limits of the normalized concave finite-block entropies are concave; see lines 829-848.
- The algebra in Proposition 5.2 is correct once `I_n'(0)=0` is available. Then `J_n(0)=0`, `J_n'(s)>=3cn`, and `H_n''(t)<=-3cnt^2`; see lines 882-896.
- The extensive lower bound for `I_n''(0)` in the Toeplitz setting follows from the matching score identity, the SCP variance bound `Var(Z_n)<=2n`, and Cauchy-Schwarz; see lines 898-920.
- Lines 922-927 correctly keep the uniform `I_n'''=O(n)` estimate as an open gap and reject rare-event deletion.

Critical gaps or needed repairs:

1. `I_n'(0)=0` is used but not stated in Proposition 5.2. Line 891 says `J_n(0)=0`, while line 884 defines `J_n(0)=2I_n'(0)`. This is true for the intended DPP mutual-information/relative-entropy setup, where `I_n(s)=D(P_{n,s}||P_{n,0})` and `P_{n,s}` is normalized at `s=0`, but it is not a consequence of the displayed hypotheses alone. Fix by adding either `I_n(0)=I_n'(0)=0` or by defining `I_n` explicitly as the full relative entropy from the decoupled complete law.

2. The radius formula at line 868 divides by `L`, while the hypothesis at line 865 only says `L<infinity`. Fix by requiring `L>0`, or by adding the convention that `3c/(10L)=infinity` when `L=0`.

3. The final sentence at lines 938-939 says the matching construction realizes the boundary-remainder concave-approximant principle. The matching construction proves a boundary-controlled quartic deficit and passes that inequality to the rate; it does not construct concave approximants satisfying (5.8). Fix by replacing that sentence with a narrower statement such as: "Theorem 2.4 uses the same boundary-normalization logic for the quartic deficit, with the explicit loss `|d|/n`; it does not by itself supply concave approximants."

These are local statement/interface fixes. They do not affect the accepted matching deficit or Theorem 1 local curvature proof.

## Primary-source bridge checks

I did not perform a broad novelty search. I used PR54's cited primary sources only as bridge checks for standard external facts:

- Borcea-Branden-Liggett, strong-Rayleigh/DPP background: https://arxiv.org/abs/0707.2340
- Pemantle-Peres, stochastic covering and concentration for strong-Rayleigh measures: https://arxiv.org/abs/1108.0687
- Kashimura-Sei-Takemura-Tanaka, elementary imset cone vocabulary: https://arxiv.org/abs/1109.2408
- Lyons-Steif stationary DPP entropy-rate setting: https://arxiv.org/abs/math/0204324

## Final classification table

| Claim | Proof status | Review verdict |
| --- | --- | --- |
| C1 local rank-two radial curvature | CORRECT | ACCEPTED_SCOPED |
| C2 exact rational fixture | CORRECT as fixture | ACCEPTED_SCOPED |
| C3 SCP martingale bound | CORRECT | ACCEPTED_SCOPED |
| C4 entropy variational inequality | CORRECT | ACCEPTED_SCOPED |
| C5 finite matching entropy deficit | CORRECT | ACCEPTED_SCOPED |
| C6 stationary entropy-rate deficit | CORRECT | ACCEPTED_SCOPED |
| C7 imset certificate interface | CORRECT as conditional certificate | ACCEPTED_SCOPED; universal assertion INCOMPLETE |
| C8 pairwise covering vs square coupling | CORRECT | ACCEPTED_SCOPED |
| C9 directed-flow/curvature interface | CORRECT as interface | ACCEPTED_SCOPED; existence/Bochner step INCOMPLETE |
| C10 curvature-to-rate criterion | CRITICAL_GAPS as written; correct after explicit hypotheses | NEEDS_FIX |

## Compute plan status

No `COMPUTE_PLAN.md` was created because I did not identify a necessary new finite load-bearing computation for this first pass. The existing exact fixture and saved output were inspected as part of the three-file source object, and no new formal proof claim depends on rerunning or extending it here.
