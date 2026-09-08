# T1 boundary and information-loss audit

STATUS: CANDIDATE. This is one bounded, isolated exploration unit, not an
independent verification or a frozen statement owned by the route lead.
The elementary claims below are PROVED_HERE in the ordinary mathematical
sense; no general DPP entropy-concavity claim is proved or disproved.
No novelty claim is made.

## Scope and exact definitions

Let E={1,...,n}, K=K* satisfy 0<=K<=I, and D=D*. Write

p_S(K)=(-1)^{|E\S|} det(K-I_{E\S}),
H(K)=-sum_S p_S(K) log p_S(K), with 0 log 0=0.

The main curvature formula applies on the strictly positive event support.
For 0<K<I every event has positive probability: with
L=K(I-K)^{-1}>0, p_S=det(I-K) det(L_S)>0.
Along an affine path with all p_S>0,

H''=-sum_S (p'_S)^2/p_S -sum_S p''_S log p_S.

For real symmetric K and purely imaginary Hermitian D, conjugation takes
K+tD to K-tD. The determinant probabilities are real, so each p_S(t) is
even and p'_S(0)=0. This statement alone gives no sign for the weighted
second term.

## Object A: exact two-site rule and lost information

Let K=[[a,c],[c,b]] with real a,b,c and 0<K<I, and
D=[[0,i*d],[-i*d,0]], d real. Set q=c^2+t^2*d^2. Direct determinants give

p_00=(1-a)(1-b)-q, p_11=ab-q,
p_10=a(1-b)+q, p_01=(1-a)b+q.

Thus p'=0 at t=0 and p''=(-2d^2,+2d^2,+2d^2,-2d^2).
Writing A=p_00, B=p_11, C=p_10, F=p_01,

H''(0)=2d^2 log(AB/(CF)).
Moreover CF-AB=c^2.

The latter identity follows by expanding both quadratic products:
the constant terms cancel and the coefficient of c^2 is
a(1-b)+(1-a)b+ab+(1-a)(1-b)=1.
All four probabilities are positive, so H''<=0, with strict inequality
exactly when c*d is nonzero.

This is a complete constant-cost rule on this two-site family. It is not
a rule for arbitrary imaginary directions in larger matrices.

Concrete exact fixtures, all using d=1 and a=b=1/2:

| c | (p_00,p_10,p_01,p_11) | H'' |
|---|---|---|
| 0 | (1/4,1/4,1/4,1/4) | 0 |
| 1/8 | (15/64,17/64,17/64,15/64) | 4 log(15/17)<0 |
| 1/4 | (3/16,5/16,5/16,3/16) | 4 log(3/5)<0 |

All three have identical full event support and identical arrays p'=0 and
p''=(-2,2,2,-2). Consequently even event support plus both derivative
arrays, when event weights are discarded, cannot distinguish zero from
strictly negative entropy curvature. The first and third are the smallest
nontrivial imaginary-direction example: a one-site purely imaginary
Hermitian matrix is zero.

This is **not** evidence that this input fails to decide positivity versus
nonpositivity: these examples are all nonpositive. That stronger
impossibility claim would need opposite-sign examples and remains open in
this audit. Keeping c=1/8 and c=1/4 also keeps the nonzero kernel-edge graph,
but only establishes different curvature values, not different signs.

Direction cannot be discarded either. At the same K=I_2/2, the imaginary
direction above has H''=0, whereas D=diag(1,0) gives H''=-4.
The norm ||D||_F is sqrt(2) for the former and 1 for the latter; if equal
norms are required, use D=diag(1,1), which gives H''=-8.
Thus K, all event weights and all event supports still do not determine
the curvature without D. Equal-norm rescaling cannot fix this.

## Object B: a cheap general-dimensional sufficient condition

For any 0<K<I and any nonzero Hermitian rank-one D, H''(K)[D,D]<0.

Proof: write D=alpha vv*, with alpha real nonzero and v nonzero.
For every fixed matrix A, det(A+t alpha vv*) is affine in t:
in its column-multilinear expansion any term containing two replaced
columns vanishes because those columns are proportional to v.
Apply this to A=K-I_{E\S}; hence every p''_S=0.
The curvature is therefore -sum (p'_S)^2/p_S<=0.
It is strictly negative because some v_i is nonzero and the marginal
identity sum_{S containing i} p'_S=D_ii=alpha |v_i|^2 is nonzero.
At least one p'_S must be nonzero. All denominators are positive.

This is a structural direction test, requiring a rank-one check rather
than event enumeration. It gives a weak safe family, not the desired
general imaginary-direction criterion (a nonzero purely imaginary
Hermitian direction cannot have rank one). It follows from elementary
determinant multilinearity and is not claimed new.

## Object C: affine feasibility controls boundary singularities

**Candidate boundary lemma.** Suppose K_0+tD is a Hermitian contraction
for every |t|<epsilon. Then the support {S:p_S(K_0+tD)>0} is constant for
sufficiently small |t|, and H(K_0+tD) is real analytic there, including at
t=0. Zero event probabilities are identically zero near 0 and can be
omitted from the entropy sum.

Proof of the matrix-face assertion:
For x in ker K_0, positivity at both signs of t forces x*Dx=0.
For any fixed nonzero admissible t, x*(K_0+tD)x=0. If A>=0 and x*Ax=0,
then A x=0, as is immediate from its orthonormal eigen-expansion.
Hence D x=0. Applying the same argument to I-K_0 gives
D ker(I-K_0)=0. Hermiticity also removes cross-block entries.
Let U_0,U_1,U_m be the mutually orthogonal eigenspaces of K_0 for
eigenvalues 0, 1, and those strictly between 0 and 1. Along the path,
the first two blocks stay 0 and I, while the restriction to U_m stays
strictly between 0 and I for small t by continuity. These three subspaces
are fixed; only the operator in U_m changes.

Proof that event support depends only on these three subspaces:
For an orthonormal eigenbasis V with eigenvalues lambda_j, expansion of
the generating determinant yields the spectral mixture identity

p_S = sum_{J: |J|=|S|} [prod_{j in J} lambda_j
                       prod_{j notin J}(1-lambda_j)] |det V_{S,J}|^2.

For completeness, expand det(I-Lambda+V* Z V Lambda) by choosing diagonal
columns from I-Lambda or columns from V* Z V Lambda. For a chosen J the
remaining minor is det((V* Z V)_{J,J}); Cauchy-Binet expands it as
sum_{|S|=|J|}|det V_{S,J}|^2 prod_{i in S} z_i.
Compare coefficients in det(I-K+ZK)=sum_S p_S prod_{i in S}z_i.

Only J containing every basis column of U_1 and no column of U_0 have
nonzero weights. For such J every remaining spectral weight is strictly
positive. Let r=dim U_1 and k=|S|-r. If k lies outside [0,dim U_m], the
probability is zero. Otherwise p_S>0 exactly when

sum_{J_m subset basis(U_m), |J_m|=k}
  |det [V_1,V_{J_m}]_S|^2 > 0.

This unweighted sum is independent of the chosen orthonormal basis in
U_m: the wedges of its k-element subsets are an orthonormal basis of
the kth exterior power of U_m, and the displayed sum is the squared
norm of the projection of the coordinate wedge e_S onto the fixed
subspace (wedge^r U_1) wedge (wedge^k U_m). Equivalently this invariance
is Parseval under the unitary matrix of k-by-k minors for a change of
basis. Changing the orthonormal basis in U_1 changes determinants only
by a unit-modulus scalar. Thus the positivity condition depends only
on the fixed subspaces, proving constant support.

Finally each p_S(t) is a polynomial. A nonzero support probability is
positive at 0, so -p_S(t) log p_S(t) is real analytic near 0.
The other probabilities are identically zero near 0. Their finite sum
is analytic. This proves the boundary lemma without substituting zero
into a logarithm.

The converse matrix-feasibility statement also holds locally: if D
annihilates U_0 and U_1, it acts only on U_m, whose eigenvalues have a
positive gap from both endpoints. Sufficiently small positive and
negative t preserve that gap.

**Purely imaginary specialization.** If K_0 is real and D purely
imaginary Hermitian, entrywise conjugation maps K_0+tD to K_0-tD and
preserves positive semidefiniteness. Even one feasible nonzero t_0
therefore gives both endpoints, and convexity gives a two-sided interval.
The lemma applies. Hence a new zero-event t^2 log|t| singularity cannot
occur along a locally feasible affine imaginary path at a real center.
A formal direction which violates the annihilation condition is not an
admissible boundary perturbation.

## Two minimal boundary examples that keep path type explicit

1. **Infeasible affine imaginary tangent.**
   K_0=diag(1,0), D=[[0,-i],[i,0]] gives
   det(K_0+tD)=det(I-K_0-tD)=-t^2.
   No nonzero t is feasible. Its formal event polynomials include
   p_00=p_11=-t^2, so they must not be inserted into Shannon entropy.

2. **Feasible nonlinear imaginary tangent with a logarithmic singularity.**
   Let v(t)=(1,i*t)/sqrt(1+t^2) and K(t)=v(t)v(t)*.
   This is a rank-one projection for every real t, but is not affine.
   Its only positive event probabilities for t!=0 are
   p_{1}=1/(1+t^2), p_{2}=t^2/(1+t^2). Consequently

   H(t)=log(1+t^2)-[t^2/(1+t^2)]log(t^2)
       =-2t^2 log|t|+t^2+O(t^4 |log|t||).

   Its tangent at 0 is the inadmissible affine direction in example 1.
   The quadratic diagonal correction is what restores feasibility;
   dropping it changes the problem. H is not twice differentiable at 0.

For contrast, K(t)=diag(t,1/2) is an affine **one-sided** boundary path:
H(t)=h(t)+log 2, H''(t)=-1/[t(1-t)] for t>0, with a leading -t log t
entropy term. It does not satisfy the two-sided-feasibility lemma.
Also the affine boundary path diag(1,1/2+t,0) does satisfy the lemma;
its fixed support is {{1},{1,2}} and its entropy is h(1/2+t).

## Reproduction, coverage, and limitations

Run from the checkout root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  timeout 30s python3 research/T1/exploration/boundary/check_boundary.py
```

The companion results.json records the exact finite fixtures, process ID,
Python version, thread caps, CPU time, peak RSS and completed assertions.
The command uses only the Python standard library. It checks rational
probabilities and derivative coefficients on the two-site examples;
floating logarithms are diagnostics only, while strict signs above follow
from exact rational inequalities. The fixed-face example is a three-site
diagonal hand-derived fixture, not a computational proof of the lemma.

No parameter or random search ran. No matrix larger than 3 was evaluated.
No GPU or external dependency was used. A preliminary dependency probe
had one shell-quoting SyntaxError; the corrected read-only probe completed
and found neither NumPy nor SymPy. No mathematical computation was lost
or inferred from that failed probe. Runtime exit status is recorded
separately in execution.json.

The next falsifiable action is independent scrutiny of Object C's
support-invariance proof, followed by checking whether the route's chosen
curvature criterion retains enough event weights and direction data.
The zero-versus-negative pair is an input-loss obstruction, not an
opposite-sign counterexample. General imaginary-direction signs,
publication novelty, and independent certification remain unresolved.
