INCOMPLETE

# P4-01: connected n=3 numerical attack, terminal report

No object passed the >1e-8 physical-Hessian acceptance threshold with both 90/140-digit evaluations, the independent signed-event directional formula, and a positive finite chord. This finite search does not prove the frozen n=3 concavity conjecture. No self-certification or rigorous interval certificate is claimed.

## Actual denominator and coverage

- Formal seed: 20260908411; n=3, full six-dimensional real symmetric Hessian.
- Continuous unique IDs 1 through 136898: 136898 OK, 0 FAILED, 0 RESERVED.
- 100000 scan calls, 20724 optimization calls, 16174 high-precision Hessian calls; total 136898, below 150000.
- Floating-point center groups: path/general 31426, triangle/general 28501, path/weak 29227, triangle/weak 31570. Their sum is 120724 floating Hessian calls.
- Spectral margin groups: <1e-6: 72085; [1e-6,1e-2): 36238; >=1e-2: 12401.
- 8053 floating objects exceeded 1e-8. Every one received 90- and 140-digit fixed-decimal review. None passed the candidate gate; unreviewed raw positives: 0.
- The first 120894 IDs belong to the original scan/optimization process (including 170 HP calls). A sequential terminal-only audit added 16004 HP calls to the SAME ledger, reviewing the remaining 8002 objects without new search points.

The unit of the capped denominator is one full Hessian objective. Each HP call additionally performs three feasible chord checks and an independent directional calculation: 48522 auxiliary chord checks / 145566 internal entropy evaluations in total. These are not separate sampled kernels. Full-event probabilities, rather than inclusion determinants, enter every entropy formula. All failures would consume a reserved ID; no failure was silently removed.

Smoke runs have separate denominators: 166 and 326 calls, all OK, both exit 0. Three executions of a 24-kernel selftest (local once, remote twice) passed; see selftest.json. Smoke/selftest counts are not included in the formal denominator.

## Best numerical objects, not counterexamples

The largest raw floating Hessian was +0.011970890934984268, source call 110565. Its 140-digit full-Hessian maximum is -1.5376535407716875106934e-14; the alternate directional formula agrees. Its three chord gaps are negative. The large floating positive is not promoted.

Among the HP-reviewed objects, the maximum computed Hessian is approximately -4.518941369616243e-26 (source call 102797, HP call 134754), a nearly disconnected but connected path. Spectral margin is approximately 1.4557853311637713e-12. For this object, the three finite-chord gaps are approximately -1.04271819e-53, -7.70763594e-52, and -1.39853229e-49. The full kernel, 140-digit direction and chord steps are in formal/audit.json under best_hp and best_hp_source.

Its exact saved decimal midpoint is the integer matrix

```
[[ 9376944826562887600000000000,             -1243601463824071,                             0],
 [            -1243601463824071, 30707893957809128000000000000, -14787683526906505600000000000],
 [                            0,-14787683526906505600000000000,  16466520818751368000000000000]]
```

divided by 40000000000000000000000000000. Here "fixed decimal" means the exact decimal strings saved from floating inputs, not their binary dyadic expansions. Near-zero negative numbers and floating positives are not mathematical certificates.

The parent-provided S3 near-identity probe was also recomputed at both precisions, within the formal ledger: maximum Hessian -0.00027962742674825590131955...; the independent direction formula agrees and no finite chord is positive.

## Execution and replay

From this directory, the original command was:

`/opt/venv/bin/python launch.py --out formal --scan 100000 --restarts 24 --optcalls 1000 --cap 150000 --seconds 3600`

After the original processes ended, the sequential audit command was:

`/opt/venv/bin/python finish_precision.py --out formal`

These commands were executed once, not restarted. Existing formal output is refused by the launcher. A later replay requires a new explicitly authorized output directory and time window; the archived original deadline must not silently be extended.

Start epoch: 1788835416.9372492. Absolute deadline: 1788839016.9372492 (2026-09-08 03:43:36.937249 UTC), less than global epoch 1788864618. Original worker wall time 662.228167 seconds, exit 0; sequential HP audit 427.367437 seconds, exit 0. Last computation ended at epoch 1788836594.5551631; elapsed start-to-final including the between-process handoff was 1177.617914 seconds.

One numerical CPU thread, 10 GiB address-space cap, no GPU. Original supervisor/worker PIDs 142497/142498 and terminal audit PID 142777 are absent in the final process audit. No other's process was stopped and no job remains alive. One read-only display command failed due to shell quoting; subsequent process-list commands returned 1 because their requested PIDs were absent. These were not numerical failures.

The formal source hashes were verified unchanged at termination; see formal_source_hashes.json. A narrow SQLite covering index was added during execution to eliminate a slow full-table budget count; it changed no row, objective or bound. Its 1.491-second operation is recorded in formal/ledger_index.json. The final SQLite SHA256 is e27791f66a28b3df3fa8b4d0876dde0f6f216287acf32ebb79b52904b3506f37.

The complete per-objective SQLite ledger and HP JSONL files remain in the private remote phase4/formal work directory. Local formal/ contains compact audit, best-object, launch, exit, source/configuration and summary snapshots. formal/summary.json is intentionally the original worker's immutable 120894-call summary; formal/audit.json and formal/precision_exit.json give the complete 136898-call terminal denominator.

The unresolved breakpoint remains the general connected n=3 theorem: finite negative samples, including boundary/rare-event/near-block attacks, do not resolve it.
