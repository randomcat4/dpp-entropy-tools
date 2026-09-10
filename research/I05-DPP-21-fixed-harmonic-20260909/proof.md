# Fixed two-harmonic path: true-rate certificate and curvature reduction

All logarithms are natural. Complete DPP event probabilities are obtained from inclusion minors by Mobius inversion, equivalently by the signed event determinant. The path is affine in the correlation kernel. No event, Fisher term, conditional acceleration, or stationary-measure response is removed.

The theorem and lemmas here are author proofs and have not been independently reviewed.

## 1. The fixed object and strict legality

Set

```text
f_t(theta)=1/2+(1/4)cos(4 pi theta)+(t/8)cos(2 pi theta).
```

Put `x=cos(2 pi theta)`. Since `cos(4 pi theta)=2x^2-1`,

```text
f_t=1/4+x^2/2+(t/8)x.                                (1.1)
```

For `|t|<=3/2`, the critical point `x=-t/8` belongs to `[-1,1]`. The quadratic is convex, so

```text
min_x f_t=1/4-t^2/128>=119/512.                      (1.2)
```

Its maximum is at an endpoint:

```text
max_x f_t=3/4+|t|/8<=15/16.                          (1.3)
```

Thus

```text
119/512<=f_t<=15/16,
min(f_t,1-f_t)>=1/16.                                 (1.4)
```

Every finite compression satisfies

```text
(1/16)I<=K_t<=(15/16)I.                              (1.5)
```

The only nonzero Toeplitz coefficients are

```text
K_t(i,i)=1/2,
K_t(i,i+/-1)=t/16,
K_t(i,i+/-2)=1/8.                                    (1.6)
```

This proves strict legality independently of PR59 and on the whole requested interval.

## 2. Complete-event conditionals

For a future word `omega=(omega_1,...,omega_r)`, let `Z(omega)` be its zero set and put

```text
M_r(t,omega)=K_t|_[1,r]-I_Z.                          (2.1)
```

Its diagonal is `+1/2` at an occupied bit and `-1/2` at an empty bit; its first and second off-diagonals are `t/16` and `1/8`.

Let

```text
b_r=(t/16,1/8,0,...,0)^T,
d=(1/16,0,...,0)^T,
A=M_r'(t),
R=M_r(t,omega)^(-1).                                  (2.2)
```

The signed determinant of the joint event with site zero occupied has the same exterior sign as the future event. Schur complementation therefore gives the exact complete-event conditional

```text
q_r(t,omega)=P_t(X_0=1|X_1...X_r=omega)
            =1/2-b_r^T R b_r.                        (2.3)
```

For complex `t`, (2.3) is used only as the analytic determinant ratio. On the real legal slice it is an ordinary conditional probability.

Using `R'=-RAR` and `b_r'=d`, direct differentiation gives

```text
q_r'=-2d^T Rb_r+b_r^T RARb_r,                        (2.4)

q_r''=4d^T RARb_r-2d^T Rd
      -2b_r^T RARARb_r.                              (2.5)
```

These formulas include the full dependence of the complete future event matrix.

## 3. A configuration-uniform comparison inverse

We first work on the complex neighborhood

```text
U={z: dist(z,[1/2,3/2])<=1/8}.                        (3.1)
```

Then `|z|<=13/8`, so the first off-diagonal has modulus at most `13/128`.

Let `H_r` be the real symmetric comparison matrix with diagonal `1/2`, first off-diagonal `-13/128`, and second off-diagonal `-1/8`. It is a strictly diagonally dominant M-matrix, since an interior row has margin

```text
1/2-2(13/128)-2(1/8)=3/64>0.                         (3.2)
```

For every complex event matrix `M_r(z,omega)`, its comparison matrix dominates `H_r`. If `M_rx=e_j`, the triangle inequality gives

```text
H_r |x| <= e_j.                                      (3.3)
```

Because `H_r^{-1}` is entrywise nonnegative,

```text
|M_r(z,omega)^(-1)| <= H_r^(-1)                     (3.4)
```

entrywise.

Put

```text
rho=49/64,
C=16384/3243.                                        (3.5)
```

For a fixed column `j`, define `v_i=rho^|i-j|`. Applying `H_r` to this vector gives the following exact positive residuals; deleting boundary neighbors only increases them:

```text
distance 0:   3243/16384,
distance 1:   146619/2097152,
distance 2:   241611/134217728,
distance >=3: rho^d * 241611/78675968.               (3.6)
```

Thus

```text
H_r v >=(3243/16384)e_j.                             (3.7)
```

Multiplication by the nonnegative inverse proves

```text
boxed:
|M_r(z,omega)^(-1)_{ij}|<=C rho^|i-j|.               (3.8)
```

This estimate is simultaneous in the word and its length. No lower bound on the probability of the word is used.

