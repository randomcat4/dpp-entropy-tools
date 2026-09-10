# Exact fixed inputs, a failed bridge, and certificate semantics

Status: **DISPROVED** for the universal auxiliary bridge `H(p_(A+B)/2) >= H((p_A+p_B)/2)` on rank-two endpoints. **No entropy-concavity counterexample** is obtained. All finite certifications here are author computations, **PENDING_REVIEW**, separate from the analytic proofs in `proof.md` and `continuation.md`.

The true Jensen sign convention is

\[
\Delta={H(A)+H(B)\over2}-H((A+B)/2),\qquad G=-\Delta.
\]

A positive auxiliary difference `H((p_A+p_B)/2)-H(p_(A+B)/2)` is not Delta. Shannon concavity can compensate it.

## 1. Dense moving rank-two endpoints with a rank-four arithmetic midpoint

Let `r=1/1000`. For actual coordinate indices i,j define `R_ij(r)` to be identity outside those coordinates, with their ordered two-by-two block

\[
\begin{pmatrix}c&-s\\s&c\end{pmatrix},\qquad
c={1-r^2\over1+r^2},\quad s={2r\over1+r^2}.
\]

These are exact rational orthogonal matrices. Put

\[
P=(I_3-\tfrac13{\bf1}{\bf1}^T)\oplus0,\quad
R=R_{14}(r),\quad V=R_{24}(r)R_{13}(r),
\]
\[
A={7\over10}RPR^T,\qquad
B={9\over10}RVPV^TR^T,\qquad M={A+B\over2}. \tag{1}
\]

This specification is an exact rational three-kernel input, not a nonlinear interpolation. Only the three matrices in (1) are used for the Jensen calculation.

The endpoint spectra are `(7/10,7/10,0,0)` and `(9/10,9/10,0,0)`. Every entry of each endpoint is nonzero. The two ranges have zero intersection, and M has rank four. Positivity follows from the Gram construction, and `M <= (9/10)I`. A particularly small but essential event is

\[
p_M(\{1,2,3,4\})=\det M
={176400000000\over1000004000006000004000001}>0. \tag{2}
\]

Thus no rare quadruple event is suppressed. For a rational version of the Cauchy--Binet check, take

\[
u=(1,-1,0,0)^T,\quad v=(1,1,-2,0)^T,\quad
F=R[u,v,Vu,Vv],
\]

and weights `(7/40,7/120,9/40,9/120)`. Then `M=F diag(weights) F^T`. The code checks all its principal minors against their full weighted sums of squared column minors, including every triple and the quadruple.

### The bridge fails, but the actual entropy inequality does not

Let `q=(p_A+p_B)/2`. Exact rational logarithm bounds give

\[
0.000997234475472836494618046919201303
\le H(q)-H(p_M)\le
0.000997234475472836494618046919201304. \tag{3}
\]

Therefore the entropy-increasing law bridge used for rank-one endpoints cannot be universally extended to rank-two endpoints. On exactly the same three kernels,

\[
-0.061988468197200066716751242851164212
\le\Delta\le
-0.061988468197200066716751242851164211. \tag{4}
\]

The true Jensen difference is strictly negative. This is a certified **method obstruction**, not a disproof of entropy concavity.

The pair-inclusion corrections relative to q have both signs: they are negative on pairs `{1,2}`, `{1,3}`, `{2,3}` and positive on `{1,4}`, `{2,4}`, `{3,4}`. Their exact fractions are stored in `certificate_compact.json`; each is checked against `-det(B-A)_ij/4`. Mixed-area coefficients themselves are nonnegative, but the difference from the endpoint mixture need not be. Higher-order exact atoms additionally involve the alternating triple/quadruple corrections from `proof.md`.

### A genuinely strict-kernel method obstruction

Use the same `epsilon=1/1000000` in

\[
A_e=\epsilon I+(1-2\epsilon)A,\quad
B_e=\epsilon I+(1-2\epsilon)B,\quad
M_e=(A_e+B_e)/2.
\]

All three kernels lie in the strict spectral interval `[epsilon,1-epsilon]`. Independent bit flips send q to `q_e=(p_Ae+p_Be)/2` because the channel is linear on laws. The exact finite-alphabet continuity bound in `proof.md` gives

\[
H(q_e)-H(p_{M_e})\ge H(q)-H(p_M)-2\omega_4(\epsilon)
>0.000868136541936321756806604581814946,
\]
\[
\Delta_e\le\Delta+2\omega_4(\epsilon)
<-0.061859370263663551978939800513777855. \tag{5}
\]

