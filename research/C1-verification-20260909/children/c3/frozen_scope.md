# C3 PR29 independent verification frozen scope

Reviewer: C3 non-author cross-check child.
Date: 2026-09-09.
Frozen input commit: `648f1906468e3e548410f98a6b1a53a978f2ea11`.
Public source directory: `verification_20260909/sources/pr29/`.
Writable public output directory: `verification_20260909/children/c3/`.
Private compute directory: reviewer-owned isolated server path `/root/i05-seven-fronts-20260909/C1/verification/c3`.

## Scope A: radial theorem

Inputs read for judgment:

- `frozen_statement_v2.md`
- `proof.md`

Claim to decide:

1. For every internal diagonal `B=diag(b_i)` with `0<b_i<1`, and every fixed Hermitian `A`, the finite DPP entropy `H(B+tA)` is concave on the entire feasible interval `{t: 0 <= B+tA <= I}`, including both signs and feasible boundary kernels.
2. For every constant `p in (0,1)` and every fixed bounded measurable real `g`, the true scalar stationary DPP entropy rate `h(p+t g)` is concave on the entire legal interval `{t: 0 <= p+t g <= 1 a.e.}`, including boundary symbols.

Required audit points: product replacement channel exactly equals the affine DPP kernel family; bidirectional KL contraction implies entrywise nonnegative mixed derivatives; entrywise Hessian nonnegativity is not confused with PSD Hessian; both half-axes are joined at `0`; diagonal changes in `A` are covered; complex Toeplitz finite compressions and boundary symbols are legal; entropy-rate concavity passes through pointwise finite-block limits, not differentiation under limits.

Out of scope: full Lyons-Steif scalar entropy-rate concavity for arbitrary chords; novelty; PR30 author self-acceptance.

## Scope B: fixed C3-M1 rate certificate

Inputs read for judgment:

- `rate/certificate_theory.md`
- `rate/rate_analysis.md`
- `rate/scripts/c3_m1_variational_boundary.py`
- `rate/scripts/c3_m1_rate_certificate.py`
- `rate/scripts/c3_m1_audit.py`
- `rate/candidate.json`
- `rate/candidate_true_symbol.json`
- `rate/artifacts/c3_m1_boundary_M64.json`
- `rate/artifacts/c3_m1_rate_n4.json`
- `rate/artifacts/c3_m1_audit_result.json`

Claim to decide:

The fixed three-symbol C3-M1 object has a certified strictly negative true entropy-rate pair gap
`(h(f_-)+h(f_+))/2 - h(f_0) < 0`, using true entropy-rate bounds, not finite-window entropy values as substitutes.

Required audit points: the three symbols are fixed and separate; true/script Fourier convention conversion is accounted for; all-one and all-zero extreme-past inequalities have the correct direction; variational residual and truncation support bounds are valid for this finite degree-two symbol; all event probabilities used by the finite suffix certificate are exact and normalized; finite conditional entropy bounds enclose the true entropy rate.

Out of scope: positive counterexample search, larger `n`, random scans, long-range symbols, family theorems, or novelty.

## Verdict vocabulary

Each scope is decided separately as one of:

- `ACCEPTED_SCOPED`
- `NEEDS_FIX`
- `REFUTED`
- `INCOMPLETE`
