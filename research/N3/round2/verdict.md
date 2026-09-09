# Round-two mathematical verdict

B0 remains INCOMPLETE: there is neither a universal proof of
`beta=0 => det(N)*alpha<=1` nor a certified violating beta-zero kernel.
The original global real three-point entropy-concavity problem also remains
INCOMPLETE. The complete event score and real affine Rayleigh squares were
retained throughout. This verdict does not infer universality from finite
non-hits. Review scope and frozen-object bindings are in
`verifications/index.md` and `provenance.md`.

## Exact partial results

1. The beta-zero slice is nonempty in the connected strict domain. On an
   explicit rational affine segment a rigorous sign change proves an exact
   root in a rational bracket, and every point of that bracket satisfies

       0.6615279258817643 < det(N)*alpha < 0.6615279260967083 < 1.

   The proof is in `falsification/beta_zero_existence.md`. It proves no
   uniqueness, no global zero-set description and no counterexample.
   Its strict negative endpoint also refutes beta>0 throughout the domain.
2. For fixed interior means x_i and fixed nonzero real edge ratios,
   a dense weak-edge ray has

       beta=4 sqrt(product_i x_i(1-x_i))+O(t)>0

   for sufficiently small t. The proof is
   `main/dense_weak_edge_beta_v1.md`. Joint degenerations of means or edge
   ratios are excluded; local entropy concavity itself was already known.
   The nonauthor review reconstructs formulas and checks fixed small-t
   cases; it supplies no separate uniform symbolic remainder theorem.
3. A rational direction satisfies Lambda'[D]=0 exactly but has positive
   cofactor acceleration. Thus a pure acceleration-sign shortcut fails.
   The true negative entropy Hessian remains positive at that witness.
4. Locking the two conditional log-odds derivatives gives a valid stronger
   Fisher projection Qlock. However its proposed cofactor dominance is
   strictly false. A rational exact Lambda tangent gives

       -0.482450470481640975 < max_k Qlock_k-C
                              < -0.482450470481640973,
       53.17428270279292381 < F-C < 53.17428270279292383.

   This also rules out every convex combination of those same three
   Qlock bounds as a universal cofactor bound. It does not refute
   F>=Qlock, Lambda-tangent concavity, B0, or global concavity. The witness
   is not asserted to be the H-optimizing direction or a beta-zero kernel.

## Exact remaining obligation and substantive stop

At a beta-zero kernel, the trace-normalized H optimizer D_H satisfies

    H(D_H,E)=eta(E)/alpha for all symmetric E,
    eta(D_H)=1, Lambda'[D_H]=0.

The missing statement is a DPP-specific proof that the complete Fisher
obeys F(D_H,D_H)>=2 tr(N adj D_H), or a rigorous counterexample on the
actual beta-zero set. Simply restating this as det(N)*alpha<=1 is the
EQUIVALENT_BLOCKER. The stronger whole Lambda-hyperplane bound also remains
open. It cannot be supplied by the tested three locked projections.

The full-square stationary unit and the distinct locked-odds projection
unit end at this same Fisher-versus-cofactor gap. The latter was followed
by one bounded falsification unit because it introduced an actual new
term, and its proposed sufficient condition is now strictly refuted.
The weak-edge and root objects are preserved partial progress; neither
closes the shared gap. Under the agreed two-distinct-unit stop rule the
route is STOPPED_SUBSTANTIVE. Final nonauthor review is integrated.
No expanded scan, autonomous wakeup or background continuation is planned.

## Correctness, formalization and value are separate

The final nonauthor review is one reused independent reviewer context,
not two independent theorem verifiers. Author labels remain frozen and
must be read with the latest review and any explicit addendum. Interval
certificates prove only their stated finite or bracket objects.

No B0 or global proof was formalized in Lean. The round-one Lean smoke test
is not evidence for these new claims. Full asymptotic and interval-proof
formalization was not undertaken. Novelty is NOT_CERTIFIED. These are
auxiliary mechanisms and explicit obstructions; they are not claimed to
solve the open problem or meet a conference-level core-theorem threshold.
