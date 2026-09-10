# I05-29: the maximal legal chord of the dense correlated PR58 fixture

Status: **PROVED (author proof plus author exact rational finite certificate); PENDING_REVIEW**. Independent mathematical review, independent arithmetic/source binding, formal verification, and novelty are separate and are not claimed.

This is a successor to PR80, not a change to its frozen review sources. The result below concerns the PR58 joint-additive obstruction fixture, not the different PR54/PR58 fixture whose accepted corridor is 3 <= t^2 <= 15. The previous 2+2 example was already in the accepted m-by-2 concavity scope; its new purpose was the negative-fiber obstruction. Here both active blocks have three actual observed coordinates and every cross entry is nonzero.

## 1. Complete definition and the theorem

All kernels are real and the physical parameter is affine:

`K(t) = [[A,tB],[tB^T,C]]`, `B=UV^T`.

For every full configuration E of the six observed coordinates,

`p_K(E)=sum_{T superset E} (-1)^(|T|-|E|) det K_T`, `det K_empty=1`,

`H(K)=-sum_E p_K(E) log p_K(E)`, `0 log 0=0`.

Natural logarithms are used. No observed-coordinate rotation, projected entropy, quantum entropy, or affine L-path is substituted.

The reference matrices are exactly the Section 3 input of
`research/I05-23-middle-20260909/ADDENDUM_JOINT_ADDITIVE.md`
at PR58 source `89aa874c24dd5a3ea98f8474826392560b1d0397`:

```text
A0 = [[219/500,-47/1000,73/1000],
      [-47/1000,461/1000,23/1000],
      [73/1000,23/1000,43/100]]
C0 = [[231/500,1/50,-49/1000],
      [1/50,43/100,11/200],
      [-49/1000,11/200,3/5]]
U0 = [[7/40,-22/125],[339/1000,13/250],[229/500,-231/500]]
V0 = [[141/200,981/1000],[-343/1000,113/250],[187/250,577/1000]]
```

### Theorem A: one fixed maximal legal chord

Let

`a_* = 4181050254735181419359 / 2416512579905515000000`,

`b_* = 4847471688450288382004871 / 6638770823916250000000000`,

and let s_* be the root in (99/100,1) of `1-a_* s+b_* s^2=0`. Put `t_*=sqrt(s_*)`.

The entire maximal legal interval of the reference K is `[-t_*,t_*]`. It is strict inside. At either endpoint K has a one-dimensional kernel and I-K is positive definite. Exact root isolations give

```text
0.999911107034345070 < s_* < 0.999911107034345071,
0.999955552529383713 < t_* < 0.999955552529383714.
```

On this **entire maximal interval**, including its continuous boundary values,

`H(K(t)) + t^4/24` is concave.                                      (1.1)

In particular, for `0<|t|<t_*`,

`H''(t) <= -t^2/2 < 0`, and `H''(0)=0`.                            (1.2)

For distinct x,y in the closed legal interval and 0<theta<1 this gives the explicit strict concavity gap

`H(theta*x+(1-theta)*y) - theta H(x) - (1-theta)H(y)`

` >= [theta*x^4+(1-theta)*y^4-(theta*x+(1-theta)*y)^4]/24 > 0`.       (1.3)

The gap in (1.3) has the concave sign; it is not an entropy counterexample.

### Theorem B: an explicit family with moving legal endpoints

For any real 3+3 path with 0<A,C<I and rank(B)=2, use the same labeled event masks S,T=0,...,7, define its complete marginal probabilities p_A,p_C, and write

`p_K(t)(S,T)=mu(S,T) q_s(S,T)`, `mu=p_A p_C`,

`q_s=1-sa+s^2 b`, `s=t^2`.

A subscript zero denotes the reference above. Suppose each of the four bounds holds:

`max_S |p_A-p_A0| <= 10^-6`, `max_T |p_C-p_C0| <= 10^-6`,

`max_{S,T}|a-a0| <= 10^-6`, `max_{S,T}|b-b0| <= 10^-6`.             (1.4)

Then (1.1)-(1.3) hold on this path's **own entire maximal legal interval**. Its squared positive endpoint is the unique zero in (99/100,1) of its full-event q, and need not equal the reference s_*.

The family in (1.4) has a concrete matrix realization: take arbitrary symmetric A,C and arbitrary 3-by-2 U,V satisfying the entrywise bounds

