# Compact nonzero-parameter tubes for stationary scalar DPP entropy rate

All logarithms are natural. The probability of a complete configuration is always the Mobius transform of the inclusion minors, equivalently the signed complete-event determinant. The parameter path is affine in the correlation kernel. No rare event, three-point event, Fisher term, or conditional acceleration is removed.

The new theorem is an author proof and has not been independently reviewed. The accepted inputs are used only in their frozen scope:

1. PR53 Theorem EW: strict exponentially weighted Fourier half-period families have a true-rate analytic description and quartic-strengthened concavity in some neighborhood of the parity-decoupled point.
2. PR34's quantitative constant-centered theorem: for a real mean-zero direction `g` and every nonzero Fourier coefficient, the constant-centered radial line has a `(4/3)|g_hat(k)|^4 t^4` concavity correction on its entire legal interval.

The purpose here is not to reprove either result. It is to combine the uniform analytic machinery behind EW with the strict radial curvature margin away from zero, obtaining one neighborhood in the **center symbol** that covers a prescribed large compact interval of the parameter.

## 1. Notation and theorem

For `beta>0`, let

```text
A_beta={u:T->C : ||u||_beta=sum_{j in Z} exp(beta|j|)|u_hat(j)|<infinity}.
```

This is a Banach algebra, and `||u||_infinity<=||u||_beta`.

Fix a real number `0<mu<1` and a real `g in A_beta` satisfying

```text
g(theta+1/2)=-g(theta),
g!=0.                                                    (1.1)
```

Thus `g_hat(j)=0` for even `j`, including `j=0`. Fix an odd `k` with `g_hat(k)!=0` and put

```text
lambda_k=|g_hat(k)|^4>0.                               (1.2)
```

Let `T>0` be such that the constant-centered radial chord is uniformly strict:

```text
delta_T=inf_{theta, |t|<=T}
        min{mu+t g(theta),1-mu-t g(theta)}>0.          (1.3)
```

### Theorem CT (compact radial tube)

There is `rho=rho(beta,mu,g,k,T)>0` such that, whenever real `c in A_beta` satisfies

```text
c(theta+1/2)=c(theta),
integral_T c=mu,
||c-mu||_beta<rho,                                    (1.4)
```

the full path `c+t g` is strictly legal for `|t|<=T` and

```text
t -> h(c+t g)+(2/3)lambda_k t^4                      (1.5)
```

is concave on `[-T,T]`.

Consequently, for distinct `t_0,t_1 in [-T,T]`, `0<q<1`, and `m=(1-q)t_0+q t_1`,

```text
h(c+m g)-(1-q)h(c+t_0g)-q h(c+t_1g)
 >=(2/3)lambda_k[(1-q)t_0^4+q t_1^4-m^4]>0.          (1.6)
```

The parameter interval in this theorem is not small: it is any prescribed compact subinterval of the strict radial legal interval. What is small is the transverse displacement of the half-period-even center from the constant symbol. The path generally does not pass through a constant symbol once `c` is nonconstant.

## 2. Uniform analytic entropy-rate tube around a compact strict chord

The proof needs a joint regularity statement in the center perturbation and the path parameter. The accepted EW proof treats one analytic parameter near one strict center. The next lemma is its compact-family and Banach-parameter form.

Let

```text
f_t^0=mu+t g,        |t|<=T.                           (2.1)
```

For a finite interval `Lambda` and zero set `Z subset Lambda`, write

```text
M_{t,Lambda,Z}=K_{f_t^0}|_Lambda-I_Z.                 (2.2)
```

### Lemma 2.1 (uniform weighted event inverses on the radial compactum)

There are `a in (0,beta)` and `B<infinity` such that

```text
sup_{|t|<=T,Lambda,Z} ||M_{t,Lambda,Z}^{-1}||_a<=B,  (2.3)
```

where

```text
||A||_a=max{sup_i sum_j exp(a|i-j|)|A_ij|,
             sup_j sum_i exp(a|i-j|)|A_ij|}.          (2.4)
```

#### Proof

The pointwise margin (1.3) implies, as an operator inequality on every finite compression,

```text
delta_T I<=K_{f_t^0}|_Lambda<=(1-delta_T)I.           (2.5)
```

For every `Z`, the signed accretivity argument from PR53 gives

```text
||M_{t,Lambda,Z}^{-1}||<=delta_T^{-1}.                (2.6)
```

