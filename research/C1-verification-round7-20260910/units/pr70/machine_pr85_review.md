# PR85 machine finite-gate source/evidence review

Overall verdict: `ACCEPTED_SCOPED` for the fixed PR70 P2/P5/P6 machine evidence packet. I found no source-level blocker in the raw implementation, input, output, or execution evidence for the single fixed object. This is C1's source/evidence FIRST verdict on the actual independent raw evidence: the fixed P2/P5/P6 finite gate is closed at this evidence level. The PR85 `MACHINE_PASS` status is raw machine data and does not by itself supply a reviewer verdict. Independent SECOND review is outside this report.

The earlier analytic PR70 report remains unchanged: analytic identities and reductions were accepted at source-review level; universal one-sided sign, paired full-entropy determinant sign, and the general real three-point theorem remain incomplete.

Combining that analytic interpretation with this fixed finite closure, the fixed negative paired-resolvent second derivative supports a local counterexample to the auxiliary complement-paired resolvent convexity route. The P5 and P6 checks remain fixed-object signs on one legal direction: they do not refute full-entropy concavity.

Public alias: `source-snapshots/pr85_machine/...`

Immutable URL base: `https://github.com/randomcat4/dpp-entropy-tools/blob/611d5f70e8bb70237755ca4fdbe8ab14c8b715c1/research/C2/pr70_obstruction52/`

## Binding and scope

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `SOURCE_BINDING.json:2-13`, `SOURCE_BINDING.json:48-115`, `SOURCE_BINDING.json:120-616`, `execution/RUN_PLAN.md:5-13`, and `execution/RUN_LEDGER.json:2-31`.

The raw packet is bound to machine head `611d5f70e8bb70237755ca4fdbe8ab14c8b715c1`, preparation head `29d4d77d7dba65de933d196a89b4db2616234991`, and frozen author head `f7be60759fd4d65184803b6585965dc7e5ccd624`. The binding records 77 public files, with the two top-level interpretation files excluded and 75 raw implementation/input/output/execution files available for review. It also records that implementation and inputs are unchanged since preparation.

The scope is the fixed PR70 paired-resolvent object only. Issue73/74 scans, other K/D/tau values, author scripts, old certificates, universal signs, and mathematical reviewer verdicts are excluded.

## Fixed input contract

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `inputs/object.json:2-53`, `outputs/run01/input_echo.json:2-53`, `inputs/expected.json:2-32`, and `inputs/REQUEST.md:1-47`.

The input echo matches the fixed source head, exact rational `K`, exact rational `D`, `tau=1/100000`, mask order `0..7`, selected bit mask 4, natural logarithms, N=80 atanh terms, and maximum interval width `1e-32`. The expected-literal file is explicitly marked as comparison targets transcribed from the frozen author source and not used to construct computed quantities.

## Independent construction coverage

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `implementation/README.md:3-11`, `implementation/independent_pr70_checker.py:18-19`, `implementation/independent_pr70_checker.py:102-154`, `implementation/independent_pr70_checker.py:291-324`, and `outputs/run01/CHECKS.jsonl:1-47`.

The checker source uses standard-library exact rationals and fixed constants N=80 and width `1e-32`. It independently constructs inclusion minors by permutation expansion and complete signed events by a separate Laplace determinant route. The output schema records both Mobius event polynomials and signed event polynomials, all eight jets, marginal polynomials, marginal jets, independent two-leaf polynomials, and normalization. The checks ledger covers dual event construction, positivity at the center, leaf marginal dual construction, full polynomial normalization, jet normalization, and every literal atom derivative.

I did not recompute those objects, but the source and raw gates cover the required finite obligations rather than merely reporting an aggregate pass.

## Legality and segment evidence

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `implementation/independent_pr70_checker.py:327-346`, `outputs/run01/legality.json`, `outputs/run01/three_point_probabilities.json`, and `outputs/run01/CHECKS.jsonl:48-110`.

The code evaluates `K-tau D`, `K`, and `K+tau D`, and also their complements. The raw legality file records leading Sylvester minors for all six cases. The checks ledger separately verifies positivity and literal equality for each minor, then verifies probability normalization and positivity for each endpoint/center atom. Endpoint positive definiteness for both `K` and `I-K` supports the claimed legal affine segment by convexity of the positive-definite cone.

## P2 paired-resolvent certificate

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `implementation/independent_pr70_checker.py:351-369`, `outputs/run01/phi_rows.json`, `outputs/run01/phi_exact.json`, `outputs/run01/intervals/Phi_pair.json`, `outputs/run01/CHECKS.jsonl:111-123`, and `inputs/expected.json:14-19`.

The implementation computes each side through quotient jets and separately checks the displayed P3 formula row by row. It emits eight P3 rows, exact `Phi0`, `Phi1`, and `Phi_pair` forms, exact agreement gates for all three P2 fractions, a broad negative-sign gate for `Phi_pair`, and a separate literal-containment gate for the printed P2 decimal interval.

Compact displayed interval reviewed: `Phi_pair` lies inside `[-4.8046265619871114230253298325745148413179, -4.8046265619871114230253298325745148413178]`, which is strictly negative and contained in the author printed interval.

## P5 curvature signs and full-term retention

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `implementation/independent_pr70_checker.py:262-270`, `implementation/independent_pr70_checker.py:371-417`, `outputs/run01/side_0_terms.json`, `outputs/run01/side_1_terms.json`, `outputs/run01/curvature_exact_forms.json`, `outputs/run01/curvature_components_intervals.json`, `outputs/run01/intervals/G0.json`, `outputs/run01/intervals/G1.json`, `outputs/run01/intervals/negative_Hconditional.json`, `outputs/run01/intervals/negative_Hfull.json`, `outputs/run01/CHECKS.jsonl:124-158`, and `inputs/expected.json:20-23`.