## 4. Explicit remote-future error

Let `R>r>=3` and let a word of length `R` extend a word of length `r`. Partition its event matrix into the near block `N=[1,r]` and the far block `F=[r+1,R]`:

```text
M_R=[[M_N,E],[E^T,M_F]].                              (4.1)
```

Since the Toeplitz range is two, `E` touches only the last two near sites and the first two far sites. The block inverse formula gives

```text
[M_R^(-1)]_NN-M_N^(-1)
 =M_N^(-1) E S_F^(-1) E^T M_N^(-1),                 (4.2)

S_F=M_F-E^T M_N^(-1)E,
S_F^(-1)=[M_R^(-1)]_FF.                              (4.3)
```

The vector `b_r` is supported on sites one and two. With

```text
a=13/128,
b=1/8,
A0=a rho+b=1661/8192,
B0=A0+b rho=2445/8192,                               (4.4)
```

(3.8) gives

```text
||E^T M_N^(-1)b_r||_1
 <=C A0 B0 rho^(r-3).                                (4.5)
```

Using (3.8) once more on the far inverse,

```text
|q_R(z)-q_r(z)|
 <=C^3 A0^2 B0^2 rho^(2r-6).                         (4.6)
```

The exact rational inequality

```text
C^3 A0^2 B0^2
 < C0:=1033420800/1263214441                         (4.7)
```

is checked by integer arithmetic in the certificate program. Consequently

```text
boxed:
|q_R(z)-q_r(z)|<=C0 rho^(2r-6)                       (4.8)
```

throughout `U`.

Letting `R` tend to infinity gives the one-sided conditional `q_infinity`. Cauchy's formula on the radius-`1/8` disk around each real `t in [1/2,3/2]` yields, for `j=0,1,2`,

```text
|d_t^j(q_infinity-q_r)|
 <=j! 8^j C0 rho^(2r-6).                             (4.9)
```

These are uniform complete-event bounds, not average or typical-word estimates.

## 5. From finite conditional entropy to the true rate

Define

```text
h_r(t)=H(X_0|X_1,...,X_r)=H_{r+1}(f_t)-H_r(f_t).     (5.1)
```

The martingale convergence theorem for finite-alphabet conditional probabilities gives

```text
h_r(t) downarrow h(f_t).                              (5.2)
```

More precisely,

```text
h_r(t)-h(f_t)
 =E_t d(q_infinity(t)||q_r(t)),                       (5.3)
```

where `d` is binary relative entropy. By the spectral margin (1.4), every real finite or infinite conditional lies in `[1/16,15/16]`. Binary relative entropy is bounded above by binary chi-square divergence, hence

```text
d(a||b)<=(a-b)^2/[b(1-b)]
        <=(256/15)(a-b)^2.                            (5.4)
```

Combining (4.8) and (5.4), for every `r>=3`,

```text
boxed:
0<=h_r(t)-h(f_t)
 <=E_r:=(256/15)C0^2 rho^(4r-12).                    (5.5)
```

This is a true entropy-rate error bound. It does not estimate `H_n/n` by trend fitting.

## 6. Exact fixed-three-symbol certificate

Take

```text
t_-=1/2,
t_0=1,
t_+=3/2,
r=18.                                                 (6.1)
```

For an `n`-site complete event, scale the signed event matrix by `32`. At the three parameters, its entries are exact integers:

```text
diagonal: +/-16,
first off-diagonal: 1,2,3 respectively,
second off-diagonal: 4.                              (6.2)
```

If `N_n(omega)` denotes the signed integer determinant, then

```text
P_t(omega)=N_n(omega)/32^n.                           (6.3)
```

The program `code/certify_midpoint_rate_gap.py` computes every `N_n` for `n=18,19` by a fraction-free width-two determinant automaton. It verifies

```text
N_n(omega)>0,
sum_omega N_n(omega)=32^n.                           (6.4)
```

A separate small-size implementation computes all inclusion determinants and performs Mobius inversion; it agrees with (6.3) for every word and each of the three parameters through length six.

The entropy is evaluated as

```text
H_n=n log 32-(1/32^n)sum_omega N_n(omega)log N_n(omega).  (6.5)
```

Integer determinants and weights are exact. The standard-library decimal logarithm is evaluated at precision `100`; according to the `decimal`/libmpdec contract it is correctly rounded to nearest. Each logarithm is then enlarged by `10^-90`, and every subsequent positive multiplication, addition, division, and subtraction is performed separately with `ROUND_FLOOR` and `ROUND_CEILING`. Thus the reported intervals contain (6.5); there is no heuristic floating tolerance.

The program exits zero only after proving

```text
lower(h_18(1))-E_18
 -[upper(h_18(1/2))+upper(h_18(3/2))]/2
 >1/10000.                                            (6.6)
```

