# Source-bound audit of the `p>4` finite-response repair

Status: **AUTHOR RE-DERIVATION / PENDING_REVIEW**.  This is a fresh audit inside the author context, not an independent FIRST or SECOND.

This note checks the two load-bearing steps of `c4_response_p4_repair.md` directly against the primary coupling formulas and then rederives the response identities without importing a general linear-response theorem.  It also records the one withdrawn boundary claim and its corrected replacement.

## 1. Exact BFG map: arbitrary `B_b` observables

Let `P(\xi|x)=G_s(\xi|x)` for a fixed small physical `s`.  If histories agree in their first `m` symbols, the DPP variation estimate gives

\[
\frac{P(\xi|x)}{P(\xi|y)}
\ge \exp[-C(1+m)^{-a}].
\]

For any `1<b<=a`, enlarge this to the decreasing majorant

\[
\gamma_m=1-\exp[-C_b(1+m)^{-b}].
\tag{1.1}
\]

This is precisely the ratio hypothesis (4.1) of Bressaud--Fernandez--Galves (BFG), not an application of their Theorem 1 to an observable outside its printed `V_phi` class.

BFG Proposition 1 constructs a coupling and the matched-suffix length `T_n`; its Lemma 1 compares `T_n` with the auxiliary Markov chain `S_n` having transitions

\[
i\to i+1\text{ with probability }1-\gamma_i,
\qquad i\to0\text{ with probability }\gamma_i.
\]

For an arbitrary continuous `F`, their equation (5.4) is the elementary coupling inequality

\[
|\mathcal L_s^nF(x)-\mathcal L_s^nF(y)|
\le \sum_{k\ge0}\operatorname{var}_k(F)\,P(T_n=k).
\tag{1.2}
\]

Repeating only the monotonicity step in their equation (5.5) gives

\[
\sum_{k\ge0}\operatorname{var}_k(F)P(T_n=k)
\le \sum_{k=0}^n\operatorname{var}_k(F)u_{n-k},
\qquad u_j:=P(S_j=0).
\tag{1.3}
\]

Let `tau` be the first positive return of `S` to zero.  BFG equations (5.7) and (5.11) state

\[
u_n=\sum_{k=1}^nf_k u_{n-k},
\qquad
f_1=\gamma_0,
\qquad
f_k=\gamma_{k-1}\prod_{j=0}^{k-2}(1-\gamma_j)\quad(k\ge2).
\tag{1.4}
\]

Since `b>1`, `sum gamma_j<infinity`; hence the product in (1.4) is bounded above and below by positive constants.  Therefore

\[
f_k\asymp(1+k)^{-b}.
\tag{1.5}
\]

For `F in B_b`, including the harmless `k=0` term,

\[
\operatorname{var}_k(F)\le C_b\|F\|_b f_{k+1}.
\tag{1.6}
\]

Substituting (1.6) into (1.3) and using the renewal equation (1.4) gives

\[
|\mathcal L_s^nF(x)-\mathcal L_s^nF(y)|
\le C_b\|F\|_b u_n.
\tag{1.7}
\]

Finally, BFG Proposition 2(iv) gives `u_n=O(gamma_n)` when `gamma_n` decreases polynomially.  The explicit sequence (1.1) is monotone and asymptotic to `C_b n^{-b}`, so

\[
\boxed{
\operatorname{osc}(\mathcal L_s^nF)
\le C_b\|F\|_b(1+n)^{-b}.}
\tag{1.8}
\]

This is the exact source bridge needed later.  No claim is made that BFG's displayed norm `||F||_phi` already equals `||F||_b`.

Primary pins: BFG ratio condition (4.1), printed pp. 4--5; maximal coupling and suffix process, pp. 5--8; equations (5.4)--(5.11), pp. 8--9; Proposition 2(iv), pp. 12--13.  Primary text: arXiv `math/9806132`.

## 2. Why the Poisson loss is one power

Assume two initial histories agree through memory `m`, and let `sigma` be the first generated mismatch.  Before time `r`, the coupled histories agree through `m+r`, so the same ratio bound at the full DPP exponent `a` gives

\[
P(\sigma=r)\le C(1+m+r)^{-a}.
\tag{2.1}
\]

If `sigma>=n`, the terminal histories agree through `m+n`, contributing at most `var_{m+n}F`.  If `sigma=r<n`, then after conditioning on the two histories just after the mismatch, the difference of the remaining marginal expectations is bounded by

\[
\operatorname{osc}(\mathcal L_s^{n-r-1}F),
\]

which is controlled by (1.8).  Thus

\[
\operatorname{var}_m(\mathcal L_s^nF)
\le C\|F\|_b\left[(1+m+n)^{-b}
+\sum_{r=0}^{n-1}(1+m+r)^{-a}(1+n-r)^{-b}\right].
\tag{2.2}
\]

Both exponents are summable because `a>=b>1`.  Summing (2.2) in `n` and exchanging the nonnegative double sum gives

\[
\begin{aligned}
\sum_{n\ge0}\operatorname{var}_m(\mathcal L_s^nF)
&\le C\|F\|_b\left[(1+m)^{1-b}
+\left(\sum_{r\ge0}(1+m+r)^{-a}\right)
 \left(\sum_{l\ge1}(1+l)^{-b}\right)\right]\\
&\le C_b\|F\|_b(1+m)^{1-b}.
\end{aligned}
\tag{2.3}
\]

