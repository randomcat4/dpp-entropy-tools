# Correction: localized support cardinality in the preconditioned trace proof

Status: **AUTHOR CORRECTION / PENDING INDEPENDENT REVIEW.**

This file has priority over the support-count statements (2.4), (5.5), and the displayed polynomial power of `m` in (5.8) of `arbitrary_A0_C4_proof.md`. The theorem and the geometric summability mechanism are unchanged.

## 1. What was too optimistic

The first proof text stated that a diagonal summand of a length-`m` product of localized reference inverses and deterministic shifts depends on at most

`C m (R+1)`

binary coordinates. That bound need not follow from the entrywise localization definition as written. Successive inverse factors can thicken each of the finitely many visited endpoint clusters, and a safe direct union bound pays one further factor of `m`.

The corrected bound used for review is

\[
\boxed{|J_{m,R,d}|\le C m^2(R+1).}
\tag{C.1}
\]

The constant depends on the finite reference range but not on the finite volume and, crucially, not on the magnitudes of the displacement tuple `d=(d_1,...,d_m)`.

No claim of the sharper `O(mR)` bound is needed.

## 2. Derivative consequence

For every complete-event local observable supported on `J`, the Bell bound remains

\[
|\partial_t^q E_tF|\le A_q |J|^q\|F\|_\infty,
\qquad 0\le q\le4.
\tag{C.2}
\]

The shell increment of the normalized trace observable still obeys

\[
\|\Delta_R F_{m,d,\Lambda}\|_\infty
\le C m B^{m-1}e^{-aR}.
\tag{C.3}
\]

Using (C.1) in (C.2), the corrected version of (5.5) is therefore

\[
\boxed{
|\partial_t^q E_t\Delta_RF_{m,d,\Lambda}|
\le C_q m^{2q+1}(R+1)^q B^{m-1}e^{-aR}.}
\tag{C.4}
\]

When `ell` of the `q` derivatives hit the affine Fourier coefficients, there are at most `m^ell` assignments. Thus, after summing localization shells and displacement tuples, a deliberately coarse uniform replacement for (5.8) is

\[
\boxed{
\sup_{\Lambda,|t|\le\tau}
\left|\partial_t^q\frac1{|\Lambda|}
E_t\operatorname{Tr}(R^0E_t)^m\right|
\le C_q m^{3q+1} B^{m-1}\eta^{m-q}(1+\|g\|_W)^q.}
\tag{C.5}
\]

Any smaller polynomial power is irrelevant to the argument.

## 3. Why the theorem survives

Choose the finite-range truncation and real parameter interval so that

\[
B\eta<\rho<1.
\]

For each fixed `q<=4`, (C.5) is bounded, up to a constant depending on `q`, by

\[
m^{3q+1}\rho^{m-q}.
\]

Hence

\[
\sum_{m\ge1}\frac1m m^{3q+1}\rho^{m-q}<\infty.
\tag{C.6}
\]

The shell sum is also finite because

\[
\sum_R(R+1)^q e^{-aR}<\infty.
\]

Therefore the sequence of limit interchanges used in the relative-KL part remains dominated through derivative order four.

The essential low-regularity point is unchanged: the Bell differentiation cost depends polynomially on the **number of localized coordinates**, while the Fourier displacement sums use only

\[
\sum_j|\widehat r(j)|,
\qquad
\sum_j|\widehat g(j)|.
\]

No factor such as `(1+|d_j|)^p` appears. Thus the correction does not insert a positive Fourier moment.

## 4. Evidence boundary

This is an author-side proof correction, not an independent review. No numerical or machine evidence is involved. The original optimistic support count is retained in Git history and is explicitly superseded here rather than silently rewritten.