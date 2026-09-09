# PR54 OUTER-WEDGE appendix second review

Frozen head: `c8486bcdb18a85f93dd27930686cc1d4146804f5`

Overall verdict: `ACCEPTED_SCOPED`.

This certifies only the OUTER-WEDGE appendix and its exact symbolic/rational verifier files at the frozen head:

- `research/I05-23-20260909/ADDENDUM_OUTER_WEDGE_FLOW_RATE.md`
- `research/I05-23-20260909/code/verify_outer_wedge_and_flow.py`
- `research/I05-23-20260909/output/verify_outer_wedge_and_flow.json`

I did not use the prior first-review artifacts and did not run any new LP/search/scout computation.

## Scope verdict table

| Claim | Status | Source anchors |
|---|---:|---|
| Exact full-event outer-wedge curvature normal form | `ACCEPTED_SCOPED` | `ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:23-95`, `code/verify_outer_wedge_and_flow.py:25-35`, `output/verify_outer_wedge_and_flow.json:7-12` |
| `W(s)>=0` as a sufficient condition for radial entropy concavity | `ACCEPTED_SCOPED` | `ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:69-75`, `97-112` |
| Four-sign determinant tilts and stochastic-order sufficient conditions | `ACCEPTED_SCOPED` | `ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:115-176` |
| No visible linear operator can implement distinct degree-one/degree-two scaling in the stated strict correlated two-point scope | `ACCEPTED_SCOPED` | `ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:180-259`, `code/verify_outer_wedge_and_flow.py:37-48`, `output/verify_outer_wedge_and_flow.json:2-5` |
| Exact one-line Farkas infeasibility witness for the standard correlated fixture | `ACCEPTED_SCOPED` | `ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:261-284`, `RESULT.md:682-725`, `code/verify_outer_wedge_and_flow.py:50-77`, `output/verify_outer_wedge_and_flow.json:14-27` |
| Finite Jensen bridge from subextensive negative `W_n` to entropy-rate concavity | `ACCEPTED_SCOPED` | `ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:288-350` |

## Review findings

### A. Outer-wedge normal form

The normal form is algebraically correct and uses the full complete-event law. Starting from the reviewed rank-two likelihood
`q_s=1-sa+s^2b` with `s=t^2`, the definitions `u=q_s-1` and `y=s^2b` give
`partial_t q_s = 2(u+y)/t` and `partial_t^2 q_s=(2u+10y)/t^2`
(`ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:25-45`, `87-93`). Substituting these into the full entropy derivative identity
`I''=E[(partial_t q)^2/q+(partial_t^2 q)log q]` yields exactly
`t^2 I''=E[Phi(u)+4y^2/(1+u)+y psi(u)]`
(`ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:47-57`, `79-95`). The symbolic checker independently expands the same identity and records zero difference
(`code/verify_outer_wedge_and_flow.py:25-35`, `output/verify_outer_wedge_and_flow.json:7-12`).

The positivity claims are also correct. For strict legal `t`, `q_s>0`, hence `u>-1`. Then `4u^2/(1+u)>=0`, `u log(1+u)>=0`, and
`psi'(u)=8/(1+u)^2+10/(1+u)>0` with `psi(0)=0`, so `psi` has the sign of `u`
(`ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:60-72`). Therefore the scalar `W(s)=E[b psi(u_s)]` is the only remaining signed expectation. If `W(s)>=0` throughout a strict legal `s` interval, then `I''(t)>=0` for both branches `t=±sqrt(s)`, so `H''(K(t))=-I''(t)<=0`. At `t=0`, the quartic onset gives `I''(0)=0`; no false division-by-zero endpoint claim is needed (`ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:75-95`).

The sufficient sign tests are one-way only, as stated. Eventwise `b u_s>=0` implies `b psi(u_s)>=0`, and the stronger condition `ab<=0` implies `b u_s=s(-ab+sb^2)>=0` for all `s>=0`
(`ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:97-112`). This is not asserted as an equivalence and does not claim a universal sign law.

### B. Four-ring tilt decomposition

The four-ring identity is exact. Since the determinant features have zero mean, a nonzero feature has equal positive and negative masses, making the four tilts well-defined probability measures
(`ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:115-144`). Expanding
`alpha beta=(alpha_+-alpha_-)(beta_+-beta_-)` gives the displayed contrast for every finite function `f`
(`ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:146-160`). Applying it to `f=psi(u_s)` preserves all complete events.