Together with the sup-norm relaxation sum, this proves

\[
\boxed{
\mathcal R_s=\sum_{n\ge0}\mathcal L_s^n\Pi_s:
\mathcal B_b\to\mathcal B_{b-1}}
\quad(b>1).
\tag{2.4}
\]

The earlier two-power bound remains true but was an artifact of replacing the time-resolved sum (2.1) by the probability of at least one mismatch before time `n`.

## 3. Difference-quotient response audit

For nearby parameters `u,s`, stationarity and `(I-L_s)R_s=Pi_s` give the exact identity

\[
(\nu_u-\nu_s)(F)
=\nu_u(\mathcal L_u-\mathcal L_s)\mathcal R_sF.
\tag{3.1}
\]

Let

\[
B_h=\frac{\mathcal L_{s+h}-\mathcal L_s}{h}
=A_{1,s}+\frac h2A_{2,s}+o(h)
\tag{3.2}
\]

on every `B_b`, `b<=a`.  Dividing (3.1) by `h` gives

\[
D\nu_s(F)=\nu_s(A_{1,s}R_sF).
\tag{3.3}
\]

For the second derivative, expand

\[
\frac{(\nu_{s+h}-\nu_s)(F)-h\nu_s(A_1R_sF)}{h^2/2}
=
u_{s+h}(A_2R_sF)
+\frac{2}{h}(\nu_{s+h}-\nu_s)(A_1R_sF)+o(1).
\tag{3.4}
\]

Apply (3.1) again to the fixed observable `A_1R_sF`.  The chain of spaces is

\[
F\in B_a
\xrightarrow{R_s}B_{a-1}
\xrightarrow{A_1}B_{a-1}
\xrightarrow{R_s}B_{a-2}.
\tag{3.5}
\]

The second inverse is legitimate exactly when `a-1>1`, i.e. `a>2`.  Taking the limit in (3.4) gives

\[
D^2\nu_s(F)=
\nu_s(A_{2,s}R_sF)
+2\nu_s(A_{1,s}R_s(A_{1,s}R_sF)).
\tag{3.6}
\]

For a moving `F_s`, ordinary differentiation adds

\[
\nu_s(F_s'')+2\nu_s(A_{1,s}R_sF_s').
\tag{3.7}
\]

No derivative of `R_s` is assumed; (3.1) is what generates the nested Poisson term.

Continuity follows from three explicit facts: the correlation series is uniformly summable in sup norm for every exponent above one; `R_s` is uniformly bounded in the one-power-weaker space; and sup convergence plus a common `B_c` bound implies convergence in every `B_{c-eta}`.  Choosing the total interpolation loss below `a-2` leaves the second Poisson input exponent above one.

## 4. Entropy and parity audit

At `t=0`, the half-period-even center has only even Fourier differences, so the two parity sublattices are independent.  For every `t`, the restriction of `K_t` to either parity sublattice is unchanged because `g` has no even Fourier coefficient.  The zero-parameter future conditional at the origin therefore depends only on the origin-parity coordinates, and

\[
\nu_{t^2}(\ell_0)=\nu_0(\ell_0).
\tag{4.1}
\]

The stationary entropy-rate identity uses the full one-sided complete-event conditional:

\[
h_s=-\nu_s(\ell_s).
\tag{4.2}
\]

Thus the exact deficit is

\[
D(s)=h_0-h_s=\nu_s(\ell_s-\ell_0).
\tag{4.3}
\]

At `s=0` the moving observable vanishes.  Its first derivative is

\[
D'(0)=\nu_0(\ell'_0).
\]

Normalization gives pointwise

\[
L_0\ell'_0=\sum_\xi G_0(\xi|x)\frac{G'_0(\xi|x)}{G_0(\xi|x)}
=\sum_\xi G'_0(\xi|x)=0,
\]

hence `D'(0)=0`.  The response lemma gives `D in C^2` in `s`, so

\[
D(s)=As^2+o(s^2).
\tag{4.4}
\]

The accepted PR53 matching inequality gives `A>=2 alpha_k`.  Therefore

\[
h''(t)=-2D'(t^2)-4t^2D''(t^2)
=-12At^2+o(t^2),
\]

and

\[
(h(t)+\alpha_k t^4)''
=-12(A-\alpha_k)t^2+o(t^2)<0
\]

for all sufficiently small nonzero `t`.  The second derivative is zero at the center, so the corrected true entropy rate is concave on a smaller symmetric interval.

## 5. Boundary correction and exact status

The claim in `c4_response_p4_repair.md` that the stationary second response of the frozen-future kernel converges at the raw kernel rate `O(N^{b-a})` was not proved and is withdrawn by `c4_response_p4_boundary_correction.md`.

What is proved uniformly is a finite **time-correlation/Poisson cutoff**: for every `0<eta<a-2`, all terms of the second response formula are approximated by sums of times below `N` with scalar error

\[
O(N^{-eta}).
\tag{5.1}
\]

This is sufficient to make the response formulas and their remainders checkable at every `p>4`; it is not a claim about a finite-window entropy Hessian or a frozen-memory stationary law.

Current author verdict:

- original PR66 `p>4` theorem: **PROVED by the new finite-response route, PENDING_REVIEW**;
- old Dobrushin A1/A2 import: still invalid and unused;
- internal complete-event inverse/two-leg input: used only in its previously reviewed conditional scope;
- independent FIRST/SECOND, machine recomputation and novelty: not claimed.