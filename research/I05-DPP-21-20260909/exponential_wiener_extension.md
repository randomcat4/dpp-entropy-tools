# Extension from finite range to an exponentially weighted Wiener class

Status: **PROVED (AUTHOR PROOF), NOT INDEPENDENTLY REVIEWED**.

This file strengthens Theorem FR in `finite_range_local_theorem.md`. It does not change the status of the whole-legal-interval problem, which remains **INCOMPLETE**.

## 1. Statement

For `beta>0`, define

```text
A_beta={u:T->C : ||u||_beta:=sum_{j in Z} exp(beta|j|)|u_hat(j)|<infinity}.
```

Let real `c,g in A_beta` satisfy

```text
c(theta+1/2)=c(theta),
g(theta+1/2)=-g(theta),
g != 0,
delta<=c(theta)<=1-delta                              (1.1)
```

for some `delta>0`. Put `mu=integral c`. For any odd `k` with `g_hat(k)!=0`, set

```text
gamma=|g_hat(k)|^2,
alpha_k=gamma^2/[8mu^2(1-mu^2)].                     (1.2)
```

### Theorem EW

There is `epsilon=epsilon(c,g,k,beta,delta)>0` such that

```text
t -> h(c+t g)+alpha_k t^4                            (1.3)
```

is concave on `[-epsilon,epsilon]`. Hence `h(c+t g)` is strictly concave there.

No smallness assumption is imposed on the ordinary or weighted Wiener norm of `c-1/2`. Finite Fourier support is a special case.

The exact parity identity, matching KL bound, Ruelle step, vanishing of the term linear in `s=t^2`, and final curvature constant are Sections 2, 3, 6, and 7 of `finite_range_local_theorem.md`. The only place where finite range was used there was the configuration-uniform exponential localization of complete-event inverses and conditionals. Sections 2–4 below replace precisely that input.

## 2. Exponential localization of every event inverse

For a finite interval `Lambda` and a complete zero set `Z subset Lambda`, write

```text
M_Z=K_c|_Lambda-I_Z.                                  (2.1)
```

The accretivity proof in Lemma 4.1 of `finite_range_local_theorem.md` applies without any range assumption and gives

```text
||M_Z^{-1}||<=delta^{-1}                              (2.2)
```

for every `Lambda,Z`.

We strengthen (2.2) to a common exponentially weighted Schur bound.

### Lemma 2.1

There are `a>0` and `B<infinity`, depending only on `c,beta,delta`, such that

```text
sup_{Lambda,Z} ||M_Z^{-1}||_a<=B,                     (2.3)
```

where

```text
||A||_a=max{sup_i sum_j exp(a|i-j|)|A_ij|,
              sup_j sum_i exp(a|i-j|)|A_ij|}.         (2.4)
```

#### Proof

Let

```text
c^(W)(theta)=sum_{|j|<=W} c_hat(j) exp(-2pi i j theta),
E_W=K_{c-c^(W)}|_Lambda.                              (2.5)
```

Young's inequality gives

```text
||E_W||<=tau_W:=sum_{|j|>W}|c_hat(j)|.                (2.6)
```

Choose `W` large enough that `tau_W<delta/4`, and put

```text
B_Z=K_{c^(W)}|_Lambda-I_Z=M_Z-E_W.                    (2.7)
```

The singular values of `M_Z` are at least `delta`. Hence those of `B_Z` are at least

```text
eta:=3delta/4.                                        (2.8)
```

Moreover `M_Z` is Hermitian with spectrum in `[-(1-delta),1-delta]`, so

```text
||B_Z||<=1-delta+tau_W<1.                             (2.9)
```

Thus `B_Z` is a Hermitian band matrix of half-bandwidth `W`, `B_Z^2>=eta^2 I`, and `||B_Z||<1`. With `q=1-eta^2`, the same polynomial identity as Lemma 4.2 gives

```text
|(B_Z^{-1})_ij|
 <=eta^{-2}q^{max(0,ceil((|i-j|/W-1)/2))}.            (2.10)
```

Choose

```text
a_W=min{beta/2, -log(q)/(8W)}.                        (2.11)
```

Summing (2.10) shows

```text
sup_{Lambda,Z}||B_Z^{-1}||_{a_W}<=C_delta(1+W).       (2.12)
```

The precise linear factor is immaterial; it follows by grouping distances into intervals of length `W` and summing a geometric series.

On the other hand,

```text
||E_W||_{a_W}
 <=sum_{|j|>W} exp(a_W|j|)|c_hat(j)|
 <=exp(-beta W/2)||c||_beta.                          (2.13)
```

Because the right side of (2.12) grows at most linearly while (2.13) decays exponentially, enlarge `W` until

```text
||B_Z^{-1}||_{a_W}||E_W||_{a_W}<=1/2                 (2.14)
```

uniformly in `Lambda,Z`. The weighted Schur norm is submultiplicative, and

```text
M_Z^{-1}=(I+B_Z^{-1}E_W)^{-1}B_Z^{-1}.               (2.15)
```

The Neumann series in the weighted norm gives (2.3) with `a=a_W` and `B=2C_delta(1+W)`. QED.

No probability of a complete event enters this proof; rare configurations are covered by the same constants.

## 3. A common complex disk

For complex `z`, put

```text
M_Z(z)=K_{c+zg}|_Lambda-I_Z=M_Z+zG_Lambda,
G_Lambda=K_g|_Lambda.                                 (3.1)
```

Since `g in A_beta` and `a<=beta/2`,

```text
sup_Lambda ||G_Lambda||_a<=||g||_a<=||g||_beta.       (3.2)
```

