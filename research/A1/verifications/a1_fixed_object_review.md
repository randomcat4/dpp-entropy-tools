# A1 fixed-object independent review

Reviewer role: independent verifier. I did not use provenance, author discussion,
source search, or the later `05a9ccb` denominator-audit JSON. All mathematical
inputs below are fixed to A1 commit `58ee11adcf0afd8d183057d61f0168127093bcad`
and, for the allowed two-point dependency only, R1 commit
`603300c06059518961766c724377c3b9d1198fc5`.

## Object binding

- A1 commit: `58ee11adcf0afd8d183057d61f0168127093bcad`
- A1 tree: `443522e843050cc0024f83e227fadfa2ef9b1d5a`
- R1 dependency commit: `603300c06059518961766c724377c3b9d1198fc5`
- R1 dependency tree: `9c1a4db5462dddaf4a3b7cc37c010927254cbda4`

| Role | Path | Blob |
|---|---|---|
| A1 hazards | `research/A1/hazards.md` | `f84758a8791cc2f32088ffc5f1e52d980a88a4c5` |
| A1 original target | `research/A1/frozen_theorem_v1.md` | `451f657eec2e36a4ad8b33a7645eaab57ac055b4` |
| Radial theorem | `research/A1/frozen_radial_slice_v1.md` | `994d4b12f41b09b70613d2c18fb8fc5248b90277` |
| Radial proof | `research/A1/proofs/radial_slice_v1.md` | `71d37d6e3effaed52f8fc23902f76e0d2e38b0ec` |
| Radial replay code | `research/A1/main/conditional_check.py` | `e39586d21b48634baa184bccd6d757287cd1eeb5` |
| Standard theorem | `research/A1/frozen_standard_modes_v1.md` | `34ec0bea1aea598b40c873d67050626a3e1205f0` |
| Standard proof | `research/A1/analytic/proof.md` | `b33c2f47e2ec099f91b48c86bb447617dfd977bc` |
| Standard replay code | `research/A1/analytic/verify.py` | `3b1903f407547914074bce47b1f0de7f178fdf61` |
| Acceleration theorem | `research/A1/frozen_acceleration_obstruction_v1.md` | `970e593eb764e7c29579294bda2688dfe4b0beb2` |
| Acceleration proof | `research/A1/probe/proof.md` | `383b26aa538cff1b1208d4145e69d1d86ad132d9` |
| Acceleration certificate code | `research/A1/probe/conditional.py` | `2e21a1cac332619ad9c0444e8256267656e643d4` |
| Acceleration certificate JSON | `research/A1/probe/conditional.json` | `21f3688c134c6844449b1b4748aba0e4e35edd35` |
| Acceleration derivative helper | `research/A1/probe/probe.py` | `49df015fb16594e8a876ba3d45b12d0822ab548d` |
| R1 theorem | `research/R1/frozen_n2_concavity_v1.md` at R1 commit | `cc247289014ba6874387da87543667e0e01616c3` |
| R1 proof | `research/R1/proofs/n2_concavity.md` at R1 commit | `7d652eae8d745d2289713db82b590d0c41c04bc7` |
| R1 later commit-bound review | `research/R1/verification/n2_concavity_commit_review.md` at A1 commit | `99c15aeb713900b0a19223b994d63b92ef03637c` |

Line references below refer to `git show <commit>:<path>` content at these
objects.

## Replay summary

I ran the frozen author replays and an independent exact replay in the isolated
verify checkout. The command log is
`research/A1/verifications/a1_verify_command_log.jsonl`. The first independent
run had exit code 1 only because Python refused to stringify very large
integers in the JSON output; after `sys.set_int_max_str_digits(0)`, the same
checks completed with exit code 0. That first failure did not report a failed
mathematical assertion.

- `radial_author_check`: exit code 0; output
  `research/A1/verifications/radial_author_check.json`.
- `standard_author_verify`: exit code 0; output
  `research/A1/verifications/standard_author_verify.stdout`.
