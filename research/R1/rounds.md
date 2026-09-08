# R1 rounds

## Round 0: setup and calibration

Status: RUNNING.

Public checkout branch: `research/R1`.

Initial components:

- `param_opt/`: bounded full-Hessian spectral parameter search over
  `n=3,...,10`.
- `prob_deriv/`: independent exact-event and directional-derivative reference.
- `certificate/`: exact rational chord verifier for a JSON candidate.

The first required tests are derivative calibration against finite differences,
exact event probability identities, and strict rejection of complex-direction
certificates as out of scope.

## Round 1: independent formula and optimizer lanes

Status: INCOMPLETE/NO_HIT finite evidence.

The probability/derivative lane completed an independent implementation check
for n=2,...,5. It verified exact inclusion-exclusion event probabilities
against the L-ensemble formula on a rational 3 by 3 kernel, checked
finite-difference first and second entropy derivatives, and confirmed
`sum p'_S=sum p''_S=0` to floating precision. Largest reported Hessian
finite-difference error was below `1e-7` in the main n=2,...,5 table.

The optimization lane completed two bounded batches over n=3,...,10:

```text
batch01: 4,960 objective calls, seed 202609081, positive > 1e-6: 0
batch02: 8,242 objective calls, seed 202609082, positive > 1e-6: 0
```

The best reported value was `-6.245093781582534e-15` at n=3, with direct
midpoint gap `-3.960165528837933e-12`. This is a near-flat negative object, not
a counterexample.

## Round 2: strict certificate tool

Status: IMPLEMENTED, with no positive candidate supplied.

The corrected rational verifier checks strict endpoint feasibility by exact
Sylvester minors, rebuilds every exact DPP event probability, and bounds the
entropy gap using rational logarithm intervals. Its three bounded tests return:

```text
negative feasible chord -> CERTIFIED_NEGATIVE_GAP
zero direction          -> GAP_UNCERTAIN
infeasible endpoint     -> NOT_FEASIBLE
```

An earlier exploratory scope deviation produced extra scout files in the work
tree. They are deliberately excluded from the committed search denominator and
result claims.

## Round 3: structured diagonal-center family

Status: VERIFIED_FOR_FAMILY.

The diagonal-center Hessian proof gives, for every diagonal strict contraction
K and every real symmetric direction V,

```text
D^2 H(K)[V,V] = - sum_i V_ii^2/(p_i(1-p_i)) <= 0.
```

An independent proof shows the stronger finite-chord statement: every
nontrivial feasible real-symmetric chord centered at a diagonal strict
contraction has strictly negative midpoint gap. The first pre-freeze wording
omitted `t>0`; the `t=0` equality counterexample and the repaired frozen
statement are both retained.

Both frozen statements and proofs were fixed in commit
`a49051d2f768ec2b926a2e4d68d5286b054f9656`. Reviewers who did not author the
respective proofs read the committed blobs via `git show`; both returned
`STATUS: CORRECT`. The reviews record the commit and Git blob IDs.

The GitHub smart-HTTPS endpoint was unavailable during result publication, so
the exact frozen tree was transported through the Git data API. Public commit
`8ae16152670e768acc4bd5792b5db71822c42c86` and the locally reviewed freeze
commit have the same tree hash `c282e54a8221dc8546b5c8da3c23a768038b9025`;
the mathematical blob IDs are unchanged.

## Round 4: margin-stratified search, block theorem, and boundary stress

Status: VERIFIED_FOR_AN_ADDITIONAL_FAMILY / FINITE_NO_HIT.

The second-stage search stratified kernels by their actual minimum distance to
the spectral boundary: `(0.2,0.4)`, `(0.05,0.2)`, `(0.01,0.05)`, and
`(0.001,0.01)`. Across `n=3,...,10`, 64 restarts completed 42,578 formal
objective calls with zero formal failures and zero values above `1e-6`.
Another 823 validation attempts include two retained pre-stabilization
failures. The formal SQLite ledger has unique contiguous IDs `1,...,42578`,
all `OK`, and the process exited 0.

