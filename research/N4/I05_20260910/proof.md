# I05: moving rank-two endpoints and multiple affine boundary faces

Status: **PROVED (author proofs, PENDING_REVIEW)** for the numbered analytic statements below. The unrestricted rank-two midpoint inequality and unrestricted real-kernel conjecture remain **INCOMPLETE**. This is a successor to agent24 / PR62 and issue #83, not a revision of their accepted scope. Main base: `65e59a46b49cd2dbb5c779a4cfae8cef26441984`.

Throughout, `0 <= K <= I` means a real symmetric positive contraction in the original observation coordinates. The complete atom law is

\[
p_K(S)=\sum_{T\supseteq S}(-1)^{|T|-|S|}\det K_T,
\quad \det K_\varnothing=1,
\quad H(K)=-\sum_Sp_K(S)\log p_K(S).
\]

Natural logarithms and `0 log 0=0` are used. Write `G=H(K0)-(H(K-)+H(K+))/2` and `Delta=-G`. A counterexample requires `Delta>0`, not merely failure of an intermediate entropy comparison.

## 1. All mixed areas and all midpoint atoms

Let `A=XX^T`, `B=YY^T`, with `X=[x1,x2]`, `Y=[y1,y2]` real n-by-2 matrices, and assume `A,B <= I`. The genuine affine line is

\[
K(t)=(1-t)A+tB,\qquad 0\le t\le1.
\]

Put `F=[x1,x2,y1,y2]`. For a coordinate set T and integers a,b in `{0,1,2}` with `a+b=|T|`, let

\[
W_{ab}(T)=\sum_{\substack{J\subseteq\{1,2,3,4\}\\
|J\cap\{1,2\}|=a,\ |J\cap\{3,4\}|=b}}
\det(F_{T,J})^2.
\]

Empty determinants equal one. Weighted Cauchy--Binet gives the exact identity

\[
\det K(t)_T=\sum_{a+b=|T|}(1-t)^a t^b W_{ab}(T). \tag{1}
\]

All W are nonnegative, but this is an inclusion-minor identity, not an entropy identity. For pairs define

\[
a_{ij}=x_{1i}x_{2j}-x_{1j}x_{2i},\quad
b_{ij}=y_{1i}y_{2j}-y_{1j}y_{2i},
\]
\[
C_{ij}=\sum_{r,s=1}^2(x_{ri}y_{sj}-x_{rj}y_{si})^2.
\]

Then

\[
\det K(t)_{ij}=(1-t)^2a_{ij}^2+t^2b_{ij}^2+t(1-t)C_{ij}. \tag{2}
\]

For triples, (1) is `(1-t)^2 t W21 + (1-t)t^2 W12`; for quadruples it is `(1-t)^2 t^2 det(F_T)^2`; larger minors vanish. Thus the new triple and quadruple terms are real and cannot be dropped by applying a rank-one theorem twice.

The pair mixed discriminant satisfies

\[
C_{ij}^2\ge4a_{ij}^2b_{ij}^2. \tag{3}
\]

To check (3), for positive definite 2-by-2 restrictions put `Z=A_ij^(-1/2) B_ij A_ij^(-1/2)`. The mixed coefficient is `det(A_ij) tr Z`, and `(tr Z)^2 >= 4 det Z`; singular restrictions follow by continuity. This does **not** imply `C_ij >= a_ij^2+b_ij^2`.

At the true midpoint let `d_T=det K(1/2)_T`. Explicitly `d_T=2^(-|T|) sum_{|J|=|T|} det(F_TJ)^2`. For every S of size at most four,

\[
p_{K(1/2)}(S)=\sum_{\substack{T\supseteq S\\|T|\le4}}(-1)^{|T|-|S|}d_T, \tag{4}
\]

and all larger atoms are zero. In particular, pairs subtract every containing triple and add every containing quadruple; singletons and the empty event contain the corresponding alternating sums as well. Formula (4), including the empty event, is the full event law in n=4,5,6 and in arbitrary n.

Let `q=(p_A+p_B)/2`. Its pair inclusion correction is

\[
\det K(1/2)_{ij}-{\det A_{ij}+\det B_{ij}\over2}
={C_{ij}-a_{ij}^2-b_{ij}^2\over4}
=-{1\over4}\det(B-A)_{ij}. \tag{5}
\]

