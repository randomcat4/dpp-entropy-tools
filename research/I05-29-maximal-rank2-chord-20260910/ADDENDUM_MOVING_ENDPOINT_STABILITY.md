# Continuation after the maximal-chord checkpoint: uniform moving-endpoint stability

Status: **PROVED (author analytic proof); PENDING_REVIEW**. This addendum was developed after the fixed-source/quantitative 3+3 package was frozen locally and GitHub/Drive publication was attempted but unavailable. It is not an independent review of RESULT.

Unlike ordinary stability on a preassigned compact interior interval, this result covers each nearby path's **own maximal legal chord**, whose singular endpoint moves. It also handles seed laws with several complete atoms vanishing at that endpoint, as happens after adding independent spectator coordinates.

## 1. Structural theorem

Fix finite block dimensions m,n and a strict real rank-two cross-block seed

`K_0(t)=[[A_0,tB_0],[tB_0^T,C_0]]`, `B_0=U_0 V_0^T`.

Assume its maximal legal interval is `[-T_0,T_0]`, with T_0>0. At the positive endpoint suppose K_0 has a one-dimensional kernel and `I-K_0(T_0)>0`. Assume also a constant g>0 such that the exact normalized complete-law curvature satisfies

`Gamma_0(t^2):=-H_0''(t)/t^2 >= g` for 0<|t|<T_0,

with its continuous value `Gamma_0(0)=6 E_{mu_0} a_0^2 >=g`.       (1.1)

Then there is a relative-open neighborhood in the real parameters (A,C,U,V), with symmetric A,C and full-column-rank U,V, on which every path satisfies

`H''(t) <= -(g/2)t^2` on its entire strict legal interior,

`H(t)+(g/24)t^4` is concave on its entire closed maximal legal chord. (1.2)

The neighborhood has moving endpoints; it is not restricted to a common proper subinterval. The case where I-K is the simple active endpoint and K is strict there follows by complete configuration complementation. No claim is made here when the two spectral constraints are simultaneously active or when the active zero has multiplicity greater than one.

## 2. Uniform spectral and coefficient data before using entropy continuity

Let N=m+n. The positive endpoint squared is determined by the two Schur operators

`R_0=C^(-1/2) B^T A^(-1) B C^(-1/2)`,

`R_1=(I-C)^(-1/2) B^T (I-A)^(-1) B (I-C)^(-1/2)`.

These operators are used only for legality, not to replace the observed-coordinate entropy. At the seed, let rho_1>rho_2>0 be the two nonzero eigenvalues of R_0. The hypotheses say

`rho_1 > ||R_1||`, `rho_1 > rho_2`, `T_0=1/sqrt(rho_1)`.

These strict inequalities persist in a preliminary parameter neighborhood. Therefore its actual positive endpoint is continuously `T=1/sqrt(rho_1)`, remains simple and remains K-active only. Shrink the neighborhood once to obtain uniform constants

`0<kappa<=1`, `nu>0`, `0<T<=T_+`, `d=det A det C >= d_->0`,

`gamma=rho_2/rho_1 <= gamma_+<1`,

`K(0)>=kappa I`, `I-K(0)>=nu I`, `I-K(T)>=nu I`,

`max_E |a_E|<=a_bar`, `max_E |b_E|<=b_bar`.                       (2.1)

All constants exist by finite-dimensional continuity and strict marginal event invertibility. They can be replaced by rational conservative bounds. For example the event-resolvent argument in RESULT Section 6 bounds all coefficients uniformly from marginal spectral margins and factor norms; no lower bound on every endpoint atom is assumed.

For 0<=r<=1 put `t=rT`, `delta=1-r`. The affine interpolation

`K(rT)=(1-r)K(0)+r K(T)`

gives

`K(rT)>=kappa delta I`, `I-K(rT)>=nu I`.                         (2.2)

This is uniform even as some complete-event probabilities vanish at r=1.

## 3. A pointwise full-law lower bound controls every logarithm

For any strict K at the actual physical t, define the algebraic matrix

`L=K(I-K)^(-1)`.

L is generally nonaffine in t and no affine-L entropy claim is used. The DPP generating polynomial follows from the defining inclusion probabilities:

`E prod_i z_i^(X_i) = det(I-K+K diag(z))`

` = det(I-K) det(I+L diag(z))`.

Comparing its complete monomial coefficients yields

`p_K(E)=det(I-K) det L_E`.                                     (3.1)

This is also the atomic identity in Kulesza--Taskar, arXiv:1207.6083v4, equations (13), (15), (25); here the generating-polynomial argument verifies the bridge for the actual K(t).

Since L-K=K^2(I-K)^(-1) is positive semidefinite, (2.2) implies `L>=kappa delta I`. Hence for every one of the 2^N complete events, including the empty event,

`p_E(rT) >= nu^N (kappa delta)^|E| >= (kappa nu)^N delta^N`.      (3.2)

The second inequality uses kappa delta<=1 and |E|<=N. Legal probabilities are at most one. Consequently

`|log p_E(rT)| <= N[log(1/(kappa nu))+log(1/delta)]`.             (3.3)

