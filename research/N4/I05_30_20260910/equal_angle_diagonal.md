# The full equal-angle diagonal is midpoint-safe

Status: **PROVED (author proof with a fresh exact interval certificate), PENDING_EXTERNAL_REVIEW**. This result was obtained after the edge and thinning checkpoints. It concerns the fixed canonical matrices below, not arbitrary rank-two endpoints, and no novelty or priority claim is made.

Let
\[
 A=\begin{pmatrix}2/5&6/25\\6/25&2/5\end{pmatrix},\qquad
 B=\begin{pmatrix}3/5&9/25\\9/25&3/5\end{pmatrix}.
\]
For `0<=t<=1`, put
\[
 c={1-t^2\over1+t^2},\qquad s={2t\over1+t^2},\qquad x=c^2,
\]
\[
 E=(e_1,e_2),\qquad V=(ce_1+se_3,ce_2+se_4),
\]
\[
 K_-=EAE^\top,\qquad K_+=VBV^\top,\qquad M={K_-+K_+\over2}.
\]
This is the true arithmetic midpoint for each fixed endpoint pair. The parameterized family of endpoint pairs is used only to prove a family of midpoint inequalities; it is not called a `K`-affine entropy path.

For `0<t<=1`, the endpoint ranges have zero intersection and `rank M=4`; for `0<t<1` the endpoint kernels do not commute. At `t=1` the coordinate supports are orthogonal. At `t=0` the ranges coincide and `rank M=2`.

Define
\[
G(x)=H(M)-{H(K_-)+H(K_+)\over2}.
\]
Every entropy is the Shannon entropy of the complete event law.

## 1. All sixteen midpoint atoms

A fresh signed-determinant expansion, independently cross-checked by Möbius inversion at rational physical points, gives
\[
\begin{array}{c|l}
S&p_M(S)\\ \hline
\varnothing&2(3x-253)(96x-221)/390625\\
1,2&-(10152x^2-213429x-62348)/781250\\
12&4(81x+44)(99x+26)/390625\\
3,4&3(1-x)(39491-2616x)/781250\\
13,24&3(1-x)(11009-384x)/781250\\
23,14&3(1-x)(14616x+11009)/781250\\
123,124&12(1-x)(423x+202)/390625\\
34&14076(1-x)^2/390625\\
134,234&3924(1-x)^2/390625\\
1234&576(1-x)^2/390625.
\end{array} \tag{1}
\]
In the row `1,2`, the same expression is used for the two singleton events. Likewise every comma-separated pair of set labels denotes equal probabilities, not a union event. All displayed regular factors are strictly positive on `[0,1]`. Thus every singleton, pair, triple and the quadruple event opened by the rank-four midpoint is retained.

## 2. Exact removal of the endpoint singularity

For a configuration `S`, let
\[
m(S)=|S\cap\{3,4\}|,
\qquad p_M(S)=(1-x)^{m(S)}q_S(x). \tag{2}
\]
By (1), every `q_S` is a positive polynomial on `[0,1]`. The expected number of occupied bottom coordinates is exactly
\[
\sum_S m(S)p_M(S)={3\over5}(1-x),
\]
so
\[
\sum_Sm(S)p'_M(S)=-{3\over5}. \tag{3}
\]

The plus endpoint is obtained from its two logical coordinates by independently marking each occupied logical coordinate into its top or bottom physical copy. Since both diagonal inclusion probabilities of `B` are `3/5`,
\[
H(K_+)=H(B)+{6\over5}h(1-x)=H(B)+{6\over5}h(x). \tag{4}
\]
Consequently the marking term in the averaged endpoint entropy is `(3/5)h(x)`.

Differentiate the complete midpoint entropy. Normalization removes the `+1` terms. Substituting (2)--(4), the entire coefficient of `log(1-x)` cancels exactly, leaving
\[
\boxed{
G'(x)=-\sum_{S\subseteq[4]}p'_M(S)\log q_S(x)
       +{3\over5}\log x.} \tag{5}
\]
This formula retains all sixteen event derivatives. At `x=0`, the final term tends to minus infinity; no numerical probability floor is introduced. At `x=1`, every `q_S(1)>0`, so (5) has a finite one-sided limit despite the vanishing rare events.

## 3. Uniform negative derivative certificate

**Theorem.** For every `0<x<=1`,
\[
G'(x)<0.
\]
Therefore
\[
G(x)\ge G(1)>
0.071729711441392005498563>0. \tag{6}
\]
Equivalently, every endpoint pair on the complete equal-angle line `t1=t2=t`, `0<=t<=1`, satisfies the strict true midpoint inequality unless the endpoints coincide.

**Certificate.** Partition `[0,1]` into the 256 rational boxes
`[j/256,(j+1)/256]`. Each `p'_M(S)` is affine and each `q_S` has degree at most two, so its exact box range is obtained from rational endpoints and, where present, its rational vertex. For every positive rational log endpoint use
\[
\log y=k\log2+
2\sum_{r=0}^{31}{z^{2r+1}\over2r+1}+R,
\qquad
0\le R\le{2z^{65}\over65(1-z^2)},\quad0\le z\le1/3. \tag{7}
\]
All additions and sign-dependent products are rational interval operations. On the first box only the valid upper bound
`log x<=log(1/256)` is needed; the lower endpoint is allowed to be minus infinity.

Every resulting upper bound for (5) is strictly negative. The least negative box is number 246 (zero based), and even there
\[
G'([246/256,247/256])
<-0.689450994698557990947319. \tag{8}
\]
The complete list of 256 outward bounds and every atom/regular factor are stored in `diagonal_extension_certificate.json`; `extend_diagonal.py` regenerates them without importing the earlier author scripts.

The anchor `x=1` is the fixed-support midpoint law with probabilities
\[
(4/25,17/50,17/50,4/25).
\]
The two endpoint four-event laws are
\[
(189,186,186,64)/625,\qquad(19,231,231,144)/625.
\]
The same rational-log method gives
\[
G(1)\in
[0.071729711441392005498563,
 0.071729711441392005498564]. \tag{9}
\]
Together with (8), this proves (6).

## 4. Scope and comparison

This line passes through the interior of the two-angle square, rather than lying on a support-degeneracy edge. Except at its fixed-support endpoint it gives zero-intersection rank-two endpoints; except at its two endpoints, the kernels are noncommuting. The true midpoint has rank four and its triple/quadruple atoms are used in (5).

The mechanism is distinct from:

- the four-event sign transfer, which changes one inclusion minor while holding the rest fixed;
- the small-angle marginal/continuity proof;
- the full-edge Bernstein proof in `fresh_recheck_and_edge_extension.md`;
- the general small-intensity expansion; and
- the independent-thinning theorem for disjoint actual coordinate blocks.

It does not close any off-diagonal interior pair `(t1,t2)` with `t1!=t2`, does not generalize the fixed `A,B`, and does not establish concavity along the nonlinear frame curve. The unrestricted moving-rank-two problem remains INCOMPLETE.
