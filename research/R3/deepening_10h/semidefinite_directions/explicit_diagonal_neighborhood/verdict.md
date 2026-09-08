# D10-S6 author verdict

STATUS: CORRECT_AFTER_INDEPENDENT_REVIEW.

The candidate replaces the existential radius in D10-S4 by a closed formula
`delta_{n,a,b}>0`.  Inside that Frobenius ball around the compact diagonal box,
every nonzero PSD or NSD direction has entropy curvature at most
`-2||D||_F^2/n`.

The proof uses an exact-event atom floor, column-multilinearity bounds for the
first three determinant derivatives, a third-derivative Lipschitz estimate for
the entropy Hessian, and the diagonal PSD trace inequality.  It deliberately
uses no empirical coverage claim.

The constant is very conservative and the general PSD/NSD question remains
open. A fresh non-author audit independently checked the determinant
mixed-derivative counts, chain-rule coefficients, atom-floor segment argument,
and `sum D_ii^2 >= ||D||_F^2/n` for singular PSD matrices; its exact small-
dimension sanity artifacts are frozen under `verifications/`.
