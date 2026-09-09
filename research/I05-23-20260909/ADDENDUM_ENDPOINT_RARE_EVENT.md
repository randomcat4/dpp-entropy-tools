# Addendum — rare-event Fisher dominance at a simple legal endpoint

Status: **PROVED (author proof), not independently reviewed**.

This result uses, rather than removes, a vanishing complete event.  Together
with the decoupling theorem in `RESULT.md`, it localizes any possible
positive-curvature interval away from both the center and every simple
spectral endpoint.

## Lemma B.1 (a simple vanishing atom forces negative infinite curvature)

Let `Omega` be finite and let `p_omega(t)` be probability polynomials (more
generally, real-analytic probabilities) on a left neighborhood of `b`, with

\[
p_\omega(t)>0\quad(t<b),\qquad \sum_\omega p_\omega(t)=1.
\]

Assume at least one atom has a simple zero at `b`.  Then the Shannon entropy

\[
H(t)=-\sum_\omega p_\omega(t)\log p_\omega(t)
\]

satisfies

\[
\lim_{t\uparrow b}H''(t)=-\infty.                            \tag{B.1}
\]

### Proof

Put `x=b-t`.  Every atom positive for `x>0` either has a positive limit at
`x=0`, or has a finite integer vanishing order `m_omega>=1`:

\[
p_\omega(b-x)=a_\omega x^{m_\omega}(1+O(x)),
\qquad a_\omega>0.                                          \tag{B.2}
\]

For a positive-limit atom, its contribution to `H''` remains bounded.  For
an atom of order `m`,

\[
-\frac{(p_\omega')^2}{p_\omega}
=-a_\omega m^2x^{m-2}(1+O(x)).                              \tag{B.3}
\]

If `m=1`, its acceleration is bounded and hence

\[
-p_\omega''\log p_\omega=O(|\log x|),                       \tag{B.4}
\]

while (B.3) equals `-a_omega/x+O(1)`.  If `m>=2`, both the
Fisher and acceleration contributions are at worst

\[
O(x^{m-2}|\log x|)=O(|\log x|).                             \tag{B.5}
\]

The exact complete-law identity

\[
H''(t)=-\sum_\omega\frac{(p_\omega')^2}{p_\omega}
       -\sum_\omega p_\omega''\log p_\omega                 \tag{B.6}
\]

uses `sum p_omega''=0`; no atom has been discarded.  Summing (B.3)--(B.5),
all simple atoms contribute

\[
-\frac{\sum_{m_\omega=1}a_\omega}{x}+O(|\log x|).
\]

The coefficient is strictly positive by hypothesis, proving (B.1). ∎

## Theorem B.2 (simple spectral endpoints of a block radial DPP)

Let `A,C` be strict real finite DPP kernels, let `B!=0`, and let

\[
K(t)=\begin{pmatrix}A&tB\\tB^{\mathsf T}&C\end{pmatrix}.
\]

Suppose `t_*>0` is a legal endpoint: `K(t)` is strict for
`0<=t<t_*` and is a positive contraction at `t=t_*`.  If either

\[
\dim\ker K(t_*)=1                                           \tag{B.7}
\]

or

\[
\dim\ker(I-K(t_*))=1,                                      \tag{B.8}
\]

then

\[
\lim_{t\uparrow t_*}H''(K(t))=-\infty.                      \tag{B.9}
\]

Consequently there is `eta>0` such that

\[
H''(K(t))<0\qquad(t_*-\eta<t<t_*).                           \tag{B.10}
\]

The same conclusion holds at the negative endpoint by the evenness of the
complete law under `t -> -t`.

### Proof

Every exact DPP atom is a polynomial in the entries of `K(t)`, hence a
polynomial in `t`.  It is positive on the strict interior.  It therefore
suffices, by Lemma B.1, to find one complete atom with a simple endpoint
zero.

If (B.7) holds, use the full atom

\[
p_{[m+\ell]}(t)=\det K(t).
\]

The Schur complement through the strict block `A` gives

\[
\det K(t)=\det A\,
\det\!\left(C-t^2B^{\mathsf T}A^{-1}B\right).                \tag{B.11}
\]

Set `M=B^T A^{-1}B` and `s_*=t_*^2`.  Congruence by the invertible block
elimination matrix shows that (B.7) is equivalent to

\[
\dim\ker(C-s_*M)=1.                                         \tag{B.12}
\]

For a nonzero vector `v` in this kernel,

\[
s_*v^{\mathsf T}Mv=v^{\mathsf T}Cv>0,                      \tag{B.13}
\]

because `C` is positive definite.  Thus the unique zero eigenvalue of
`C-sM` crosses with strictly negative derivative at `s=s_*`; the other
eigenvalues are positive.  Its determinant has a simple zero in `s`, and,
since `t_*>0`, (B.11) has a simple zero in `t`.  Lemma B.1 applies.

If (B.8) holds, use the empty atom

\[
p_\varnothing(t)=\det(I-K(t)).
\]

Now the Schur complement through `I-A` gives

\[
\det(I-K(t))=\det(I-A)\,
\det\!\left(I-C-t^2B^{\mathsf T}(I-A)^{-1}B\right).          \tag{B.14}
\]

The identical argument, with `C` replaced by `I-C`, proves that this atom
has a simple zero.  This establishes (B.9)--(B.10). ∎

## Exact checkability and scope

For rational `A,B,C`, the two endpoint determinants in (B.11) and (B.14)
are univariate rational polynomials in `s=t^2`.  A simple endpoint can be
certified exactly by a square-free factorization or by verifying that the
endpoint root and the derivative have nonzero resultant; an algebraic
isolating interval then fixes which root is the legal endpoint.  No finite
sampling or deletion of rare configurations is involved.

The theorem does not cover a multiple spectral endpoint.  At a quadratic
vanishing atom, the acceleration term can grow like `+|log(t_*-t)|`, so a
simple-root hypothesis cannot simply be dropped.  Thus the remaining
whole-chord search is localized to a compact middle interval together with
nongeneric multiple-endpoint cases.