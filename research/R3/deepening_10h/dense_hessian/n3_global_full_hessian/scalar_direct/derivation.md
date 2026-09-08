# Direct event-score certificates for the remaining scalar

AUDITED SCOPED IDENTITIES AND BLOCKERS. Global rho<=1 remains INCOMPLETE.
A fresh non-author implementation independently reconstructed the core
identities, sufficient conditions, path blocker, and three score corrections.
U8's reviewed reduction and boundary expansions are inputs, not newly claimed
discoveries here.

## 1. Definitions and a strengthened nondegeneracy fact

Write K=[[x,a,b],[a,y,c],[b,c,z]]. Coordinates on Sym(3) are
(D11,D22,D33,D12,D13,D23), so the Frobenius gradient corresponding to a
coordinate gradient has its last three entries divided by two.

Let p_S be the eight exact Möbius atoms. Define

F(D,E)=sum_S dp_S[D] dp_S[E]/p_S,

N=-diag(l23,l13,l12)-Lambda K, delta=det N,

eta(D)=tr(N^-1 D), E=N^-1/2 D N^-1/2.

The reviewed identity is B(D)=F(D)+delta||E||_F²-delta(tr E)²,
where B=-Hess H. Connected strict K implies N>0 and all p_S>0.

**Lemma 1: F itself is positive definite at every connected strict n=3 K.**
If F(D)=0, all exact atom derivatives vanish, hence every inclusion moment
derivative vanishes. The first moments give Dii=0. For each nonzero edge,
d det K_ij=-2Kij Dij then gives Dij=0. If all edges are present this finishes.
Otherwise connectedness on three vertices leaves exactly one missing edge,
say a=0 and bc!=0. The remaining determinant derivative is 2bc D12, so it
also vanishes only when D12=0. This covers every connected graph, including
paths and all sign patterns. No numerical rank test is used.

## 2. The scalar as an exact regularized score projection

For each S put W_S=gradient_Frobenius p_S. For any real eight-vector g define

L(g)=sum_S g_S W_S,

Q(g)=||I-N^1/2 L(g) N^1/2||_F² + delta Var_p(g).

Constants in g do not change L because sum W_S=0. One may therefore impose
E_p g=0. Let the operator T from Sym(3) to the mean-zero event space be

(T E)_S=dp_S[N^1/2 E N^1/2]/sqrt(delta p_S).

In orthonormal Frobenius coordinates U8 gives
rho=<I,(I+T* T)^-1 I>. Completing the square in the elementary least-squares
identity gives

**rho(K)=min_g Q(g).**                                              (10)

Indeed take w_S=sqrt(delta p_S)g_S in
min_w(||I-T*w||²+||w||²). The minimizer is automatically mean-zero after
removing its constant component. This identity is an explicit eight-event
inequality: a single exhibited g with Q(g)<=1 certifies B>=0; Q(g)<1
certifies B>0. Merely rewriting the minimization does not prove its value
is at most one globally.

## 3. An exact one-dimensional formula for unregularized trace capacity

Let V=eta^T F^-1 eta. Equivalently V is the minimum variance of a statistic g
satisfying L(g)=N^-1. This follows either by Lagrange multipliers or the
minimum-norm solution of the six independent score constraints. The seven
nonempty inclusion indicators T_A(S)=1_(A subset S), together with constants,
span all functions on the eight events. Their covariance matrix is

C_AB=det K_(A union B)-det K_A det K_B.                            (11)

C is positive definite: a zero-variance linear combination of the seven
indicators is constant on all eight atoms; its value at the empty atom is
zero and Boolean Möbius inversion then makes all seven coefficients zero.

Order the seven moments as (x,y,z,q12,q13,q23,r), and let J be their 7 by 6
Jacobian. Then

V=min_{J^T beta=eta} beta^T C beta.                               (12)

The feasible set is an affine line, by Lemma 1. If a,b,c are all nonzero,
the following supplies an explicit parametrization beta=beta0+t h. Write

v12=-eta12/(2a), v13=-eta13/(2b), v23=-eta23/(2c),

h12=bc/a-z, h13=ac/b-y, h23=ab/c-x.

The pair entries of beta0 are v12,v13,v23 and its r entry is zero. Its first
three entries are

(eta1-y v12-z v13, eta2-x v12-z v23, eta3-x v13-y v23).

The pair entries of h are h12,h13,h23; its r entry is one; its diagonal
entries are

