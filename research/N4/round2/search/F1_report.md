# F1 result: INCOMPLETE, numerical non-hit with layer diagnosis

All 72 prescribed rational centers on six fixed rational 4x3 frames completed.
There are 72 full six-dimensional Hessians, 216 rational finite chords, and no
positive numerical candidate. This does not establish face concavity.

Layer convention: the reported contribution is
`C_k=-sum_{|S|=k}[(p'_S)^2/p_S+p''_S log p_S]`. Its sum is the full entropy
curvature because total mass acceleration vanishes. The literal entropy of
one layer instead has second derivative `C_k-P_k''`; the diagnostic now
reports both and must not conflate them. Every layer sign below concerns C_k.

The largest Frobenius-normalized Hessian eigenvalue is -0.0179060465701,
at index 48, A=(2/5)I and z=(-4,-4,-16,1)/17. Its rounded rational top
direction has Fisher contribution -0.0112872787316 and acceleration
-0.00661876786726. Both are small and negative. Its three gaps are
-2.67251496e-6, -6.33330695e-4, and -0.0400165829. Across frames, the weak
isotropic curvatures occur with small coordinates of z; no positive balance
is hidden behind the weak value. Frame 0 (balanced z) instead has its best
value -0.0896713092 in a one-zero spectrum. Thus geometry influences weakness,
but this six-frame sample is not evidence of a single governing scalar.

The largest positive acceleration along a *top-Hessian* direction is at
index 53, frame 4 with spectrum (1/10000,1/1000,3/4): acceleration
+0.104962731685 versus Fisher contribution -5.38847096894. The top-cardinality
layer contributes only +0.000239691773 net, so it is not the main positive
contribution there. Its center and full matrices are frozen in
`F1/highest_top_acceleration.json`.

Each of the 72 acceleration matrices has a positive eigenvalue. The maximum
is +16.8605599869 at index 57; that eigenvector incurs Fisher -2204.52213120
and total curvature -2187.66157121. This direction's triple layer is already
negative (-25.44356276), while cardinalities 0 and 2 contribute about
-464.17 and -1694.98. Large acceleration alone supplies no useful candidate.

Among the actual 72 top-Hessian directions, 54 have negative total
acceleration, 19 have positive triple-layer acceleration, and 13 have
positive *net* triple-layer curvature. The lower layers are essential to
the total-negative result in those 13 cases. The search used the direct
event determinant and did not assume the principal investigator's new
coarsened-layer identities.

## Scope and actual execution

- 6 rational frames, 12 exact spectra/rotations per frame, seed 202609090427.
- 66 noncommuting top directions; 6 isotropic controls commute necessarily.
- Every chord keeps U fixed and is A-affine. Every endpoint passed exact
  rational Sylvester tests for A and I-A; V entries have denominator 10^9
  before reduction and t values denominator 10^12 before reduction.
- 1080 proper event jet evaluations; 504 entropy calls and 7560 proper-event
  determinants; 864 exact positive-definiteness checks. Full event and its
  derivatives were structural zero throughout and never entered Fisher.
- 60-digit mpmath direct determinant/inverse jets. One first-center mixed
  direction was checked against 16 exact Fraction Leibniz jets, including
  exact zero full-event jet. This selfcheck is not independent review.
- F1 PID 161087, exit 0, elapsed 5.626 seconds, one thread each for
  OMP/OpenBLAS/MKL/NumExpr, no GPU. Dependencies and source SHA256 are in
  `F1/manifest.json`. No active F1 job remains.
- 0 failed center attempts. The closest finite gap numerically is
  -1.9790848722e-11 at index 38, tiny because its step is about 6.93e-6;
  this is not a curvature improvement or sign ambiguity at 60 digits.

Reproduce from this directory on the existing route environment:

```text
python face_search.py --out F1_replay
python diagnose_F1.py
```

The diagnostic script reads existing F1 records and adds no centers. Keep the
original F1 directory: the run intentionally refuses to overwrite an output
directory. The full six Hessians, all event jets, rational U/A/V/t, feasibility
flags and cardinality decomposition are in `F1/cases.jsonl`.

## Checkpoint

F1 is complete; no further four-point scan is running or authorized by this
result alone. The remaining obligation is a full-face proof or positive
finite rational chord. A separately frozen five-point work unit may be
started only after the proposed support-entropy mechanism is confirmed;
F1 does not itself license dimension expansion.
