# I05-DPP-25 — polynomial regularity threshold for Lyons entropy-rate local concavity

## Status

**PROVED (author proof; not independently reviewed).**

This packet is based on frozen `main@9dcb6e9079ca57f94e0e30d63161cda89ca61fae` and uses the accepted PR53 theorem packet only where explicitly stated. It does not use the unreviewed PR59 as a proof input.

The new result replaces exponential Fourier decay by the polynomially weighted Wiener condition

\[
\sum_{m\in\mathbb Z}(1+|m|)^p\,|\widehat u(m)|<\infty,
\qquad p>4.
\]

For a strict-margin half-period-even center `c` and any nonzero half-period-odd direction `g` in this class, the same quartic correction as in accepted PR53 gives a nonempty local concavity interval for the true stationary DPP configuration entropy rate. Real symbols need not be even; complex Hermitian Toeplitz kernels are included.

The proof is independent of the exponential Hölder/Ruelle–Perron–Frobenius route. Its bridge is

\[
\text{polynomial Fourier tails}
\Longrightarrow
\text{uniform polynomial localization of every complete-event inverse}
\Longrightarrow
\text{squared remote-coordinate influence}
\Longrightarrow
\text{finite-first-moment 1D interaction}
\Longrightarrow
\text{Dobrushin analyticity for general 1D classical systems}.
\]

The DPP is identified with the equilibrium state by an exact conditional cross-entropy variational argument. The accepted PR53 matching/negative-association estimate is reused only after analytic response has been established, to obtain the strictly positive quartic coefficient floor.

## Frozen theorem

See [`frozen_statement.md`](frozen_statement.md). The coefficient is

\[
\alpha_k=\frac{|\widehat g(k)|^4}{8\mu^2(1-\mu^2)},
\qquad \mu=\widehat c(0),
\]

for any odd `k` with `\widehat g(k)\ne0`.

## Proof packet

- [`proof.md`](proof.md): complete-event localization, one-sided conditional influence, finite-first-moment interaction, Dobrushin response input, and curvature conclusion.
- [`equilibrium_bridge.md`](equilibrium_bridge.md): exact conditional cross-entropy/pressure identification and sign audit.
- [`route_comparison_and_obstruction.md`](route_comparison_and_obstruction.md): comparison of three structurally different routes and a rigorous scalar counterexample to the bare smooth-approximation mechanism.
- [`sources.md`](sources.md): primary-source bridge and exact scope of each citation.
- [`verification.md`](verification.md): algebra, constants, quantifiers, and failure-mode checks.
- [`attempts.md`](attempts.md): rejected or incomplete routes, the `p>4` threshold origin, and remaining lower-regularity gaps.

## Scope separation

This is not the I05-21/PR59 “fixed exponential regularity class on a prescribed compact parameter tube” line. The present result changes the regularity class itself and proves an existential nonempty local interval for each fixed pair `c,g`.

The theorem strictly extends the accepted exponential class: `frozen_statement.md` gives explicit strict-margin power-law symbols in `\mathcal A_p` that lie in no exponentially weighted Wiener class.

The packet does not claim the threshold `p>4` is sharp, and it does not prove the theorem for the unweighted Wiener class or arbitrary measurable symbols. `attempts.md` records the exact missing uniform estimate in those classes.

## Computation and code

No numerical computation, interval arithmetic, enumeration, or code is used. Consequently there are no numerical inputs, floating-point errors, or computational certificates.

## Literature-scope audit

The load-bearing imported response result is Dobrushin's theorem for general one-dimensional classical lattice systems with power-law-decaying/finite-first-moment interactions. Cassandro–Olivieri is used as an independent finite-first-moment decimation and complex-parameter mechanism check, not as the sole citation for arbitrary block-function interactions.

The constructed interaction satisfies the stronger unnormalized bound

\[
\sum_{A\ni0}\operatorname{diam}(A)\,\|U_A\|_\infty<\infty,
\]

so it lies inside standard finite-first-moment conventions with or without orbit normalization. Independent review should audit this imported theorem application and the complete-event inverse localization. Author self-check is not counted as independent acceptance.
