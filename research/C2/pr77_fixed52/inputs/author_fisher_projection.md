# Exact adjacent-pair projection of the full Fisher-information rate

Status: **PROVED (AUTHOR PROOF), NOT INDEPENDENTLY REVIEWED**.

This result supplies a quantitative negative term in the Poisson/RPF curvature formula. It does not by itself sign the acceleration and invariant-measure response.

## 1. Full finite Fisher and the adjacent-pair statistic

Let `P_{n,t}` be the complete DPP law of the fixed symbol on `[1,n]`. Its full score and Fisher information are

```text
S_n(x)=partial_t log P_{n,t}(x),
I_n(t)=E_t S_n^2=sum_x [p'_{n,t}(x)]^2/p_{n,t}(x).    (1.1)
```

Every complete event appears in (1.1).

Put

```text
u=t/16,
Z_i=X_iX_{i+1},
T_n=sum_{i=1}^{n-1}Z_i.                               (1.2)
```

The adjacent two-point inclusion determinant gives

```text
m(t):=E_t Z_i=1/4-u^2=1/4-t^2/256,
m'(t)=-t/128.                                         (1.3)
```

Since `E_t S_n=0`, differentiation under the finite complete law gives

```text
partial_t E_t T_n
 =E_t[(T_n-E_tT_n)S_n].                               (1.4)
```

Cauchy-Schwarz therefore yields the exact full-Fisher projection

```text
I_n(t)>=[(n-1)t/128]^2/Var_t(T_n).                    (1.5)
```

This is a lower bound on the complete Fisher term; it is not a replacement for that term.

## 2. Exact asymptotic variance

The process is two-dependent because its kernel vanishes at distances larger than two. Hence the variables `Z_i` and `Z_j` are independent when `|i-j|>=4`. The required covariances follow from inclusion determinants on at most four sites:

```text
c_0=Var(Z_0)=3/16-u^2/2-u^4,

c_1=Cov(Z_0,Z_1)=7/128-u^2/4-u^4,

c_2=Cov(Z_0,Z_2)=-31/4096-u^2/32,

c_3=Cov(Z_0,Z_3)=-1/256,

c_j=0 for j>=4.                                      (2.1)
```

For example,

```text
E Z_0Z_1=det K_{0,1,2}=15/128-3u^2/4,                (2.2)
```

and the four-consecutive determinant factors under reflection into

```text
[(15/64-u^2)+u/4][(15/64-u^2)-u/4]
 =225/4096-17u^2/32+u^4.                              (2.3)
```

Subtracting `m(t)^2` gives `c_2`. For the set `{0,1,3,4}`, the only connection between the two adjacent pairs that survives in the determinant contributes `-(1/2)^2(1/8)^2=-1/256`, giving `c_3`.

Thus

```text
V(t):=lim_{n->infinity}Var(T_n)/n
 =c_0+2(c_1+c_2+c_3)
 =561/2048-17t^2/4096-3t^4/65536.                    (2.4)
```

On `1/2<=|t|<=3/2`,

```text
277197/1048576<=V(t)<=286141/1048576.                 (2.5)
```

In particular it is strictly positive.

## 3. Identification with the true conditional Fisher rate

Let `G_t` be the positive normalized one-sided complete-event conditional constructed from the exact signed event matrices, and put

```text
psi_t=partial_t log G_t.                              (3.1)
```

Normalization gives

```text
E_t[psi_t(X_iX_{i+1}...) | X_{i+1},X_{i+2},...]=0.   (3.2)
```

Hence the shifted `psi_t` are reverse martingale differences and are pairwise orthogonal in `L^2(P_t)`.

The finite right-to-left chain rule writes `S_n` as a sum of finite-future conditional scores. The configuration-uniform bounds in `proof.md` give, for some summable sequence independent of `n`,

```text
|partial_t log G_t^(r)-partial_t log G_t|
 <=416 C0(49/64)^(2r-6)        for r>=3.              (3.3)
```

Indeed, use `q>=1/16`, `|q'|<=9/8`, the value error `e_r`, and derivative error `8e_r`. The three boundary depths below `3` contribute only another fixed constant. Consequently

```text
S_n=sum_{i=1}^n psi_t o shift^i+R_n,
sup_n ||R_n||_infinity<infinity.                     (3.4)
```

Orthogonality and Cauchy-Schwarz imply

```text
lim_{n->infinity}I_n(t)/n=nu_t(psi_t^2)=:I(t).        (3.5)
```

This proves existence of the full Fisher-information rate without deleting rare configurations.

## 4. Quantitative true-rate bound

Divide (1.5) by `n` and use (2.4) and (3.5):

```text
boxed:
I(t)=nu_t(psi_t^2)
 >=t^2/[16384 V(t)].                                  (4.1)
```

The function `s/V(s)`, with `s=t^2`, is increasing because

```text
V(s)-sV'(s)=561/2048+3s^2/65536>0.                   (4.2)
```

At `|t|=1/2`, `V=286141/1048576`. Therefore the whole target interval has the uniform bound

```text
boxed:
nu_t(psi_t^2)>=16/286141>0.                           (4.3)
```

The exact regression remainder is also nonnegative:

```text
liminf_{n->infinity}(1/n)
 E_t[S_n-a_t(T_n-E_tT_n)]^2>=0,

a_t=m'(t)/V(t),                                      (4.4)
```

and expansion of (4.4) recovers (4.1).

## 5. Relation to curvature

The independently derived response identity is

```text
h''(t)=-nu_t(psi_t^2)
       +nu_t((psi_t^2-xi_t)v_t)
       -2nu_t(psi_t R_t(psi_t v_t)).                  (5.1)
```

Equation (4.3) rigorously supplies at least `16/286141` of negative curvature through the full Fisher term. The last two terms in (5.1) are not known to have a favorable sign, and no crude norm estimate obtained here is small enough to be dominated by (4.3). Thus (4.3) is a structural quantitative advance and a calibration target for issue #74, but not a proof of the continuum curvature theorem.