The stochastic-order criterion is a correct sufficient condition. With the usual first-order stochastic dominance convention, `L_{++}(u_s) >=_st L_{+-}(u_s)` gives
`E_{++} psi(u_s) >= E_{+-} psi(u_s)`, and `L_{--}(u_s) >=_st L_{-+}(u_s)` gives the second nonnegative difference. Their sum is exactly `W(s)/(m_A m_C)` (`ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:162-176`).

### C. Visible-state scaling obstruction

The linear-collision theorem is valid. If `d` lies in the span of the three degree-one features and is nonzero, any linear operator scaling each `G_ij` by `theta` must scale `d` by `theta`, contradicting a required `theta^2` scaling for `0<theta<1`. The generator version with eigenvalues `-1` and `-2` is the same linearity argument (`ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:193-212`).

The strict correlated two-point corollary supplies the needed span relation. For `G=V^T Y^{-1}V`, inversion gives
`Y=V G^{-1}V^T=V adj(G)V^T/det(G)`. Since subtracting `E_{T^c}` changes only diagonal entries, the off-diagonal entry of every `Y_T` is the same nonzero `c`, so
`det(G_T)=c^{-1} e_1^T V adj(G_T)V^T e_2`, a linear combination of `G_11,G_12,G_22`
(`ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:214-257`). The symbolic verifier expands this numerator and gets zero difference from the displayed linear formula
(`code/verify_outer_wedge_and_flow.py:37-48`, `output/verify_outer_wedge_and_flow.json:2-5`).

This is a scoped disproof of a visible-state linear scaling mechanism only. It does not rule out hidden-state dilation, does not prove or disprove universal `W(s)` sign, and does not conflict with fixed higher-state flow certificates outside the strict correlated two-point/invertible-`V` collision scope
(`ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:247-259`, `282-284`, `354-366`).

### D. One-line Farkas witness

The witness is exact under the directed-flow LP interface. `RESULT.md:682-725` defines variables `r_xy>=0`, balance equations, feature equations, and the Farkas sign convention `A^T y>=0`, `b^T y<0`. For the fixture
`C=[[1/2,1/10],[1/10,1/2]]`, `V=I_2`, all four states satisfy `d=-10G_12`
(`ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:261-273`, `output/verify_outer_wedge_and_flow.json:14-27`).

Taking multiplier `10` on the `G_12` equation at target state `11` and multiplier `1` on the `d` equation at target state `11` gives each incoming flow variable coefficient
`10(G_12(x)-G_12(11))+(d(x)-d(11))=0`; all other variables have coefficient zero because all other multipliers are zero. The combined right-hand side is
`-(6/25)*10*(-5/12)-2*(6/25)*(25/6)=1-2=-1<0`
(`ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:275-282`, `code/verify_outer_wedge_and_flow.py:50-77`). This is a valid rational Farkas certificate; no LP solve is needed.

### E. Finite Jensen rate bridge

The rate bridge is valid and avoids differentiation under a limit. For each finite `n`, the outer-wedge normal form gives
`t^2 I_n''(t) >= t^4 W_n(t^2) >= -t^4 rho_n`; by continuity this also covers `t=0`. Hence
`H_n''(t)=-I_n''(t)<=t^2 rho_n<=T^2 rho_n` on the common strict legal interval
(`ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:288-338`). Therefore
`F_n(t)=H_n(t)-(T^2 rho_n/2)t^2` is concave, and Jensen for `F_n` gives exactly the finite defect bound in (D.2)
(`ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:340-346`).

After dividing by `N_n`, the assumed pointwise entropy-rate limits at the three fixed points `x,y,z` are enough, and `rho_n/N_n -> 0` removes the finite defect. No derivative of `h` is asserted or needed (`ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:312-324`, `346-350`). The common-interval and normalization hypotheses are explicit (`ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:292-323`).

## Specific correction / precision note

No blocking correction is needed for the scoped mathematics. One wording change would make the normal-form discussion cleaner:

- At `ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:69-75`, replace “The only term in (A.1) that is not pointwise nonnegative is `W(s)`” with “The only contribution whose expectation is not already forced nonnegative is `s^2 W(s)`.” This avoids calling `W(s)`, an expectation, a pointwise term of (A.1). The proof and conclusion are unchanged.

## Limitations

This review does not certify the original `RESULT.md`, except for the narrow directed-flow LP interface lines needed for the Farkas witness. It also does not certify general whole-chord concavity, hidden-state dilation, universal `W(s)>=0`, the compact middle interval, or any successor changes outside the three unchanged OUTER-WEDGE files.
