# Correction: boundary error for the `p>4` finite-response proof

Status: **AUTHOR CORRECTION / PENDING_REVIEW**.

This file supersedes only equations (7.3)--(7.5) of `c4_response_p4_repair.md`.  The kernel truncation estimate (7.2) is correct, but the displayed second-response rate `O(N^{b-a})` was asserted too quickly: in the nested term `R A_1 R`, the quotient resolvent identity can consume an additional polynomial space before the outer Poisson inverse is applied.  That rate is therefore **withdrawn**.  It is not used in the entropy-concavity proof.

The verifiable boundary estimate needed for the finite response lemma is instead the following cutoff of its Poisson/correlation sums.

## 1. One-Poisson cutoff

For `F in B_b`, `b>1`, define

\[
\mathcal R_s^{<N}F
:=\sum_{n=0}^{N-1}\mathcal L_s^n(F-\nu_sF).
\]

The relaxation estimate (4.7) in the main file gives, uniformly for small physical `s`,

\[
\boxed{
\|\mathcal R_sF-\mathcal R_s^{<N}F\|_\infty
\le C_b\|F\|_b N^{1-b}.}
\tag{C.1}
\]

Thus truncating the first-response correlation sum

\[
D\nu_s(F)=\nu_s(A_{1,s}\mathcal R_sF)
\]

at time `N` has scalar error `O(N^{1-b})`.

## 2. Interpolated inner-tail estimate

For the DPP application take the full memory exponent `a=p/2>2`.  Put

\[
U_{N,s}F=(\mathcal R_s-\mathcal R_s^{<N})F.
\]

Equation (C.1) with `b=a` gives

\[
\|U_{N,s}F\|_\infty\le C\|F\|_aN^{-(a-1)}.
\tag{C.2}
\]

Both `R_sF` and its partial sums are uniformly bounded in `B_{a-1}` by the same first-disagreement estimate used in Lemma 5.2 (the proof sums a subset of nonnegative upper bounds).  Hence

\[
\sup_N\|U_{N,s}F\|_{a-1}\le C\|F\|_a.
\tag{C.3}
\]

For `0<eta<a-2`, the elementary variation interpolation inequality

\[
\|U\|_{B_{c-eta}}
\le C_{c,eta}
\|U\|_\infty^{eta/c}
\|U\|_{B_c}^{1-eta/c},
\qquad c>eta,
\tag{C.4}
\]

follows by bounding

\[
\operatorname{var}_mU
\le\min\{2\|U\|_\infty,\|U\|_{B_c}(1+m)^{-c}\}
\]

and optimizing in `m`.  Applying (C.4) with `c=a-1` to (C.2)--(C.3) gives the explicit strong-tail estimate

\[
\boxed{
\|U_{N,s}F\|_{B_{a-1-eta}}
\le C_{a,eta}\|F\|_aN^{-eta}.}
\tag{C.5}
\]

The restriction `eta<a-2` is exactly what leaves `a-1-eta>1`, so one more Poisson inverse is legal.

## 3. Two-Poisson response cutoff

For a fixed observable, the nested part of the second response is

\[
T_s(F)=\nu_s\bigl(A_{1,s}\mathcal R_s(A_{1,s}\mathcal R_sF)\bigr).
\]

Define its finite correlation-sum approximation by

\[
T_s^{<N}(F)=
\nu_s\bigl(A_{1,s}\mathcal R_s^{<N}
(A_{1,s}\mathcal R_s^{<N}F)\bigr).
\]

Decompose

\[
\begin{aligned}
T_s(F)-T_s^{<N}(F)
={}&\nu_s A_{1,s}(\mathcal R_s-\mathcal R_s^{<N})
(A_{1,s}\mathcal R_sF)\\
&+\nu_s A_{1,s}\mathcal R_s^{<N}
A_{1,s}(\mathcal R_s-\mathcal R_s^{<N})F.
\end{aligned}
\tag{C.6}
\]

The first input `A_1 R F` lies in `B_{a-1}`.  Equation (C.1), now with exponent `a-1>1`, bounds the first line by

\[
O(N^{2-a}).
\tag{C.7}
\]

For the second line, (C.5) and boundedness of `A_1` give an input of size `O(N^{-eta})` in `B_{a-1-eta}`.  Since `a-1-eta>1`, the partial Poisson sums are uniformly bounded from that space to the sup norm.  Hence the second line is `O(N^{-eta})`.

Therefore, for every `0<eta<a-2`,

\[
\boxed{
|T_s(F)-T_s^{<N}(F)|
\le C_{a,eta,F}N^{-eta}.}
\tag{C.8}
\]

The non-nested term `nu_s(A_2 R_sF)` has the sharper error `O(N^{1-a})`.  Combining these bounds with the moving-observable Leibniz terms gives a uniform finite-correlation-sum approximation to all terms in (6.4):

\[
\boxed{
|\text{second response}-\text{its time-}N\text{ Poisson cutoff}|
\le C_{eta}N^{-eta},
\quad 0<eta<a-2.}
\tag{C.9}
\]

This is the boundary error used by the repaired proof.  It is positive for every `a>2`, hence for every `p>4`.

## 4. What remains unclaimed

The canonical frozen-future kernel itself still satisfies

\[
\|\partial_s^j(\log G_s-\log G_s^{[N]})\|_{B_b}
=O(N^{b-a}),\qquad b<a,\ j=0,1,2,
\]

as proved in (7.2) of the main file.  This correction does **not** claim that the corresponding stationary second responses converge at the same exponent.  A separate multiscale perturbation argument would be needed for that stronger statement.

No theorem threshold or entropy conclusion changes.  The load-bearing one-power Poisson lemma and the `p>4` response/curvature chain are unaffected.