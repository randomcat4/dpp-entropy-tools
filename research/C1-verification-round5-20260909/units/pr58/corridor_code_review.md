# PR58 original corridor independent evidence static code review

Reviewed implementation: `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py`.

Reviewed execution wrapper and artifacts: `source-snapshots/pr72_corridor/execution/run_guard.sh`, `source-snapshots/pr72_corridor/execution/RUN_LEDGER.json`, and `source-snapshots/pr72_corridor/outputs/run01/*`.

Overall static-code status: CORRECT.

Scoped verdict: ACCEPTED_SCOPED. No blocking static implementation defect was found in the independent finite-evidence source. This code review does not execute the verifier or independently recompute its fractions.

## Independence and dependencies

The verifier is self-contained and uses the Python standard library plus `Fraction`; its import block is at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:11`-`24`. It explicitly blocks CAS/numeric modules through `FORBIDDEN_MODULE_PREFIXES` and `reject_forbidden_modules` at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:62` and `77`-`84`.

The input loader reads the frozen binding and `RESULT.md`, parses the literal section-4 matrices, constructs `B=UV^T`, and records the author checker as not opened/executed/imported at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:865`-`920`. The raw `inputs.json` repeats those author-checker flags at `source-snapshots/pr72_corridor/outputs/run01/inputs.json:200`-`203`.

The author output reference is used only after the independent event, identity, corridor, and s10 layers have been built. That comparison order is visible in the run sequence at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:843`-`852` and in the comparison function at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:1467`-`1548`.

## Event and identity construction

The event construction is direct. The source forms complete-event matrices from the six-point kernel at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:529`-`563`, computes polynomial determinants with exact fraction polynomial arithmetic at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:250`-`347`, and enumerates all left/right masks at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:924`-`992`. It extracts only even terms up to degree four in `t`, checks the constant term, and then runs the Schur/resolvent `a,b` comparison as a posthoc check at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:955`-`968`.

The identity layer checks global `a,b` cancellations, both conditional fiber cancellations, and all principal/complementary Mobius identities at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:1039`-`1077`. The artifact records the Mobius identity status and subset count at `source-snapshots/pr72_corridor/outputs/run01/identities.json:312`-`314`, and status OK at `source-snapshots/pr72_corridor/outputs/run01/identities.json:2704`.

## Corridor interval code

The code computes extrema of each quadratic `q_s=1-sa+s^2b` by checking endpoints and the rational vertex when present at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:623`-`640`. The corridor routine verifies the four intervals cover `[3,15]`, checks positive `q_minus`, computes `Psi`, `M2lower`, the left bound, and the squared margin, and fails if any strict margin is nonpositive at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:1143`-`1224`.

The raw `corridor.json` records the four interval labels and no-gap coverage at `source-snapshots/pr72_corridor/outputs/run01/corridor.json:2`-`10`, exact rational endpoint/margin fields and strict flags for the four intervals at `source-snapshots/pr72_corridor/outputs/run01/corridor.json:4993`-`5018`, `10008`-`10033`, `15059`-`15084`, and `20074`-`20099`, and status OK at `source-snapshots/pr72_corridor/outputs/run01/corridor.json:20158`.

## s10 log and curvature code

The log enclosure is a one-sided rational atanh enclosure at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:658`-`696`. The `s=10` routine computes `q`, `u`, `y`, `psi`, `W`, and the direct curvature contribution over all events at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:1282`-`1327`, records per-event log data at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:1329`-`1352`, and checks the `q_min`, derivative log cancellations, normal-form equality, `W` sign, and curvature lower/width targets at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:1353`-`1378`.

The raw `s10.json` records `W.upper_endpoint_negative: true`, the `W` width check, `log_terms: 80`, `q_min_matches_expected: true`, status OK, the curvature lower check, and the curvature width check at `source-snapshots/pr72_corridor/outputs/run01/s10.json:20`-`22`, `32802`-`32815`, and `33057`-`33061`. A structural artifact read found 64 event records with 80 stored log terms each, for 5120 stored atanh terms; this was not a value recomputation.

## Reference comparison and output boundaries

The required reference keys are defined as `Amax`, `Bmax`, six corridor quantities for each of four intervals, and `s10.q_min` at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:763`-`773`. The comparison routine records missing, mismatched, matched, and extra keys before failing on any required discrepancy at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:1491`-`1548`.

The raw comparison artifact records all 27 required exact matches and no required missing/mismatched keys at `source-snapshots/pr72_corridor/outputs/run01/reference_compare.json:4`-`541` and `546`-`582`. It also records that printed decimal endpoints are treated only as rounded display text at `source-snapshots/pr72_corridor/outputs/run01/reference_compare.json:544`.

The wrapper and ledger record the execution boundary: non-overlap lock, fixed deadline, one CPU/thread settings, no GPU, run start/finish markers, and exit 0 at `source-snapshots/pr72_corridor/execution/run_guard.sh:21`-`53` and `source-snapshots/pr72_corridor/execution/RUN_LEDGER.json:17`-`41`. The public pass file lists completed layers and no failures at `source-snapshots/pr72_corridor/outputs/run01/MACHINE_PASS.json:3`-`10` and `23`-`47`.

## Static review limitations

I did not run the code, recompute determinants, evaluate rational inequalities, run SymPy, compare numeric outputs independently, or perform formal verification. The static conclusion is that the independent source and raw artifacts have the right shape, scope boundaries, and failure gates to support C1 acceptance of the original finite evidence when paired with C2's machine pass.

The only remaining source issue found in this closure is not a code defect: original `RESULT.md` (5.1) should mark the displayed `W(10)` upper-endpoint decimal as approximate/rounded display text. No code change is required for that wording repair.