- `a1_direct_replay_rerun`: exit code 0; output
  `research/A1/verifications/a1_direct_replay.json`.

The independent replay used Python `3.12.3`, SymPy `1.13.3`, and one BLAS/OpenMP
thread. It passed 15 radial symbolic checks, 23 standard symbolic checks, and
9 acceleration certificate checks. The acceleration replay confirmed minimum
principal minor `325079/4000000`, a strictly positive lower endpoint for `R`,
and a strictly negative upper endpoint for the full three-point entropy second
derivative in the same direction.

## 1. Fixed-site radial coupling slices

STATUS: CORRECT

The theorem in `frozen_radial_slice_v1.md` claims strict concavity only on the
fixed `(c,v)` radial slice, with complete-event entropy and with the nonaffine
conditional acceleration retained; it does not claim the original full
three-point target. The proof establishes that scope.

The complete conditional event laws are correctly identified. In
`radial_slice_v1.md:21-32`, conditioning on site 3 being present gives the
Schur complement `C_1`, while conditioning on site 3 being absent gives `C_0`.
This is a complete-event law statement after Mobius inversion, not a substitution
of inclusion minors for event probabilities. The independent replay checked all
eight identities
`p_K(S without 3)=(1-c)p_{C_0}(S)` and
`p_K(S with 3)=c p_{C_1}(S)`, plus normalization.

Strict feasibility is also covered. Lines `17-19` prove `C_1>0`, `C_1<I`,
`C_0>0`, and `C_0<I` using Schur complements and the strict contraction
premise. Positivity of the complete event law for strict contractions is
justified in lines `7-11`; the same L-ensemble argument applies to the
conditional two-point kernels.

The line-second-derivative formula at `40-45` has the correct acceleration term:

```text
2r^2 (Df(C_0)[W]-Df(C_1)[W]).
```

The independent replay checked the two matrix acceleration identities. The
first two terms are nonpositive by the allowed R1 two-point theorem. For the
last term, lines `49-54` compare derivatives along the same feasible rank-one
line `A+uW`; this uses only scalar concavity of the two-point entropy along that
line and does not assume a general matrix-order monotonicity of the entropy
gradient.

The strictness argument closes. Lines `56-69` prove the rank-one line entropy is
strictly concave because the complete event probabilities are affine and at
least one complete-event derivative is nonzero. Lines `71-80` then split affine
parameter lines into `r != 0` and `r = 0`: if `r != 0`, the second derivative is
strictly negative except possibly at the single point where `s=0`, and the
triangular Green-kernel integration gives a strict finite chord inequality; if
`r=0`, the strict two-point chord theorem applies to both conditional kernels
because `B != 0`.

No critical gap was found in the use of the R1 dependency. I read the R1 theorem
and proof at commit `603300c...`, and independently checked that A1 only needs
its strict real two-point finite-event entropy concavity, not any three-point
or inclusion-minor statement. The later R1 commit-bound review was read only as
context and not used as a substitute for this condition check.

## 2. Half-filled triangle standard modes

STATUS: CORRECT

The frozen theorem in `frozen_standard_modes_v1.md` is a local Hessian statement
on the four-dimensional subspace
`tr V=0`, `V_12+V_13+V_23=0`. It expressly excludes the complementary
two-dimensional symmetric component and any full-Hessian or finite-chord claim
in lines `28-31`. The proof preserves that scope.

The full six-dimensional reduction in `analytic/proof.md:56-62` is an identity
for all real symmetric directions, splitting the Hessian into a trivial
two-dimensional block `T` and a standard block `S`. The representation argument
in lines `64-72` is sufficient: simultaneous permutations force constant block
coefficients and remove mean/zero-sum cross terms. The author replay checked 24
exact identities, including the derivative tables and six-dimensional identity;
my independent replay checked the event probabilities, Fisher decomposition by
cardinality, and log-acceleration decomposition.

For the standard block at half filling, the sign proof is valid. Lines
`104-115` factor the four cardinality probabilities and define `M`, `Lg`, `m`,
and `ell`. Lines `125-143` prove

