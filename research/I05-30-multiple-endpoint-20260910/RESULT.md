# I05-30 — multiple endpoint atoms: order-group Fisher dominance and a dense 3+3 double-endpoint chord

Status: **PROVED (author analytic proof / author exact finite certificate); PENDING_REVIEW.** Novelty is **NOT_ASSESSED**. This is a successor to PR95; it does not modify or inherit review of PR94/95.

Throughout, entropy is the complete-configuration Shannon entropy with natural logarithms and `0 log 0=0`. The physical path is always a true affine kernel path. No observed-basis entropy rotation, affine-L replacement, von Neumann entropy, event deletion, or Fisher truncation is used.

## 1. General affine DPP boundary setup

Let

`K(t)=K_*+(t-T)D`

be a finite real symmetric affine path, with

`0<K(t)<I` for `T-eps_0<t<T`, and `0<=K(T)<=I` a genuine legal boundary point. Put `eps=T-t>0`.

For every complete event `E subset [N]`, write `p_E(t)` for its exact probability. It is a polynomial in `t` (equivalently the signed determinant `(-1)^(N-|E|) det(K(t)-I_{E^c})`), so if `p_E(T)=0` then

`p_E(T-eps)=c_E eps^(k_E)+O(eps^(k_E+1))`,                   (1.1)

for an integer `k_E>=1` and `c_E>0`.

The complete entropy curvature is exactly

`-H''(t)=sum_E (p_E')^2/p_E + sum_E p_E'' log p_E`.         (1.2)

All terms below refer to this full identity.

## 2. A simple complete atom is forced at every affine spectral boundary

Let

`r_0=dim ker K(T)`, `r_1=dim ker(I-K(T))`.

At least one is nonzero.

### Lemma 2.1 — active spectral clusters enter the strict interior linearly

If `r_0>0`, the compression

`A_0=-P_0 D P_0` on `ker K(T)` is positive definite. Indeed for every nonzero `v` in that kernel,

`v^T K(T-eps)v=eps v^T A_0 v>0`.

Likewise, if `r_1>0`,

`A_1=P_1 D P_1>0` on `ker(I-K(T))`, because

`v^T(I-K(T-eps))v=eps v^T A_1 v>0`.

Consequently the `r_0` eigenvalues born from zero are all comparable to `eps`, and the deficits `1-lambda` of the `r_1` eigenvalues born from one are all comparable to `eps`. A direct block-Schur proof gives the comparison: on the orthogonal complement of the endpoint kernel the endpoint matrix has a positive spectral gap, while its kernel block is `eps A_i`; the off-diagonal block is `O(eps)`, so the Schur complement is `eps A_i+O(eps^2)`.

### Lemma 2.2 — a forbidden cardinality has linear mass

The exact cardinality generating polynomial is

`E[z^|X|]=det(I-K+zK)=prod_j (1-lambda_j+z lambda_j)`.       (2.1)

This identity follows directly by diagonalizing the determinant; no entropy is evaluated in that basis.

If `r_0>0`, the endpoint law cannot have more than `N-r_0` occupied points. For the forbidden interior cardinality

`m_+=N-r_0+1`,

(2.1) and Lemma 2.1 give

`P(|X|=m_+)=Theta(eps)`.                                     (2.2)

For a lower bound, occupy exactly one of the `r_0` small eigenmodes and all endpoint-nonzero modes; all factors outside the small cluster stay bounded below. For an upper bound, cardinality above `N-r_0` requires at least one small eigenmode to be occupied, so a union bound by the sum of those eigenvalues is `O(eps)`.

If `r_1>0`, apply the same argument to the forbidden low cardinality

`m_-=r_1-1`: one near-one eigenmode must fail, and

`P(|X|=m_-)=Theta(eps)`.                                     (2.3)

Each probability in (2.2) or (2.3) is a sum of nonnegative complete-event polynomials, all zero at the endpoint. Hence at least one complete event has `k_E=1` in (1.1). More strongly, the sum of the leading coefficients of the simple atoms in the relevant cardinality class is strictly positive.

