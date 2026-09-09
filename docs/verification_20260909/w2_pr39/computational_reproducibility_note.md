# PR39 bounded computational reproducibility check

Status: `ACCEPTED_SCOPED` for the named finite arithmetic checks, subject to the same scope limits below.

Frozen PR head: `5558a6b22ef8eb080d198d4af6b1a5cfe2fb164f`.

Frozen inputs checked:

- `research/W2/nonconstant_orbit/inputs/new.json`
- `research/W2/nonconstant_orbit/output/new_audit.json`
- `research/W2/nonconstant_orbit/code/audit_new.py` was inspected but not imported or executed by the independent checker.

Independent checker:

- `independent_pr39_exact_checker.py`

Run from a checkout or copied PR39 package root containing the frozen `research/W2/nonconstant_orbit/...` tree:

```powershell
python independent_pr39_exact_checker.py --output independent_pr39_exact_check.server.json
```

Run from this local frozen artifact directory:

```powershell
python independent_pr39_exact_checker.py --output independent_pr39_exact_check.local.json
```

The checker is independent in the following sense:

- It does not import or call the author audit script.
- It rebuilds the n=4 DPP event probabilities from principal minors and Möbius inversion.
- It cross-checks the event laws by the mixed-row determinant formula.
- It derives the `t4`, `t6`, and `t8` KL/entropy-series coefficients by exact formal log-series expansion from those event polynomials.
- It verifies Boolean-character moments by comparing law moments to principal minors of `B=2K-I`.
- It recomputes the local-channel witness from block determinants and checks the stated finite conflict.

Local Windows smoke result: `PASS_INDEPENDENT_EXACT_CHECKS` with SymPy `1.14.0`; output saved as `independent_pr39_exact_check.local.json`.

Scope limits:

- finite named n=4 even and non-even examples only;
- finite Boolean moment and closed-walk identities only;
- finite local-channel witness only;
- no scan over symbol families;
- no independent proof of the full analytic theorem or entropy-rate limit;
- no certification of the full legal interval beyond the stated finite fixtures.

## Integrator server rerun

The unchanged independent checker was rerun after saving the server frozen plan, with one arithmetic thread, no GPU, a 600-second timeout, and a 32-GiB address-space cap. It completed normally with exit 0 in 2.452382 seconds (Python 3.12.3, SymPy 1.14.0). All five named check groups passed. The JSON is [the server result](independent_pr39_exact_check.server.json); the bounded plan is [saved separately](server_frozen_plan.md). Standard error was empty. This is a reproducibility execution of the same independent checker, not another independent proof reviewer.
