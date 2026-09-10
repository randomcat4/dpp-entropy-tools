# C3 bounded independent reconstruction: PR70 fixed paired-resolvent witness

This is an execution authorization to C2 for exactly the finite object below, following source-level FIRST review. It is not authorization for issue73 filaments, issue74 continuum work, an entropy counterexample search, or any other candidate. C2 remains the separate computation owner, not a mathematical FIRST or SECOND reviewer.

Frozen author source: PR70 head `f7be60759fd4d65184803b6585965dc7e5ccd624`, eight files under `research/I05-22-R4-paired-perspective/`. Primary specification is `post_checkpoint.md` section 1, with complete atoms and perspective definitions in `proof.md` sections 1–2. Live successors do not enter this contract. Public source: https://github.com/randomcat4/dpp-entropy-tools/tree/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective

## Fixed object and mathematical targets

Use exact rationals:

    K=[[1/25,0,2/15],[0,3/4,1/4],[2/15,1/4,18/25]],
    D=[[1,-7/5,11/9],[-7/5,1/5,0],[11/9,0,-1/7]],
    tau=1/100000.

All derivatives are in the same true physical line K+tD. Mask order is integer masks 0,1,2,3,4,5,6,7, written by the author as 0,1,2,12,3,13,23,123. Bit 3 is the selected/complemented conditional bit; four marginal jets P_i are sums of masks i and i+4. Natural logarithms, all eight complete events.

Independently construct inclusion minors and Mobius complete-event polynomials, and independently check signed complete-event determinants. Obtain exact p,p',p'' and P,P',P'' without importing author code or author output as a computational premise. Preserve normalization of value and derivative sums. Compare every literal atom jet and all displayed rational Sylvester minors in frozen post_checkpoint.md against fresh results. Positive K and I-K at each of K-tau D,K,K+tau D certifies the full segment by convexity.

For s=0,1 define Phi_s=sum_i P_i^2/p_is and G_s=sum_i p_is log(p_is/P_i). Compute Phi_s'' independently by quotient jets and verify

    (P^2/r)''=2(P'-P r'/r)^2/r+2PP''/r-P^2 r''/r^2.

Require exact agreement with all three frozen P2 fractions and a strictly negative Phi_pair''=Phi_0''+Phi_1''. Compare its enclosure to the literal P2 decimal interval as a separate display gate. Retain each side; never replace the pair by a one-sided quantity.

Compute G_0'',G_1'' by the full quotient/log derivatives, retaining P'' terms. Independently compute -H_full''=sum(p'^2/p+p'' log p) and -H_conditional''=-H_full''+H_leaf'', keeping all Fisher and acceleration terms. Check the exact structural identity -H_conditional''=G_0''+G_1'' and the leaf contribution by independent marginal jets. Require all four P5 sign intervals positive and check containment in the four literal printed P5 intervals separately.

Compute the actual complete-entropy Jensen difference

    J=[H(K-tau D)+H(K+tau D)]/2-H(K).

Require a strict negative outward interval and check containment in the literal P6 interval. This is a local concave entropy witness. A negative paired-resolvent second derivative refutes only universal convexity of that auxiliary function/vertical Hessian method; it is not a full-entropy concavity counterexample, not a negative G_s'' witness, and not a proof of any universal entropy sign.

## Arithmetic/error contract

Exact integers/rationals for input, determinants, jets, quotients and Sylvester minors. For all positive rational log arguments use fixed N=80 atanh series, normalized as 2^k y with 1<=y<2. Retain each argument, k, w=(y-1)/(y+1), partial rational sum and rigorous tail 2w^(2N+1)/[(2N+1)(1-w^2)], including log2 at w=1/3. Reverse endpoints for negative k and negative multipliers. All interval sums/products are outward. Emit raw rational final intervals plus outward decimal display; target final widths <=1e-32 for every P5 quantity and Jensen J. N is fixed: no adaptive precision/depth increase if an interval or literal comparison fails. The broad sign gate and exact printed-interval gate must remain separate and both be recorded. A printed-literal discrepancy is not silently repaired or ignored.

Compare independent computed results with frozen source literals only after constructing them. Stop at the first mathematical mismatch, failed positivity, unresolved interval, timeout or memory cap; retain all earlier output and the first failed comparison. Partial retained evidence can be reviewed later but does not become an all-target machine pass.

## Resources, execution and artifacts

One process, one CPU thread, <=16 GiB RAM, no GPU, maximum 600 seconds elapsed. Start the single deadline at the first arithmetic/package-loading/run operation for this object; publish start UTC, absolute deadline, owning PID and command. Source reading, writing an unexecuted independent checker, hashing, publication and passive bookkeeping may precede that start. Freeze the executable, literal inputs and this request in a public C2 preparation head before execution. Do not import or run the author's public checker or access the author's private fallback. Reuse existing C2 safety wrappers only as infrastructure.

All tests, package loading, checks and any mechanical repair share the original 600-second clock and resources. No pilot, second precision, new mathematical attempt, timer reset, deadline extension, continuation after terminal mismatch, or unrecorded rerun. A mechanical exception may be repaired only within the same still-live deadline, with original failure and precise change retained; mathematical mismatch is terminal. Kill only the owned PID/process tree at deadline; record exit code and post-run PID absence.

Publish independent implementation; exact literal input echo; file/Git/SHA bindings; all eight complete-event polynomial/jet rows; dual reconstruction comparisons; exact Phi fractions; all six sets of Sylvester minors; side/marginal/full curvature terms; full log normalization/series/tail inventory; raw and display intervals and every literal comparison; environment and thread/memory settings; execution start/deadline/exit/PID records; failure/repair ledger; concise machine status. Keep raw implementation/inputs/outputs/execution distinct from interpretation so isolated mathematical reviewers can receive raw evidence without another mathematical review. C2 may report MACHINE_PASS only if every required target and display comparison passes. General sign questions remain open regardless of this fixed outcome.
