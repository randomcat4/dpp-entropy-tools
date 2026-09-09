# FINAL RESULT — fixed two-harmonic nonzero-parameter unit

Date: 2026-09-10. Base: `main@9dcb6e9079ca57f94e0e30d63161cda89ca61fae`.

All new statements are **PROVED (AUTHOR PROOF), NOT INDEPENDENTLY REVIEWED** unless explicitly marked incomplete. No result inherits acceptance from PR59.

## A. Fixed object and legality

For

```text
f_t(theta)=1/2+(1/4)cos(4*pi*theta)+(t/8)cos(2*pi*theta),
```

the whole interval `[-3/2,3/2]` is strict:

```text
119/512<=f_t(theta)<=15/16,
min{f_t(theta),1-f_t(theta)}>=1/16.
```

The amplitude `1/4` is unchanged.

## B. True-rate results at fixed nonzero parameters

For complete-configuration Shannon entropy rate per original lattice coordinate,

```text
h(f_1)-[h(f_{1/2})+h(f_{3/2})]/2>1/10000.            (B.1)
```

Moreover,

```text
h''(1/2)<-1/2500,
h''(1)  <-1/1000,
h''(3/2)<-1/500,                                      (B.2)
```

and the same bounds hold at the three negative parameters by the exact diagonal gauge.

These are true-rate statements. The finite quantity is the depth-18 conditional entropy `H_19-H_18`; configuration-uniform analytic tails enclose its value and second derivative relative to the infinite rate. No sequence `H_n/n` is fitted or differentiated.

## C. Full response and structural negative term

For the normalized complete-event conditional `G_t`, define

```text
phi=log G,
psi=partial_t phi,
xi=partial_t^2 phi,
R=(I-L)^(-1)Pi,
v=Rphi.
```

The full response is

```text
h''=-nu(psi^2)+nu((psi^2-xi)v)-2nu(psi R(psi v)).     (C.1)
```

The complete Fisher-information rate obeys the exact observable-projection bound

```text
nu_t(psi_t^2)>=t^2/[16384 V(t)]>=16/286141,           (C.2)
V(t)=561/2048-17t^2/4096-3t^4/65536,                 (C.3)
```

for `1/2<=|t|<=3/2`. Formula (C.2) quantifies a negative component of (C.1); it does not discard the acceleration or stationary-measure response.

## D. Reproducible certificates

At `t=1/2,1,3/2`, multiply every complete-event matrix by `32`. The exact entries are diagonal `+/-16`, first off-diagonal `1,2,3`, and second off-diagonal `4`.

The main programs enumerate all complete event values or jets by a fraction-free width-two determinant automaton. Independent exact checks use:

- inclusion-minor Mobius inversion through length six;
- direct Bareiss event determinants through length eight;
- exact polynomial interpolation of direct determinant jets through length six;
- independent Leibniz determinants for the pair/triple/four-site covariance polynomials.

Logarithms are evaluated with correctly rounded 100-digit `decimal` arithmetic, widened by `10^-90`, followed by directed floor/ceiling operations. All recorded author runs exit zero under CPython 3.13.5 with no third-party dependency.

## E. INCOMPLETE

The continuum statement

```text
h''(t)<0 for every 1/2<=|t|<=3/2                     (E.1)
```

is not proved. Six negative curvature points and the Jensen chord (B.1) do not logically imply (E.1). No positive true-rate counterexample is obtained.

Issue #74 freezes the remaining outward-rounded finite-memory/Riccati continuum certificate, including an explicit true-rate tail/resolvent gate. It is a requested computation, not evidence used here.

## F. Review and novelty boundary

`verification.md` and `verification_round2.md` are author audit contracts. The proof, code, and execution are not an independent review, CI result, novelty opinion, or publication-priority claim.