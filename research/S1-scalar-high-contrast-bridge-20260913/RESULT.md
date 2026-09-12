# Continuation result and execution boundary

## Status

PROVED AS AUTHOR MATHEMATICS / PENDING INDEPENDENT REVIEW: centered complete-configuration Fisher density 4/(1-c^2), explicit finite-size/count-score bounds, and a continuum high-contrast sparse-density true-rate Jensen wedge.

INCOMPLETE: high-contrast universal entropy-rate concavity, a genuine entropy-rate counterexample, and a volume-uniform acceleration bound. Novelty is NOT ASSESSED. No independent review or merge is claimed.

## Fresh computation (separate from the previous archive)

One production and one deterministic replay completed. Each reconstructs 9 fixed n=8 Toeplitz inputs, all 2,304 terminal complete atoms (plus the prefix trees), 24 independent exact determinant-jet comparisons on one rational three-site projection, 8 sparse-wedge rational witnesses, and 6 analytic crossover inequalities. The replay rejects 3 deliberately corrupted output dictionaries. All 9 selected finite curvature upper bounds are negative. Invalid probability cases: 0. Failed certified comparisons: 0.

The 9 inputs are the Cartesian product of three frozen shapes (half-band, four-band, thin band) and c in {501/1000,99/100,9999/10000}. They were selected to test the new bounds, not to claim a comprehensive adversarial screen. Replays are not counted as new independent search inputs. The previous 2,828 screens and 50 certificates are not added to this denominator.

Production wall time reported by the checker: 6.402367680 seconds. Replay: 6.201598122 seconds. No asynchronous job, remote server, GPU, or GitHub Actions run was used. The direct checker uses standard-library arithmetic and no BLAS. Commands additionally set OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1.

## Reproduce

    python code/verify_continuation.py --verify certificate/continuation.json

Fresh production to a separate path:

    python code/verify_continuation.py --write /tmp/scalar-continuation.json

The certificate stores exact rational outward endpoints. Decimal displays in narrative summaries are not used to decide signs. Source SHA-256 values are recomputed by the entrypoint; any source alteration changes the literal result and requires a new evidence version.

## Important finite-size observation

For the fixed four-band set at c=9999/10000, n=8 gives F_n/n in (7.714422218917,7.714422218919), whereas the PROVED limit is 20001.0000500025.... Its acceleration term A_n/n is approximately 3.160933322911. Neither number is an entropy-rate curvature. The analytic sufficient scale for F_n/n to exceed half its limit is n>=2,097,152 under the coarse J=4 bound; no full configuration enumeration at that scale is claimed.

## Publication scope and trust boundary

This continuation imports the two small arithmetic/complete-event source files from the preceding local package and adds a new checker and new literal output. It does not import or re-label the entire old 125-file archive. Its hash-only provenance record remains explicitly non-evidentiary for absent old outputs.

Production and replay share the arithmetic core; the exact three-site determinant/jet check is an alternative algebraic expression, not an independent researcher. There were no failed fresh production/replay attempts for this continuation before the recorded successful runs. Historical failures remain in their original archive and are not erased or re-counted here.

The branch only adds/updates its own research directory. S4 PR145, main, accepted proofs, reviews, branch protection and workflow settings are not modified.