### Theorem 2.3 — arbitrary multiplicity and simultaneous constraints are endpoint-concave

For every finite affine DPP path satisfying Section 1,

`H''(t) -> -infinity as t -> T-`.                            (2.4)

No simplicity assumption on `ker K(T)` or `ker(I-K(T))` is required; they may both be nontrivial simultaneously.

#### Proof

Partition the zero endpoint atoms by their order `k_E` in (1.1).

For `k_E=1`,

`(p_E')^2/p_E = c_E/eps+O(1)`,

while `p_E'' log p_E=O(log(1/eps))`.

For `k_E=2`, the Fisher term is `O(1)` and the acceleration-log term is `O(log(1/eps))`. For `k_E>=3`, both are `O(eps^(k_E-2) log(1/eps))`, apart from the nonnegative Fisher term. Endpoint-positive atoms contribute only `O(1)`.

Lemma 2.2 gives a nonempty simple-order group with total coefficient `A_1=sum_{k_E=1} c_E>0`. Therefore the complete expression satisfies

`-H''(T-eps)=A_1/eps+O(log(1/eps)) -> +infinity`.             (2.5)

This proves (2.4), preserving every Fisher and acceleration term. QED.

This strictly extends the previously accepted simple-endpoint statement: the proof works for repeated zero eigenvalues, repeated one eigenvalues, and simultaneous `K`/`I-K` activity.

## 3. Rank-two radial specialization: the dangerous double atoms are explicit

Now return to the rank-two cross-block path

`K(t)=[[A,tB],[tB^T,C]]`, `rank B=2`, `s=t^2`,

with strict decoupled marginals. For every complete event,

`p_E(t)=mu_E q_E(s)`,

`q_E(s)=1-a_E s+b_E s^2`, `mu_E>0`.                          (3.1)

Let `s_*=T^2` and `Delta=s_*-s`.

A boundary zero is either simple or double. If it is double then solving

`q_E(s_*)=q_E'(s_*)=0`

gives the exact universal form

`a_E=2/s_*`, `b_E=1/s_*^2`,

`q_E(s)=(1-s/s_*)^2=Delta^2/s_*^2`.                         (3.2)

For a simple zero write

`q_E(s_* - Delta)=c_E Delta+b_E Delta^2`, `c_E>0`.           (3.3)

The order-group contributions to `-H''` are then:

* simple event:
  `F_E=4 s_* mu_E c_E/Delta+O(1)`, while its acceleration-log term is `O(log(1/Delta))`;
* double event:
  `F_E -> 16 mu_E/s_*`, but
  `p_E'' log p_E = -(16 mu_E/s_*) log(1/Delta)+O(1)`.         (3.4)

Thus a double atom by itself has exactly the feared behavior: its Fisher pole has collapsed to a constant while its acceleration logarithm diverges with the wrong sign in `-H''`.

However Theorem 2.3 proves that the complete DPP boundary cannot consist only of double atoms. In rank two,

`A_s:=sum_(simple boundary E) mu_E c_E >0`,                   (3.5)

and therefore

`-H''(t)=4 s_* A_s/Delta+O(log(1/Delta)) -> +infinity`.      (3.6)

So a hypothetical quadratic likelihood in which every zero atom were double would indeed create endpoint convexity, but that pattern is **not realizable by a strict-interior affine DPP**. This is a realizability obstruction, not an entropy counterexample.

## 4. A new dense correlated 3+3 double endpoint outside the PR94 grouped-channel shape

The general theorem is now tested on a true correlated rank-two object whose positive endpoint has a two-dimensional kernel.

Let

`P=I_3-(1/3) 11^T`,

and

`L_A=[[2/5,0,0],[1/20,3/8,0],[-1/25,1/30,7/20]]`,

`L_C=[[7/20,0,0],[-1/30,2/5,0],[1/24,-1/28,3/8]]`.

Set

`A=L_A L_A^T`, `C=L_C L_C^T`, `B=L_A P L_C^T`.              (4.1)

