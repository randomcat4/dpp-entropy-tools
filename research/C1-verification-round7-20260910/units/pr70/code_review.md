# PR70 FIRST static code review

Scope: static source review of `source-snapshots/pr70/verify_bridges.py` only. I did not run Python, SymPy, author scripts, finite certificates, or formal tools.

Overall static verdict: `ACCEPTED_SCOPED`; no blocking source defect found for the script's stated role as an author algebra-identity checker. The script is not independent evidence and does not certify the post-checkpoint rational/log obstruction.

Immutable source URL:

`https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/verify_bridges.py`

## Findings

No `NEEDS_FIX` finding was identified for the stated public verifier scope.

## Checked behavior

- Complete atom construction uses inclusion-exclusion over all masks and asserts total mass one: `verify_bridges.py:8-16`, `verify_bridges.py:40-41`.
- Assert gates are centralized through exact SymPy cancellation: `verify_bridges.py:17-21`.
- The script checks complete event conditional jets and the two-leaf marginal acceleration term: `verify_bridges.py:40-52`.
- The selected-side cofactor grouping and additive-table cancellation are checked symbolically: `verify_bridges.py:54-61`.
- The scaling check uses a symbolic third-coordinate scale and verifies selected masses scale by the square of that scale, matching the prose convention `lambda=scale^2`: `verify_bridges.py:63-69`.
- The generic `L/C/R` coefficient check includes mixed direction variables and the lower-block congruence for `R`: `verify_bridges.py:71-84`.
- The quadratic-perspective sum of squares is checked as an exact identity: `verify_bridges.py:86-94`.
- The four-evaluation Gram inverse basis identities are checked: `verify_bridges.py:95-107`.
- The parallel-sum code is only a noncommuting fixture, and the source text correctly says the universal proof is in prose: `verify_bridges.py:109-113`.

## Static limitations

- The script relies on `assert`, so optimized Python would bypass the checks. The packet warns against `python -O` in `README.md:29-31` and `verification.md:13`; this is therefore a documented limitation rather than a hidden defect. A hardened verifier could replace `assert` with explicit exceptions.
- The `L/C/R` equality is checked by taking the Hessian with respect to direction variables. This is acceptable because the compared expression is constructed as a homogeneous quadratic form in those variables. If the script is later edited to include affine or constant terms, it should also check the full residual directly.
- The script does not prove positivity inequalities, determinant signs, legal-domain coverage, logarithm enclosures, Jensen intervals, or issue73 filament outcomes. Those are outside this file's stated role.
- The script imports SymPy and writes an output JSON, but no CI or proof-assistant result is claimed by the packet.

## C2 code/evidence requirements

For independent finite review, C2 should not treat `verify_bridges.py` or author output JSON as independent evidence. C2 should rebuild the event generator, quotient derivatives, rational arithmetic, log interval enclosures, and output artifacts independently from public formulas and literal inputs. At minimum, C2 raw artifacts should include source hashes, command transcript, environment versions, exact input echo, atom jets, exact rational signs, outward log/Jensen intervals, and endpoint legality certificates.
