# Exact-event reproduction and coverage

Use Python 3.12 with SymPy 1.14.0 in an isolated environment. The script uses
one CPU thread, no GPU. From the repository root:

```text
python research/A2/artifacts/moving_frame_check.py --mode smoke
python research/A2/artifacts/moving_frame_check.py --mode symbolic
python research/A2/artifacts/moving_frame_check.py --mode certify
```

The recorded files correspond to one smoke chord, six additional distinct
certificate chords, and 48 symbolic event functions (16 for each of the two
endpoints and midpoint). Every job completed with exit code zero. Per-job
records include PID, command, source SHA256, versions and elapsed time; no
random seed was used because the fixtures are deterministic. Two bounded
single-thread jobs overlapped, with a 4 GiB memory ceiling each. The smoke
preceded both. No historical search was rerun.

For every one of the seven rational chords the checker verifies:

- symmetry, positivity of all 15 nonempty principal minors of K and I-K,
  separately for both endpoints and their actual arithmetic midpoint;
- exact normalization and nonnegative full event probabilities;
- equality between inclusion-exclusion and the mixed-row determinant for
  all 16 events of all three kernels;
- a rational outward enclosure of Delta. All seven upper endpoints are
  strictly negative. This is finite-point evidence, not the family theorem.

The symbolic output records exact rational masses and Taylor polynomials
through t^3. Symbolic normalization is checked. The proof, rather than a
finite list of expansions, establishes the claimed uniform remainder.

## Strict logarithm enclosure

For any positive rational q, the implementation reduces q=2^k r with
1<=r<2. With z=(r-1)/(r+1), it uses

    log r = 2 sum_(j=0)^(N-1) z^(2j+1)/(2j+1) + tail,
    0<=tail<=2 z^(2N+1)/[(2N+1)(1-z^2)].

The same bound encloses log 2. All series arithmetic and tail inequalities
are rational; k<0 reverses the relevant bound when combining log 2.
N=96 and outward rounding to a denominator 2^256 yield rational log bounds.
Multiplication by -p reverses the interval for each positive event mass;
zero events contribute exactly zero. The endpoint-average lower bound uses
the midpoint entropy upper bound, and conversely for the upper bound.
Decimal display uses directed rounding at 48 digits after all sign decisions
have already been made on exact rationals. No floating sign is accepted.

This checker is not a Lean proof. The separately recorded Lean component
checks only the fixed integer matrix identities underlying noncommutation.

The [independent replay record](independent_audit_execution.md) retains a
failed local missing-dependency attempt and the subsequent seven-point
standard-library check. Its [recorded source](independent_rational_check.py)
is supplied without rerunning the completed job. The reviewer replay uses
Decimal entropy only as a cross-check; it does not replace the strict outward
enclosures above. Replay PIDs were not captured and are explicitly unavailable.

The [structure report](structure_validation.json) checks required artifacts
only. It passed with no errors and two exact-phrase freeze-marker warnings,
not mathematical failures. Its two CORRECT entries are two reports by one
reviewer, as explicitly stated in the main README and verdict.
