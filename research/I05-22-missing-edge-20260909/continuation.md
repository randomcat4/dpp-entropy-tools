# Post-checkpoint continuation: general missing-edge Schur reduction

Author status: the identities, positive two-dimensional block, and two method obstructions below are **PROVED (author proof), not independently reviewed**. The remaining four-dimensional inequality and radial monotonicity conjecture are **INCOMPLETE**. This work was performed after opening PR51; the heavy elimination request is issue52. No result from that request is assumed.

## 1. An exact product-domain parameterization

For a connected missing-edge center

\[
K=\begin{pmatrix}x&0&b\\0&y&c\\b&c&z\end{pmatrix},\quad bc\ne0,
\]

write

\[
v=x(1-x),\quad w=y(1-y),\quad A=b^2/v,\quad B=c^2/w,\quad q=z-A(1-x)-B(1-y).
\]

The exact domain \(0<K<I\) is equivalent to

\[
0<x,y<1,\quad A,B>0,\quad q>0,\quad q+A+B<1. \tag{19}
\]

Indeed the Schur complement of diag(x,y) in K is q; that of diag(1-x,1-y) in I-K is 1-q-A-B. The signs of b,c may be restored by diagonal sign conjugation. The leaf marginal is \(P_{ij}=\operatorname{Bern}_x(i)\operatorname{Bern}_y(j)\), and its four conditional probabilities are

\[
t_{ij}=q+A(1-i)+B(1-j). \tag{20}
\]

This is a full parameterization, not a finite box or a weak-coupling approximation. For an arbitrary physical symmetric direction, let d=D11,e=D22, and write its conditional derivative as

\[
T_{ij}=m+f(i-x)+g(j-y)+h(i-x)(j-y). \tag{21}
\]

Here m is the product expectation, f,g are the averaged single contrasts, and h is the double contrast. The inverse direction map is

\[
\begin{aligned}
D_{33}&=m-Ad-Be,\\
D_{13}&=\frac b2\left(\frac{1-2x}{v}d-\frac fA\right),\quad
D_{23}=\frac c2\left(\frac{1-2y}{w}e-\frac gB\right),\\
D_{12}&=\frac{bc}{2AB}h.
\end{aligned} \tag{22}
\]

It follows directly from the eight-event quotient derivative in PR41, independently checked in `verify_exact.py`. All six direction coordinates are free; h is not discarded.

## 2. The logs and the rectangle coefficient

Put \(\psi(t)=\log(t/(1-t))\), \(f_0(t)=t\log t+(1-t)\log(1-t)\), and define

\[
\ell_j=\psi(t_{0j})-\psi(t_{1j})>0,\quad k_i=\psi(t_{i0})-\psi(t_{i1})>0,
\]

\[
v_0=\log\frac{(1-t_{10})(1-t_{01})}{(1-t_{00})(1-t_{11})},\quad
v_1=\log\frac{t_{10}t_{01}}{t_{00}t_{11}},\quad \Lambda=v_0-v_1.
\]

Here v0,v1 are log weights, not the variance v. Both are positive on (19), and \(\ell_0-\ell_1=k_0-k_1=\Lambda\). Set \(\ell=(1-y)\ell_0+y\ell_1\), \(k=(1-x)k_0+xk_1\), \(n=v_0-\Lambda z\), and

\[
\begin{aligned}
J&=f_0(t_{00})+f_0(t_{11})-f_0(t_{10})-f_0(t_{01})\\
&=\int_0^A\int_0^B\frac{d\alpha\,d\beta}{(q+\alpha+\beta)(1-q-\alpha-\beta)}\\
&=A k_0+B\ell_0+q\Lambda-v_0>0. \tag{23}
\end{aligned}
\]

The second equality is the fundamental theorem of calculus; the last follows by collecting the eight scalar logarithms.

## 3. Complete six-direction matrix, with a proved two-dimensional block

Let \(u=(m,f,g,h)^T\), \(a_{ij}=(1,i-x,j-y,(i-x)(j-y))^T\), and

\[
F_c=\sum_{i,j}\frac{P_{ij}}{t_{ij}(1-t_{ij})}a_{ij}a_{ij}^T. \tag{24}
\]

