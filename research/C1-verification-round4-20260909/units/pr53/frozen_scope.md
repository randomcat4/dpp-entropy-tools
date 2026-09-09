# Frozen scope for PR53 first proof review

Reviewer: `C1 PR53 first reviewer`
Source: immutable PR53 snapshot from `randomcat4/dpp-entropy-tools`, commit `e0688fbb713e55f93acf791b83437ddf2cc06b7f`.
Local source directory: `source-snapshots/pr53`.

Status: frozen for verification. This review may accept or reject only the claims below. It may not add hypotheses, reinterpret the theorem, promote diagnostics to proof, or review excluded claims.

## Objects and definitions

All logarithms are natural. Entropy means complete-configuration Shannon entropy for finite determinantal point processes, never the spectral entropy `Tr b(K)` unless explicitly stated as von Neumann entropy of a quasifree state.

Let `T = R/Z`. A fixed real measurable scalar symbol `f:T->[0,1]` defines the stationary scalar DPP kernel

```text
K_f(i,j) = integral_T f(theta) exp(2 pi i (i-j) theta) dtheta.
```

For the half-period orbit, `f_t=c+t g`, with

```text
c(theta+1/2)=c(theta),
g(theta+1/2)=-g(theta).
```

The finite parity window is `{0,...,2m-1}`, reordered as even sites followed by odd sites. Under this permutation the kernel has block form

```text
K_m(t) = [ A_m      t C_m  ]
         [ t C_m*   A_m    ].
```

`P_m(t)` is the complete DPP law of this finite block kernel, `P_A` is the complete law of `A_m`, and `Q_m=P_A tensor P_A`.

For a general strict two-block finite kernel

```text
K_t = [ A    t C  ]
      [ t C* B    ],
```

with `0<A<I` and `0<B<I`, a complete configuration has first-block zero set `Z_x` and second-block zero set `Z_y`. Define

```text
M_x=A-I_{Z_x},       N_y=B-I_{Z_y},       s=t^2.
```

For the inverse lemma, `A` is a finite Hermitian matrix with

```text
delta I <= A <= (1-delta)I,       0<delta<=1/2,
```

and `M_Z=A-I_Z`. In the finite-range version, `A_ij=0` whenever `|i-j|>w`, with fixed `w>=1`.

For the operator route, `rho_K` is the finite gauge-invariant quasifree state with one-particle covariance `K`; its occupation-basis diagonal is the complete DPP law of `K`. `Delta` denotes occupation-basis dephasing.

## Claims under review

1. Parity joining identity and mutual-information-rate equivalence.

   For every legal `t`,

   ```text
   H(K_m(t)) = 2 H(A_m) - I_m(t),
   I_m(t)    = D(P_m(t) || Q_m).
   ```

   If `a_hat(k)=c_hat(2k)`, then

   ```text
   i(t) := lim_{m->infinity} I_m(t)/m
         = 2[h(a)-h(f_t)].
   ```

   Therefore concavity of `t -> h(c+t g)` on a legal interval is equivalent to convexity of `i(t)`.

2. Complete-event determinant likelihood and finite curvature identity.

   For strict finite two-block kernels, the exact complete-event likelihood relative to `Q=P_A tensor P_B` is

   ```text
   r_s(x,y)=det(I-s N_y^{-1} C* M_x^{-1} C).
   ```

   With `J(s)=E_Q[r_s log r_s]`, differentiation on a strict legal interval gives

   ```text
   J'(s)  = E_Q[r_s' log r_s],
   J''(s) = E_Q[(r_s')^2/r_s + r_s'' log r_s],
   H''(t) = -2 J'(s)-4s J''(s).
   ```

   Thus the exact finite concavity sign obligation is `J'(s)+2sJ''(s)>=0`. A volume-uniform version up to a sublinear or bounded boundary term remains an obligation, not a proved theorem.

3. Configuration-uniform inverse and exponential inverse decay under strict finite range.

   Under the spectral margin above, every complete-event matrix satisfies

   ```text
   ||M_Z^{-1}|| <= delta^{-1}.
   ```

   If `A` has bandwidth `w`, then with `q=1-delta^2` and `k0(d)=max(0,ceil((d/w-1)/2))`,

   ```text
   |(M_Z^{-1})_ij| <= delta^{-2} q^{k0(|i-j|)}.
   ```

   For strict finite-range half-period families this gives configuration-uniform, volume-uniform exponential locality for the conditional perturbations `D_y=-C(B-I_{Z_y})^{-1}C*`.

4. Balanced fermionic beam-splitter reduction and occupation-entropy remainder.

   For strict finite positive contractions `K_0,K_1`, the balanced number-conserving fermionic beam splitter maps `rho_{K_0} tensor rho_{K_1}` to a quasifree state with covariance

   ```text
   [ M   D ]
   [ D   M ],       M=(K_0+K_1)/2,       D=(K_1-K_0)/2,
   ```

   up to the sign convention for `D`. Both output occupation marginals are the DPP law of `M`. If `q` is the full output occupation-measurement distribution, then

   ```text
   H(q) <= 2H(M).
   ```

   The finite inequality

   ```text
   H(q) >= H(K_0)+H(K_1)
   ```

   would imply finite midpoint concavity. The exact decomposition is

   ```text
   2H(M)-H(K_0)-H(K_1)
     = I_q(X:Y) + [H(q)-H(K_0)-H(K_1)].
   ```

   The bracket is an unproved occupation-entropy gain. Known fermionic convolution or quantum entropy inequalities prove only the von Neumann/spectral statement, not this occupation-measurement inequality.

## Explicit non-claims

The source does not claim whole-legal-interval entropy-rate concavity, a proof of `J_m'(s)+2sJ_m''(s)>=-o(m)`, a proof of `(BS-occ)`, a positive true entropy-rate Jensen gap, a quantum/spectral entropy substitution for DPP Shannon entropy, a novelty result, or certification by the finite floating-point probe.

## Success criteria

The review must assign each scoped claim `CORRECT` or `CRITICAL_GAPS`; identify the exact remaining unproved sign obligation; check Fourier/parity indexing, rate normalization, non-normal event matrices, inverse bounds, volume-independent decay constants, tensor/fermionic marginals, and entropy distinctions; and distinguish exact proof from floating diagnostics.