The sign in (5) can vary with the coordinate pair, even for two dense moving rank-two endpoints and a rank-four midpoint. Nonnegative mixed discriminants therefore do not supply the entropy-increasing mass-transfer bridge of PR62. The separate fixed-input certificate tests this stronger bridge and labels its failure as a **method counterexample only**.

## 2. Three-coordinate indefinite directions: the exact lemma being used

This is the accepted PR43-E input, reproduced here to make the next theorem checkable. Let C be a strict real three-point kernel and D a real symmetric rank-two matrix with nonzero eigenvalues of opposite signs. For an affine parameter z every complete atom has the form `p_z=p+z r+z^2 c`.

Choose a unit null vector n of D. Then `adj(D)=gamma n n^T`, where `gamma<0`, and put `kappa=n^T C n in (0,1)`. For `{i,j,k}={1,2,3}` set `delta_ij=det D_ij=gamma n_k^2 <=0`. Let `e^{ij|k=epsilon}` put `(1,-1,-1,1)` on the four configurations with coordinate k fixed to epsilon. The complete coefficient law is

\[
c=\sum_{i<j}\delta_{ij}\big[(1-\kappa)e^{ij|k=0}+\kappa e^{ij|k=1}\big]. \tag{6}
\]

Indeed, both sides have zero total and singleton inclusion moments, pair moments `delta_ij`, and triple moment `tr(adj(D)C)=gamma kappa`. Boolean Mobius inversion proves equality, not just agreement after summing a selected layer.

Each conditional two-coordinate DPP has nonpositive covariance. Its positive complete 2-by-2 table therefore satisfies `p00 p11 <= p10 p01`. Pairing (6) with `log p_z` consequently gives `<c,log p_z> >=0`. The full Hessian is

\[
H''(z)=-\sum_S{(r(S)+2z c(S))^2\over p_z(S)}-2\sum_Sc(S)\log p_z(S)\le0. \tag{7}
\]

The scalar kappa is constant along the line because `Dn=0`. This proves concavity throughout the strict legal interval. For boundary kernels apply the argument to `epsilon I+(1-2epsilon)C(z)` and let epsilon decrease to zero. No observation-basis rotation occurs. A direction of rank at most one has affine atoms by determinant multilinearity and is handled directly by Shannon concavity.

Source binding: main `docs/verification_round3_20260909/accepted_pr43.md`, and `research/I05-W1-20260909-R2/proof/04_three_point_indefinite_rank2.md`, read against the above base. This is not counted as a new independent theorem or review.

## 3. A rank-two moving-support exclusion with a common dense mode

**Theorem 1.** Partition the actual coordinate set as `J disjoint E`, with `|J|=3`. Let `u` be real, let `v,w` be nonzero independent real vectors supported in J, and let `c,a,b>0`. Suppose

\[
A=c uu^T+a vv^T<I,\qquad B=c uu^T+b ww^T<I,
\qquad r=c\|u_E\|^2>0. \tag{8}
\]

Then the endpoints have rank two, their ranges intersect exactly in `span(u)` and genuinely move, and their true arithmetic midpoint has rank three. Moreover

\[
G(A,B)\ge r\,G(a v_Jv_J^T,b w_Jw_J^T)>0. \tag{9}
\]

No orthogonality between u and v or w is assumed. In particular, the common-mode cross areas need not vanish. The ambient n is arbitrary (in particular n=4,5,6), but the moving directions must be supported on three **actual** coordinates. This is a separate restricted proposition, not an unrestricted rank-two result.

### Exact conditional laws, including every cross term

For any `L` supported on J and with `K=c uu^T+L` legal, write

\[
C_L={c\over1-r}u_Ju_J^T+L_J.
\]

The full outside law is independent of L:

\[
P(X_E=\varnothing)=1-r,\quad P(X_E=\{j\})=c u_j^2,
\quad P(|X_E|\ge2)=0. \tag{10}
\]

Here `0<r<1` follows from (8). Conditioning on no outside points uses the Schur complement

\[
K_J+K_{JE}(I-K_E)^{-1}K_{EJ}
=L_J+{c\over1-r}u_Ju_J^T=C_L. \tag{11}
\]

Conditioning on an outside point j with `u_j!=0` subtracts
`K_{rest,j} K_{j,rest}/K_jj` and cancels the entire common rank-one term. The remaining outside coordinates have zero rows and the J kernel is exactly L_J. Hence for **every** T,