This is the complete conditional Fisher, representing both outcomes of the third bit. The full Fisher is \(d^2/v+e^2/w+u^TF_cu\). Define

\[
L=\begin{pmatrix}A\ell/(2v)&J\\J&Bk/(2w)\end{pmatrix}, \tag{25}
\]

\[
C=\begin{pmatrix}
-\ell&(2x-1)\ell/2&w\Lambda&-w\Lambda(2x-1)/2\\
-k&v\Lambda&(2y-1)k/2&-v\Lambda(2y-1)/2
\end{pmatrix}, \tag{26}
\]

\[
R=\begin{pmatrix}
0&0&0&0\\
0&v\ell/(2A)&0&-vw\Lambda/(2A)\\
0&0&wk/(2B)&-vw\Lambda/(2B)\\
0&-vw\Lambda/(2A)&-vw\Lambda/(2B)&vw n/(2AB)
\end{pmatrix}. \tag{27}
\]

The exact full negative entropy Hessian is

\[
\mathcal B_K(D)=\binom de^T\left[L+\operatorname{diag}(1/v,1/w)\right]\binom de
+2\binom de^TCu+u^T(F_c+R)u. \tag{28}
\]

In (28), binom(d,e) denotes the two-component column vector. To verify the formula, start from the eight-event cofactor identity (3) in the main proof. Its log part at this arrow center is

\[
-2k_0\det D_{23}-2\ell_0\det D_{13}-2v_0\det D_{12}
+2\Lambda\operatorname{tr}(K\operatorname{adj}D).
\]

Substitute (22), b²=Av,c²=Bw and z=q+A(1-x)+B(1-y), and collect terms. The result is exactly the quadratic form with blocks L,C,R. `verify_general.py` checks the identity by symbolic rational arithmetic, importing no other author's verifier.

**Lemma.** L itself is positive definite on the full domain (19); no marginal Fisher is needed for this claim.

**Proof.** The function \(f_0''(t)=1/t+1/(1-t)\) is strictly convex: its second derivative is \(2/t^3+2/(1-t)^3>0\). Applying the convex trapezoid inequality on each integration segment in (23) gives

\[
J<\tfrac B2(\ell_0+\ell_1),\qquad J<\tfrac A2(k_0+k_1).
\]

Moreover

\[
\ell-w(\ell_0+\ell_1)=(1-y)^2\ell_0+y^2\ell_1>0,
\]

and \(k-v(k_0+k_1)=(1-x)^2k_0+x^2k_1>0\). Consequently

\[
J^2<\frac{AB}{4}(\ell_0+\ell_1)(k_0+k_1)
<\frac{AB\ell k}{4vw}=L_{11}L_{22}.
\]

Both diagonal entries are positive, proving the lemma.

The exact remaining full-domain obligation is therefore the explicit four-by-four inequality

\[
S_{\mathrm{full}}:=F_c+R-C^T\left[L+\operatorname{diag}(1/v,1/w)\right]^{-1}C\succeq0. \tag{29}
\]

The stronger conditional-entropy candidate is

\[
S_{\mathrm{cond}}:=F_c+R-C^TL^{-1}C\succeq0. \tag{30}
\]

Completing squares proves that (29) is equivalent to the desired arrow-center Hessian inequality. Equation (30) would imply it because the inverse decreases after adding the positive marginal block. Neither (29) nor (30) has been proved here. The gain is a globally proved eliminable positive block and a fully specified remaining matrix, not an assertion that a smaller matrix is automatically positive.

## 4. The exact mixed term preventing naive two-point iteration

For j=0,1 set

\[
Q_{1j}=\frac{A\ell_j}{2v}d^2-\ell_jd(T_{0j}+T_{1j})+\frac{v\ell_j}{2A}(T_{1j}-T_{0j})^2,
\]

and for i=0,1 set

\[
Q_{2i}=\frac{Bk_i}{2w}e^2-k_ie(T_{i0}+T_{i1})+\frac{wk_i}{2B}(T_{i1}-T_{i0})^2.
\]

Expansion gives the exact acceleration identity

\[
\sum_Sp''_S\log p_S=
\sum_j\operatorname{Bern}_y(j)Q_{1j}+\sum_i\operatorname{Bern}_x(i)Q_{2i}
+2Jde-\frac{vwJ}{2AB}h^2. \tag{31}
\]

