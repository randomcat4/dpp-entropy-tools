# PR41 / issue 45 C2 bounded exact verification

Status: PASS for the bounded computational verification unit requested for issue 45.

This report covers exact symbolic identities in PR41. It is not a C1 analytic
review of the full theorem, not a proof-assistant formalization, and not a
novelty review.

## Input

- Frozen source snapshot: `runs/C2/verification3/source41/randomcat4-dpp-entropy-tools-6fd61dc/research/N3/round3/I05-W4-20260909/round2`
- Frozen commit supplied by parent task: `6fd61dcd299417fc3a4eab3af682c03dd816b670`
- Required source files read in full: `frozen_statement.md`, `HANDOFF.md`, `proof.md`, and `code/verify_symbolic.py`
- Extra source files read for manifest and expected output: `README.md`, `CLAIM.md`, `RESULT.md`, `requirements.txt`, `inputs/exact_inputs.json`, and `outputs/verify_symbolic.txt`

## Domain

The checked domain is complete-configuration Shannon entropy for finite DPPs,
with real symmetric 3 by 3 strict-contraction kernels and all six real symmetric
affine directions. Event order is `(0, 1, 2, 12, 3, 13, 23, 123)`.

## Algorithm

The independent verifier in `verify_pr41_independent.py` does not import the
author verifier. It constructs every full-event probability from principal
determinants by Mobius inclusion-exclusion:

`p_K(S) = sum_{T superset S} (-1)^(|T|-|S|) det(K_T)`.

It then differentiates `p(K+tD)` at `t=0` exactly with SymPy, checks first and
second jets, reconstructs the Fisher and acceleration pieces, and compares the
claimed block decompositions and rational/minor certificates. It uses exact
SymPy expressions and rational arithmetic only; no floating point value is used
as proof.

## Dependencies and limits

- Python: `3.12.3`
- SymPy: `1.14.0`
- Source requirement: `requirements.txt:1` gives `sympy==1.14.0`
- Thread limits set: `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`,
  `MKL_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`, `VECLIB_MAXIMUM_THREADS=1`
- Memory cap: `ulimit -v 4194304` KiB
- Timeout: `2700` seconds
- GPU: not used

## Command and outputs

Durable final runner PID: `171670`. Python verifier PID recorded in evidence:
`171674`.

Recovery directory:
`[C2_EXECUTION_ROOT]/verification3/pr41`

Final invocation, as recorded in `logs/invocation.txt`:

```text
[C2_EXECUTION_ROOT]/.venv/bin/python [C2_EXECUTION_ROOT]/verification3/pr41/verify_pr41_independent.py --source-round2 [C2_EXECUTION_ROOT]/verification3/pr41/source41_round2 --out [C2_EXECUTION_ROOT]/verification3/pr41/evidence.json
```

Exit code: `0`.

Stdout:

```text
STATUS PASS
EVIDENCE [C2_EXECUTION_ROOT]/verification3/pr41/evidence.json
```

Stderr: empty.

Machine-readable evidence is in `evidence.json`; copied run logs are under
`logs/`.

## Checklist

| Item | Source lines | Result |
| --- | --- | --- |
| Replay author script as subprocess, without import | `README.md:21-31`, `code/verify_symbolic.py:329-335`, `outputs/verify_symbolic.txt:1-6` | PASS |
| Full-event determinant/Mobius probabilities for R2-T1 | `frozen_statement.md:7-25`, `frozen_statement.md:27-59`, `proof.md:22-50`, `proof.md:52-91` | PASS |
| Strong-family first jets in coordinates `(P, Delta, Z, R, H, N)` | `proof.md:93-122` | PASS |
| Strong-family second-jet log-weight group sums | `proof.md:124-137` | PASS |
| Full Fisher block and scalar terms | `proof.md:139-170` | PASS |
| Acceleration term and combined `G_s`/scalar decomposition | `proof.md:172-213` | PASS |
| `G_s'` matrix, leading Sylvester minors, and `G_0` certificate | `proof.md:215-283` | PASS |
| `sigma=-1` sign conjugation with full direction bijection | `frozen_statement.md:38-48`, `proof.md:281-283` | PASS |
| Rational strong-coupling witness `kappa=1/3` | `frozen_statement.md:61-67`, `proof.md:285-314`, `inputs/exact_inputs.json:4-17` | PASS |
| Two-point conditional entropy algebra identities | `frozen_statement.md:89-95`, `proof.md:316-463` | PASS |
| Block plus isolated point: all eight events, first jets, second-jet marginal cancellations, Fisher split, acceleration cancellation | `frozen_statement.md:69-96`, `proof.md:465-517`, `inputs/exact_inputs.json:19-27` | PASS |
| General missing-edge transform: four `t_ij`, four `T_ij`, Jacobian, inverse transform, and event-adaptive Fisher expression | `frozen_statement.md:108-119`, `proof.md:519-612` | PASS |

## Verified identities

For R2-T1, the independent reconstruction matches the frozen eight probabilities
`((1-s)/8, 1/8, 1/8, (1+s)/8, (1+s)/8, 1/8, 1/8, (1-s)/8)`, the first-jet table,
the three second-jet group sums, the full Fisher formula, the acceleration
formula, and the final `G_s` plus scalar block decomposition.

The `G_s'` certificate was checked entrywise, including the three leading minors:

```text
s*(s**4 - s**2 + 1)/((s - 1)**2*(s + 1)**2)
-s**2*(s**4 - s**2 + 4)/((s - 1)**3*(s + 1)**3)
-48*s**3/((s - 1)**3*(s + 1)**3)
```

On `0<s<1`, these are the same positive quantities as the source formulas with
`D_s=(1-s)(1+s)>0`. The sign step uses the elementary facts recorded in
`evidence.json`, such as `s^4-s^2+1=(s^2-1/2)^2+3/4>0`.

For R2-T2, the independent reconstruction verifies the full eight-event block
factorization and the claimed cancellation of connection directions in the
second-order event sum. It also verifies the two-point conditional entropy
algebra used by the proof: the delta identity, the `2x2` determinant certificate,
and the derivative identity behind `log t <= (t-1)/sqrt(t)` on `t >= 1`.

For the general missing-edge center, the verifier checks only the stated
coordinate reduction: the four conditionals, four direction transforms, nonzero
Jacobian for `bc != 0`, inverse transform, and event-adaptive Fisher expression.

## Failures and limitations

No symbolic identity failed in the final run. An earlier server run, runner PID
`171188` with Python PID `171192`, was interrupted during an overlarge
missing-edge quotient simplification after seven objects had already passed. Its
partial checkpoint was preserved privately as `evidence_slow_interrupted.json`;
this was an implementation-performance issue, not a failed algebraic identity.

Remaining unverified or out of scope:

- General connected missing-edge `6x6` event-weighted inequality.
- General strict real three-dimensional `K`-affine entropy concavity.
- Any strict entropy counterexample.
- C1 full theorem proof review.
- PR41 novelty.
- Proof-assistant formalization.
