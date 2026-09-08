# Local contract check record

Result status: CANDIDATE. Mathematical conclusion: INCOMPLETE.
Date: 2026-09-07. Repository base:
`96b2c3ac2fb5bb5a6b74b04e193787c1cd764c5e`.

Executed from the isolated repository root:

```text
python research/T3/specs/check_contract.py
```

The local interpreter's absolute executable path was replaced above with
`python` to keep machine/user paths out of the public record. Arguments and
working-directory semantics are unchanged. This record concerns contract checks,
not the proposed numerical `certify` command.

- Environment: Windows, Python 3.12.14, jsonschema 4.25.1; transitive versions
  are pinned in `requirements.txt`. Dependencies were installed only in an
  isolated local virtual environment. No system dependencies were installed.
- Actual exit code: 0. JSON Schema Draft 2020-12 passed its meta-schema check.
- Both example documents passed schema and selected semantic validation.
- 25 negative contract/parser cases were rejected.
- Exact `Fraction` arithmetic checked scalar endpoint feasibility and `H''=-1`.
- Computation was a single lightweight process; no numeric worker pool, GPU,
  exhaustive search, strict log backend or performance benchmark was used.
- Numerical certificate coverage: planned 1 illustrative request, started 0,
  completed 0, failed 0, certified 0. No numerical execution was attempted.
- Numerical certificate hash: null. No certificate was generated.

Example input SHA-256 (raw file bytes):
`99249617e1968b51aee6bd448df2177defd9712809f0d9cc17e99ba840e7e6de`.

Illustrative response SHA-256 (raw file bytes, not a certificate hash):
`4e82278a2a5a867ff337107c60f4a257c5918c17603afb061bb98dfd00c2079b`.

This smoke check does not inspect strict witness files, validate transcendental
enclosures, prove uniform cell coverage, resolve symlinks in evidence bundles,
or independently review the mathematics. The numerical core, independent
reference cross-check, interrupt/resume integration and strict acceptance cases
in `contract.md` remain unexecuted dependencies. No VERIFIED status is claimed.