\[
p_K(T)=\begin{cases}
(1-r)p_{C_L}(T\cap J),&T\cap E=\varnothing,\\
c u_j^2p_{L_J}(T\cap J),&T\cap E=\{j\},\\
0,&|T\cap E|\ge2.
\end{cases} \tag{12}
\]

The entropy chain rule now gives the exact identity

\[
H(K)=H(X_E)+(1-r)H(C_L)+rH(L_J). \tag{13}
\]

Thus nothing is being treated as two independent rank-one DPPs. The first conditional branch retains the full common-mode interactions, and (12) also retains midpoint triple events.

For the endpoint choices `L-=a vv^T`, `L+=b ww^T`, the C branch is a true affine three-coordinate line with direction `b ww^T-a vv^T`. Independence of v,w gives

\[
e_2(D)=-ab(\|v\|^2\|w\|^2-(v^Tw)^2)<0,
\]

so Section 2 proves that branch has nonnegative G. The occupied-outside branch is precisely the rank-one endpoint problem of PR62. Its strict midpoint inequality gives (9).

### Why the rank-one input is strict

For completeness, write the rank-at-most-two midpoint of the two rank-one J kernels as `alpha xx^T+beta yy^T`, with x,y orthonormal, `alpha+beta<1`, and `m=alpha beta>0`. Set `b_ij=(x_i y_j-x_j y_i)^2` and `c_i=x_i^2+y_i^2`. The mixture q and the midpoint law are joined by the valid laws

\[
p_s(\varnothing)=1-\alpha-\beta+s,\quad
p_s(i)=(\alpha-s)x_i^2+(\beta-s)y_i^2,\quad
p_s(ij)=s b_{ij},\quad 0\le s\le m.
\]

All other atoms are zero. Cauchy--Binet gives `sum b_ij=1` and `sum_{j!=i} b_ij=c_i`. The full entropy derivative is

\[
{dH(p_s)\over ds}=\sum_{i<j}b_{ij}\log{p_s(i)p_s(j)\over p_s(\varnothing)s b_{ij}}.
\]

Lagrange's identity and
`(alpha-s)(beta-s)-s(1-alpha-beta+s)=m-s>0` make each active logarithm strictly positive for `0<s<m`. Shannon concavity for q completes the proof. This is PR62's accepted proof mechanism, not a claim of priority here.

## 4. Multiple-boundary theorem for a fixed genuine affine line

**Theorem 2 (linear-emergence asymptotic).** Let `K(h)=K_b+hD` be a fixed real affine line of legal kernels for all sufficiently small `h>=0`. Define the complete atoms as above and discard only atoms that are identically zero on a neighborhood. Then

\[
\beta=\sum_{S:p_{K_b}(S)=0}\left.{d\over dh}p_{K(h)}(S)\right|_{h=0}\ge0,
\]
\[
H''(h)=-{\beta\over h}+O(1+|\log h|),\qquad h\downarrow0. \tag{14}
\]

In particular, beta>0 implies `H''(h)->-infinity`. No simple eigenvalue or simple determinant-root assumption is made.

**Proof.** Every atom is a polynomial of degree at most n. A nonzero polynomial atom either has a positive value at zero or has an expansion `p(h)=a h^m(1+O(h))`, with integer `m>=1` and `a>0`. By taking a sufficiently small common interval, all such atoms are positive there. At a simple zero,
`(p')^2/p=a/h+O(1)`. At a zero of order m>=2 this term is `O(h^(m-2))`, hence bounded. At a positive boundary atom it is bounded as well. The sum of the simple-zero coefficients a is exactly beta.

For each nonzero polynomial atom, `p''` is bounded and `log p=O(1+|log h|)`. The complete acceleration sum is therefore `O(1+|log h|)`. Substitution in

