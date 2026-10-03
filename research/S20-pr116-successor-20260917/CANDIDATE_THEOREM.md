# PR116 successor: candidate sharp uniform curvature bound

**Scope: the natural exchangeable 3+3 family only.**
**Status of this recovery delivery: candidate author result; not an independent review.**

Let `Q=11^T/3`, `P=I_3-Q`, `r=alpha(1-alpha)`,
`A=alpha P+beta Q`, `C=I-A` and `B=sqrt(r)P`, where `0<alpha,beta<1`.
The physical affine kernel is `K(t)=[[A,tB],[tB,C]]`, `-1<=t<=1`.
`H(t)` denotes complete-configuration Shannon entropy of the 64 observed events,
with natural logarithms. It does not denote spectral entropy.

The strongest result reported during the preceding work was

    H''(t) <= -64 r^2 t^2,             -1<t<1,

with the corresponding closed-chord statement that

    H(t) + (16/3) r^2 t^4

is concave. Endpoint second derivatives need not be finite; the closed-chord
claim uses continuity, not an assertion of finite endpoint curvature.

The proof route is to use all complete events, writing `s=t^2` and
`p_E(t)=mu_E(1-a_E s+b_E s^2)`, and to prove the joint-kernel bound

    J(s,u) = sum_E mu_E [4(a_E-2s b_E)^2/d_E^2
              + 2(a_E-s b_E)(a_E-6s b_E)/d_E] >= 64r^2,
    d_E = 1+u(-a_E s+b_E s^2),   0<=u<=1.

The identity `-H''(t)/t^2 = integral_0^1 J(s,u)du` then supplies the result.
The Fisher and acceleration terms are both retained. The previous work
reported four subregion certificates for the 64 bound. Earlier intermediate
results reported a 44,625-coefficient `alpha=1/10` certificate and a
2,275,875-coefficient full-parameter positivity certificate with 20 negative
coefficients absorbed by disjoint positive terms. These are records of what
was reported, not fresh execution claims made by this recovery note.

The exact model in this delivery reconstructs every complete event directly
from determinants and tests the sharpness datum at `alpha=beta=1/2`, `s=0`:
`Gamma=4` and `r^2=1/16`. Thus, conditional on the uniform bound being proved,
64 cannot be replaced by a larger constant. That single exact datum is not
by itself a proof of the uniform bound.

## Evidence boundary

The prior continuation could not bind readable execution responses to the
reported continuum certificate. It therefore cannot newly certify the
four-region certificate from that session. `exact_model.py` supplies a
separate, standard-library-only exact model and finite checks. Those finite
checks must not be substituted for the missing continuum verification.
No independent review, novelty assessment, formal verification, merge,
general rank-two theorem or entropy-rate theorem is claimed.

## Upstream context

Repository: `randomcat4/dpp-entropy-tools`
PR116: `https://github.com/randomcat4/dpp-entropy-tools/pull/116`
Frozen PR116 head: `3f276c09fe4da3aded2ab6cf457adb7fdc4254d8`
Canonical old handoff:
`research/I05-31-rank2-middle-20260910/FINAL_HANDOFF.md`

PR116 was already merged. This is a successor Draft PR, not a claim to have
newly merged PR116.