Indeed, with `S=Z^c` and `J=I_S direct-sum(-I_Z)`, the cross terms in `v*J Mv` are purely imaginary and

```text
Re(v*J Mv)
 =v_S*K_SS v_S+v_Z*(I-K_ZZ)v_Z
 >=delta_T||v||^2.                                    (2.7)
```

This covers every complete word, regardless of its probability.

Choose `W` so large that

```text
T sum_{|j|>W}|g_hat(j)|<delta_T/4.                    (2.8)
```

Let `f_t^(W)` be the Fourier truncation of `f_t^0` and set

```text
B_{t,Z}=K_{f_t^(W)}|_Lambda-I_Z.
```

The difference from `M_{t,Lambda,Z}` has operator norm below `delta_T/4`, uniformly in `t,Lambda,Z`. Hence all singular values of `B_{t,Z}` are at least `eta=3delta_T/4`, while `||B_{t,Z}||<1`. The polynomial inverse identity

```text
B_{t,Z}^{-1}=sum_{r>=0}B_{t,Z}(I-B_{t,Z}^2)^r        (2.9)
```

and the bandwidth `W` show that its entries decay geometrically away from the diagonal, uniformly in `t,Lambda,Z`. Choosing

```text
a_0=min{beta/2,-log(1-eta^2)/(8W)}                   (2.10)
```

gives a finite uniform bound

```text
sup_{t,Lambda,Z}||B_{t,Z}^{-1}||_{a_0}<=C.           (2.11)
```

The weighted tail of `f_t^0-f_t^(W)` is bounded by

```text
T sum_{|j|>W}exp(a_0|j|)|g_hat(j)|
 <=T exp(-(beta-a_0)W)||g||_beta.                     (2.12)
```

Enlarge `W` if necessary so that the product of (2.11) and (2.12) is at most `1/2`. The weighted Schur norm is submultiplicative, so the Neumann identity

```text
M_{t,Lambda,Z}^{-1}
 =[I+B_{t,Z}^{-1}(M_{t,Lambda,Z}-B_{t,Z})]^{-1}
   B_{t,Z}^{-1}                                       (2.13)
```

proves (2.3), with `a=a_0`. QED.

### Lemma 2.2 (joint analytic rate near the whole radial compactum)

Let `E_beta` be the real closed subspace of `A_beta` consisting of half-period-invariant, mean-zero functions. There is `rho_0>0` such that

```text
F(u,t)=h(mu+u+t g)                                    (2.14)
```

is jointly real analytic for

```text
u in E_beta, ||u||_beta<rho_0, |t|<T+rho_0,           (2.15)
```

where the displayed parameter set is understood after reducing `rho_0` so that all real symbols in a neighborhood of `[-T,T]` are strict. More precisely, every point of `{0}x[-T,T]` has a common complex Banach neighborhood, and finitely many such neighborhoods cover the compact set. The derivatives `partial_t^j F`, in particular `j<=4`, are jointly continuous on a real neighborhood of `{0}x[-T,T]`.

#### Proof

Fix a real `t_* in [-T,T]`. Lemma 2.1 gives a bound `B` for every complete-event inverse at `f_{t_*}^0`, in the same weighted Schur norm. For complex `u` and `z-t_*` satisfying

```text
||u||_a+|z-t_*|||g||_a<(2B)^{-1},                    (2.16)
```

the event matrix is

```text
M(u,z)=M_{t_*,Lambda,Z}+K_{u+(z-t_*)g}|_Lambda,
```

and the weighted Neumann series gives

```text
sup_{Lambda,Z}||M(u,z)^{-1}||_a<=2B.                 (2.17)
```

The radius is independent of the word and volume.

For a future word `x=(x_1,...,x_r)`, the exact signed-event Schur complement gives

```text
q_{r,u,z}(x)
 =P_{u,z}(X_0=1|X_1...X_r=x)
 =f_hat(0)-b_r(u,z)M_{r,x}(u,z)^{-1}d_r(u,z).         (2.18)
```

For complex parameters this is only the holomorphic continuation of the determinant ratio; positivity is used only on the real strict slice. The weighted inverse estimate implies, by the same near/far block resolvent identity as in accepted Theorem EW,

```text
sup_x |q_{R,u,z}(x)-q_{r,u,z}(x_1,...,x_r)|
 <=C exp(-a_1 r),                                     (2.19)
```

