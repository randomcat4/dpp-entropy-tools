# Strict finite-range half-period symbols: a true entropy-rate theorem

Status of the theorem in this file: **PROVED (AUTHOR PROOF), NOT INDEPENDENTLY REVIEWED**.

Status of the original whole-legal-interval problem: **INCOMPLETE**.

All logarithms are natural. Every probability below is the complete-configuration DPP probability obtained from the inclusion minors by Möbius inversion (equivalently, by the signed determinant formula). No event, Fisher term, or conditional acceleration is deleted. The parameter path is the genuine affine path in the correlation kernel.

## 1. Statement

For a real trigonometric polynomial `u` on `T=R/Z`, write

```text
u_hat(j)=integral_T u(theta) exp(2 pi i j theta) dtheta.
```

Let `c,g` be real trigonometric polynomials such that

```text
c(theta+1/2)=c(theta),
g(theta+1/2)=-g(theta),
g is not identically zero,
0<delta<=c(theta)<=1-delta<1                     (1.1)
```

for some `delta>0`. The center `c` may be nonconstant and its mean need not be `1/2`. Put

```text
mu = integral_T c(theta)dtheta in (0,1).
```

Choose any odd integer `k>=1` with `g_hat(k) != 0`, and set

```text
gamma = |g_hat(k)|^2,
C_k   = gamma^2/[4 mu^2(1-mu^2)],
alpha_k = C_k/2 = gamma^2/[8 mu^2(1-mu^2)].       (1.2)
```

### Theorem FR

There is an `epsilon=epsilon(c,g,k)>0` such that `c+t g` is strictly legal for `|t|<=epsilon` and

```text
t -> h(c+t g)+alpha_k t^4                         (1.3)
```

is concave on `[-epsilon,epsilon]`. Consequently `t -> h(c+t g)` is strictly concave there.

The interval is obtained from a spectral-gap/analyticity argument and is not claimed to be the whole legal interval. Its existence is uniform in the window size and is proved at the entropy-rate level; it is not inferred from a finite sample.

This is structurally outside PR39. PR39 assumes mean `1/2`, `2||c-1/2||_W<1`, and then gives an explicit small interval by a complex row-sum expansion. Theorem FR instead assumes finite Fourier range and a pointwise spectral margin. It permits arbitrary mean and arbitrarily large Wiener norm subject to strict legality.

## 2. Exact finite parity identity

Let `P_{n,t}` be the complete DPP law on `Lambda_n={1,...,n}` with kernel `K_{c+tg}|_{Lambda_n}`. The half-period identities imply

```text
c_hat(j)=0 for odd j,
g_hat(j)=0 for even j.                              (2.1)
```

Thus the restrictions of `P_{n,t}` to the even and odd sites do not depend on `t`. At `t=0` these two parity restrictions are independent, since all cross-parity entries of `K_c` vanish. Therefore

```text
D(P_{n,t} || P_{n,0}) = H_n(c)-H_n(c+t g).          (2.2)
```

Indeed, `P_{n,0}` is the product of the two true marginals of `P_{n,t}`, so the relative entropy in (2.2) is exactly their mutual information. This uses all complete configurations.

Let `U=diag((-1)^j:j in Lambda_n)`. Equation (2.1) gives

```text
K_{c-tg}|_{Lambda_n}=U K_{c+tg}|_{Lambda_n} U*.
```

Every signed event determinant is invariant under this diagonal conjugation. Hence every finite cylinder probability, every finite conditional probability, and `H_n(c+tg)` are even functions of `t`.

Taking `n->infinity` in (2.2), separately for each fixed legal `t`, gives

```text
R(t):=lim_n D(P_{n,t}||P_{n,0})/n
     =h(c)-h(c+t g).                                  (2.3)
```

No derivative has been interchanged with this limit.

## 3. A finite matching gives a true rate lower bound

Fix the odd `k` from (1.2). On each arithmetic chain of step `k` inside `Lambda_n`, pair consecutive vertices. This gives a vertex-disjoint matching `M_n` of step-`k` edges with

```text
|M_n| >= (n-k)/2.                                     (3.1)
```

