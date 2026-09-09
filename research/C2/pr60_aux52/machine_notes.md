# PR60 auxiliary fixed-radial certificate: machine notes

Status: **MACHINE_PASS** for the scoped auxiliary certificate in
`outputs/run01/certificate.json`.

This note records only the finite machine-evidence unit for the PR60
continuation fixed-diagonal radial obstruction and the accompanying true
curvature/Jensen checks. It is not an entropy counterexample, not a refutation
of the Lambda-zero M theorem, not a general Lambda-nonzero theorem, and not a
novelty or theorem-review verdict. C1's analytical Claim4 FIRST remains a
separate gate.

## Source and run binding

- Frozen PR60 input commit: `f869fd251c0d6fdad737b6d5efa287307795a87d`.
- Frozen public source packet: `ee8f0a105798494474b1afd41f69af96794c8f5f`.
- Local source packet: `8078ff901b5262cba16e22f26046e486d2ae679a`.
- Public request/comment binding: request `5604536353`, claim `5604627611`.
- Run: `outputs/run01/`, started `2026-09-09T15:59:05Z`, finished
  `2026-09-09T15:59:06Z`, deadline `2026-09-09T16:09:05Z`.
- Process record: arithmetic PID `174471`; timeout PID `174469`; wrapper PID
  `174455` per root handoff; PID absent check at `2026-09-09T15:59:56Z`.
- Exit: `exit_code=0`; certificate elapsed `0.57009441s`; failed runs `0`.
- Resource intent: one process, one CPU/thread, 16 GiB, no GPU, 600 second
  wall-clock deadline. `cpu_affinity.txt` records CPU affinity `0`.
- Artifacts: all 12 JSON files in `outputs/run01/` parse as valid JSON;
  `stderr.log` is empty and `stdout.log` reports `MACHINE_PASS`.

## Independent construction covered

The runner reconstructs the eight complete-event signed determinant
polynomials for `K* + epsilon D* + delta C*` from the literal rational matrices
in the request. It cross-checks them against principal-minor
inclusion-exclusion and derives the exact jets
`p, pD, pDD, pC, pDC, pDDC` from the matched polynomials. The author reference
checker `continuation_exact_reference.py` is recorded only as forbidden input
metadata and was not imported or executed.

The exact base event law in mask order `(0,1,2,12,3,13,23,123)` is

```text
(1069,61006,106,319,11068306,1307119,55519,6556)/12500000.
```

The conditional-odds check gives

```text
exp(Lambda)=65729622186464/3466472577089 > 1.
```

The exact radial legality bound is

```text
|s|^2 < 442775/434223,
```

and the checker confirms that it contains `[999/1000,1001/1000]`. Rational
Sylvester/all-principal-minor checks are strict for `K*`, `I-K*`, the two
radial endpoints, `K* - hD*`, `K*`, `K* + hD*`, and all three complements, with
`h=1/100000`.

## Log and interval method

All logarithms use exact rational range reduction and the positive atanh series
with `N=80` terms. For positive rational `x`, the checker writes
`x=2^k y` with `1 <= y < 2`, encloses `log y` by

```text
0 <= log(y) - 2*sum_{j=0}^{N-1} w^(2j+1)/(2j+1)
     <= 2*w^(2N+1)/((2N+1)*(1-w^2)),  w=(y-1)/(y+1),
```

uses the same formula for `log 2`, and reverses interval endpoints when a
negative `k` scales the `log 2` interval. Decimal displays are rounded outward
to 35 places. Exact rational endpoints and widths are retained in
`certificate.json` under `radial_derivative.interval`,
`true_negative_entropy_curvature.interval`, and
`complete_configuration_jensen_gap.jensen_interval`.

## Certified signs

For the fixed-diagonal radial derivative, the checker retains every term

```text
sum[2 pD pDC/p - pD^2 pC/p^2 + pDDC log(p) + pDD pC/p].
```

It also verifies the exact rational term

```text
R =
62198092976944951510582016487593946984085346423771060505
/1445745402739430543847620534728498621094597199216967098368
```

and the log-cube coefficient identity
`pDDC = (-66/3125)*[-1,+1,+1,-1,+1,-1,-1,+1]` in mask order. The resulting
outward interval is contained in displayed equation (33):

```text
[-0.01912227459137764707182987490765265,
 -0.01912227459137764707182987490765264] < 0.
```

For the true complete-event negative entropy curvature, the checker evaluates

```text
sum[pD^2/p + pDD log(p)]
```

and obtains an outward interval contained in displayed equation (35):

```text
[0.09085487822146532947682573934164664,
 0.09085487822146532947682573934164665] > 0.
```

For the complete-configuration Jensen gap
`(H(K*-hD*)+H(K*+hD*))/2-H(K*)`, the checker derives all three event laws from
the exact polynomials and independently rechecks them by direct determinant
probabilities. The outward interval is contained in displayed equation (36):

```text
[-0.00000000000454275478584750276044882,
 -0.00000000000454275478584750276044881] < 0.
```

## Machine verdict scope

The machine packet independently certifies the stated auxiliary radial-method
failure while simultaneously certifying favorable true curvature and negative
Jensen sign for the same three kernels. The exact outputs keep all eight event
polynomials, all six jets per event, exact rational interval endpoints and
widths, all legality minors, and per-event Fisher/log/mixed contributions.
This PASS is machine evidence for C1/C3 review workflow only; it does not by
itself upgrade PR60's continuation claims to independent analytical FIRST or
SECOND status.
