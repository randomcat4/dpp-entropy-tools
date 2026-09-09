# PR62 mathematical first review

Overall verdict: `CORRECT/ACCEPTED_SCOPED` for the analytic rank-one midpoint theorem and its sufficiently small common bit-flip lift. `INCOMPLETE` for independent computation, formal verification, the unrestricted real-kernel target, and the continuous multiring interval target. Novelty/priority is `NOT_ASSESSED`.

I found no mathematical blocker in the frozen theorem proof.

Line citations use the `source-snapshots/pr62/` alias table in `frozen_scope.md`; shorthand citations to a PR62 filename inherit the same frozen head and blob recorded there.

## Claim statuses

| Claim | Status | Reason |
| --- | --- | --- |
| True arithmetic midpoint of two real rank-one kernels is complete-law Shannon midpoint-concave, strict unless the kernels coincide | `CORRECT/ACCEPTED_SCOPED` | The proof keeps the complete atom law, constructs an exact bridge from the averaged endpoint law to the midpoint DPP law, and proves strictly positive entropy derivative on the whole open transfer interval. |
| All rank-one degeneracies, zero coordinates, moving directions, unequal eigenvalues, and equality cases | `CORRECT/ACCEPTED_SCOPED` | The proof separates the rank-two case `m>0` from the collinear case `m=0`, and equality reduces exactly to identical endpoint kernels. |
| Small common independent-bit-flip lift gives strict interior affine chords with an explicit finite-alphabet continuity margin | `CORRECT/ACCEPTED_SCOPED` | The bit-flip generating-function identity gives the lifted DPP kernel, the coupling gives the TV bound, and the cited Fannes-Audenaert finite-alphabet bound gives `G - 2 omega_n(epsilon)`. |
| Six-coordinate rational fixture values and exact script PASS | `INCOMPLETE` as independent computation; author evidence only in C1 | The script and output are source-consistent, but C1 instructions prohibit arithmetic/SymPy reconstruction of the finite certificate. The fixture is not needed for the analytic theorem. |
| Dense 3+3 signed-multiring exact atom/legality setup | `INCOMPLETE` as independent finite evidence; author evidence only in C1 | The prose and script describe exact rational setup checks, but C1 did not independently reconstruct those finite claims. |
| Dense 3+3 signed-multiring line as a family theorem or interval sign certificate | `INCOMPLETE` | The PR itself labels this incomplete and restricts the displayed signs to finite high-precision diagnostics. |
| Unrestricted real-kernel conjecture/counterexample target | `INCOMPLETE` | The README and failure ledger explicitly do not claim it. |
| Novelty/priority | `NOT_ASSESSED` | The prior-art file is a scope audit, not a novelty audit or certificate. |
| Formal verification | `INCOMPLETE` | No Lean or other formal artifact is present or checked in this C1 review. |

## Rank-one midpoint theorem

The theorem is frozen for `n>=2`, unit `x,y in R^n`, and `0<a,b<1`, with `K_- = a xx^T`, `K_+ = b yy^T`, and `K_0 = (K_-+K_+)/2`; it claims complete-configuration Shannon midpoint concavity and equality iff `K_-=K_+` (`source-snapshots/pr62/moving_rank1_theorem.md:L15-L32`, head `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77`, blob `57cf8735a215bba8059e364a0ae905426c2f2873`). The proof defines entropy using the full atom law, not inclusion probabilities (`moving_rank1_theorem.md:L5-L13`).

The rank-one endpoint atom law is correct: empty mass `1-a`, singleton masses `a x_i^2`, and no atoms of size at least two (`moving_rank1_theorem.md:L34-L45`). Averaging the two endpoint laws gives empty mass `1-s`, singleton masses `(K_0)_{ii}`, and no pair atoms, and Shannon concavity gives the endpoint-mixture lower bound (`moving_rank1_theorem.md:L46-L64`). Equality in this first concavity step occurs exactly when the two endpoint atom laws coincide.

For the midpoint law, the spectral form `K_0 = alpha uu^T + beta ww^T` with orthonormal `u,w` gives the complete atom formula

```text
p(empty) = (1-alpha)(1-beta)
p({i}) = (alpha-alpha beta) u_i^2 + (beta-alpha beta) w_i^2
p({i,j}) = alpha beta (u_i w_j - u_j w_i)^2
```

