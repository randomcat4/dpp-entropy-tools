# Continuation after the first I05 checkpoint

Status: **PROVED (author proof; PENDING_REVIEW)** for Theorem 3 and the exact endpoint analysis below. The multiple-ring compact-middle inequality is **INCOMPLETE**. This file continues the work after uploading `proof.md`; it is not merely a packaging update. All notation, entropy conventions and `Delta=-G` are as in that file.

## 1. The three-coordinate input lifts through arbitrary correlated outside coordinates

**Theorem 3.** Let A,B be any legal real n-point kernels. Suppose `D=B-A` is supported on `J x J` for a set J of three actual observation coordinates, and that `D_J` has rank two with its two nonzero eigenvalues of opposite signs. Then the complete-configuration entropy on the entire true chord `K(z)=A+zD`, `0<=z<=1`, is strictly concave. Neither the outside block nor the cross block need be diagonal, weakly coupled, or rank one.

For `G=H(K(1/2))-[H(A)+H(B)]/2`, the following explicit bounds hold:

\[
G\ge {1\over2}\max_i D_{ii}^2. \tag{18}
\]

If every diagonal entry of D is zero, then, for each nonzero off-diagonal entry `d=D_ij`, writing `c=A_ij`,

\[
G\ge 2d^2(c+d/2)^2+{d^4\over12}>0. \tag{19}
\]

These claims include legal boundary endpoints. This is a coordinate-supported class, NOT a theorem about an arbitrary spectral rank-two direction after a basis rotation. It is a derived consequence of the accepted three-coordinate lemma reproduced in `proof.md`, not a novelty claim.

### Proof of the conditional affine bridge

First suppose the whole chord is strict. Put `E=J^c`. Its full outside atom law `q(T)=p_{K_E}(T)` is independent of z and strictly positive. For every complete `T subset E`, set

\[
Y_T=K_E-E_{E\setminus T}.
\]

Here the second term is the diagonal indicator matrix on the absent outside coordinates. The signed event determinant shows Y_T is invertible because q(T)>0. Schur factorization of each **complete** event gives

\[
p_{K(z)}(S\cup T)=q(T)\,p_{C_T(z)}(S),\qquad S\subseteq J,
\]
\[
C_T(z)=K_J(z)-K_{JE}Y_T^{-1}K_{EJ}. \tag{20}
\]

There is no z-dependence in Y_T or either cross block. Consequently `C_T'(z)=D_J` exactly. Successive inclusion/exclusion conditioning of a strict contraction gives a strict real conditional contraction; equivalently apply the ordinary positive Schur complements for each included or excluded bit. Thus the three-coordinate lemma applies to every T, without altering observation coordinates.

The chain rule and the fixed q weights give

