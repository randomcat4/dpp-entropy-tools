# I05-29 — signed conditional-pair decomposition beyond additive projection

Base: current `main`, 2026-09-10.  Continuation of the accepted PR54/PR58 rank-two cross-block program.

Status of this packet:

- **PROVED (author proof; PENDING_REVIEW)**: exact conditional two-event decomposition of the complete rank-two curvature, retaining the sign of the mixed term and every complete event/Fisher/acceleration contribution.
- **DISPROVED (analytic, no machine work)**: the stronger route that relaxes `(Delta u,Delta y)` to a free two-dimensional vector and demands pairwise PSD for every positive `(q,q')`.
- **PROVED (author proof; PENDING_REVIEW)**: a DPP-constrained ratio-cone sufficient criterion depending on the actual relation `Delta u=-s Delta a+Delta y`; this is structurally different from the accepted best additive projection.
- **INCOMPLETE**: certification that the new ratio-cone criterion covers the accepted PR58 `s=9/10` additive-projection-failure fixture; no claim of coverage is made here.
- **INCOMPLETE**: general dense correlated rank-two whole-chord concavity.

No old RUNNING flag or author self-assessment is treated as independent acceptance.

## 1. Frozen accepted input

For a strict real rank-two cross-block point

`K(t)=[[A,tB],[tB^T,C]]`, `s=t^2`,

use the accepted complete-law likelihood

`q=1+u=1-sa+s^2 b`, `y=s^2 b`,

and

`Phi(u)=4u^2/q+2u log q`,

`psi(u)=8u/q+10 log q`.

With `I(t)=H(A)+H(C)-H(K(t))`, accepted PR54/PR58 gives

`t^2 I''(t)=E_mu[Phi(u)+4y^2/q+y psi(u)]`.            (1.1)

For each fixed left configuration `S`, the right conditional reference law is `nu=p_C`; fixed DPP marginals imply

`E_nu a=E_nu b=0`, hence `E_nu u=E_nu y=0`.          (1.2)

The same statements hold after interchanging left and right.

## 2. Exact signed two-event identity on one conditional fiber

Fix `S` and draw `T,T'` independently from `nu=p_C`.  Write primes for the second copy and

`Delta u=u-u'`, `Delta y=y-y'`, `q=1+u`, `q'=1+u'`.

Define the positive logarithmic divided difference

`L(q,q')=(log q-log q')/(q-q')` if `q!=q'`, and `L(q,q)=1/q`.

### Theorem 2.1 (conditional signed-pair decomposition)

On every strict conditional fiber,

`E_nu[Phi(u)+4y^2/q+y psi(u)]`

is exactly

`E_{nu x nu} J(T,T')`,                                      (2.1)

where

`J=2[(u^2+y^2)/q+(u'^2+y'^2)/q']`

`  + L(q,q') (Delta u)^2`

`  + [5 L(q,q') + 4/(q q')] Delta u Delta y`.              (2.2)

Consequently the full curvature is the `p_A`-average of these exact right-fiber pair expectations.  The symmetric left-fiber version is identical.

#### Proof

Because `E u=0`, the independent-copy covariance identity gives

`E[2u log q]=E[(u-u')(log q-log q')]`

`              =E[L(q,q')(Delta u)^2]`.                    (2.3)

Because `E y=0`, similarly

`10E[y log q]=5E[(y-y')(log q-log q')]`

`              =5E[L(q,q') Delta y Delta u]`.              (2.4)

Also `u/q=1-1/q`, so

`(u/q-u'/q')=(q-q')/(q q')=Delta u/(q q')`.

Thus

`8E[y u/q]=4E[(y-y')(u/q-u'/q')]`

`           =4E[Delta y Delta u/(q q')]`.                  (2.5)

Finally, for any one-copy function `g`, `E[g]=E[(g+g')/2]`; hence

`E[4u^2/q+4y^2/q]`

`=E[2((u^2+y^2)/q+(u'^2+y'^2)/q')]`.                       (2.6)

Adding (2.3)--(2.6) proves (2.1)--(2.2).  No absolute value, event deletion, spectral rotation, or change of physical parameter is used.  QED.

