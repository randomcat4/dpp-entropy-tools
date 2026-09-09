# Frozen Scope - PR59 Second Verification

## Review Mode

This is an independent second mathematical verification of frozen PR59 author package `head892a121a6e26fcf638c75de917e50a4503b5675e`, mapped into `verification_round4/pr59_second/input/` by `input_binding.json`.

I treated `input/clarifications.md` as part of the frozen author proof, as instructed. I did not read first-review material, PR59 comments, other pending author branches, PR57/PR58/PR60 material, C1 round-four review files, private Drive material, or `C:/canglan/`.

No author source file was modified. No Python, SymPy, numerical, or Lean computation was run. The JSON outputs and scripts were inspected as author artifacts only.

## Frozen PR59 Claims Reviewed

1. Compact radial tube theorem: for fixed `beta>0`, `0<mu<1`, real half-period-odd nonzero `g in A_beta`, odd `k` with `g_hat(k)!=0`, and any prescribed strict legal compact interval `[-T,T]` for `mu+t g`, there is `rho>0` such that every real half-period-even mean-`mu` center `c` with `||c-mu||_beta<rho` satisfies concavity of `h(c+t g)+(2/3)|g_hat(k)|^4 t^4` on `[-T,T]`.
2. Exact normalized Holder/RPF five-term true-rate Hessian identity at an arbitrary strict parameter, retaining local Fisher, acceleration, invariant-law response, and resolvent centering terms.
3. Finite-state true-rate error bridge: an existence-level exponentially small RPF remainder interface, not an executed interval certificate.
4. Beam-splitter occupation-distribution obstruction: finite-window and per-cell output occupation mutual information is `O(u^4)` at a midpoint and therefore gives no second-order sign; occupation Shannon entropy is not replaced by quantum/von-Neumann entropy.
5. Explicit mean-`1/3` nonconstant center family with nonempty amplitude range.

## Accepted Public Premises Used

The accepted inputs were used only in the following scoped ways.

- `runs/C3/integration/docs/verification_20260909/w2/radial_quartic_audit.md`: accepted W2/PR34 constant-centered radial theorem. Its accepted scope states concavity of `h(p+s(f-p))+(4/3)|fhat(k)|^4 s^4` on the full feasible radial interval (`lines 6-28`) and verifies the quartic constant (`lines 85-109`). PR59 uses this only at the constant center `mu+t g`, after the standard rescaling from `p+s(f-p)` to the chosen direction `g`.
- `runs/C3/integration/docs/verification_round3_20260909/accepted_pr53.md`: accepted PR53/EW local theorem and machinery. Its precise theorem is local in `t` for strict half-period centers (`lines 7-25`), and its rate-theorem explanation accepts the complete-event inverse, fixed Holder/RPF, and no-limit-differentiation bridge (`lines 29-39`). It also records that whole-legal intervals, arbitrary centers, endpoints, arbitrary measurable symbols, and true counterexamples remain outside acceptance (`lines 53-55`).
- `runs/C3/integration/research/I05-DPP-21-20260909/exponential_wiener_extension.md`: used for the accepted exponentially weighted event-inverse/RPF construction and its exact scope, especially event inverse localization (`lines 45-154`), common complex disk and one-sided conditionals (`lines 156-231`), and the local EW theorem statement (`lines 31-40`).
- `runs/C3/integration/research/I05-DPP-21-20260909/finite_range_local_theorem.md`: used as the finite-range backbone recorded by PR53, including the parity identity (`lines 54-86`), matching KL lower bound (`lines 88-143`), uniform event inverse proof (`lines 145-206`), RPF rate formula before differentiation (`lines 305-341`), and vanishing of the `s=t^2` linear term (`lines 343-397`).
- `runs/C3/integration/research/I05-DPP-21-20260909/sources.md`: used only for public source roles and boundaries; it explicitly separates bibliography from acceptance (`lines 1-3`) and states that no cited source proves whole-legal-interval concavity (`lines 63-65`).

## Accepted Scope

The review accepts, subject to the line-by-line reasoning in `review_report.md`, only the compact radial-tube theorem around constant-centered radial chords, the normalized Holder/RPF Hessian identity under its spectral-gap hypotheses, the finite-state exponential-remainder interface as an analytic existence statement, the beam-splitter second-order obstruction, and the explicit mean-`1/3` family as a corollary of Theorem CT.

## Excluded Scope

This review does not accept or upgrade any claim about:

- arbitrary strict exponentially local centers far from the constant-center tube;
- legal endpoint continuation or a radius uniform as a radial endpoint is approached;
- the old PR39 fixed example on its full `[-384,384]` interval;
- arbitrary measurable symbols beyond the accepted radial theorem's constant-centered use;
- nonnegativity of the beam-splitter occupation-entropy gain;
- a true entropy-rate counterexample;
- novelty, priority, publication readiness, or main-branch acceptance.
