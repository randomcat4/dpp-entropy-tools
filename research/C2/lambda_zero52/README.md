# C2 issue 52: radial Hessian derivative on the Lambda-zero family

Status: RUNNING. This is a new bounded computation under [issue 52](https://github.com/randomcat4/dpp-entropy-tools/issues/52), separate from the merged PR47 packet and C3's review of the half-filled theorem in PR51.

Frozen author source: PR51 `2e4b8754ad4af2fe055ebeeef1159877773372a3`, `research/I05-22-missing-edge-20260909/continuation.md`, section 5. The complete requested rational construction is preserved in `inputs/frozen_issue52.md`; it is an input assertion to verify, not a theorem inherited from the author. Main queue was read at `f6d9eb6d2b6f7d6001bf5f230911f1e8c723f84e`.

The target is positive definiteness of `M = d/du[-Hess H(K(u))]` for all `|mu|, |nu|, |r| < 1` and `0 < u < 1`, in the six fixed direction coordinates `(A,B,C,E,F,G)` defined by the input. The center curve and the physical affine test direction are distinct. The direction congruence is held fixed when differentiating in u.

| Unit | Responsibility | Arithmetic execution |
|---|---|---|
| `compute/` | Independent event reconstruction, rational identity check and bounded sign computation | Sole owner, one process |
| `formula_review/` | Independent analytic audit of the event-to-M formula and domain | None |
| `structure/` | Bounded analytic congruence/factor/obstruction route | None |

All three children are direct, with no descendants. A new sign certificate or counterexample requires a subsequent fresh nonauthor review. Routine coordination stays in issue52 and the associated draft PR; C3 alone integrates main.

See `frozen_contract.md` for acceptance and stopping rules, `STATUS.md` for progress, and `provenance.md` for role separation. No computational outcome has yet been accepted.
