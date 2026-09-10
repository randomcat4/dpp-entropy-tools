# S1 analytic FIRST for PR116

Status: **MIXED: PASS_SCOPED_ANALYTIC_INTERFACE + EVIDENCE_INSUFFICIENT; STOPPED_HANDOFF_READY**.

This review freezes the substantive author packet at
`71ea4dcd752e0f6ba396af64fe379e7c55407d76`.  All 28 author files at that
head were read.  The later PR head
`3f276c09fe4da3aded2ab6cf457adb7fdc4254d8` was checked only for its three
closeout commits: removal of an empty placeholder, supersession of an
unstarted historical contract, and addition of a final inventory.  Those
commits change no load-bearing theorem, formula, source, or retained output.

This is an analytic FIRST only.  No author checker, symbolic script,
Bernstein certificate, or local contract was run.  No PR116 S3 conclusion or
conversation comment was read.  Novelty was not assessed, no SECOND is
issued, and no merge is authorized or performed.

## Executive disposition

The PR116 packet contains a sound and useful analytic core, but it is not a
completed proof of the compact-middle sign.

1. **PASS_SCOPED_ANALYTIC.**  The natural family has the stated true affine
   physical-kernel path and maximal chord.  The rank-two complete-event
   likelihood form, full Fisher--acceleration curvature identity, eventwise
   six-slope sufficient cone, block-complement symmetry, joint resolvent
   representation, and reverse-mixture KL curvature identity are correct.
2. **PASS_SCOPED_ANALYTIC.**  The cardinality/label representation is a
   lossless re-indexing of all 64 complete configurations.  The bivariate
   cardinality polynomial and the three symmetric label channels preserve the
   original Shannon problem; they do not coarse-grain it.
3. **PASS_SCOPED_ANALYTIC.**  The fixed-parameter endpoint phase is correct:
   integrated acceleration has an explicit negative logarithmic phase, while
   the full Fisher contribution has a strictly positive `delta^-1` pole.  The
   negative-acceleration phase is therefore a method obstruction, not a
   Shannon-entropy counterexample.
4. **PASS_SCOPED_ANALYTIC_INTERFACE / S2 GATE.**  Conditional on the displayed
   11-type exact table, the reserve comparison in `RESULT_EXCHANGEABLE.md`
   proves the claimed single `alpha=1/10, beta=1/3` whole-chord bound.  The
   adverse-row extrema, reserve arithmetic, physical pair-statistic Fisher
   bound, and quartic correction are correct.  The 11-type table itself and
   its 64-event source binding remain author finite evidence until S2
   independently reconstructs them.
5. **PASS_SCOPED_ANALYTIC_INTERFACE / S2 GATE.**  Conditional on the displayed
   13-type table and global `M_b` identity, the sharpened uniform endpoint
   theorem at `alpha=1/10`, `0<delta<=10^-4`, is correct.  The eventwise
   inequality `(-z)_+ <=25s^2b^2/4`, the deduction `M_b<=1`, the retained
   six-event Fisher pole, and the final exact comparison are sound.  The
   table and moment identity require independent finite/algebraic binding.
6. **EVIDENCE_INSUFFICIENT.**  The exact Bernstein positivity claim for the
   acceleration kernel, the exact negative rational-kernel point, and their
   displayed large rational values have no standalone generator plus literal
   output in the frozen packet.  They are not accepted by this FIRST.
7. **NOT_STARTED / OPEN.**  No full `alpha=1/10` joint-kernel certificate was
   run, and no proof or counterexample for the compact-middle sign of the full
   two-parameter family is established.

Accordingly, the correct overall disposition is mixed.  S3 may import the
analytic identities and endpoint phase with the scope below.  The special
whole-chord theorem and the uniform endpoint band are importable only after
the stated S2 input/arithmetic gate.  The Bernstein and exact-point claims
need their own independent reconstruction and must not be inferred from this
review.

## Analytic reconstruction

### Physical path and complete curvature

On each repeated `P` mode the kernel is

`[[alpha, t sqrt(alpha(1-alpha))], [t sqrt(alpha(1-alpha)), 1-alpha]]`.

Its determinant is `alpha(1-alpha)(1-t^2)` and its trace is one; the `Q`
mode remains the fixed pair `beta,1-beta`.  Hence the maximal legal chord is
exactly `[-1,1]`, with simultaneous two-dimensional nullspaces of `K` and
`I-K` at both endpoints.

