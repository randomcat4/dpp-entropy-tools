# D10-H13 independent frozen-data audit

## Layered verdict

- **CORRECT — frozen accounting and strongest-point reconstruction.** The four ledgers contain exactly 20,004 entries: 20,000 proposal entries and four explicitly repeated source entries. No entry has positive stored curvature/gap or rho >= 1. The strongest saved case independently reproduces at 120 decimal digits. Exact rational LDL proves its direction positive definite and the requested entire small affine chord strictly feasible.
- **SCOUT — finite search and H10–H13 profile.** The profile is consistent with attenuation farther into the spectral interior. It proves neither monotonicity, a boundary law, optimality over centers, nor entropy concavity.
- **INCOMPLETE — full seed regeneration, all-proposal high-precision reconstruction, and remote provenance.** No search/gate module was imported or executed. The four seed trajectories were not regenerated. The README's statement about remote/local hash matching and remote directory removal is not independently verified here.

These verdicts concern the hashes in `fresh_audit.json`, not later modifications. The mathematical sign checked is H'' in the frozen direction, not the full Hessian's definiteness.

## Frozen versions and reproducibility

Principal SHA256 values:

| Artifact | SHA256 |
|---|---|
| strongest NPZ, shard 0 | `7d7cc5ffb5898025f420b50e4223c69c14c0393783171cdcbdd21c2554d5c82e` |
| source NPZ | `8c842a895aef3cec017b3148a404bd6195e78d3f64ebb77d383f7f9003ddbd3d` |
| `spectral_basis_refine.py` | `28ae523c10184dc1effe2f857adbdad4156683292f2ad7da2d281e2af6ad7268` |
| `commuting_spectral_search.py` | `dd55e9f05afd128a4e64e06ab705ba031fb0f32f0ea4a44a0169b625b9050a37` |
| author recheck JSON | `4b6dab551e531b17780c303608c24fa22861484f493ab0b4b4143d4037ddd1c2` |
| README | `12b7f2c16f7e776c56cd52d34cb6143d092927bca7dfd1adbdd2ce07d785d53d` |
| independent audit script | `0cc9bbbb4ba57b3b394f44b4970bcbf775ec55644c4dfc79c4c0524ba7b6094b` |

JSON records every root file and all 16 shard data files, full exact rational LDL pivots, exact-decimal K/D arrays, and supporting profile hashes. Every frozen file remained unchanged during the final replay.

Command, from the repository root:

```powershell
& 'C:/Users/UIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' research/R3/deepening_10h/dense_hessian/commuting_spectral/results_server_round21_interior3/verifications/fresh_audit.py
```

The standalone script uses numpy only for NPZ input and explicitly labelled float diagnostics. All determinant/entropy reconstruction uses an independent Decimal implementation; all feasibility checks use Fraction. BLAS thread limits are one. Final replay: exit code 0, 22.31 seconds. An earlier successful replay before extra profile/progress checks also returned exit code 0 in 22.08 seconds.

Discovery/version note: an initial read of README failed because that file had not yet appeared (shell exit code 1, no mathematical check executed). It was present at final replay, was read fully, and its hash above is included. This is not a silent endorsement of a moving version. No author file was edited.

## Complete accounting

Each ledger has indices -1,0,...,4999 with no omission or repetition of an index. Index -1 is `source_base`. Each log has exactly 1,000 progress records at completed=5,10,...,5000 plus a final manifest identical to the corresponding manifest file. Every running best in those 1,000 records agrees with the ledger-prefix maximum. The accepted counts exclude the source, as the implementation intends.

| shard | seed | proposals + source | accepted proposals | best index | best rho |
|---|---:|---:|---:|---:|---:|
| 0 | 2026090874 | 5000 + 1 | 1188 | 70 | 0.5313886643536545 |
| 1 | 2026090875 | 5000 + 1 | 1279 | 140 | 0.5139125403080159 |
| 2 | 2026090876 | 5000 + 1 | 1262 | 308 | 0.5291758946384805 |
| 3 | 2026090877 | 5000 + 1 | 1277 | 4912 | 0.5208749979891850 |

All manifests report exit code 0 and positive_count=0. All 20,004 stored statuses are NO_HIT; both stored PSD and unrestricted ratios are <1, all stored total curvatures are negative, all stored gaps are negative. The largest gap is -0.001076903693402187. These are counts of entries, not a proof that all centers are distinct or that every entry was independently recomputed.

Source spectrum margin 0.12 is directly checked from its NPZ. The basis and affine spectral contraction of the H10 strongest NPZ reproduce exactly in numpy. Every proposal has stored margin >=0.09999999999999998. The difference of approximately 2e-17 from 0.10 is consistent with evaluating 1-0.9 in float64, not a substantive violation of the clipping design. The exact frozen rational matrix is not claimed to have margin exactly 0.10; its rigorously certified margin below is 1/2000.

## Search semantics review

For an event S, let M_S=K-I_(S complement). Multilinearity in the absent diagonal entries gives

`(-1)^|S complement| det M_S = sum_{T subset S complement} (-1)^|T| det K_(S union T)`.

This is exact-event probability, not the inclusion probability det K_S. For a symmetric projector basis E_a, the code's score is tr(M_S^-1 E_a), and the log-determinant Hessian is -tr(M_S^-1 E_a M_S^-1 E_b). Consequently its Fisher and acceleration matrices represent

`F_ab=sum p s_a s_b`,

