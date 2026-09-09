# RESULT

Status: PARTIAL.

No B0 counterexample was found. The child result is a certified new
near-boundary beta-zero family, not a proof of the global implication.

## Main certified object

For the rational sparse-edge endpoint variant

    K(epsilon,q)=epsilon I+(7/10) u(q)u(q)^T,
    u(q)=(3/5,4/5,q sqrt(epsilon)),

with epsilon=10^-8, the server interval certificate proves that beta has an
exact zero for q in

    [4418854248579277079/2305843009213693952,
     8837708497158554159/4611686018427387904].

Equivalently, kappa=q^2 lies in the exact interval recorded in
`outputs/sparse_rational_certificate.json`.  Every point in the certified q
bracket is strict, connected, has positive event probabilities, has positive
leading minors for N, and satisfies

    0.925605324011963372275912789435720081
      < det(N) alpha
      < 0.925806704946127239064572716414179284 < 1.

Thus this exact beta-zero point is not a B0 counterexample.  It is useful
because it gives a new sparse-edge root tube close to the suspected boundary
`det(N) alpha=1`.

This is a finite-epsilon certificate only for the displayed rational kernel.
It should not be conflated with the unit-normalized finite-epsilon variant
`u_1^2=2/5,u_2^2=3/5,u_3^2=kappa epsilon`.  The leading sparse mechanism uses
the same kappa=q^2 limit, but a separate mapping/uniform remainder proof is
needed before transferring the finite-epsilon certificate.

## High-precision trend

The same rational family gives the following beta-zero scouts:

| epsilon | q at beta root | kappa=q^2 | det(N) alpha |
|---:|---:|---:|---:|
| 10^-6 | 2.03852336981346 | 4.15557752927563 | 0.902313673401247 |
| 10^-8 | 1.91637255048258 | 3.67248375224311 | 0.925706012741381 |
| 10^-12 | 1.79680854193789 | 3.22852093638097 | 0.949767086159469 |

The asymptotic cue supplied to this child predicts

    kappa_* = (3/7)(exp(40/21)-1) = 2.450489125337259...

and `det(N)alpha = 1 - 1/(lambda log(1/epsilon)) + O(log(1/epsilon)^-2)`.
The table is consistent with an approach to the boundary from below, but it is
not a uniform asymptotic proof.

## Calibration and fixed-ratio probe

The old `epsilon=10^-2,u=(1,2,3)/sqrt(14)` root was reproduced as a
high-precision calibration.  The bounded fixed-ratio table for
epsilon=10^-2,10^-3,10^-4,10^-5 found two beta sign-change roots per epsilon.
For the left root, `t/epsilon` is

    0.226189936752769, 13.1823655622027, 142.490271811763, 1435.54444106261.

This separates the observed roots from any finite `t=epsilon*s` tube.  The
corresponding `det(N)alpha` values stay near 0.645-0.662, far below 1.

## Scope

The result does not prove B0 globally, does not classify all beta-zero
components, does not certify uniqueness of the displayed root, and has not
received independent nonauthor review or Lean verification.
