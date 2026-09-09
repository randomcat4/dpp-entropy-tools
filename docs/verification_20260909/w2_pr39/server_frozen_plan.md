# PR39 frozen server verification plan

Source: public PR39, head `5558a6b22ef8eb080d198d4af6b1a5cfe2fb164f`.
This plan is saved before the server run. The already recorded local smoke check is retained separately; it is not the server result.

Inputs are the unchanged independent checker `independent_pr39_exact_checker.py`, the frozen `inputs/new.json`, and the frozen author `output/new_audit.json`. The author program is not imported or executed. No new input family is generated.

The bounded checks are the two named n=4 event laws (16 events each), reconstructed by principal minors and Mobius inversion and cross-checked by mixed-row determinants; exact KL coefficients through t^8; all Boolean-character moments; closed walks of lengths 1 through 6 at t=1/2; the rational two-block local-channel witness; and the tail-series constant at 1/2.

Run once in the integrator's dedicated server verification directory with Python 3.12 and SymPy 1.14, one arithmetic thread, no GPU, at most 32 GiB address space and a 600-second wall-time limit. Save the JSON, standard output, standard error, and numeric exit code. Stop at the first failure or timeout, preserving partial artifacts; routine execution corrections may be recorded and rerun on these same inputs. No scan, interval enlargement, or new mathematical search is authorized by this plan.

Acceptance requires normal exit 0, `PASS_INDEPENDENT_EXACT_CHECKS`, and all five named check groups passing. These checks certify only the named finite fixtures. The analytic theorem and entropy-rate passage are evaluated in the two separate nonauthor proof audits; the full legal interval is not certified by these calculations.
