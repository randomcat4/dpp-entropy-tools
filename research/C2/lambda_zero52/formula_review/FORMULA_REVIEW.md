# Formula review for issue52 Lambda=0 radial derivative

STATUS: CORRECT for the event-to-M identity audited here.

This review is scoped to the literal issue52 matrix contract and PR51 continuation section 5 as frozen for C2. It does not audit the general PR51 half-filled theorem, the general continuation Schur-complement lemma, novelty, or the global positivity of M.

## Source binding and role boundary

Audited sources:

- The frozen [issue52](https://github.com/randomcat4/dpp-entropy-tools/issues/52) body, preserved in `../inputs/frozen_issue52.md`.
- PR51 `research/I05-22-missing-edge-20260909/continuation.md`, commit `2e4b8754ad4af2fe055ebeeef1159877773372a3`, section 5.
- The C2 claim in issue52, comment `5600800028`.
- `../frozen_contract.md`.

No candidate implementation was imported or executed. No Python, SymPy, CAS, or numerical arithmetic job was launched by this formula-review unit.

## Conventions

Parameters are

\[
\mu,\nu,r\in(-1,1),\qquad u\in(0,1),
\]

with

\[
x={1+\mu\over2},\quad y={1+\nu\over2},\quad
v=x(1-x)={1-\mu^2\over4},\quad w=y(1-y)={1-\nu^2\over4},
\]

\[
a={1+r\over2},\quad b={1-r\over2},\quad s=u^2,\quad J=1-u^4,\quad L=1-r^2u^4.
\]

The frozen center is the positive-spoke representative

\[
K(u)=
\begin{pmatrix}
x&0&u\sqrt{av}\\
0&y&u\sqrt{bw}\\
u\sqrt{av}&u\sqrt{bw}&{1\over2}-{u^2(a\mu+b\nu)\over2}
\end{pmatrix}.
\]

Changing spoke signs is a diagonal sign conjugation of this representative; the frozen rational input uses the displayed positive square roots. The physical affine test direction \(D\) is represented by fixed coordinates

\[
\zeta=(A,B,C,E,F,G)
\]

through

\[
D_{11}=vA,\quad D_{22}=wB,\quad D_{33}=C,\quad
D_{12}=\sqrt{abvw}\,E,\quad D_{13}=\sqrt{av}\,F,\quad D_{23}=\sqrt{bw}\,G.
\]

These six coordinates are held fixed while differentiating with respect to \(u\). This is essential: differentiating after a further \(u\)-dependent change of direction would compute a different quadratic form. The congruence is invertible throughout the open domain because \(a,b,v,w>0\).

## Domain and the eight atoms

Let

\[
P_{ij}={\bigl(1+(2i-1)\mu\bigr)\bigl(1+(2j-1)\nu\bigr)\over4},\qquad
e_i=i-x,\qquad f_j=j-y.
\]

The first two coordinates are independent at the missing-edge center, so \(P_{ij}>0\). The conditional probability that the third bit equals 1, given leaf state \((i,j)\), is

\[
t_{ij}=q+u^2a(1-i)+u^2b(1-j),\qquad q={1-u^2\over2}.
\]

Equivalently,

\[
t_{00}={1+s\over2},\quad
t_{01}={1+rs\over2},\quad
t_{10}={1-rs\over2},\quad
t_{11}={1-s\over2}.
\]

The complete eight atoms are

\[
p_{ij1}=P_{ij}t_{ij},\qquad p_{ij0}=P_{ij}(1-t_{ij}),\qquad i,j\in\{0,1\}.
\]

All are strictly positive because \(0<P_{ij}\) and \(0<t_{ij}<1\). The displayed center also satisfies \(0<K<I\): using the leading diagonal \(x,y\), the Schur complement of \(K\) is

\[
K_{33}-{K_{13}^2\over x}-{K_{23}^2\over y}={1-u^2\over2}>0,
\]

and the corresponding Schur complement of \(I-K\), using \(1-x,1-y\), is also

\[
(I-K)_{33}-{K_{13}^2\over1-x}-{K_{23}^2\over1-y}={1-u^2\over2}>0.
\]

For the conditional Bernoulli denominators,

\[
4t_{ij}(1-t_{ij})=
\begin{cases}
J,& i=j,\\
L,& i\ne j.
\end{cases}
\]

This is exactly the stated `denij` map.

## First jets and Fisher split

For the leaf marginal,

\[
P'_{ij}=P_{ij}(e_iA+f_jB)
\]

in the fixed \(\zeta\)-coordinates. Direct quotient differentiation of the eight inclusion-exclusion atoms gives the conditional first jet

\[
T_{ij}=q_{ij}^{T}\zeta,
\]

where

\[
q_{ij}=
\begin{pmatrix}
u^2ae_i^2\\
u^2bf_j^2\\
1\\
2u^2ab e_if_j\\
-2uae_i\\
-2ubf_j
\end{pmatrix}.
\]

Thus the atom first derivatives are

\[
p'_{ij1}=P_{ij}\{(e_iA+f_jB)t_{ij}+T_{ij}\},
\]

\[
p'_{ij0}=P_{ij}\{(e_iA+f_jB)(1-t_{ij})-T_{ij}\}.
\]

For each fixed \((i,j)\), the two \(k=0,1\) Fisher terms satisfy

\[
{(p'_{ij1})^2\over p_{ij1}}+{(p'_{ij0})^2\over p_{ij0}}
= { (P'_{ij})^2\over P_{ij}}+
P_{ij}{T_{ij}^2\over t_{ij}(1-t_{ij})}.
\]

The cross terms cancel. Summing over the four leaf states gives the retained marginal Fisher

\[
\sum_{i,j}P_{ij}(e_iA+f_jB)^2=vA^2+wB^2,
\]

namely \(\operatorname{diag}(v,w,0,0,0,0)\), and the complete conditional Fisher

\[
Fmat=\sum_{i,j}{4P_{ij}\,q_{ij}q_{ij}^{T}\over den_{ij}}.
\]

The marginal Fisher is part of the full negative entropy Hessian, but it is independent of \(u\), so its radial derivative is zero.

## Second jets and log acceleration

Let \(\Delta_T=\det K_T\). The eight exact atoms are obtained by Mobius inversion:

\[
p_S=\sum_{S\subseteq T\subseteq\{1,2,3\}}(-1)^{|T|-|S|}\Delta_T.
\]

At the missing-edge center \(K_{12}=0\), collection of the second-jet log term

\[
\sum_S p_S''\log p_S
\]

against the minors gives the following log coefficients:

\[
C_{12}=\log{p_{110}p_{000}\over p_{100}p_{010}}
=\log{(1-t_{11})(1-t_{00})\over(1-t_{10})(1-t_{01})}
=-v_0,
\]

\[
C_{13}=\log{p_{101}p_{000}\over p_{100}p_{001}}
=\log{t_{10}(1-t_{00})\over(1-t_{10})t_{00}}
=-\ell_0,
\]

\[
C_{23}=\log{p_{011}p_{000}\over p_{010}p_{001}}
=\log{t_{01}(1-t_{00})\over(1-t_{01})t_{00}}
=-k_0,
\]

and

\[
C_{123}=\log{p_{111}p_{100}p_{010}p_{001}
\over p_{110}p_{101}p_{011}p_{000}}
=v_0-v_1=\Lambda.
\]

Here

\[
\ell_0=\psi(t_{00})-\psi(t_{10}),\qquad
k_0=\psi(t_{00})-\psi(t_{01}),
\]

\[
v_0=\log{(1-t_{10})(1-t_{01})\over(1-t_{00})(1-t_{11})},\qquad
v_1=\log{t_{10}t_{01}\over t_{00}t_{11}},
\]

with \(\psi(t)=\log(t/(1-t))\).

For the Lambda-zero path,

\[
v_0=v_1=\log{L\over J},
\]

so the triple determinant second jet is multiplied by zero. The remaining second derivatives are

\[
\Delta_{12}''=2(D_{11}D_{22}-D_{12}^2),\quad
\Delta_{13}''=2(D_{11}D_{33}-D_{13}^2),\quad
\Delta_{23}''=2(D_{22}D_{33}-D_{23}^2).
\]

Therefore the log-acceleration quadratic form is

\[
R_u(\zeta)=
-2v_0(D_{11}D_{22}-D_{12}^2)
-2\ell_0(D_{11}D_{33}-D_{13}^2)
-2k_0(D_{22}D_{33}-D_{23}^2).
\]

After substituting the fixed direction congruence, the only nonzero entries of its symmetric matrix \(R(u)\) are

\[
R_{12}=-v_0vw,\quad R_{13}=-\ell_0v,\quad R_{23}=-k_0w,
\]

\[
R_{44}=2v_0abvw,\quad R_{55}=2\ell_0av,\quad R_{66}=2k_0bw.
\]

The required derivatives of the log coefficients are

\[
{d\ell_0\over du}=4u\left({1\over J}+{r\over L}\right)=n_2,
\]

\[
{dk_0\over du}=4u\left({1\over J}-{r\over L}\right)=n_1,
\]

\[
{dv_0\over du}={4u^3(1-r^2)\over JL}=n_3.
\]

Thus \(Q=R'(u)\) has exactly the stated nonzero entries:

\[
Q_{12}=-n_3vw,\quad Q_{13}=-n_2v,\quad Q_{23}=-n_1w,
\]

\[
Q_{44}=2n_3abvw,\quad Q_{55}=2n_2av,\quad Q_{66}=2n_1bw.
\]

The signs follow from the negative coefficients of the three two-minor log ratios and the positive square terms inside each minor.

## Resulting radial derivative

The full negative entropy Hessian in the fixed coordinates is

\[
B(u)=\operatorname{diag}(v,w,0,0,0,0)+Fmat(u)+R(u).
\]

Since the marginal term is independent of \(u\),

\[
{dB(u)\over du}=Fmat'(u)+R'(u)=Fmat'(u)+Q=M(\mu,\nu,r,u).
\]

At \(u=0\), all conditional probabilities equal \(1/2\), the log-acceleration coefficients \(v_0,\ell_0,k_0\) vanish, and \(q_{ij}=(0,0,1,0,0,0)^T\). Hence

\[
Fmat(0)=4\,e_3e_3^T,\qquad R(0)=0,
\]

and

\[
B(0)=\operatorname{diag}(v,w,4,0,0,0),
\]

as stated.

## Scoped verdict

The literal identity

\[
M=derivative_u(Fmat)+Q
\]

is correct under the frozen conventions. The all-eight-event reconstruction confirms:

- strict \(K\) and \(I-K\) domain on the open parameter range;
- the Lambda-zero cancellation of the complete-event triple log coefficient;
- the conditional Fisher vector \(q_{ij}\) and the \(J/L\) denominator assignment;
- the signs and factors in \(Q\);
- retention of the constant marginal Fisher and its zero radial derivative;
- the initial full negative Hessian \(\operatorname{diag}(v,w,4,0,0,0)\);
- the need to keep the direction congruence fixed in \(u\).

No critical formula gap was found. This review does not prove \(M\succ0\). The remaining obligations are an exact global sign certificate for \(M\), or an exact rational negative quadratic form if one exists. A negative direction for \(M\) would only refute radial monotonicity; it would not by itself be a DPP entropy counterexample.
