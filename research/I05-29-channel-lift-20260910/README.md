# I05-29 successor: original hard fixture's maximal chord and exact channel families

Author status: **PROVED (author proof / author rational certificate), PENDING_REVIEW** for the scoped claims below. General rank-two concavity remains **INCOMPLETE**; novelty **NOT_ASSESSED**. This branch starts from main c6618e37640c5d019d9bbdc6fbffdc7fe31241f1 and succeeds PR80 / issue93 without modifying their frozen sources.

## Results and dependencies

`WHOLE_CHORD.md` proves, for the original PR58 s=.9 dense correlated 3+3 fixture, `H''(t)<=-t^2/5` throughout its maximal strict legal interval and concavity of `H(t)+t^4/60` on the closed interval. It also proves the same conclusion for a nonempty relative-open neighborhood centered at that fixture, on each member's own moving maximal legal interval. The neighborhood radius is not quantified. This proof is based on a single whole-interval signed full-curvature bound plus an explicit singular-endpoint inequality, not a time grid or an additive-projection criterion.

`CHANNEL_LIFT.md` proves an exact entropy identity for arbitrary finite local binary-input channels: an affine diagonal correction plus a fixed nonnegative mixture of truly K-affine DPP entropies. The actual observed-mode expansion law is proved by complete-event determinants. Applying the accepted main m-by-2 theorem then gives higher-dimensional, internally correlated, dense rank-two structural families on their entire maximal chords, with no small-perturbation condition. The accepted m-by-2 theorem itself is not a new result here.

`MODE_FAMILY.md` gives explicit 3+3 rational matrices, an exact maximal endpoint, a quantitative whole-chord curvature bound, and a strictly negative complete conditional-KL fiber within that same family. It also proves the original PR58 fixture is outside the grouped representation, explaining why its separate direct proof is necessary.

All entropy means complete-configuration Shannon entropy, natural logarithms, 0log0=0, in the actual observed coordinates. There is no L-affine replacement, spectrum-based entropy replacement, or quantum von Neumann entropy argument. Zero and rare events are handled in the full-law identities, including the endpoint Fisher divergence and every acceleration term.

## Reproduction

Use Python with SymPy. Recorded executions used Python3.13.5, SymPy1.14.0, one numerical thread. From this directory run:

```
python code/verify_whole_chord.py
python code/verify_channels.py
```

The scripts import only `code/exact_core.py`, `code/fixtures.py`, the Python standard library and SymPy. They use an existing `output` directory and write new JSON evidence there. They do not launch background or remote work, install dependencies or access credentials. Assertions must be enabled; do not use Python's `-O` option.

The full generated whole-chord JSON contains all 64 exact event coefficients, extrema and signed lower contributions. The repository includes `output/whole_chord_compact_evidence.json`, a labeled compact projection retaining the global bounds, endpoint data and every event's exact signed lower contribution. The companion artifact contains the full literal generated JSON; running the committed script reconstructs it, including all coefficients and extrema. The compact projection is storage only, not a new computation. Final stdout/stderr and exit records are literal saved process outputs; the channel development concatenation is labeled separately. See `FAILURE_LEDGER.md` for all known stops, corrections, non-applicability and exact remaining scope.

Every logarithm sign is enclosed by rational atanh series with an explicit tail, outward mantissa rounding and outward dyadic endpoints. All quadratic extrema and determinant/Mobius identities are exact. Decimal displays for interval budgets enclose the conservative computed budget, not the unknown actual curvature range. Float arithmetic is used only for elapsed-time metadata.

## Review boundaries

The original PR58 source is `research/I05-23-middle-20260909/ADDENDUM_JOINT_ADDITIVE.md` at 89aa874c24dd5a3ea98f8474826392560b1d0397. The accepted m-by-2 source scope is `research/C1-verification-20260909/children/w1/W1_ROUND2_INDEPENDENT_REVIEW.md` on the starting main. C1/C2/C3 reviews of earlier packets are not claimed to cover this one. All new proofs and arithmetic here are author-owned until separately reviewed; requests are not running jobs without actual issue claims. No general conjecture, novelty, formal verification, or independent source binding is claimed by the PASS text in author output.