## 3. Fast falsification of the over-relaxed pairwise-PSD route

A tempting next step is to lower-bound, at fixed differences,

`u^2/q+u'^2/q' >= (Delta u)^2/(q+q')`,

`y^2/q+y'^2/q' >= (Delta y)^2/(q+q')`,                     (3.1)

and then demand the resulting quadratic form be PSD for every free pair `(Delta u,Delta y)`.

This gives

`Q=A (Delta u)^2+B (Delta y)^2+C Delta u Delta y`,          (3.2)

with

`A=2/(q+q')+L`, `B=2/(q+q')`,

`C=5L+4/(q q')`.                                           (3.3)

The free-vector PSD requirement would be `C^2<=4AB`.

### Proposition 3.1

The free-vector pairwise-PSD requirement is impossible even infinitesimally around equal likelihoods, hence it cannot be the desired general mechanism.

#### Proof

At `q'=q>0`, `L=1/q`, so

`A=2/q`, `B=1/q`, `C=5/q+4/q^2`.

PSD would require

`(5+4/q)^2 <= 8`,

which is impossible because the left side is strictly larger than `25`. QED.

This is a method counterexample only.  It says nothing adverse about entropy concavity.

## 4. DPP-constrained ratio cone

The failed relaxation in Section 3 threw away the rank-two identity

`Delta u=-s Delta a+Delta y`.                               (4.1)

Therefore `(Delta u,Delta y)` is not a free planar vector on an actual event pair.  When `Delta u!=0`, put

`r=Delta y/Delta u`.

Using (3.1) only after imposing the actual ratio gives the lower pair kernel

`J >= Q = (Delta u)^2 F(q,q',r)`,                               (4.2)

where

`F(q,q',r)= L+2(1+r^2)/(q+q') + r[5L+4/(q q')]`.           (4.3)

If `Delta u=0`, then the exact pair kernel (2.2) reduces to the nonnegative first line

`2[(u^2+y^2)/q+(u'^2+y'^2)/q']`.

### Theorem 4.1 (conditional ratio-cone sufficient criterion)

Fix one side, say the left side.  Suppose that at a strict legal `s=t^2>0`, for every left configuration `S` and every pair of right configurations `T,T'` with `Delta u!=0`, the actual DPP pair satisfies

`F(q,q',Delta y/Delta u) >= 0`.                             (4.4)

Then `t^2 I''(t)>=0`, hence `H''(t)<=0` because `t!=0`. Strictness follows if (4.4) is strict on a positive-mass pair with `Delta u!=0`, or if a positive-mass one-copy atom has `u` or `y` nonzero. For the latter condition, the diagonal pair `T=T'` has `J=4(u^2+y^2)/q>0`; all other pairs are nonnegative under the cone hypothesis. Thus `t^2 I''(t)>0` and `H''(t)<0`. Pair-local reserve-square strictness is described separately in the signed-fiber addendum.

The same theorem holds with left/right interchanged.

#### Proof

Apply (3.1) inside the exact identity (2.2), but only on the actual DPP ratio `r`.  Each pair contribution is then bounded below by (4.2), and the `Delta u=0` case is directly nonnegative.  Average first over `T,T'`, then over `S`.  QED.

### Corollary 4.2 (interval family form)

Let a parameterized family of strict rank-two DPPs satisfy, on an `s`-interval, deterministic envelopes

`0<q_-<=q_+` and `q,q' in [q_-,q_+]`, and for every actual conditional pair with `Delta u!=0`,

`r=Delta y/Delta u in R`,                                   (4.5)

where `R` is a fixed union of intervals.  If

`inf_{q,q' in [q_-,q_+], r in R} F(q,q',r) >=0`,            (4.6)

then `H''(t)<=0` for every physical parameter with `t^2` in the stated interval and `t!=0`. Hence entropy is concave on each connected `t`-interval covered by these hypotheses. Strict curvature requires at each parameter either a positive-mass `Delta u!=0` pair with strict `F`, or the positive-mass one-copy/diagonal witness from Theorem 4.1. This statement alone does not cover other `t`-bands or the endpoint `t=0`.

