# Low-Denominator Noncommuting Face and BSC-Lift Certificate

Status: CONFIRMED_NEGATIVE_DIAGNOSTIC. This is a finite rational diagnostic
certificate, not a counterexample and not a theorem.

Executable artifact: `finite_noncommuting_bsc_cert.py`.

Run artifact: `finite_noncommuting_bsc_certificate.json`.

Run metadata: PID `33400`, exit status `0`, script SHA-256
`876fb9c4d9a7421da1dc9f0133c85863fbd1464f0d28095f5b43b7ba16fac54b`,
Python `3.12.14`.

## Fixture

Use the Householder frame with null vector
`z=(1/5,2/5,2/5,4/5)` and

```text
U =
[ 4/5  -2/5  -2/5 ]
[-2/5   1/5  -4/5 ]
[-2/5  -4/5   1/5 ]
[ 1/5   2/5   2/5 ].
```

The script checks exactly that `U^T U=I_3` and `U^T z=0`.

The latent matrices are

```text
A =
[ 2/5   1/20   1/30 ]
[ 1/20  1/3   -1/25 ]
[ 1/30 -1/25   1/2  ]

V =
[ 1/7    2/15  -1/18 ]
[ 2/15  -1/8    1/20 ]
[-1/18   1/20   1/10 ].
```

Here `[A,V] != 0`. The finite chord uses `t=1/20`, and the common BSC lift
uses `epsilon=1/100`.

## Exact Checks

Sylvester leading-minor checks prove `0<A-tV<I_3` and `0<A+tV<I_3`.

For the face event polynomials under `K(s)=U(A+sV)U^T`:

```text
p_[4](s) = 0
sum_proper p_S(0) = 1
sum_proper p'_S(0) = 0
sum_proper p''_S(0) = 0
```

All 15 proper events are positive at `s=0`, `s=-t`, and `s=t`; the full event
is deleted exactly.

With 48-term rational log intervals,

```text
Delta_face in [-8.6555894403771017e-05,
               -8.6555894403771017e-05]   printed precision
```

so the tested boundary chord is strictly negative.

For the common lift `K_j(e)=eI_4+(1-2e)K_j`, exact leading-minor checks prove
strict `0<K_j(e)<I_4` for `j=-1,0,+1`, and all 16 lifted events are positive.
With 48-term rational log intervals,

```text
Delta_lift in [-7.9835082773968232e-05,
               -7.9835082773968232e-05]   printed precision
```

so this lifted finite interior chord is also strictly negative. It is only a
sanity certificate for the common BSC lift path.
