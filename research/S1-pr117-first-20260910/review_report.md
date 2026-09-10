# Independent FIRST review report for PR117

## Verdict

**ACCEPTED_SCOPED** at exact head
`70d69bf5c47282c953010518ff264cb2a7a09bf9`.

The arbitrary-strict-`A_0` local theorem is supported by the submitted proof.
The version under review keeps the true affine kernel, every occupied/vacant
atom, the Fisher and atom-acceleration terms, and the thermodynamic response.
No finite-window sign experiment is used as a theorem.

## First-principles audit of the load-bearing bridge

### 1. Reference truncation and complete-event coercivity — pass

Absolute Fourier convergence permits a symmetry-preserving, same-mean finite
truncation `c^0` with `||c-c^0||_W=epsilon_0` arbitrarily small.  Uniform
convergence gives `delta_0 <= c^0 <= 1-delta_0`, where
`delta_0=delta-epsilon_0>0`.

For `M_x^0=T_Lambda(c^0)-I_Z`, multiplication by the occupied/vacant sign
matrix cancels the cross terms and bounds the smallest singular value by
`delta_0`.  Hence `||(M_x^0)^(-1)|| <= delta_0^(-1)` uniformly in the word and
volume.  Since `-I <= M_x^0 <= I`, self-adjointness and this singular gap
justify

`(M_x^0)^(-1)=M_x^0 sum_{q>=0}(I-(M_x^0)^2)^q`.

Finite bandwidth then gives an event- and volume-uniform exponential
off-diagonal estimate.  Positivity of `M_x^0` is neither stated nor needed.

### 2. Configuration-local inverse approximation — pass

The inverse of the complete-event compression to the two endpoint
neighborhoods has the same coercive gap.  Deleting the finite-band couplings
through the cut and applying the resolvent identity places one exponentially
decaying inverse factor between each endpoint and the cut.  This yields the
claimed entrywise error.  Summing the near-diagonal `O(R)e^{-aR}` part and the
off-diagonal exponential tail yields

`sup_(Lambda,x) ||R_x^0-R_x^[R]||_(2->2) <= C e^{-aR}`.

After one fixed starting radius, `||R_x^[R]|| <= B=delta_0^(-1)+1`.  The
decay rate and starting radius may depend badly on the already frozen
finite-range reference; no uniformity over a sequence of truncations is
used.

### 3. Trace-log preconditions and real branch — pass

The exact complete-event determinant ratio is

`p_t(x)/p_0(x)=det(I+R_x^0 E_t)`, `E_t=T(c-c^0+t g)`.

The segment between `c^0` and `c+t g` remains strictly legal after the stated
choices, so the determinant ratio stays positive along that segment.  The
ordinary real log is therefore the analytic branch issuing from one.  The
uniform contraction

`||R_x^0 E_t|| <= delta_0^(-1) eta < 1`

justifies the full trace-log series, including its nonvanishing `m=1` term.

### 4. Operator norm versus absolute displacement sums — pass

This is the main reverse-audit point.  The proof never turns an operator-norm
bound into an entrywise absolute inverse-walk sum.  It expands only

`E_t=sum_d e_t(d)S_d`, with `sum_d |e_t(d)| <= eta`.

For each fixed displacement tuple, partial shifts have norm at most one and

`|Lambda|^(-1)|Tr prod_j(R_x^[R]S_(d_j))| <= B^m`.

Thus absolute displacement summation costs only the Wiener coefficients of
`e_t` and `g`; it does not cost row sums of `R_x^[R]`.  The stronger geometric
condition required after localization is `B eta<1`, but it is available in
the correct quantifier order:

1. choose `epsilon_0` so small that `epsilon_0<delta/2` and
   `B epsilon_0<1/4`;
2. here `B<=2/delta+1`, independently of the truncation range;
3. freeze that truncation and choose `tau` with
   `B tau ||g||_W<1/4`.

Consequently `B eta<1/2`.  This is not the withdrawn condition
`||u||_1 epsilon_0<1`: no inverse-envelope norm that can deteriorate with the
truncation appears.

### 5. Bell differentiation and corrected support count — pass

Jacobi/Bell differentiation of each complete marginal gives, through order
four,

`|partial_t^q p_(J,t)(x)| <= p_(J,t)(x) A_q |J|^q`.

It follows after summing every atom that a bounded local observable pays only
its support cardinality, while rare atoms remain present.

For a diagonal anchor of a length-`m` product of `R^[R]` and fixed shifts,
each inverse hop has range at most `R`.  At the `j`-th stage the possible
endpoint cloud has width `O(jR)` about a displacement-dependent center.
Taking the union of the endpoint neighborhoods over all stages costs at most
`C m^2(R+1)`.  Large physical displacements translate these clouds but do not
increase their cardinality.  This validates the authoritative correction.

