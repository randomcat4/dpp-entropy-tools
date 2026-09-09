# PR58 Corridor Finite-Certificate Second Review

Overall verdict: CORRECT within the bounded static-audit scope. The independent packet gives a complete exact finite certificate for the fixed `3+3` middle corridor `3<=s=t^2<=15` and for the `s=10` negative-`W` / positive-curvature point, subject to the stated limitation that I did not rerun the checker. This closes my earlier "INCOMPLETE in this review" status for these finite certificates at static SECOND level.

## Status Table

| claim | status | evidence |
| --- | --- | --- |
| 25-file packet binding and file integrity | CORRECT | `corridor_input_binding.json`; all SHA-256 hashes matched local files |
| Independent implementation avoids author checker and CAS/numeric modules | CORRECT | implementation lines 1-9, 62, 77-84, 865-920, 1561-1579 |
| 64 complete-event construction | CORRECT | implementation lines 529-563, 924-992; `events.json` has `event_count=64` |
| `q(t)=1-a t^2+b t^4` extraction and posthoc `a,b` resolvent check | CORRECT | implementation lines 955-968; no odd or degree `>4` terms recorded in `events.json` |
| Product normalization and global cancellations | CORRECT | implementation lines 1039-1042; `identities.json` records `sum_mu=1`, `sum_mu_a=0`, `sum_mu_b=0` |
| Left/right fiber cancellations | CORRECT | implementation lines 1044-1057; `identities.json` has 8 left and 8 right zero fibers |
| Principal and complementary Mobius identities | CORRECT | implementation lines 1059-1077; `identities.json` has `subset_count=64` |
| Strict legality bridge on `[3,15]` | CORRECT | implementation lines 1191-1192, 1273-1278; complete event positivity plus both Mobius families |
| Exact interval extrema and margins | CORRECT | implementation lines 623-640 and 1143-1222; `corridor.json` has four intervals, 64 event extrema per interval, strict `q` and strict margin on each |
| 27 exact rational comparisons with frozen author output | CORRECT | implementation lines 711-773 and 1467-1548; `reference_compare.json` status `MATCHED_REQUIRED_EXACT_FRACTIONS`, matched count 27 |
| `s=10` negative `W(10)=E[b psi]` | CORRECT | implementation lines 1282-1314 and 1369-1374; `s10.json` has negative rational upper endpoint and width check passed |
| `s=10` full scaled curvature `t^2 I''(t)>0.170377...` | CORRECT | implementation lines 1316-1327 and 1357-1378; `s10.json` has lower and width checks passed |
| Distinction between `W` and scaled contribution `V=s^2W` | CORRECT | implementation lines 1307, 1311-1314 use `mu*b` for `W`; curvature uses `y=s^2b` separately |
| Original (5.1) decimal display concern | CLOSED by wording patch | `decimal_display_patch.diff`; see `decimal_display_closure.md` |

## Complete Events And Legality

The implementation constructs complete-event probabilities directly from the displayed rational matrices rather than importing the author checker. For an included coordinate it uses the corresponding column of `K`; for an excluded coordinate it uses the corresponding column of `I-K` (implementation lines 529-550), then takes the exact determinant. This is the complete-event DPP atom formula, equivalent to the signed diagonal-subtraction form.

For the full `6x6` radial kernel, the code builds the polynomial kernel with cross block `tB` (lines 553-563), enumerates all `8 x 8 = 64` left/right complete events (lines 947-951), divides by the positive product atom `mu=p_A p_C` (lines 952-955), and rejects any likelihood polynomial with an odd term, degree above four, or constant term different from one (lines 956-965). It then checks the extracted `a,b` against the Schur/resolvent formula as a posthoc cross-check (lines 966-968). The `events.json` packet records all 64 events from `000000` through `111111`, and my JSON inspection found no bad constant or degree record.

The legality bridge is also complete. The code verifies product normalization and global cancellations (lines 1039-1042), all 8 left and 8 right fiber cancellations (lines 1044-1057), and both Mobius families for all 64 subsets as polynomial equalities (lines 1059-1077). Therefore strict positive complete atoms on the corridor imply positivity of all principal minors and all complementary principal minors by summing complete atoms over supersets or disjoint events. For this fixed finite real symmetric kernel, that is enough to certify `0<K(t)<I` throughout the corridor.

## Corridor Inequalities

For each interval `[3,9]`, `[8,12]`, `[11,14]`, and `[14,15]`, the implementation checks endpoints and the rational vertex `a/(2b)` when it lies in the interval (lines 623-640 and 1165-1188). The recorded `corridor.json` has 64 per-event extrema on each interval; only `[11,14]` has internal vertex candidates, and those are included.

The interval bound then matches Corollary 3.2 from the original analytic review. It computes `q_-`, `q_+`, `Psi`, `M2lower`, the positive left side, and the squared margin (lines 1191-1204). It rejects nonpositive `q_-`, nonpositive moment lower bound, nonpositive left side, or nonpositive squared margin. The JSON output records strict positivity for `q` and for the squared margin on all four intervals, with verified coverage of `[3,15]` (lines 1217-1222 and `corridor.json` coverage fields).

The exact values required by the author output are compared as rational numbers, not decimals. `reference_compare.json` lists 27 mandatory comparisons and all are `MATCH`: `Amax`, `Bmax`, the six displayed corridor quantities for each of four intervals, and `s=10 min q`.

Thus, combining this finite certificate with the already accepted analytic Corollary 3.2 proves the fixed-fixture statement `H''(t)<0` for `3<=t^2<=15`. The proof is still only for this fixed fixture and this fixed corridor.

## The `s=10` Log And Curvature Certificate

For `s=10`, the implementation evaluates each of the 64 rational `q` values and rejects nonpositive values; it also checks the exact minimum against the frozen value `121400093597/249280204050` (lines 1300-1308 and 1353-1356).

The log enclosure uses the atanh series with one-sided signed remainder (lines 658-695). This is applied per complete event at `s=10` (lines 1308-1314). The `W` interval is accumulated with coefficient `mu*b` (lines 1311-1314), so it certifies the author's `W(10)=E[b psi(u_10)]`. It does not silently switch to the scaled contribution `V=s^2W`; the scaled curvature computation uses `y=s^2b` separately (line 1307).

The curvature check includes both parts of the second derivative. The implementation forms `t^2 q''` as the acceleration log coefficient (line 1316), forms the Fisher contribution `4(u+y)^2/q` (line 1323), and accumulates the log and rational pieces into `t^2 I''` (lines 1326-1327). It also checks that the derivative log coefficient and rational Fisher expression agree exactly with the displayed normal form (lines 1317-1325 and 1365-1368), that the `+1` and `log(mu)` terms cancel by global and fiber sums (lines 1357-1364), and that the lower endpoint and width meet the stated targets (lines 1371-1378).

The stored `s10.json` has a negative exact rational upper endpoint for `W(10)`, a width below `5.83e-83`, a curvature lower endpoint above the stated positive threshold, and a width below `8.71e-79`. Therefore the `s=10` finite certificate supports both claims: the sufficient sign law `W(s)>=0` fails for this fixture, while the full retained curvature remains favorable there. This is not an entropy counterexample.

## Limits

No critical gap was found in the bounded finite-certificate packet. The acceptance here is static: I inspected the implementation and recorded JSON outputs, but did not rerun any checker or perform new arithmetic. The result does not extend to the whole legal chord, other fixtures, joint-additive material, novelty, or formal verification.

No new machine obligation is needed for this scoped certificate. A future formal or replay-level audit could rerun the executable from the bound head, but that is a different evidence layer.
