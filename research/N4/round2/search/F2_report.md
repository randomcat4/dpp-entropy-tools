# F2: INCOMPLETE; failed top-only budget is real, lower layers compensate

Search checkpoint status: **STOPPED_SUBSTANTIVE** after the two distinct
bounded units F1 and F2. No new numerical job is authorized by this report.

The frozen 24-center five-point unit completed with no positive numerical
curvature and no positive finite chord. All 48 selected rational directions
are noncommuting; every one of the 144 rational A-affine chords is exactly
feasible. These are finite numerical diagnostics, not a concavity theorem.

The proposed new mechanism actually occurs: **10 of 48 directions have
`H(q)*d'' > (d')^2/d`**. This includes 4 directions on the independently
certified baseline frame, 2 on variant 1 and 4 on variant 2. Therefore the
failure of the top-only Fisher budget is not just a loose entropy upper
bound or an untested possibility. Nonetheless, the full curvature remains
negative in every recorded direction and in the entire six-dimensional
Hessian at every sampled center.

## Layer convention and the compensation example

The execution records split the exact full-entropy identity as

`C_k = -sum_{|S|=k}[(p'_S)^2/p_S + p''_S log(p_S)]`, with `H''=sum C_k`.

For `d=det(A)` and `c=H(q)`, the top contribution in this convention is
`C_3 = c*d'' - d''log(d) - (d')^2/d`. This is what `top_layer.total` records.
The **literal** entropy of the top layer has second derivative
`H_top''=C_3-d''`; more generally `H_k''=C_k-P_k''`. The extra terms cancel
only when all layers are summed. `mechanism_diagnostic.json` reports both
conventions explicitly, with `mass_second` and `literal_layer_entropy_second`.

The strongest recorded geometry/Fisher ratio is index 23, variant 2,
spectrum (49/100,1/2,51/100), acceleration-top direction:

| Quantity | Numerical value |
|---|---:|
| c*d'' | +1.94210259517 |
| Top Fisher cost | 1.48555467282 |
| Geometry / top Fisher | 1.30732488727 |
| -d''log(d) | +2.05113946625 |
| C_3 | +2.50768738860 |
| C_0 | +0.56463297322 |
| C_1 | -3.02581018899 |
| C_2 | -3.62862948161 |
| Full H'' | -3.58211930878 |

Here the literal top entropy second derivative is +1.52148755259 and the
literal lower-layer sum is -5.10360686137. Thus compensation persists under
either correctly applied convention; it is not an artifact of assigning
the canceled linear terms. The noncommutator norm is 0.00105773231914.

The independently certified baseline frame has the same phenomenon at
index 7, clustered spectrum, acceleration-top direction: geometry
+1.87210023933 exceeds top Fisher 1.48406688171 (ratio 1.26146621989),
`C_3=+2.43715982732` while the lower sum is -6.02509367981 and total
curvature -3.58793385250. Its noncommutator norm is 0.000881127930172.

Across all 48 directions, geometry is nonpositive in 17, positive but within
the top Fisher budget in 21, and exceeds that budget in 10. There are 25
positive C_3 values and 22 positive literal H_top'' values. Total acceleration
is positive in 30 directions. Neither positive top-layer entropy curvature
nor positive full acceleration is enough to produce positive full curvature.

## The weak total curvature is a different regime

The largest full Hessian eigenvalue is -0.342586745734 at index 15, variant 1,
clustered spectrum. The rounded rational top direction gives
-0.342586745984, with total acceleration -0.098621963479 and Fisher
-0.243964782505. In this direction `C_3=-1.88194038366` stabilizes a positive
lower sum +1.53935363768. A universal attempt to assign one sign to every
cardinality layer would therefore miss both compensation directions.

Maximum Hessian eigenvalues by frame are -0.394341933918, -0.342586745734,
and -0.378425812531. The variant projection entropies are numerical values
1.71588404168 and 1.96927896787; their exact rational q weights and exact
positive support/sum checks are stored, but the baseline's strict entropy
interval is not claimed for either variant.

## Execution and provenance

- Existing frozen v2, three declared rational frames, eight nonisotropic
  spectra each, seed 202609090529. The independent baseline gate was read
  from `review/n5_projection_q_certificate.md` before execution.
- 24 attempted/completed centers, 24 full six-dimensional Hessians,
  624 supported-event jets, 48 rational directions and 144 rational chords.
- 312 entropy evaluations / 8112 supported-event determinants;
  576 exact endpoint Sylvester checks; 3 exact frame checks and 48 exact
  rational determinant jets for d,d',d''.
- All 26 support events are directly computed. Six size-four/five events
  and their jets are structural zeros, excluded before Fisher arithmetic.
- The decomposition was checked against the direct 26-event derivatives at
  60 digits. Logarithms are numerical, not interval-certified. This is
  an execution selfcheck, not non-author verification of a counterexample.
- PID 161588, exit 0, 6.512 seconds, OMP/OpenBLAS/MKL/NumExpr all one thread,
  no GPU. The process was subsequently confirmed absent. Source and helper
  SHA256, versions, arguments and actual counters are in `F2/manifest.json`.
- No failed center, no positive candidate file. The least-negative tested
  gap is -3.91138115795e-10 (index 9, Hessian-top, t=5798387/500000000000);
  it is a short-step quantity, not a small curvature margin.

The rational centers, directions, steps, full Hessians, all event jets and
both directional decompositions are in `F2/cases.jsonl`. Diagnostic scripts
read the saved records only and do not add evaluations. Reproduce a fresh
run without overwriting the original:

```text
python face5_search.py --out F2_replay
python diagnose_F2.py
```

For direct review, `F2/selected_mechanism_cases.json` separately freezes the
exact rational U,A,V and all three rational t values for index 23
(strongest geometry/Fisher ratio) and index 15 (highest total curvature).
It includes each C_k, mass second derivative P_k'', literal H_k'', exact
d,d',d'' and both Fisher/acceleration totals. The source record and selected
direction are identified; this extraction adds no kernel evaluations.

## Remaining obligation and stopping point

The top-only Fisher budget fails on actual noncommuting directions. That
failure is absorbed by lower layers in the tested positive-geometry regime;
conversely, a negative top contribution can absorb positive lower layers.
The unresolved issue is a coupled bound that controls these competing
terms for all admissible A,V,U, or a positive fixed rational chord. Merely
restating that coupled sum as an inequality would be equivalent to the
original face target and would not supply a new proved lemma.

In the recorded convention the remaining exact inequality is
`C_0+C_1+C_2 <= (d')^2/d + (log(d)-H(q))*d''` for every admissible fixed
frame and direction. This is an explicit **equivalent unresolved obligation**,
not a claimed reduction to a strictly weaker lemma. The data show why neither
a top-only budget nor unconditional negative lower-layer signs can close it.

F1 and F2 now provide two distinct bounded units and explicit opposing
compensation patterns. No new batch, dimension, restart or job is running.
This search task is stopped pending a concrete new mathematical unit from
the principal investigator. No issue or PR was opened by this child.
