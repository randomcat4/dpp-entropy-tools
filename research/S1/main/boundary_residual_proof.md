# Extreme-past kernel enclosure by a rational residual

Status: author proof, independent review pending. Scope is the frozen uniformly interior finite-degree symbol; no entropy sign is yet claimed.

Let the past coordinates be -1,-2,... and future coordinates 0,1,... . Write T for the half-line compression of K_f to the past, B for its past-to-future block, and C for the future block. The uniform symbol margin gives T>=epsilon I by the Fourier quadratic-form identity. Degree m implies that B is supported on its first m rows and m columns.

Conditioning on successively longer all-one pasts converges to the kernel

    C_infinity=C-B* T^(-1) B.

This follows either from the finite DPP inclusion Schur complement and convergence of the uniformly coercive Galerkin problems, or by the following direct residual argument. The bounded, positive, invertible T has a unique solution Y=T^(-1)B. Finite supported vectors are dense in the energy norm since epsilon I<=T<=I. Their Galerkin minimizers therefore converge in norm to Y. Each finite Schur complement is the corresponding conditioned kernel, and its finite minors converge to those of the displayed limit.

Choose any finitely supported matrix X with rational real and imaginary parts, and zero-extend it to the half-line. Set R=B-TX. All entries of R can be checked exactly: only the first M+m rows can be nonzero when X has M rows. Then

    Y-X=T^(-1)R,
    ||Y-X||_op <= ||R||_F/epsilon.

Let A=C-sym(B*X), where sym(Q)=(Q+Q*)/2. Because B*Y is Hermitian,

    ||A-C_infinity||_op
      <= ||B||_F ||R||_F/epsilon =: delta.

The script replaces both Frobenius norms by the sum of the absolute real and imaginary parts of all entries, giving a coarser rational upper bound. This does not rely on the precision, convergence, or correctness of the numerical solver that proposed X. The rational residual checks the proposed X afterward. The error and the correction are confined to the first m future coordinates and are independent of the window length.

The finite and infinite all-one conditioned kernels retain the spectral margin: minimizing the quadratic form of the full kernel over past coordinates gives a Schur complement >=epsilon I, and subtraction of a positive term leaves it <=C<=(1-epsilon)I. Applying the same construction to 1-f and then complementing gives the all-zero conditioned kernel.

The output contains the rational X, exact residual bound, rational m-by-m corner of A, and delta for f_0, f_tau and their complements. Endpoint f_-tau follows by conjugation, but no duplicate calculation is counted. To certify an entropy-rate sign, these kernel enclosures still need outward error propagation through the finite conditional probabilities and their binary entropies; that obligation is not hidden in this result.
