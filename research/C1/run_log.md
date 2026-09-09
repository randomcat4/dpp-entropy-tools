# C1 execution log

Date: 2026-09-09. All computation is CPU-only and starts with OPENBLAS_NUM_THREADS=1, OMP_NUM_THREADS=1. Connection details and authentication never enter this package.

## Source and workspace

Independent clone of the source public checkout, with no hard links, verified at commit e988aa3003484f6368133b8bc0c668331629e369 and tree e7c177ca74da59744443dbfcaadafd98724767ec. A Git bundle was transferred to the isolated server C1 directory and cloned there; the same commit/tree were verified. Children own separate directories and do not write the parent checkout. Initial server memory availability was ample for the 32GiB line cap; no GPU was used.

## Main computations

Runtime: Python 3.12.3; NumPy 2.1.2; SciPy 1.14.1; mpmath 1.3.0; SymPy 1.13.3. Existing runtime reused, no dependency installation.

| Command, from main directory | PID | Exit | Scope |
|---|---:|---:|---|
| python precheck.py | 162887 | 0 | Exactly three fixed kernels, complete event Hessian and covariance projection |
| python tilt_probe.py | 163223 | 0 | Three exact-mechanism tilt probes and eight fixed star diagnostics |
| python sparse_limit_algebra_failed_v1.py (originally named sparse_limit_algebra.py) | 164297 | 0 | Algebra of an incomplete limiting system; discarded, not a true-model check |
| python sparse_limit_algebra.py | 164431 | 0 | Corrected limiting scalar simplified symbolically; asymptotic proof is separate |

Outputs and scripts are included in main/. No background main process remains after these commands. All arithmetic here is floating diagnostic, not a sign certificate.

## Environment/setup failures

- Initial GitHub read encountered a stale loopback proxy. Only the calling process's HTTP_PROXY/HTTPS_PROXY/ALL_PROXY variables were cleared; authorized gh then succeeded.
- System python3 had no NumPy. Reused the existing scientific runtime; no package was installed.
- A shell path-probe draft had quoting errors and exited without changing files. The source run log supplied the existing runtime location.
- First local commit attempt had no author identity; configured this isolated checkout with the source checkout's Codex identity. Initial push had no new commits and Draft PR creation correctly failed. Retried after the actual commit; Draft PR #30 was created successfully.
- No TLS bypass, credential transfer, global setting change, or deletion of another line's work occurred.

Lean L0 availability was checked separately; see formal/README.md. No C1 theorem was formally verified.

## Final nonauthor checks and publication

The audit context completed sparse proof review (PID 165270), a separate
60-step certificate rerun (PID 165603), and an independently written finite
certificate reconstruction (PID 165764), all exit 0. The fresh reviewer
completed a separate sparse reconstruction (PID 165426) and endpoint check,
both exit 0. Full reports, scripts and outputs are included. Its default
24-step certificate rerun failed by interval overestimation and is preserved;
the public reproduction command explicitly fixes the successful 60 steps.

All mathematical work stopped with the global B0 assertion incomplete.
No C1-owned mathematical process, descendant agent or scheduled continuation
remains. Four direct child contexts were used sequentially; the first three
were exactly the assigned geometry, mechanism and audit roles.

Ordinary git push to github.com repeatedly failed at the network connection
stage after the initial Draft PR had been created. The authorized GitHub API
remained reachable. The final publication path constructs the exact committed
tree through the Git data API, verifies its hash against the local tree before
changing the branch reference, and uses a non-force reference update. Local
and public commit IDs can differ because of the API-created commit; their
tree mapping is reported on the Draft PR. No TLS bypass, credential copying,
global Git setting change or source-branch merge is used.

Local release checks inspect only artifact structure, Python syntax, JSON,
frozen source/review bindings, manifest coverage and ZIP round-trip bytes.
They are not additional mathematical experiments. The standalone validator
is validate_archive.py; the math-theorem structural validator report is in
validation/skill_structure.json.
