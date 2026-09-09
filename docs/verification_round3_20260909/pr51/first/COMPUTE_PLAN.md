# PR51 first-review compute plan

This plan is frozen before any arithmetic execution.

Primary method: analytic proof review of the public files. Computation is limited to small exact algebra checks needed to audit the proof's displayed identities.

Inputs:

- public source lines in `proof_half_filled.md`, `sources_and_routes.md`, and `verification.md`;
- no private Drive code or non-public author verifier;
- no PR41/PR43 theorem used as a black box.

Exact finite objects to check if needed:

1. The eight complete-event probabilities from determinant inclusion-exclusion for a symbolic real symmetric `3 x 3` kernel and for the half-filled missing-edge specialization.
2. First and second affine coefficients for `K+tD`, enough to validate the cofactor identity used in `proof_half_filled.md:40-52`.
3. The complement/sign involution action and vanishing cross-block terms for the `2+4` decomposition in `proof_half_filled.md:84-91`.
4. The four-dimensional block `G_s(r)`, derivative matrix `dot G`, determinant identity, `r=0` leading principal minors, and `G_0` seed in `proof_half_filled.md:130-195`.
5. The illustrative Jensen interval in `proof_half_filled.md:197-223`, only to check the sign/error-bound scope and not as theorem evidence.

Acceptance standard:

- symbolic identities must simplify to exact zero over rational-function domains after clearing stated positive denominators;
- positivity arguments must be analytic/rational-symbolic, not floating eigenvalue evidence;
- finite rational examples can support source consistency but cannot prove the theorem;
- any exact mismatch in displayed identities, quantifiers, strictness, endpoint handling, or decomposition is a material gap.

Resource limits:

- initial arithmetic thread count: 1;
- no GPU;
- set BLAS/OpenMP-style thread variables to `1`;
- memory cap target: at most 4 GiB for bounded checks;
- wall-clock cap target: at most 15 minutes per bounded check;
- no full search, no LP replay, no prior PR41/43 full replay, and no descendants.

Stop / recovery:

- stop immediately on an exact algebra mismatch and report the first material blocker;
- if a check becomes heavy, retain partial output, mark the unverified identity as `INCOMPLETE`, and continue analytic review of independent source-level issues;
- if local tooling lacks a needed dependency, use the existing owned review environment only for the bounded script, without recording private connection details in public artifacts.
