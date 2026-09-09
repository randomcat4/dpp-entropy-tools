# Execution ledger

All research computations ran in the isolated C2 compute directory or its disjoint child directories. No GPU, one BLAS/OpenMP/MKL thread per active numerical job, no system package installs. A C2-local Python virtual environment was created; versions are frozen in requirements.txt. No full-machine process arguments were inspected and no unrelated process was stopped.

|Run|Evidence|Outcome|
|---|---|---|
|Main exact first preflight|main_check.py, successful JSON|Python completed successfully; inline shell status suffix was incorrectly escaped and wrapper returned 1|
|Main corrected execution|run_main.sh, main_check.log/json/exit|Exit 0, PID 163018; identical exact fixture and no added search|
|Mechanism fixture|mechanism/check.py and check.out|Exact/jet checks passed, foreground computation completed|
|Search v1|search/results_v1.json|24-record design completed; wrapper status suffix failed|
|Search v1.1|search/run.sh, run.log, results.json, exit_status.txt|Same 24-record design, corrected wrapper and noncommuting representative selection, exit 0|
|First independent formula check|reviews/first/independent_c2_verify.py and output.txt|All 32 polynomial identities/26-event support and exact jet sums passed|
|Candidate proof audits|verification.md and review reports|Separate from author calculations|

Main library versions: Python 3.12.3, numpy 2.5.3, scipy 1.18.1, sympy 1.14.0, mpmath 1.3.0. Search records its own PID and source hash in results.json. All selected directions and failure versions are retained. Repeated wrapper repairs are not counted as new research centers.

Local shell tooling used the bundled PowerShell 7 with explicit UTF-8 file IO. A read-only JSON inspection initially rejected case-distinct keys m/M; the read was repeated in case-sensitive hashtable mode without changing data. Git author identity was configured only in the independent C2 checkout. The two new proof commits were reattached to the verified identical-tree public source before publication; no mathematical content changed.

Source/public tree checks, issue creation and publication run locally using the already-authorized GitHub client. Only process-local proxy variables were cleared for those requests. This log intentionally omits connection details and authentication data.
