# Mathematical/source FIRST report

## Status

`CORRECT_WITHIN_SCOPE`.

The new multiscale lemma closes the optional quantitative frozen-memory response question for every `p>4` without reviving the withdrawn raw stationary truncation rate.  No critical mathematical gap was identified.  Two local clarifications are recommended below; neither changes the DPP entropy specialization or the stated exponent.

## 1. Canonical freezing and uniformity

The approximant is correctly defined by freezing the future in the normalized complete-event kernel,

\[
G_{s,N}(\xi\mid x)=G_s(\xi\mid x_1,\ldots,x_N,0,0,\ldots).
\]

It is a finite-memory conditional chain, not a finite-section DPP.  This distinction is maintained throughout the source.

The asserted uniform `B_a` control of the frozen family is valid.  If `T_Nx=(x_1,\ldots,x_N,0,\ldots)`, then for `m<N`, agreement of `x,y` through coordinate `m` implies agreement of `T_Nx,T_Ny` through `m`, while for `m>=N` the two frozen images are identical.  Thus

\[
\operatorname{var}_m(F\circ T_N)\le \operatorname{var}_m(F)\quad(m<N),
\qquad
\operatorname{var}_m(F\circ T_N)=0\quad(m\ge N).
\]

The common complete-event disk transfers this observation to the required parameter derivatives, and non-nullness is uniform.  Therefore the prior BFG/first-disagreement relaxation, one-power Poisson estimate, and boundary time-tail proof do apply with constants independent of `N`.

## 2. Spatial operator and invariant-law comparison

The `C(X)` operator estimate

\[
\delta_N=\max_{0\le j\le2}\|\partial_s^j(L_{s,N}-L_s)\|_{\infty\to\infty}
=O(N^{-a})
\]

follows from the differentiated complete-event conditional estimate and uniform non-nullness.  The finite-time telescope gives `n delta_N`, with no hidden strong-space inverse.

The invariant-law identity has the correct orientation:

\[
(\nu_{s,N}-\nu_s)H
=\nu_{s,N}(L_{s,N}-L_s)R_sH.
\]

Since `R_s:B_b->B_{b-1}` and `b>1`, this yields the stated `O(delta_N)` weak comparison on `B_b`; total-variation convergence is neither used nor claimed.

## 3. First truncated response

Termwise comparison of the two length-`M` Poisson sums contributes `O(delta_N(1+n))` at time `n`.  Summing gives `O(delta_N M^2)`.  Applying the invariant-law comparison to the unperturbed `B_{a-1}` integrand adds no larger term.  Thus the first-response finite algebra is correctly bounded by `O(delta_N M^2)`.

## 4. Nested second response

For

\[
Y_s^{<M}=A_{1,s}R_s^{<M}F_s,
\]

the proof uses both estimates that are needed:

- `||Y_N-Y||_infinity=O(delta_N M^2)`;
- a uniform `B_{a-1}` bound, alongside the crude `B_a` bound `O(M)`.

The outer truncated Poisson operator has sup norm at most `2M`, so changing its input costs `O(delta_N M^3)`.  For the same input, the operator telescope costs only `O(delta_N M^2)` because the sharper `B_{a-1}` bound controls the sup norm, while the centering comparison uses the `B_a=O(M)` bound.  The final invariant expectation has a sufficient `B_a=O(M^2)` bound.  Consequently the nested term is indeed

\[
O(\delta_NM^3),
\]

and the non-nested `A_2R` and moving-observable Leibniz terms are no worse.  No third strong-space Poisson inverse is smuggled into the argument.

## 5. Time tails and balancing

The previously proved one-power boundary cutoff is uniform over the full and frozen families by the norm-contraction observation in Section 1.  Restoring the infinite correlation sums therefore contributes

\[
O(M^{-\eta}),\qquad 0<\eta<a-2.
\]

Together with `delta_N=O(N^{-a})`, this gives

\[
O\!\left(M^{-\eta}+N^{-a}M^3\right).
\]

Balancing with `M=floor(N^{a/(3+eta)})` is correct for sufficiently large `N` and yields `N^{-a eta/(3+eta)}`.  The exponent is increasing in `eta`; because `eta<a-2` is strict, the proof obtains every exponent strictly below

\[
\frac{a(a-2)}{a+1},
\]

not the endpoint itself.  The source states this quantifier correctly and makes no optimality claim.

## 6. Local clarifications

### LC1 — abstract moving-observable notation

In the general moving-observable formulation, (1.4) gives an observable truncation error `O(N^{-a})`, whereas `delta_N` is defined only from transfer-operator differences.  The proof occasionally writes the combined error as `C_F delta_N`.  For a completely arbitrary moving observable, the literal implication `O(N^{-a})=O(delta_N)` need not follow from the displayed upper bound on `delta_N`.

The local repair is to set

\[
\varepsilon_N:=\delta_N+max_{0\le j\le2}
\|\partial_s^j(F_{s,N}-F_s)\|_\infty=O(N^{-a})
\]

and replace `delta_N` by `epsilon_N` in estimates involving a changed observable.  Every power count and the final rate are unchanged.  In the entropy specialization `F=log G`, common non-nullness and the binary normalized kernel identify the log-observable error with the corresponding kernel/operator errors, so the displayed shorthand can also be justified directly there.

Severity: non-blocking local clarification; no change to the DPP entropy conclusion.

### LC2 — README spectral-margin quantifier

The rewritten README says `delta<=c<=1-delta` without explicitly declaring `delta>0`.  It should say “for some `0<delta<1/2`” (or restore the equivalent strict-margin wording).  The mathematical packet consistently uses strict non-nullness, so this is a theorem-statement edit rather than a proof defect.

Severity: non-blocking static clarification.

## Final scoped conclusion

At frozen head `290a84064eaae2e857d637f58531e95f4ca3cb3b`, the new multiscale source correctly proves canonical frozen-memory response convergence through order two for every `p>4`, with the strict family of polynomial exponents stated above.  It does not prove a finite-section DPP identity, a finite-window curvature sign, an endpoint rate, or any result at `p<=4`.
