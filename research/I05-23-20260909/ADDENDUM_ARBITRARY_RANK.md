# Addendum — arbitrary-rank strict radial curvature near decoupling

Status: **PROVED (author proof), not independently reviewed**.

This strengthens Section 1 of `RESULT.md`.  The rank-two statement there
has sharper constants because its complete likelihood is quadratic.  The
argument below shows that the local strict-curvature phenomenon itself does
not depend on rank two.

## Theorem A (finite explicit certificate for every nonzero cross block)

Let

\[
0\prec A\prec I,\qquad 0\prec C\prec I,
\]

and let `B` be any nonzero real `m x ell` matrix of rank `r`.  Put

\[
K(t)=\begin{pmatrix}A&tB\\tB^{\mathsf T}&C\end{pmatrix}.
\]

There is an explicitly computable `delta>0` such that `K(t)` is strict and

\[
H''(t)\le-3\underline\sigma_{ij}^{\,2}t^2<0
\qquad(0<|t|\le\sqrt\delta),                                 \tag{A.1}
\]

where `(i,j)` is any pair with `B_ij != 0` and

\[
\underline\sigma_{ij}^{\,2}
=\frac{B_{ij}^4}{A_{ii}C_{jj}(1-A_{ii}C_{jj})}.              \tag{A.2}
\]

All complete configurations and the complete Fisher term are retained.
For rational input, choose certified positive rational lower bounds for
the four spectral margins and a certified positive rational upper bound
for `||B||_op`, for example by exact root isolation and rational matrix-norm
bounds. Substitute those bounds for `epsilon` and `beta` below and replace
`log 2` by its rational upper bound `1`; the resulting radius is rational.

## Complete likelihood polynomial

For complete configurations `S,T`, let

\[
X_S=A-E_{S^c},\qquad Y_T=C-E_{T^c},\qquad
\mu(S,T)=p_A(S)p_C(T).
\]

Strictness makes `X_S,Y_T` invertible.  With `s=t^2`, the Schur complement
gives the exact full-law likelihood

\[
q_s(S,T):=\frac{p_s(S,T)}{\mu(S,T)}
=\det\!\left(I_\ell-sY_T^{-1}B^{\mathsf T}X_S^{-1}B\right)
=1+\sum_{k=1}^{r}s^k w_k(S,T).                               \tag{A.3}
\]

The determinant has degree at most `r` because the perturbation has rank
at most `r`.  Normalization for every `s` implies

\[
\mathbb E_\mu w_k=0\qquad(1\le k\le r).                      \tag{A.4}
\]

The first coefficient is

\[
w_1(S,T)=-\operatorname{tr}
 \left(Y_T^{-1}B^{\mathsf T}X_S^{-1}B\right).                \tag{A.5}
\]

Let

\[
\sigma^2=\mathbb E_\mu w_1^2.
\]

For `Z_ij=1_{\{i\in S,j\in T\}}`, the exact two-point inclusion law is

\[
\mathbb E_{p_s}Z_{ij}=A_{ii}C_{jj}-sB_{ij}^2.
\]

Differentiating at zero and using (A.3)--(A.4),

\[
\mathbb E_\mu[Z_{ij}w_1]=-B_{ij}^2.
\]

Since `Z_ij` is Bernoulli under the product law `mu`, Cauchy--Schwarz gives

\[
\sigma^2\ge
\frac{B_{ij}^4}{A_{ii}C_{jj}(1-A_{ii}C_{jj})}
=\underline\sigma_{ij}^{\,2}>0.                             \tag{A.6}
\]

Thus the first complete-law score cannot vanish for a nonzero cross block.

## An explicit radius

Define

\[
\varepsilon=\min\{\lambda_{\min}(A),\lambda_{\min}(C),
\lambda_{\min}(I-A),\lambda_{\min}(I-C)\},
\qquad\beta=\|B\|_{\rm op},
\]

and finite coefficient bounds

\[
W_k=\max_{S,T}|w_k(S,T)|,
\]

\[
C_0=\sum_{k=1}^rW_k,\quad
C_1=\sum_{k=1}^rkW_k,\quad
C_2=\sum_{k=1}^rk(k-1)W_k,\quad
C_3=\sum_{k=1}^rk(k-1)(k-2)W_k.                             \tag{A.7}
\]

Equation (A.6) implies `C_0>0`.  Set

\[
\delta_0=\min\left\{
\left(\frac{\varepsilon}{2\beta}\right)^2,
1,\frac1{2C_0}\right\},                                    \tag{A.8}
\]

\[
L_3=C_3\log2+6C_1C_2+4C_1^3,                               \tag{A.9}
\]

\[
\delta=\min\left\{\delta_0,
\frac{3\underline\sigma_{ij}^{\,2}}{10L_3}\right\}.         \tag{A.10}
\]

Here `C_1>0`, so `L_3>0`.

For `0<=s<=delta_0`, (A.3), `s<=1`, and (A.8) give

\[
|q_s-1|\le sC_0\le\frac12,
\]

hence `1/2<=q_s<=3/2` and `|log q_s|<=log 2`.  Also

\[
|q_s'|\le C_1,\qquad |q_s''|\le C_2,
\qquad |q_s'''|\le C_3.                                     \tag{A.11}
\]

## Entropy derivatives and true `t`-curvature

The two block marginals are fixed, so

\[
H(K(t))=H(A)+H(C)-I(s),
\qquad I(s)=\mathbb E_\mu[q_s\log q_s].                     \tag{A.12}
\]

Normalization removes the derivatives of `q_s` without logarithms and
yields

\[
I''(s)=\mathbb E_\mu\left[q_s''\log q_s+
\frac{(q_s')^2}{q_s}\right],                                \tag{A.13}
\]

\[
I'''(s)=\mathbb E_\mu\left[q_s'''\log q_s+
3\frac{q_s'q_s''}{q_s}-\frac{(q_s')^3}{q_s^2}\right].        \tag{A.14}
\]

The second term in (A.13) is the full Fisher term.  At zero,

\[
I'(0)=0,\qquad I''(0)=\sigma^2.                              \tag{A.15}
\]

Equations (A.11)--(A.14) give

\[
|I'''(s)|\le C_3\log2+6C_1C_2+4C_1^3=L_3.                  \tag{A.16}
\]

Let

\[
J(s)=2I'(s)+4sI''(s)=-H''(\sqrt s).
\]

Then `J(0)=0` and

\[
J'(s)=6I''(s)+4sI'''(s)
\ge6\sigma^2-10L_3s
\ge3\underline\sigma_{ij}^{\,2}
\quad(0\le s\le\delta).                                    \tag{A.17}
\]

Therefore

\[
J(s)\ge3\underline\sigma_{ij}^{\,2}s.
\]

Finally, the first term in (A.8) and Weyl's inequality give
`K(t) >= epsilon I/2` and `I-K(t) >= epsilon I/2` throughout the stated
range.  Substituting `s=t^2` proves (A.1). ∎

## Scope and relation to the main target

The theorem applies to arbitrary finite cross rank and arbitrary internal
correlation, but only near the decoupling point.  It does not imply the
whole legal radial chord and does not replace the unresolved rank-two
four-cycle or nonreversible-entropy mechanisms.  Its role is a general,
checkable weak lemma: any strict counterexample to whole-chord concavity
must occur away from a certified neighborhood of `t=0`.