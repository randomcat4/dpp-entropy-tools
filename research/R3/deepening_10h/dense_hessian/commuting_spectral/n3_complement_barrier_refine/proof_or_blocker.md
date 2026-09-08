# Complement-product barrier

STATUS: ANALYTIC_REFINEMENT_CORRECT_AFTER_INDEPENDENT_REVIEW.
GLOBAL: INCOMPLETE.

## 1. Exact event input and the two-layer barrier

Use the objects in `frozen_problem.md`. Spectral Bernoulli mixing followed by
the projection-DPP observation channel gives the singleton vector y=Pr and
the pair vector z=Ps, pairs indexed by missing coordinate. The latter uses
the squares of complementary 2 by 2 minors of a real orthogonal 3 by 3 Q:
they equal the corresponding squared entries of Q. Thus the SAME P acts on
both layers. Empty and full events are e=product(1-theta_i), f=product theta_i.
Equivalently these eight events are obtained by Mobius inversion of principal
inclusion determinants. They are not those determinants themselves.

For a positive layer x with mass pi, write

    D_P(x) = sum_a (Px)'_a^2/(Px)_a - pi'^2/pi >= 0.

It equals the sum of squares
sum_a (Px)_a[((Px)'_a/(Px)_a)-pi'/pi]^2. Let h=H(N), N=|Y|.
The verified M7 identity is

    B = -H(Y)'' = -h'' + D_P(r) + D_P(s) + A,
    A = <Pr'',log alpha> + <Ps'',log beta>.                 (1)

The known full Shepp--Olkin theorem gives -h''>=0 and C=-Hess h PSD.
Its hypotheses hold because N is the sum of independent spectral Bernoullis
with success probabilities theta_i+t v_i. The source is Hillion--Johnson,
[Theorem 1.2](https://arxiv.org/pdf/1503.01570). This theorem is imported only
for the count distribution, not for the DPP's complete event law.

## 2. Pair the complementary accelerations before taking bounds

Fix a rate pair {j,k}, with remaining index i. Its contributions to r'' and
s'' are respectively

    2 v_j v_k [theta_i e_i -(1-theta_i)(e_j+e_k)],
    2 v_j v_k [(1-theta_i)e_i -theta_i(e_j+e_k)].

Since P is row stochastic, P(e_j+e_k)=1-Pe_i. Therefore their output
coefficients at observation coordinate a are P_ai-(1-theta_i) and P_ai-theta_i.
Summing the logarithms yields the EXACT coefficient identity

    A = 2 sum_{j<k} v_j v_k C_i,                            (2)
    C_i = sum_a P_ai log(alpha_a beta_a)
          -(1-theta_i) log(product_a alpha_a)
          -theta_i log(product_a beta_a).                 (3)

The powers 1-theta_i and theta_i must be attached to alpha and beta in this
order. Changing that order is an incorrect complement identification.

Equation (3) uses both layers jointly. No layerwise L1 triangle inequality
or separate maximum absolute log deviation is used. All dependence on v has
been factored into its three pair products; C_i depends only on Q and theta.

For a fixed base, A>=0 on the entire nonnegative rate cone iff all C_i>=0:
sufficiency follows from (2); necessity follows by setting the complementary
two rates positive and the remaining rate zero. This is an exact sign test
for A alone, NOT a characterization of the total entropy Hessian.

## 3. Product condition and expanded continuous region

Let m=min_a alpha_a beta_a. The column weights P_ai are nonnegative and sum
to one. Hence their weighted mean in (3) is at least log m. Also alpha and
beta are positive probability triples, so AM--GM gives

    product alpha <= 1/27,    product beta <= 1/27.

The remaining coefficients 1-theta_i and theta_i are positive and sum to
one. Keeping track of the MINUS signs in (3) therefore gives

    C_i >= log m + log 27 = log(27m).                     (4)

This direction of the inequality is essential. The AM--GM bound is applied
to products of normalized layer probabilities, not unnormalized atoms.

Consequently if m>1/27, all C_i have a strictly positive common lower bound.
At least two positive rates then make A>0 in (2), and (1) gives B>0.
If only rate v_j is positive, all pair products vanish, but the count law is
affine in theta_j. Thus -h''=sum_n pi_n'^2/pi_n>0: indeed
sum_n n pi_n'=v_j is nonzero. This proves strictness also on cone boundary
supports. The same proof applies to v<=0 after replacing v by -v.

The simpler rational condition alpha_a,beta_a>=1/5 implies m>=1/25>1/27.
Because each layer sums to one, this permits every atom up to 3/5. The old
rectangle [1/4,4/9] is contained in this new region. More generally the whole
M7 logarithmic region with delta<log(3)/3 lies inside the product region:
there alpha_a,beta_a>3^(-4/3), so m>3^(-8/3)>1/27.

The containment is strict on realizable, connected DPP parameters, as the
exact examples in Section 5 establish. The product condition also permits
an atom below 1/5 if the complementary layer at the SAME coordinate compensates.

## 4. Quantitative margins and equality

Suppose theta_i in [epsilon,1-epsilon], 0<epsilon<1/2. Put
L=1/[epsilon(1-epsilon)]. For the count Hessian C=-Hess h, its diagonal
entries are single-coordinate Fisher informations. The count score has
covariance 1 with N, and Var N<=3/4, hence C_jj>=4/3. Conditioning a latent
Bernoulli score on N contracts L2, hence C_jj<=L. Since C is PSD,
|C_ij|<=L.

For unit v>=0 let a=max v_j and s=sum_{i!=j}v_i; a^2>=1/3. The other
principal block is PSD, giving

    v^T C v >= (4/3)a^2 - 2L a s.

If s<=a/(3L), this is at least 2/9. Otherwise sum_{i<j}v_i v_j>=a s>1/(9L).
If min C_i>=mu>0, (1)--(2) therefore give the general bound

    B >= min{2/9, 2mu/(9L)} ||v||^2.                     (5)

For product condition m>=m0>1/27, choose mu=log(27m0). Necessarily m<=1/9:
3 sqrt(m)<=sum_a sqrt(alpha_a beta_a)<=1 by Cauchy--Schwarz. Thus m0<=1/9,
mu<=log3, and 2mu/(9L)<=2/9. The simpler explicit bound is

    B >= [2 log(27m0) epsilon(1-epsilon)/9] ||v||^2.      (6)

At the one-fifth region use m0=1/25, giving coefficient
2 log(27/25) epsilon(1-epsilon)/9. This coefficient is conservative, not sharp.

For strict product/coefficient premises, equality in B>=0 occurs exactly at
v=0. Equality in A>=0 may occur at any one-coordinate rate. When C_i>=0
but some vanish, A=0 iff v_j v_k C_i=0 for all three pairs. We do not claim
strict total curvature on every such coefficient boundary from that fact alone.

Strict conditions define an open set in (Q,theta). For a compact strict
parameter family with m>=m0>1/27, (6) is uniform over ALL nonnegative rates,
including all normalized supports. If a fixed-Q affine segment stays in that
family, twice integration gives midpoint gap <= -c h^2 ||v||^2/2, with c the
coefficient in (6). A pointwise certificate is not automatically an entire
feasible-line certificate. No direction mixing eigenvectors is included.

## 5. Realizable exact examples, not generic probability triples

Let U=J/3, w=(1,2,-3)^T, V=ww^T/14, W=I-U-V. These are rational orthogonal
rank-one projectors. Take

    K=(1/5)U+(1/2)V+(4/5)W,
    D=(1/5)U+(1/3)V+(2/3)W.

K has three distinct eigenvalues, heterogeneous diagonal, and every off-diagonal
nonzero; D>0 has rank three and is not proportional to K. At this base

    alpha=(71,53,23)/147,
    beta=(29/98,16/49,37/98),
    m=851/14406>1/27.

In particular alpha_3=23/147<1/5 and alpha_1>4/9, so the point violates both
the old rectangle and the new simple one-fifth condition but satisfies the
stronger joint-product condition. The script certifies 27 y_a(t)z_a(t)-R(t)T(t)>0
for all a throughout |t|<=1/100 using exact degree-six polynomial coefficient
bounds. The entire segment has spectral margin 29/150. This proves continuum
coverage by algebraic inequalities, conditional on the theorem candidate.

A second explicit base theta=(1/5,13/20,4/5) in the same projectors satisfies
the one-fifth condition, has minimum conditional atom 269/1197<1/4, and
violates the old rectangle. Thus even the simple one-fifth subregion genuinely
extends M7 on connected, heterogeneous, strict kernels.

The pointwise C_i test is stronger still. At theta=(1/10,1/5,9/10), same
projectors, m=26789/1431576<1/27; nevertheless all three C_i are strictly
positive by exact rational exponent-clearing certificates in the JSON.
For rational P,theta, choose d clearing all weights in (3). Then

    exp(d C_i) = product_a (alpha_a beta_a)^(d P_ai)
                 / [(product alpha)^(d(1-theta_i))
                    (product beta)^(d theta_i)].          (7)

This is a positive rational number, so comparison with 1 is an exact arithmetic
sign certificate. The script saves d and the full rational ratio; Decimal
logarithms are supplementary and not needed to decide these coefficient signs.

## 6. What remains open; vulnerable steps for independent review

The general total barrier remains INCOMPLETE. When some C_i<0, the count and
within-layer Fisher terms might still dominate. Equations (2)--(3) do not
solve that domination problem. Claiming C_i>=0 for every DPP would imply global
Psi''<=0 from (1), contrary to the existing verified M6 positive-Psi example.
That already falsified shortcut is explicitly not reused here.

Most vulnerable steps: (a) the index of the missing coordinate in the pair
layer; (b) row sums in deriving (3) versus column sums in deriving (4);
(c) signs and normalization in AM--GM; (d) single-rate strictness; (e) using
full count concavity, not merely a directional numerical check, for C PSD;
(f) not treating rational point certificates as a general optimization theorem.

The bounded tests are SCOUT/sanity only: six chosen centers do not establish
any universal claim. The arguments above are the candidate proof. No global
new-theorem, novelty, or venue-strength claim is made. A targeted source search
did not establish an existing identical refinement; absence was not certified.