`A_ab=-sum p log(p) [s_a s_b-tr(M^-1 E_a M^-1 E_b)]`,

and the entropy Hessian is A-F. The tensor `einsum("ij,kj->jik",basis,basis)` indeed produces the rank-one column projectors. Whitening the Fisher matrix gives the unrestricted generalized Rayleigh maximum. A same-sign top vector is feasible in the positive-rate cone.

The positive-rate optimizer is heuristic in general: log-rate clipping and finite Adam iterations do not establish a complete positive-cone optimum when the top unrestricted vector has mixed signs. No such completeness is asserted here. The selected strongest entry has a same-sign unrestricted maximizer, and its saved positive direction attains the reported ratio to numerical precision. `positive_count` explicitly includes the source and tests both ratio and actual chord; the independent accounting additionally tests raw positive signs, below the author's reporting thresholds. No silent omission affecting the frozen ledger count was found.

## Independent 120-digit reconstruction

We first symmetrize the saved float matrices as `(X+X.T)/2` in numpy, then interpret each shortest decimal string as an exact rational. This is the author's explicitly stated frozen-point convention and is fully recorded. It is not identical to interpreting each original float as an exact dyadic number.

For every one of the 4096 principal subsets, the independent script computes the determinant jet of K_A+tD_A through order two, using truncated-polynomial elimination. It then applies full Boolean Möbius subtraction to all three coefficients. Thus p,p',p'' come directly from inclusion probabilities. An independent pivoted determinant implementation evaluates all 4096 signed-event determinants at the center; maximum disagreement with Möbius atoms is 1.70905e-120. Normalization residuals are approximately 4e-119, 1.119039e-118, and -7.577e-119 for p,p',p'' respectively.

With natural logarithms:

`F=sum (p')^2/p`, `A=-sum p'' log p`, `H''=A-F`, `rho=A/F`.

| quantity | independent value (rounded) |
|---|---:|
| H | 7.959951776957553551048354624 |
| Fisher | 119.810871536744122688221032858 |
| acceleration | 63.666139000957678382440109909 |
| H'' | -56.144732535786444305780922950 |
| rho | 0.531388664353653984599382046 |
| minimum exact-event atom | 5.735451636623712213178448736e-7 |

The author's 50/80-digit values agree with these results at their reported precision. Decimal calculations here are high-precision replay, not an outward-rounded interval proof of logarithm error; no invented error bar is attached. The large separation from zero and agreement of distinct event constructions support the stated stable-negative reconstruction verdict.

For actual entropy chords, the independently derived signed-event formula is evaluated at both endpoints, at 120 digits. Gap means `(H(K-tD)+H(K+tD))/2-H(K)`; a positive value, not a negative value, would be the target anomaly.

| t | actual midpoint gap | 2 gap/t² |
|---|---:|---:|
| 1/200 | -0.000701914485868101594675306 | -56.1531588694481275740 |
| 1/1000 | -0.000028072534647714980506446 | -56.1450692954299610129 |
| 1/10000 | -0.000000280723679516309387229 | -56.1447359032618774459 |

All three steps lie within the exactly certified chord interval. The central differences converge to the independently reconstructed negative H''.

## Exact feasibility, direction, and scope

Fraction LDL without pivoting has 12 strictly positive exact pivots for D and for each of

`K ± D/200 - I/2000`, `I-K ∓ D/200 - I/2000`.

Rounded minimum pivots (not eigenvalue bounds):

| test | minimum pivot |
|---|---:|
| D | 0.9371876266596245 |
| K-D/200-I/2000 | 0.16077584385122906 |
| I-K+D/200-I/2000 | 0.19763445413827305 |
| K+D/200-I/2000 | 0.17539457729826224 |
| I-K-D/200-I/2000 | 0.1816650212582473 |

The full positive Fraction pivots in JSON, not their floating minima, certify positive definiteness by LDL congruence. Convex interpolation between the two endpoint matrices proves `I/2000 < K+tD < (1-1/2000)I` for every real |t|<=1/200. D has rank 12. This is an exact K-affine real-symmetric chord.

Floating diagnostics give commutator Frobenius norm 2.58e-15 and reconstruction discrepancies below 1.8e-16 from the stored spectral pair. The exact decimal reconstruction need not commute *exactly* after serialization/symmetrization. We certify the exact real-symmetric PSD-direction chord and numerical agreement with the intended fixed-Q construction; we do not silently certify exact algebraic commutation of the rounded matrices.

## H10–H13 comparison and remaining blocker

The script reads the four saved best metadata files of each batch and selects each maximum, recording its hash. Earlier batches' whole ledgers are not re-audited here.

| batch | best-point observed spectral margin | best rho |
|---|---:|---:|
| H10 | 0.015371444079016916 | 0.5746069386526107 |
| H11 | 0.02171078114876157 | 0.5745947308664667 |
| H12 | 0.05 | 0.5729410207438331 |
| H13 | 0.09999999999999998 | 0.5313886643536545 |

This finite profile shows a visibly weaker mechanism at the deeper interior best point, while retaining substantial positive acceleration. It does not compare global constrained optima, hold all other parameters fixed, or prove monotonicity. The threshold for positive total curvature is still rho>1, well above every value here. The next evidentiary gap is full seeded trajectory regeneration if provenance completeness is required, or a new analytical bound if a general statement is intended; simply increasing a finite denominator does not close that gap.
