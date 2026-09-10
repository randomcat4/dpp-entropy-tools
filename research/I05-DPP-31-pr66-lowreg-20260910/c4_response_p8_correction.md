# Correction to the BFG relaxation step in `c4_response_p8.md`

Status: **AUTHOR CORRECTION; this file is part of the p>8 proof and supersedes the proof paragraph of Lemma 4.1 in `c4_response_p8.md`.**

The statement of Lemma 4.1 is retained.  The original proof paragraph was too compressed: Bressaud--Fernandez--Galves Theorem 1 is written for observables whose variations are controlled relative to the chosen continuity modulus, so one must not simply replace their observable by an arbitrary `B_b` observable without changing the coupling majorant.

Here is the missing argument.

Let

\[
\phi_t=\log G_t,
\qquad
\operatorname{var}_m\phi_t\le C(1+m)^{-a},
\qquad a=p/2,
\]

uniformly on the real parameter interval.  Fix `1<b<=a`.  The BFG chain condition only requires a decreasing sequence `gamma_m` for which

\[
\inf_{u_m=v_m}\frac{G_t(\xi\mid u)}{G_t(\xi\mid v)}\ge1-\gamma_m.
\tag{C.1}
\]

The canonical choice `1-exp(-var_m phi_t)` is not mandatory.  By uniform non-nullness and the displayed polynomial variation bound, we may choose a common decreasing majorant

\[
\bar\gamma_m^{(b)}\le C_b(1+m)^{-b},
\qquad \bar\gamma_0^{(b)}<1,
\tag{C.2}
\]

that dominates `1-exp(-var_m phi_t)` for every small `t`.  For example, take the decreasing envelope of

\[
\max\{1-e^{-\sup_t\operatorname{var}_m\phi_t},\;c_b(1+m)^{-b}\}
\]

with `c_b` chosen so the second term dominates the first for large `m`; enlarge finitely many initial entries while keeping them below one, which is possible from the common non-nullness bound.

Run the BFG maximal coupling with `bar gamma^(b)` rather than the smaller canonical sequence.  Their Proposition 2(iv) applies to this polynomial majorant and gives

\[
(\bar\gamma^{(b)})_n^*\le C'_b(1+n)^{-b}.
\tag{C.3}
\]

Moreover the first-return probabilities of the dominating renewal chain satisfy, by BFG equation (5.11),

\[
\mathbf P(\tau=k)\asymp \bar\gamma^{(b)}_{k-1}
\]

up to constants because `sum_m bar gamma_m^(b)<infinity` for `b>1` and therefore the infinite product `prod_m(1-bar gamma_m^(b))` is strictly positive.

Now let `F in B_b`.  In the BFG proof, before their equation (5.9), the only observable-specific quantity is

\[
\sum_{k\ge0}\operatorname{var}_k(F)\,\mathbf P(T_n=k).
\]

Since

\[
\operatorname{var}_k(F)\le\|F\|_b(1+k)^{-b}
\le C\|F\|_b\mathbf P(\tau=k+1),
\tag{C.4}
\]

we may repeat their renewal convolution step verbatim with `bar gamma^(b)`.  This gives

\[
\sup_{x,y}|\mathcal L_t^nF(x)-\mathcal L_t^nF(y)|
\le C_b\|F\|_b(\bar\gamma^{(b)})_n^*
\le C_b'\|F\|_b(1+n)^{-b}.
\tag{C.5}
\]

Integrating one endpoint against the stationary law proves

\[
\|\mathcal L_t^n(F-\nu_tF)\|_\infty
\le C_b'\|F\|_b(1+n)^{-b},
\]

which is Lemma 4.1.

This correction matters in the second Poisson step.  After

\[
R:B_b\to B_{b-2},
\]

the next relaxation estimate is obtained by rerunning the coupling with the enlarged polynomial majorant `bar gamma^(b-2)`, not by pretending that a `B_{b-2}` observable lies in the original BFG `V_phi` norm.

No theorem statement or threshold changes: two Poisson inverses remain valid for any `b>4`, hence for DPP memory exponent `a=p/2>4`, i.e. `p>8`.
