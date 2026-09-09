# I05-C1-20260909 evidence package

The global B0 question is unresolved. Read RESULT.md for the exact PARTIAL
scope, proof.md for the full integrated argument, and verification.md for
the independent review bindings. The two frozen statements distinguish the
original universal question from the restricted sparse-family result.

This directory is self-contained: no private server, source checkout, or
previous conversation is needed to read its proofs or reproduce its named
computations. The complete original author texts are retained under
geometry/, main/, and mechanism/. Historical labels such as "review pending"
inside frozen author files describe their time of authorship; the current
review record is verification.md. Old discarded algebra is explicitly named
failed_v1 and never used as proof.

Issue: https://github.com/randomcat4/dpp-entropy-tools/issues/28

Draft PR: https://github.com/randomcat4/dpp-entropy-tools/pull/30

The PR is stacked on source PR #24. It must remain a draft; no merge or
automatic research continuation is implied by the package.

## Reproduction

Reference runtime: Python 3.12.3, NumPy 2.1.2, SciPy 1.14.1,
mpmath 1.3.0, SymPy 1.13.3 on Linux x86_64. All recorded research arithmetic
ran on the authorized server, one CPU thread per library, without GPU.
The finite root certificate itself uses exact fractions and explicit
outward interval bounds; its mpmath calculations only select brackets and
produce the separately labelled diagnostic table.

In an environment with the listed packages, run from this directory:

```sh
python reproduce.py --suite core --output-dir reproduced/core
python reproduce.py --suite geometry --output-dir reproduced/geometry
python reproduce.py --suite certificate --output-dir reproduced/certificate
python reproduce.py --suite audit --output-dir reproduced/audit
```

`--suite all` runs those fixed suites and the original bounded mechanism
precheck. The runner writes only to a new `reproduced/` directory (or an
explicit `--output-dir`) and records each command, stdout, stderr and exit
status. Existing evidence files are not overwritten. Process IDs, platform
strings and elapsed times naturally vary. Numeric JSON fields and exact
rational enclosures are the relevant comparison. No random scan, network
request or package installation is performed by the runner.

The precise successful standalone certificate command is:

```sh
python mechanism/scripts/sparse_rational_certificate.py --cert-steps 60 --table-exps 6,8,12 --table-steps 80 --cert-exp 8 --output reproduced/sparse_rational_certificate.json
```

The script's historical default of 24 certification bisections does not
certify this narrow bracket. Sixty bisections are part of the recorded
successful input, not an optional performance choice.

`geometry/sparse_detail.py` and `main/sparse_limit_algebra_failed_v1.py`
preserve discarded predictions. They are excluded from the successful
default suites. Their historical output is evidence of a corrected error,
not an additional theorem. The unsuccessful interval prototypes are retained
under mechanism/scripts/ with their failure descriptions in attempts.md.

MANIFEST.sha256 covers every distributed file other than that manifest
itself. A nested author manifest under mechanism/ has only that child's
historical scope; the root manifest is authoritative for this final package.
The package has no C1 Lean theorem; formal/README.md reports only an L0
environment check.