`max |A-A0|, max |C-C0|, max |U-U0|, max |V-V0| <= 10^-12`.         (1.5)

Every member of this parameter box is in (1.4). Both marginal blocks remain fully correlated, U,V retain full column rank two, and every entry of B=UV^T remains nonzero. Thus this is an actual positive-dimensional dense correlated family, not just an untested sufficient interface.

## 2. The exact full-law curvature

For a strict marginal event S put `A^S=A-diag(1_{i notin S})` and similarly C^T. The complete determinant identity is

`p_K(E)=(-1)^(6-|E|) det(K-diag(1_{i notin E}))`.

It follows either by expanding the chosen diagonal entries, or directly from the stated Mobius definition. Schur complementation and `B=UV^T` give

`q_s=det(I_2-s G_A(S)G_C(T))`,

`G_A=U^T(A^S)^(-1)U`, `G_C=V^T(C^T)^(-1)V`,

`a=tr(G_A G_C)`, `b=det(G_A)det(G_C)`.                            (2.1)

All event matrices are invertible for strict marginals; Section 6 also proves a uniform inverse bound. Fixed block marginals imply both conditional cancellations and in particular `E_mu a=E_mu b=0`.

Consequently `I(t)=H(A)+H(C)-H(K(t))=E_mu[q_s log q_s]`. Define

`v=a-2sb`, `w=a-sb`, `h=a-6sb`, `z=wh`,

`lambda(q)=log(q)/(q-1)`, `lambda(1)=1`.

Differentiating the complete law, including every Fisher and acceleration term,

`I''(t)=E_mu[4t^2 v^2/q + 2(-a+6sb)log q]`.

Therefore for s>0,

`Gamma(s):=-H''(t)/t^2=E_mu[4v^2/q+2z lambda(q)]`.                 (2.2)

At s=0 the right side continuously equals `6 E_mu a^2`. Thus (2.2) is a regular normalized formula at the decoupling point; no division by a zero numerical bound is made. Also `I(t)=(t^4/2)E_mu a^2+O(t^6)`, proving H''(0)=0.

## 3. Keep the signed global moment and charge only its negative mass

The elementary integral formula

`lambda(q)=integral_0^1 [1+theta(q-1)]^(-1) dtheta`

shows positivity and strict decrease. Fix an event group G and a whole s-interval J. Sums below retain the original mu weights and are **not renormalized** when one event is handled separately. Suppose

`q_lo <= q <= q_hi`, `lambda_lo <= lambda(q) <= lambda_hi`,

`sum_G mu v^2 >= V`, `sum_G mu z >= Z`,

`N_J := sum_G mu max_{s in J} (-z(s))_+ <= N`.

Because `z lambda(q) >= lambda_lo z-(lambda_hi-lambda_lo)(-z)_+`, (2.2) gives the full signed-group bound

`Gamma_G >= 4V/q_hi+2 lambda_lo Z-2(lambda_hi-lambda_lo)N`.          (3.1)

Neither individual pairs, individual events, nor individual conditional fibers need be nonnegative. The mixed moment is kept with its true sign.

For exact interval checking only three quadratic moments are needed. Set

`M_a=sum_G mu a^2`, `M_ab=sum_G mu ab`, `M_b=sum_G mu b^2`.

Then

`sum_G mu v^2=M_a-4s M_ab+4s^2 M_b`,

`sum_G mu z=M_a-7s M_ab+6s^2 M_b`,

`-z=-a^2+7sab-6s^2b^2`.                                       (3.2)

Every minimum/maximum in (3.2), and each q extremum, is decided by its two endpoints and the quadratic vertex if that vertex lies in J. These are finitely many **exact continuum extrema**, not a grid.

## 4. Three whole-interval bounds, with the rare full event kept separately

Let e=(7,7) denote the full six-coordinate event. The following table is valid not only at the reference but throughout (1.4):

| J in s | group G | q_lo | q_hi | V | Z | N | lambda_lo | lambda_hi |
|---|---|---|---|---|---|---|---|---|
| [0,9/10] | all 64 | 1/30 | 3 | 109/200 | 109/200 | 29/250 | 1/2 | 18/5 |
| [9/10,99/100] | all 64 | 1/400 | 31/10 | 83/100 | 49/50 | 27/200 | 1/2 | 61/10 |
| [99/100,1] | the other 63 | 1/50 | 31/10 | 89/100 | 109/100 | 14/125 | 1/2 | 41/10 |

