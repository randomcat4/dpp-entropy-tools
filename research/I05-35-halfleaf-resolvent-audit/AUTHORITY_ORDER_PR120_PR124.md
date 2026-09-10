# Authoritative reading order for PR120, PR124, PR127 and PR132

Status date: 2026-09-10. This file only fixes source/review precedence and duplicate accounting. It does not delete, rewrite, merge, or supersede either historical branch.

## 1. Main controls accepted scope

Read current `main` first, in this order:

1. `docs/research_status.md`;
2. `docs/verification_round5_20260910/accepted_pr127_pr124_pointwise.md`.

At `main@3e27a09e9185cb63d8a42e4db022008ee9828136`, the only I05-35 result already recorded on main is the exact pointwise-resolvent obstruction from PR124/PR127. Its accepted scope is exactly: strict physical legality, all-eight-event Mobius reconstruction, exact negative rational `Phi_r''`, and the boundary that this is neither an integrated `G1''` counterexample nor a Shannon-entropy counterexample.

## 2. Positive analytic FIRST is newer than the older handoff, but is not yet main

PR132 at review head `6370ca1ae64cfc9e58c491568445f02fadcf0a71` gives an analytic `ACCEPTED_SCOPED` FIRST for the positive units frozen at PR124 author head `344723af6affab240c9f87c395d4e8c1b7b19f6d`:

- the equal-strength half-leaf theorem;
- the punctured small-edge theorem, compact-uniform on positive face-parameter sets;
- fixed-positive-edge local persistence to unequal leaf diagonals;
- the residual-only negative gap as a method obstruction only.

PR132 is open and unmerged at this writing. Therefore its verdict is the controlling independent FIRST for those source units, but it is not yet an S3/main acceptance record. No later work should describe these units as unreviewed; it also must not describe them as merged or globally accepted on main.

## 3. Duplicate theorem accounting

PR120 head `c2fa3906a2f8f0d2176e26a881333d5d7b484cde` is the earlier source of the equal-strength theorem. PR124 head `344723af6affab240c9f87c395d4e8c1b7b19f6d` proves the same hypotheses and conclusion by a materially different certificate.

The result is counted once:

- theorem-source precedence: PR120;
- alternative independently checked proof certificate: PR124, reviewed in PR132;
- no duplicated theorem credit or duplicated acceptance count.

The proof difference is substantive:

- PR120 uses a six-dimensional exact integrated one-sided Hessian, leaf-exchange block reduction, a scalar determinant polynomial, concavity in `Gamma=rho*C-V`, and two endpoint inequalities proved by positive even-power series;
- PR124 uses symmetric/antisymmetric sectors, retains a positive three-node chain in the symmetric sector, optimally absorbs the shared-cell term, and proves the remaining gap by an all-coefficient power-series argument.

## 4. Nonduplicate PR124 unit

PR124's punctured small-edge theorem is additional. It is not contained in PR120. Its exact core is

`E(a,b)=L-C(F+R)^(-1)C^T`,

and it proves positivity only for one normalized strength tending to zero while the other stays in a compact positive set, plus the corresponding physical occupied/vacant passage. It does not settle the compact unequal-strength middle.

## 5. Pointwise obstruction source order

The exact negative `Phi_r''` witness appears in both PR120 and PR124 packets. For accepted-scope citation and theorem accounting, use:

1. main acceptance page `accepted_pr127_pr124_pointwise.md`;
2. PR127 independent FIRST report;
3. frozen PR124 author source at `344723af...`;
4. PR120's earlier packet only as preserved source history.

Do not count the duplicate event checker or duplicate fraction twice. Do not revive pointwise-in-`r` positivity as a target.

## 6. Current continuation target

The next target is neither the already proved equal-strength spine nor the already proved punctured small-edge regime. It is the compact unequal-strength middle for the exact integrated two-dimensional Schur core `E(a,b)`, with `a,b` bounded away from zero and infinity. Any conclusion must retain the complete one-sided logarithmic functional; if one-sided `G1''` fails, the next object is the paired occupied/vacant forms plus the exact leaf marginal.

All new claims remain author results pending an independent review unless a later frozen review record states otherwise. Novelty and formal verification are not assessed here.