(-y h12-z h13-(yz-c²),
 -x h12-z h23-(xz-b²),
 -x h13-y h23-(xy-a²)).

These formulas follow directly by differentiating q and r. Hence

**V=beta0^T C beta0-(beta0^T C h)²/(h^T C h).**                  (13)

At a path, no division by a missing edge is allowed. If a=0, bc!=0, the
off-diagonal constraint first fixes beta_r=eta12/(2bc); choose beta12 as
the free parameter, solve the other two pair constraints, then the three
diagonal constraints. Formula (13), with that affine solution, still holds.
Alternatively any independent six rows of J determine the affine line.

Thus V uses only moment covariances and one one-dimensional quadratic
minimization, not a six by six Fisher inversion.

## 4. A sufficient scalar condition, with equality cases

Cauchy–Schwarz in the F metric gives F(D)>=eta(D)²/V. Splitting
E=E0+(tr E)I/3 then gives

B(D)>=delta||E0||² + (1/V-2delta/3)(tr E)².                     (14)

Consequently the explicit condition

**S(K):=(2delta/3)V <= 1**                                      (15)

is sufficient for rho<=1. If S<1, B is positive definite. If S=1, a
nonzero null direction can occur only when E0=0, namely D is a multiple
of N, and equality also holds in Fisher Cauchy–Schwarz. Equivalently
F(N,N)=6delta (or F^-1 eta is proportional to the coordinate vector of N).
If that equality fails, B remains positive definite even at S=1.

The same bound arises from (10) by choosing the minimum-variance unbiased
trace estimator g0, then optimizing only its scalar multiple:

rho <= min_t [3(1-t)²+delta V t²]
     = 3delta V/(3+delta V).

This is a genuine sufficient test but emphatically not a necessary one.

## 5. Four event indicators: an adaptive five-category certificate

Choose T=(empty,12,13,23), and group the other four atoms into R. Set

C_T=diag(p_T)-p_T p_T^T,

b_s=tr(N W_s),

M_st=tr(N W_s N W_t)+delta(C_T)_st, s,t in T.                   (16)

C_T>0 because all four selected atom masses and the remaining mass are
positive. Thus M>0, with no rank assumption on the four gradients.

Restrict (10) to linear combinations of the four centered event indicators.
Completing the resulting four-variable square gives

**rho <= R_T:=3-b^T M^-1 b.**                                  (17)

The explicit four by four condition b^T M^-1 b>=2 is sufficient for B>=0;
a strict inequality certifies B>0. It involves eight exact atom values,
four first gradients, and N's four logarithmic coefficients only. No
unproved conditional-independence assertion is used.

Equivalently replace F by the five-category Fisher form

F_T(D)=sum_{s in T} dp_s[D]²/p_s + dp_R[D]²/p_R.

The exact missing information is

F(D)-F_T(D)=sum_{s in R} p_s (dp_s[D]/p_s-dp_R[D]/p_R)² >=0.    (18)

Let B_T=F_T+delta G_N-delta eta eta^T. Its Schur scalar is exactly R_T;
Woodbury proves (17) directly, and B>=B_T. This interpretation explains
both the certificate and the potential loss from grouping atoms.

Complementation produces T'=(123,1,2,3). The complementary test has
R_T'(K)=R_T(I-K), because p, W transform by complement/sign and N is
complement invariant. Therefore

