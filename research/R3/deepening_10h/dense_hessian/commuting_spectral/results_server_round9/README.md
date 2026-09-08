# Round 9 fixed-eigenvector spectral scout

AUTHOR STATUS: `HIGH_PRECISION_STABLE_NEGATIVE`, pending fresh non-author audit.

## Scope

Four isolated one-thread shards evaluated 5,000 twelve-dimensional centers
each, for a total of 20,000.  The orthogonal eigenbasis was frozen from the
previous verified round-6 point; each center changed only the eigenvalues and
optimized a strictly positive spectral-rate vector.  The four proposal modes
were a neighborhood of the frozen spectrum, two edge clusters, a broad logit
spread, and five spectral clusters.

This is a targeted float64 scout.  It is not a proof about all fixed-basis
directions.

## Complete scout ledger

- rows: `20000`
- float candidate statuses: `0`
- shard seeds: `2026090816` through `2026090819`
- centers per shard: `5000`
- dimension: `12`
- enforced spectral margin floor: `0.01`
- best positive-rate mechanism ratio:
  `rho=0.5464281988363302`
- best row: shard `3`, local index `1033`, mode `two_edge_clusters`
- float midpoint gap at the stored step:
  `-0.00024496617428049206`

The mechanism ratio is

\[
\rho=\frac{\text{event-acceleration term}}{\text{Fisher loss}}.
\]

Positive entropy curvature requires `rho>1`.  This round improves the stable
diagnostic record from about `0.5261` to about `0.5464`, but does not cross the
threshold.

## Frozen strongest-point gate

`recheck_best.py` interprets the symmetrized float entries as exact decimal
rationals and recomputes all 4,096 exact events by independent mixed-event
determinant elimination.

At 70 decimal digits it gives

```text
Fisher       = 71.5139357409703116120035912052615395654888436753676...
acceleration = 39.0772310986354385442031973729597914673985512029115...
H''          = -32.4367046423348730678003938323017480980902924724561...
rho          = 0.5464281988363298115096314979233096556129685380154...
```

Actual 70-digit midpoint gaps are negative at all three recorded scales:

```text
t=0.0038860925981574566  gap=-2.44966174283158023405286376875e-4
t=0.001                  gap=-1.62185329529431393194488771160e-5
t=0.0001                 gap=-1.62183541273822423039597174618e-7
```

The corresponding central second differences converge to the analytic
`H''` from the negative side.  Mixed-event and Möbius atom calculations agree
in float64 to maximum absolute error `1.91e-16`; the 70-digit normalization,
first-derivative and second-derivative residuals are at most about `2.1e-68`.

Exact rational LDL certificates prove that the frozen decimal-rationalized
direction is positive definite and that every point on

\[
|t|\le 1/200
\]

has both `K(t)` and `I-K(t)` strictly above the spectral margin `1/2000`.
Thus the negative result is not explained by an infeasible chord.

## Provenance and integrity

- search script SHA-256:
  `dd55e9f05afd128a4e64e06ab705ba031fb0f32f0ea4a44a0169b625b9050a37`
- source NPZ SHA-256:
  `e614dff920277e60929a6f8e1cfb37bd19d7c8d30a6a61a9488c424a8eb7ff3f`
- strongest NPZ SHA-256:
  `807ac23ae9b0c54c39d909ca543b72f69d95a9cc986cb7d4ff8295444d73cc01`

The copied local files matched the producing machine's hashes before the
temporary remote directory was removed.  Raw per-row ledgers, manifests and
logs are retained under `results_0/` through `results_3/` and beside them.

## Boundary

The high-precision gate certifies only the frozen strongest point and its
displayed feasible interval.  The other 19,999 rows remain float scout data.
Zero hits do not prove generic fixed-eigenvector PSD/NSD concavity.