For each complete event, Schur reduction through the rank-two cross block
gives

`p_E(t)=mu_E q_E(t^2)`,  `q_E(s)=1-a_Es+b_Es^2`.

Writing `v=a-2sb`, `h=a-6sb`, `w=a-sb`, and `z=wh`, direct differentiation
gives `q'=-2tv` and `q''=-2h`.  Since the two observed block marginals are
fixed along the off-diagonal path, the `log(mu_E)` acceleration terms cancel
row by row and column by column.  With `q-1=-sw`, this yields

`-H''(t)/t^2 = sum_E mu_E[4v_E^2/q_E+2z_E log(q_E)/(q_E-1)]`.

This also verifies the eventwise six-slope lemma: positive `q`, positive
logarithmic secant, nonnegative Fisher, and `z>=0` eventwise imply concavity.
The stated finite root test for `z=(a-sb)(a-6sb)` is correct.

One wording repair is required before canonical import.  Several notes point
only to `sum mu a=sum mu b=0` when introducing the curvature formula.  Those
two scalar normalization identities alone do not cancel the `log(mu_E)`
term.  The formula is nevertheless correct here because the physical path
has fixed left and right complete marginals, which supplies the stronger
conditional cancellations.  The proof text should say this explicitly.

### Lossless cardinality/label reduction

After complementing the right configuration, both sides have the same
exchangeable DPP marginal.  A subset of three labels is bijectively encoded
by its cardinality and, at cardinalities one and two, its occupied or missing
label.  Thus the proposed representation loses no complete event.

The two repeated `P` modes have the exact Bernoulli-pair generating factor

`g_s(x,y)=[(1-alpha)^2+rs]+r(1-s)(x+y)+[alpha^2+rs]xy`,

and the uncoupled `Q` mode contributes
`h_beta(x)h_beta(y)`.  Coefficient extraction therefore gives the actual
joint cardinality law.

A bounded independent reconstruction of the shifted-event `P` compressions
also recovers the displayed label-channel gaps.  For a level-one event the
two compression eigenvalues differ by

`2 sqrt(r)(1-beta)/[(1-alpha)(2alpha+beta-3alpha beta)]`,

and for a level-two event by

`-2 sqrt(r) beta/[alpha(alpha+2beta-3alpha beta)]`.

Normalized projected coordinate directions have squared inner product one
for equal labels and `1/4` for unequal labels, giving the factor `3/4` and the
three formulas in the author note.  Simultaneous permutation symmetry makes
the conditional label marginals uniform, so the `Phi_3` chain-rule
decomposition is exact.

### Endpoint phase and Fisher dominance

The four endpoint-zero groups have the author weights

`W_H=2 alpha^2(1-alpha) beta L`,
`W_L=2 alpha(1-alpha)^2(1-beta) N`,
`W_M=(2/3)alpha(1-alpha)LN`,
`W_D=2[alpha(1-alpha)]^2 beta(1-beta)`,

with `L=2alpha+beta-3alpha beta` and
`N=alpha+2beta-3alpha beta`.  These are exactly the three simple groups and
the empty/full double group obtained from the per-subset marginal masses.
Using their displayed endpoint slopes gives

`A_norm=C_A log(1/delta)+O(1)`,

`C_A=alpha(1-alpha)[7+x^2-7y^2-4xy+3x^2y^2]/3`,

where `x=2alpha-1`, `y=2beta-1`, and

`F_norm=C_F/delta+O(1)`,

`C_F=(16alpha(1-alpha)/3)`
`    *[3beta(1-beta)+alpha(1-alpha)+(beta-alpha)^2]>0`.

The two endpoint-phase notes are algebraically consistent; their
`alpha=1/10` specialization is
`C_A=(3/625)(-127beta^2+167beta-4)`.  Hence the open
negative-acceleration wedge is real, while the full curvature remains
favorable sufficiently near the endpoint for every fixed strict parameter
pair.  This conclusion is also within the qualitative endpoint scope already
available from accepted PR102.  PR102 supplies no compact-middle sign and is
not used for one here.  PR95 concerns a different exact fixture and supplies
no theorem imported into PR116.

The moving-parameter boundary-ray and two-scale formulas are mutually
consistent with this phase analysis.  Their detailed coefficient expansions,
however, are still table-derived author algebra and should be included in the
same S2 coefficient audit rather than treated as independently certified by
this FIRST.