For an edge `e={i,i+k}`, set `Z_e=X_i X_{i+k}`. Since `k` is odd, its endpoints lie in different parity blocks. Under `P_{n,0}` they are independent and each has mean `mu`, while under `P_{n,t}` the two-point inclusion determinant is

```text
E_0 Z_e = mu^2,
E_t Z_e = mu^2-gamma t^2.                             (3.2)
```

For `u<=0`, `exp(u Z_e)` is nonnegative and decreasing in the coordinates of `e`. Determinantal negative association, applied successively to the disjoint edges, yields

```text
E_0 exp(u sum_{e in M_n} Z_e)
 <= [1-mu^2+mu^2 exp(u)]^{|M_n|}.                     (3.3)
```

The entropy variational inequality

```text
D(P||Q)>=E_P F-log E_Q exp(F)
```

with `F=u sum_e Z_e`, followed by optimization over `u<=0`, gives the exact binary-KL bound

```text
D(P_{n,t}||P_{n,0})
 >= |M_n| d(mu^2-gamma t^2 || mu^2),                  (3.4)
```

where `d(a||b)=a log(a/b)+(1-a)log((1-a)/(1-b))`. Legality guarantees `0<=mu^2-gamma t^2<=mu^2`, so the optimizing tilt is indeed nonpositive.

Divide (3.4) by `n`, use (2.3), and let `n->infinity`. For every fixed legal `t`,

```text
R(t)>=1/2 d(mu^2-gamma t^2 || mu^2).                  (3.5)
```

In particular, as `t->0`,

```text
R(t)>= C_k t^4+O(t^6),                                (3.6)
```

because

```text
d(a-x||a)=x^2/[2a(1-a)]+O(x^3).
```

The remaining task is to prove that `R` is analytic and has no quadratic term. This is where finite Fourier range replaces PR39's small Wiener disk.

## 4. Uniform inverses for every complete event

Let `K` be any finite Hermitian matrix satisfying

```text
eta I <= K <= (1-eta)I,       0<eta<=1/2.             (4.1)
```

For a complete configuration `x`, let `Z(x)` be its zero set and put

```text
M_x=K-I_{Z(x)}.                                       (4.2)
```

### Lemma 4.1 (configuration-uniform inverse)

For every `x`,

```text
||M_x^{-1}|| <= eta^{-1}.                             (4.3)
```

#### Proof

Let `S=Z(x)^c` and `J=I_S direct-sum (-I_Z)`. For `v=(v_S,v_Z)`, the two cross terms in `v*J M_x v` are negatives of each other's conjugates. Hence

```text
Re(v*J M_x v)
 =v_S* K_SS v_S+v_Z*(I-K_ZZ)v_Z
 >=eta ||v||^2.                                       (4.4)
```

Since `J` is unitary,

```text
eta||v||^2<=|v*J M_xv|<=||v|| ||M_xv||.
```

Thus the smallest singular value of `M_x` is at least `eta`. QED.

This proof includes arbitrarily rare configurations and does not use a lower probability bound for them.

### Lemma 4.2 (uniform exponential inverse decay)

Assume additionally that `K_ij=0` for `|i-j|>w`. Put `q=1-eta^2`. Then

```text
|(M_x^{-1})_ij|
 <= eta^{-2} q^{max(0,ceil((|i-j|/w-1)/2))}.          (4.5)
```

#### Proof

The matrix `M_x` is Hermitian, `||M_x||<=1`, and Lemma 4.1 gives `M_x^2>=eta^2 I`. Therefore

```text
M_x^{-1}=M_x(M_x^2)^{-1}
        =sum_{r>=0} M_x(I-M_x^2)^r.                   (4.6)
```

The norm of `I-M_x^2` is at most `q`; the `r`th summand has bandwidth `(2r+1)w`. Terms below the exponent in (4.5) have zero `(i,j)` entry, and the remaining geometric tail is at most `q^r/(1-q)=eta^{-2}q^r`. QED.

## 5. Holomorphic Hölder one-sided conditionals

