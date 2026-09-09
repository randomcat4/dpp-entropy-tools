# Addendum — exact rank-two spectral test for endpoint simplicity

Status: **PROVED (author proof), not independently reviewed**.

This makes the simple-endpoint hypothesis in
`ADDENDUM_ENDPOINT_RARE_EVENT.md` directly checkable from `A,B,C`.

Let `A,C` be strict and let `rank(B)=2`.  Define the two positive
semidefinite, rank-two whitened cross operators

\[
R_0=C^{-1/2}B^{\mathsf T}A^{-1}BC^{-1/2},                   \tag{C.1}
\]

\[
R_1=(I-C)^{-1/2}B^{\mathsf T}(I-A)^{-1}B(I-C)^{-1/2},       \tag{C.2}
\]

and put

\[
\rho_0=\lambda_{\max}(R_0),\qquad
\rho_1=\lambda_{\max}(R_1).                                 \tag{C.3}
\]

Both numbers are positive.  The squared positive endpoint of the full
legal radial interval is

\[
s_*=t_*^2=\frac1{\max\{\rho_0,\rho_1\}}.                   \tag{C.4}
\]

Indeed, Schur complementation gives

\[
K(t)\succeq0
\iff I-sR_0\succeq0
\iff s\le\rho_0^{-1},                                      \tag{C.5}
\]

and

\[
I-K(t)\succeq0
\iff I-sR_1\succeq0
\iff s\le\rho_1^{-1}.                                      \tag{C.6}
\]

At `s=s_*`, the nullity of `K(t_*)` equals the multiplicity of `rho_0`
when `rho_0=max(rho_0,rho_1)`; the analogous statement holds for `I-K`
and `rho_1`.  Because each `R_nu` has rank exactly two, an active endpoint
has nullity two rather than one exactly when its two positive eigenvalues
coincide.

For a rank-two positive semidefinite matrix `R`, this exceptional equality
has the basis-free polynomial form

\[
\Delta(R):=2\operatorname{tr}(R^2)-(\operatorname{tr}R)^2=0, \tag{C.7}
\]

because `Delta(R)=(lambda_1-lambda_2)^2`.  Consequently:

## Corollary C.1

If at least one active operator `R_nu`, meaning
`rho_nu=max(rho_0,rho_1)`, satisfies

\[
\Delta(R_\nu)>0,                                             \tag{C.8}
\]

then the corresponding full or empty complete event has a simple zero and

\[
\lim_{t\uparrow t_*}H''(K(t))=-\infty.                       \tag{C.9}
\]

Thus a rank-two path can evade the rare-event endpoint theorem only if
**every** operator attaining the larger value in (C.3) obeys the exact
isotropy equation (C.7).  If `rho_0=rho_1`, it is enough that either active
operator have `Delta>0`.

### Proof

Equations (C.5)--(C.6) follow by congruence from the two Schur complements

\[
C-sB^{\mathsf T}A^{-1}B,
\qquad
I-C-sB^{\mathsf T}(I-A)^{-1}B.
\]

Congruence also preserves nullity, so the endpoint nullities are the
multiplicities of the eigenvalue `1/s_*` in the active whitened operators.
Rank preservation under multiplication by positive definite matrices
shows that `R_0,R_1` both have rank two.  Formula (C.7) is immediate from
their two positive eigenvalues.  Condition (C.8) therefore gives a
one-dimensional endpoint kernel, and Theorem B.2 applies. ∎

## Exact arithmetic interface

No matrix square root is needed for certification.  The two nonzero
eigenvalues of `R_0` are the generalized eigenvalues of

\[
B^{\mathsf T}A^{-1}B\,v=\rho\,Cv,                            \tag{C.10}
\]

and similarly for `R_1`.  For rational input, their quadratic factor,
comparison of `rho_0` and `rho_1`, and the discriminant in (C.7) can all be
certified with rational polynomial arithmetic and algebraic root-isolating
intervals.

This result still does not settle the compact interior of the legal chord
or the exceptional double-endpoint locus.