as stated in `moving_rank1_theorem.md:L66-L103`. The Cauchy-Binet identities for the wedge weights `b_ij` and coordinate sums `c_i` are the needed normalization facts (`moving_rank1_theorem.md:L75-L87`).

The mass-transfer path is valid. For `0<=r<=m=alpha beta`, it moves exactly from the endpoint average `q` to the midpoint law `p_{K_0}` (`moving_rank1_theorem.md:L105-L123`). The path remains a probability law: the empty mass is nonnegative because `s=(a+b)/2<1`, singleton masses are nonnegative because `r<=alpha beta<=min(alpha,beta)`, and pair masses are nonnegative. The total mass is preserved by `sum_i c_i=2` and `sum_{i<j} b_ij=1`.

The derivative computation is also correct. Differentiating entropy along `p_r` gives the pairwise logarithmic expression in `moving_rank1_theorem.md:L125-L132`; the constants cancel because `1 - sum_i c_i + sum b_ij = 0`. Lagrange's identity gives the factorization in `moving_rank1_theorem.md:L134-L144`, and

```text
(alpha-r)(beta-r) - r(1-s+r) = alpha beta - r > 0
```

for `0<r<m`. Therefore every active term with `b_ij>0` has a positive logarithm (`moving_rank1_theorem.md:L147-L155`). Since the wedge weights sum to one in the rank-two case, at least one active pair exists, so `dH(p_r)/dr>0` throughout `(0,m)`. Continuity at the endpoints then gives `H(p_m)>H(p_0)` for `m>0` (`moving_rank1_theorem.md:L155-L160`).

The degeneracy and equality discussion is adequate. If `m=0`, the sum of the two positive rank-one matrices has rank one, so the ranges are collinear. Then `p_{K_0}=q`; strictness is exactly strict concavity of Shannon entropy unless the endpoint laws coincide. In the collinear case, that means `a=b`, which is the same as `K_-=K_+` (`moving_rank1_theorem.md:L162-L165`). If the endpoint atom laws coincide but the kernels differ by coordinate signs and are not collinear, then `m>0` and the bridge supplies strictness. Zero coordinates cause no issue because any zero-coordinate pair weight has zero contribution.

## Strict bit-flip lift

The lift is a genuine affine chord: `K_sigma^(epsilon)=epsilon I+(1-2epsilon)K_sigma` preserves the midpoint relation and places every eigenvalue in `[epsilon,1-epsilon]` for `0<epsilon<1/2` (`moving_rank1_theorem.md:L167-L187`). This establishes strict interior legality without changing to a curved path.

The independent-bit-flip identification is correct. If a bit originally equal to 0 contributes `(1-epsilon)+epsilon z_i` and a bit originally equal to 1 contributes `epsilon+(1-epsilon)z_i`, the complete probability-generating polynomial transforms as written in `moving_rank1_theorem.md:L223-L244`, producing exactly the DPP law for `epsilon I+(1-2epsilon)K`.

The TV and entropy margin are correctly scoped. Under the natural coupling, the original and flipped configurations differ only if at least one bit flips, so the TV distance is at most `delta_n(epsilon)=1-(1-epsilon)^n` (`moving_rank1_theorem.md:L246-L248`). Audenaert's primary paper states the finite-dimensional sharp entropy continuity bound, reduces it to classical probability distributions, and uses TV distance `T=(1/2)sum_i |p_i-q_i|`; after changing from base-2 logs to natural logs, this is the bound used in `moving_rank1_theorem.md:L201-L220` and `L246-L256`. Because `omega_n(epsilon)->0` as `epsilon->0`, every distinct rank-one chord has sufficiently small strict lifts satisfying `2 omega_n(epsilon)<G`.

## Six-coordinate fixture

The fixture is correctly presented as an executable certificate for one explicit six-coordinate example, not as the proof of Theorem 1. The theorem document gives the Householder data, endpoint scalars, boundary gap, epsilon, certified lifted lower bound, and actual evaluated lifted gap (`moving_rank1_theorem.md:L258-L299`). The saved output reports the same data and positivity margin (`source-snapshots/pr62/output/verify_rank1_midpoint.txt:L1-L21`, head `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77`, blob `3429b53381dec9ca952cc977584bb2defe9da633`).

