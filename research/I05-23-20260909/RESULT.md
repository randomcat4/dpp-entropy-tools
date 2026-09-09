# I05-23 — correlated rank-two blocks, entropy transport, and rate bridge

Issue: [#50](https://github.com/randomcat4/dpp-entropy-tools/issues/50)

Frozen base: `main@9f49a75904f0f1a66e4ab62b7b49ca496051b541`.

The open PR43 author snapshot read for scope separation was
`a7da3951a8ce02839dfa27f7205a1032d6f80f50`. Nothing below treats an
open-PR assertion as a reviewed theorem. In particular, the PR43
three-point indefinite-rank-two theorem, feature Hessian, arbitrary-rank
diagonal sector, and special correlated dense `3+3` family are not premises
of the new proofs here.

## Status table

| Item | Status in this branch |
| --- | --- |
| Strict radial curvature near the decoupling point for arbitrary nonzero rank-two `B`, with an explicit finite certificate | **PROVED (author proof)**; not independently reviewed |
| Quantitative finite-block entropy deficit from a cross matching, retaining the full law | **PROVED (author proof)**; not independently reviewed |
| Exact passage of that deficit to a two-layer stationary entropy rate | **PROVED (author proof)**; not independently reviewed |
| Universal conditional-four-cycle cone for every correlated rank-two line | **INCOMPLETE** |
| General nonreversible/hidden-state entropy-curvature construction | **INCOMPLETE** |
| Whole legal chord for dense internally correlated blocks larger than two, or a strict exact counterexample | **INCOMPLETE** |

The proved statements are strictly weaker than whole-chord concavity. In
particular, a quartic entropy deficit from `t=0` is not being promoted to a
sign for `H''(t)` away from zero.

## Relation to already-reviewed repository results

The accepted `m x 2` and two-observation-coordinate-support theorems prove
the whole legal radial chord but do not cover dense rank-two couplings with
both blocks larger than two. The older R3 weak-coupling theorem concerns a
different fixed-beta path family and obtains a nondegenerate Hessian by
continuity from a diagonal product kernel. Here the cross-block radial
direction is degenerate at `t=0` (`H''(0)=0`); Theorem 1 identifies and
controls the first nonzero `t^2` curvature term directly in the complete
rank-two likelihood. No novelty or priority claim is made without a
separate literature audit.

## New results

1. Section 1 writes the complete likelihood for rank two as
   \[
   q_s(S,T)=1+s\,u(S,T)+s^2v(S,T),\qquad s=t^2,
   \]
   and proves
   \[
   H''(t)<0\quad (0<|t|\le \sqrt\delta)
   \]
   for an explicit, checkable `delta>0` whenever `B != 0`. No complete
   event and no Fisher term is removed.

2. Section 2 proves, for any matching `M` of left-right coordinates,
   \[
   H(K(0))-H(K(t))
   \ge {t^4\over 2(m+\ell)}
       \left(\sum_{(i,j)\in M}B_{ij}^2\right)^2.
   \]
   The proof uses the full relative entropy, a strong-Rayleigh stochastic
   covering martingale bound, and the exact two-point inclusion shift
   `-t^2 B_ij^2`. For a jointly stationary two-layer Toeplitz DPP this
   gives a nonzero entropy-rate deficit with an explicit boundary term.

3. Section 3 gives the exact elementary-imset certificate that would settle
   every indefinite rank-two conditional line. It also proves that pairwise
   stochastic-covering couplings do not imply the required square coupling.
   Thus the literature's data processing/coupling statement is not itself
   the missing second-order bridge.

4. Section 4 records the directed-flow linear feasibility system and the
   additional entropy-production curvature inequality that is required
   after feasibility. The target is a trajectory-specific Bochner
   inequality with normalized constant `1/2`; a channel, stationarity, data
   processing, or a modified log-Sobolev inequality alone is insufficient.

5. Section 5 isolates the general normalized finite-block hypotheses under
   which curvature, rather than only the quartic deficit, passes to an
   entropy rate. It identifies the currently missing uniform
   third-derivative/entropy-production estimate.

## Exact fixture

Run

```bash
python research/I05-23-20260909/code/verify_local_and_matching.py
```

The fixture uses rational, internally correlated `3+3` blocks and a dense
non-coordinate rank-two `B`; it enumerates all 64 complete configurations.
It is outside the structural form of PR43's special `3+3` author family.
Expected exact output is stored in
`output/verify_local_and_matching.txt`. The author run used Python 3.13.5
and SymPy 1.14.0 and exited with code zero. The host injected an unrelated
`artifact_tool` spreadsheet-warmup traceback on process startup; the saved
file is the script's exact stdout, and every script assertion passed.

This fixture checks the formulas and certificate arithmetic. It is not a
finite-sample proof of any global claim; the proofs are the symbolic
arguments below.

---

# 1 — strict local radial curvature at decoupling

## Theorem 1 (explicit rank-two local certificate)

Let `A` be an `m x m` and `C` an `ell x ell` strict real DPP kernel:
\[
0\prec A\prec I,\qquad 0\prec C\prec I.
\]
Let `B != 0` have rank two, and put
\[
K(t)=\begin{pmatrix}A&tB\\ tB^{\mathsf T}&C\end{pmatrix}.
\]
There is an explicitly computable number `delta>0` such that `K(t)` is
strict and
\[
 H''(t)<0\qquad\text{for }0<|t|\le\sqrt\delta.                 \tag{1.1}
\]
Every complete configuration and the complete Fisher term are retained.

More precisely, factor `B=UV^T` with `U,V` of full column rank two. For
complete left and right configurations `S,T`, define
\[
 X_S=A-E_{S^c},\qquad Y_T=C-E_{T^c},
\]
\[
 G_A(S)=U^{\mathsf T}X_S^{-1}U,\qquad
 G_C(T)=V^{\mathsf T}Y_T^{-1}V.
\]
Strictness makes all `X_S,Y_T` invertible. With
\[
 \mu(S,T)=p_A(S)p_C(T),
\]
put
\[
 u(S,T)=-\operatorname{tr}(G_A(S)G_C(T)),\qquad
 v(S,T)=\det G_A(S)\det G_C(T),                              \tag{1.2}
\]
\[
 \sigma^2=\sum_{S,T}\mu(S,T)u(S,T)^2.                        \tag{1.3}
\]
Then `sigma^2>0`.

The following data give one fully finite radius. Let
\[
 \varepsilon=\min\{\lambda_{\min}(A),\lambda_{\min}(C),
                    \lambda_{\min}(I-A),\lambda_{\min}(I-C)\},
 \quad \beta=\|B\|_{\mathrm{op}},
\]
\[
 U_0=\max_{S,T}|u(S,T)|,\qquad V_0=\max_{S,T}|v(S,T)|.
\]
Choose any nonzero entry `B_ij` and define
\[
 \underline\sigma^2_{ij}
 =\frac{B_{ij}^4}
 {A_{ii}C_{jj}(1-A_{ii}C_{jj})}>0.                           \tag{1.4}
\]
Set
\[
 \delta_{\rm leg}=\left(\frac{\varepsilon}{2\beta}\right)^2,
\]
\[
 \delta_0=\min\left\{\delta_{\rm leg},1,
                     \frac1{2(U_0+V_0)}\right\},              \tag{1.5}
\]
\[
 M_1=U_0+2\delta_0V_0,\qquad
 L_3=12M_1V_0+4M_1^3,                                        \tag{1.6}
\]
\[
 \delta=\min\left\{\delta_0,
              \frac{3\underline\sigma^2_{ij}}{10L_3}\right\}. \tag{1.7}
\]
Here `U_0>0`, hence `L_3>0`, so (1.7) is well-defined. For every
`0<|t|<=sqrt(delta)` one has the quantitative estimate
\[
 H''(t)\le -3\underline\sigma^2_{ij}\,t^2<0.                 \tag{1.8}
\]

For rational input, every quantity except the optional spectral norm
bounds can be calculated exactly by rational arithmetic. A rational
Gershgorin lower margin for `A,C,I-A,I-C` and the Frobenius upper bound
`||B||op^2<=||B||F^2` give a wholly rational replacement for
`delta_leg`.

## Proof

### Step 1: exact complete likelihood

Write `s=t^2`. The complete-event determinant identity gives
\[
 p_s(S,T)
 =(-1)^{m+\ell-|S|-|T|}
   \det\begin{pmatrix}X_S&tB\\tB^{\mathsf T}&Y_T\end{pmatrix}.
\]
Taking the Schur complement and then the rank-two determinant lemma,
\[
 \frac{p_s(S,T)}{p_A(S)p_C(T)}
 =\det(I_2-sG_A(S)G_C(T))
 =1+s\,u(S,T)+s^2v(S,T).                                    \tag{1.9}
\]
Call this likelihood `q_s`. Since `sum mu q_s=1`,
\[
 \mathbb E_\mu u=0,\qquad \mathbb E_\mu v=0.                 \tag{1.10}
\]

The left and right marginal kernels remain exactly `A` and `C`. Therefore
\[
 H(K(t))=H(A)+H(C)-I(s),                                     \tag{1.11}
\]
where
\[
 I(s)=D(p_s\Vert\mu)
     =\sum_{S,T}\mu(S,T)q_s(S,T)\log q_s(S,T).                \tag{1.12}
\]
This is an identity for the full complete law, not a projected statistic.

### Step 2: the first score cannot vanish

For a nonzero entry `B_ij`, let
\[
 Z_{ij}(S,T)=\mathbf 1_{\{i\in S,j\in T\}}.
\]
Under `mu`, this is Bernoulli with mean
\[
 a_{ij}=A_{ii}C_{jj}\in(0,1).
\]
By the defining DPP inclusion formula,
\[
 \mathbb P_s(i\in X_L,j\in X_R)
 =\det\begin{pmatrix}A_{ii}&\sqrt{s}B_{ij}\\
                      \sqrt{s}B_{ij}&C_{jj}\end{pmatrix}
 =A_{ii}C_{jj}-sB_{ij}^2.                                   \tag{1.13}
\]
Differentiating at zero and using (1.9),
\[
 \mathbb E_\mu[Z_{ij}u]=-B_{ij}^2.                           \tag{1.14}
\]
Together with `E_mu u=0`, Cauchy--Schwarz gives
\[
 B_{ij}^4
 \le \operatorname{Var}_\mu(Z_{ij})\,\mathbb E_\mu u^2
 =a_{ij}(1-a_{ij})\sigma^2.                                  \tag{1.15}
\]
Thus
\[
 \sigma^2\ge\underline\sigma^2_{ij}>0.                       \tag{1.16}
\]

This argument also explains why a finite event cannot be discarded: one
two-point inclusion is used only to certify that the score of the complete
law is nonzero.

### Step 3: full relative-entropy derivatives

From (1.12), normalization, and `q_s>0`,
\[
 I'(s)=\mathbb E_\mu[q_s'\log q_s],
\]
\[
 I''(s)=\mathbb E_\mu\left[q_s''\log q_s+
                         \frac{(q_s')^2}{q_s}\right],         \tag{1.17}
\]
\[
 I'''(s)=\mathbb E_\mu\left[
             3\frac{q_s'q_s''}{q_s}
             -\frac{(q_s')^3}{q_s^2}\right].                 \tag{1.18}
\]
The second term in (1.17) is the complete Fisher term. At zero,
\[
 I(0)=I'(0)=0,\qquad I''(0)=\sigma^2.                         \tag{1.19}
\]

For `0<=s<=delta_0`, (1.5) and `s<=1` imply
\[
 |su+s^2v|\le s(U_0+V_0)\le\frac12,
\]
so `q_s>=1/2`. Also
\[
 |q_s'|\le M_1,\qquad |q_s''|\le2V_0.
\]
Equation (1.18) therefore yields
\[
 |I'''(s)|\le12M_1V_0+4M_1^3=L_3.                            \tag{1.20}
\]

### Step 4: convert the `s` information curvature to the true `t` path

Define
\[
 J(s)=2I'(s)+4sI''(s).
\]
By (1.11),
\[
 H''(t)=-J(t^2).                                              \tag{1.21}
\]
Moreover `J(0)=0` and
\[
 J'(s)=6I''(s)+4sI'''(s).                                    \tag{1.22}
\]
Using (1.19)--(1.20),
\[
 I''(s)\ge\sigma^2-L_3s,
\]
and hence
\[
 J'(s)\ge6\sigma^2-10L_3s
       \ge3\underline\sigma^2_{ij}
 \quad(0\le s\le\delta).                                     \tag{1.23}
\]
Thus
\[
 J(s)\ge3\underline\sigma^2_{ij}s>0\quad(s>0).               \tag{1.24}
\]
Weyl's inequality and `sqrt(delta)<=epsilon/(2 beta)` give
`K(t) >= epsilon I/2` and `I-K(t) >= epsilon I/2`; the path is strict.
Combining (1.21) and (1.24) proves (1.1) and (1.8). ∎

## Scope

This theorem covers dense, non-coordinate, internally correlated blocks of
arbitrary sizes, but only on a certified neighborhood of `t=0`. It neither
uses nor reproves PR43's special correlated `3+3` family. It does not imply
whole-chord concavity.

---

# 2 — matching entropy gap and an exact stationary entropy-rate bridge

This route deliberately proves a weaker statement than radial curvature.
It gives a quantitative entropy loss from the decoupled point on the whole
legal chord, and then passes that loss to an entropy rate. It does **not**
turn data processing or mutual-information monotonicity into a claim about
`H''`.

## Lemma 2.1 (SCP martingale moment bound)

Let `mu` be a strict strong-Rayleigh law on `{0,1}^N`. If
`F:{0,1}^N -> R` is 1-Lipschitz in Hamming distance, then for every real
`lambda`,
\[
 \log\mathbb E_\mu
 \exp\{\lambda(F-\mathbb E_\mu F)\}
 \le\frac N2\lambda^2.                                      \tag{2.1}
\]

### Proof

Reveal the coordinates in a fixed order and let
\[
 M_k=\mathbb E_\mu[F\mid X_1,\ldots,X_k].
\]
Strong-Rayleigh measures and all their conditionalizations have the
stochastic covering property. Given a history through coordinate `k-1`,
the conditional laws of the remaining coordinates under `X_k=0` and
`X_k=1` admit a coupling in which the remaining configurations differ in
at most one bit. Including coordinate `k`, the two full configurations
differ in at most two bits. Thus the two possible conditional values of
`M_k` differ by at most two.

Conditioned on the past, `M_k-M_{k-1}` has mean zero and lies in an interval
of length at most two. Hoeffding's lemma gives
\[
 \mathbb E[e^{\lambda(M_k-M_{k-1})}\mid X_1,\ldots,X_{k-1}]
 \le e^{\lambda^2/2}.
\]
Iterating over all `N` coordinates proves (2.1). ∎

The literature bridge used here is precise: determinantal laws are strong
Rayleigh, and strong Rayleigh implies stochastic covering. Pairwise
negative correlation alone would not justify the martingale coupling.

## Lemma 2.2 (entropy variational inequality)

For probability laws `P<<mu` and any real random variable `F`,
\[
 D(P\Vert\mu)\ge
 \lambda\{\mathbb E_PF-\mathbb E_\mu F\}
 -\log\mathbb E_\mu e^{\lambda(F-\mathbb E_\mu F)}
                                                               \tag{2.2}
\]
for every real `lambda`.

### Proof

Tilt `mu` by the density proportional to
`exp(lambda(F-E_mu F))` and apply nonnegativity of the relative entropy of
`P` from the tilted law. ∎

## Theorem 2.3 (finite cross-matching entropy deficit)

Let `A` and `C` be strict real finite DPP kernels and let
\[
 K(t)=\begin{pmatrix}A&tB\\tB^{\mathsf T}&C\end{pmatrix}
\]
be legal at the displayed value of `t`, with left size `m` and right size `ell`.
Let `M` be a matching in the bipartite support of `B`: no two selected
pairs share a left or right coordinate. Put
\[
 W_M=\sum_{(i,j)\in M}B_{ij}^2,\qquad N=m+\ell.
\]
Then
\[
 H(K(0))-H(K(t))
 \ge\frac{t^4W_M^2}{2N}.                                    \tag{2.3}
\]
If `B!=0`, choosing one nonzero edge makes the inequality strict for every
legal `t!=0`.

### Proof

Let `P_t` be the complete joint law and
\[
 \mu=P_0=p_A\otimes p_C.
\]
The marginal laws of the two blocks do not change with `t`, so
\[
 H(K(0))-H(K(t))
 =D(P_t\Vert\mu).                                            \tag{2.4}
\]
The baseline `mu` is a product of two determinantal laws and is therefore
strong Rayleigh.

For the chosen matching define
\[
 Z_M=\sum_{(i,j)\in M}
       \mathbf1_{\{i\in X_L\}}\mathbf1_{\{j\in X_R\}}.
\]
Because the pairs are vertex-disjoint, changing one occupancy bit changes
`Z_M` by at most one. Hence Lemma 2.1 applies. For each selected edge,
the exact DPP inclusion identity is
\[
 \mathbb E_{P_t}[X_iX_j]
 =A_{ii}C_{jj}-t^2B_{ij}^2.
\]
Consequently
\[
 \mathbb E_{P_t}Z_M-\mathbb E_\mu Z_M=-t^2W_M.               \tag{2.5}
\]
Apply (2.2), then (2.1), with `lambda=-t^2W_M/N`:
\[
\begin{aligned}
 D(P_t\Vert\mu)
 &\ge -\lambda t^2W_M-\frac N2\lambda^2\\
 &=\frac{t^4W_M^2}{2N}.
\end{aligned}
\]
Together with (2.4), this proves (2.3). The argument uses a statistic only
as a variational test of the full relative entropy; no complete event is
deleted or replaced. ∎

## Theorem 2.4 (two-layer stationary entropy-rate deficit)

Let a real DPP on `Z x {L,R}` be stationary under simultaneous cell shifts,
with block Toeplitz kernel
\[
 {\cal K}_t=
 \begin{pmatrix}{\cal A}&t{\cal B}\\
                 t{\cal B}^{\mathsf T}&{\cal C}\end{pmatrix},
\qquad {\cal B}_{i,j}=b_{j-i},
\]
assume every finite restriction of the two diagonal blocks is strict, and
suppose `t` is in a legal interval. Let `H_n(t)` be the entropy of the
restriction to cells `1,...,n` in both layers, and
\[
 h(t)=\lim_{n\to\infty}\frac{H_n(t)}n
\]
its entropy rate per cell. For every fixed offset `d`,
\[
 h(0)-h(t)\ge\frac{t^4|b_d|^4}{4}.                           \tag{2.6}
\]
In particular, if the cross block is not zero, `t=0` is a strict global
maximizer of the entropy rate along the legal radial chord.

### Proof

For `n>|d|`, match each left coordinate `i` for which both
`i` and `i+d` lie in the window to the right coordinate `i+d`.
There are
\[
 q_n=n-|d|
\]
such disjoint pairs, and
\[
 W_n=q_n|b_d|^2,\qquad N_n=2n.
\]
Theorem 2.3 gives the exact finite-boundary estimate
\[
 \frac{H_n(0)-H_n(t)}n
 \ge \frac{t^4(n-|d|)^2|b_d|^4}{4n^2}.                       \tag{2.7}
\]
A stationary finite-alphabet process has
`h(t)=lim_n H_n(t)/n` by block-entropy subadditivity. Taking the limit in
(2.7) proves (2.6). ∎

## What this does and does not transfer

The finite-to-rate passage is valid because the matching has asymptotic
density one and (2.7) includes the explicit boundary remainder
`|d|/n`. Repeating one finite sample by direct sums would instead create
a different block-i.i.d. process and would not establish (2.6) for the
original stationary law.

Equation (2.6) is a quartic deficit. A function can have such a deficit
from zero while failing to be concave elsewhere. Thus this theorem is not
being used as a substitute for the required second-derivative sign.

---

# 3 — conditional four-cycles: exact bridge and exact limitation

## 3.1 Elementary conditional four-cycles

For distinct `i,j` and
`R subseteq [n]\{i,j}`, define
\[
 e^{ij\mid R}
 =\delta_R-\delta_{R\cup i}-\delta_{R\cup j}
  +\delta_{R\cup\{i,j\}}.                                   \tag{3.1}
\]
For any set function `f`,
\[
 \langle e^{ij\mid R},f\rangle
 =f(R)-f(Ri)-f(Rj)+f(Rij).                                  \tag{3.2}
\]
Thus the cone generated by the vectors (3.1) is dual to the cone of
supermodular set functions. This is the elementary-imset cone.

For a strict determinantal complete law `p`, conditioning every coordinate
outside `{i,j}` leaves a two-coordinate strong-Rayleigh law. Its two
coordinates are negatively correlated. Equivalently,
\[
 p(R)p(Rij)\le p(Ri)p(Rj),                                  \tag{3.3}
\]
and hence
\[
 \langle e^{ij\mid R},\log p\rangle
 =\log\frac{p(R)p(Rij)}{p(Ri)p(Rj)}\le0.                     \tag{3.4}
\]

## 3.2 The exact certificate for an indefinite rank-two line

Let
\[
 D=aa^{\mathsf T}-bb^{\mathsf T}
\]
and suppose `K+zD` stays strict on an interval. For every complete event,
rank-one multilinearity gives
\[
 p_{K+zD}=p+zr+z^2c.                                         \tag{3.5}
\]
Introduce the positive rectangle
\[
 K(x,y)=K+xaa^{\mathsf T}+ybb^{\mathsf T}
\]
and let
\[
 m=\left.\partial_x\partial_y p_{K(x,y)}\right|_{x=y=0}.
\]
There are no `x^2` or `y^2` determinant terms, so substituting
`x=z,y=-z` yields
\[
 c=-m.                                                       \tag{3.6}
\]

If one can solve the finite conic system
\[
 m=\sum_{i<j}\sum_{R\subseteq[n]\setminus\{i,j\}}
       w_{ij\mid R}e^{ij\mid R},
 \qquad w_{ij\mid R}\ge0,                                   \tag{3.7}
\]
then (3.4) and (3.6) imply
\[
 \langle c,\log p\rangle\ge0.                               \tag{3.8}
\]
Using `p''=2c`, the complete entropy curvature is
\[
 H''(z)
 =-\sum_\omega\frac{(p'_\omega)^2}{p_\omega}
  -2\langle c,\log p\rangle\le0.                             \tag{3.9}
\]
Both the acceleration term and the full Fisher sum are present.

For rational `K,a,b`, (3.7) is a rational linear feasibility problem with
`2^n` equations and
\[
 {n\choose2}2^{n-2}
\]
nonnegative variables. A feasible proof is a rational weight table.
Infeasibility requires a rational Farkas vector `f` satisfying
\[
 \langle e^{ij\mid R},f\rangle\ge0\quad\text{for every face},
 \qquad \langle m,f\rangle<0.                               \tag{3.10}
\]
A floating LP status is neither kind of certificate.

The universal assertion that (3.7) always holds is **INCOMPLETE**. The
three-coordinate formula in open PR43 is an author claim under review and
is not imported here as a premise.

## 3.3 Projection/hidden-state reduction and its missing square

A rank-one Loewner increment of a positive contraction can be represented
by adding one orthogonal direction in a projection dilation. Lyons'
stochastic-domination theorem, and the later strong-Rayleigh stochastic
covering property, provide pairwise monotone couplings for nested
subspaces.

The four-cycle certificate needs more. For the four projection laws
associated with
\[
 H,\quad H\oplus u,\quad H\oplus v,\quad H\oplus u\oplus v,
\]
one needs a single square coupling supported on quadruples
\[
 (R,\ R\cup i,\ R\cup j,\ R\cup\{i,j\}),\qquad i\ne j.       \tag{3.11}
\]
Its face masses would be the weights in (3.7). Pairwise couplings along
the four edges of the square do not automatically glue to (3.11).

### Proposition 3.1 (pairwise covering is insufficient)

On the Boolean lattice of `{1,2}`, set
\[
 \mu_{00}=\delta_\varnothing,\quad
 \mu_{10}=\delta_{\{1\}},\quad
 \mu_{01}=\delta_{\{1\}},\quad
 \mu_{11}=\delta_{\{1,2\}}.                                 \tag{3.12}
\]
Each upper law stochastically covers the adjacent lower law:
\[
 \mu_{10}\triangleright\mu_{00},\quad
 \mu_{01}\triangleright\mu_{00},\quad
 \mu_{11}\triangleright\mu_{10},\quad
 \mu_{11}\triangleright\mu_{01}.                             \tag{3.13}
\]
Nevertheless there is no square coupling of the form (3.11).

#### Proof

The bottom and top are forced to be `empty` and `{1,2}`. A square with
these endpoints has the two distinct middle sets `{1}` and `{2}`. In
(3.12), both prescribed middle marginals are the point mass at `{1}`.
Contradiction. ∎

This is a limitation of the proposed inference, not a counterexample to
(3.7) for DPP rectangles. It proves that the literature's pairwise
stochastic covering theorem cannot by itself supply the missing
second-order certificate.

## 3.4 Numerical diagnostic and corrected interpretation

An initial full-row floating equality solve occasionally reported
`infeasible` for projection rectangles. The right-hand side was displaced
from the exact face-column space by roundoff of order `1e-15`; the
overdetermined equality solver treated that displacement as infeasibility.
After restricting to an independent row basis, those same instances were
feasible to numerical tolerance.

Therefore no numerical disproof is claimed. The only admissible next
outcomes are an analytic construction of (3.7), a rational feasible table
for a scoped family, or an exact rational Farkas witness (3.10).

---

# 4 — nonreversible stationary flow and entropy-curvature interface

This section separates three statements that must not be conflated:

1. a positive stationary directed flow exists;
2. the flow realizes the exterior degrees `1` and `2`;
3. entropy production has the second-order decay required by the true
   `t`-curvature.

Only the conjunction of all three can prove radial entropy concavity by
this route.

## 4.1 Exact directed-flow feasibility system

Let the visible right-block configuration space be a finite set `Omega`
and let `mu_x>0` be its stationary target law. For every ordered pair
`x!=y`, use the stationary flow
\[
 r_{xy}=\mu_x q_{xy}\ge0                                    \tag{4.1}
\]
as unknown. Stationarity is the balance system
\[
 \sum_{x\ne y}r_{xy}=\sum_{z\ne y}r_{yz}
 \qquad(y\in\Omega).                                         \tag{4.2}
\]
The adjoint generator acting on densities relative to `mu` is
\[
 (L^\dagger f)(y)
 =\frac1{\mu_y}\sum_{x\ne y}r_{xy}\{f(x)-f(y)\}.              \tag{4.3}
\]

For a rank-two factorization, vectorize the three entries of
`G_C=(G_11,G_12;G_12,G_22)` and put `d=det G_C`.
The exact exterior scaling equations are
\[
 L^\dagger G_{11}=-G_{11},\quad
 L^\dagger G_{12}=-G_{12},\quad
 L^\dagger G_{22}=-G_{22},\quad
 L^\dagger d=-2d.                                            \tag{4.4}
\]
Equivalently, for each state `y`,
\[
 \sum_{x\ne y}r_{xy}\{g_k(x)-g_k(y)\}
 =-\mu_yg_k(y)\quad(k=1,2,3),                                \tag{4.5}
\]
\[
 \sum_{x\ne y}r_{xy}\{d(x)-d(y)\}
 =-2\mu_yd(y).                                               \tag{4.6}
\]

For rational `mu,g_k,d`, (4.1)--(4.6) are a rational linear system
`Ar=b, r>=0`. A feasibility certificate is a rational nonnegative flow
table satisfying every equality. By Farkas' lemma, infeasibility is
certified by a rational vector `y` with
\[
 A^{\mathsf T}y\ge0,\qquad b^{\mathsf T}y<0.                 \tag{4.7}
\]
A floating LP status is only a scout.

Issue #45 already owns the literal fixed PR43 directed LP, so this branch
does not duplicate that computation.

## 4.2 Exact entropy trajectory and the missing curvature inequality

Let
\[
 f_s=1-s\,a+s^2b,\qquad
 a=\operatorname{tr}(G_AG_C),\quad b=\det G_A\det G_C.
\]
If (4.4) holds and `s=s_*e^{-tau}`, then
\[
 \partial_\tau f_s=L^\dagger f_s.                            \tag{4.8}
\]
Define the full relative entropy
\[
 {\cal I}(\tau)=\langle f_s,\log f_s\rangle_\mu.
\]
Stationarity gives
\[
 {\cal I}'=\langle L^\dagger f_s,\log f_s\rangle_\mu,         \tag{4.9}
\]
\[
 {\cal I}''
 =\langle (L^\dagger)^2f_s,\log f_s\rangle_\mu
  +\left\langle\frac{(L^\dagger f_s)^2}{f_s}\right\rangle_\mu.
                                                                    \tag{4.10}
\]
The second term is the complete Fisher term.

Writing the same mutual information as `I(s)`, the true affine kernel path
satisfies
\[
 -H''(t)=2I'(s)+4sI''(s)
        =\frac2s\{2{\cal I}''+{\cal I}'\}.                   \tag{4.11}
\]
Thus feasibility of (4.1)--(4.6) is still insufficient. One must prove,
on every legal density in the trajectory,
\[
 2{\cal I}''+{\cal I}'\ge0.                                  \tag{4.12}
\]

Let the entropy production be
\[
 {\cal D}(\tau)=-{\cal I}'(\tau).
\]
Then (4.12) is exactly
\[
 {\cal I}''\ge\frac12{\cal D},
 \qquad\text{equivalently}\qquad
 {\cal D}'\le-\frac12{\cal D}.                               \tag{4.13}
\]
This is a trajectory-specific Bochner/entropy-curvature estimate in the
normalization where degree-one features have eigenvalue `-1`. A modified
log-Sobolev inequality instead compares `D` with `I`; it does not by itself
compare `-D'` with `D`. Data processing supplies only `D>=0`. Neither
statement implies (4.13).

The discrete entropic-Ricci and Bakry--Emery literature is relevant at
this exact point: it develops second-entropy-derivative or Bochner
inequalities for Markov semigroups. Most standard formulations are
reversible, whereas the present search is explicitly nonreversible, so a
citation to that theory is a template for the missing estimate, not a
black-box proof.

## 4.3 Hidden-state extension: exact interface

Let `tildeOmega` be a finite hidden extension, `tildeMu` a positive
stationary law, `J` a prescribed lift of visible densities, and `Pi` the
visible marginalization/conditional-expectation map. To reproduce the
radial family one needs the exact intertwining
\[
 \Pi e^{\tau\widetilde L^\dagger}Jg_k=e^{-\tau}g_k,\qquad
 \Pi e^{\tau\widetilde L^\dagger}Jd=e^{-2\tau}d,              \tag{4.14}
\]
or at minimum the differentiated equations at zero together with
semigroup closure of the lifted feature space.

Merely exhibiting a Markov chain on hidden states, or merely matching one
visible marginal, does not establish (4.14). Even (4.14) does not equate
hidden and visible relative entropies; marginalization gives only data
processing. The visible trajectory must still satisfy (4.12), or a hidden
inequality must be shown to descend with the required direction and
constants.

## Status

The finite linear/certificate interface and the exact curvature target are
proved above. Existence of such a flow for every correlated DPP block, and
the required nonreversible Bochner estimate, remain **INCOMPLETE**.

---

# 5 — general finite-block to entropy-rate curvature bridge

The matching theorem in Section 2 gives an unconditional rate deficit.
Passing an actual second-derivative sign requires stronger uniform
information. This section states exactly what is enough and what remains
missing.

## Proposition 5.1 (pointwise finite concavity passes to a rate)

Let `P_t` be a stationary finite-alphabet process and let `H_n(t)` be the
entropy of its first `n` cells. If every `H_n` is concave on an interval
`J`, then
\[
 h(t)=\lim_{n\to\infty}\frac{H_n(t)}n
\]
is concave on `J`.

### Proof

For `t0,t1 in J` and `theta in [0,1]`,
\[
 \frac1nH_n((1-\theta)t_0+\theta t_1)
 \ge(1-\theta)\frac1nH_n(t_0)
    +\theta\frac1nH_n(t_1).
\]
Stationary block-entropy subadditivity gives the pointwise limits. Passing
to the limit proves the same Jensen inequality for `h`. ∎

For a stationary DPP whose infinite kernel is affine in `t`, every finite
restriction is the true affine principal submatrix. No affine `L`-path or
spectral-basis rotation enters this argument.

## Proposition 5.2 (uniform local information-curvature criterion)

Suppose the finite restrictions split into two fixed-marginal blocks and
write
\[
 H_n(t)=H_n(0)-I_n(s),\qquad s=t^2.
\]
Assume that for all `n>=n0` and `0<=s<=delta0`,
\[
 I_n''(0)\ge c\,n,\qquad |I_n'''(s)|\le L\,n                \tag{5.1}
\]
with constants `n0<infinity`, `c>0`, and `L<infinity` independent of `n`.
Then for
\[
 0\le s\le\delta:=\min\{\delta_0,3c/(10L)\},                 \tag{5.2}
\]
\[
 H_n''(t)\le-3c\,n\,t^2\quad(0<|t|\le\sqrt\delta),            \tag{5.3}
\]
and the entropy rate is concave on this neighborhood. Since the radial
path is even and `H_n'(0)=0`, one also has the normalized strict deficit
\[
 h(0)-h(t)\ge \frac c4 t^4
 \qquad(0<|t|\le\sqrt\delta).                                \tag{5.4}
\]

### Proof

Let
\[
 J_n(s)=2I_n'(s)+4sI_n''(s)=-H_n''(\sqrt{s}).
\]
Exactly as in the finite proof,
\[
 J_n'(s)=6I_n''(s)+4sI_n'''(s)
 \ge6cn-10Lns\ge3cn.
\]
Since `J_n(0)=0`, (5.3) follows for every `n>=n0`. The finitely many
smaller blocks are irrelevant to the pointwise normalized limit, so the
same limiting Jensen argument as Proposition 5.1 passes concavity to the
rate. Integrating (5.3) twice from zero gives
`H_n(0)-H_n(t)>=cn t^4/4`; division by `n` and passage to the limit proves
(5.4). ∎

## A proved extensive lower bound for the first condition

For the stationary two-layer Toeplitz setting of Theorem 2.4, let `u_n`
be the complete score at `s=0`, so
\[
 I_n''(0)=\mathbb E_{\mu_n}u_n^2.
\]
Using the matching statistic with offset `d`,
\[
 \mathbb E_{\mu_n}[u_n Z_n]=-(n-|d|)|b_d|^2.                 \tag{5.5}
\]
The SCP martingale bound (2.1) implies
\[
 \operatorname{Var}_{\mu_n}(Z_n)\le N_n=2n                  \tag{5.6}
\]
by differentiating the moment bound at zero. Cauchy--Schwarz therefore
gives
\[
 I_n''(0)
 \ge\frac{(n-|d|)^2|b_d|^4}{2n}.                            \tag{5.7}
\]
Thus the first hypothesis in (5.1) holds asymptotically with any
`c<|b_d|^4/2` when `b_d!=0`.

The second hypothesis, a uniform extensive bound on `I_n'''` (or an
equivalent entropy-production estimate), is not proved here. Bounding it
by the maximum reciprocal complete-event probability would generally be
useless because rare events can be exponentially small; those events
cannot be deleted. This is the precise remaining finite-to-rate
curvature gap.

## Boundary-remainder variant

More generally, if concave approximants `tilde H_n` satisfy
\[
 \sup_{t\in J}|H_n(t)-\widetilde H_n(t)|\le b_n,\qquad
 \frac{b_n}{n}\longrightarrow0,                             \tag{5.8}
\]
then any pointwise normalized limit of `tilde H_n` equals `h` and is
concave. The uniform error (5.8), not a finite sample, is the needed
certificate. The matching construction in Theorem 2.4 realizes this
principle directly with the explicit boundary loss `|d|/n`.

---

# Primary sources and exact bridge points

1. Russell Lyons, **Determinantal Probability Measures**, *Publications
   Mathématiques de l'IHÉS* **98** (2003), 167--212.
   DOI: `10.1007/s10240-003-0016-0`; arXiv: `math/0204325`.

   Used for the finite determinantal measure, projection dilation, and
   Loewner/nested-subspace stochastic-domination context. The present
   branch does not infer a four-way square coupling from the pairwise
   domination theorem.

2. Julius Borcea, Petter Brändén, Thomas M. Liggett,
   **Negative Dependence and the Geometry of Polynomials**,
   *Journal of the American Mathematical Society* **22** (2009),
   521--567. DOI: `10.1090/S0894-0347-08-00618-8`;
   arXiv: `0707.2340`.

   Used at the precise bridge: finite DPP laws are strong Rayleigh;
   strong-Rayleigh laws are closed under conditioning and imply the
   negative-dependence/stochastic-order properties used here.

3. Robin Pemantle, Yuval Peres,
   **Concentration of Lipschitz Functionals of Determinantal and Other
   Strong Rayleigh Measures**, *Combinatorics, Probability and Computing*
   **23** (2014), 140--160.
   DOI: `10.1017/S0963548313000345`; arXiv: `1108.0687`.

   Used for the stochastic covering consequence and its martingale
   interpretation. Lemma 2.1 is written out in full with the constants
   actually used, rather than imported as an unnamed concentration bound.

4. Takuya Kashimura, Tomonari Sei, Akimichi Takemura, Kentaro Tanaka,
   **Cones of Elementary Imsets and Supermodular Functions: A Review and
   Some New Results**, in *Harmony of Gröbner Bases and the Modern
   Industrial Society* (World Scientific, 2012), 117--152.
   DOI: `10.1142/9789814383462_0008`; arXiv: `1109.2408`.

   Used only for the exact polyhedral vocabulary: elementary imsets
   generate the cone dual to supermodular functions. The DPP sign bridge
   is independently shown in (3.3)--(3.9).

5. Jonathan Hermon, Justin Salez,
   **Modified Log-Sobolev Inequalities for Strong-Rayleigh Measures**,
   *Annals of Applied Probability* **33** (2023), 1501--1514.
   DOI: `10.1214/22-AAP1847`; arXiv: `1902.02775`.

   Relevant to entropy dissipation for chains with strong-Rayleigh
   stationary law. The branch explicitly records why a modified
   log-Sobolev estimate (`D` versus entropy) is not the required
   second-order estimate (`-D'` versus `D`).

6. Matthias Erbar, Jan Maas,
   **Ricci Curvature of Finite Markov Chains Via Convexity of the Entropy**,
   *Archive for Rational Mechanics and Analysis* **206** (2012),
   997--1038. DOI: `10.1007/s00205-012-0554-z`;
   arXiv: `1111.2687`.

   Used as the cross-domain source for Bochner/second-entropy-derivative
   methods. Its standard reversible framework is not silently applied to
   the nonreversible flow sought here.

7. Russell Lyons, Jeffrey E. Steif,
   **Stationary Determinantal Processes: Phase Multiplicity,
   Bernoullicity, Entropy, and Domination**, *Duke Mathematical Journal*
   **120** (2003), 515--575.
   DOI: `10.1215/S0012-7094-03-12032-3`;
   arXiv: `math/0204324`.

   Used for the stationary determinantal/entropy-rate setting.

8. András Mészáros, **Limiting Entropy of Determinantal Processes**,
   *Annals of Probability* **48** (2020), 2615--2643.
   DOI: `10.1214/20-AOP1435`; arXiv: `1905.11459`.

   Gives broader limiting-entropy context. No sofic approximation theorem
   is needed for the elementary one-dimensional block limit proved here.

---

# Failed or delimited routes

## 1. Universal reversible exterior scaling

Not revived. The open PR43 author packet gives a two-point inner-product
obstruction `-125/78` to the required self-adjoint eigenvalue
orthogonality. Because that packet is under independent review, this
branch cites it only as an author claim and does not make it a premise of
a new theorem.

## 2. Quasi-free quantum channel to classical occupancy kernel

Not revived. A quasi-free completely positive map does not generally
descend to a classical stochastic kernel on complete occupancy
configurations with the required exterior-degree scaling.

## 3. Data processing or mutual-information monotonicity as curvature

Rejected. Data processing yields first-order entropy decay. True radial
curvature is equivalent to
`2 Ical'' + Ical' >= 0`, or `-D' >= D/2`, which is a second-order
entropy-production inequality.

## 4. Pairwise stochastic covering as a square coupling

Disproved as a logical implication by Proposition 3.1. Four pairwise
covering relations need not admit a common face-supported grand coupling.
This does not disprove the DPP-specific four-cycle cone; that question
remains open.

## 5. Floating full-row imset LP infeasibility

Discarded as a numerical artifact. Projection-rectangle right-hand sides
computed by floating orthogonalization missed the exact face-column space
at roughly `1e-15`. An overdetermined equality solve could label that
infeasible. Independent-row solves removed the false obstruction.
No `DISPROVED` label is attached without a rational Farkas witness.

## 6. Finite replication as entropy-rate proof

Rejected. Direct-sum replication changes the process to block-i.i.d.
A valid rate passage needs all finite restrictions or an explicit uniform
boundary remainder. Theorem 2.4 supplies such a remainder for a genuine
stationary two-layer process.

## 7. Rare-event truncation for uniform third derivatives

Rejected. Bounds based on deleting small-probability configurations or
replacing `1/p` by a cutoff would remove part of the Fisher term. The
uniform `I_n'''=O(n)` condition in Proposition 5.2 remains an honest gap.
