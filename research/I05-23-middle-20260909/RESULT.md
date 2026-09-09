# I05-23 round 2 — compact middle curvature by full-law compensation

Issue: #50.  Branch base: `main@9dcb6e9079ca57f94e0e30d63161cda89ca61fae`.

Status of this packet:

- **PROVED (author complete proof), not independently reviewed**: a general rank-two compensation criterion that permits `W(s)<0`;
- **PROVED (author complete proof), not independently reviewed**: for the accepted dense correlated non-coordinate rational `3+3` fixture from PR54, `H''(t)<0` on the compact middle corridor `3 <= t^2 <= 15`;
- **DISPROVED**: the possible universal sign law `W(s)>=0` (only that sufficient sign law, not entropy concavity).  At `s=10`, the same fixture has a rigorously negative `W(10)` while the full curvature remains rigorously favorable;
- **INCOMPLETE**: the whole legal chord for general dense correlated rank-two blocks, and the whole legal chord even for this fixture.

All formulas use the complete configuration law. No rare event, three-point event, or Fisher contribution is removed. The path is always the true kernel-affine path

`K(t)=[[A,tB],[tB^T,C]]`.

The accepted PR54 local-center theorem, simple-endpoint theorem, global entropy-deficit theorem, outer-wedge normal form, and visible-state obstruction are inputs and are not claimed anew.

---

## 1. Frozen accepted input and the actual middle obstruction

For `rank(B)=2`, write `s=t^2` and use the accepted full-law likelihood

`q_s = P_s/(p_A tensor p_C) = 1 - s a + s^2 b`.

Set

`u=q_s-1`, `y=s^2 b`,

`Phi(u)=4u^2/(1+u)+2u log(1+u)`,

`psi(u)=8u/(1+u)+10 log(1+u)`.

The accepted PR54 identity is

` t^2 I''(t) = E[ Phi(u) + 4 y^2/(1+u) + y psi(u) ]`,      (1.1)

where `I(t)=D(P_{t^2} || p_A tensor p_C)=H(A)+H(C)-H(K(t))`.

`Phi>=0` and the quadratic `4y^2/q` term is nonnegative.  PR54 isolated

`W(s)=E[b psi(u_s)]`

as the only expected contribution whose sign was not already forced.  Since `E[y psi]=s^2 W`, `W>=0` is sufficient for concavity, but it was explicitly not proved necessary.

The present round attacks exactly the missing case `W<0`: can the two positive terms compensate it on a compact middle interval?

---

## 2. Route comparison before selection

### Route A — direct full-law outer-wedge compensation

The bridge is exactly (1.1).  It is finite, retains the full Fisher term, and does not ask for a channel.  The new observation is that the signed term should not be separated from `4y^2/q`.  Weighted Cauchy--Schwarz gives a quantitative compensation inequality with no sign assumption on `W`.

This route produces a finite rational certificate once one has rational bounds for `q`, `E[u^2]`, `E[b^2]`, and `psi` on a parameter interval.

### Route B — nonreversible / hidden-state entropy dissipation

The accepted PR47 three-point example proves only existence of one directed stationary generator with the required degree-one/degree-two exterior eigenrelations.  Along an exterior trajectory the true curvature still requires

`2 calI'' + calI' >= 0`, equivalently `D' <= -D/2`,                 (2.1)

where `D=-calI'` is entropy production.  This is a second-order entropy-decay / Bochner inequality, not mere data processing and not generator feasibility.

Primary literature confirms the distinction.  Caputo--Dai Pra--Posta, *Convex entropy decay via the Bochner--Bakry--Emery approach*, Ann. IHP Probab. Stat. 45 (2009), DOI `10.1214/08-AIHP183`, develops Bochner identities precisely to control convexity of entropy decay.  Erbar--Maas, *Ricci curvature of finite Markov chains via convexity of the entropy*, Arch. Rat. Mech. Anal. 206 (2012), DOI `10.1007/s00205-012-0554-z`, builds a discrete entropy-convexity framework for Markov chains.  These are structural templates for (2.1), not black-box proofs here: the present accepted fixed generator is nonreversible, and PR54 already proves that a universal visible-state exterior semigroup is impossible even linearly on correlated two-point blocks.

Therefore this round deepens Route A first.  Hidden-state dilation remains a distinct reserve mechanism, not a hidden assumption in the proof below.

---

## 3. General compensation theorem allowing `W<0`

Let

`q=1+u>0`,

`P = E Phi(u)`,

`A2 = 4 E[y^2/q]`,

`Rpsi = E[q psi(u)^2]`.

### Theorem 3.1 (full-law Cauchy compensation)

For every strict legal rank-two point,

` t^2 I''(t) >= P + A2 - (1/2) sqrt(A2 Rpsi)`.             (3.1)