Let `w` contain the Fourier supports of both `c` and `g`. For a word `x=(x_1,...,x_r)` on the future sites `{1,...,r}`, write `Z(x)={j:x_j=0}` and

```text
M_{r,x}(z)=K_{c+zg}|_{[1,r]}-I_{Z(x)}.                (5.1)
```

At `z=0`, Lemmas 4.1-4.2 apply with `eta=delta`, uniformly in `r` and `x`.

Choose `a>0` so small that `exp(2aw)(1-delta^2)<1`. On finite matrices define the weighted Schur norm

```text
||A||_a=max{sup_i sum_j exp(a|i-j|)|A_ij|,
              sup_j sum_i exp(a|i-j|)|A_ij|}.         (5.2)
```

It is submultiplicative. Lemma 4.2 implies a finite constant `B_0(c,delta,a)` such that

```text
sup_{r,x} ||M_{r,x}(0)^{-1}||_a <= B_0.               (5.3)
```

The banded matrix `G_r=K_g|_{[1,r]}` has

```text
sup_r ||G_r||_a <= B_g<infinity.                       (5.4)
```

Consequently, for

```text
|z|<r_0:=(2B_0B_g)^{-1},                              (5.5)
```

the weighted-norm Neumann series gives

```text
M_{r,x}(z)^{-1}
 =[I+z M_{r,x}(0)^{-1}G_r]^{-1}M_{r,x}(0)^{-1},
||M_{r,x}(z)^{-1}||_a<=2B_0.                          (5.6)
```

The radius and bound are independent of the word and its length.

Let `b_r(z)` and `d_r(z)` be the row and column coupling site `0` to `[1,r]`. The exact complete-event Schur complement gives

```text
q_{r,z}(x):=P_z(X_0=1 | X_1...X_r=x)
 =c_hat(0)+z g_hat(0)-b_r(z)M_{r,x}(z)^{-1}d_r(z).    (5.7)
```

For real legal `z=t`, this is an ordinary conditional probability. Equation (5.7) is used only as a holomorphic continuation for complex `z`.

Because `c,g` have range `w`, the vectors `b_r,d_r` are supported within distance `w` of site `0`. If `R>r>w` and a word of length `R` extends a word of length `r`, partition `M_{R,x}` into the remote block `[r+1,R]` and the near block `[1,r]`. The Schur-complement correction to the near block is supported within `w` of the cut at `r`. Formula (5.6) therefore gives

```text
sup_{|z|<=r_1}|q_{R,z}(x)-q_{r,z}(x_1,...,x_r)|
 <=A exp(-a r)                                         (5.8)
```

for every fixed `r_1<r_0`, with `A` independent of `R,r,x`. Explicitly, the resolvent identity writes the difference as a product of: a row propagated from the support of `b_r` to the cut, the bounded cut Schur term, and a column propagated back to the support of `d_r`; each propagation is bounded by (5.6). This proves (5.8) without averaging over or deleting remote configurations.

It follows that `q_{r,z}` converges uniformly to a limit `q_z` on the one-sided tail space. If two tails agree in their first `r` symbols, (5.8) gives

```text
|q_z(x)-q_z(y)|<=2A exp(-ar).                          (5.9)
```

Fix `0<b<min(a,1)` and use the norm `||F||_b=||F||_infinity+sup_{m>=0} exp(bm) var_m(F)` on the one-sided tail space, where `var_m` compares tails agreeing in their first `m` symbols. Applying (5.8) also at shorter truncations gives a uniform stronger `a`-variation bound for `q_{r,z}` and `q_z`. Together with the sup-norm error in (5.8), this yields `||q_{r,z}-q_z||_b<=C exp(-(a-b)r)` on each smaller disk. The finite-cylinder maps are holomorphic in this fixed space; Cauchy's formula on disks `|z|<=r_1<r_2<r_0` gives convergence there also for parameter derivatives. Therefore

```text
z -> q_z                                                    (5.10)
```

is a Banach-space holomorphic map.

For real sufficiently small `t`, `c+tg` lies in `[delta/2,1-delta/2]`. Applying (4.4) once with site `0` occupied and once with it empty gives

