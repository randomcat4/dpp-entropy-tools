# D10-U10j freeze

STATUS: PROOF CANDIDATE PENDING INDEPENDENT AUDIT.
GLOBAL PATH: INCOMPLETE. No author-side CORRECT claim.

The new proposed bound is universal in beta, under explicit smallness
conditions: there exist c,C,x0>0 such that, whenever 0<x<x0,
R=2+beta+1/beta, xR^6<=c and exp(-beta/x)<=x^2,

|sigma-phi|<=C sqrt(x)R^6.

All R powers are traced in [proof_candidate.md](proof_candidate.md), including
coercivity, the minimizing direction, the inverse constraint matrix, and
the final cofactor energy error. The constants are existential, not numerical
threshold certificates. This is not extrapolated from U10i's compact-beta
big-O statement.

Consequently, for each fixed 0<theta<1/12, a sufficiently small-x continuous
region x^theta<=beta<=x^(-theta) is proposed to have negative full Sym(3)
entropy Hessian. Theta=1/24 gives an O(x^(1/4)) absolute error in sigma.
This covers some beta->0 and beta->infinity regimes, including all fixed
logarithmic powers and their reciprocals.

Faster noncompact drifts, including beta=p x log(1/x) corresponding to s=x^p,
remain OPEN in this proof. The cutoff 1/12 is only a conservative bound
from the estimate, not an asserted transition or counterexample threshold.

The standard-library [sanity.py](sanity.py) and [sanity.json](sanity.json)
check exact exponent bookkeeping and 18 rate examples only. No new Hessian
grid was run and no rate example establishes the theorem.

Review priorities: universal versus beta-dependent constants, the use of
det(N)/lambda_max(N)^2>=c/R, refined minimizer norm O(R), and the finite
order of shrinking the smallness constant to avoid circularity.