\[
H(K(z))=H(q)+\sum_Tq(T)H(C_T(z)),
\]
\[
H''(K(z))\le-\sum_Tq(T)\sum_S{(p'_{C_T(z)}(S))^2\over p_{C_T(z)}(S)}
=-\sum_X{(p'_{K(z)}(X))^2\over p_{K(z)}(X)}. \tag{21}
\]

The equality is the complete Fisher identity for a fixed outside marginal. This is why arbitrary correlations outside J cause no lost acceleration or mixed-direction terms here. Merely saying that conditioning preserves DPPs would not suffice without the affine identity in (20).

### Strictness and quantitative bounds

For any fixed indicator statistic f of a complete configuration, Cauchy--Schwarz with the centered statistic yields

\[
\sum_X{p'_X{}^2\over p_X}
\ge {\big(dE[f]/dz\big)^2\over\operatorname{Var}(f)}
\ge4\big(dE[f]/dz\big)^2. \tag{22}
\]

For f equal to the occupancy of coordinate i, `dE[f]/dz=D_ii`, so `H''<=-4 max_i D_ii^2`. The midpoint gap for a twice differentiable function equals the integral of minus its second derivative with weight

\[
w(z)=\tfrac12\min(z,1-z),\quad
\int_0^1w(z)dz=1/8,
\]

which proves (18).

When the diagonal of D is zero, choose `f=1_{i,j both occupied}` for a pair with d nonzero. Its inclusion probability is the exact two-point minor, so

\[
{dE[f]\over dz}=-2d(c+zd),\qquad
H''\le-16d^2(c+zd)^2.
\]

Using `integral w(z)(z-1/2) dz=0` and `integral w(z)(z-1/2)^2 dz=1/192` gives (19). Thus the Fisher part alone supplies a strictly positive midpoint margin; the conditional acceleration parts have the already proved favorable sign. Applying this argument on every subinterval proves strict concavity, not just one midpoint inequality.

For arbitrary legal boundary endpoints, apply the proof to the common bit-flip regularization `A_e=epsilon I+(1-2epsilon)A`, and similarly to B. The direction becomes `(1-2epsilon)D`, still supported on J and indefinite of rank two. In (18) the bound gains the factor `(1-2epsilon)^2`. In (19), both off-diagonal c and d scale by `(1-2epsilon)`, so the entire bound gains `(1-2epsilon)^4`. Let epsilon decrease to zero and use finite-event entropy continuity. This proves the boundary assertions without assuming differentiability of entropy at a zero atom.

### Consequence for the common-mode rank-two theorem

For `A=c uu^T+a vv^T`, `B=c uu^T+b ww^T` in Theorem 1 of `proof.md`, the direction is supported on J and indefinite. Hence **every** common lift `0<epsilon<1/2` of this particular class remains strictly concave. This stronger lift statement follows from Theorem 3, not from asserting that a small-epsilon continuity estimate works at arbitrary epsilon. It does not enlarge the accepted PR62 lift statement for unrelated families.

For the exact six-point example

\[
u=(1,2,3,4,5,6)^T,\quad v=(1,-1,1,0,0,0)^T,
\quad w=(1,2,-1,0,0,0)^T,
\]
\[
c=1/200,\qquad a=1/12,\qquad b=1/20,
\]

we have

\[
\operatorname{diag}(B-A)=(-1/30,7/60,-1/30,0,0,0).
\]

Therefore the entire open lift range has the explicit bound

\[
G_\epsilon\ge {49\over7200}(1-2\epsilon)^2>0. \tag{23}
\]

At epsilon zero the finer conditional decomposition gives `G>= (77/200)G_rank1`, and the direct rational-log certificate gives

\[
0.031373360749276697060039678872067269
\le G\le
0.031373360749276697060039678872067270.
\]

The endpoints have rank two, their ranges intersect in span(u), and the true midpoint has rank three. Cross terms have been checked atom by atom, rather than omitted by entropy additivity.

## 2. An independent strong-correlated, multiple-isotropic-endpoint construction

Set

\[
n=(1,2,2)^T/3,\quad P=I_3-nn^T,
\]
\[
A={1\over5}I_3+{3\over5}nn^T,
\qquad C=I_3-A,
\qquad B={2\over5}P,
\]
\[
K(t)=\begin{pmatrix}A&tB\\tB&C\end{pmatrix},\qquad
D=\begin{pmatrix}0&B\\B&0\end{pmatrix}. \tag{24}
\]

All entries are rational. The two internal triangles have opposite products of off-diagonal signs. Both blocks are correlated, B is dense of rank two and is not supported on two actual columns or rows. The parameter is genuinely K-affine.

For legality ONLY, decompose into span(n) and its two-dimensional orthogonal complement. The eigenvalues are `1/5,4/5` and two copies each of

\[
\lambda_\pm(t)={1\over2}\pm\sqrt{{9\over100}+{4t^2\over25}}.
\]

Consequently the full legal interval is `[-1,1]`, strict inside. At each endpoint there are simultaneously two zero and two unit eigenvalues. The determinant has multiple roots there; the accepted simple-endpoint hypothesis does not cover this geometry. No entropy is computed in that eigenbasis.

### Exact failure of the accepted conditional sufficient test

Consider the complete left event `S={2}` (one-based labels). Its conditional direction matrix is

\[
M_S=B(A-\operatorname{diag}(1,0,1))^{-1}B
=\begin{pmatrix}
-532/3105&88/3105&178/3105\\
88/3105&-44/621&176/3105\\
178/3105&176/3105&-53/621
\end{pmatrix}.
\]

Its rank is two, trace is `-113/345`, and second elementary symmetric coefficient is `44/1725>0`. Hence it is negative semidefinite of rank two, not indefinite. In addition, the three off-diagonal ratios `C_ij/(M_S)_ij` are

\[
-207/44,\qquad -207/89,\qquad -207/44.
\]

They are inconsistent, so there is no scalar sigma making `C-sigma M_S` diagonal. This one actual complete event fails both indefinite-direction and diagonal-anchor alternatives of accepted PR43-G. The special PR43-H sufficient family also does not apply. This is a failure of that sufficient test, NOT a conclusion that the entropy has positive curvature.

### All 64 atoms and the exact multiple-endpoint coefficient

Use the rational factorization `B=UV^T`, where

\[
V=\begin{pmatrix}2&2\\-1&0\\0&-1\end{pmatrix},
\qquad U={2\over5}V(V^TV)^{-1}.
\]

For every complete pair of left/right configurations S,T, define

\[
\mu_{ST}=p_A(S)p_C(T),\quad
G_A(S)=U^T(A-E_{S^c})^{-1}U,\quad
G_C(T)=V^T(C-E_{T^c})^{-1}V.
\]

The full signed six-point event determinant factors exactly as

\[
p_{ST}(t)=\mu_{ST}\bigl[1-t^2\operatorname{tr}(G_A(S)G_C(T))
+t^4\det G_A(S)\det G_C(T)\bigr]. \tag{25}
\]

The code constructs every coefficient as a rational, checks normalization and its first two derivatives identically, and checks all 64 atoms against independent signed determinants and Mobius inversion at `t=0,1/2,3/4,9/10,1`.

At `t=1`, twenty atoms vanish. With `h=1-t`, their exact orders and total linear masses are:

| Cardinality | Order in h | Number | Sum of coefficients of h |
|---|---:|---:|---:|
| 0 | 2 | 1 | 0 |
| 1 | 1 | 6 | 64/625 |
| 2 | 1 | 3 | 1664/16875 |
| 4 | 1 | 3 | 1664/16875 |
| 5 | 1 | 6 | 64/625 |
| 6 | 2 | 1 | 0 |

For a direct algebraic check of the extra linear atoms, one has

\[
p_{\{1,4\}}(t)=p_{\{2,3,5,6\}}(t)
={32(1-t^2)(387-62t^2)\over1265625},
\]

and the other four atoms on sets `{2,5}`, `{3,6}`, `{1,2,4,5}`, `{1,3,4,6}` equal

\[
{16(1-t^2)(176t^2+1449)\over1265625}.
\]

The remaining 44 atoms are positive at t=1. Summing every linear zero, not only impossible-cardinality layers, gives

\[
\beta={6784\over16875},\qquad
\lim_{t\uparrow1}(1-t)H''(t)=-{6784\over16875}<0. \tag{26}
\]

The count-layer lower bound from Theorem 2 is only `128/625`; the additional cardinality-two and cardinality-four zero atoms account for the difference. This explicitly shows why a calculation using only the count distribution would miss part of the complete Fisher singularity. Evenness gives the analogous endpoint limit at -1.

### What finite certified probes say

Every logarithm below is enclosed by exact dyadic arithmetic with an explicit tail; no decimal logarithm decides a sign. All 64 atoms and the entire Fisher sum are used. The exact certificate contains narrower outward intervals than this display.

| t | Certified enclosure for H''(t) | Certified enclosure for true Delta on t +/- 1/100 |
|---|---|---|
| 1/2 | [-1.342673241463,-1.342673241462] | [-0.000067139132,-0.000067139131] |
| 3/4 | [-3.384684311428,-3.384684311427] | [-0.000169271836,-0.000169271835] |
| 9/10 | [-7.745687117608,-7.745687117607] | [-0.000387724251,-0.000387724250] |

These are finitely many exact sign certificates, not a continuous covering argument. Theorem 2 closes a sufficiently small neighborhood of each multiple endpoint, but no explicit overlap with a compact-middle covering has yet been proved. That computation is a separate REQUESTED task; neither it nor old issue #61 is assumed running.

## 3. Remaining quantifiers

Theorem 3 closes all true chords whose indefinite rank-two difference is supported on three actual coordinates, even with arbitrary correlated outside kernels. General moving rank-two endpoints can have a rank-four difference spread over all n coordinates and do not satisfy this condition. The method counterexample in `fixtures.md` has precisely a rank-four midpoint and is not covered by this coordinate condition.

Theorem 2 excludes the very end of each fixed moving-support rank-two chord and each fixed strict-interior affine line approaching a multiple boundary. It supplies no uniform neighborhood when angles, eigenvalues or degeneracy scales change, no quantitative compact-middle covering, and no global Jensen conclusion. The new multiring construction remains unresolved between the finitely certified points. None of these results settles the unrestricted real-kernel conjecture or establishes novelty.
