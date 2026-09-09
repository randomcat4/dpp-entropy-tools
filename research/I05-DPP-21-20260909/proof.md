# Exact bridges beyond the PR39 small-Wiener argument

All logarithms are natural. This file concerns complete-configuration Shannon entropy. It never substitutes the spectral entropy `Tr b(K)` for that quantity.

## 1. Frozen scope and parity block form

Let `f_t=c+t g`, with

```text
c(theta+1/2)=c(theta),
g(theta+1/2)=-g(theta).
```

For the window `{0,...,2m-1}`, reorder the observed coordinates as the even sites followed by the odd sites. Half-period symmetry gives

```text
K_m(t) = [ A_m      t C_m  ]
         [ t C_m*   A_m    ].                         (1.1)
```

Indeed, the even Fourier coefficients of `g` and the odd Fourier coefficients of `c` vanish. The two diagonal blocks are equal because the two parity classes are translates. The observed basis has only been permuted; no spectral basis rotation has occurred.

Write `P_m(t)` for the complete DPP law of (1.1), `P_A` for the complete law of `A_m`, and `Q_m=P_A tensor P_A`. The two parity marginals of `P_m(t)` are fixed and equal to `P_A`. At `t=0` they are independent.

## 2. Exact joining and mutual-information-rate bridge

### Proposition 2.1 (finite joining identity)

For every legal `t`,

```text
H(K_m(t)) = 2 H(A_m) - I_m(t),
I_m(t)    = D(P_m(t) || Q_m).                         (2.1)
```

#### Proof

Since `Q_m` is the product of the two true marginals of `P_m(t)`, the elementary identity

```text
D(P_XY || P_X tensor P_Y)=H(P_X)+H(P_Y)-H(P_XY)
```

gives (2.1). Every complete configuration is retained. At a boundary point the identity follows by continuity with the convention `0 log 0=0`. QED.

Let `a` be the decimated scalar symbol with Fourier coefficients
`a_hat(k)=c_hat(2k)`. Then `H(A_m)=H_m(a)`. Entropy-rate existence for each fixed symbol follows from stationarity and subadditivity. Hence (2.1) proves the existence of

```text
i(t) := lim_{m->infinity} I_m(t)/m
      = 2[h(a)-h(f_t)],                               (2.2)
```

without a separate mutual-information limit theorem.

### Corollary 2.2 (exact reformulation)

On any legal interval, `t -> h(c+t g)` is concave if and only if the parity mutual-information rate `i(t)` in (2.2) is convex.

This is the common target seen by prediction, cluster, and operator methods. It is not itself a sign proof.

## 3. Complete-event determinant likelihood

This section derives a finite, nonperturbative likelihood formula. Let more generally

```text
K_t = [ A    t C  ]
      [ t C* B    ],                                  (3.1)
```

where `0<A<I` and `0<B<I`. For a complete configuration `x` in the first block and `y` in the second, let `Z_x,Z_y` be their zero sets and define

```text
M_x=A-I_{Z_x},       N_y=B-I_{Z_y}.                   (3.2)
```

Strictness implies that every complete-event probability is positive and therefore `M_x,N_y` are invertible. The signed determinant formula for a complete DPP event is

```text
p_t(x,y)=(-1)^{|Z_x|+|Z_y|}
          det [ M_x     t C  ] .                       (3.3)
              [ t C*    N_y ]
```

Taking a Schur complement and writing `s=t^2` yields the exact density relative to the decoupled product law `Q=P_A tensor P_B`:

```text
r_s(x,y) := p_t(x,y)/Q(x,y)
          = det(I-s N_y^{-1} C* M_x^{-1} C).          (3.4)
```

No rank truncation is made. Although the matrices in (3.4) need not be Hermitian, the determinant is real and positive for every legal real `s`, because it is a probability ratio.

Set

```text
J(s)=D(P_t||Q)=E_Q[r_s log r_s].                      (3.5)
```

Since `E_Q r_s=1`, differentiation on a strict legal interval gives

```text
J'(s)  = E_Q[r_s' log r_s],                           (3.6)
J''(s) = E_Q[(r_s')^2/r_s + r_s'' log r_s].           (3.7)
```

The first term in (3.7) is the full Fisher term. The second is the complete acceleration term. Neither may be omitted. From `H(K_t)=H(A)+H(B)-J(t^2)`,

```text
H''(t) = -2 J'(s)-4s J''(s),       s=t^2.             (3.8)
```

Thus the exact finite sign obligation is

```text
J'(s)+2s J''(s) >= 0.                                 (3.9)
```

For the parity family, a volume-uniform version of (3.9), up to an `o(m)` boundary term, would pass to the rate through finite Jensen inequalities. Formula (3.9) is strictly weaker than demanding `J''>=0`, and it shows why an ordinary convexity claim for the determinant likelihood can be unnecessarily strong.

### Conditional version