The implementation keeps the full entropy, leaf marginal entropy, conditional entropy, Fisher terms, acceleration terms, side terms, and retained `P''` contributions visible in raw artifacts. It differentiates side entropies both as `r log(r)-r log(P)` and as `P q log(q)`, then gates rowwise and total agreement. It separately gates the structural identity `-Hconditional''=G0''+G1''`.

Compact displayed intervals reviewed:

- `G0`: `[6.3836477267924650532084343120505471181471, 6.3836477267924650532084343120505471181472]`.
- `G1`: `[9.2177300388618574492302078622332257604485, 9.2177300388618574492302078622332257604486]`.
- `negative_Hconditional`: `[15.6013777656543225024386421742837728785956, 15.6013777656543225024386421742837728785957]`.
- `negative_Hfull`: `[41.8563777656543225024386421742837728785956, 41.8563777656543225024386421742837728785957]`.

The checks ledger contains separate width, broad-positive-sign, and literal-containment gates for each of the four P5 quantities.

## Log interval evidence

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `implementation/independent_pr70_checker.py:177-257`, `outputs/run01/log_inventory.json:2-37`, `outputs/run01/logs/log2.json`, `outputs/run01/logs/log_000.json` through `outputs/run01/logs/log_027.json`, and `outputs/run01/CHECKS.jsonl:135-146` plus `CHECKS.jsonl:159-174`.

The source implements rational atanh log bounds with N=80, normalization `argument=2^k*y`, the stated rational tail formula, and endpoint reversal for negative multipliers. The log inventory records 28 rational log arguments plus `log2`. I inspected every log certificate file for the expected schema: each `log_000` through `log_027` has argument, N=80, normalized series, and interval fields; `log2.json` has N=80 and direct series/tail fields. The checks ledger separately gates all 28 positive log arguments.

I did not inspect or reproduce the huge internal rational term lists in the report.

## P6 Jensen interval and interpretation

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `implementation/independent_pr70_checker.py:419-430`, `outputs/run01/jensen_exact_form.json`, `outputs/run01/jensen_assembly.json`, `outputs/run01/three_entropy_intervals.json`, `outputs/run01/intervals/Jensen.json`, `outputs/run01/CHECKS.jsonl:175-178`, and `inputs/expected.json:24`.

The implementation defines the complete entropy as `-sum p log p` and then constructs `J=[H(K-tau D)+H(K+tau D)]/2-H(K)`. It evaluates the Jensen linear form and also assembles the same interval from the three entropy intervals, then gates overlap, width, broad negative sign, and literal containment.

Compact displayed Jensen interval reviewed: `[-0.0000000020928189192765834280721741836172, -0.0000000020928189192765834280721741836171]`. This is a concave-direction witness for this fixed legal triple. It is not a full-entropy concavity counterexample.

## Execution records

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `execution/run_guard.sh:1-43`, `execution/RUN_LEDGER.json:8-31`, `outputs/run01/start_utc.txt:1`, `outputs/run01/deadline_utc.txt:1`, `outputs/run01/exit.json:1`, `outputs/run01/pid_absence.json:1`, `outputs/run01/environment.json`, `outputs/run01/stdout.log:1`, `outputs/run01/stderr.log`, and `outputs/run01/output_hashes.json`.

The execution record binds `run01` to start `2026-09-10T02:10:08Z`, deadline `2026-09-10T02:20:08Z`, finish `2026-09-10T02:10:10Z`, arithmetic PID `175598`, exit code 0, no repairs, no prior arithmetic attempts, one CPU, 16 GiB memory cap, and no GPU. The post-run PID absence record checks PID `175598` absent at `2026-09-10T02:10:38Z`. `stderr.log` is empty and `stdout.log` reports `MACHINE_PASS` with exit code 0 and elapsed time about 1.155 seconds.

The output-hash manifest records raw output hashes and includes the name of `invocation_private.txt`; the file itself is absent from the public raw tree, matching the ledger redaction note. I treat this as a publication/redaction note, not a mathematical evidence gap.

## Final machine classification

- C1 source/evidence FIRST for the fixed PR70 P2/P5/P6 gate: `ACCEPTED_SCOPED`; fixed gate closed.
- Fixed PR70 P2 fraction gate: `ACCEPTED_SCOPED`.
- Fixed PR70 P5 four-sign interval gates: `ACCEPTED_SCOPED`.
- Fixed PR70 P6 Jensen interval gate: `ACCEPTED_SCOPED`.
- Single-run/deadline/PID/no-retry execution record: `ACCEPTED_SCOPED`.
- Raw machine evidence packet as finite gate closure: `ACCEPTED_SCOPED`.
- Fixed negative paired-resolvent second derivative, combined with the accepted analytic explanation: local counterexample to the auxiliary complement-paired resolvent convexity route.
- PR85 machine `MACHINE_PASS` alone: raw machine status, not a reviewer verdict by itself.
- Independent SECOND review: `OUT_OF_SCOPE`.
- Universal one-sided claim: `INCOMPLETE`.
- Universal paired full-entropy determinant sign: `INCOMPLETE`.
- General real three-point theorem: `INCOMPLETE`.
- Full-entropy concavity refutation: `NOT_SUPPLIED`.
- Novelty: `NOT_ASSESSED`.
- Formal verification: `NOT_PERFORMED`.

No `CRITICAL_GAPS` found within this fixed machine evidence scope.