Consequently a sufficient condition for strict entropy concavity at that point is

`P + A2 > (1/2) sqrt(A2 Rpsi)`.                              (3.2)

This is a different sufficient criterion that can hold with `E[y psi]<0`; no logical implication from `W>=0` to (3.2) is claimed.

#### Proof

From (1.1), only `E[y psi]` needs control.  Weighted Cauchy--Schwarz gives

`|E[y psi]| <= sqrt(E[y^2/q] E[q psi^2])`

`              = (1/2) sqrt(A2 Rpsi)`.

Substitute the lower sign into (1.1).  This proves (3.1)--(3.2).  No eventwise term is deleted. ∎

### Corollary 3.2 (rational interval envelope)

Fix an `s` interval `[L,R]`, `0<L<=R`.  Suppose throughout that

`0 < q_- <= q_s <= q_+`,

`|psi(u_s)| <= Psi`,

`E[u_s^2] >= M2 > 0`,

and put `B2=E[b^2]`.

Then

`P >= 4 M2/q_+`,

`A2 <= 4 R^4 B2/q_-`,

`Rpsi <= q_+ Psi^2`.

Hence

`t^2 I''(t) >= 4 M2/q_+ - R^2 Psi sqrt(B2 q_+/q_-)`.        (3.3)

In particular the whole interval is strictly entropy-concave if

`4 M2/q_+ > R^2 Psi sqrt(B2 q_+/q_-)`.                      (3.4)

For rational inputs, (3.4) is certified without floating point by checking positivity of both sides and then the rational inequality

`(4M2/q_+)^2 > R^4 Psi^2 B2 q_+/q_-`.                       (3.5)

#### Proof

`Phi(u)>=4u^2/q`, hence `P>=4E[u^2]/q_+`.  The other two displayed bounds are immediate from `q>=q_-`, `q<=q_+`, `|psi|<=Psi`, and `|y|=s^2|b|<=R^2|b|`.  Insert them into (3.1) and discard the positive `+A2` term after using its upper bound only inside the negative square-root term. ∎

This compensation bound controls a negative signed term using the retained full Fisher/quadratic contribution; its displayed sufficient inequality must still be verified.

---

## 4. A compact middle corridor for a dense correlated `3+3` fixture

Use the exact rational fixture already present in accepted PR54:

`A = [[1/2,1/20,1/30],[1/20,2/5,1/25],[1/30,1/25,3/5]]`,

`C = [[2/5,-1/30,1/40],[-1/30,1/2,1/35],[1/40,1/35,11/20]]`,

`U = [[1/100,1/100],[2/100,1/100],[3/100,1/100]]`,

`V = [[1,0],[1,1],[1,2]]`, `B=UV^T`.

Accepted PR54 already checked that both internal blocks are strict and correlated, `rank(B)=2`, every entry of `B` is nonzero, the left and right null planes are non-coordinate, and the unique left null vector is not an `A` eigenvector, excluding the special accepted PR43 correlated `3+3` family.

For all 64 complete pairs `(S,T)`, the verifier reconstructs exactly

`a(S,T)=tr(G_A(S)G_C(T))`,

`b(S,T)=det G_A(S) det G_C(T)`,

and the complete product weight `mu=p_A(S)p_C(T)`.

Define exact moments

`Amax=max |a|`, `Bmax=max |b|`,

`Ea2=E[a^2]`, `Eab=E[ab]`, `Eb2=E[b^2]`.

For each rational interval `[L,R]`, exact extrema of every quadratic

`q_s(S,T)=1-sa+s^2b`

are obtained by checking `L`, `R`, and the rational vertex `a/(2b)` when it lies in the interval.  Thus the bounds `q_-`, `q_+` are exact, not sampled.

For `q in [q_-,q_+]`, set

`u_max=max(1-q_-, q_+-1)`.

The elementary inequalities

`-log q <= (1-q)/q` for `0<q<=1`,

`log q <= q-1` for `q>=1`

give a rational bound

`|psi(q-1)| <= 8 u_max/q_- + 10 max((1-q_-)/q_-, q_+-1) =: Psi`.   (4.1)

Also

`E[u_s^2]=s^2(Ea2-2s Eab+s^2 Eb2)`.

For this fixture `Eab>0`; therefore on `[L,R]`

`E[u_s^2] >= L^2(Ea2-2R Eab)`,                              (4.2)

and the verifier checks the parenthesis is positive.

### Theorem 4.1 (certified middle corridor)

For this fixed dense correlated `3+3` rank-two family,

`H''(t)<0` whenever

`3 <= t^2 <= 15`.                                            (4.3)

Equivalently, strict curvature is certified on both compact middle bands

`sqrt(3) <= |t| <= sqrt(15)`.

#### Proof

Apply Corollary 3.2 on four overlapping rational `s` intervals:

