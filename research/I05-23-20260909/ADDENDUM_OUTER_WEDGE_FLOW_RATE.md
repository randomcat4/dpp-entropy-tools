# Addendum — outer-wedge curvature normal form, observed-flow obstruction, and a finite-Jensen rate bridge

Status: **PROVED / DISPROVED at the scoped statements below (author proof), not independently reviewed**.

This addendum continues issue #50 and PR #54. It does not alter the status of the universal dense-correlated whole legal chord, which remains **INCOMPLETE**. It uses only the main-reviewed rank-two likelihood identity

\[
q_s(S,T)=\frac{P_s(S,T)}{p_A(S)p_C(T)}=1-s\,a(S,T)+s^2b(S,T),\qquad s=t^2,
\]

with

\[
a=\operatorname{tr}(G_A G_C),\qquad b=\det G_A\,\det G_C,
\]

and the main-reviewed zero means of the first and second exterior features. The open PR43 nonreversible-flow and special `3+3` claims are not used as premises.

All expectations below are with respect to the complete product law \(\mu=p_A\otimes p_C\); no complete event, rare event, three-point event, or Fisher term is removed.

---

## A — exact outer-wedge curvature normal form

Define

\[
u_s=q_s-1=-sa+s^2b,\qquad y_s=s^2b,
\]

and, for \(u>-1\),

\[
\Phi(u)=\frac{4u^2}{1+u}+2u\log(1+u),
\]

\[
\psi(u)=\frac{8u}{1+u}+10\log(1+u).
\]

Let

\[
I(t)=D(P_{t^2}\|\mu)=H(A)+H(C)-H(K(t)).
\]

### Theorem A.1 (one signed outer-wedge scalar)

For every strict legal \(t\ne0\),

\[
\boxed{
 t^2 I''(t)
 =\mathbb E_\mu\!\left[
   \Phi(u_s)+\frac{4y_s^2}{1+u_s}+y_s\psi(u_s)
 \right].
} \tag{A.1}
\]

Moreover

\[
\Phi(u)\ge0,
\qquad
\psi'(u)=\frac8{(1+u)^2}+\frac{10}{1+u}>0,
\qquad \psi(0)=0. \tag{A.2}
\]

Hence \(\psi(u)\) has the sign of \(u\). The only term in (A.1) that is not pointwise nonnegative is

\[
W(s):=\mathbb E_\mu[b\,\psi(u_s)]. \tag{A.3}
\]

Consequently, if \(W(s)\ge0\) throughout a legal \(s\)-interval, then the true affine-kernel radial path is entropy-concave on the corresponding \(t\)-interval.

### Proof

Since \(\mathbb E_\mu q_s=1\), differentiation of the full relative entropy gives

\[
I''(t)=\mathbb E_\mu\left[
 \frac{(\partial_tq_s)^2}{q_s}+(\partial_t^2q_s)\log q_s
\right]. \tag{A.4}
\]

With \(s=t^2\), \(u=u_s\), \(y=y_s\),

\[
\partial_tq_s=\frac2t(u+y),
\qquad
\partial_t^2q_s=\frac1{t^2}(2u+10y). \tag{A.5}
\]

Substitution in (A.4), multiplication by \(t^2\), and expansion give (A.1). The first term of \(\Phi\) is nonnegative, and \(u\log(1+u)\ge0\) for \(u>-1\). Formula (A.2) follows by direct differentiation. At \(t=0\), \(I''(0)=0\) by the even quartic onset, so interior continuity supplies the center point. ∎

### Corollary A.2 (eventwise mixed-discriminant sufficient condition)

At a fixed \(s\), if

\[
b(S,T)u_s(S,T)\ge0\qquad\text{for every complete }(S,T), \tag{A.6}
\]

then \(W(s)\ge0\). A stronger \(s\)-independent condition is

\[
a(S,T)b(S,T)\le0\qquad\text{for every complete }(S,T). \tag{A.7}
\]

Indeed, \(bu_s=s[-ab+sb^2]\ge0\), and \(\psi(u)\) has the sign of \(u\). This is only a sufficient condition, not a conjectured universal sign law.

---

## B — determinant-sign four-ring decomposition

Write

\[
\alpha(S)=\det G_A(S),\qquad \beta(T)=\det G_C(T),
\qquad b(S,T)=\alpha(S)\beta(T).
\]

The reviewed exterior-moment cancellations give

\[
\mathbb E_{p_A}\alpha=0,\qquad \mathbb E_{p_C}\beta=0. \tag{B.1}
\]

Assume neither feature is identically zero. Let

\[
m_A=\mathbb E\alpha_+=\mathbb E\alpha_->0,
\qquad
m_C=\mathbb E\beta_+=\mathbb E\beta_->0,
\]

and define four probability tilts

\[
\nu_A^\pm(S)=\frac{p_A(S)\alpha_\pm(S)}{m_A},
\qquad
\nu_C^\pm(T)=\frac{p_C(T)\beta_\pm(T)}{m_C}. \tag{B.2}
\]