```text
delta/2<=q_t(x)<=1-delta/2                              (5.11)
```

for every tail. Define the normalized positive Hölder `g`-function

```text
g_t(1x)=q_t(x),
g_t(0x)=1-q_t(x).                                      (5.12)
```

The diagonal gauge from Section 2 shows `q_{r,-t}=q_{r,t}`; hence `q_{-t}=q_t`. The holomorphic family in (5.10) therefore contains only even powers and can be written

```text
g_t=G_s,       s=t^2,                                 (5.13)
```

with `s -> G_s` holomorphic near `0` in a Hölder space.

## 6. Transfer operator and an analytic true entropy rate

We use the following standard Ruelle-Perron-Frobenius fact for the mixing full shift on the finite alphabet `{0,1}`, in the fixed Hölder space chosen above. The simple eigenvalue and spectral gap follow, for example, from Cioletti-Silva, Theorem 2.1, as recorded in `sources.md`. Their integral operator with the uniform prior on `{0,1}` and potential `log(2G_s)` is exactly the sum operator (6.1). We use their Hölder theorem, not a spectral-gap assertion for the full Walters class.

> A strictly positive normalized Hölder `g`-function has a unique `g`-measure. Its transfer operator on a Hölder space has the simple isolated eigenvalue `1` and a spectral gap. For a Banach-holomorphic family of such functions, the normalized eigenmeasure is holomorphic as a functional on Hölder observables.

For completeness, the analytic statement follows from the spectral-gap statement by choosing a small contour around `1`: the Riesz projection

```text
Pi_s=(2 pi i)^{-1} integral_contour (z-L_s)^{-1} dz
```

is holomorphic, has rank one, and its dual projection applied to any fixed probability functional, followed by normalization at the constant function `1`, gives the holomorphic eigenmeasure. The normalization `L_s 1=1` keeps the eigenvalue exactly at `1`.

Here

```text
(L_s F)(x)=sum_{a=0,1} G_s(ax)F(ax).                  (6.1)
```

The stationary DPP law is a `G_s`-measure: its finite conditional probabilities are (5.7), and (5.8) gives their uniform limit. Uniqueness therefore identifies it with the transfer-operator eigenmeasure, denoted `nu_s`.

The chain rule written from right to left gives, for a finite block,

```text
H(X_0,...,X_{n-1})
 =sum_{j=0}^{n-1} H(X_j | X_{j+1},...,X_{n-1}),       (6.2)
```

and the analogous sum for relative entropy. The logarithms are uniformly Lipschitz on the interval in (5.11), while (5.8) is exponentially summable. Hence replacing each finite-tail conditional in (6.2) by `G_s` makes an error bounded by a constant independent of `n`. Dividing by `n` proves the exact rate formulas

```text
h(c+t g)=-nu_s(log G_s),                              (6.3)
R(t)=nu_s(log(G_s/G_0)),       s=t^2.                 (6.4)
```

Both sides are analytic near zero. This is a volume-uniform derivation of the rate formula; it does not differentiate a sequence `H_n/n`.

## 7. The linear term in `s` vanishes

Write the right side of (6.4) as `mathcal R(s)`. Since `G_0/G_0=1`,

```text
mathcal R(0)=0.
```

On differentiating the analytic formula at zero, the derivative of `nu_s` multiplies the zero observable and disappears. Thus

```text
mathcal R'(0)=nu_0(dot G_0/G_0).                       (7.1)
```

Condition on the tail `x`. The conditional distribution of the first bit under `nu_0` is `G_0(ax)`, so

```text
nu_0(dot G_0/G_0)
 =integral sum_{a=0,1} G_0(ax) dot G_0(ax)/G_0(ax) dnu_0(x)
 =integral sum_{a=0,1} dot G_0(ax) dnu_0(x)=0,         (7.2)
```

because `G_s(0x)+G_s(1x)=1`. Therefore

```text
R(t)=A t^4+O(t^6)                                     (7.3)
```

for some real `A`.

The true rate inequality (3.5), not a finite-window coefficient extrapolation, now gives

```text
A>=C_k=gamma^2/[4mu^2(1-mu^2)]>0.                    (7.4)
```

