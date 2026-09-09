# Independent r=0 certificate-chain check

Status: FRESH NONAUTHOR FIRST CORRECT; C3 SECOND pending. Frozen main:
`9dcb6e9079ca57f94e0e30d63161cda89ca61fae`. This successor is separate
from archived PR55 and preserves its INCOMPLETE first review.

The independent verifier reconstructs `Rstar -> det -> P -> Q` from the
displayed four-dimensional formula, then verifies the domain and inertia
argument on `|mu|,|nu|<1, 0<u<1, r=0`. Existing coefficient tables are only
downstream comparison targets. The guarded author run passed every layer
in 9.707 seconds; both independent determinant methods, both Q transforms,
and every position of the complete coefficient box agree.

Start with [author_proof.md](author_proof.md),
[RESULT.json](outputs/author01/RESULT.json), and the
[execution ledger](execution/LEDGER.md). Full exact expressions, polynomial
division records, and coefficient tables accompany the summary result.
Source binding is in [inputs/SOURCE_BINDING.json](inputs/SOURCE_BINDING.json).

To reproduce with Python 3.12 and SymPy 1.14.0, from the repository root:

```sh
python research/C2/r0_independent52/implementation/verify_r0_chain_independent.py \
  --source-root research/C2/r0_independent52/inputs/source \
  --out <new-output-directory> --wall-seconds 2700
```

For the authorized resource/deadline wrapper, see `execution/run_guard.sh`.
Set `C2_ABSOLUTE_DEADLINE_EPOCH` to an existing shared deadline when appropriate;
the verifier uses the earlier deadline. The wrapper also enforces the hard
wall limit, address-space limit and single CPU/thread allocation.

The fresh nonauthor FIRST accepted the frozen author candidate; see
[review_first/REVIEW.md](review_first/REVIEW.md) and the
[current hand-off](FINAL_HANDOFF.md). C3 reserves
unseen SECOND and integration. No full-r conclusion, entropy counterexample,
novelty or proof-assistant certification is claimed.