Lemma 2.1 and another weighted-norm Neumann series imply that for

```text
|z|<r_0:=[2B||g||_a]^{-1},                            (3.3)
```

all complete-event matrices are invertible and

```text
sup_{Lambda,Z,|z|<r_0}||M_Z(z)^{-1}||_a<=2B.          (3.4)
```

This disk is independent of the volume and the complete configuration. Positivity is used only on the real legal slice; (3.4) is a complex analytic estimate.

## 4. Exponentially local one-sided complete-event conditionals

Let `x=(x_1,...,x_r)` be a future word, and let `M_{r,x}(z)` be its event matrix. The exact Schur complement is again

```text
q_{r,z}(x)=P_z(X_0=1|X_1...X_r=x)
 =c_hat(0)+z g_hat(0)-b_r(z)M_{r,x}(z)^{-1}d_r(z).    (4.1)
```

The rows `b_r(z)` and columns `d_r(z)` are no longer finitely supported, but their weighted `l^1` norms are uniformly bounded by `||c||_a+|z|||g||_a`, and their tails beyond distance `r` are `O(exp(-ar))`.

For `R>r`, split `[1,R]` into the near block `N=[1,r]` and far block `F=[r+1,R]`. The full inverse block formula gives

```text
[M_R(z)^{-1}]_{NN}-M_N(z)^{-1}
 =M_N(z)^{-1}E_NF(z) S_F(z)^{-1}E_FN(z)M_N(z)^{-1},  (4.2)
```

where

```text
S_F=M_F-E_FN M_N^{-1}E_NF.                           (4.3)
```

With `S_F=M_F-E_FN M_N^{-1}E_NF`, the block inverse formula gives exactly `S_F^{-1}=[M_R^{-1}]_{FF}`. Restricting rows and columns cannot increase the weighted Schur norm, so (3.4) bounds this inverse uniformly. The opposite Schur formula also writes it as `M_F^{-1}` plus the standard correction; no additional correction is added to the `FF` block itself.

Multiplying a row localized at site zero by `M_N^{-1}E_NF` produces a row on `F` whose ordinary `l^1` norm is `O(exp(-ar))`: in the weighted norm, every index of `F` has distance at least `r` from zero. The analogous column on the right has the same bound. Terms in the full quadratic form involving the direct tails `b_F` or `d_F` are also `O(exp(-ar))`. Therefore, on every smaller disk `|z|<=r_1<r_0`,

```text
sup_x |q_{R,z}(x)-q_{r,z}(x_1,...,x_r)|
 <=A exp(-a' r)                                       (4.4)
```

for some `A<infinity` and `a'>0` independent of `R,r,x`.

Equation (4.4) proves uniform convergence to a limit `q_z` on the one-sided tail space. Fix `0<b<min(a',1)` and use `||F||_b=||F||_infinity+sup_{m>=0} exp(bm) var_m(F)`, where `var_m` compares tails agreeing in their first `m` symbols. Applying (4.4) also at shorter truncations gives uniform stronger `a'`-variation bounds for the finite conditionals and their limit. Interpolation with the sup-norm error gives `||q_{r,z}-q_z||_b<=C exp(-(a'-b)r)` on each smaller disk. The finite-cylinder maps are holomorphic in this fixed space. Cauchy's formula on disks `|z|<=r_1<r_2<r_0` gives convergence in the same norm for parameter derivatives, so `z->q_z` is Banach-holomorphic in this fixed weaker Hölder space.

For real sufficiently small `t`, (1.1) gives a strict spectral margin for `c+tg`. The complete-event accretivity argument gives a uniform conditional bound away from zero and one. Hence

```text
g_t(1x)=q_t(x),
g_t(0x)=1-q_t(x)                                      (4.5)
```

is a strictly positive normalized Hölder `g`-function. Half-period diagonal gauge invariance makes it even in `t`, so it is holomorphic in `s=t^2`.

This establishes exactly the analytic input used in Sections 6 and 7 of `finite_range_local_theorem.md`.

## 5. Completion of Theorem EW

The finite parity identity and matching argument do not require finite range. Thus, for each fixed legal `t`,

```text
R(t):=h(c)-h(c+tg)
 >=1/2 d(mu^2-gamma t^2 || mu^2).                    (5.1)
```

Section 4 and the finite-alphabet Ruelle-Perron-Frobenius theorem give

```text
R(t)=mathcal R(t^2),
mathcal R(s)=nu_s(log(G_s/G_0)),                      (5.2)
```

with `mathcal R` analytic. Normalization `G_s(0x)+G_s(1x)=1` gives `mathcal R'(0)=0`. Therefore

```text
R(t)=A t^4+O(t^6),
A>=gamma^2/[4mu^2(1-mu^2)].                          (5.3)
```

After reducing `epsilon`,

```text
R''(t)>=6 gamma^2 t^2/[4mu^2(1-mu^2)].               (5.4)
```

The second derivative of the correction in (1.3) is exactly the right side of (5.4), so (1.3) is concave. Strictness follows from strict convexity of `t^4`. QED.

## 6. Scope and comparison

Theorem EW is a non-small-norm analytic-symbol domain. It is not obtained by a constant-center theorem, an `L`-ensemble interpolation, a spectral-basis rotation, or a finite-window fit. It includes complex Hermitian Toeplitz kernels coming from real non-even symbols.

The exponential Fourier hypothesis is used for a common complex Hölder neighborhood. It is not asserted to be necessary. Ordinary `H^{1/2}` or psi-mixing alone does not provide the weighted complete-event inverse estimate used here. The sign remains local in `t`; nothing in this extension proves whole-legal-interval concavity.