# Two-scale continuity detail for the finite-response lemma

Status: **AUTHOR PROOF SUPPLEMENT / PENDING_REVIEW**.

This note expands the continuity paragraph following equations (6.5)--(6.7) of `c4_response_p4_repair.md`.  It is important when `a=p/2` is only slightly larger than two: the two interpolation losses must have total strictly below `a-2`.

## 1. Uniform operator input

Fix a compact physical `s`-interval inside the common non-null neighborhood.  For every `1<b<=a`, the coupling proof gives constants independent of `s` such that

\[
\|L_s^n(F-\nu_sF)\|_\infty
\le C_b(1+n)^{-b}\|F\|_{B_b},
\tag{1.1}
\]

and

\[
\|R_sF\|_{B_{b-1}}
\le C_b\|F\|_{B_b}.
\tag{1.2}
\]

The coefficient family `G_s` is `C^2` in `B_a`.  Hence, for every `0<c<=a`,

\[
s\longmapsto L_s,\ A_{1,s},\ A_{2,s}
\]

is continuous in the operator norm on `B_c`; the second-order Taylor remainder of `L_s` is `o(h^2)` in that norm.  Indeed, if `x,y` agree in their first `m` sites, then `\xi x,\xi y` agree in their first `m+1`, and

\[
\operatorname{var}_m\left(
\sum_\xi B_s(\xi|\cdot)F(\xi\cdot)
\right)
\le C\left[
\|F\|_\infty\operatorname{var}_mB_s
+\|B_s\|_\infty\operatorname{var}_{m+1}F
\right]
\tag{1.3}
\]

for `B_s=G_s`, either derivative, or a Taylor remainder.  Since `c<=a`, the right side is controlled in `B_c`.

Weak continuity of `nu_s` is supplied directly by the complete-event determinant formula in `c4_response_p4_measure_continuity.md`.

## 2. Continuity of one Poisson inverse

Let `s_j->s` and let `F_{s_j}->F_s` in `B_b`, with `b>1`, while the family is uniformly bounded there.  Write

\[
R_{s_j}F_{s_j}
=\sum_{n\ge0}L_{s_j}^n(F_{s_j}-\nu_{s_j}F_{s_j}).
\]

For every fixed cutoff `N`, the partial sum through `N` converges uniformly to the corresponding `s`-sum.  This follows from operator continuity, weak continuity of `nu`, and uniform convergence of the observables.

The remaining tail is uniformly bounded in sup norm by

\[
C_b\sup_j\|F_{s_j}\|_{B_b}
\sum_{n>N}(1+n)^{-b},
\]

which tends to zero independently of `j`.  Therefore

\[
\|R_{s_j}F_{s_j}-R_sF_s\|_\infty\to0.
\tag{2.1}
\]

Equation (1.2) gives a common `B_{b-1}` bound.  For `0<eta<b-1`, use

\[
\|U\|_{B_{b-1-\eta}}
\le C
\|U\|_\infty^{\eta/(b-1)}
\|U\|_{B_{b-1}}^{1-\eta/(b-1)}.
\tag{2.2}
\]

Applying (2.2) to the difference in (2.1) proves

\[
R_{s_j}F_{s_j}\longrightarrow R_sF_s
\quad\text{in }B_{b-1-\eta}.
\tag{2.3}
\]

## 3. Two successive inverses

Choose positive numbers `eta_1,eta_2` satisfying

\[
\eta_1+\eta_2<a-2.
\tag{3.1}
\]

For a `C^2(B_a)` family `F_s`, apply (2.3) with `b=a` and `eta=eta_1`:

\[
U_s:=R_sF_s
\quad\text{is continuous in }B_{a-1-\eta_1}.
\tag{3.2}
\]

Set

\[
H_s:=A_{1,s}U_s.
\]

Operator continuity from (1.3) gives

\[
H_s\quad\text{continuous in }B_{a-1-\eta_1}.
\tag{3.3}
\]

The exponent in (3.3) is larger than one by (3.1).  Apply (2.3) again, now with

\[
b=a-1-\eta_1
\]

and interpolation loss `eta_2`:

\[
R_sH_s
\quad\text{is continuous in }
B_{a-2-\eta_1-\eta_2}.
\tag{3.4}
\]

The final exponent is positive by (3.1), so the observable is continuous and uniformly bounded.  Consequently

\[
s\longmapsto
\nu_s\bigl(A_{1,s}R_s(A_{1,s}R_sF_s)\bigr)
\tag{3.5}
\]

is continuous.  The terms with only one Poisson inverse are covered already by (3.2).  The same argument applies to `F_s'`.

This proves continuity of every term in

\[
\begin{aligned}
\frac{d^2}{ds^2}\nu_s(F_s)
={}&\nu_s(F_s'')
+2\nu_s(A_{1,s}R_sF_s')
+\nu_s(A_{2,s}R_sF_s)\\
&+2\nu_s(A_{1,s}R_s(A_{1,s}R_sF_s)).
\end{aligned}
\tag{3.6}
\]

It also proves right-continuity at `s=0` because every argument used one-sided convergence only.

## 4. Difference quotients with exact remainders

For completeness, fix `s` and a fixed `F in B_a`.  The exact identity is

\[
(\nu_{s+h}-\nu_s)(F)
=\nu_{s+h}(L_{s+h}-L_s)R_sF.
\tag{4.1}
\]

On `B_{a-1}`,

\[
L_{s+h}-L_s
=hA_{1,s}+\frac{h^2}{2}A_{2,s}+o(h^2).
\tag{4.2}
\]

Dividing (4.1) by `h`, using weak continuity and (4.2), gives

\[
\nu_s'(F)=\nu_s(A_{1,s}R_sF).
\tag{4.3}
\]

Subtract `h` times (4.3) from (4.1), divide by `h^2/2`, and obtain

\[
\begin{aligned}
\frac{2}{h^2}
\bigl[(\nu_{s+h}-\nu_s)(F)-h\nu_s(A_{1,s}R_sF)\bigr]
={}&2\frac{(\nu_{s+h}-\nu_s)(A_{1,s}R_sF)}{h}\\
&+\nu_{s+h}(A_{2,s}R_sF)+o(1).
\end{aligned}
\tag{4.4}
\]

The first quotient on the right is legitimate because

\[
A_{1,s}R_sF\in B_{a-1},
\qquad a-1>1.
\]

Apply (4.3) to that fixed observable.  The limit of (4.4) is

\[
\nu_s''(F)
=2\nu_s(A_{1,s}R_s(A_{1,s}R_sF))
+\nu_s(A_{2,s}R_sF).
\tag{4.5}
\]

For a moving observable, (3.6) follows from the ordinary second-order chain rule for the scalar-valued linear functional `F -> nu_s(F)`.  No derivative of `R_s` is assumed or inserted.

## 5. Threshold accounting

The only strict inequalities required are

\[
a>2,
\qquad
\eta_1>0,
\qquad
\eta_2>0,
\qquad
\eta_1+\eta_2<a-2.
\]

Thus the response proof closes for every `a=p/2>2`, equivalently every `p>4`; it does not hide a stronger exponent threshold in the continuity step.