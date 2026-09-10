# Fixed-object machine result

**MACHINE_PASS**, run01, exit 0. All 178 ordered checks passed; there was no mechanical repair or failed attempt. Source was public before execution. The single 600-second clock began at 2026-09-10 02:10:08 UTC with immutable deadline 02:20:08 UTC; the guard recorded completion at 02:10:10 UTC. Arithmetic PID 175598 was absent at 02:10:38 UTC. Reported checker time was 1.154991258867085 seconds and peak RSS was 22568 KiB, under one CPU thread and the 16 GiB cap.

Both independent event constructions agree for every polynomial coefficient. All 24 literal atom jet entries, six sets of leading Sylvester minors, exact P2 fractions, side/full/marginal derivative identities, probability normalizations, and fixed N=80 error gates passed. All required P5 and Jensen arithmetic widths are at most 1e-32. Broad signs and containment in the original literal printed intervals passed separately.

Outward 40-place displays from the raw evidence:

| Quantity | Lower | Upper |
|---|---|---|
| G0'' | 6.3836477267924650532084343120505471181471 | 6.3836477267924650532084343120505471181472 |
| G1'' | 9.2177300388618574492302078622332257604485 | 9.2177300388618574492302078622332257604486 |
| -Hconditional'' | 15.6013777656543225024386421742837728785956 | 15.6013777656543225024386421742837728785957 |
| -Hfull'' | 41.8563777656543225024386421742837728785956 | 41.8563777656543225024386421742837728785957 |
| Jensen | -0.0000000020928189192765834280721741836172 | -0.0000000020928189192765834280721741836171 |

The paired-resolvent second derivative agrees exactly with the negative fraction in P2; both sides are retained in `outputs/run01/phi_exact.json`. The 28 rational log arguments and separate log2 certificate include every normalization, series term, partial sum and tail. All event polynomials, jets, side Fisher/acceleration terms, marginal contributions, rational interval endpoints and 178 comparison rows are retained under `outputs/run01/`.

This fixed computation supports the stated auxiliary-method obstruction and locally concave entropy witness. It does not refute entropy concavity, prove a universal entropy sign, or replace isolated mathematical FIRST/SECOND review. No PR77, issue73/74 continuum, PR79 deeper enumeration or PR80 task was executed in this run.
