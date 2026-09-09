# PR30 independent scoped audit

The unchanged nonauthor report is `REVIEW.md`, bound to PR30 head `94d67909bf8c1ea06da6350cf7907d6665cb166a`. Source paths in that report refer to the public `research/C1/` and `research/N3/` paths at that exact commit; no source code is duplicated here. The three PR24 dependency bindings are in `../dependency_binding.json`. C3 separately audited and merged PR24 and PR30.

The accepted asymptotic result concerns the unit-normalized family with lambda=7/10 and s=2/5. Exact beta zeros exist for all sufficiently small epsilon, and all zeros in the frozen kappa interval satisfy det(N) alpha = 1 - 10/(7 log(1/epsilon)) + O(log(1/epsilon)^-2). This only excludes a uniform positive safety margin. It does not refute the original concavity question.

The finite rational interval certificate concerns a different family, with u=(3/5,4/5,q sqrt(epsilon)). The server rerun at 60 bisection steps passed with strict opposite endpoint signs and a whole-bracket upper bound below 0.925807. Its exact interval endpoints, minimum atom probability, pivots, environment and owned PID are in `evidence/server_cert60/sparse_rational_certificate_cert60.json`; exit code 0 and raw logs are adjacent.

From the repository root, with mpmath 1.3.0 available:

```sh
python3 research/C1/mechanism/scripts/sparse_rational_certificate.py --cert-steps 60 --output /tmp/pr30_cert60.json
python3 research/C2/verification2/beta/evidence/analytic_sparse_check.py
```

The second script is an independent high-precision check of leading terms, explicitly labeled NUMERIC_ASYMPTOTIC_SPOT_CHECK_ONLY. It is not a proof of uniform remainders. Those are assessed in the written proof review. The included symbolic-algebra output supports the corrected common-event cross term; the author source remains under research/C1/main/sparse_limit_algebra.py.

No PR31 self-approval, global B0 certificate, uniqueness theorem, explicit epsilon threshold, novelty certification or Lean formalization is claimed.
