# Two exact boundaries for off-block DPP entropy transfer

Status: CANDIDATE. The explicitly quantified false implications B1 and B2 below are DISPROVED by the displayed families. Independent verification is pending. This contribution does not assess any global DPP entropy-concavity conjecture or validate another author's proof.

## Definitions and two-site law

K is a finite Hermitian contraction, with P(S subset X)=det K_S. H(K) is full-subset Shannon entropy, with natural logarithms and 0 log 0=0. Write h(x)=-x log x-(1-x)log(1-x).

For K=[[a,t],[conj(t),b]], the probabilities in order empty, {1}, {2}, {1,2} are
((1-a)(1-b)-|t|^2, a(1-b)+|t|^2, (1-a)b+|t|^2, ab-|t|^2).
Indeed P(11)=det K, P(10)=a-P(11), P(01)=b-P(11), and P(00)=1-P(11)-P(10)-P(01). No identity between H(K) and tr h(K) is assumed.

Block-diagonal kernels give independent block restrictions. To see this directly, expand E product_i[1+(z_i-1)1_{i in X}] using the inclusion law. The resulting generating polynomial is det(I-K+K diag(z)), which factors across blocks. Thus H of a direct sum equals the sum of its full-subset entropies.

## B1. Operator-norm error alone gives no dimension-free total-entropy modulus

False implication B1: There is a function omega satisfying omega(r)->0 as r->0 such that
|H(K)-H(B)| <= omega(||K-B||_op)
for all finite sizes, with B a block pinching of K, even if both spectra lie in [1/4,3/4].

Use singleton blocks, B_m=I_(2m)/2, and
K_m=direct_sum_(j=1)^m [[1/2,t_m],[t_m,1/2]].
For 0<=t_m<=1/4, both spectra lie in [1/4,3/4], B_m is precisely the pinching, and ||K_m-B_m||_op=t_m.

Each pair has two probabilities 1/4-t_m^2 and two probabilities 1/4+t_m^2. Grouping the two pairs of equal probabilities gives
H(K_m)=m[log 2+h(1/2+2t_m^2)],
H(B_m)=2m log 2,
H(B_m)-H(K_m)=m[log 2-h(1/2+2t_m^2)].

Since h''(1/2)=-4 and h is even about 1/2, Taylor's theorem gives
h(1/2+x)=log 2-2x^2+O(x^4).
Therefore log 2-h(1/2+2t^2)=8t^4+O(t^8).
Fix 0<c<=1/4 and set t_m=c m^(-1/4). Then ||K_m-B_m||_op->0, whereas
H(B_m)-H(K_m)=8c^4+O(1/m)->8c^4>0.
This disproves B1 with a uniform spectral margin on both K_m and B_m.

What it refutes: a dimension-free absolute total-entropy modulus depending only on operator norm.
What it does not refute: dimension-dependent bounds, Schatten-norm bounds, normalized-entropy continuity, or perturbation budgets scaled with dimension. The error per site in this family tends to zero. The quartic leading term is special to this diagonal center and is not claimed as a general sharp exponent. Direct-sum replication is used solely as a boundary example, not a new stationary mechanism.

## B2. A block buffer is necessary for a buffer-independent quadratic bound

False implication B2: There is a universal finite C such that
H(B)-H(K) <= C ||K-B||_F^2
for every finite Hermitian contraction K and its block pinching B, without a prescribed common spectral margin on B.

For 0<p<1/2 set
B_p=diag(p,1-p),
K_p=[[p,sqrt(p(1-p))],[sqrt(p(1-p)),1-p]].
K_p has trace 1 and determinant 0, so its eigenvalues are 0 and 1. Its law is (0,p,1-p,0): exactly one point is selected. B_p is its singleton pinching. Hence
H(B_p)=2h(p), H(K_p)=h(p),
||K_p-B_p||_F^2=2p(1-p),
[H(B_p)-H(K_p)]/||K_p-B_p||_F^2=h(p)/[2p(1-p)].
Because h(p)=p log(1/p)+O(p), this ratio tends to infinity. This disproves B2 in dimension two.

The failure persists with strict interiority at every parameter. Fix 0<theta<1 and replace the offdiagonal by sqrt(theta p(1-p)), obtaining K_(p,theta). Its trace is 1 and determinant is (1-theta)p(1-p)>0. Its eigenvalues are
[1 +/- sqrt(1-4(1-theta)p(1-p))]/2,
both strictly between 0 and 1. The block pinching remains B_p.

Its law is
((1-theta)p(1-p), p^2+theta p(1-p),
 (1-p)^2+theta p(1-p), (1-theta)p(1-p)).
The three probabilities tending to zero have positive leading coefficients (1-theta), theta, and (1-theta). For fixed a>0,
-(ap+O(p^2))log(ap+O(p^2))=a p log(1/p)+O(p).
The remaining probability is 1-(2-theta)p+O(p^2) and contributes O(p). Thus
H(K_(p,theta))=(2-theta)p log(1/p)+O(p),
H(B_p)-H(K_(p,theta))=theta p log(1/p)+O(p),
||K_(p,theta)-B_p||_F^2=2theta p(1-p),
and the ratio is (1/2)log(1/p)+O(1)->infinity.
The asymptotics fix theta; their constants may depend on theta. For example theta=1/2 is sufficient.

What it refutes: a universal quadratic constant after dropping a fixed margin on B. Pointwise strict interiority of B (and even K) does not provide a uniform constant.
What it does not refute: quadratic bounds with a B-dependent or margin-dependent constant, or other continuity estimates without a buffer. This family does not establish that K itself needs a spectral buffer, nor establish an optimal dependence on the B buffer.

## Reproduction and status

The accompanying artifacts/boundary_examples.py uses standard-library Python only. It checks the probability identities with exact rational arithmetic at ten specified (p,theta) pairs, and evaluates five specified dimension-scaling rows. It avoids enumerating 2^(2m) subsets. The numerical entropy values are diagnostics, not interval or formal certificates; the displayed all-parameter derivations are the proof candidate.

From the checkout root:
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 NUMEXPR_NUM_THREADS=2 python3 research/T2/artifacts/boundary_examples.py

Coverage: 10 planned and completed exact-law cases; 5 planned and completed scaling cases; no search or general numerical coverage claim. Independent certification remains pending. No outside proof or literature claim is used. These elementary examples are not presented as novel theorems.

The only statements labelled DISPROVED are B1 and B2 as quantified above. No realification transfer or stationary entropy-rate inference is claimed.