uniformly in a smaller polydisc and in `R>r`. No word is discarded. Cauchy's formula gives the same estimate for any fixed finite number of parameter derivatives.

Thus the conditionals converge in one fixed weaker Holder norm to a Banach-holomorphic limit `q_{u,z}`. On the real slice, the pointwise spectral margin and signed accretivity bound keep `q_{u,t}` uniformly away from zero and one. Hence

```text
G_{u,t}(1x)=q_{u,t}(x),
G_{u,t}(0x)=1-q_{u,t}(x)                              (2.20)
```

is a positive normalized Holder `g`-function.

The finite-alphabet Ruelle operator

```text
(L_{u,z}A)(x)=sum_{a=0,1}G_{u,z}(ax)A(ax)             (2.21)
```

has, at each real baseline, the simple isolated eigenvalue `1` and a spectral gap on the fixed Holder space. Since the operator is Banach-holomorphic, a contour Riesz projection gives a holomorphic normalized eigenmeasure `nu_{u,z}` in a neighborhood of that baseline. The right-to-left finite entropy chain rule and (2.19) have a geometrically summable total replacement error, so before any differentiation one has

```text
h(mu+u+t g)=-nu_{u,t}(log G_{u,t}).                   (2.22)
```

This proves local joint analyticity. The real segment `[-T,T]` is compact, so finitely many baseline neighborhoods give one real neighborhood of `{0}x[-T,T]` and joint continuity of the stated derivatives. QED.

The argument in Lemma 2.2 is not an exchange of `d/dt` with `lim H_n/n`. Formula (2.22) is first obtained from a volume-uniform `O(1)` chain-rule error; derivatives are then taken in the limiting RPF formula.

## 3. The normalized curvature extends through the parity point

For `u in E_beta`, the symbol `mu+u` is half-period invariant, while `g` is half-period anti-invariant. Translation of the symbol by `1/2` is diagonal conjugation of every Toeplitz compression. Therefore

```text
F(u,-t)=F(u,t).                                       (3.1)
```

Evenness alone would still permit a `t^2` term. The exact parity joining removes it.

At `t=0`, the even and odd coordinate processes are independent, while their two marginals remain fixed for all `t`. Consequently, for every finite window,

```text
D(P_{n,u,t}||P_{n,u,0})
 =H_n(mu+u)-H_n(mu+u+t g).                            (3.2)
```

At the rate level, Lemma 2.2 and the right-to-left relative-entropy chain rule give

```text
R_u(t):=F(u,0)-F(u,t)
 =nu_{u,t}(log(G_{u,t}/G_{u,0})).                     (3.3)
```

Write `s=t^2`. The normalized conditional family is analytic in `s`. At `s=0`, differentiating (3.3) gives no contribution from the derivative of `nu`, because the observable is zero. The remaining term is

```text
integral sum_{a=0,1}
 G_{u,0}(ax) [partial_s G_{u,s}(ax)|_0]/G_{u,0}(ax)
 dnu_{u,0}(x)
 =integral sum_a partial_s G_{u,s}(ax)|_0 dnu_{u,0}(x)
 =0,                                                   (3.4)
```

by `G_{u,s}(0x)+G_{u,s}(1x)=1`. Thus

```text
partial_t^2 F(u,0)=0                                  (3.5)
```

for every sufficiently small real `u in E_beta`.

By joint analyticity, `partial_t^2F(u,t)` has a factor `t^2`. Define

```text
Psi(u,t)=partial_t^2F(u,t)/t^2,      t!=0,
Psi(u,0)=(1/2)partial_t^4F(u,0).                      (3.6)
```

Then `Psi` is jointly real analytic, hence continuous, on a neighborhood of `{0}x[-T,T]`.

## 4. Proof of Theorem CT

At `u=0`, the path is the constant-centered radial line `mu+t g`. The accepted PR34 quantitative theorem says that

```text
F(0,t)+(4/3)lambda_k t^4                              (4.1)
```

is concave on the entire legal interval. On the strict interval containing `[-T,T]`, Lemma 2.2 makes it twice differentiable. Therefore, for `t!=0`,

```text
partial_t^2F(0,t)+16lambda_k t^2<=0,
Psi(0,t)<=-16lambda_k.                                (4.2)
```

Taking `t->0` and using (3.6) gives the same bound at `t=0`:

```text
Psi(0,t)<=-16lambda_k,       |t|<=T.                  (4.3)
```

The set `{0}x[-T,T]` is compact and `Psi` is continuous. Hence there is `rho_1>0` such that

```text
Psi(u,t)<=-8lambda_k                                 (4.4)
```

whenever `u in E_beta`, `||u||_beta<rho_1`, and `|t|<=T`. Reduce `rho_1` further so that `||u||_infinity<delta_T/2`; then every symbol is strictly legal on the whole interval.

For `t!=0`, (4.4) gives

```text
partial_t^2F(u,t)<=-8lambda_k t^2.                    (4.5)
```

At `t=0`, (3.5) gives equality to zero. Since

```text
partial_t^2[(2/3)lambda_k t^4]=8lambda_k t^2,         (4.6)
```

the corrected function in (1.5) has nonpositive second derivative throughout an open neighborhood of the closed interval. It is therefore concave on `[-T,T]`. The Jensen form (1.6) follows by subtracting the correction. Since `t^4` is strictly convex, the final bracket in (1.6) is positive for distinct endpoints, proving strict concavity of `F`. Take `rho=min(rho_0,rho_1,delta_T/2)`. QED.

### What the compactness argument does and does not do

The proof uses a single center neighborhood that covers all `t in [-T,T]`. It is not a circular application of PR53 at each re-centered point. In fact `c+t_*g` is not half-period invariant when `t_*!=0`, so Theorem EW cannot simply be restarted there. The nonzero-parameter sign comes instead from the already proved constant-centered whole-line curvature margin and continuity of the normalized RPF curvature in the transverse center variable.

The theorem does not give a center radius uniform as `T` approaches a legal endpoint. The spectral margin and RPF neighborhoods can shrink there.

## 5. A fixed nonconstant family covering a visibly nonzero interval

Fix any `beta>0` and take

```text
mu=1/3,
g(theta)=(1/8)cos(2pi theta),
T=2.                                                   (5.1)
```

Then `g_hat(1)=1/16`, so

```text
lambda_1=1/65536,
(2/3)lambda_1=1/98304.                                (5.2)
```

For `|t|<=2`, the radial symbols `mu+t g` lie in `[1/12,7/12]`. Theorem CT supplies `rho(beta)>0`. For

```text
c_epsilon(theta)=1/3+epsilon cos(4pi theta)            (5.3)
```

one has

```text
||c_epsilon-mu||_beta=|epsilon|exp(2beta).             (5.4)
```

Thus every nonzero `epsilon` satisfying

```text
|epsilon|<min{rho(beta)exp(-2beta),1/24}              (5.5)
```

gives a nonconstant center, a strict full path on `[-2,2]`, and

```text
t -> h(c_epsilon+t g)+t^4/98304                       (5.6)
```

concave on that whole interval. The path does not pass through a constant symbol because its Fourier modes at frequencies `1` and `2` cannot simultaneously vanish. It includes, for example, a neighborhood of `t_*=1`, far from the parity-decoupled point. PR39 does not apply because the mean is `1/3`, not `1/2`.

The amplitude threshold in (5.5) is existential through `rho`; the theorem's substantive content is the prescribed interval `[-2,2]`, not an explicit tiny radius in `t`.

## 6. Exact prediction/RPF second variation at an arbitrary strict parameter

The tube theorem needed only continuity, but a direct nonzero-center attack requires the full RPF Hessian. This section derives it without suppressing the stationary-measure response.

Let `G_t` be a positive normalized Holder `g`-function on the one-sided binary shift, depending twice differentiably on `t`. Put

```text
phi=log G,
psi=dot phi,
xi=ddot phi,
(LA)(x)=sum_a G(ax)A(ax),
nu L=nu,
Pi A=A-nu(A),
R=(I-L)^(-1)Pi=sum_{n>=0}L^n Pi.                      (6.1)
```

All quantities in this section are evaluated at the same fixed `t`. Normalization gives

```text
L1=1,
L psi=0,
nu(psi)=0,
dot L(A)=L(psi A).                                    (6.2)
```

For a parameter-dependent Holder observable `A_t`, differentiating `nu_tL_t=nu_t` on the zero-mean subspace gives the exact linear-response formula

```text
d_t nu_t(A_t)=nu(dot A)+nu(psi R A).                  (6.3)
```