Crucially, this bound does not presume that the other atoms have positive boundary limits. It still applies when multiple atoms vanish at the seed endpoint and acquire very small nonzero endpoint masses after perturbation.

## 4. Keep one uniform Fisher pole and bound the full acceleration sum

The full-event probability has the exact rank-two factorization

`p_full(rT)=d(1-r^2)(1-gamma r^2)`.

For 1/2<=r<1,

`|p_full'(t)| = (2dr/T)(1+gamma-2gamma r^2)`

` >= d(1-gamma)/T_+`,

while `p_full(t)<=2d delta`. Its Fisher term therefore obeys

`(p_full')^2/p_full >= c/delta`,

`c=d_-(1-gamma_+)^2/(2T_+^2)>0`.                              (4.1)

No other Fisher term is harmful. For every complete event,

`p_E''(t)=mu_E(-2a_E+12t^2 b_E)`.

Since the complete mu weights sum to one,

`sum_E |p_E''(t)| <= M:=2a_bar+12T_+^2 b_bar`.                  (4.2)

Use the exact complete Shannon curvature, not a fiber or marginal proxy:

`-H''(t)=sum_E (p_E')^2/p_E + sum_E p_E'' log p_E`.

Equations (3.3), (4.1), and (4.2) give the uniform endpoint estimate

`-H''(rT) >= c/delta - MN[log(1/(kappa nu))+log(1/delta)]`.       (4.3)

Every acceleration term is included. This proves uniform Fisher dominance over the complete logarithmic loss, including small perturbed rare atoms.

For a fully explicit choice, set

`A=MN/(kappa nu)`, `D=MN`.

The inequalities `log x<=x` and `log(1/delta)<=delta^(-1/2)` for 0<delta<=1 yield a positive uniform endpoint width

`delta_0 <= min{1/2, c/(4A), (c/(4D))^2, c/(g T_+^2)}`.          (4.4)

All these constants are positive; if desired take a smaller positive rational delta_0. For 0<delta<=delta_0,

`-H''(rT) >= c/(2delta)`,

`Gamma(t^2)=-H''(t)/t^2 >= c/(2delta T_+^2) >=g/2`.              (4.5)

The elementary bound involving delta follows, for example, because `sqrt(x)-log x` on x>=1 has its minimum at x=4 and `2-log4>0`.

## 5. Complete the moving-endpoint neighborhood

The preliminary neighborhood and delta_0 were chosen before invoking compactness of the entropy curvature. On the remaining compact region `0<=r<=1-delta_0`, all kernels and their complements are uniformly strict by (2.2). The exact normalized expression

`Gamma=E_mu[4(a-2sb)^2/q + 2(a-sb)(a-6sb)lambda(q)]`

is jointly continuous in the finite parameters and r, including r=0 because lambda(1)=1. At the seed it is at least g by (1.1). Shrinking the parameter neighborhood now gives Gamma>=g/2 uniformly on that compact part. The previously proved endpoint estimate (4.5) still applies on the smaller neighborhood. This proves (1.2) across the entire actual legal interval, not merely before its moving singular endpoint.

Evenness handles the negative endpoint, the analytic zero-point limit gives H''(0)=0, and continuity of x log x extends concavity to the closed chord. This completes the theorem.

## 6. Consequence for every fixed pair of block dimensions at least three

Take the explicit 3+3 source in RESULT, and append arbitrary fixed strict marginal DPP blocks A_* and C_* as independent spectators:

`A_seed=A0 directsum A_*`, `C_seed=C0 directsum C_*`,

with U0,V0 padded by zero rows. For any fixed m,n>=3 this is an actual rank-two path in the observed coordinates. Independence gives exact additivity of the full Shannon entropy, so its normalized curvature remains at least 1/2. The maximal endpoint remains the source's s_*; its K-nullspace is still one-dimensional and I-K is strict there. All hypotheses of the theorem apply with g=1/2.

Therefore in every fixed pair m,n>=3 there is a nonempty relative-open rank-two class satisfying

`H''(t)<=-t^2/4` throughout each member's strict maximal legal chord,

`H(t)+t^4/48` concave on its closed maximal legal chord.            (6.1)

The open class contains kernels with both marginal blocks fully correlated and every cross entry nonzero: these are obtained by small symmetric and full-column-rank factor perturbations, avoiding the finitely many polynomial equations that set an entry to zero. No spectator event is discarded in the proof. Section 3 explicitly controls every newly rare atom after this perturbation.

The radius for this arbitrary-dimensional extension is existential and depends on dimension and the chosen spectators. Only RESULT's 3+3 coefficient radius 10^-6 and matrix-factor entry radius 10^-12 are numerical radii. No dimension-uniform radius, no universal rank-two theorem, and no statement at simultaneously active or multiple spectral endpoints is asserted.

## 7. What changed after the checkpoint

The first packet established a specific maximal chord plus a quantitative 3+3 parameter box. This continuation adds a proved uniform treatment of moving simple endpoints and of other vanishing atoms. That is the missing step needed to extend a seed's whole maximal chord, rather than only a compact interior band, to fully active higher-dimensional correlated open classes. It uses no extra fixed-point entropy computation and does not rely on the outcome of any requested review or external job.
