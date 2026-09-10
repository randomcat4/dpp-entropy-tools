# PR88 C1 FIRST review report

Scoped verdict: `ACCEPTED_SCOPED` for the analytic source claims stated below; `SOURCE_ONLY / PENDING_C2` for the author finite certificates, large-rational arithmetic, interval-log enclosures, exact enumerations, and stored output; `NOT_ASSESSED` for novelty, formal proof, and merge readiness.

No source-level `NEEDS_FIX` item is raised in this bounded FIRST. PR88 does not close the unrestricted moving rank-two endpoint problem, and it says so explicitly in `README.md` lines 72-74, `proof.md` lines 267-269, and `continuation.md` lines 239-243.

## Accepted scoped analytic claims

The probability and sign conventions are explicit and consistent. The packet defines complete DPP atoms by inclusion-exclusion and uses `G=H(midpoint)-1/2 H(left)-1/2 H(right)` with `Delta=-G` in `proof.md` lines 5-13. That convention is carried into `continuation.md` lines 1-3, so later statements about negative `Delta` are not sign-flipped entropy counterexamples.

The rank-two midpoint expansion is complete for the stated purpose. In `proof.md` lines 15-79, the author writes the Cauchy--Binet expansion through the shared four-column Gram representation, gives the pair formula, includes triple and quadruple midpoint atoms, and records the pair inclusion correction. The text correctly says the pair mixed discriminant inequality does not imply the needed atomwise mixture comparison and that entropy sign cannot be obtained from inclusion minors alone. This directly rejects the old “split rank two into rank one modes” shortcut also summarized in `README.md` lines 48 and 62.

The PR43-E three-coordinate input is reproduced enough for this FIRST. `proof.md` lines 81-99 give the full quadratic complete-atom law, the null-vector/adjugate representation, the Boolean Mobius identification of the acceleration law, the conditional two-coordinate covariance sign, and the full Hessian formula retaining both Fisher and acceleration terms. The source cites earlier accepted material at line 101, but the load-bearing mechanism is present in this packet, so I did not require or read the old review record.

The common dense-mode theorem is accepted within its stated hypotheses. `proof.md` lines 103-187 restrict to actual coordinates split as `J disjoint E`, with a common dense rank-one mode and motion only through two independent vectors supported on the three-coordinate block. The conditional decomposition in lines 120-160 keeps the outside and cross terms through the Schur complement and exact entropy chain identity, rather than replacing the problem by an informal marginal. The `C` branch is a true affine three-coordinate line with indefinite rank-two direction (`proof.md` lines 161-167), and the occupied-outside branch uses a rank-one strict argument rederived in lines 169-186. Thus the strict midpoint gap for this common dense-mode class is analytically supported. It does not apply to arbitrary unrelated rank-two endpoints.

The fixed affine multiple-boundary theorem is accepted as a local endpoint theorem. `proof.md` lines 188-210 prove the expansion `H''(h)=-beta/h+O(1+|log h|)` for a fixed legal affine line by separating positive atoms, simple emerging atoms, higher-order rare atoms, and the acceleration contribution. This retains the full Fisher term and does not drop logarithmic acceleration terms. The count-layer derivative in lines 212-238 gives the basis-invariant lower bound on `beta`, and Corollaries 2a-2b at lines 239-243 show `beta>0` for strict inward boundary lines and for fixed moving-rank-two chords near endpoints. The same lines correctly leave the compact middle undecided and do not provide a uniform threshold over varying endpoint angles or scales.

The coordinate-supported indefinite rank-two lift in `continuation.md` is accepted as a whole-chord theorem under its actual-coordinate support condition. Theorem 3, lines 5-22, assumes `D=B-A` is supported on `J x J` for three observation coordinates and that `D_J` is rank two indefinite. The proof at lines 23-53 conditions on complete outside configurations by a signed Schur complement, keeps arbitrary outside and cross blocks fixed, and obtains a strict three-coordinate conditional kernel with derivative exactly `D_J`. Lines 54-83 then use Fisher lower bounds from one-coordinate or two-coordinate inclusion statistics to get a strictly positive midpoint gap on every subinterval, with endpoint passage by common bit-flip regularization and continuity. This proves strict concavity for the true chord in that class. It does not cover a spectral rotation or a general rank-four spread difference, as restated in `continuation.md` lines 239-243.

The strict-kernel lift argument is accepted in its stated continuity range. `proof.md` lines 245-265 use the common independent bit-flip channel, total variation at most `1-(1-epsilon)^n`, and a finite-alphabet continuity modulus to obtain `G_epsilon >= G - 2 omega_n`. This is a valid “positive gap survives sufficiently small common noise” statement and, for the coordinate-supported class, `continuation.md` lines 84-119 correctly derives the all-`0<epsilon<1/2` result from Theorem 3 rather than from a small-epsilon continuity assertion.

The packet correctly separates method obstruction from entropy counterexample. `README.md` lines 17, 48, 65, and 72 state that the auxiliary rank-two event-mixture bridge failure is method-only and that a real disproof would still require legal exact kernels with positive true `Delta`. `fixtures.md` lines 3, 51-95, and 166 make the same separation. This FIRST accepts that logical distinction. The finite signs offered for the bridge, the strict-kernel lift, and the true `Delta` remain author evidence only here.

## Source/evidence-only material left pending

The following PR88 material is not promoted to independently verified fact in this FIRST:

- The dense four-point bridge witness and strict-kernel method obstruction in `fixtures.md` lines 13-95 and `verify.py` lines 139-174.
- The six-point common-mode fixture values and lift lower bounds in `README.md` lines 29-34, `fixtures.md` lines 96-130, `continuation.md` lines 84-119, and `verify.py` lines 184-210.
- The strong-correlated multiring exact matrices, all 64 atom quartics, endpoint coefficient `beta=6784/16875`, conditional-anchor failure, and finite negative probes in `README.md` line 18, `continuation.md` lines 120-238, `fixtures.md` lines 132-166, `verify.py` lines 219-281, and `certificate_compact.json` line 1.
- The compact certificate contents in `certificate_compact.json` line 1, including interval-log signs and exact atom arrays.

These are useful author-supplied evidence records, but under the C1 source-only constraint I did not execute or reconstruct them. PR88 itself labels the heavy continuous verification as requested/not running in `README.md` lines 5 and 74, and this report does not create or expand a C2 contract.

## Still open

- The unrestricted moving rank-two endpoint entropy-concavity problem remains open. PR88 closes the common dense-mode class and the coordinate-supported rank-two-difference class, but general moving rank-two endpoints can have rank-four differences spread over all coordinates (`README.md` lines 72-74; `continuation.md` lines 239-243).
- The strong-correlated double-endpoint multiring compact middle remains incomplete. Endpoint asymptotics and finite samples are not a continuous full-interval proof (`README.md` lines 18, 65-67; `continuation.md` lines 227-243).
- Novelty is not assessed. The source lists primary background in `README.md` lines 52-56, but this FIRST did not perform prior-art research.
- Formal verification was not performed.

## Required extra source

No additional pure source is required for this bounded FIRST. The PR43-E three-coordinate input and the rank-one strict mechanism are both rederived in the PR88 packet at `proof.md` lines 81-99 and 169-186. Earlier review-status mentions, including `README.md` line 42, were ignored as evidence.
