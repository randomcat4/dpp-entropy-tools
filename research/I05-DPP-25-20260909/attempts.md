# Attempts, failures, and remaining threshold questions

This ledger records routes that were tested but are not used as substitutes for the theorem proof. A failed sufficient condition, a finite-window observation, or a smooth approximation without uniform response does not count as a counterexample to the entropy-rate statement.

## 1. Finite-window curvature extrapolation — rejected

For a finite block, the complete configuration entropy is

\[
H_n(f)=-\sum_{x\in\{0,1\}^n}p_f(x)\log p_f(x),
\qquad
p_f(x)=(-1)^{|Z_x|}\det(T_n(f)-I_{Z_x}).
\]

Even exact curvature signs for several values of `n` do not give the sign of the entropy-rate curvature. A proof would need a common parameter interval and a volume-uniform bound on the differentiated conditional-entropy tail. No finite-window computation is used here.

## 2. Spectral entropy or fermionic von Neumann entropy — rejected

The scalar integral

\[
\int_{\mathbb T}\bigl[-f\log f-(1-f)\log(1-f)\bigr]
\]

and the entropy of the associated quasi-free fermionic state are not the classical configuration Shannon entropy rate of the DPP. Spectral rotations preserve eigenvalues but not the configuration law. Neither object is substituted for `h(f)`.

## 3. Bare smooth approximation — disproved as a mechanism

Approximating `c,g` by trigonometric polynomials or exponentially decaying symbols and applying the accepted PR53 theorem gives approximant-dependent intervals. Entropy-value convergence alone does not prevent those intervals from shrinking to zero.

The entire functions

\[
F_N(t)=t^4+N^{-2}e^{-N^2t^2}
\]

converge uniformly to `t^4`, while each is strictly concave on `|t|\le(2N)^{-1}` for `N\ge2`; the limit is not concave on any neighborhood of zero. The calculation is given in `route_comparison_and_obstruction.md`.

This disproves only the inference

\[
\text{uniform value convergence + some local interval for each approximant}
\Longrightarrow
\text{a local interval for the limit}.
\]

It is not a DPP entropy-rate counterexample.

## 4. Centered quartic deficit alone — rejected

The matching/negative-association argument proves a lower bound

\[
h(c)-h(c+tg)\ge C t^4+O(t^6)
\]

once a response expansion is available. A pointwise lower bound at the center does not control the sign of the second derivative at nearby nonzero parameters. It cannot by itself establish local concavity.

## 5. Direct negative-association midpoint inequality — unresolved

Negative association controls selected increasing events and yields the accepted matching lower bound. It does not presently compare the full configuration entropies at three arbitrary parameters `t_1,(t_1+t_2)/2,t_2`. No valid direct Jensen inequality for the true entropy rate was found. This route remains open rather than disproved.

## 6. Generic inverse-closedness theorem alone — insufficient

Jaffard- and Wiener-type inverse localization theorems support the expected polynomial decay of inverses, but the proof needs one constant valid simultaneously for

- every finite conditioning window;
- every complete-event diagonal pattern `I_Z`;
- every parameter in a common complex disk.

A theorem for one fixed infinite matrix does not automatically provide this family-uniform statement. The packet therefore includes a direct finite-section band-truncation/Neumann proof.

## 7. Cassandro–Olivieri as the sole general-spin citation — rejected

Cassandro and Olivieri give a finite-first-moment many-body analyticity theorem and a transparent decimation proof of Dobrushin's result. The article's concrete formulation is in lattice-gas interaction coordinates. Expanding an arbitrary binary block function into monomials can cost an exponential coefficient norm, so no uncontrolled basis conversion is inserted here.

The load-bearing imported result is instead Dobrushin's general one-dimensional classical lattice-system theorem, which states analytic dependence of the specific free energy and correlations on a power-law-decaying potential. Cassandro–Olivieri is retained as an independent finite-first-moment/complex-parameter mechanism check, not as the sole justification for arbitrary interval functions.

## 8. Why the present proof stops at `p>4`

The direct inverse estimate chooses a localization exponent `q` satisfying

\[
p>2q+1.
\]

The deliberately convention-independent interaction moment bound requires

\[
q>\frac32.
\]

These inequalities have a simultaneous solution exactly when `p>4`. This is a proved sufficient threshold, not a claimed sharp threshold.

A sharper inverse theorem with family-uniform constants, or a pressure theorem requiring only the orbit-normalized first moment, may lower the threshold. Such an improvement must still preserve a common complex response disk; ordinary entropy continuity is not enough.

## 9. Summable Fourier coefficients and arbitrary measurable symbols — open here

For the unweighted Wiener class, and a fortiori for arbitrary measurable symbols with a strict spectral margin, the present argument does not produce an exponent `q>3/2` for the two-leg conditional influence. The precise missing estimate is one of the following equivalent-strength replacements:

1. a window/configuration-uniform complete-event inverse localization strong enough that the single-coordinate influence sequence has finite second moment in the interval-interaction counting convention;
2. a common complex parameter disk with uniform fourth-response bounds for the true entropy rate;
3. a common finite-Jensen interval obtained by a direct variational or negative-dependence argument.

No genuine three-symbol entropy-rate counterexample is claimed. Producing one would require rigorous upper and lower bounds for three fixed infinite-volume entropy rates, not finite-window extrapolation.

## 10. Computation ledger

No numerical computation, interval arithmetic, symbolic elimination, or enumeration was required. There was therefore no task exceeding the delegation threshold and no Codex/local-agent computation was opened.
