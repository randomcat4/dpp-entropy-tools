# Frozen computation contract

Frozen 2026-09-09. Source commits and output paths are listed in README.md. The exact upstream instructions for PR43 are `research/I05-W1-20260909-R2/continuation/CODEX_VERIFICATION_TASKS_v2.md`; PR41 uses `research/N3/round3/I05-W4-20260909/round2/`.

## Domains and acceptance

PR41: reconstruct probabilities of all eight configurations from inclusion determinants. Differentiate the affine kernel in all six real symmetric coordinates. Test the stated algebraic identities in the strong-coupling, block-decoupling, and missing-edge calculations. A verified identity is distinguished from positivity arguments or theorem units requiring analytic review. Do not replace all directions by a finite list of sampled directions.

PR43 B/C: reconstruct all 256 configurations of the exact 3+5 fixture at each of t = 1/5, 1/2, 1, and every conditional configuration. Check refresh, reversible, and occupation-channel obstruction fixtures exactly. Strict kernel legality requires exact rational criteria, not floating eigenvalues.

PR43 D: use exactly

```
C = [[1/2,1/12,1/15],[1/12,2/5,1/20],[1/15,1/20,3/5]]
V = [[1,0],[0,1],[1,1]]
```

States are 000,001,010,011,100,101,110,111. The rightmost bit is matrix coordinate 1, the middle bit coordinate 2, and the leftmost bit coordinate 3, matching the upstream helper's reversed-bit labels. The implementation records this map explicitly. All 56 ordered pairs x != y have variables r_xy >= 0. Keep eight flow-balance equations and four feature equations at every state. For f = G11,G12,G22,d and lambda = 1,1,1,2:

```
sum_{y != x} r_xy - sum_{y != x} r_yx = 0
sum_{x != y} r_xy (f(x)-f(y)) = -lambda mu(y) f(y)
```

Here mu is the complete-event DPP law, G(T)=V^T(C-E_{T^c})^{-1}V, and d=det(G). No detailed balance equations may be added. Accept a rational feasible flow verified against every equation, or a rational Farkas vector with the documented sign convention and exact separating inequality. Floating optimization is discovery only. An implementation's own exact substitution is not independent certificate review.

The literal v2 D equations are authoritative. The old continuation handoff, rational-example payload and generated payload still describe reversible conductances; they must not be used to define this LP. C3 identified this interface hazard in issue 45. The later PR43 document revision renames this object G without changing the fixed matrices or feature equations; see `source_version_notes.md`.

## Resources, error and stop

Initial aggregate cap: eight CPU threads, 32 GiB memory, no GPU. Actual initial allocation: three processes with one arithmetic thread and at most four GiB each; main retains room for bounded replay/review. Dependency versions and run metadata are recorded in the unit outputs. No system/global environment changes.

Each initial unit has a 45-minute wall ceiling. No random input scan and no extension of the previous single-box search is authorized by this packet. All accepted statements use exact rational/symbolic identities. A timeout, failed identity, or unresolved rational reconstruction is an explicit retained result. Long jobs checkpoint each completed object, save PID/invocation/logs/exit status, and check the owned PID before recovery. Do not stop jobs belonging to another unit.

## Deferred dependencies

PR43 E depends on D feasibility and author clarification of the closed legal endpoint / strictly positive event-bound requirements, and the meaning of the requested 1e-20 interval width. PR43 F supplies an acceptance gate but no finite candidate list or search box; request these before claiming a search. PR43 G does not authorize automatic random replacement of C,V. These questions are posted in issue 45. The initial exact work does not depend on their answers.

General real-kernel entropy concavity and true stationary entropy-rate targets remain outside this packet's acceptance claims. No numerical failure of an auxiliary sufficient condition is called an entropy counterexample.
