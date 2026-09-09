# I05-DPP-25 — polynomial regularity threshold for Lyons entropy-rate local concavity

## Status

**PROVED (author proof; not independently reviewed).**

This packet is based on frozen `main@9dcb6e9079ca57f94e0e30d63161cda89ca61fae` and uses the accepted PR53 theorem packet as an input only where explicitly stated. It does not use the unreviewed PR59 as a proof input.

The new result replaces exponential Fourier decay by an explicit polynomially weighted Wiener condition:

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
\text{Dobrushin--Cassandro--Olivieri analyticity}.
\]

The matching/negative-association lower bound from accepted PR53 is then reused only to identify a strictly positive quartic coefficient floor.

## Frozen theorem

See [`frozen_statement.md`](frozen_statement.md). The coefficient is

\[
\alpha_k=\frac{|\widehat g(k)|^4}{8\mu^2(1-\mu^2)},
\qquad \mu=\widehat c(0),
\]

for any odd `k` with `\widehat g(k)\ne0`.

## Proof packet

- [`proof.md`](proof.md): complete-event localization, one-sided conditional influence, interaction construction, analyticity, and curvature conclusion.
- [`route_comparison_and_obstruction.md`](route_comparison_and_obstruction.md): comparison of three structurally different routes and a rigorous scalar counterexample to the bare smooth-approximation mechanism.
- [`sources.md`](sources.md): primary-source bridge and exact scope of each citation.
- [`verification.md`](verification.md): algebra, constants, quantifiers, and failure-mode checks.
- [`attempts.md`](attempts.md): rejected or incomplete routes and why they do not prove the theorem.

## Scope separation

This is not the I05-21/PR59 “fixed exponential regularity class on a prescribed compact parameter tube” line. The present result changes the regularity class itself and proves only an existential nonempty local interval, exactly as frozen below.

## Computation and code

No numerical computation, interval arithmetic, enumeration, or code is used. Consequently there are no numerical inputs, floating-point errors, or computational certificates. All estimates are symbolic and dimension-uniform.

## Review state

The proof invokes the one-dimensional finite-first-moment analyticity theorem of Dobrushin and of Cassandro–Olivieri in an explicitly stated Banach-neighborhood form. The interaction constructed here satisfies the stronger unnormalized bound

\[
\sum_{A\ni0}\operatorname{diam}(A)\,\|U_A\|_\infty<\infty,
\]

so it is inside the usual finite-first-moment conventions with or without orbit normalization. Independent review should audit that imported theorem invocation and the chain-to-interaction identification; no self-review is counted as independent acceptance.
