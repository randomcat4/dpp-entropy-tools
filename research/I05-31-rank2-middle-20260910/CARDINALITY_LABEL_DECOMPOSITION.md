# I05-31 — exact cardinality/label decomposition of the natural two-parameter family

Status: **AUTHOR ANALYTIC PROOF / PENDING_INDEPENDENT_REVIEW; novelty NOT_ASSESSED.** This is an exact re-indexing of the complete observed-coordinate Shannon law. It does not coarse-grain away any event: the cardinality and label variables below are a bijective encoding of every subset of three coordinates.

Let

`A=alpha P+beta Q`, `C=I-A`, `B=sqrt(alpha(1-alpha))P`,

and complement the right observed configuration, writing `Y=T^c`. Complementation is a bijection of complete configurations and does not alter Shannon entropy. Both `S` and `Y` then have the same marginal DPP law `pi=p_A`.

## 1. A subset is exactly a cardinality plus, on the middle levels, one label

For `S subset {1,2,3}`, put `K=|S|`. If `K=1`, let `J` be the occupied label. If `K=2`, let `J` be the missing label. At levels zero and three no label is needed. Thus `(K,J)` is a bijective encoding of all eight subsets.

The marginal law is exchangeable and uniform inside each cardinality level. Its four total cardinality probabilities are

`pi_0=(1-alpha)^2(1-beta)`,

`pi_1=(1-alpha)[2alpha(1-beta)+(1-alpha)beta]`,

`pi_2=alpha[alpha(1-beta)+2(1-alpha)beta]`,

`pi_3=alpha^2 beta`.                                         (1.1)

The same formulas hold for `Y`.

The joint complete law is invariant under simultaneous permutations of the three labels. Consequently, conditional on a pair of middle cardinalities `k,l in {1,2}`, its label law has only two values: one for `J_S=J_Y` and one for `J_S!=J_Y`.

## 2. Cardinality likelihoods are coefficients of one explicit bivariate polynomial

Put `r=alpha(1-alpha)`, `s=t^2`, `delta=1-s`. In the spectral P sector, after right complementation, each of the two repeated modes is an ordinary pair of Bernoulli(alpha) variables with joint generating polynomial

`g_s(x,y)=[(1-alpha)^2+rs]`

`         +r delta (x+y)`

`         +[alpha^2+rs]xy`.                                 (2.1)

The Q modes on the two sides are independent Bernoulli(beta), so their factor is

`h_beta(x)h_beta(y)`, `h_beta(x)=1-beta+beta x`.

Cardinality is basis-invariant. Therefore the **actual observed** joint cardinality law is exactly

`P(K=k,L=l)=[x^k y^l] g_s(x,y)^2 h_beta(x)h_beta(y)`.         (2.2)

Define its likelihood ratio relative to the fixed cardinality marginals by

`qbar_kl=P(K=k,L=l)/(pi_k pi_l)`.                             (2.3)

Equations (1.1)-(2.3) give all sixteen cardinality cells without a complete-event determinant expansion.

## 3. The three nontrivial symmetric label channels

Only the cells `(1,1)`, `(2,2)`, `(1,2)` and `(2,1)` carry two labels. Let `q^=_kl` and `q^!=_kl` be the complete-event likelihood ratios for equal and unequal labels. Then

`qbar_kl=(q^=_kl+2q^!=_kl)/3`.                               (3.1)

There are only three distinct channels because `(1,2)` and `(2,1)` coincide.

Set

`L=2alpha+beta-3alpha beta`,

`N=alpha+2beta-3alpha beta`.

The shifted-event P-compressions on a level-one event have two eigenvalues whose difference is

`Delta_1=2 sqrt(r)(1-beta)/[(1-alpha)L]`,

while on a level-two event the eigenvalue difference is

`Delta_2=-2 sqrt(r) beta/[alpha N]`.                          (3.2)

For the three label directions, the squared inner product is one for equal labels and `1/4` for unequal labels. The determinant coefficient is orientation-independent. Hence

`q^=_kl-q^!=_kl=(3/4)s Delta_k Delta_l`.                     (3.3)

Together, (2.3), (3.1) and (3.3) determine both likelihoods exactly. In particular,

`q^=_11-q^!=_11=3sr(1-beta)^2/[(1-alpha)^2L^2]`,

`q^=_22-q^!=_22=3sr beta^2/[alpha^2N^2]`,

`q^=_12-q^!=_12=-3s beta(1-beta)/(LN)`.                      (3.4)

The opposite sign of the mixed label channel is structural, not a numerical accident.

## 4. Exact Shannon/mutual-information decomposition

Let

`theta_kl=(q^=_kl-q^!=_kl)/(q^=_kl+2q^!=_kl)`.

Then

`q^=_kl=qbar_kl(1+2theta_kl)`,

`q^!=_kl=qbar_kl(1-theta_kl)`.                               (4.1)

For `-1/2<theta<1`, define the mutual information of the three-state symmetric label channel

`Phi_3(theta)`

`=[(1+2theta)/3] log(1+2theta)`

` +[2(1-theta)/3] log(1-theta)`.                             (4.2)

The true mutual information between the two full observed configurations is exactly

`I(S;Y)`

`= sum_(k,l=0)^3 pi_k pi_l qbar_kl log qbar_kl`

`  + sum_(k,l in {1,2}) pi_k pi_l qbar_kl Phi_3(theta_kl)`.  (4.3)

The first line is the mutual information of the two cardinalities. The second line is the sum of the conditional label mutual informations; `(1,2)` and `(2,1)` are both included. Formula (4.3) follows directly from the chain rule and the uniform one-diagonal/two-off-diagonal label law. It is algebraically identical to the original sum over all 64 complete events.

Since the block marginals are fixed in `t`,

`H(K(t))=H(A)+H(C)-I(S;Y)`.                                  (4.4)

Thus proving convexity of the right side of (4.3) in the physical `t` is exactly the original complete-Shannon concavity problem, with no Fisher or acceleration term removed.

## 5. Reduction achieved and remaining sign

The generic 13 complete-event likelihood types are now reorganized into:

- sixteen explicit cardinality coefficients of the single polynomial (2.2), reduced further by symmetry;
- three three-state symmetric label channels determined by (3.4).

This is a strict algebraic reduction, not a finite sample. It isolates the only orientation-sensitive mechanism in three scalar channel parameters. The full Fisher–acceleration joint kernel can be differentiated directly from (4.3), or equivalently from `JOINT_KERNEL_F_DIVERGENCE_IDENTITY.md`.

No claim is made here that the cardinality term or each label term is separately convex. Such a claim would require proof: their acceleration pieces can exchange sign even though their sum may remain favorable.