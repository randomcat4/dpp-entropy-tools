# D10-U10b run log

Scope:

- Writable directory: `research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/scalar_information/`.
- No U8 author/audit files, `scalar_direct`, shared indexes, or other routes were modified.
- No subagents, no server, no submission.
- `C:\canglan\` was not used as a search root, work directory, or file source.

## Commands

From repository root:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/scalar_information/scalar_information_sanity.py
```

Exit code: `0`.

Output JSON:

```text
research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/scalar_information/scalar_information_sanity_results.json
```

The script uses only Mobius inversion of inclusion determinants, exact
`Fraction` first jets, and `Decimal` logs/linear solves.  It does not import the
author search, gate, or recheck scripts.

## Result summary

| case | `rho` | Fisher-only scalar `det(N)eta^T F^-1 eta` | note |
| --- | ---: | ---: | --- |
| heterogeneous triangle | `0.0710645104532210...` | `0.0753649014986808...` | routine strict connected check |
| signed path-like | `0.4988385485368981...` | `0.9924575561987278...` | connected path support, near Fisher-only threshold |
| near rank-one dense | `0.3121025757096994...` | `0.4234515115991816...` | rational equal-soft-eigenvalue style point |
| score-only shortcut blocker | `0.6364350521741918...` | `1.6324286014007979...` | strict connected DPP disproving Fisher-only shortcut |

All four cases have positive exact atoms, `N` with positive Decimal LDL pivots,
and `B=A-det(N)eta eta^T` with positive Decimal LDL pivots.

## Hashes

Input hashes read by this route:

| file | SHA256 |
| --- | --- |
| `n3_global_full_hessian/frozen_problem.md` | `ACFE5CBC817616C34994C6BD793367BED80429339641913E10318321091F0241` |
| `n3_global_full_hessian/proof_or_blocker.md` | `E5FE916565DF17AF12455F123ED60FBD708B735FDA21EDA187BA2484E12243EB` |
| `n3_global_full_hessian/derivation.md` | `E809CBD5B69E9E0648D1FF5DEE2B5472B39DD31E016EAAC9A55E15B00BCF55E5` |
| `n3_global_full_hessian/verdict.md` | `EF2C15512467DCA97AB29459048869664C3E72B746D64DDF1AE2252A388D3CF0` |
| `n3_global_full_hessian/verifications/boundary/fresh_boundary_audit.md` | `5225BA95E98B1326215002619CAC9DAEA012493C189A2C3DABB839E4AEA99F29` |

Artifact hashes, before this run-log table was patched:

| file | SHA256 |
| --- | --- |
| `scalar_information/proof_or_blocker.md` | `49263C78FC9D30F91E3D0A6F46C3ED08C470F4A7FB5CEE4B0430AE440FF027D3` |
| `scalar_information/scalar_information_sanity.py` | `DDA8873E5F42EEE0D108FF38BE0477B5EF446221A0F5530D3FD5870620ECA8B6` |
| `scalar_information/scalar_information_sanity_results.json` | `FB1E97385145E85129A4DB0191603A210F8DEC2358C7E407FFB19F9D3344CEA8` |
| `scalar_information/verdict.md` | `B841D1AB2B6354536EEE361AAF5D1AA8517372F522FC74A6A957719E80F50A50` |