For the midpoint, (5.5) gives `h(f_1)>=h_18(1)-E_18`; for the endpoints, conditioning gives `h(f_t)<=h_18(t)`. Therefore (6.6) proves

```text
boxed:
h(f_1)-[h(f_{1/2})+h(f_{3/2})]/2>1/10000.            (6.7)
```

This is a strict true-rate Jensen gap in the concave direction. It is not a counterexample and does not by itself prove curvature between the three parameters.

## 7. Independent Poisson/correlation form of the RPF Hessian

This section rederives the response formula needed for the nonzero-parameter sign; it does not treat PR59 as an accepted dependency.

Let `G_t` be a positive normalized Holder `g`-function on the one-sided binary shift, and define

```text
phi=log G,
psi=dot phi,
xi=ddot phi,
(LA)(x)=sum_a G(ax)A(ax),
nu L=nu,
Pi A=A-nu(A),
R=(I-L)^(-1)Pi=sum_{n>=0}L^n Pi.                     (7.1)
```

Normalization gives

```text
L1=1,
L psi=0,
L(xi+psi^2)=0,
nu(psi)=0.                                            (7.2)
```

For a differentiable observable `A_t`, differentiation of `nu_tL_t=nu_t` gives the linear-response identity

```text
d_t nu_t(A_t)=nu(dot A)+nu(psi R A).                 (7.3)
```

Indeed, for `u=RA`, `(I-L)u=A-nu(A)` and

```text
(dot nu)(A)=(dot nu)((I-L)u)=nu(dot L u)=nu(psi u).  (7.4)
```

The entropy rate is

```text
h=-nu(phi).                                           (7.5)
```

Put `v=Rphi`. From (7.2) and (7.3),

```text
h'=-nu(psi v).                                        (7.6)
```

The Poisson equation is

```text
(I-L)v=phi-nu(phi),
nu(v)=0.                                              (7.7)
```

Differentiating it gives, up to an additive constant that disappears after multiplication by `psi`,

```text
dot v=psi+R(psi v)-Pi(psi v)+constant.               (7.8)
```

Differentiate (7.6), apply (7.3), use `nu(psi)=0`, and substitute (7.8). The exact result is

```text
boxed:
h''=-nu(psi^2)+nu((psi^2-xi)v)
    -2nu(psi R(psi v)).                               (7.9)
```

No response term has been deleted. Since the transfer operator is adjoint to the shift,

```text
nu(F L^n A)=nu((F o shift^n)A).                       (7.10)
```

Expanding the centered resolvent in (7.9), and using `nu(psi)=0`, gives the correlation form

```text
boxed:
h''=-nu(psi^2)-nu((xi+psi^2)v)
    -2sum_{n>=1}nu((psi o shift^n)psi v).             (7.11)
```

The first term is negative conditional Fisher information. The second and third terms contain the complete conditional acceleration and invariant-law response. Reverse-martingale orthogonality of `psi` alone does not sign them because `v` contains the present symbol as well as its future.

For the fixed finite-range DPP, Sections 3–4 give exponential Holder control of `G_t` and its first two derivatives uniformly on `[1/2,3/2]`. Standard Ruelle linear response therefore makes (7.9)–(7.11) absolutely convergent true-rate formulas. The remaining mathematical issue is their sign.

## 8. A fully explicit finite-memory curvature tail

The preceding Poisson formula motivates the transfer computation. There is also a direct conditional-mutual-information error formula that avoids an unquantified derivative limit.

Let

```text
d_r=h_r-h_{r+1}
   =I(X_0;X_{r+1}|X_1,...,X_r).                       (8.1)
```

Write `W=(X_1,...,X_r)`, `Y=X_{r+1}`,

```text
a(t)=q_{r+1}(t,W,Y),
b(t)=q_r(t,W),
Delta=a-b.                                             (8.2)
```

Then

```text
d_r(t)=sum_{W,Y}p_t(W,Y)d(a(t)||b(t)).                (8.3)
```

### Uniform derivative ingredients

On the real target interval, the event comparison matrix has diagonal margin `1/16`, so

```text
||M_r(t,omega)^(-1)||_infinity<=16.                  (8.4)
```

Equations (2.4)–(2.5), with

```text
||b||_1<=7/32,
||b||_infinity<=1/8,
||d||_1=1/16,
||A||_infinity<=1/8,                                 (8.5)
```

give

```text
|q_r'|<=U1:=9/8,
|q_r''|<=U2:=37/8.                                    (8.6)
```

By (4.9), if

```text
e_r=C0 rho^(2r-6),                                   (8.7)
```

then

```text
|Delta|<=e_r,
|Delta'|<=8e_r,
|Delta''|<=128e_r.                                    (8.8)
```

Let `F(x)=x log x+(1-x)log(1-x)`. On `[delta,1-delta]`, `delta=1/16`, set