This is a genuine structural family theorem: the input is a likelihood window plus an event-pair ratio cone, not an additive Hilbert residual.  It can in principle be certified from block-level inequalities controlling `Delta a` versus `Delta b`.

## 5. Why this is different from the accepted additive projection

The accepted best additive projection replaces the signed quantity

`<h,psi>_{P_s}`, `h=y/q`,

by a worst-sign Cauchy bound after subtracting all additive functions of the two block configurations.  The PR58 `s=9/10` witness proves that this relaxation can lose too much even though true curvature remains favorable.

The pair identity (2.2) does not enlarge that additive space.  It changes the place where information is discarded: it first uses the exact zero conditional means and keeps the sign of `Delta y Delta u`.  Only after that does Theorem 4.1 use the DPP relation (4.1) through the actual scalar ratio `r`.

The over-relaxed two-dimensional PSD variant fails analytically by Proposition 3.1, so any successful use of this route must retain the DPP ratio constraint; this failure is preserved rather than hidden.

## 6. Comparison with a structurally different route and primary sources

A second route is a genuine second-order entropy-dissipation inequality for a fixed nonreversible or hidden-state generator.  It is structurally different from Sections 2--4 because it would explain curvature through a semigroup/intertwining rather than complete-event pair symmetrization.

Caputo--Dai Pra--Posta, *Convex entropy decay via the Bochner--Bakry--Emery approach*, Ann. IHP Probab. Stat. 45 (2009), DOI 10.1214/08-AIHP183, develops Bochner identities precisely to prove convex decay of relative entropy for discrete Markov processes.  This supports the need for a second-order dissipation estimate, not mere data processing.

Erbar--Maas, *Ricci curvature of finite Markov chains via convexity of the entropy*, Arch. Rat. Mech. Anal. 206 (2012), arXiv:1111.2687, uses geodesic entropy convexity for finite reversible Markov chains in a nonlocal transport metric.  Its reversible/geodesic hypotheses do not identify the physical DPP radial parameter with such a geodesic and therefore do not directly prove the present claim.

The accepted visible two-point feature collision already rules out the simplest universal visible linear exterior-scaling mechanism.  A hidden dilation would still need an exact visible marginal and a proof that the required second-order curvature descends after projection.  No such bridge is claimed here.

## 7. The new `s=9/10` fixture: current first falsification status

For the accepted PR58 additive-projection-failure fixture at `s=9/10`, the retained certificate gives

`P0 > 5.4701601089890834`,

`A2 = 1.0088153687530381...`,

`W<0`, and

`t^2 I'' > 4.653598245398841 >0`,                           (7.1)

while `R_add>192.456...` exceeds the old sufficient threshold `<166.442`.

Those facts establish that the old projection loses sign information, but they do not by themselves certify (4.4), because (4.4) is an event-pair ratio condition.  I do **not** infer it from (7.1).

A bounded checker should test (4.4) on the existing 64-event rational fixture without recomputing the whole chord.  That test is a falsification check for the new theorem interface, not a main result.  Until such a check is independently run, coverage of the `s=9/10` witness is **REQUESTED / PENDING_REVIEW**, not proved.

## 8. Heavy-compute boundary and remaining gap

Issue #63 is already the bounded >60-minute whole-chord job for the older additive criterion on the accepted PR54 fixture.  This packet does not duplicate it and does not turn another 64-event run into the main contribution.

The main analytic next step is one of:

1. derive block-level sufficient bounds forcing the actual ratios `r=Delta y/Delta u` into a cone where (4.3) is nonnegative; or
2. replace pairwise nonnegativity by an exact signed average inequality over each conditional fiber, allowing bad individual pairs to cancel; or
3. construct a fixed nonreversible/hidden generator with exact marginalization and prove the genuine second-order entropy-dissipation inequality.

General dense correlated rank-two whole-chord concavity remains **INCOMPLETE**.  This packet proves a new exact decomposition and a new structural sufficient theorem, disproves its most naive over-relaxation, and keeps the accepted `s=9/10` target explicitly open rather than claiming it by self-review.