Consequently

```text
R''(t)=12A t^2+O(t^4).                                (7.5)
```

After reducing `epsilon` if necessary,

```text
R''(t)>=6C_k t^2       for |t|<=epsilon.              (7.6)
```

Since `h(c+t g)=h(c)-R(t)` and `12 alpha_k=6C_k`, equations (1.2) and (7.6) give

```text
[d^2/dt^2][h(c+t g)+alpha_k t^4]<=0.                 (7.7)
```

This proves (1.3). Because `t^4` is strictly convex, the finite Jensen inequality for (1.3) implies strict concavity of `h(c+t g)` for every nontrivial subchord. QED.

## 8. Explicit center excluded by PR39's Wiener hypothesis

The theorem is not merely a change of constants inside PR39. Define the Rudin-Shapiro polynomials by

```text
P_0=Q_0=1,
P_{r+1}(z)=P_r(z)+z^{2^r}Q_r(z),
Q_{r+1}(z)=P_r(z)-z^{2^r}Q_r(z).                      (8.1)
```

For `|z|=1`,

```text
|P_r(z)|^2+|Q_r(z)|^2=2^{r+1}.                       (8.2)
```

The degree-15 polynomial is

```text
P_4(z)=1+z+z^2-z^3+z^4+z^5-z^6+z^7
       +z^8+z^9+z^10-z^11-z^12-z^13+z^14-z^15.      (8.3)
```

Put `z=exp(4 pi i theta)` and

```text
c(theta)=1/2+(1/16) Re(P_4(z)-1),
g(theta)=(1/64) cos(2 pi theta).                     (8.4)
```

Then `c` is half-period invariant, `g` is half-period anti-invariant, and `c` is nonconstant with mean `1/2`. From (8.2),

```text
|c(theta)-1/2|<=(4 sqrt(2)+1)/16<1/2,
min(c,1-c)>=(7-4 sqrt(2))/16>0.                       (8.5)
```

Each of the 15 nonconstant monomials in (8.3) contributes total absolute Fourier mass `1/16`, so

```text
||c-1/2||_W=15/16,
2||c-1/2||_W=15/8>1.                                 (8.6)
```

Thus PR39 does not apply to this center. Here `g_hat(1)=1/128`, so `gamma=2^{-14}` and Theorem FR gives an `epsilon>0` such that

```text
t -> h(c+t g)+t^4/(3*2^27)                           (8.7)
```

is concave on `[-epsilon,epsilon]`. One may take `epsilon` no larger than the elementary legality radius

```text
64*(7-4sqrt(2))/16=28-16sqrt(2),
```

but this proof does not claim that the transfer-operator radius equals that full legal radius.

## 9. Route comparison and remaining gap

### Prediction/variational route — selected and closed locally

The exact one-sided Schur complement (5.7) retains the full configuration-dependent inverse. Lemmas 4.1-4.2 control every event, including rare events. The Ruelle operator turns this volume-uniform control into the analytic rate formulas (6.3)-(6.4). The sign then comes from the exact KL variational bound (3.4), not from dropping acceleration terms.

### Cluster route — useful only after quasilocal reorganization

Expanding the determinant likelihood directly in powers of `t^2` requires a small operator/activity norm and recreates PR39's perturbative obstruction. The weighted inverse algebra above supplies convergence without a small Wiener row sum, but the sign is obtained more efficiently through the matching KL lower bound. No claim is made that individual cluster coefficients have one sign.

### Operator route — still open

The balanced fermionic beam-splitter identity in `proof.md` reduces finite midpoint concavity to an occupation-basis entropy inequality. Existing fermionic entropy-power results prove a von-Neumann/spectral entropy statement, not that occupation inequality. This route remains a precise bridge but is not used in Theorem FR.

### Unresolved scope

Theorem FR does not prove concavity on the entire legal interval, does not cover arbitrary measurable symbols, and gives no entropy-rate counterexample. Extending the Hölder/analytic argument to a compact interval does not by itself control the sign away from `t=0`; the exact remaining global obligation is still the sign of the parity mutual-information curvature.