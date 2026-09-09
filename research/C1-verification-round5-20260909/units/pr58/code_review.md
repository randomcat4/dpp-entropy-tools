# PR58 static code review

STATUS: CORRECT

SCOPED VERDICT: ACCEPTED_SCOPED for static implementation shape. The script appears to implement the PR58 formulas faithfully, but it is author code and its saved output is not an independent C1 reconstruction.

## Files Reviewed

- `source-snapshots/pr58/code/verify_middle_compensation.py`, 173 lines.
- `source-snapshots/pr58/output/verify_middle_compensation.txt`, 30 lines.
- Accepted PR54 fixture checker copied from public base for source comparison only: `source-snapshots/base/research/I05-23-20260909/code/verify_local_and_matching.py`.

## Static Findings

No blocking source-level bug found.

The PR58 script uses the same fixture literals as accepted PR54: PR58 `verify_middle_compensation.py:11-25` matches PR54 `verify_local_and_matching.py:15-29`. PR58 then rebuilds atom probabilities through the complete-event determinant formula at `verify_middle_compensation.py:31-46`, matching the accepted checker pattern at PR54 `verify_local_and_matching.py:35-45`.

The rank-two feature construction is aligned with the prose. PR58 computes `G_A`, `G_C`, `a=tr(G_A G_C)`, `b=det(G_A)det(G_C)`, and `mu=p_Ap_C` at `verify_middle_compensation.py:48-56`, then checks the global zero means at `:58-59`. This matches PR58 `RESULT.md:160-172` and the accepted rank-two likelihood interface in `accepted_main/research/I05-23-20260909/ADDENDUM_OUTER_WEDGE_FLOW_RATE.md:5-19`.

The interval certificate code matches the displayed criterion. `q_range` checks endpoints and the rational vertex of each quadratic at `verify_middle_compensation.py:67-82`; `certify_interval` checks `qminus>0`, builds the rational `Psi`, computes the lower moment bound, and asserts the squared strict margin at `:84-105`. These correspond to PR58 `RESULT.md:174-202` and `:218-224`.

The log enclosure code is structurally appropriate for the `s=10` claims. It uses the atanh transform and a rational absolute-remainder bound at `verify_middle_compensation.py:110-121`; interval addition with signed coefficients is handled at `:123-126`; `Wup<0` and `Tlo>0` are asserted at `:154-156`. The total-curvature integrand split at `:144-150` matches `Phi + 4y^2/q + y psi`: rational part `4u^2/q + 4y^2/q + 8yu/q`, log coefficient `2u+10y`.

The saved output has the expected print sequence from `verify_middle_compensation.py:158-173`: pass marker, rank/event count, four interval certificates, the corridor conclusion, and the `s=10` sign/curvature intervals at `verify_middle_compensation.txt:1-30`.

## Reproducibility Notes

The script imports only SymPy beyond the standard library (`verify_middle_compensation.py:4-9`) and PR58 states the author run used Python 3.13.5 and SymPy 1.14.0 at `RESULT.md:276`. No requirements file or lockfile is added in PR58, so reproducing the author environment requires installing a compatible SymPy manually.

All proof gates are Python `assert` statements (`verify_middle_compensation.py:44-46`, `:58-59`, `:87`, `:95`, `:104`, `:154-156`). The documented reproduction command at `RESULT.md:266-270` uses plain `python`, so those gates are active in the intended run. For archival robustness, a future checker could replace asserts with explicit exceptions so `python -O` cannot disable them.

The decimal calls at `verify_middle_compensation.py:170-173` occur only after exact rational assertions. I found no place where a floating value is promoted to a theorem in the script.

## Review Boundary

I did not execute this script, import SymPy, recompute rational margins, or independently check the log enclosures. C2 should implement an independent reconstruction and treat this script as an author reference, not as the verifier of record.