`[3,9]`, `[8,12]`, `[11,14]`, `[14,15]`.

For every piece the verifier computes exact rational `q_-`, `q_+`, `Psi`, the moment lower bound (4.2), and the squared margin (3.5), and asserts the latter is strictly positive.  Since the four pieces cover `[3,15]`, (4.3) follows.

The positive `q_-` on every piece also proves strict legality directly: all 64 exact event masses `mu q_s` are positive.  By Möbius inversion their inclusion minors and complementary inclusion minors are positive, hence `0<K(t)<I`.  No spectral sampling is used. ∎

This is a new middle-interval statement, not a consequence of the accepted local-center theorem or the simple-endpoint asymptotic theorem.

---

## 5. The sufficient sign `W>=0` actually fails inside that corridor

At `s=10`, the same exact fixture has

`min q = 121400093597 / 249280204050 > 0`.

The verifier encloses every logarithm using

`log x = 2 sum_{k=0}^{N-1} z^(2k+1)/(2k+1) + R_N`,

`z=(x-1)/(x+1)`,

`|R_N| <= 2 |z|^(2N+1) / ((2N+1)(1-z^2))`,

with `N=80` and pure rational outward rounding.  Summing all 64 complete events gives

`W(10) = E[b psi(u_10)]`

inside an interval of width `< 5.83e-83` whose exact rational upper endpoint is negative and is printed approximately as

`-6.607689421828591727648293551781519992839111897380129530e-7 < 0`.   (5.1)

Thus the possible universal sign law `W(s)>=0` is **DISPROVED**.

This is not an entropy counterexample.  On the same point the complete normal-form quantity satisfies

`t^2 I''(t) > 0.17037745196806863130550498470533808479721333392335`,       (5.2)

with interval width `<8.71e-79`.  Therefore `H''(t)<0` there.  The negative `W` is more than compensated by the positive terms retained in (1.1).

This strict example is the reason the present route is materially different from merely proving another sufficient sign condition.

---

## 6. Code, inputs, arithmetic, and error standard

Reproduction:

```sh
python research/I05-23-middle-20260909/code/verify_middle_compensation.py
```

Saved output:

`research/I05-23-middle-20260909/output/verify_middle_compensation.txt`.

Author run: Python 3.13.5, SymPy 1.14.0.

The interval corridor itself uses exact rational arithmetic only.  The `W(10)` and direct curvature point check use the displayed atanh series with a rigorous rational remainder on every event logarithm.  No floating sign is promoted to a theorem.  The script enumerates all 64 complete events and checks all asserted inequalities by exact rational comparison before printing decimals.

No long LP, full-chord interval elimination, or heavy enumeration was run in this round.

---

## 7. Failed/delimited routes

1. **Universal `W>=0`.** Now strictly false by (5.1).  This only kills that sufficient sign law; it does not refute entropy concavity.
2. **Visible nonreversible exterior semigroup as a universal mechanism.** Already excluded in accepted PR54 on correlated two-point blocks by a linear feature collision.  It is not revived.
3. **Fixed three-point generator existence implies curvature.** False inference.  PR47 supplies feasibility only; the second-order entropy-production inequality (2.1) remains separate.
4. **Bochner/Ricci citation as a black box.** Not used.  The cited theories motivate the correct second-order quantity but do not automatically cover this nonreversible visible trajectory.
5. **Finite point certificates as whole interval proof.** Avoided.  The corridor theorem uses four exact interval envelopes, not samples.
6. **Global entropy deficit as curvature.** Not used.  The accepted matching deficit still only proves the decoupled point is a strict entropy maximizer.

---

## 8. Remaining gap and next exact object

The principal problem remains **INCOMPLETE**.

For the explicit fixture, this round certifies the substantial compact middle region `3<=s<=15`; accepted PR54 separately certifies a tiny neighborhood of `s=0` and an unspecified neighborhood of its simple endpoint (`s_*` is about 19.5, but no floating value is used here as a theorem).  The gaps between those certified regions are not silently closed.

For a general dense correlated rank-two pair, Corollary 3.2 is a new finite checkable sufficient structure, not a proof of the whole chord.  The next general analytic target is to control its four quantities

`q_-`, `q_+`, `E[u_s^2]`, `E[b^2]`

from block-level resolvent data without enumerating all configurations, or to obtain a sharper covariance estimate for `E[y psi]` that exploits the separate conditional cancellations `E_T a=E_T b=0` and `E_S a=E_S b=0`.

If a full legal interval certification for a chosen general family requires long exact interval subdivision/elimination, it should be handed to C2 with frozen matrices, target intervals, rational/log enclosure scheme, and a stop rule rather than run as an unbounded web computation.

No novelty or publication-priority claim is made.  This author proof requires independent review before integration.
