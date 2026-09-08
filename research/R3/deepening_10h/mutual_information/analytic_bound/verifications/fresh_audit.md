# D10-C2V fresh audit: fixed n=11 analytic bound

STATUS: CORRECT

This is a non-author strict verification of
`research/R3/deepening_10h/mutual_information/analytic_bound/`.  `CORRECT`
means the fixed eleven-dimensional continuous interval certificate was checked
from exact-event definitions and the strongest constants were independently
recomputed.  It does **not** prove the general rank-two PSD local conjecture,
does **not** certify an R3 positive gap, and does **not** extend beyond the
fixed center/direction and interval stated in `derivation.md`.

## Scope and audited files

- `derivation.md:1-2` states this is a fixed n=11 rank-two PSD ray certificate,
  not a general rank-two PSD theorem.
- `derivation.md:5-24` defines `M`, `D=uu^T+c vv^T`, strict feasibility,
  exact event probabilities, `H(t)`, and the R3 sign convention
  `Delta(t)=[H(t)+H(-t)]/2-H(0)`.
- `derivation.md:26-40` introduces the exact decomposition
  `Delta(t)=G(t)-K(t)-J(t)`, where `K(t)` in that local paragraph is KL cost,
  not the DPP kernel.
- `derivation.md:43-72` derives the `L2/L4` expansion and identifies
  `L2=B+F/2`,
  `L4=sum[b^2/(2p)-a^2b/(2p^2)+a^4/(12p^3)]`.
- `derivation.md:75-88` correctly says the general rank-two PSD sign is not
  closed and then freezes a fixed n=11 family.
- `derivation.md:90-127` gives the exact fixed `M`, `u`, `v`, `D`, rank-two
  PSD/non-thinning/block nondegeneracy claims, and the frozen conclusion
  `Delta(t)<=-t^2/2` for `|t|<=1/32`.
- `derivation.md:130-150` states exact LDL spectral margins and structural
  nondegeneracy away from decoupling/repeated-row boundaries.
- `derivation.md:152-178` states the 2048 exact coefficient certificate,
  exact small-n Möbius gate, atanh log interval method, rounding grid, and
  certified `L2/L4` intervals.
- `derivation.md:180-203` states the `H''''` formula, the uniform `<941` bound,
  and the Taylor step to `Delta(t)<=-t^2/2`.
- `sanity_certificate.py:47-54` builds the frozen `M,D`.
- `sanity_certificate.py:56-63` computes exact-event probabilities by the
  signed determinant formula, not principal minors.
- `sanity_certificate.py:67-75` gives exact rational LDL pivots for
  `M-1/10 I` and `I-M-1/10 I`.
- `sanity_certificate.py:77-92` implements the atanh log interval and
  floor/ceil grid rounding directions.
- `sanity_certificate.py:94-105` provides an n=4 direct Möbius gate.
- `sanity_certificate.py:111-138` constructs 2048 exact coefficients, checks
  normalization, accumulates `B`, `Fisher`, `L2`, `L4`, max relative
  coefficients, and the uniform fourth-derivative bound.
- `sanity_certificate.py:151-155` writes the frozen certificate and coefficient
  ledger.
- `extend_radius.py:7-18` checks `L2>11/20`, `H4<941`, `maxA<4`, `maxB<3`,
  the `1/32` radius inequalities, spectral margin, cross-block lower bound, and
  diagonal separation.
- `extend_radius.py:19-37` reuses the frozen 2048 coefficients for endpoint
  Decimal sanity checks and writes `radius_1_over_32.json`.
- `results/certificate.json:31-45` records `uu=58`, `vv=60`, `uv=-17`,
  rank `2`, trace `3/2`, base margin `1/10`, 2048 events, `sum p=1`,
  `sum a=sum b=0`, and positive minimum center atom.
- `results/certificate.json:56-75` records the certified `L2`, `L4`,
  `H''''`, `maxA`, and `maxB` bounds.
- `results/certificate.json:81-100` records the n=4 Möbius gate at
  `t=-1/100,0,1/100`.
