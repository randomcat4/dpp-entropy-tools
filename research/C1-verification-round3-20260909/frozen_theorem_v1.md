# C1 round-three frozen verification v1

Status: RUNNING; no new acceptance is issued by this freeze.

## Objects and source versions

Review complete-configuration Shannon entropy of finite real DPP kernels,
using all events `p_K(S)=sum_(T contains S)(-1)^(|T|-|S|) det(K_T)` and
the actual kernel-affine paths. No spectral or cardinality entropy is
substituted, and no observed-coordinate condition may be replaced by a
basis rotation.

- PR41: `6fd61dcd299417fc3a4eab3af682c03dd816b670`, complete `round2/`
  directory under `research/N3/round3/I05-W4-20260909/`.
- PR43: `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78`, complete directory
  `research/I05-W1-20260909-R2/`.

Author files remain immutable. Primary review source snapshots are stored
outside the review checkout under `sources/pr41` and `sources/pr43`.

## Three independent bounded units

1. PR41: R2-T1 strong-coupling connected three-point centers
   `[[1/2,0,k],[0,1/2,sigma*k],[k,sigma*k,1/2]]`, sigma=+/-1,
   `0<8k^2<1`, with every nonzero real symmetric direction, not merely
   directions preserving that center family. Also R2-T2 for an arbitrary
   strict two-point block plus an isolated Bernoulli coordinate, its
   two-point conditional-entropy lemma, and the stated exact general
   missing-edge reduction without promoting its unresolved inequality.
2. PR43 rank-two unit: all claims in `frozen_statement_continuation.md`
   concerning every strict real three-point kernel and indefinite rank-two
   direction; the correlated dense 3+3 structured family; and the exact
   exterior sufficient-statistic/compressed-Hessian identities used there.
   Review `proof/04_three_point_indefinite_rank2.md`,
   `proof/05_diagonal_and_feature_routes.md`, and
   `proof/06_correlated_3plus3_family.md`, including all dependencies.
3. PR43 channel/extension unit: claims D--J in
   `continuation/frozen_statement_v3.md`, with the explicit v3/v2-task
   corrections to adjoint direction and reversibility taking precedence
   over historical reversible-only handoffs. Review diagonal active
   sectors, individual conditional diagonal anchors, Markov-adjoint
   intertwining and curvature identity, diagonal exterior degrees,
   reversible obstruction, and the classical-occupation-channel
   obstruction. These are distinct claims, not one collective theorem.

The PR43 root continuation-v1 and nested v3 packets coexist. Their
publication-level relationship is being asked in the repository; each
explicit mathematical statement can be reviewed under its own frozen file
while that clarification is pending. No summary is allowed to silently
change a quantifier in its proof source.

## Dependencies and limits

The imported diagonal-anchor theorem is the independently reviewed C3
finite theorem at PR29 commit `648f1906468e3e548410f98a6b1a53a978f2ea11`.
Reviewers must inspect its statement/proof and actual hypotheses, without
using prior review opinions as evidence for the new claims.

Authors cannot approve their own work. Each initial reviewer has a fresh
context and receives no old verdict as evidence. C1 may integrate reports
but may not approve a proof it substantively authors or merge main.
Major new general claims require a risk-appropriate second independent
review after the first passes.

Each child owns only its assigned local and server directory. No child may
spawn descendants. The line cap is eight CPU and 32 GiB, no GPU; children
initially use one numerical thread and at most 8 GiB each, 600 seconds per
short fixed check. Freeze exact input, algorithm, error bound and stopping
condition before execution. Jobs expected beyond 60 minutes are handed to
the compute lane through an issue. Do not guess missing computation inputs.
Keep scripts, exact inputs, outputs, PID/versions/exits and failed versions;
no checksum inventory is required.

## Outcomes and exclusions

Per claim report CORRECT / CRITICAL_GAPS, together with repository status
ACCEPTED_SCOPED / NEEDS_FIX / REFUTED / INCOMPLETE and exact source locations.
A proof gap is distinct from a theorem counterexample. Finite or floating
checks do not certify universal claims. Novelty is a separate, unassessed
question unless explicitly reviewed.

No new open-ended theory, random search, unrestricted conjecture claim,
private-source access, or direct main merge belongs to this task. Ordinary
claims, questions and READY handoffs use repository issues/PRs/STATUS;
routine cross-task messages to the coordinator are not sent.