Explicitly,

`A=[[4/25,1/50,-2/125],`
`   [1/50,229/1600,21/2000],`
`   [-2/125,21/2000,11269/90000]]`,

`C=[[49/400,-7/600,7/480],`
`   [-7/600,29/180,-79/5040],`
`   [7/480,-79/5040,2027/14112]]`,

`B=[[7/75,-14/225,-43/1260],`
`   [-77/2400,347/3600,-47/720],`
`   [-973/18000,-737/27000,12821/151200]]`.                 (4.2)

Both marginal blocks are internally correlated; `B` is dense and has rank two.

### Exact maximal chord and repeated endpoint

For `|t|<1`, Schur complementation by `A` gives

`C-t^2 B^T A^-1 B`
` =L_C [I-t^2 P] L_C^T`
` =L_C[(I-P)+(1-t^2)P]L_C^T >0`.                            (4.3)

At `t=1` this Schur complement has rank one, hence `K(1)` has nullity exactly two. The same holds at `t=-1` by block-sign congruence.

The exact Gershgorin absolute row-sum bound for `K(t)` on `|t|<=1` is at most

`12149/31500 <1`.                                            (4.4)

Therefore `I-K(t)>0` on the entire closed interval and the maximal legal chord is exactly `[-1,1]`.

### PR94 does not generate this cross block

PR94's three-observed-coordinate expansion from two base coordinates forces a proportional pair among the three observed columns; applying it on the other side gives the analogous row condition. For (4.2), exact nonzero 2x2 witnesses are

columns `(0,1),(0,2),(1,2)`: `7/1000,-23/3200,247/33600`,

rows `(0,1),(0,2),(1,2)`: `7/1000,-133/22500,2191/360000`.

Hence no pair of columns and no pair of rows is proportional. This only proves noncoverage by that exact PR94 grouped-channel construction; it is not a claim about every possible channel representation.

## 5. Complete compact-interior bound for the new fixture

For the 64 complete events, the checker reconstructs `mu_E,a_E,b_E` exactly from the defining complete law and independently cross-checks the rank-two Schur formula. It proves on the whole continuum `0<=s<=1` that

`(1-s)^2 <= q_E(s) <= 11/8` for every E.                     (5.1)

It also gives the exact moments

`M_a=E_mu[a^2]`, `M_ab=E_mu[ab]`, `M_b=E_mu[b^2]`,

and the strict rational comparisons

`M_a>1/60`, `M_ab<0`, `M_b>0`,                               (5.2)

`M_a-7M_ab+(37/2)M_b <1/50`.                                (5.3)

Put

`v=a-2sb`, `z=(a-sb)(a-6sb)`,

`lambda(q)=log(q)/(q-1)`, `lambda(1)=1`.

The exact normalized curvature is

`Gamma(s):=-H''(t)/t^2`
` =E_mu[4v^2/q+2 z lambda(q)]`,                              (5.4)

with `Gamma(0)=6M_a` by continuous extension.

Take

`s_0=9999/10000`.

By (5.1), on `0<=s<=s_0`,

`10^-8 <= q <=11/8`.

The decreasing secant `lambda` satisfies, by rational atanh enclosures,

`4/5 < lambda(q) <19`.                                      (5.5)

Furthermore

`E[v^2]=M_a-4sM_ab+4s^2M_b >1/60`,

`E[z]=M_a-7sM_ab+6s^2M_b >1/60`,

and by `|xy|<=(x^2+y^2)/2`,

`E|z| <= M_a-7sM_ab+(37/2)s^2M_b <1/50`.                   (5.6)

Using `q<=11/8` and writing the interval `[4/5,19]` as midpoint plus half-width gives

`Gamma(s)`
` > (32/11)(1/60)+(99/5)(1/60)-(91/5)(1/50)`
` =239/16500 >1/100`.                                       (5.7)

This is one continuum estimate over all 64 events, not a positive sampling grid.

## 6. The final endpoint band: a double bad atom is rescued by a simple cardinality group