Direct floating Mobius inversion was unstable for a rare event in a
high-occupancy self-test. The corrected pipeline evaluates the complement
kernel `I-K`, still using inclusion determinants followed by Boolean Mobius
inversion, maps events back by complementation, reverses first-direction signs,
and preserves second-direction signs. Complement, entropy, derivative, mass,
finite-difference, checkpoint, and optimizer smoke tests passed. The failed
pre-stabilization attempt remains in the denominator.

The best second-stage Hessian value was `5.930937647366978e-15`, comparable to
its `6.0037609269151225e-15` eigen residual and far below the promotion gate.
The recorded feasible chord gaps were `-1.138755756358023e-12` and
`-2.9154478831117103e-10`; no object was promoted.

The block-cross theorem was frozen in commit
`64c5bc0910c10c8baba1208326c799c0d0dffeec`, tree
`8b75d4f4b5739a3e89fb9fef65d1ce83dc003ed8`. A non-author reviewer read the
fixed blobs and returned `STATUS: CORRECT`. Exact-rational n=3 and n=4 sanity
examples preserved block marginals and gave negative midpoint gaps.

The phase-1 rational verifier also passed a fixed near-boundary stress suite.
It certified negative cases with minimum complete-event probabilities `1e-8`
and `1e-12`, retained zero and deliberately unseparated gaps as
`GAP_UNCERTAIN`, and rejected a boundary endpoint and non-rational input.

The phase-2 numerical source and compact evidence were frozen in commit
`187e8a8a3f3ad3b03d686930253ebeaf0b5e228b`, tree
`dc7acefc43aa51745bb4b96138a3fd9d86e5f40d`. A reviewer who did not author the
search read the fixed result, ledger, summary, source, and best-object blobs.
The reviewer independently reconciled all counts, checked the Mobius and
complement signs, and returned `STATUS: CORRECT`; see
`verification/phase2_param_commit_review.md`.

## Round 5: global `n=2` concavity and block composition

Status: `VERIFIED / GENERAL_N_GE_3_OPEN`.

Two theorem statements were frozen before proof.  For `n=2`, exact event
coordinates reduce the entropy Hessian to `-(G-2LQ)`.  Under
`A+B+C+D=1`, its determinant pencil is

```text
det(G-sQ)=[16r+4sE-s^3P]/(16rP).
```

The quadratic coefficient cancels.  The inequalities `sqrt(P)L<=r` and
`E>4r^2` keep the determinant positive over the full path `0<=s<=2L`, so
inertia remains positive definite.  The diagonal locus is handled directly
by `H''=-F<=0`.  This proves global concavity in dimension two and strict
midpoint loss for every nonzero chord.

Independently, Shannon subadditivity proves that at a block-diagonal center the
global gap is bounded by the sum of principal-block gaps.  A nonzero
cross-block kernel entry makes both endpoint block laws dependent, hence the
bound strict; no cross-block entry gives product laws and equality.  Combining
the two results covers all block-diagonal centers with blocks of size at most
two in arbitrary real-symmetric directions.

The fixed theorem/proof commit is
`603300c06059518961766c724377c3b9d1198fc5`, tree
`9c1a4db5462dddaf4a3b7cc37c010927254cbda4`.  Two reviewers who did not author
the corresponding proof read only the fixed Git objects.  Both returned
`CORRECT`; their reports record the theorem, proof, symbolic, and sanity blob
IDs.

The preregistered `n=2` falsification search completed 122,832 formal calls and
32 optimization restarts, all `OK`, plus two successful 90-digit checks.  The
raw floating maximum `1.455e-11` became `-5.227e-12` at high precision.  A
separate event-coordinate probe made 200,000 random checks and a rational
kernel/direction probe made 100,000 checks, also without a counterexample.
None of these finite denominators is used in the proof.

Two attractive but insufficient routes are retained.  A Cramer--Rao bound
using only the two marginal means is too weak and its required matrix
inequality fails on legal negatively associated four-event laws.  Replacing
the exact log odds by the one-sided bound `L<=c^2/(AD)` likewise demands a
strictly stronger false matrix inequality.  Neither failed route is a
counterexample to entropy concavity.

