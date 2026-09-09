# C3 result package

Start with RESULT.md, then frozen_statement_v2.md, proof.md and verification.md.
The proved result is radial scalar entropy-rate concavity; the full
Lyons–Steif conjecture remains open. sources.md separates prior work from
the present argument and leaves novelty unconfirmed.

The mathematical proof requires no computation. Optional reproductions:

    python -m venv .venv
    .venv/bin/python -m pip install -r requirements.txt
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/bin/python main_precheck.py

The Windows venv executable is `.venv/Scripts/python.exe`. Set the same
thread variables in the current process. main_precheck.py writes its JSON
in the working directory. Use a copy of the extracted package when rerunning
so the original manifest stays verifiable.

For the one fixed cycle mechanism, run `python check.py` from mechanism/.
It reads input.json and writes all its event data and diagnostic outputs.
See mechanism/mechanism.md for exact analytic formulas and finite scope.

From rate/ run:

    python scripts/c3_m1_variational_boundary.py --candidate candidate.json --output artifacts/c3_m1_boundary_M64.json --M 64 --bits 160
    python scripts/c3_m1_rate_certificate.py --candidate candidate.json --boundary artifacts/c3_m1_boundary_M64.json --output artifacts/c3_m1_rate_n4.json --n 4
    python scripts/c3_m1_audit.py --candidate candidate.json --true-symbol candidate_true_symbol.json --boundary artifacts/c3_m1_boundary_M64.json --rate artifacts/c3_m1_rate_n4.json --output artifacts/c3_m1_audit_result.json

The data files are rational or explicitly marked floating diagnostics.
Outward interval-log endpoints in rate/artifacts are the strict numerical
certificate. Floating tables are readable summaries, not exact endpoints.
All three symbols and six extreme pasts were handled individually.

Optional independent certificate checks, from review/:

    python c3_m1_numeric_audit.py --rate-dir ../rate --output c3_m1_numeric_audit.json

This recomputes rational determinants and residuals independently. It does
not independently regenerate interval logarithms; the review records that
limitation and the separate author-code reproduction.

Run `python verify_manifest.py` from the package root to verify every listed
file. MANIFEST.sha256 excludes itself and lists all other result files.
`structure_validation.json` checks artifact structure only, not mathematics.
