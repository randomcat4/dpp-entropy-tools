# PR60 U4 auxiliary SECOND scope

This file is a bounded addendum for the previously excluded U4 unit only. It preserves the earlier PR60 SECOND reports unchanged and does not re-review U1-U3 or U5.

Overall U4 scope verdict: **CORRECT** for the fixed-diagonal radial-method obstruction and the associated actual-curvature/Jensen safety checks, under the frozen source and auxiliary machine-evidence boundaries below.

## Accepted scope

- Frozen author target: `input/continuation.md` section 3, lines 72-158. This defines the fixed-diagonal radial extension, the matrices `K*`, `D*`, `C*`, the radial legality bound, the base event law and `exp(Lambda)`, the radial derivative display, the all-event jet derivation, the rational log method, the true `-H''(K*;D*)` display, and the three-kernel Jensen display.
- Author comparison script: `input/continuation_exact.py` lines 1-16 and 73-103 only as a comparison target. I did not run it and did not treat it as independent evidence.
- Auxiliary packet: `aux_input/`, bound by `aux_input_binding.json`, PR71 head `8878516c0ad12e60884419fc03525b2a7caa7be3`, executable head `ee8f0a105798494474b1afd41f69af96794c8f5f`, and author head `f869fd251c0d6fdad737b6d5efa287307795a87d` (`aux_input_binding.json` lines 2-4 and 163-165).
- Accepted mathematical content: for the displayed rational `K*`, `D*`, `C*`, and `h=1/100000`, the complete eight-event exact certificate supports:
  - strict legality of `K*`, `I-K*`, the radial endpoints `s=999/1000` and `s=1001/1000`, and the three Jensen kernels `K*±hD*`, `K*` with complements;
  - the displayed complete-event law at `s=1` and `exp(Lambda)=65729622186464/3466472577089>1`;
  - the full radial derivative formula for `(d/ds)[-Hess H(K(s))](D*,D*)` with all eight events and all six mixed jets, yielding the displayed strictly negative interval;
  - the actual complete negative entropy curvature `-H''(K*;D*)` is strictly positive in the displayed interval;
  - the actual complete-configuration Jensen gap `(H(K*+hD*)+H(K*-hD*))/2-H(K*)` is strictly negative in the displayed interval.

## Exclusions

- No U1-U3 or U5 claim is extended or re-reviewed here.
- The derivative negativity is accepted only as an auxiliary-method obstruction. It is not an entropy counterexample, not a DPP entropy concavity refutation, not a refutation of the Lambda-zero `M` theorem, and not a general Lambda-nonzero theorem. This is also the author-stated interpretation at `input/continuation.md` lines 120 and 156, and the auxiliary certificate's `not_claimed` list at `aux_input/outputs/run01/certificate.json` lines 2546 and 3074-3076.
- No PR57 premise is used for this U4 addendum.
- No C1 FIRST report/code/output/conclusion, no C3 disposition, no machine_notes, and no top-level summary README were inspected.
- No new arithmetic, SymPy, entropy job, remote job, formal run, or author-checker execution was performed by me. My work was static source/proof/raw-certificate inspection plus permitted file hashing.

## Evidence boundaries

- `aux_input_binding.json` lists 26 files; I checked that all 26 files are present and that every listed SHA-256 matches the local packet. The binding itself has SHA-256 `53324b339c30ebc6994592042c8513171315c3679d63d7c6ce6adee7f42d407d`.
- The auxiliary run ledger records one bounded run, zero failed runs, zero repairs, exit code 0, no live arithmetic, one CPU/thread, no GPU, 16 GiB, and a 600 second wall-clock contract (`aux_input/execution/RUN_LEDGER.json` lines 2-42).
- The wrapper records the single-process guard, deadline, thread limits, CPU affinity, memory cap, stdout/stderr routing, and final exit recording (`aux_input/execution/run_guard.sh` lines 1-54).
- I used the auxiliary implementation as a candidate proof algorithm and accepted it only after inspecting the relevant source formulas and raw outputs, not from the string `MACHINE_PASS` alone.