- `results/radius_1_over_32.json:3-13` records radius `1/32`, uniform gap bound
  `Delta(t) <= -t^2/2`, equality case `t=0`, spectral margin `17/320`,
  cross-block lower bound `13/64`, diagonal lower bound `893/41760`, and
  remainder cost `<1/20`.

The author scripts refuse to overwrite existing frozen outputs
(`sanity_certificate.py:107-108`, `extend_radius.py:4-5`), so I did not rerun
them in place.  Instead I used a separate independent verifier in this
verification directory.

## Independent derivation checks

For a fixed strict kernel line `K(t)=M+tD`, exact events are

```text
p_S(t)=(-1)^|S^c| det(K(t)-I_{S^c}).
```

Because `D` has rank `2`, every event determinant is a polynomial of degree at
most `2`.  Writing

```text
p_S(t)=p_S+t a_S+t^2 b_S
```

is therefore legitimate as an algebraic identity; the interpolation nodes
`t=-1,0,1` need not be feasible kernels and are not used as probability laws.
Normalization gives

```text
sum_S p_S=1,  sum_S a_S=0,  sum_S b_S=0.
```

The entropy Taylor coefficient is

```text
H''(0)=-2 sum b_S log p_S - sum a_S^2/p_S = -2L2,
L2 = B + F/2,
B=sum b_S log p_S,
F=sum a_S^2/p_S.
```

Thus

```text
Delta(t) = -L2 t^2 + O(t^4).
```

The fourth derivative formula in `derivation.md:184-185` is correct.  For
`r(t)=p+ta+t^2b`, `r'=a+2tb`, `r''=2b`, and

```text
d^4[-r log r]/dt^4
= -12 b^2/r + 12 b(r')^2/r^2 - 2(r')^4/r^3
= -[12b^2/r - 12(r')^2b/r^2 + 2(r')^4/r^3].
```

If `A=|a|/p`, `B=|b|/p`, and `|t|A+t^2B<1/2`, then `r(t)>p/2`; also
`|r'(t)|<=p(A+2B)` for `|t|<=1`.  Hence the per-event bound used by the author,

```text
p[24B^2 + 48(A+2B)^2B + 16(A+2B)^4],
```

is a valid upper bound for `|d^4[-r log r]/dt^4|`.  Summing the exact rational
upper bounds gives `<941`.

Applying Taylor with Lagrange remainder to `H(t)` and `H(-t)` separately, the
odd terms cancel in the symmetric average:

```text
Delta(t) = -L2 t^2 + R(t),   |R(t)| <= 941 t^4/24.
```

Since `L2>11/20` and `941/(24*32^2)<1/20`,

```text
Delta(t) < -(11/20)t^2 + (1/20)t^2 = -t^2/2
```

for every `0<|t|<=1/32`; at `t=0`, `Delta(0)=0`.  Therefore the equality case
for `G=KL+JS` is exactly `t=0` on the certified interval, with the stated gap
sign convention.

## Independent code run

I added
`research/R3/deepening_10h/mutual_information/analytic_bound/verifications/fresh_bound_check.py`.
It does not import the author certificate scripts.

Key locations:

- Frozen constants and proof parameters: `fresh_bound_check.py:17-19`.
- Exact determinant/rank primitives: `fresh_bound_check.py:60-122`.
- Frozen `M,D` reconstruction: `fresh_bound_check.py:126-143`.
- Signed event determinant and direct Möbius exact-event oracle:
  `fresh_bound_check.py:147-177`.
- Exact LDL: `fresh_bound_check.py:181-192`.
- atanh log interval and floor/ceil grid rounding:
  `fresh_bound_check.py:196-235`.
- Frozen coefficient ledger read and validation:
  `fresh_bound_check.py:238-248`.
- Independent recomputation of `B`, `Fisher`, `L2`, `L4`, `H4`, `maxA`,
  `maxB`: `fresh_bound_check.py:251-289`.
- Main coefficient/Möbius/radius/Taylor predicates:
  `fresh_bound_check.py:301-430`.

Command:

```text
python.exe research/R3/deepening_10h/mutual_information/analytic_bound/verifications/fresh_bound_check.py
```

Final evidence-bearing run exit code: `0`.

Result:

```text
status: PASS
failed_predicate_indices: []
coefficient_rows: 2048
coefficients_match_recomputed_signed_event_determinants: true
degree_two_check_at_t_2: true
center_mobius_matches_signed_event_formula: true
sum_p: 1
sum_a: 0
sum_b: 0
endpoint sums at |t|=1/32: 1, 1
endpoint min atom at |t|=1/32:
3373333683736281300711239286101839/42015549311157481171727155200000000000
```

The independent recomputation exactly matched the frozen certificate:

```text
min center p:
57137776180548380116876667077/707427756451331512185600000000000

B interval:
[-4050637330674392213089/200000000000000000000000,
 -10126593326685980307541/500000000000000000000000]

Fisher interval:
[1152084393369664835283143/1000000000000000000000000,
 1152084393369664835285191/1000000000000000000000000]

L2 interval:
[69473626253932557072081/125000000000000000000000,
 555789010031460457027013/1000000000000000000000000]

L4 interval:
[156704027228230468633811/1000000000000000000000000,
 156704027228230468635859/1000000000000000000000000]

H4 upper:
7347940288246368337888531/7812500000000000000000
```

The simplified radius predicates also checked exactly:

```text
maxA < 4, maxB < 3
(1/32)*4 + (1/32)^2*3 = 131/1024 < 1/2
941/(24*32^2) = 941/24576 < 1/20
spectral margin = 1/10 - (1/32)*(3/2) = 17/320
L2_lower - 941/(24*32^2)
= 194062358253985171216243/375000000000000000000000 > 1/2
```

## Rank-two PSD and nondegeneracy

The independent run checked:

```text
||u||^2 = 58
||v||^2 = 60
u·v = -17
Gram determinant = 3191 > 0
rank(D) = 2
trace(D) = 3/2
```

It also checked the block conditions from `derivation.md:107-115`:

```text
block A Gram determinant = 527
block B Gram determinant = 1080
rank(D_A) = 2
rank(D_B) = 2
D_AB is nonzero
```

Exact LDL pivots matched the certificate:

```text
min LDL pivot of M - (1/10)I:
47/180

min LDL pivot of I - M - (1/10)I:
3336775110398426604566713849/36590680854950191324086990060
```

Thus `(1/10)I < M < (9/10)I`.  Since `D` is PSD and
`||D||op <= trace(D)=3/2`, the whole interval `|t|<=1/32` satisfies

```text
(17/320)I < M±tD < (303/320)I.
```

The structural nondegeneracy numbers also matched:

```text
center cross-block Frobenius norm squared = 81/1210 > 1/16
uniform cross-block lower bound = 13/64
uniform diagonal separation lower bound = 893/41760 > 1/50
```

## Log bounds and rounding direction

For every rational `p in (0,1]`, the proof writes `p=2^-k z`,
`1<=z<2`, and uses

```text
log z = 2 sum_{j=0}^{N-1} x^{2j+1}/(2j+1) + R_N,
x=(z-1)/(z+1),
0 <= R_N <= 2 x^(2N+1)/((2N+1)(1-x^2)).
```

The independent script recomputed this with `N=18` and grid `10^24`.
For `log p = log z - k log 2`, the lower endpoint uses the lower bound for
`log z` and the upper bound for `log 2`; the upper endpoint uses the upper
bound for `log z` and the lower bound for `log 2`.  It then floors lower
contributions and ceils upper contributions before summing.  This is the
correct outward rounding direction, including events with negative `b`.

## Boundary notes

No critical gap was found in the fixed n=11 continuous interval certificate.
The following limits remain essential:

1. The verified conclusion is only for the frozen center `M`, direction `D`,
   and `|t|<=1/32`.
2. The general rank-two PSD local inequality remains `INCOMPLETE`, exactly as
   `derivation.md:75-88` and `verdict.md` state.
3. Decimal values are sanity displays only; the proof-bearing quantities are
   rational coefficient, LDL, log-interval, and Taylor-remainder certificates.
4. Direct exact-event semantics were checked at full n=11 for the center by
   Möbius inversion in the independent verifier, while the author-supplied
   small n=4 gate remains a separate implementation sanity check.

Within this scope, D10-C2V is `STATUS: CORRECT`.