The last row is an algebraic bound for the other 63 q-polynomials on [99/100,1]. It does **not** assert K(1) is legal. Only its restriction to s<s_* is used for the DPP.

The corresponding exact right sides of (3.1) are

`8287/15000 > 1/2`,

`4177/7750 > 1/2`,

`110979/77500 > 7/5`.                                          (4.1)

The lambda constants follow from the six elementary comparisons

`log 3>1`, `log 30<87/25`, `log(31/10)>21/20`,

`log 400<6`, `log 50<4`, `log 300<6`.

For example, `lambda(1/400)=(400/399)log400<61/10` and `lambda(31/10)>1/2`. The checker encloses these six logs using the rational atanh series and a proved geometric remainder. It never evaluates floating logarithms to decide a sign.

### The rare event is not dropped

For e=(7,7), throughout (1.4) and 99/100<=s<=1, exact robust comparisons give

`b_e>0`, `a_e-2s b_e>1/4`, `|z_e|<3`,

`q_e(99/100)<1/300`, `q_e(1)<0`.                               (4.2)

Thus q_e strictly decreases to its unique root s_* in (99/100,1); before that root, `0<q_e<=1/300`. For 0<q<=1/300, the function q log(1/q) increases with q, so

`q log(1/q) <= log300/300 < 1/50`.

Keep this event's Fisher denominator with its own logarithmic term:

`phi_e=4v_e^2/q_e+2z_e lambda(q_e)`

` >= 1/(4q_e)-6 log(1/q_e)/(1-q_e)`

` > [1/4-36/299]/q_e = 155/(1196 q_e) > 0`.                    (4.3)

Hence the final part of Gamma is bounded by

`Gamma >= 110979/77500 + mu_e*155/(1196 q_e) > 1/2`.             (4.4)

This also proves Gamma tends to positive infinity at the endpoint. It does not infer a global sign from an asymptotic statement; (4.4) covers the entire final interval.

### Legality and maximality are established, not assumed

At t=0 both K and I-K are positive definite. The full-event determinant is `det K(t)=mu_e q_e(t^2)`. The first two rows of the table keep q_e positive up to 99/100, and (4.2) gives its first simple zero s_* afterwards. Thus no eigenvalue of K can cross zero before s_*, while K is positive semidefinite with a one-dimensional kernel at s_*.

The empty-event q is among the retained events in all rows and remains positive on [0,1]. Since `p_empty(t)=det(I-K(t))`, I-K stays positive definite there by continuity. The positive root of q_e is therefore the actual positive legal endpoint. The feasible set of an affine real-symmetric contraction path is convex; since q_e becomes negative immediately after s_*, there can be no later legal reentry. Evenness follows by conjugation with diag(I_3,-I_3). This proves the maximal interval assertion.

Equations (4.1)-(4.4) imply Gamma>1/2 everywhere inside it. Equation (2.2), the independent zero-point argument, and continuity of x log x at zero prove (1.1)-(1.3) up to both boundary configurations.

## 5. Exact finite evidence and the coefficient-space neighborhood

At the reference, the exact extrema behind the table have the following outward decimal displays; exact rational values are saved in `output/rational_certificate.json`:

| J / retained count | q minimum | q maximum | minimum E v^2 | minimum E z | N_J upper budget |
|---|---|---|---|---|---|
| [0,.9] / 64 | .034262558347522... | 2.838260765883187... | .550051427542580... | .550051427542580... | .115244632565240... |
| [.9,.99] / 64 | .002747503342768... | 3.072571446626742... | .837946913012560... | .982702550533286... | .134113304674964... |
| [.99,1] / 63 | .024683091733607... | 3.099172572816601... | .897267385836438... | 1.098321651709216... | .110590226982404... |

Here N_J is the sum of individual maxima, not the asserted exact maximum of their sum. Only its upper-budget meaning is used.

Let epsilon=10^-6 in (1.4). Reference and perturbed coefficients satisfy |a|<=2, |b|<=1. For s in [0,1],

`|v|<=4`, `|w|<=3`, `|h|<=8`, `|z|<=24`,

`|Delta q|<=2 epsilon`, `|Delta v|<=3 epsilon`,