Indeed, `dot nu(I-L)=nu dot L`; applying this to `RA`, for which `(I-L)RA=Pi A`, proves (6.3). This is a direct spectral-gap calculation, not an invocation of a sign theorem.

Define the one-step conditional entropy observable

```text
B=-L phi,
h=nu(B),
u(B)=h,
u(RB)=0,
 u=RB.                                                 (6.4)
```

Differentiating `B=-sum_a G(ax)log G(ax)` and using `Lpsi=0` yields

```text
dot B=-L(psi phi),
ddot B=-L((xi+psi^2)phi+psi^2).                        (6.5)
```

The term `-L(psi^2)` is the full one-step conditional Fisher contribution. The remaining term in `ddot B` is the local conditional acceleration.

Differentiate `h=nu(B)` once:

```text
h'=nu(dot B)+nu(psi u).                                (6.6)
```

The Poisson equation `(I-L)u=B-h` gives, after differentiation,

```text
(I-L)dot u=dot B-h'+L(psi u).                         (6.7)
```

A particular solution is `R(dot B+L(psi u))`; the additive constant required by differentiating `nu_t(u_t)=0` disappears after multiplication by `psi`, because `nu(psi)=0`. Differentiating (6.6), applying (6.3), and using

```text
R(LA)=RA-Pi A                                         (6.8)
```

gives the exact identity

```text
boxed:
h''=nu(ddot B)+nu(xi u)
    +2nu(psi R dot B)
    +2nu(psi R(psi u))
    -nu(psi^2 u).                                     (6.9)
```

Every `R` in (6.9) includes the centering `Pi`. Formula (6.9) is the precise prediction-potential bridge at an arbitrary nonzero center. The first term alone is not the entropy curvature: the other four terms are the response of the stationary past/future distribution and include the effects that a naive conditional-entropy argument loses.

### A checkable sufficient bound

Let `||.||_H` be a Holder Banach-algebra norm, let `C_H` be its multiplication constant, and put `M=||R||_{H->H}`. Since `||u||_H<=M||B||_H`, (6.9) implies

```text
h''<=nu(ddot B)+E,                                    (6.10)
```

where

```text
E=M||xi||_infinity||B||_H
  +2M||psi||_infinity||dot B||_H
  +2C_H M^2||psi||_infinity||psi||_H||B||_H
  +M||psi||_infinity^2||B||_H.                       (6.11)
```

Therefore `sup_x ddot B(x)+E<0` is a sufficient nonzero-center curvature condition. It is deliberately not asserted to hold automatically. It keeps the conditional Fisher, acceleration, and all response terms in one explicit inequality.

## 7. Finite-state certification bridge for a compact interval

For strict `A_beta` symbol chords, the complete-event inverse estimate gives finite-future conditionals `G_t^{(r)}` satisfying, uniformly on a compact strict interval `J`,

```text
max_{j<=2}||partial_t^j(G_t^{(r)}-G_t)||_H
 <=C_J exp(-a_J r).                                   (7.1)
```

The logarithms obey the same type of estimate because all real conditionals stay uniformly away from zero. The corresponding transfer operators converge in operator norm. A contour separating the simple eigenvalue `1` from the remaining spectrum, together with the resolvent identity, gives

```text
||nu_t^{(r)}-nu_t||+||R_t^{(r)}-R_t||
 <=C'_J exp(-a'_J r).                                 (7.2)
```

Substitution in (6.9) yields a volume-independent error bound

```text
sup_{t in J}|C_r(t)-h''(t)|
 <=C''_J exp(-a''_J r),                               (7.3)
```

where `C_r` is the right side of (6.9) computed from `G_t^{(r)}`.

Because `G_t^{(r)}` depends on only `r` future bits, its invariant law and centered resolvent are finite matrices on at most `2^r` states. Thus a directed interval-arithmetic certificate

```text
sup_{t in J} C_r(t)+C''_J exp(-a''_J r)<0             (7.4)
```

proves true entropy-rate concavity on `J`. This is not finite-window extrapolation: (7.3) is a proved uniform error from the exact RPF rate formula. No such heavy interval computation was run in this round; (7.4) records a rigorous future interface and its required error term.

## 8. Balanced fermionic beam splitter: exact comparison and second-order obstruction

The accepted PR53 bridge identifies the occupation diagonal of a gauge-invariant quasifree state with the complete DPP law. Fix a strict `t_*` and set