### Special chord and uniform endpoint interface

For `alpha=1/10, beta=1/3`, the proof after the 11-row table is complete.  The
three adverse acceleration types are bounded by the positive `q=1-s`
reserve, and the remaining exact coefficient is

`195191/1755000>0`.

The binary statistic for one matching coordinate pair has derivative
`-2t/25`; data processing and `r(1-r)<=1/4` therefore give complete Fisher
at least `16t^2/625`.  It follows, conditional on the table binding, that

`H''(t)<=-(16/625)t^2`

and `H(t)+(4/1875)t^4` is concave on the closed chord.

For the beta-uniform endpoint band, the likelihood floor `q_E>=delta^2`
follows from `a_E<=2` and endpoint nonnegativity.  The adverse-mass inequality
and the displayed moment formula give

`A_norm>=-(25/2)lambda(delta^2)`.

Retaining the stated aligned six-event group gives
`F_norm>=1/(25delta)` for `delta<=1/100`.  The elementary monotonicity and
`log(10)<7/3` comparison then close `delta<=10^-4`.  This reasoning is sound,
but both exact table inputs (`a_E<=2` and the retained group) and the global
`M_b` formula remain in the S2 gate.

### Joint kernel and reverse-mixture divergence

The resolvent identities put the full curvature, without separating or
dropping terms, into

`Gamma(s)=integral_0^1 J(s,u) du`,

`J=sum_E mu_E[4v_E^2/d_E(u)^2+2z_E/d_E(u)]`,

`d_E=(1-u)+u q_E>0` on the strict path.

For the genuine mixture `m_u=(1-u)mu+up_t`, differentiation gives

`D(mu||m_u)''=u^2t^2 J(s,u)`.

The load-bearing cancellation is
`sum mu h=0` together with
`1-d=usw`, which converts the second derivative's `d^-1` term into the joint
acceleration term.  Equivalently,
`J=(1/s)d^2/dt^2[D(mu||m_u)/u^2]`.  The identity is correct, including the
continuous chi-square limit at `u=0`.

Convexity of the scalar generator in `q` does not imply convexity in `t`,
because `q(t)` is quartic.  Therefore the identity is a valid analytic
interface, not a positivity proof.

## Finite-evidence ledger

| Unit | S1 disposition | Required next gate |
|---|---|---|
| `verify_exchangeable.py` and retained stdout | Source logic is structurally consistent; author `PASS` not adopted | S2 independent 64-event reconstruction and exact table/reserve comparison |
| `certify_integrated_acceleration_negative.py` and retained stdout | Directed fixed-point logarithm method is structurally sound; exact inequality not adopted | S2 independent replay/source-output binding |
| `check_endpoint_phase.py` | Source-only cross-check; no execution claim | Optional S2 algebra replay if coefficients are imported |
| 13-type generic table and global moments | Analytic consequences pass conditionally | S2 exact reconstruction at the frozen head |
| Bernstein `R>0` box for `u<=15/16` | **EVIDENCE_INSUFFICIENT**; generator/output absent | Fresh independent certificate with complete source/output |
| Exact negative `R` point and large fractions | **EVIDENCE_INSUFFICIENT**; generator/output absent | Fresh exact reconstruction from the 64-event law |
| Full joint-kernel contract | **NOT_STARTED** | New authorization and a resource-compliant contract only if S3 chooses this route |

The operative six-hour contract requests one CPU and a 16-GiB address-space
ceiling.  The current local policy caps the whole local workload at 2 CPU and
8 GiB, with no GPU, and the remote server is unavailable.  The contract was
correctly left unstarted and cannot be executed locally as written.  No
resource budget was consumed.

## Exact remaining open scope

- The sign of full `Gamma` on the compact strict middle of the natural
  two-parameter family is open.
- Pointwise joint-kernel positivity `J>=0` on the full
  `alpha=1/10` cube is neither proved nor refuted by accepted evidence here.
- The acceleration-only pointwise Bernstein claim and exact negative point
  remain pending finite reconstruction.
- No true Shannon-entropy counterexample is established.
- No universal dense rank-two theorem, general real-kernel theorem, or true
  Toeplitz entropy-rate extension follows from PR116.

S3 remains the sole integrator.  Any selective import should preserve the
fixed-marginal cancellation clarification, the S2 gates, and the distinction
between acceleration/joint-kernel method obstructions and the sign of the
actual Shannon curvature.