Conditioning on the complete second-block configuration `y` gives the exact conditional DPP kernel

```text
K_{A|y}(t)=A+sD_y,
D_y=-C(B-I_{Z_y})^{-1}C*.                             (3.10)
```

The law of `y` is independent of `t`. Hence

```text
H(K_t)=H(B)+Phi(s),
Phi(s)=sum_y P_B(y) H(A+sD_y),                         (3.11)
H''(t)=2Phi'(s)+4sPhi''(s).                            (3.12)
```

Differentiating the normalization identity for the complete `B` events gives

```text
sum_y P_B(y)(B-I_{Z_y})^{-1}=0,
sum_y P_B(y)D_y=0.                                    (3.13)
```

Therefore `Phi'(0)=0`. Away from zero, however, the `D_y` are generally high-rank and indefinite. The missing statement is an averaged sign for (3.12), not a pointwise Hessian sign for every `y`.

## 4. A configuration-uniform inverse lemma

PR39 obtains a volume-uniform complex disk by imposing a small absolute Fourier row sum. The following lemma instead uses only a spectral margin and therefore remains valid when that Wiener condition fails.

### Lemma 4.1 (all complete-event matrices are uniformly invertible)

Let `A` be a finite Hermitian matrix satisfying

```text
delta I <= A <= (1-delta)I,       0<delta<=1/2.       (4.1)
```

For every set `Z`, put `M_Z=A-I_Z`. Then

```text
||M_Z^{-1}|| <= delta^{-1}.                            (4.2)
```

#### Proof

Let `S=Z^c` and `J=I_S direct-sum (-I_Z)`. For `v=(v_S,v_Z)`, the cross terms in `v* J M_Z v` are negatives of one another's conjugates. Consequently

```text
Re(v* J M_Z v)
 = v_S* A_SS v_S + v_Z*(I-A_ZZ)v_Z
 >= delta ||v||^2.                                    (4.3)
```

Since `J` is unitary,

```text
delta ||v||^2 <= |v*J M_Zv| <= ||v|| ||M_Zv||.
```

Thus the least singular value of `M_Z` is at least `delta`, proving (4.2). QED.

This argument includes every zero/one pattern and does not use a lower bound on the probability of that pattern.

### Lemma 4.2 (explicit inverse decay for finite range)

Under the hypotheses of Lemma 4.1, assume in addition that `A_ij=0` whenever `|i-j|>w`, with `w>=1`. Put `q=1-delta^2` and

```text
k0(d)=max(0, ceil((d/w-1)/2)).                         (4.4)
```

Then every complete-event matrix satisfies

```text
|(M_Z^{-1})_ij| <= delta^{-2} q^{k0(|i-j|)}.           (4.5)
```

#### Proof

`M_Z` is Hermitian and `-I<=M_Z<=(1-delta)I`, so `||M_Z||<=1`. Lemma 4.1 gives `M_Z^2>=delta^2 I`. Therefore

```text
R=I-M_Z^2,        0<=R<=qI,
M_Z^{-1}=M_Z(M_Z^2)^{-1}=sum_{k>=0} M_Z R^k.           (4.6)
```

`M_Z` has bandwidth `w`, `R` has bandwidth `2w`, and `M_ZR^k` has bandwidth `(2k+1)w`. The `(i,j)` entry vanishes for `k<k0(|i-j|)`. Bounding each remaining entry by the operator norm and summing a geometric series gives

```text
sum_{k>=k0} ||M_Z|| ||R||^k <= q^{k0}/(1-q)
                              = delta^{-2}q^{k0}.
```

QED.

### Consequence for the half-period family

Assume `c,g` are trigonometric polynomials and on a compact parameter interval `J`

```text
delta <= c+t g <= 1-delta        a.e., t in J.        (4.7)
```

After parity reordering, `A_m` and `C_m` have bandwidth bounded independently of `m`. Lemma 4.2 applies to every matrix `A_m-I_Z`. Hence all matrices `D_y` in (3.10) are exponentially quasilocal, uniformly in `m`, `y`, and `t in J`. In particular, truncating `D_y` to distance `R` makes an operator-norm error bounded by `C(delta,w,c,g) q^{R/(2w)}`, rather than by a bound involving the probability of `y`.

This is a genuine nonperturbative interface outside `2||c-1/2||_W<1`: large Fourier row sums are allowed. It establishes uniform locality/convergence control, but not the sign in (3.9) or (3.12).

## 5. Balanced fermionic beam splitter: an operator reduction

This route is independent of the prediction/cluster route.

For a strict finite positive contraction `K`, let `rho_K` be the gauge-invariant quasifree state with one-particle covariance `K`. In the occupation basis its diagonal is exactly the complete DPP law. One direct formula is

```text
rho_K = det(I-K) direct-sum_{r=0}^n wedge^r L,
L=K(I-K)^{-1};                                         (5.1)
```

therefore

```text
< S | rho_K | S > = det(I-K) det L_S = p_K(S).        (5.2)
```

