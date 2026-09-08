# D10-B3 verdict

STATUS: AUTHOR_IMPLEMENTED_NO_VERIFIED_POSITIVE_SIGNAL

This is an author-side implementation verdict, not an independent `CORRECT`
certificate.

POST-AUDIT NOTE: `verifications/fresh_audit.md` has since independently
reconstructed the recurrence, exact-event gate, frozen anomaly, exact LDL
certificate, and all 4608 corrected scout evaluations, with status `CORRECT`
for those scoped claims.

## What is established in this work unit

The missing second-order path jet evaluator has been implemented in
`jet_hessian.py`.

For a fixed-beta line \(\tau(t)=\tau_0+t\delta\), it computes

\[
H(0),\qquad H'(0),\qquad H''(0)
\]

by differentiating the selected-run path \(L\)-ensemble entropy DP.  The core
calculation is \(O(n^2)\) and does not use finite differences.

The implementation passed direct exact-event checks for n=5,6,7.  Those checks
compute atom derivatives by Möbius inversion from inclusion probabilities and
compare against the path jet:

- n=5 rank2: max absolute difference about `5.77e-15`;
- n=6 full-rank: max absolute difference about `1.78e-15`;
- n=7 full-rank: max absolute difference about `1.07e-15`.

Low-dimensional full \(\tau\)-Hessians were also constructed by polarization
for n=5 and n=6; both sampled Hessians had negative largest eigenvalue.  This
is only finite evidence.

## Scout result and correction

A first float scout over n=5..100, 24 trials per n, rank2 and full-rank
buckets, reported 13 positive high-dimensional \(H''\) signs.  The largest was
the first n=93/rank2 signal:

\[
H''_{\rm legacy}=184.7448188718266.
\]

Per the follow-up instruction, that case was frozen completely and replayed
with a separate high-precision Decimal jet plus actual symmetric chord entropy
differences.  This exposed a bug in the legacy final normalization: computing
\(T/Z\) as \(T\cdot Z^{-1}\) formed \(Z^{-3}\), and for this case
\(Z\approx1.34\times10^{118}\), so the reciprocal-cube term underflowed.

The implementation now uses a stable quotient recurrence for \(C=A/B\):

\[
C_0=A_0/B_0,\qquad
C_1=(A_1-B_1C_0)/B_0,
\]

\[
C_2=(A_2-2B_1C_1-B_2C_0)/B_0.
\]

After this fix, stable float and Decimal agree.  The positive sign is rejected:

\[
H''_{\rm stable\ float}=-0.007024918933640795,
\]

\[
H''_{\rm Decimal}
=-0.007024918933615582731289762931393827\ldots .
\]

The normalized Decimal curvature is

\[
H''/\|\dot K\|_F^2
=-11.554503628620022\ldots .
\]

For \(h=0.0005\), the Decimal value-only midpoint gap is

\[
-8.78114868789936\ldots\times10^{-10},
\]

and the recorded second differences converge to the same negative \(H''\).

Thus the n=93 positive signal is not a candidate.  It is a legacy float
underflow/cancellation artifact in the second derivative of the normalized
\(T/Z\) term.

The corrected same-scope stable-float scout over n=5..100 produced:

- total evaluations: 4608;
- positive normalized \(H''>10^{-10}\): 0;
- global max / closest-to-zero normalized \(H''\): n=34, rank2, trial 8,
  `-3.2491091342052325`.

## Feasibility of the frozen rejected signal

Even though the sign is rejected, the frozen center itself is strictly feasible.
Interpreting the saved decimal float strings as exact rational parameters,
exact tridiagonal LDL checks certify

\[
P-4I\succ0,\qquad 50I-P\succ0,\qquad P=S^{-1}.
\]

Therefore

\[
\frac1{50}I\preceq S=I-K\preceq\frac14I,
\]

so the strict DPP margin is at least \(1/50\).  The failure is not infeasibility.

## Why n<93 did not show a positive signal

No mathematical threshold at n=93 is supported.  The first scout used the
legacy float second-order accumulator and a random deterministic sample.  The
fact that no earlier n produced a reported positive sign only reflects that
this particular finite run did not hit an earlier legacy instability above
threshold.

After the stable quotient fix, the same deterministic n=5..100 run produced no
positive signal at any n.  This is still not a threshold theorem or a global
concavity theorem; it is only a finite corrected scout.

The abrupt legacy high-n jump is best explained by reciprocal-cube underflow in
the quotient jet: in the frozen n=93 case, Decimal arithmetic gives

\[
(\log Z)''\approx0.2082391792394403,\qquad
(T/Z)''\approx0.2152640981730559,
\]

whose difference is a small negative number.  The stable float path gives
\((T/Z)''\approx0.21526409817308104\).  The legacy inverse-jet path instead
computed \((T/Z)''\approx-184.5365796926\), creating a spurious large positive
\(H''\).

## Current research conclusion

No verified positive entropy-curvature or midpoint-gap candidate is produced by
D10-B3.

The reliable deliverable is the \(O(n^2)\) second-order jet algorithm, with the
stable quotient fix, and its n≤7 exact-event validation.  The corrected
`curvature_scout.json` contains no positive n≤100 signal.  Any future positive
float sign must still be replayed through the Decimal branch or a log-scaled /
interval-certified jet before being promoted to `FLOAT_CANDIDATE`.

## Remaining obligations

1. Independent non-author verification of `jet_hessian.py` and the derivation:
   completed in `verifications/fresh_audit.md`.
2. If high-dimensional sign search continues, use Decimal, compensated,
   log-scaled, or interval-certified arithmetic for sign promotion.
3. Do not infer global concavity or nonconcavity of the fixed-beta tau family
   from the finite n≤100 run.