For example, the leaf-1 squared contrasts contribute the f² and fh entries in (27) and the h² coefficient \(vw[(1-y)\ell_1+y\ell_0]/(2A)\). Adding the analogous leaf-2 coefficient and comparing with (27) leaves exactly \(-vwJ/(2AB)\). The d-e cross term is 2Jde. This proves (31), and the separate symbolic check also passes.

One cannot simply add two-point conditional-entropy proofs along these faces: that would spend the same Fisher twice and omit the last two terms in (31). The precise coupling left to control is explicit.

## 5. Lambda=0 subfamily and the handed-off rational matrix

Equation (20) gives

\[
v_1=\log\left(1+\frac{AB}{q(q+A+B)}\right),\quad
v_0=\log\left(1+\frac{AB}{(1-q-A-B)(1-q)}\right).
\]

Thus Lambda=0 if and only if q=(1-A-B)/2. Parameterize this entire subfamily by

\[
\mu=2x-1,\quad\nu=2y-1,\quad a=(1+r)/2,\quad b_*=(1-r)/2,\quad A=u^2a,\quad B=u^2b_*,
\]

where \(|\mu|,|\nu|,|r|<1\) and \(0<u<1\). Then

\[
K(u)=\begin{pmatrix}
x&0&u\sqrt{av}\\0&y&u\sqrt{b_*w}\\
u\sqrt{av}&u\sqrt{b_*w}&1/2-u^2(a\mu+b_*\nu)/2
\end{pmatrix}. \tag{32}
\]

Use direction coordinates \(\zeta=(\alpha,\beta,\gamma,\eta,\xi,\omega)\) fixed as u varies:

\[
D_{11}=v\alpha,\quad D_{22}=w\beta,\quad D_{33}=\gamma,\quad
D_{12}=\sqrt{ab_*vw}\eta,\quad D_{13}=\sqrt{av}\xi,\quad D_{23}=\sqrt{b_*w}\omega. \tag{33}
\]

Let \(J_u=1-u^4,L_u=1-r^2u^4\), and define

\[
\begin{aligned}
P_{ij}&=[1+(2i-1)\mu][1+(2j-1)\nu]/4,\\
e_i&=i-x,\quad f_j=j-y,\\
q_{ij}&=(u^2ae_i^2,u^2b_*f_j^2,1,2u^2ab_*e_if_j,-2uae_i,-2ub_*f_j)^T,\\
d_{ij}&=J_u\ (i=j),\quad d_{ij}=L_u\ (i\ne j),\\
F(u)&=\sum_{i,j}4P_{ij}q_{ij}q_{ij}^T/d_{ij}.
\end{aligned} \tag{34}
\]

This is the full conditional Fisher; the marginal Fisher is the constant diag(v,w,0,0,0,0). Define

\[
n_1=4u(1/J_u-r/L_u),\quad n_2=4u(1/J_u+r/L_u),\quad n_3=4u^3(1-r^2)/(J_uL_u).
\]

Let Q be symmetric, with only the following nonzero entries (indices 1–6):

\[
Q_{12}=-n_3vw,\ Q_{13}=-n_2v,\ Q_{23}=-n_1w,\quad
Q_{44}=2n_3ab_*vw,\ Q_{55}=2n_2av,\ Q_{66}=2n_1b_*w.
\]

The exact radial derivative of the full negative Hessian, in the fixed coordinates (33), is

\[
M(\mu,\nu,r,u)=F'(u)+Q. \tag{35}
\]

Indeed Lambda stays zero, the diagonal cofactor matrix is the same log matrix as (5) in the main proof, and n1,n2,n3 are its u derivatives. This derives (35) without dropping any entropy term.