### Theorem B.1 (exact four-ring identity)

For every function \(f(S,T)\),

\[
\boxed{
\mathbb E_\mu[b f]
=m_Am_C\bigl(
 \mathbb E_{++}f-\mathbb E_{+-}f
 -\mathbb E_{-+}f+\mathbb E_{--}f
\bigr),
} \tag{B.3}
\]

where the four expectations use the corresponding product tilts from (B.2). In particular, taking \(f=\psi(u_s)\) rewrites the sole signed curvature scalar \(W(s)\) as a four-ring contrast.

Because \(\psi\) is increasing, the finite stochastic-order conditions

\[
\mathcal L_{++}(u_s)\succeq_{\rm st}\mathcal L_{+-}(u_s),
\qquad
\mathcal L_{--}(u_s)\succeq_{\rm st}\mathcal L_{-+}(u_s) \tag{B.4}
\]

are sufficient for \(W(s)\ge0\). On the finite configuration space, (B.4) is equivalent to finitely many cumulative-distribution inequalities, so it is an exact checkable interface.

### Proof

Expand \(\alpha=\alpha_+-\alpha_-\) and \(\beta=\beta_+-\beta_-\), use (B.1) to normalize all four positive parts by the same \(m_A,m_C\), and collect the four product expectations. Monotonicity of \(\psi\) gives (B.4). ∎

This determinant-sign four-ring is different from the Boolean elementary-imset face decomposition in `RESULT.md`: it is available in arbitrary block dimension but supplies a stochastic-order certificate rather than a universal face-cone representation.

---

## C — a stronger obstruction to universal observed-state exterior scaling

Section 4 of `RESULT.md` formulates the directed stationary-flow system

\[
L^\dagger G_{11}=-G_{11},\quad
L^\dagger G_{12}=-G_{12},\quad
L^\dagger G_{22}=-G_{22},\quad
L^\dagger d=-2d,\qquad d=\det G. \tag{C.1}
\]

The next statement shows that nonreversibility alone does not rescue this visible-state mechanism in the smallest correlated block.

### Theorem C.1 (linear collision)

Let \(T\) be **any linear operator** on functions on a finite configuration space. If

\[
d\in\operatorname{span}\{G_{11},G_{12},G_{22}\}\setminus\{0\}, \tag{C.2}
\]

then there is no \(0<\theta<1\) such that

\[
TG_{ij}=\theta G_{ij}\quad(i,j\in\{1,2\}),
\qquad Td=\theta^2d. \tag{C.3}
\]

Likewise no linear generator can satisfy the degree-one eigenvalue \(-1\) and the degree-two eigenvalue \(-2\) on the same functions.

### Proof

If \(d=c_{11}G_{11}+c_{12}G_{12}+c_{22}G_{22}\), linearity forces \(Td=\theta d\), contradicting \(Td=\theta^2d\) because \(0<\theta<1\) and \(d\ne0\). The generator statement is identical. ∎

### Corollary C.2 (every strict correlated two-point block, invertible feature frame)

Let

\[
C=\begin{pmatrix}c_{11}&c\\c&c_{22}\end{pmatrix},
\qquad c\ne0,
\]

be a strict two-point DPP kernel and let \(V\in GL_2(\mathbb R)\). For a complete event \(T\), set

\[
Y_T=C-E_{T^c},\qquad G_T=V^TY_T^{-1}V,\qquad d_T=\det G_T.
\]

Then pointwise in \(T\),

\[
\boxed{
 d_T=\frac1c\,e_1^TV\operatorname{adj}(G_T)V^Te_2.
} \tag{C.4}
\]

Since the adjugate of a symmetric `2 x 2` matrix is linear in its three entries, (C.2) holds. Explicitly, for \(V=((v_{ij}))\),

\[
d=\frac1c\bigl[
 v_{12}v_{22}G_{11}
 -(v_{11}v_{22}+v_{12}v_{21})G_{12}
 +v_{11}v_{21}G_{22}
\bigr]. \tag{C.5}
\]

Thus **no visible-state linear operator at all** — reversible or nonreversible, positive or not — can realize the degree-one/degree-two scaling on this scope.

### Proof

From \(G=V^TY^{-1}V\),

\[
Y=VG^{-1}V^T=\frac{V\operatorname{adj}(G)V^T}{\det G}.
\]

The off-diagonal entry of every \(Y_T\) is the same nonzero number \(c\), which yields (C.4); expanding the `2 x 2` adjugate gives (C.5). ∎

This strictly strengthens the open-PR reversible inner-product obstruction in this two-point scope. It does **not** contradict the reviewed `m x 2` radial entropy theorem; it only rules out this particular visible linear semigroup mechanism.

### Exact one-line Farkas witness for the standard correlated fixture

For

\[
C=\begin{pmatrix}1/2&1/10\\1/10&1/2\end{pmatrix},\qquad V=I_2,
\]

all four complete states satisfy

\[
d=-10G_{12}. \tag{C.6}
\]