Because this C1 review is source/evidence-only, I do not certify the displayed rational and high-precision numerical values independently. If the integration gate requires independent computational acceptance of the fixture itself, the source-bound C2 task is: independently reconstruct the complete atoms and bit-flip law from the literal matrices and formulas in `moving_rank1_theorem.md:L258-L299`, not from an author-script rerun; use the author script and saved output only as comparison records. C2 should certify rational atom/channel identities and rigorous outward logarithm enclosures for `G`, `omega_6(1/1000)`, and `G-2 omega_6(1/1000)>0`. A high-precision rerun alone does not establish a strict certified sign.

## Multiring fixture and issue #61 handoff

The multiring document is explicitly marked `INCOMPLETE`; it says the exact setup and finite evaluations are valid but no interval-family sign theorem and no counterexample are claimed (`source-snapshots/pr62/multiring_fixture.md:L1-L5`, head `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77`, blob `5ddc8b57959e655ba921ca3b6849d85457d325e6`). The line, Schur-complement legality claims, complete-event quartic representation, and full Hessian formula are presented in `multiring_fixture.md:L6-L140`; in this C1 review, those exact finite setup claims remain pending independent finite reconstruction. Separately, the diagnostic section states that the logarithms are 110-digit evaluations, not outward-rounded interval certificates, and the final scope section says these signs do not prove `H''<0` between sample points or for other choices of `A,C,B` (`multiring_fixture.md:L142-L176`).

The saved output preserves that status: it prints `MOTIVATED_110_DIGIT_DIAGNOSTIC_NOT_INTERVAL_CERTIFICATE`, lists exact setup checks, reports the twelve sampled points, and ends with the nonclaim that finite diagnostics do not prove an interval or family theorem (`source-snapshots/pr62/output/probe_multiring_fixture.txt:L1-L16` and `L83-L91`, head `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77`, blob `595f3680b4caa95765f25b6c50f61dff4a2f40ae`). No diagnostic point is being promoted to a theorem in the PR text.

## Scope and prior art

The README and theorem scope agree: the accepted theorem covers rank-one endpoint chords, including moving frames, unequal endpoint eigenvalues, zero coordinates, and dimensions `n=4,5,6`; it does not cover arbitrary rank-two endpoints, moving rank-three frames, large lifts, or the unrestricted real problem (`source-snapshots/pr62/README.md:L6-L19`, blob `7aed571e22e5b4637949daf53ff3a5f29fa8707f`; `moving_rank1_theorem.md:L301-L310`). The failure ledger repeats the same remaining gaps (`source-snapshots/pr62/failure_ledger.md:L43-L49`, blob `19811a3728f33829fffbe2f5cc6b7282a073545c`).

The prior-art file correctly separates route A from route B and expressly denies novelty certification (`source-snapshots/pr62/prior_art.md:L1-L3`, head `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77`, blob `2395efc17869c325217a04ed0fdc8000d6791c9b`). Its cited accepted-main boundaries are consistent with the accepted PR54 scope: PR54 gives local near-decoupling and simple-endpoint results but not whole-chord concavity (`source-snapshots/accepted_main/docs/verification_round3_20260909/accepted_pr54.md:L7-L29`, accepted base `9dcb6e9079ca57f94e0e30d63161cda89ca61fae`). The accepted-main RESULT also records that open PR43 claims were not premises (`source-snapshots/accepted_main/research/I05-23-20260909/RESULT.md:L7-L12`).

Novelty/priority was not audited in this review. The proof is elementary and source-distinct from the cited Shepp-Olkin eigenvalue-count theorem, but I did not perform an exhaustive literature search or certify priority. The PR's own statement that correctness and novelty require separate review should remain in force (`prior_art.md:L74-L94`; `moving_rank1_theorem.md:L308-L310`).

## Final recommendation

Accept PR62 only in the scoped sense:

- The analytic rank-one midpoint theorem and small strict bit-flip lift are correct.
- The six-coordinate fixture and both output files remain author computational evidence unless C2 independently reconstructs the finite certificate from the literal matrices/formulas with rigorous bounds.
- The dense multiring exact setup remains pending independent finite evidence; its sampled signs are diagnostics only. The continuous multiring target, unrestricted real-kernel target, and formal verification remain incomplete. Novelty/priority is not assessed here.
