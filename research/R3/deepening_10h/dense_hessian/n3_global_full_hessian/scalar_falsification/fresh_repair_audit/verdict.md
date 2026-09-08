# U10c repaired scalar search: fresh non-author recheck

STATUS: **SCOUT — independently reconstructed finite evidence, with metadata
corrections required.** No global theorem or full-domain claim is certified.

This reviewer did not author U10c. The implementation in audit.py imports
neither the author search nor any earlier audit/research implementation.
The author script was read only to extract the fixed rational orthogonal
basis and deterministic parameter grids. The repaired compact ledger and
local candidate artifact were the frozen data inputs.

## Main result

The corrected high-precision values reproduce:

| case | independently reconstructed rho |
|---|---:|
| theta=.99, epsilon=10^-96, rates (1,1) | 0.99509994460201969229112579538559592802217186504829290476… |
| theta=.5, epsilon=10^-96, rates (2,3) | 0.99325250311940130939025336008385825478443438818613575443… |
| highest apparent float threshold, same stored K | 0.50000000000000000000041666666666666662028936845376798740… |

Both complement partners of the first two cases give the same mathematical
scalar. Across all 140 complement pairs the largest numerical discrepancy
is 6.39e-215; a numerical ordering between these tied partners is not a new
maximum mechanism. The complete repeated results, not just the table, are
in results.json.

The independent run has **445 attempts, 444 valid strict kernels, one exact
nonstrict rejection, and zero reconstructed rho>1**. The smallest remaining
gap at the best valid point is about 0.004900055398, not a rounding-floor
positive signal. Decimal logarithms and solves are high-precision numerical
checks, not interval certificates for rho.

## Frozen input hashes

| file | SHA256 |
|---|---|
| repaired author script | `51cb756953df0827eaf653a07ab629946ad553ac000b310988d6b18fd559f580` |
| compact search ledger | `a5dfe862e6cc7d6b8c37768db61082e8df0ab62a835c35777235002040826036` |
| candidate artifact | `e4f1d053be458f29fc9dad94b3bc44dde168b4ae9bb907af2ab68af9b7702583` |
| author verdict | `8c90b704bc922f48cfe76485d90d7a3904119b2f0ef48c5934b24800685d1e26` |
| independent audit.py | `4d87b51f26b8338086a0f2766a4ad9682b585915557fc250f2f4c1648a09db33` |

The input files remained unchanged between the beginning and end of the
reconstruction. The JSON also binds the repair-status and run-log hashes.
These findings attach to the frozen versions, not subsequent edits.

## Independent mathematics and the repaired p0 jet

In the observation coordinate order (11,22,33,12,13,23), define
M_S=K-I_(S complement). The independent implementation calculates

p_S=(-1)^|S complement| det M_S,

dp_S[D]=(-1)^|S complement| tr(adj(M_S) D).

Thus an off-diagonal coordinate derivative is twice the corresponding
adjugate entry. Each atom and each of its six first derivatives is also
rebuilt separately from principal inclusion minors using full Boolean
Möbius subtraction. The two constructions agree exactly as Fractions at
every attempted kernel, and sum_S dp_S=0 exactly in all six coordinates.

In particular

dp0=(-1,-1,-1,0,0,0)+dq12+dq13+dq23-dr.

The constant -1 applies only to diagonal coordinates. An all-six-coordinate
-1 would fail the exact normalization-jet test in the last three entries.
The repaired p0 jet is therefore checked through two independent algebraic
representations, not accepted from the repaired source line alone.

The independent Fisher matrix is the exact-rational sum
F_ij=sum_S (partial_i p_S)(partial_j p_S)/p_S, converted to Decimal only
for the subsequent logarithm-dependent computation. It reconstructs

l12=log(p0 p12/(p1 p2)), l13, l23 analogously,

Lambda=log(p123 p1 p2 p3/(p0 p12 p13 p23)),

N=-diag(l23,l13,l12)-Lambda K,

eta_i=tr(N^-1 E_i),

A_ij=F_ij+det(N)tr(N^-1 E_i N^-1 E_j),

rho=det(N)eta^T A^-1 eta.

