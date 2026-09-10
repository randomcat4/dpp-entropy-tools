# Parity mutual information and local corrected concavity

Status: **AUTHOR PROOF / PENDING REVIEW**.

This file turns the `C^4` entropy-rate result into the corrected local concavity theorem. The proof keeps separate the possible quadratic and quartic cases; it does not assume in advance that the quadratic response vanishes.

## 1. Complete-event parity conjugacy

Let

\[
D_{jj}=(-1)^j.
\]

Half-period Fourier support gives

\[
T(c-tg)=D\,T(c+tg)D.
\tag{1.1}
\]

For every finite complete event with zero-set diagonal `I_Z`, one has `DI_ZD=I_Z`. Therefore

\[
\det(T_I(c-tg)-I_Z)
=\det(T_I(c+tg)-I_Z).
\tag{1.2}
\]

Every complete-event probability, every finite entropy, and the entropy rate are even functions of `t`.

## 2. Fixed parity marginals and independence at the center

Write

\[
E=2\mathbb Z,
\qquad O=2\mathbb Z+1.
\]

If two coordinates have the same parity, their difference is even. Since `g` has only odd Fourier modes,

\[
T_E(c+tg)=T_E(c),
\qquad
T_O(c+tg)=T_O(c).
\tag{2.1}
\]

Restriction of a DPP to a coordinate subset is the DPP with the compressed kernel. Hence the complete laws of the even and odd coordinate processes are independent of `t`.

At `t=0`, `c` has only even Fourier modes, so all cross-parity kernel entries vanish. The kernel is block diagonal with respect to `E direct_sum O`; therefore the two parity DPPs are independent at the center.

Fix a finite interval `Lambda_n={1,...,n}` and write its parity parts as `E_n,O_n`. Let `P_{n,t}` be the full complete-event law, and let `P_{E_n},P_{O_n}` be its fixed parity marginals. Then

\[
P_{n,0}=P_{E_n}\otimes P_{O_n}.
\tag{2.2}
\]

Consequently

\[
\begin{aligned}
D(P_{n,t}\|P_{n,0})
&=D(P_{n,t}\|P_{E_n}\otimes P_{O_n})\\
&=H(P_{E_n})+H(P_{O_n})-H(P_{n,t})\\
&=H(P_{n,0})-H(P_{n,t}).
\end{aligned}
\tag{2.3}
\]

Divide by `n` and let `n` tend to infinity. The entropy-rate limits exist, so

\[
\boxed{
J(t):=h(c)-h(c+t g)
=d(P_t\|P_0)
=I_t(E;O)\ge0.}
\tag{2.4}
\]

Thus `t=0` is a true entropy-rate maximum along this path. Equation (2.4) is an identity between complete configuration laws, not between inclusion probabilities.

## 3. Accepted matching floor

For every odd `k` with `\widehat g(k)\ne0`, the regularity-free parity matching/negative-association inequality accepted with PR53 gives, for every sufficiently small legal real `t`,

\[
J(t)
\ge\frac12\,d_{\rm Ber}
\left(
\mu^2-|\widehat g(k)|^2t^2
\,\middle\|\,
\mu^2
\right).
\tag{3.1}
\]

Its expansion at zero is

\[
\frac12\,d_{\rm Ber}(q-a t^2\|q)
=\frac{a^2}{4q(1-q)}t^4+O(t^6).
\tag{3.2}
\]

With

\[
q=\mu^2,
\qquad a=|\widehat g(k)|^2,
\]

put

\[
C_k
=\frac{|\widehat g(k)|^4}
{4\mu^2(1-\mu^2)},
\qquad
\alpha_k=C_k/2.
\tag{3.3}
\]

Then

\[
J(t)\ge C_k t^4+O(t^6).
\tag{3.4}
\]

No response regularity is imported from PR53; only this already accepted finite/matching inequality is used.

## 4. Two exhaustive curvature cases

The complete-event loop theorem gives `J in C^4` on a neighborhood of zero. It is even, nonnegative, and satisfies `J(0)=0`. Hence

\[
J'(0)=0,
\qquad
J''(0)\ge0.
\tag{4.1}
\]

Define

\[
F(t)=h(c+t g)+\alpha_k t^4
=h(c)-J(t)+\alpha_k t^4.
\tag{4.2}
\]

### Case 1: `J''(0)>0`

Then

\[
F''(0)=-J''(0)<0.
\]

Continuity of `F''` gives an `epsilon>0` such that

\[
F''(t)<0
\qquad(|t|\le\epsilon).
\tag{4.3}
\]

### Case 2: `J''(0)=0`

Even `C^4` Taylor expansion gives

\[
J(t)=A t^4+o(t^4),
\qquad
A=J^{(4)}(0)/24.
\tag{4.4}
\]

Comparing (4.4) with the lower bound (3.4) yields

\[
A\ge C_k=2\alpha_k.
\tag{4.5}
\]

Differentiating the `C^4` expansion twice,

\[
J''(t)=12A t^2+o(t^2).
\tag{4.6}
\]

Therefore

\[
F''(t)
=-12(A-\alpha_k)t^2+o(t^2)
\le-12\alpha_k t^2+o(t^2)<0
\tag{4.7}
\]

for all sufficiently small nonzero `t`, while `F''(0)=0`.

The two cases exhaust all possibilities. Shrinking the interval to preserve legality gives

\[
\boxed{F''(t)\le0	ext{ on }[-\epsilon,\epsilon],}
\tag{4.8}
\]

with strict inequality away from zero. Thus `F` is concave on that interval.

## 5. Relation to the Fisher/acceleration identity

For every finite interval the exact Shannon curvature is

\[
H_n''(t)
=-\sum_x\frac{(p_{n,t}'(x))^2}{p_{n,t}(x)}
-\sum_xp_{n,t}''(x)\log p_{n,t}(x).
\tag{5.1}
\]

The first term is the complete Fisher contribution and the second is the full atom-acceleration term. The loop proof does not replace (5.1) by one of its summands: it starts from the exact complete atom factorization (2.5) of the companion file, sums over the full law, and proves convergence of the derivatives of the resulting exact KL. Hence (4.8) is a conclusion about the full classical entropy curvature, including both terms in (5.1).