**min(R_T,R_T')<=1**                                           (19)

is a complement-invariant sufficient condition valid for every connected
strict K. Section 8 disproves that it holds at every such K. Its strict sublevel set
is open in the full six-dimensional connected strict kernel domain by
continuity of atoms, logs and inverses. This is a precise, verifiable
continuous subclass, not a finite grid promoted to an open region.

## 6. Why the trace-capacity shortcut cannot settle the boundary

Use the reviewed dense rank-one family K_e=e I+(theta-e)P, P=uu^T, with
fixed 0<theta<1 and all ui!=0. Put L=log(1/e). U8 establishes

N=L(I-theta P)+O(1), delta=(1-theta)L³(1+O(1/L)),

F=e^-1 F_-1+F0+O(e), ker F_-1={uv^T+vu^T}=:T0.

On T0 write D=alpha P+uv^T+vu^T, v perpendicular to u. The limiting Fisher
form has no radial/mixing cross term and has radial coefficient
1/[theta(1-theta)]. Moreover

eta(D)=alpha/[L(1-theta)]+O(||D||/L²).

F0 is positive definite on T0; the inverse normal Fisher block is O(e).
The block inverse therefore yields

V=theta/[(1-theta)L²]+O(L^-3),

**S(K_e)=(2theta/3)L+O(1) -> infinity.**                        (20)

But the reviewed actual scalar is
rho(K_e)=1-1/(theta L)+O(L^-2)<1 eventually. Thus the implication
"all DPPs obey (15)" is analytically false on an explicit strict connected
family. This is a failure of discarding the traceless regularization,
not a positive-curvature counterexample. It also prevents a universal gap.

## 7. The adaptive coarsening preserves the relevant boundary information

For the same rank-one family, the three pair atoms vanish linearly, the
full atom quadratically, and the empty and singleton atoms remain positive.
The five-category Fisher F_T has exactly the same pole F_-1 as F: it retains
each of the three pair events. On T0 its finite limiting form is

F_T,0(D,D)=(tr D)²/[theta(1-theta)].

Indeed p0 tends to 1-theta with derivative -tr D, and p_R tends to theta
with derivative tr D; pair derivatives on T0 vanish at leading order.
The lost information is only in the two tangent mixing directions, not
the radial P direction. The cofactor term supplies 2L||v||²+O(||v||²)
on these mixing directions, as in the reviewed U8 block argument.

Scale span(P), its two mixing directions and T0-perpendicular by
1,L^-1/2,sqrt(e). The scaled B_T tends to the positive definite blocks
1/[theta(1-theta)], 2||v||², and F_-1 restricted to its normal space.
Mixed blocks vanish: the pole has exactly zero tangent and mixed blocks,
remaining Fisher terms are bounded, and cofactor terms are O(L).
This proves B_T>0 for every sufficiently small e>0 on this fixed family.

The reviewed moving-space inverse expansion also applies without requiring
F_T itself to be positive definite: F_T+delta G_N is positive definite,
the same pole has the same exact kernel, its tangent/mixed blocks are O(1/L)
after normalization, and its finite radial Fisher coefficient is unchanged.
It gives the sharper certificate asymptotic

**R_T(K_e)=1-1/(theta L)+O(L^-2).**                            (21)

All constants may depend on fixed theta,u. No uniformity when theta tends
to 0 or 1, ui tends to zero, or soft eigenvalue rates become unequal is
asserted. Complementation proves the counterpart for T' near I-K_e.

A fixed orientation cannot replace the adaptive test. Near I-K_e the
four T events are the old full atom plus old singletons. The full-atom
score contribution is bounded: p_full=theta e² and dp_full=O(e)||D||.
The singleton contributions and remaining mass are bounded as well.
Thus F_T(I-K_e)=O(1), while delta G_N is of order L, and

**R_T(I-K_e)=3+O(1/L) -> 3.**                                 (22)

This analytically disproves universal applicability of the fixed T test.
The complementary test retains (21). Neither (21) nor (22) decides whether
the adaptive condition (19) holds everywhere; the following exact point settles
that stronger shortcut negatively.

## 8. Exact rational blocker to both orientations of five-category grouping

Take the strict connected path and the positive-definite direction

K=[[1/2,3/10,0],[3/10,1/2,3/10],[0,3/10,1/2]],

D=[[1,-3/5,1/3],[-3/5,5/6,-3/5],[1/3,-3/5,1]].

K has eigenvalues 1/2,1/2±3sqrt(2)/10, all strictly between zero and one.
Exact rational LDL additionally certifies D>0 and a margin 1/1000 throughout
the affine chord |t|<=1/100. In bitmask order 0,1,2,12,3,13,23,123 the
probability and derivative arrays are

p=(7,25,43,25,25,43,25,7)/200,

dp=(-137,-197,-463,197,-197,31,197,569)/600.

Here Lambda=0 and N=diag(n,m,n), with n=log(43/7), m=log(625/301).
Direct Fraction computation gives

F_T(D)=12487351/3386250,

F(D)=56578567/1693125,

2tr(N adj D)=(142/75)n+(16/9)m.

Therefore the hybrid surrogate B_T, NOT an entropy Hessian in its own right,
satisfies

**B_T(D)=12487351/3386250-(142/75)log(43/7)
                       -(16/9)log(625/301)<0,**               (23)

while the actual negative entropy Hessian is

**B(D)=56578567/1693125-(142/75)log(43/7)
                      -(16/9)log(625/301)>0.**                (24)

Both inequalities are certified by rational logarithm intervals, not just
floating signs. For q>1, y=(q-1)/(q+1), use

L_m(q)=2 sum_{j=0}^{m-1} y^(2j+1)/(2j+1),

0<log(q)-L_m(q)<=2 y^(2m+1)/[(2m+1)(1-y²)].

With m=120, the script stores all exact endpoints and checks the signs in
Fraction arithmetic. Rounded values are B_T(D)=-1.0482033815378993 and
B(D)=28.68078384622142. These rounded values are only displays of the exact
interval certificates.

Let S=diag(1,-1,1). Then I-K=SKS, and event probabilities are invariant under
diagonal sign conjugation. Complementation and sign conjugation therefore
give B_T'(SDS)=B_T(D)<0. Thus both R_T and R_T' exceed one at this K.
The adaptive five-category sufficient test is genuinely non-universal.
The high-precision values are R_T=R_T'=1.0953535868173425751, whereas
the actual rho is 0.5132681842709295321. The latter full-rho computation is
sanity evidence; the theorem-level obstruction already follows from (23),
the sign conjugation, and the exact rank-one Schur criterion.

This does NOT disprove entropy concavity: (24) proves precisely the opposite
sign in the frozen witness direction. The obstruction is loss of conditional
score information under the proposed grouping.

## 9. Retaining the missing information: three orthogonal score contrasts

For disjoint nonempty event groups A,B, write p_A=sum_A p_s, j_A=dp_A in
six-coordinate form, and define

h_(A,B)=p_B j_A-p_A j_B,

w_(A,B)=1/[p_A p_B(p_A+p_B)].

The exact Fisher gain from splitting A union B into its two children is
w h h^T. This follows by expanding
j_A j_A^T/p_A+j_B j_B^T/p_B-(j_A+j_B)(j_A+j_B)^T/(p_A+p_B).
The corresponding centered binary contrast functions are orthogonal across
a nested partition tree: a child contrast has conditional mean zero within
its parent, while its ancestors are constant on that parent.

Split R={1,2,3,123} in this fixed sequence:

1. {123} versus {1,2,3};
2. {1} versus {2,3};
3. {2} versus {3}.

Then, exactly for every strict K,

**F=F_T+w1 h1 h1^T+w2 h2 h2^T+w3 h3 h3^T.**                  (25)

This is not a lower bound or a discarded remainder. The sanity script
verifies the entire 6 by 6 identity in exact Fraction arithmetic at every
listed point, in addition to the proof by the partition tree.

Set A0=F_T+delta G_N and Ai=Ai-1+wi hi hi^T. Every Ai is positive definite.
Sherman–Morrison gives nonnegative, explicit scalar corrections

ci=delta (eta^T Ai-1^-1 hi)² /
                [wi^-1+hi^T Ai-1^-1 hi],

**rho=R_T-c1-c2-c3.**                                         (26)

The full remaining problem is therefore exactly

**c1+c2+c3 >= R_T-1 whenever R_T>1.**                         (27)

This is an EQUIVALENT_BLOCKER, not a solved or strictly weaker lemma.
Every term is verifiable from the eight atoms, their six first derivatives
and N. Positivity of the three corrections alone does not prove that their
sum is large enough.

Retaining only the first split gives a six-category sufficient certificate
rho<=R6:=R_T-c1. A general assertion R6<=1 would be stronger than the full
claim and is presently unproved, not inferred from finite passes. At the
exact path obstruction, the corrections are approximately

(c1,c2,c3)=(0.5475945716632780954,
           0.0049791631619406727,
           0.0295116677211942749).

Thus the first retained conditional score already lowers the surrogate
scalar to R6=0.5477590151540644797. The script separately certifies in
rational log intervals that the first split makes B6(D)>0 for the explicit
direction (23). This rescues that witness, not a general theorem.

## 10. Review priorities and exact stopping point

The global eight-event projection bound and the equivalent correction
inequality (27) remain unresolved. Neither Fisher trace capacity nor
five-category grouping can be imposed globally; both now have analytic or
exact rational blockers. Six-category grouping is a precise next
sufficient-condition candidate, not an established universal property.

Most fragile points for fresh review: Frobenius versus six-coordinate
gradients in (10)/(16); the estimator constraints and S=1 equality case;
the sign-conjugation transfer of (23); the update denominator in (26);
and the moving tangent-space transfer of the first coefficient in (21).
The block-scaled proof of eventual B_T>0 does not rely on that sharper
coefficient. No positive-curvature counterexample to the original DPP
problem has been claimed.
