# Quantitative spatial memory truncation for the one-loss response proof

Status: **PROVED AS AN AUTHOR LEMMA / PENDING REVIEW**.

This addendum proves the optional estimate stated in Section 8 of `c4_response_p4_one_loss.md`.  It is not needed for the original `p>4` theorem.  The direct infinite-volume theorem uses only the correlation-sum cutoff there.  A polynomial rate for comparing the full second responses of the true and memory-`N` kernels requires one extra memory power in the elementary norm comparison, hence this addendum assumes `a>3` (`p>6`).

## 1. Abstract setup

Let `L` and `Ltilde` be normalized transfer operators with invariant laws `nu` and `nutilde`.  Assume both families satisfy the one-power Poisson estimate on the same scale:

\[
Q:B_r\to B_{r-1},
\qquad
\widetilde Q:B_r\to B_{r-1},
\qquad r>1,
\tag{1.1}
\]

with common constants.  Here

\[
QF=\sum_{n\ge0}L^n(F-\nu F),
\qquad
\widetilde QF=\sum_{n\ge0}\widetilde L^n(F-\widetilde\nu F).
\]

Let `A_j=partial_s^j L` and `Atilde_j=partial_s^j Ltilde`, `j=1,2`.  Fix `b>3`.  Suppose, uniformly in the parameter,

\[
\max_{j=0,1,2}
\|\partial_s^j(\widetilde L-L)\|_{B_r\to B_r}
\le\varepsilon
\tag{1.2}
\]

for `r=b-1,b-2,b-3`, and the unperturbed and perturbed derivative operators are uniformly bounded on those spaces.

## 2. Two exact comparison identities

For every `F in B_r`, `r>1`, invariance and the Poisson equation give

\[
(\widetilde\nu-\nu)F
=\widetilde\nu(\widetilde L-L)QF.
\tag{2.1}
\]

Indeed

\[
(\widetilde\nu-\nu)F
=\widetilde\nu(F-\nu F)
=\widetilde\nu(I-L)QF
=\widetilde\nu(\widetilde L-L)QF.
\]

There is also a Poisson comparison modulo constants:

\[
\widetilde QF-QF
=\widetilde Q\bigl((\widetilde L-L)QF\bigr)
-\widetilde\nu(QF)\mathbf1.
\tag{2.2}
\]

To verify it, apply `I-Ltilde` to both sides.  The source on each side is

\[
(\widetilde L-L)QF
-\widetilde\nu((\widetilde L-L)QF)\mathbf1,
\]

where (2.1) identifies the centering constant.  Both sides have the same `nutilde` mean.  Since every derivative operator satisfies

\[
A_j\mathbf1=\widetilde A_j\mathbf1=0,
\tag{2.3}
\]

the uncontrolled constant in (2.2) disappears in every response formula.

## 3. First Poisson/derivative block

For `F in B_b`, (2.2), (1.1), and (1.2) give

\[
\widetilde A_j\widetilde QF-A_jQF
=(\widetilde A_j-A_j)QF
+\widetilde A_j\widetilde Q((\widetilde L-L)QF),
\tag{3.1}
\]

up to a constant killed by `Atilde_j`.  Since

\[
QF\in B_{b-1},
\quad
(\widetilde L-L)QF\in B_{b-1},
\quad
\widetilde Q(\widetilde L-L)QF\in B_{b-2},
\]

we obtain

\[
\|\widetilde A_j\widetilde QF-A_jQF\|_{B_{b-2}}
\le C\varepsilon\|F\|_{B_b}.
\tag{3.2}
\]

Equation (2.1), applied to `A_jQF in B_{b-1}`, also gives

\[
|\widetilde\nu(A_jQF)-\nu(A_jQF)|
\le C\varepsilon\|F\|_{B_b}.
\tag{3.3}
\]

Thus the first-response formula is Lipschitz under the kernel perturbation.

## 4. The nested second-response block

Put

\[
Y=A_1QF,
\qquad
\widetilde Y=\widetilde A_1\widetilde QF.
\]

Then `Y,Ytilde in B_{b-1}` and (3.2) gives

\[
\|\widetilde Y-Y\|_{B_{b-2}}
\le C\varepsilon\|F\|_{B_b}.
\tag{4.1}
\]

Because `b-2>1`, a further Poisson inverse is legal on the difference:

\[
\|\widetilde Q(\widetilde Y-Y)\|_{B_{b-3}}
\le C\varepsilon\|F\|_{B_b}.
\tag{4.2}
\]

For the same fixed `Y`, (2.2) gives, again modulo a constant,

\[
\widetilde QY-QY
=\widetilde Q((\widetilde L-L)QY).
\]

Here `QY in B_{b-2}` and `b-2>1`, so

\[
\|\widetilde QY-QY\|_{B_{b-3}/\mathbf1}
\le C\varepsilon\|F\|_{B_b}.
\tag{4.3}
\]

Combining (4.2)--(4.3), applying the outer derivative operator, and using (2.3),

\[
\|\widetilde A_1\widetilde Q\widetilde Y-A_1QY\|_{B_{b-3}}
\le C\varepsilon\|F\|_{B_b}.
\tag{4.4}
\]

Finally, (2.1) compares the two invariant expectations of the fixed observable `A_1QY in B_{b-2}`.  The condition `b-2>1` is exactly what makes this last comparison summable.  Hence

\[
\left|
\widetilde\nu(\widetilde A_1\widetilde Q\widetilde A_1\widetilde QF)
-\nu(A_1QA_1QF)
\right|
\le C\varepsilon\|F\|_{B_b}.
\tag{4.5}
\]

The `A_2QF` part is covered by Section 3.  Therefore the full fixed-observable second-response coefficient differs by `O(epsilon)`.

The same calculation, applied to `F_s,F_s',F_s''`, proves the moving-observable statement used for entropy.

## 5. Canonical memory truncation

Let `G_s^[N]` be obtained by freezing the future after coordinate `N`.  If

\[
\sup_s\|\partial_s^j\log G_s\|_{B_a}<\infty,
\qquad j=0,1,2,
\]

then for every `r<a`,

\[
\|\partial_s^j(\log G_s-\log G_s^{[N]})\|_{B_r}
\le C_{r,j}N^{r-a}.
\tag{5.1}
\]

Uniform non-nullness transfers (5.1) to the kernels and their transfer operators.  In (1.2), the largest of the required errors occurs at `r=b-1`, so

\[
\varepsilon_N\le C N^{b-1-a}.
\tag{5.2}
\]

Choose

\[
b=3+\eta,
\qquad0<\eta<a-3.
\]

Then the value, first response, and second response of a uniformly `B_a` moving observable satisfy

\[
\max_{j=0,1,2}
\left|
\partial_s^j\{\nu_s^{[N]}(F_s^{[N]})-\nu_s(F_s)\}
\right|
\le C_{\eta,F}N^{-(a-2-\eta)}.
\tag{5.3}
\]

For the DPP memory exponent `a=p/2`, this quantitative spatial statement is available for `p>6`.  It is separate from the direct `p>4` infinite-volume response theorem.

## 6. Scope

This addendum repairs only the previously unsupported optional spatial-rate sentence.  It does not use finite-window entropy signs, and it does not turn a memory-truncated chain into a DPP claim.  The true `p>4` curvature theorem is proved directly before truncation; (5.3) is a consistency/rerun certificate in the stronger range.
