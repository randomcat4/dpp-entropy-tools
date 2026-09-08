# Verdict

Original frozen target: INCOMPLETE. The bounded probe found no floating
positive candidate and proves no general Hessian sign.

Owner's subsequent frozen conditional-acceleration obstruction: PROVED by
the author, awaiting independent fixed-object review. See `proof.md` and
the rational interval certificate `conditional.json`, index 1. This proves
that the conditional acceleration term can be strictly positive at a strict
connected asymmetric triangle. The same direction's total entropy second
derivative is strictly negative.

512 predeclared rational centers comprised 8 diagonal templates, 4 edge
ratios, 2 cycle signs and 8 radii. All centers were certified strictly feasible
by rational principal minors. Each was evaluated with the full six-direction
entropy Hessian and a floating feasible chord. Twelve selected starts each
received at most 250 Nelder-Mead calls. All 3000 calls are retained: 2920
evaluations and 80 rejected-domain calls. All refinement terminations hit
their fixed 250-evaluation cap. No hidden restart or additional refinement.

The maximum center Hessian eigenvalue was approximately -1.914e-7. The
best scaled refinement approached a nearly block kernel. These are finite
floating observations only. No strict entropy counterexample candidate was
promoted, and no chord certificate is claimed.

An additional diagnostic at the same 512 centers checked the exact-form
probability-acceleration matrix identity described in `structure.md` and
found no positive offdiagonal-only acceleration eigenvalue. This does not
prove that restricted sign globally. Four subsequently authorized manual
rational conditioning diagnostics yielded two positive and two negative
acceleration contributions, all retained in `conditional.json`.

Correctness and value are separate: the local obstruction is explicit and
checkable; novelty was not investigated or claimed. No Lean verification or
non-author review has yet been performed by this author.