The stored `lift_bridge_lower_bound_enclosure` encloses the lower-bound expression in (5), not the unknown exact lifted bridge gap. Likewise `lift_Delta_upper_bound_enclosure` encloses the upper-bound expression, not the actual lifted Delta. These meanings are intentionally distinct. Both strict signs follow without evaluating any lifted probability approximately.

## 2. Common dense-mode six-point fixture

All matrices are specified by

\[
u=(1,2,3,4,5,6)^T,\quad v=(1,-1,1,0,0,0)^T,
\quad w=(1,2,-1,0,0,0)^T,
\]
\[
A=uu^T/200+vv^T/12,\quad
B=uu^T/200+ww^T/20,\quad M=(A+B)/2.
\]

The trace bounds are `tr A=141/200<1`, `tr B=151/200<1`, so their Gram representations establish legality exactly. Their ranks are 2,2,3. With J the first three coordinates, `r=77/200` and the empty-outside conditional background coefficient is `1/123`.

The code reconstructs all 64 complete events for each of A,B,M in two ways and checks every conditional identity (12) of `proof.md`, including every exact zero. Stored certificates give

\[
G\in[0.031373360749276697060039678872067269,
0.031373360749276697060039678872067270],
\]
\[
rG_{rank1}\in[0.014128687905724210814873294528214101,
0.014128687905724210814873294528214102].
\]

For epsilon `1/100000`, the sufficient small-lift lower-bound expression has enclosure

\[
[rG_{rank1}-2\omega_6(\epsilon)]
\subset[0.012345017011345265336015381459734658,
0.012345017011345265336015381459734659].
\]

Independently, the later analytic continuation proves the all-epsilon bound `G_e>=49(1-2epsilon)^2/7200` for this entire coordinate-supported class. A finite fixed-input calculation is not what establishes that all-epsilon conclusion.

## 3. Strong multiring fixture

The exact input, legal interval, conditional-anchor failure, all-atom quartic formula, and endpoint coefficient `6784/16875` appear in `continuation.md` Section 2. Its three certified sample points are `t=1/2,3/4,9/10`; each local Jensen calculation uses the actual three kernels at `t-1/100,t,t+1/100`. Their spectra remain strictly between zero and one by the explicit legality formula.

The whole compact middle is **INCOMPLETE**. The only calculation actually executed in this session is the bounded script below, not a long scan and not old issue #61's different fixture.

## 4. Reproducible execution and explicit logarithm error

Run from this directory:

```sh
python verify.py certificate.json
```

The author run used Python 3.13.5 and SymPy 1.14.0 and exited successfully. The fixed run took approximately 0.616 seconds in that environment; this is a recorded elapsed time, not a forecast for another machine. No independent review, CI, formalization or continuous interval-family certification is implied.

The event interface is adapted from accepted agent24 `code/verify_rank1_midpoint.py`. This is a single fixed-input verification script, not a new generic search framework. All inputs are embedded as exact rational expressions; no external data or random seed is required.

For each rational `x>0`, reduce `x=2^k m` with `1<=m<2` and put `z=(m-1)/(m+1)`. Then

\[
\log x=k\log2+2\sum_{j=0}^{N-1}{z^{2j+1}\over2j+1}+R_N,
\]
\[
0\le R_N\le {2z^{2N+1}\over(2N+1)(1-z^2)}
\le {9\over4(2N+1)3^{2N+1}}. \tag{6}
\]

The code takes `N=80` and dyadic scale `2^192`. Every nonnegative product, division and partial sum is rounded downward for the lower bound and upward for the upper bound. The explicit tail in (6) is added upward. `log 2` uses z=1/3 and the same method. Multiplication by a negative k or a negative entropy/acceleration coefficient reverses interval endpoints. Thus all rounding, range reduction and transcendental truncation errors are enclosed.

Every final internal entropy, gap and curvature interval is checked to have width below `10^-45`. For readability the JSON endpoints are rounded **outward** to 36 decimal places; these displayed intervals are wider than the internal ones. There are no numerical probability floors, omitted positive rare terms, or decimal-log sign decisions. Exact zero atoms use `0 log 0=0`.

The complete Fisher sums at the three multiring points are evaluated as rational numbers, without interval cancellation. Their corresponding acceleration terms `-sum p'' log p` are enclosed separately and then combined. This explicitly retains the full Hessian rather than only a cardinality layer or one favorable direction component.

`certificate_compact.json` stores all three exact atom arrays for the four-point fixture, all three for the six-point common-mode fixture, and all 64 triples of coefficients `[t^0,t^2,t^4]` for the multiring law. Array index is `mask=sum(2^(i-1), i in S)` with one-based coordinate labels. Exact zero entries are retained. Its compaction changes only JSON representation; `verify.py` emits the same mathematical records in labeled form. An independent verifier should reconstruct from the specified kernels, not trust the stored values.