The conjecture M>0 on this whole four-parameter domain would imply the full entropy Hessian there by integration from diag(v,w,4,0,0,0) at u=0. It is **not proved**. Its potentially heavy exact determinant/positivity computation was handed off in [issue52](https://github.com/randomcat4/dpp-entropy-tools/issues/52), with explicit rational input, independent reconstruction, proposed commands, resource ceiling, stopping rules and certificate gate. The issue is a request, not a claim that a worker is running.

A bounded 1500-point double-precision scout (seed 22051) found no negative eigenvalue; that is not a certificate. The exact symbolic matrix construction completed locally, but an r=0 determinant expansion hit the 35-second process ceiling. No determinant or global sign was obtained. No unbounded job remained running. The analytic work in sections 1–4 and 6 continued without a response to that request.

## 6. Two precise obstructions encountered after choosing the route

### 6.1 Conditional resolvent convexity is too strong

For a general nearby physical kernel define

\[
\Phi(K)=\sum_{i,j}P_{ij}(K)^2/p_{ij1}(K)=\sum_{i,j}P_{ij}(K)/t_{ij}(K).
\]

This is a conditional perspective resolvent, not the full-atom shifted resolvent rejected earlier. The possible shortcut Phi''>=0 is false even at a strict arrow center. An exact example is

\[
K_* =\begin{pmatrix}23/25&0&1/5\\0&2/5&8/25\\1/5&8/25&3/10\end{pmatrix},\quad
D_* =\begin{pmatrix}0&-1&-4/5\\-1&1/3&1/20\\-4/5&1/20&-2/15\end{pmatrix}.
\]

On the true affine line, exact rational differentiation gives

\[
\Phi''(K_*;D_*)=-\frac{53670727895896612562246875}{14117659525214393686902}<-3800. \tag{36}
\]

For each marginal P and full atom R=p_(ij1), the formula is

\[
(P^2/R)''=2(P'-PR'/R)^2/R+2PP''/R-P^2R''/R^2.
\]

No rare event is removed. In this specific direction the rare event's conditional first derivative T11 is exactly zero, while its other terms remain in the sums. All eight atoms and derivatives are used.

Crucially the actual entropy has the opposite sign needed for a counterexample:

```
-H''(K_*;D_*) in
[85.39754587008524590529296252441265816,
 85.39754587008524590529296252441265817].
```

All three exact kernels K_* +/- D_*/10000 and K_* pass strict Sylvester checks for themselves and complements. The entire segment |t|<=1/10000 is therefore legal by convexity. Its complete entropy Jensen difference is

```
[-0.00000042702288120241526682286996218,
 -0.00000042702288120241526682286996217].
```

This is an auxiliary-method counterexample, **not a DPP entropy counterexample or a candidate positive gap**. The exact script uses the same rational log enclosures as (18) in the main proof.

### 6.2 Coefficientwise positive power-series matrices also fail

In the already proved half-filled equal-strength family put

\[
K_s=\begin{pmatrix}1/2&0&\sqrt{s/8}\\0&1/2&\sqrt{s/8}\\\sqrt{s/8}&\sqrt{s/8}&1/2\end{pmatrix},\quad
D_s=\begin{pmatrix}1/4&-1/4&0\\-1/4&1/4&0\\0&0&s/6\end{pmatrix}.
\]

For each fixed s in (0,1), D_s is a legitimate fixed direction for taking H'' at K_s. Substitution into the full Fisher plus acceleration yields

\[
\mathcal B_{K_s}(D_s)=\frac12+\frac89s^2+\frac{s^2}{18(1-s^2)}-\frac s6\log\frac{1+s}{1-s}
=\frac12+\frac{11}{18}s^2-\frac1{18}s^4+O(s^6). \tag{37}
\]

Thus requiring every coefficient matrix after this natural rescaling to be positive semidefinite is false: the s^4 coefficient has the exact negative value -1/18 on the displayed rescaled vector. The full sum is strictly positive by the main theorem; the negative coefficient is not positive entropy curvature. Since the testing direction varies with the center parameter s, (37) does not refute the fixed-coordinate derivative conjecture (35).

## 7. Final boundary of this author task

The unequal-strength half-filled full-six-direction theorem in `proof_half_filled.md` remains the completed center-family result. This continuation adds a global positive eliminable block, full remaining Schur complement, exact face coupling, Lambda=0 rational derivative input, and two rigorous failures of stronger routes.

The full arbitrary-diagonal missing-edge inequality (29) remains unproved. No strict positive entropy Jensen candidate was found or fabricated. The compute request is not counted as a mathematical result. All new results remain author-level and unreviewed; novelty is separate and unresolved.
