# Proof and Certificate

Status: `CERTIFIED_NEGATIVE_PAIR_GAP` for `S1-R2-B1`.

## Fixed Three-Symbol Object

The symbol is

```text
f_t(x)=p+t dp+sum_{k=1}^3 ((a_k+t da_k) cos(2 pi k x)
                         +(b_k+t db_k) sin(2 pi k x)).
```

with

```text
p  = 9/20
a  = (9/50, -2/25, 1/25)
b  = (1/25, 3/100, -1/50)
dp = 1/50
da = (1/20, -1/25, 3/100)
db = (-3/100, 1/20, 1/25)
tau = 1/8
epsilon = 11/400.
```

The uniform margin is checked by exact Fraction arithmetic.  For all `|t|<=tau`,

```text
|p+t dp-1/2| <= 21/400,
sum_k |a_k+t da_k| + sum_k |b_k+t db_k| <= 21/50,
```

so

```text
|f_t(x)-1/2| <= 189/400,
epsilon = 1/2 - 189/400 = 11/400.
```

The three actual endpoint/centre triangle margins are stronger:

```text
t=-1/8: 7/100
t=0:    3/50
t=1/8:  1/20
```

but the certificate uses the frozen uniform `epsilon=11/400`.

## Extreme-Past Kernels

For each `t in {-tau,0,tau}` and for both `f_t` and `1-f_t`, the script computes a rational finitely supported matrix `X` for the half-line equation

```text
T Y = B,
```

where `T` is the all-past Toeplitz compression, `B` is the past-to-future block, and `C` is the future block.  With

```text
R = B - T X,
H_X = B*X + X*B - X*T*X,
A_X = C - H_X,
```

the exact variational identity is

```text
A_X - C_infty = R* T^{-1} R,
```

where `C_infty=C-B*T^{-1}B` is the true Lyons--Steif all-one extreme-past kernel.  Since `T>=epsilon I`,

```text
0 <= A_X-C_infty <= (||R||_F^2/epsilon) I.
```

The implementation bounds `||R||_F` by the rational sum of absolute real and imaginary parts and records `delta=r_bound^2/epsilon`.

The six computed operator-error upper bounds are:

```text
t=-1/8, f:     1.3849052183269602e-31
t=-1/8, 1-f:   3.6452428705615193e-53
t=0,    f:     9.937685288339921e-30
t=0,    1-f:   3.3250707019379004e-54
t=1/8,  f:     4.5184132950619655e-28
t=1/8,  1-f:   4.429901528059021e-55
```

All are far below `11/400`.

As a cross-check using the separately authored round-one outer-factor implementation, I compared all six leading `3 by 3` corners with the finite Fejer--Riesz/Lyons--Steif outer-factor formula already developed there.  The maximum numerical corner difference was `1.55431223e-15`, consistent with ordinary floating-point root/factor reconstruction error.

## Rate Bounds

For each of the three symbols, the certificate computes:

```text
U_n(f_t) = H(X_0 | X_{-n},...,X_{-1})
```

as an upper bound on `h(f_t)`, using exact finite DPP event probabilities.

It also computes a lower bound `L_n(f_t)` by conditioning on each length-`n` suffix and using the two extreme-past one-site probabilities.  The all-one boundary comes from the enclosed kernel for `f_t`; the all-zero boundary comes from `1-f_t` and complementing.  For each suffix, the lower entropy contribution is the minimum of binary entropy over the certified interval.  This is exactly the Lyons--Steif Section 6 method with finite, outward-enclosed boundary kernels.

The strict negative-pair gate is

```text
((U_-(n)+U_+(n))/2) - L_0(n) < 0.
```

The run at `n=4` gives:

```text
t=-1/8:
  L = 0.68704911842059224
  U = 0.68705776108887717

t=0:
  L = 0.68748387346393514
  U = 0.68749508399726134

t=1/8:
  L = 0.68788035176808082
  U = 0.68789529374763303
```

Therefore

```text
lower gap = -3.0348902924818035e-05
upper gap = -7.3460456800473595e-06.
```

The upper endpoint is strictly negative, so the fixed pair is rigorously excluded as a positive rate counterexample.  Since `n=4` already separates the sign, the planned `n=8` expansion was not run.

## Exact Arithmetic Coverage

The boundary unit computed six extreme kernels:

```text
3 t-values x 2 complement choices = 6 cases
M = 64
residual rows checked per case = 67
actual residual complex entries = 1206
```

The rate unit at `n=4` computed:

```text
3 symbols x 3 event distributions x 2^(n+1)
= 3 x 3 x 32
= 288 exact determinants.
```

Every event mass was a positive Fraction, and each distribution was checked to normalize to one by exact rational equality.  Complex Bareiss divisions were required to divide exactly, and Hermitian determinants were required to have zero imaginary part.

The interval-log step used mpmath interval arithmetic at 45 decimal digits, then extracted rational dyadic endpoints for the final outward sums.

## Minimum Remaining Gap

No mathematical or implementation gap remains for this fixed-pair negative exclusion, assuming the standard Lyons--Steif DPP conditioning, negative association and entropy-rate formula accepted in the frozen task.

Remaining S1 obligations are outside this file:

- this does not prove a family theorem for non-even mixed directions;
- this does not prove or disprove the full scalar entropy-rate concavity conjecture;
- positive finite jets still require a separate rate certificate with all three symbols handled individually.