In the directed-flow equations of `RESULT.md`, take only the multiplier of the \(G_{12}\) equation at state `11` to be \(10\), and the multiplier of the \(d\) equation at the same state to be \(1\); all balance and other feature multipliers are zero. Every nonnegative flow variable receives coefficient zero by (C.6), while the combined right-hand side is exactly

\[
-\frac6{25}\,10\left(-\frac5{12}\right)
-2\frac6{25}\frac{25}{6}=1-2=-1<0. \tag{C.7}
\]

This is a rational Farkas infeasibility certificate; no LP solve is needed.

A hidden-state dilation is not ruled out by Theorem C.1 because visible functions need not be closed under a fixed visible linear semigroup. It still must satisfy the separate projection-loss/entropy-curvature obligation already identified in `RESULT.md`.

---

## D — finite Jensen bridge from a subextensive bad outer-wedge budget

The previous rate section asks for pointwise finite concavity or a uniform third-derivative estimate. The outer-wedge normal form yields a different, strictly weaker transfer criterion that never interchanges differentiation with the volume limit.

Consider finite rank-two radial families indexed by \(n\), with volume \(N_n\), complete entropies \(H_n(t)\), and a common strict legal interval \([-T,T]\). Define \(W_n(s)\) by (A.3).

### Theorem D.1 (subextensive negative wedge implies concave rate)

Assume there are \(\rho_n\ge0\) such that

\[
W_n(s)\ge-\rho_n\qquad(0\le s\le T^2). \tag{D.1}
\]

Then for every \(x,y\in[-T,T]\), \(0\le\lambda\le1\), and \(z=\lambda x+(1-\lambda)y\),

\[
\boxed{
\lambda H_n(x)+(1-\lambda)H_n(y)-H_n(z)
\le
\frac{T^2\rho_n}{2}\lambda(1-\lambda)(x-y)^2.
} \tag{D.2}
\]

If the pointwise entropy-rate limit

\[
h(t)=\lim_{n\to\infty}\frac{H_n(t)}{N_n} \tag{D.3}
\]

exists and

\[
\rho_n/N_n\to0, \tag{D.4}
\]

then \(h\) is concave on \([-T,T]\).

### Proof

By (A.1), the two omitted terms are nonnegative, so

\[
t^2 I_n''(t)\ge t^4W_n(t^2)\ge-t^4\rho_n.
\]

Hence

\[
H_n''(t)=-I_n''(t)\le t^2\rho_n\le T^2\rho_n. \tag{D.5}
\]

Therefore

\[
F_n(t)=H_n(t)-\frac{T^2\rho_n}{2}t^2
\]

is concave. Jensen's inequality for \(F_n\) is exactly (D.2). Divide by \(N_n\) and pass to the pointwise limits at the three fixed parameters; (D.4) kills the defect and gives the entropy-rate Jensen inequality. ∎

This criterion keeps all finite events and the full Fisher term. It is not a finite-sample proof: the genuinely extensive requirement is the uniform whole-interval bound (D.1) with sublinear negative part (D.4).

For scalar Toeplitz DPP windows the cross-cut rank generally grows with the window, so this rank-two theorem does not by itself produce a new scalar entropy-rate theorem. It is a precise finite-to-rate bridge for any family where a rank-two outer-wedge representation and the subextensive bound can be proved.

---

## Status and route comparison

| statement | status |
| --- | --- |
| outer-wedge normal form (A.1) and the sole signed scalar \(W(s)\) | **PROVED (author proof), not independently reviewed** |
| determinant-sign four-ring identity (B.3) and stochastic-order sufficient condition | **PROVED (author proof), not independently reviewed** |
| universal visible-state degree-one/degree-two scaling in the correlated two-point scope | **DISPROVED (author proof), not independently reviewed** |
| subextensive negative-\(W_n\) finite-Jensen transfer to entropy-rate concavity | **PROVED (author proof), not independently reviewed** |
| universal sign \(W(s)\ge0\) for dense correlated rank-two blocks | **INCOMPLETE** |
| hidden-state dilation with a descending second-order entropy bound | **INCOMPLETE** |
| whole legal chord for the general dense two-sided correlated rank-two family, or a strict counterexample | **INCOMPLETE** |

Mechanism comparison: the visible nonreversible-flow route has an exact linear obstruction already in the correlated two-point scope, while a hidden dilation still faces the second-order projection-loss obligation. The outer-wedge route does not assume a channel and reduces the full curvature question to the scalar \(W(s)\), with the four-ring and rate interfaces above. It is therefore the preferred continuation route.

## Source boundary

The DPP and entropy-rate background remains the primary literature already listed in `RESULT.md` (Lyons; Borcea--Brändén--Liggett; Lyons--Steif). The finite Markov entropy-dissipation comparison uses the same Erbar--Maas Bochner/entropy-curvature literature cited there. Those sources motivate the mechanism comparison; none supplies (A.1), (B.3), (C.4), or (D.2), which are proved directly above.
