# PR91 C1 FIRST frozen source scope

Reviewer role: C1 source/evidence-only FIRST for PR91. This review is bounded to frozen head `c7a072ec4eea0c5b0f445bca5796873a9e234948` against base `65e59a46b49cd2dbb5c779a4cfae8cef26441984`. The immutable comparison URL is <https://github.com/randomcat4/dpp-entropy-tools/compare/65e59a46b49cd2dbb5c779a4cfae8cef26441984...c7a072ec4eea0c5b0f445bca5796873a9e234948>.

`SOURCE_BINDING.json` reports 14 added files at this head. I read the frozen PR91 source/evidence packet listed below, plus the frozen source binding and compare metadata. I did not read prior FIRST/SECOND/C3 review reports, old PR77 verification/output, private raw archives, or any later head.

| Public alias | Lines | Git blob | SHA-256 |
|---|---:|---|---|
| `source-snapshots/pr91/SOURCE_BINDING.json` | n/a | n/a | n/a |
| `source-snapshots/pr91/COMPARE.json` | n/a | n/a | n/a |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/README.md` | 41 | `afdc44254678ab3f46b28f23fb95982e4b298b3b` | `ca901e26f75f5dec054980f9c6d791f1cedddb1fa0d076a8c0cd48c3268813ee` |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/RESULT.md` | 118 | `0ff85de23cf2065fb10bc6357bbe14486e86a37c` | `3e1b2547637aac64598c1ddff840c7beaf2906b517c88c916fbe4db30176264b` |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/proof.md` | 238 | `32aa6310285b8649663e380e79dba2da4d8b2f70` | `58da558b23f99bc815ebf15b53cd5de3db9434982cab56b5830f6b6a1e615847` |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/coding_and_fisher.md` | 152 | `254b9cb751681ee4a11231810988c6ae690a9365` | `ca55d4bb0c2b21b644d0e3a96f583824c19a0d54e31f007c57621b8e7b955b9a` |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/curvature_certificate.md` | 128 | `a0eb94ce87dc8b2dd35d1154e383e484f374c97c` | `9aa41986ec263140dd8b2d76059ee6cbb21bf9bd39e84d122f84dd568dc47bdc` |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/post_handoff_cancellation.md` | 160 | `09ba22b1365d2014c48f0b508dcad32498dea68b` | `152623f50a4c8dad9d2234ecfef99db5805dea46cd04dd54b6379d06bff97988` |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/sources_and_attempts.md` | 44 | `1c9e3733a5fd7c18112bb35180824bd61644f557` | `a3a62c4fa73f03e78b8361d07afa2a7caa696dceef59caa93450a5584cd1fb33` |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/compute_contract.md` | 59 | `76b25839408ca416fad7737c643e788136619311` | `81112767b2e4b53c64b69a512bfaa55198b3c53652d2aa081756bc5ee99d6ffc` |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/code/exact_checks.py` | 187 | `6ea28272df620b778dcc268edd7b3e4000be3888` | `c28d371ee6633b5ba3015f928802eff540d6818345ef64b826b46437ad847771` |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/code/check_tightening.py` | 47 | `da982c0509126c2ea2929ef8ed6d4e703e2ef74e` | `40a54793e67d4293dfaa9e9ce674c2e3bc131e3941a7b646842b7fdf051153c8` |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/code/poisson_scout.py` | 142 | `976b836b13496fb1b87cec452e02ef9fe149f41f` | `ab2ad8b10256cca871cc7c4297550adb6160fcad3f3259f26183f601b282187d` |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/output/exact_output.json` | 45 | `5f06208ee0734dd2c637d8d59d4529060b98efaf` | `4349d4e9e844acef4b50f689dd5a3a5b2dd1ef58f314afc07333a239b51eb638` |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/output/tightening_output.json` | 28 | `e40627f5ab00564532429e2c291e5978a88b7059` | `cf7803dea2e980729f5bc8c69c841c7aedabc32620427bd4f852666f4df9a62f` |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/output/scout_summaries.json` | 56 | `783e325666d5c61121445eadc8ef3150742cd049` | `5dfc98ecc0386d7eff55dfaa1f89cfc9bfba96e4bc796bf4219edf628a47ac0d` |

Scope actually reviewed:

- Complete-event correction-state/Riccati representation and the four branch weights.
- Positivity, normalization, branch contraction, and full probability-law contraction including changing weights.
- Per-original-coordinate entropy-rate normalization and its factor `1/2`.
- Parameter jets, full coding Fisher, smooth resolvent, invariant-law second response, and three-Poisson residual certificate.
- The post-handoff affine-cancellation refinement and whether it preserves the full response formula.
- Source/evidence status for author exact checks, 252 complete events, scout samples, output JSON, and the compute contract.

Explicit exclusions:

- No arithmetic execution, Python/SymPy import, checker run, finite enumeration, interval/log/entropy job, formal check, numerical reconstruction, or author-source edit was performed.
- No independent C2 or continuum job was created or authorized by this FIRST.
- PR77 fixed-point finite certificates, PR79 upper-budget results, author PASS strings, scout samples, and private raw archives were not used as proof of PR91 claims.
- No private Drive raw data was downloaded or linked in these reports.
- Novelty, priority, formal verification, merge readiness, and the final whole-interval sign `h''(t)<0` are outside this FIRST.

No extra predecessor source was needed for the bounded analytic judgment: PR91’s current packet states the fixed object, complete-event algebra, contraction, rate normalization, response formulas, and open gates directly.