The source states the shell sup bound for the normalized trace.  The same
telescoping operator estimate in fact bounds each anchored diagonal entry,
because `|A_ii|<=||A||`; hence it is legitimate to combine that bound with the
local Bell estimate before averaging anchors.  This is an implicit
one-line clarification, not a missing norm assumption.

With the corrected support count, shell differentiation costs

`C_q m^(2q+1)(R+1)^q B^(m-1)e^(-aR)`.

Derivatives falling on the affine coefficients add at most `m^q` and the
absolute Fourier sums.  The resulting coarse majorant

`C_q m^(3q+1) B^(m-1) eta^(m-q)(1+||g||_W)^q`

is summable in walk length under `B eta<rho<1`.  The finitely many terms with
`m<q` are harmless.  The support correction changes only a polynomial factor
and does not repair, replace, or assume a norm switch.

### 6. Relative-KL thermodynamic limit — pass

At fixed walk length, displacement tuple, and localization radius, every
anchored observable is a translate of one finite-coordinate function away
from the interval boundary.  Stationarity gives the infinite-volume
expectation exactly there; the boundary fraction vanishes.  The same finite
marginal calculation gives derivatives through order four.

The established uniform majorants permit dominated convergence in the stated
order: volume, localization shells, displacement tuples, then walk length.
Therefore the relative-entropy density exists locally uniformly with four
continuous derivatives, and normalized finite-volume derivatives converge.

### 7. Fixed-reference cross entropy — pass

For the strict finite-band reference, the complete-event Schur complement is
uniformly nonnull.  The same inverse decay makes the effect of a distant
future cut exponentially small.  Hence the one-sided log conditional is
bounded and has an exponentially summable cylinder-shell decomposition.

Differentiating its expectation under the true complete law costs
`(R+1)^q` on the radius-`R` shell, which remains summable against `e^{-aR}`.
For the finite chain rule, the conditional error at remaining future length
`R` has the same exponential bound; summing `R^q e^{-aR}` also controls the
differentiated boundary discrepancy.  This proves the claimed `C^4`
cross-entropy density.

### 8. True Shannon entropy and curvature — pass

The exact finite identity

`D(p_t||p_0)=-H(p_t)-E_t log p_0`

uses all complete atoms.  Passing both reviewed limits yields
`h(c+t g)=-d_0(t)-ell_0(t) in C^4`; no spectral-basis entropy is substituted.

Half-period symmetry fixes both parity marginals, makes them independent at
zero, and makes the complete law even in `t`.  Thus
`J(t)=h(c)-h(c+t g)` is even, nonnegative, and `C^4`.  If `J''(0)>0`, strict
local concavity follows by continuity.  If `J''(0)=0`, even `C^4` Taylor
expansion and the accepted matching floor give quartic coefficient
`A>=|g_hat(k)|^4/[4 mu^2(1-mu^2)]=2 alpha_k`.  Therefore
`(h(c+t g)+alpha_k t^4)''<0` for sufficiently small nonzero `t`, with equality
at zero, proving concavity on a smaller symmetric legal interval.

## Contract-unit ledger

| Unit | Result | Reason |
|---|---|---|
| U1 truncation | PASS | symmetry, mean, Wiener tail, and strict margin preserved |
| U2 event inverses | PASS | sign-coercivity and self-adjoint finite-band decay |
| U3 localization | PASS | resolvent cut estimate and Schur row/column summation |
| U4 trace-log | PASS | positive real branch and operator contraction; `m=1` kept |
| U5 full-law derivatives | PASS | atomwise Jacobi/Bell bound retains every word |
| U6 derivative majorant | PASS | anchorwise operator bound plus corrected `O(m^2R)` support |
| U7 relative KL | PASS | four nested limits have uniform derivative majorants |
| U8 cross entropy | PASS | exponential reference conditional shells and boundary sum |
| U9 entropy identity | PASS | exact complete-Shannon finite identity survives the limit |
| U10 curvature | PASS | parity identities, matching floor, and both Taylor cases |
| U11 source boundary | PASS | corrected BGS wording is source-accurate; the withdrawn route is not used |

## Evidence boundary

This is a mathematical source review, not a computation or a novelty search.
Failure of the withdrawn inverse-envelope method remains only a method
obstruction and is not converted into an entropy counterexample.  The verdict
applies only to the frozen head and the scope in `frozen_scope.md`.

The final source delta was checked against Fang--Shin's primary paper.  Its
introduction explicitly attributes norm-controlled inversion of the `p=1`
BGS algebra in `B(ell^2)` to Baskakov, so PR117 is correct to withdraw its
earlier contrary wording.  Fang--Shin's own nonsymmetric theorem imposes
`r>d(1-1/p)` on `C_(p,r)`, which does not turn that theorem itself into an
unweighted `p=1,r=0` result.  PR117's corrected neutral boundary accurately
avoids both overclaims, and no part of the finite-range proof depends on this
literature statement.