\[
H''=-\sum_S(p'_S)^2/p_S-\sum_Sp''_S\log p_S
\]

proves (14). This argument explicitly keeps the complete Fisher term and all higher-order rare atoms.

### A basis-invariant count calculation forces beta>0

Let `r0=rank K_b<n`, let `P0` be the orthogonal projector onto `ker K_b`, and let `pdet(K_b)` mean the product of its positive eigenvalues (empty product one). Then

\[
\left.{d\over dh}P_{K(h)}(|X|=r0+1)\right|_{h=0}
=\operatorname{pdet}(K_b)\operatorname{tr}(P0D)=:c_0. \tag{15}
\]

To verify (15), use only the **count generating polynomial**

\[
E[z^{|X|}]=\det(I+(z-1)K(h)).
\]

Diagonalize K_b for this determinant computation, not for configuration entropy. In the determinant derivative at h=0, a diagonal D entry on a zero mode contributes
`(z-1)D_jj product_{lambda_i>0}(1-lambda_i+z lambda_i)`.
Terms from nonzero modes have degree at most r0. The coefficient of `z^(r0+1)` is consequently (15). This also proves the formula without choosing analytic eigenvalue branches.

Since the entire layer `|X|=r0+1` has zero probability at h=0 and all its atom derivatives are nonnegative, beta is at least c0. Applied to `I-K(h)`, the same argument gives

\[
c_1=\operatorname{pdet}(I-K_b)\operatorname{tr}(P1(-D)), \tag{16}
\]

when `P1` projects onto `ker(I-K_b)` and that kernel is nonzero. The two cardinality layers used in (15) and (16) are disjoint, so when both are present `beta>=c0+c1`.

**Corollary 2a.** If `0<K_b+hD<I` for all sufficiently small h>0 and K_b is a boundary kernel, then beta>0, irrespective of the multiplicities at zero and one. Indeed, on a nonzero `x in ker K_b`, strict positivity gives `h x^T D x>0`, so the compression of D to that nullspace is positive definite. The complementary assertion holds on `ker(I-K_b)`. At least one of c0,c1 is strictly positive.

**Corollary 2b.** Let A,B be legal rank-two kernels with distinct ranges and put `K(h)=(1-h)A+hB`. At A, `tr(P_ker(A)(B-A))=tr(P_ker(A)B)>0`, so beta>0 by (15), even when the ambient midpoint is not strictly positive definite. The same holds at B. Thus every fixed moving-rank-two chord has strictly negative curvature sufficiently near its endpoints. The entropy in the compact middle is still undecided.

These are fixed-line, finite-dimensional statements. The neighborhood size and beta need not be uniform as endpoints, frame angles, or degeneracy scales vary. They do not settle fast-moving families with simultaneous parameter limits, nor Jensen's inequality for the full chord. They strengthen the available simple-endpoint exclusion, not the global conjecture.

## 5. Common bit-flip lifts preserve a proved strict sign

For any three legal kernels on a true chord, use the same

\[
K^{(\epsilon)}=\epsilon I+(1-2\epsilon)K,\quad0<\epsilon<1/2.
\]

The midpoint is preserved and the spectrum lies in `[epsilon,1-epsilon]`. This map is exactly independent flipping of every occupation bit: substituting the two diagonal bit-generating factors into `det(I-K+ZK)` yields
`det(A_epsilon(I-K)+B_epsilon K)=det(I-K^epsilon+ZK^epsilon)`.

Put `delta=1-(1-epsilon)^n`. Coupling before and after flips gives total variation at most delta. With `d=2^n` and `delta<=1-1/d`, the finite-alphabet continuity inequality gives

\[
|H(p^\epsilon)-H(p)|\le\omega_n(\epsilon)
=h_2(\delta)+\delta\log(2^n-1). \tag{17}
\]

Thus `G_epsilon>=G-2 omega_n`; any certified positive lower bound on G supplies an explicit sufficiently small lift. For the method comparison `H(q)-H(p_mid)`, q also goes through the same bit-flip channel by linearity, so exactly the same two-omega error applies. This does not identify that comparison with the true Jensen gap.

For a self-contained proof of the classical bound, take a maximal coupling of two laws with mismatch probability T. The indicator of mismatch has entropy h2(T), and given a mismatch there are at most d-1 possible alternatives. Hence `H(X|Y),H(Y|X)<=h2(T)+T log(d-1)`, which bounds the entropy difference. The right-hand side is increasing for `T<=1-1/d`, allowing T to be replaced by delta. Audenaert's primary paper independently supplies this sharp bound; it is used only for classical complete-event distributions, never as a replacement by von Neumann entropy.

## Checkpoint and remaining work

This file is an analytic checkpoint. Fixed-input rational-log certificates, the new strong-correlated double-endpoint fixture, and its failed conditional-anchor test are to be recorded separately in this same work unit. No independent reviewer or machine queue has been assumed running. The universal moving rank-two midpoint problem, the strong-correlated fixture's full compact middle, and novelty remain INCOMPLETE.
