# D10-S7 author verdict

STATUS: `CORRECT` for the stated closed-ball certificate.
GENERAL GLOBAL QUESTION: INCOMPLETE. FINITE COMPUTATION: SCOUT/SANITY ONLY.

The S5 existential full-Hessian neighborhood has an explicit candidate radius:

    delta = 36163/16056110400
          approximately 2.25228894788864929578461294088e-6.

The proposed theorem covers the entire closed Frobenius ball around the given
rational K_*. Every symmetric K in this ball is automatically strict, all
eight exact probabilities are at least 87/2500, and for every symmetric D,

    H''_K[D,D] <= -(43/100)||D||_F^2.

No commutation, PSD/NSD, rank, or direction-normalization assumption is needed.
The base matrix remains genuinely connected and heterogeneous on this ball.
The radius is very conservative, not an approximation to the maximal region.

The proof rederives the signed exact-event determinant from Mobius inversion,
uses its operator norm <=1 for strict kernels, counts mixed column replacements
as 3,6,6, and bounds the third derivative of -p log p. A rational bound
|1+log p|<=3 yields L=160561104/841. The three radius restrictions separately
protect strictness, the atom floor, and half of the verified base curvature
margin. The integration is in the Frobenius geometry and is uniform over all
directions; no six-coordinate norm is silently substituted.

The finite sanity script checked the constants exactly, reconstructed the
eight base atoms/eigenvalues, and compared Mobius versus signed-determinant
mixed jets at 12 rational perturbed kernels and 4 directions each. All 384
event-jet checks passed. Decimal curvature checks were only supplementary.
They are not the justification for coverage of the continuous ball.

The only non-elementary supplied premise is S5's already verified base
full-Hessian bound. A fresh non-author implementation independently checked
the determinant/Mobius semantics, derivative factorials, `3/6/6` replacement
counts, absolute `f'` bound, strictness-before-integration order, eight-event
factor, Frobenius geometry, and the closed-ball/all-directions quantifiers. It
also checked 84 mixed-jet cases / 672 event jets with no failures.

No global concavity, optimal radius, or novelty certification is claimed. The
result is an explicit local certificate built from previously verified base
data and elementary uniform estimates.