`|Delta(v^2)|<=24 epsilon`, `|Delta z|<=37 epsilon`.              (5.1)

The two marginal probability vectors each have eight entries, so

`||mu-mu0||_1 <= ||p_A-p_A0||_1+||p_C-p_C0||_1 <=16 epsilon`.

Consequently, uniformly in s and for either retained event group,

`|Delta sum mu v^2| <=280 epsilon`,

`|Delta sum mu z| <=421 epsilon`,

`|Delta N_J| <=421 epsilon`.                                   (5.2)

The positive-part operation and taking a supremum are each 1-Lipschitz in sup norm, which proves the last inequality. Interval infima inherit the same bounds. The checker verifies each table comparison with these full perturbation penalties already applied: it subtracts 2epsilon from q minima, adds it to q maxima, subtracts 280epsilon/421epsilon from the two moment minima, and adds 421epsilon to N_J. All inequalities are strict.

For the rare event it additionally verifies (4.2) after errors 2epsilon in q, 3epsilon in v, 37epsilon in z, and epsilon in b. In particular the reference `q_e(1)=-14495058440362077306739/604128144976378750000000000` remains strictly negative after adding 2epsilon. Thus endpoint motion, rather than a fixed compact subchord, is included in the perturbation proof.

## 6. Map an explicit matrix-factor box into the coefficient family

The reference obeys `3I/10<A0,C0<7I/10`, `||U0||_F<9/10`, `||V0||_F<19/10`; these are checked by exact leading minors and sums of squares. Put eta=10^-12. Entry perturbations in (1.5) give operator errors at most 3eta, hence all intervening A,C have spectrum in [1/4,3/4], and `||U||<=1`, `||V||<=2`.

For any diagonal coordinate projection D and any A with spectrum in [1/4,3/4], `||(A-D)^(-1)||<=4`. To see this, split into the coordinates of D and its complement. For a putative eigenvalue lambda in (-1/4,1/4), one diagonal block of A-D-lambda I is positive definite and the other is negative definite; its Schur complement is strictly negative. Thus there is no eigenvalue in that interval. This proves the bound without rotating the observed coordinates.

The resolvent identity now gives `||Delta(A-D)^(-1)||<=48eta`. Expanding the two factors in G yields

`||G_A||<=4`, `||G_C||<=16`,

`||Delta G_A||<=72eta`, `||Delta G_C||<=240eta`.

Taking the trace in (2.1),

`|Delta a| <=2(72*16+4*240)eta =4224eta`.

For a 2-by-2 matrix of operator norm at most M, its determinant has Lipschitz bound 2M times the operator perturbation. Hence

`|Delta det G_A|<=576eta`, `|Delta det G_C|<=7680eta`,

`|Delta b|<=(576*256+16*7680)eta=270336eta`.

Finally `||A-D||<=1`, and the derivative of its 3-by-3 determinant gives `|Delta p_A(S)|<=9eta`, and the same bound for C. All these bounds are below epsilon=10^-6.

The top two-row minors of U0,V0 remain nonzero: their changes are at most `4eta+2eta^2`, smaller than the exact original minors. Thus U,V stay full-column-rank and B stays rank two. Also `||Delta B||<=9eta`, below every reference |B_ij|. Every internal off-diagonal remains nonzero under its eta perturbation. This completes Theorem B, including the explicit family (1.5).

## 7. Evidence classification and remaining quantifiers

`code/verify_maximal_chord.py` uses only Python's standard library. It reconstructs all 64 complete-event polynomials from **all principal minors and the defining Mobius sum**. It then cross-checks every a,b against the separately computed Schur formula. Odd powers and degree six vanish exactly; global and both conditional coefficient cancellations are checked. Polynomial interval extrema, six rational log comparisons, all perturbation margins, rank/legality data and both endpoint isolations use exact arithmetic. No pointwise entropy rerun is used as a substitute for the three continuum rows.

The recorded execution completed all 417 checks. Its stdout is saved literally, with separate generated rational evidence and the 64-row coefficient table. This is author-side computation, not an independent C2 certificate or independent proof review.

The theorem settles the maximal chord for the explicitly defined source and box. It does not settle all dense correlated rank-two paths, the other PR54 fixture's whole chord, general mixed kernel directions, arbitrary finite-kernel entropy concavity, entropy rates, or novelty. The separate method comparison and failure account are in `SOURCES_AND_FAILURES.md`.