```text
M2=max|F''|=256/15,
M3=max|F'''|=57344/225,
M4=max|F''''|=27656192/3375.                          (8.9)
```

The Bregman integral

```text
d(a||b)=Delta^2 int_0^1(1-s)F''(b+sDelta)ds          (8.10)
```

and two differentiations imply the uniform bounds

```text
|d(a||b)|<=A0 e_r^2,
|d_t d(a||b)|<=A1 e_r^2,
|d_t^2 d(a||b)|<=A2 e_r^2,                            (8.11)
```

where

```text
A0=M2/2,
A1=8M2+(M3 U1)/2,
A2=192M2+16M3 U1+(M4 U1^2+M3 U2)/2.                 (8.12)
```

For an `(r+1)`-site complete event, let `S=(log p)'`. The signed accretivity bound and `||K_t'||<=1/8` give

```text
|S|<=2(r+1),
|S'|<=4(r+1),
|p''/p|<=4(r+1)^2+4(r+1).                             (8.13)
```

Differentiating (8.3) and summing the positive real event weights gives

```text
boxed:
|d_r''(t)|
 <=[A2+4(r+1)A1
    +(4(r+1)^2+4(r+1))A0]e_r^2.                      (8.14)
```

Analogous bounds for `d_r` and `d_r'` are summable. Therefore

```text
h''(t)=h_R''(t)-sum_{r>=R}d_r''(t)                   (8.15)
```

uniformly on `[1/2,3/2]`.

Put `q=rho^4`. The tail in (8.14) is a quadratic polynomial in `r` times `q^r`; it has the closed exact sums

```text
sum_{r>=R}q^r=q^R/(1-q),

sum_{r>=R}r q^r
=q^R[R/(1-q)+q/(1-q)^2],

sum_{r>=R}r^2q^r
=q^R[R^2/(1-q)+2Rq/(1-q)^2
     +q(1+q)/(1-q)^3].                               (8.16)
```

Thus a directed interval upper bound for the finite conditional curvature `h_R''`, plus the explicit rational tail obtained from (8.14)–(8.16), proves a true-rate curvature sign. This is the analytic acceptance gate frozen in computation issue #74. A negative `H_n''/n` without (8.14) is not accepted.

## 9. Beam-splitter comparison: finite-block second order

For completeness, take endpoint kernels at `t_*-u` and `t_*+u`. The balanced fermionic beam splitter produces a doubled quasifree covariance

```text
K_out(u)=[[K_{t_*},uK_g],[uK_g,K_{t_*}]].            (9.1)
```

Both occupation marginals equal the DPP at `t_*`. For a fixed block of `n` original sites, write its complete occupation law as `Q_{u,n}`, the output mutual information as `I_out,n`, and the occupation-entropy gain as `E_occ,n`. The exact finite entropy identity is

```text
2H_n(t_*)-H_n(t_*-u)-H_n(t_*+u)
 =I_out,n(u)+E_occ,n(u).                              (9.2)
```

Dividing this value identity by `n` and taking the stationary entropy-rate limits gives the corresponding value identity, with rates measured per original lattice coordinate. This passage alone does not justify differentiating those limits.

At `u=0`, `Q_{0,n}` is the product of its marginals. Layer-sign conjugation sends `u` to `-u` without changing any complete occupation event. For each fixed finite block, strict positivity therefore gives

```text
Q_{u,n}-Q_{0,n}=O_n(u^2),
I_out,n(u)=D(Q_{u,n}||Q_{0,n})=O_n(u^4).              (9.3)
```

The constants here may depend on `n`. Consequently the justified finite-block second-order identities are

```text
I_out,n''(0)=0,
E_occ,n''(0)=-2H_n''(t_*).                            (9.4)
```

The output mutual information supplies no quadratic sign at this finite-block level. The corresponding assertions for the derivatives of the true rates require an additional uniform-in-volume fourth-order remainder or an analytic response bridge for the doubled output process. That bridge is not established in this section, and those true-rate derivative assertions remain INCOMPLETE. No such assertion is used in the fixed midpoint and point-curvature certificate route in Sections 6-8.

The unresolved occupation-entropy gain is classical Shannon entropy. A von-Neumann entropy inequality for the underlying quasifree state is a different entropy and cannot replace its sign.

## 10. Conclusion and remaining gap

Equation (6.7) is a fixed-amplitude, nonzero-parameter, rigorously error-controlled true entropy-rate result. Equations (7.9) and (8.15) are two exact curvature bridges. Neither proves that every point of `[1/2,3/2]` has negative curvature without the remaining sign estimate or the interval computation in #74.

Accordingly, the fixed midpoint theorem is `PROVED (AUTHOR PROOF), NOT INDEPENDENTLY REVIEWED`; the requested whole-interval curvature theorem remains `INCOMPLETE`.