Let

```text
W = 2^{-1/2} [ I   I ]
               [-I   I ]                              (5.3)
```

on two copies of the one-particle space, and let `Gamma(W)` be its fermionic second quantization. For two kernels `K_0,K_1`, put

```text
tau = Gamma(W)(rho_{K_0} tensor rho_{K_1})Gamma(W)*.
```

Quasifree covariance transforms covariantly, so

```text
K_tau = W(K_0 direct-sum K_1)W*
      = [ M   D ] ,
        [ D   M ]                                      (5.4)
M=(K_0+K_1)/2,       D=(K_1-K_0)/2
```

(up to an irrelevant sign convention for `D`). Both output marginals are `rho_M`.

Let `q` be the full occupation-measurement distribution of `tau`. Ordinary classical subadditivity gives

```text
H(q) <= 2 H(M).                                        (5.5)
```

Consequently, the following finite inequality would imply midpoint concavity for every finite DPP:

```text
H(q) >= H(K_0)+H(K_1).                    (BS-occ)      (5.6)
```

Indeed, (5.5)-(5.6) give `2H(M)>=H(K_0)+H(K_1)`.

The known fermionic convolution entropy inequality is not (5.6). Quantum subadditivity and unitary invariance give only

```text
2 S(rho_M) >= S(rho_{K_0})+S(rho_{K_1}),               (5.7)
```

where `S(rho_K)=Tr b(K)` is spectral/von-Neumann entropy. DPP Shannon entropy is instead

```text
H(K)=S(Delta rho_K)
    =S(rho_K)+D(rho_K || Delta rho_K),                  (5.8)
```

with `Delta` occupation-basis dephasing. Thus (5.6) additionally requires control of relative entropy of coherence under the beam splitter. Replacing (5.8) by (5.7), or diagonalizing `K`, would change the problem and is invalid.

There is also an exact decomposition of the desired midpoint gap:

```text
2H(M)-H(K_0)-H(K_1)
 = I_q(X:Y) + [H(q)-H(K_0)-H(K_1)],                    (5.9)
```

where `I_q(X:Y)=2H(M)-H(q)>=0` is the classical mutual information between the two output occupation strings. The bracket is the unproved occupation-entropy gain. Formula (5.9) shows that (BS-occ) is sufficient but stronger than midpoint concavity.

A local quasifree channel can scale the off-diagonal covariance block while fixing the diagonal covariance blocks, but it does not preserve the occupation diagonal algebra when the fixed block is correlated. Therefore quantum data processing does not manufacture a classical channel between the DPP laws. This is consistent with, and conceptually explains, the accepted PR39 local-classical-channel obstruction.

## 6. Route comparison and selected next obligation

### Prediction / conditional entropy

Equations (3.10)-(3.13) are exact and retain parameter-dependent weights and accelerations. Lemma 4.2 supplies uniform locality for finite-range strict symbols. The remaining work is to reorganize the average in (3.12) so that the Fisher term controls the signed acceleration up to a boundary error.

### Nonperturbative cluster regrouping

Equation (3.4) is a determinant polymer activity over the two parity blocks. A naive power series in `s` requires a norm smaller than one and merely recreates PR39. The finite-range alternative is to truncate the event inverses spatially using (4.5), group connected components in physical distance, and bound only the boundary disagreement. This controls convergence without assuming `2||c-1/2||_W<1`; it still needs a sign-preserving regrouping.

### Operator / ergodic route

Equations (5.4)-(5.9) reduce finite midpoint concavity to an occupation-coherence inequality for a balanced fermionic beam splitter. Existing quantum entropy-power inequalities control (5.7), not (5.6). The route is retained because a proof of (5.6), or merely a lower bound on its bracket by `-I_q`, would close the finite problem before taking any entropy-rate limit.

### Selected route

The finite-range prediction/cluster route is selected for the next analytic step because Lemma 4.2 already supplies a volume-uniform, configuration-uniform estimate unavailable in PR39. The precise missing lemma is:

```text
For fixed bandwidth, spectral margin delta, and a compact legal s-interval,
J_m'(s)+2sJ_m''(s) >= -C_boundary
```

with `C_boundary` independent of `m`, for the exact likelihood (3.4). Such a bound yields rate concavity by applying finite Jensen first and then dividing by `m`. No derivative of the limiting entropy rate is required.

## 7. What has and has not been proved

**PROVED here, as author derivations not independently reviewed:** Proposition 2.1, Corollary 2.2, formulas (3.3)-(3.13), Lemmas 4.1-4.2, and the balanced-beam-splitter reduction (5.4)-(5.9).

**NOT proved:** (3.9) globally, the boundary-uniform signed estimate in Section 6, (BS-occ), whole-legal-interval concavity for the PR39 example, or any positive true entropy-rate Jensen gap.

Finite numerical probes, if run, are diagnostics only and cannot upgrade this status.