The first commit attempt failed because this checkout lacked local author
identity.  Setting repository-local identity to match prior R1 commits fixed
the transport issue; no global Git setting was changed.

## Round 6: the connected `n=3` obstacle

Status: `FINITE_NO_HIT / EXACT_REDUCTION / GENERAL_N_GE_3_OPEN`.

The preregistered connected-center attack completed 136,898 continuous unique
objective calls, all `OK`: 120,724 floating Hessians and 16,174 fixed-decimal
90/140-digit Hessian reviews.  All 8,053 floating values above `1e-8` were
reviewed at both precisions and none passed the independent directional and
finite-chord gate.  The raw maximum `0.0119708909` became
`-1.53765354e-14` at 140 digits.  All processes exited normally.  These finite
denominators do not prove the frozen `n=3` statement.

For a compound-symmetric center, Boolean Mobius inversion and exact `S_3`
symmetry split the six-dimensional Hessian into one trivial `2x2` block and
two copies of one standard `2x2` block; all trivial-standard entries vanish
exactly.  Independent probes checked 17,042 centers and 40,000 strict feasible
chords without a robust positive.  Shepp--Olkin concavity plus direct affine
differentiation proves both diagonal entries of the trivial block strictly
negative.  Its determinant remains one explicit scalar obstruction; the
standard block signs and finite-midpoint step also remain open.  Repeated-grid
work was retired rather than promoted.

During public replay, the base Python lacked `sympy` and the first symbolic
invocation exited 1.  No dependency was installed; an already available
SymPy 1.14 runtime then reproduced the exact identities with exit 0.  One
read-only 20,000-sample replay lost its captured session output after the
process ended, so a second identical replay was run and exited 0 with the
recorded summary.  These validation replays are outside the 136,898-call
formal denominator.

## Round 7: exact equicorrelation Hessian closure

Status: `VERIFIED_LOCAL_HESSIAN / STRICT_CONCAVITY_INSIDE_FAMILY / GENERAL_N3_OPEN`.

The two logarithms in the standard `S_3` block were reduced to functions of
the odds ratio `rho`.  Complementation restricts the proof to `rho>=1`.
Monotonicity in `W=-U` lowers the determinant to

```text
2c^2 q0+R q1 T+R^2 lambda mu T^2,
```

where exact factorization proves `q0,q1>0` off the product diagonal.

The remaining trivial determinant was then parameterized by fixed `rho` and
written as a degree-four Bernstein polynomial in `lambda`.  Each of its five
coefficients is nonnegative using `0<=A<=B`, `A<1/3`, and a rational upper
bound obtained from `log y<=(y-1)/sqrt(y)`.  A new dependency-free exact
certificate rebuilds the Fisher formulas, determinant substitution,
Bernstein expansion, and coefficient identities with rational arithmetic;
replay exits `0`.

Two nonauthor contexts independently reviewed both block proofs and returned
`CORRECT`.  Consequently the full six-dimensional Hessian is negative
semidefinite at every strict compound-symmetric `3 x 3` kernel, and negative
definite away from `lambda=mu`.  Because the compound-symmetric parameter
domain is convex and the kernel map affine, the trivial-block result also
integrates to strict global concavity along every nonconstant chord contained
in that family; two reviewers returned `CORRECT` for this corollary.

This round does not prove the frozen arbitrary-direction finite-midpoint claim
at a compound-symmetric center and does not resolve a general connected
`3 x 3` kernel.  A low-frequency text-only reviewer timed out without a
verdict; that infrastructure failure was not treated as a mathematical
decision.

The negative-definite conclusion off `lambda=mu` has a full-dimensional
continuity consequence.  Strict kernels have strictly positive L-ensemble
event probabilities, so entropy is real analytic on `0<K<I`.  Negative
definiteness is open; hence every non-product compound-symmetric kernel has a
small convex ball of general real-symmetric kernels on which the Hessian stays
negative definite and every nonconstant chord has strict midpoint loss.  Two
independent nonauthor reviews returned `CORRECT`.  No uniform radius or global
connected-`n=3` coverage is claimed.