```text
K_-=K_{c+(t_*-u)g},
K_+=K_{c+(t_*+u)g},
M=K_{c+t_*g},
V=K_g.                                                 (8.1)
```

The balanced one-particle unitary applied to the two quasifree inputs produces a quasifree output with covariance

```text
K_out(u)=[[M,uV],[uV,M]].                              (8.2)
```

Its two occupation marginals are both the DPP law with kernel `M`. Let `Q_{n,u}` be its full occupation distribution on a finite doubled window, and let `I_{n,out}(u)` be the classical mutual information between the two output layers. Then

```text
H(Q_{n,u})=2H_n(M)-I_{n,out}(u),                      (8.3)
```

and the midpoint gap has the exact decomposition

```text
2H_n(M)-H_n(K_-)-H_n(K_+)
 =I_{n,out}(u)+E_{n,occ}(u),                          (8.4)
```

where

```text
E_{n,occ}(u)=H(Q_{n,u})-H_n(K_-)-H_n(K_+).            (8.5)
```

No quantum entropy appears in these formulas.

At `u=0`, `Q_{n,0}` is the product of its two fixed marginals. Conjugating the second layer by `-I` sends `u` to `-u`, so every complete output event is even in `u`. Hence

```text
Q_{n,u}-Q_{n,0}=O(u^2),
I_{n,out}(u)=D(Q_{n,u}||Q_{n,0})=O(u^4).              (8.6)
```

For strict exponentially local symbols, the same weighted inverse/RPF argument applies after grouping the two modes at each lattice site into a four-letter alphabet. It gives the true rates

```text
h_out(u)=lim_n H(Q_{n,u})/n,
i_out(u)=2h(t_*)-h_out(u),
e_occ(u)=h_out(u)-h(t_*-u)-h(t_*+u),                  (8.7)
```

all analytic near zero, and

```text
2h(t_*)-h(t_*-u)-h(t_*+u)=i_out(u)+e_occ(u).          (8.8)
```

Equation (8.6) and the rate formula imply

```text
i_out(u)=O(u^4),
i_out''(0)=0,
e_occ''(0)=-2h''(t_*).                               (8.9)
```

Thus the always nonnegative output mutual information contributes nothing to the quadratic curvature. At second order, proving the occupation-entropy gain nonnegative is exactly as hard as proving `h''(t_*)<=0`; it is not a free consequence of output correlations. Known fermionic beam-splitter inequalities concern von-Neumann entropy of the quasifree state, whereas `e_occ` is the Shannon entropy of a fixed occupation measurement. Substituting the former for the latter changes the problem.

This does not disprove the beam-splitter route at finite separation `u`. It identifies the precise missing classical term and shows why output mutual information alone cannot propagate the local theorem away from zero.

## 9. Route comparison, failed shortcuts, and remaining gap

### Prediction/RPF route

This route supplies both the new theorem and the arbitrary-center Hessian formula. The decisive new bridge is the normalized curvature

```text
Psi(c,t)=h''(c+t g)/t^2,                              (9.1)
```

which extends through `t=0` on the half-period family. The constant-centered theorem gives a uniform negative margin for `Psi` on a whole compact interval; joint RPF analyticity transports that margin to nonconstant centers. This genuinely covers nonzero `t` without pretending that `c+t_*g` retains the even-center hypothesis.

### Beam-splitter/occupation route

The exact decomposition (8.8) remains useful for finite separations, but (8.9) shows that its manifestly nonnegative mutual-information term is quartic. The unknown occupation-entropy gain carries the entire Hessian sign. Quantum spectral entropy cannot supply it.

### Shortcuts that do not close the problem

- Re-centering at `t_*` breaks the half-period-even center condition.
- Analyticity and the fact that `t=0` is a global entropy maximum do not imply concavity.
- The true-rate deficit from `t=0` does not determine the sign of its second derivative away from zero.
- Pointwise concavity of each conditional kernel in a random future is unavailable; its acceleration and the response of the future law must remain.
- A finite negative curvature sample without the RPF error (7.3) is not a rate proof.

### Remaining open scope

Theorem CT is a tube around constant-centered radial chords. It does not cover a general exponentially local center far from every constant, does not reach legal endpoints, and does not prove the full legal interval for the PR39 example. The sign of (6.9) for arbitrary strict half-period centers, or an exact true-rate counterexample, remains open. No novelty or publication-priority judgment is made here.