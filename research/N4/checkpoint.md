# N4 checkpoint — 2026-09-09

Latest state: round two is also `STOPPED_SUBSTANTIVE`; see its
[checkpoint](round2/checkpoint.md), [verdict](round2/verdict.md), and
[execution ledger](round2/run_ledger.md). The current remaining obligation is
the fixed-face cross-layer entropy budget. The first-round checkpoint below
is preserved as historical evidence, not as the latest restart proposal.

State: `STOPPED_SUBSTANTIVE`. Global real-kernel concavity: `INCOMPLETE`.
Public collaboration: issue #21 and Draft PR #23. No automatic retry/heartbeat.

## Completed work and coverage

| Unit | Retained research evaluations | Affine chords | Result |
| --- | ---: | ---: | --- |
| P1: K4/diamond gauge classes | 36 | 108 | no positive candidate |
| S1: moving frames and unequal scales | 160 | 960 | no positive candidate |
| S2: rare-scale and soft-column probes | 24 | 216 | no interaction amplification |
| S3: strong-coupling gain optimization | 294 | 2646 | near-unit gain explained by shared Fisher mode |

Total 514 evaluations and 3930 chords, not unique matrices. Optimizer repeats
are included. Self-tests, precision replays, independent certificates and failed
attempts are separate denominators.

M1 supplied the exact mixed-Hessian/singular Schur gate. M2's simultaneous
radial-column and central-block concavity theorem received a frozen-object
non-author CORRECT review. P2's conditional separated-scale exclusion also
received CORRECT; its rational benchmark's two limiting Hessians were certified
strictly negative by rational logarithm intervals. V1 independently certified
three strictly negative rational affine chords. No positive-gap certificate exists.

## Substantive stopping reason

The radial theorem fixes leaf marginals and each connection direction.
For arbitrary nonradial directions the conditional centers separate along
b_j b_j^T, while the gradient difference is tested against e_j e_j^T.
The proved radial sign no longer applies. For two chosen column directions,
let c_j be conditional-Hessian costs, a_j conditional acceleration, and m the
mixed Hessian. The exact remaining obligation is

`c_j-a_j>=0`, and
`c3*c4-m^2 >= c3*a4+c4*a3-a3*a4`,

with M1's singular kernel compatibility conditions. This is an equivalent
remaining sign problem in that restricted space, not a newly proved lemma.
General directions also vary central and leaf blocks.

Distinct soft-scale and strong-coupling attacks did not refute or prove it.
S3's largest gain .9989720185 comes from the full-inclusion event's large
rank-one Fisher term. Deleting it leaves a positive negative-Hessian residual
in an 80-digit author diagnostic, minimum eigenvalue about 2.4331. This is
a point diagnosis, not a universal boundary theorem. There is no current
mechanism-based reason to expand the same scan or move to n=5..8.

The smallest useful new unit would prove/refute the mismatched-gradient budget
using actual DPP constraints, or supply a boundary tangent object with an
indefinite residual after common divergent Fisher terms are removed. A fresh
literature/direction reassessment should precede any restart.

## Frozen evidence and operational state

- Baseline fa504ec74e16843fafc395880d7ba99b4c1d2129; bundle SHA256 matches
  e8305bf822329d8a6fd001facefbed4fc24c0e71c755a7eb10910aed0bcb87b7.
- P2: commit 1abc7408b92831fddad6e2defde8daa2529daac3, proof blob
  3971f764b66716445f4df3b3c13499ef0566c7d7.
- M2: child commit 03a2424555f599d4cdfcb3f4a2533e5008c56d60, proof blob
  c9e710944f43215a57efcf12a158b272f47cdef5.
- Search child final 91c8b45; independent review 4690863 plus archival b9fe5d3.
- Successful research PIDs 157823,158332,158733,159251 ended. Failed search
  PID159210 ended. Precision diagnostic PID159599 ended.
- Review PIDs158760,159181,159490 ended. Large-denominator attempt observed
  as Python158898 with parent158897 was terminated; no certificate or reliable
  script self-reported exit/PID was retained for that attempt. See review ledger.
- Exactly three child contexts were used without descendants. All child research
  and route-owned computations have ended. Unrelated jobs were not stopped.
- Results are in research/N4 on the route branch and isolated child branches.
  No uncommitted research result is intentionally omitted. Private transport
  files remain outside the public repo.

The finite certificates, scoped proofs, global status and novelty have separate
judgements in verdict.md. No unrestricted-concavity claim is certified.