## Round 8: a convex strict-concavity tube near product diagonals

Status: `VERIFIED_LOCAL_TUBE / GENERAL_N3_OPEN`.

For `K=diag(d)+E`, the exact event law relative to the product Bernoulli law
has density `1+g`, where `g` is a quadratic pair term plus the cubic triangle
term.  The entropy correction begins with negative edge quartics and a
negative `x^2y^2z^2` term.  Exact block-axis cancellation and diagonal-sign
symmetry classify every remaining analytic monomial into four types.

Using the anisotropic weights

```text
x^2+y^2z^2,        y^2+x^2z^2,        z^2+x^2y^2,
```

the complete analytic remainder Hessian is uniformly smaller by a factor
`epsilon^2` than the leading negative form, even when edge ratios approach
zero arbitrarily fast.  The diagonal block remains uniformly negative and the
mixed block is absorbed by Young's inequality.  Thus, for each fixed interior
margin, a sufficiently small whole convex tube around the product-diagonal
cube has negative-semidefinite Hessian; connected centers have a
negative-definite Hessian.  Despite exact block kernels on disconnected
strata, every nonconstant chord in the tube has strict negative curvature
except at at most isolated points, hence strict finite-chord concavity.

Two independent nonauthor contexts audited the full uniform analytic argument
and returned `CORRECT`.  A dependency-free exact script separately checked
all eight event polynomials and the degree four, six, and seven entropy terms,
with degree five absent; it exited `0`.  This is a local tube theorem, not
general connected `3 x 3` concavity.

## Round 9: general `3 x 3` four-interaction normal form

Status: `EXACT_REDUCTION / GENERAL_RESIDUAL_OPEN`.

The complete-event acceleration space has dimension four: three pair-minor
second jets and one determinant second jet.  Its dual log potential consists
of three pair atom interactions and one three-body interaction, giving the
exact scalar normal form

```text
D2H=-F-sum sigma_ij theta_ij-tau theta_123.
```

The proved `n=2` theorem and Fisher data processing peel off any nonnegative
edge weighting of total mass at most one, leaving an explicit three-body
residual.  A natural rigid attempt to cancel all pair log terms is obstructed
at a simple strict rational point: its forced weights make the Fisher bracket
about `-16.68539`.  This retires only that decomposition, not the entropy
claim.

In normalized L-ensemble correlations, the four theta coordinates become six
conditional pair log odds, all nonpositive.  Their present-minus-absent
differences all equal the same three-body theta, leaving two allocation
freedoms.  Optimizing the dangerous coefficients gives a scalar sufficient
condition `F>=D_*` and an exact narrow sign cone with `D_*=0`.  The identities
and their dependency-free replays received nonauthor `CORRECT` reviews; the
general Fisher bound remains unproved.

## Round 10: collapsed allocation dual

Status: `EXACT_REDUCTION / FOUR_FISHER_COMPARISONS_OPEN`.

Linear-program duality reduces the two-dimensional definition of `D_*` to a
single dual coordinate `r`.  The DPP identity that all three present-minus-
absent conditional log odds coincide makes all three edge breakpoint shifts
equal.  The dual objective is therefore a concave piecewise-linear function
with only two interior breakpoints, so its maximum is attained among exactly
four displayed endpoint/breakpoint values (with duplicates removed).

This collapse is valid when conditional odds vanish (the affected edge box
collapses while the common dual interval may only shorten) and uses the signed negative part
`sum min(sigma_e,0)`.  It turns the remaining sufficient condition into four
explicit piecewise-quadratic Fisher-versus-log-odds comparisons, ordinary
quadratic forms on each fixed `sigma` sign cone, but proves none of those
comparisons globally.  A four-object exact rational sanity check found no
failure and is intentionally not promoted as theorem evidence.