At `s=1`, exactly eight complete atoms vanish for this fixture.

Seven are simple:

`(S,T)=(3,3),(3,7),(5,7),(6,7),(7,3),(7,5),(7,6)`,

and the full event `(7,7)` is double with

`q_77(s)=(1-s)^2`.                                          (6.1)

The full-event atom is therefore an actual instance of the dangerous term (3.4).

The six size-five simple events can be kept together. Their total probability is exactly

`R_5(s)=P(|X|=5)`
` =(1-s)(14595963-3190277 s)/51200000000`.                  (6.2)

Let `delta=1-s`. Weighted Cauchy inside this true cardinality group gives

`sum_(|E|=5) (p_E')^2/p_E >= (R_5')^2/R_5`,                 (6.3)

where primes are physical `t` derivatives. For `s>=s_0`, the exact rational constants in (6.2) give

`(R_5')^2/R_5 > 1/(1200 delta)`.                             (6.4)

No individual simple atom is selected or discarded.

For the full acceleration sum, the exact rank-two coefficients give

`sum_E |p_E''(t)|`
` <=2 E_mu|a|+12 E_mu|b| <1/4`.                             (6.5)

The same exact quadratic certificate behind (5.1) gives `q_E>=delta^2`, and

`min_E mu_E=194481/25600000000 >1/140000`.                  (6.6)

Hence every complete event, including the double full atom, obeys

`p_E >= delta^2/140000`,

so

`|log p_E| <= log(140000)+2log(1/delta)`.                    (6.7)

Using all Fisher terms as nonnegative and retaining all acceleration terms,

`-H''(t)`
` > 1/(1200 delta)`
`   -(1/4)[log(140000)+2log(1/delta)]`.                      (6.8)

For `0<delta<=10^-4`, the right side decreases as `delta` increases because its derivative is

`-1/(1200 delta^2)+1/(2delta)<0`.

At `delta=10^-4`, the rational log enclosures give

`log(140000)<12`, `log(10000)<10`,

and therefore (6.8) is strictly larger than

`25/3-8=1/3`.                                                (6.9)

Thus the final endpoint band is strictly concave despite the double atom's own adverse logarithmic divergence.

## 7. Whole maximal-chord conclusion

Combining (5.7) and (6.9), for every `0<|t|<1`,

`H''(t) <= -(1/100)t^2`.                                    (7.1)

At `t=0`, analyticity gives `H''(0)=0`. Hence

`H(t)+t^4/1200`                                              (7.2)

is concave on the whole closed maximal legal chord `[-1,1]`, and `H` is strictly Jensen-concave there for distinct points.

This is a true dense correlated 3+3 rank-two whole chord with a repeated two-dimensional spectral endpoint. It is not obtained by a spectral entropy rotation and it lies outside the exact grouped-channel shape proved in PR94.

## 8. What this resolves and what remains open

**PROVED (author proof; PENDING_REVIEW):**

1. every finite true affine DPP legal endpoint has `H'' -> -infinity`, with arbitrary zero/one multiplicities and simultaneous `K`/`I-K` activity;
2. in rank-two radial form, double complete atoms have an adverse logarithmic acceleration divergence, but a simple-order complete-event group is forced and its `1/Delta` Fisher pole dominates;
3. the explicit dense correlated 3+3 fixture (4.1)-(4.2) has a two-dimensional `K` kernel at each endpoint and satisfies the whole-chord bound (7.1).

**DISPROVED as a realizable endpoint mechanism:** a boundary in which all vanishing quadratic rank-two atoms are double. Such an abstract likelihood would have the wrong entropy sign, but Lemma 2.2 forbids it for an affine DPP entering from a strict interior.

**INCOMPLETE:** a universal whole-chord theorem for arbitrary dense correlated rank-two blocks. The endpoint part is now removed from that problem; any counterexample must occur in a compact strict interior region. Uniform parameter-neighborhood control through a splitting multiple endpoint is not claimed here and is a separate two-scale stability problem.

Novelty remains separate from mathematical correctness.