```text
m > 2 ell > 0
```

by an integral comparison using the increasing function
`g(s)=6s/(1+2s^2)` and the strict bound `4q^2<1`. Lines `146-155` then show the
non-Fisher part of `S` is positive definite, while the Fisher part is a sum of
nonnegative squares over positive probabilities. This proves positive
definiteness of `S` for `0<r<1/4`.

The transfer to `r<0` in lines `157-161` is legitimate: complementation gives
`H(K)=H(I-K)`, `I-K(1/2,r)=K(1/2,-r)`, and the Hessian is quadratic in the
direction. The `r=0` endpoint inside the open range is also handled exactly:
line `163` gives `S(u,v)=8u^2`, and lines `173-174` yield
`D^2H=-4 sum_i V_ii^2`, so purely off-diagonal standard directions are flat at
second order, exactly as the frozen theorem states.

The proof does not let the standard block masquerade as the full Hessian.
Lines `178-188` explicitly leave the trivial block `T` as an unproved equivalent
blocker for full six-dimensional nonpositivity, and say that arbitrary `(d,r)`
would require both blocks.

No critical gap was found.

## 3. Conditional-acceleration obstruction

STATUS: CORRECT

The frozen statement in `frozen_acceleration_obstruction_v1.md` claims only that
one conditional-kernel acceleration contribution

```text
R = 2 (Df(C_0)[ww^T] - Df(C_1)[ww^T])
```

is strictly positive and is therefore an obstruction to a blanket proof shortcut.
It expressly does not claim the total Hessian or a finite chord gap is positive
in lines `28-31`. The proof keeps that distinction.

The feasibility calculation is exact. In `probe/proof.md:16-30`, all edges are
nonzero, the leading principal minors of `K` and `I-K` are positive, and the
conditional kernels have positive leading minors and determinants. My replay
checked all principal minors of both `K` and `I-K`, not only the leading ones,
and recovered the displayed minimum `325079/4000000`.

The two-point entropy derivative formula in lines `34-43` is correct for the
direction `ww^T` with `w=e_2`:

```text
Df(C)[ww^T]=(1-u)log(p00/p01)+u log(p10/p11).
```

The displayed event numerators for `C_0` and `C_1` in lines `45-47` match the
complete-event probabilities, and the formula for `R` in lines `49-55` follows
with the correct coefficients.

The sign certificate in lines `57-79` is rigorous. The atanh log interval has a
nonnegative exact rational tail after powers-of-two range reduction; coefficient
signs are handled by reversing interval endpoints when necessary. My independent
replay recomputed the exact Fraction intervals and verified that the replayed
interval lies inside the displayed outer enclosure

```text
[229172119980517/500000000000000000,
 91668847992207/200000000000000000].
```

The lower endpoint is strictly positive, so claim 2 is certified without using
the decimal diagnostics in `conditional.json`.

The proof correctly identifies `R` as an acceleration contribution and not as
the total Hessian. Lines `85-115` derive
`C_1''=-2ww^T/c`, `C_0''=2ww^T/(1-c)` and hence the gradient-times-acceleration
sum equals `R`. Lines `117-132` separately display the weighted conditional
Hessian terms and state that the total full entropy second derivative is in a
strictly negative interval. My replay independently recomputed that interval
and verified it lies within the displayed outer enclosure

```text
[-32529701732259701/500000000000000000,
 -65059403464519401/1000000000000000000].
```

This confirms the object refutes only the nonpositivity shortcut for the
acceleration term, not the full entropy concavity question.

No critical gap was found.

## Evidence limits

This review did not certify the original existential target
`research/A1/frozen_theorem_v1.md`; that target remains marked incomplete in
the frozen file. I did not audit novelty, prior art, or any author/provenance
material. I did not run a search or use finite non-hits as theorem evidence.
No Lean or other formal kernel proof was present or run. The computation here
is limited to exact symbolic replay and rational interval certificates for the
three frozen auxiliary statements above.