E_12 has ones in both symmetric entries; this retains the factor two in
eta and the correct Frobenius/coordinate conversion. Each solve has an
explicit residual check. Positivity of K and I-K is checked with exact
Fraction principal minors. N's principal minors are checked at high
precision; this is not presented as an independent interval proof of N>0.

The largest two requested cases use 372 and 756 decimal digits respectively;
other extreme grids use up to 1716 digits. The rational-Q family is built
with exact fractions 1/3 and 2/3, not the author's finite-decimal rounded
thirds. Agreement with every retained boundary comparison is better than
1e-40 in rho. Stored successful top/path rows agree better than 1e-50.

## Denominators, rejected points and compact-ledger limitations

The six compact route records sum exactly as follows:

| route | attempted | accepted by float screen | rejected |
|---|---:|---:|---:|
| L-ensemble atom boundaries | 564 | 429 | 135 |
| unequal soft rates | 5400 | 1960 | 3440 |
| disconnected/sign-mixed edges | 3672 | 3552 | 120 |
| spectral corners | 6000 | 5594 | 406 |
| biased interior | 6000 | 6000 | 0 |
| targeted local hill | 16800 | 4488 | 12312 |
| total | 38436 | 22023 | 16413 |

Every route's rejection-reason subtotals agree. The local top-25 list is
the exact prefix of the top-40 artifact. These are **compact-accounting
checks**, not independent regeneration of all 38,436 float trajectories.
The artifact does not contain every raw proposal. Consequently actual
full float seed regeneration and raw-proposal validation remain INCOMPLETE.
The phrase “accepted strict kernels” must be read as “accepted by the float
screen,” not a rigorous certificate for every accepted serialized matrix.

The high-precision denominator is independently rebuilt in full:

- 15 stored top-float attempts: 14 valid, one exact nonstrict rejection;
- 280 boundary probes: 4 theta values × 5 epsilon exponents × 7 rate pairs
  × 2 complement choices, all independently regenerated and evaluated;
- 150 path probes: 5 diagonal tuples × 5 edge-weight pairs × 6 exponents,
  all present without duplicate parameter records and independently evaluated.

The 280 complete boundary records were not all retained in the original
candidate artifact, so this audit reconstructs that fixed grid from its
parameters and stores all 280 outputs. It does not mistake the retained
top-40 list for the complete denominator.

The rejected top-float point is source_rank_float=10. Its exact decimal-
rational full-event atom, also det K, is

`-107527435613099183/1562500000000000000000000000000000000000000000000000`.

It is negative. The original repaired artifact already records this as
`nonpositive_atom_decimal`; the independent rejection confirms it. It is
neither a missing result nor an admissible positive-rho candidate.

## Float false threshold and metadata corrections

The stored float value 0.9999999999875521 belongs to a near-disconnected
path. The exact-rational reconstruction has Lambda=0 and N diagonal entries
approximately (2e-10,1e-20,2e-10); its rho is the .500000… value above.
The float artifact instead has Lambda about 6.66e-16 and reports a minimum
N eigenvalue about 1.36e-26. This is a severe conditioning hazard, not a
credible threshold crossing. The corrected p0 jet and higher precision
recover the stable value well below one.

Three metadata clarifications are needed in the frozen author prose:

1. The verdict says **54** near-threshold rho>.95 records. The frozen
   compact ledger says **69**, and this independent full 445-attempt
   reconstruction also gives **69**. The ledger is correct on this count;
   the prose is stale.
2. “15 top-float checks” is an attempts count, not 15 successful strict
   kernels. One is the explicit rejection above.
3. The verdict's elapsed time 27.63113284111023 seconds differs from the
   frozen ledger/run-log 27.824203968048096 seconds. Timing is provenance
   metadata, not evidence affecting the mathematical ratios.

None of these is silently repaired in author files by this reviewer.

## Final scope

The p0-jet repair and the three highlighted finite numerical claims survive
fresh reconstruction. There are zero credible rho>1 points in the valid
reconstructed set. This is **SCOUT only**, with the exact limitations above.
It does not prove rho<=1 globally, strict full-Hessian negativity throughout
the kernel domain, complete float-scout coverage, or a rigorous interval
bound for every reported Decimal ratio.
