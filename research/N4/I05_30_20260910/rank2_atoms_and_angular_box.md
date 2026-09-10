# Moving rank-two endpoints: complete atoms and an explicit exclusion box

Status: **PROVED (author proof; PENDING_REVIEW)** for the identities and theorems below. The unrestricted moving-rank-two entropy question is **INCOMPLETE**. No novelty claim. Successor issue: #84, original lineage #21/PR62. Base: main at 65e59a46b49cd2dbb5c779a4cfae8cef26441984. Only this new directory is changed.

All logarithms are natural. Write eta(x)=-x log x, eta(0)=0, and h(x)=eta(x)+eta(1-x). Throughout, H is the Shannon entropy of the COMPLETE event law p_K(S)=sum_{T superset S}(-1)^(|T|-|S|) det K_T, with empty determinant 1. Define G=H((K-+K+)/2)-(H(K-)+H(K+))/2. A counterexample to entropy concavity would require G<0; a positive counterexample-oriented Jensen difference is J=-G.

## 1. Frozen feasible family and its degeneracies

Let

A=[[a,r],[r,d]], B=[[b,z],[z,e]], 0<A<I2, 0<B<I2,
E=(e1,e2), V=(c1 e1+s1 e3,c2 e2+s2 e4),
cj=(1-tj^2)/(1+tj^2), sj=2tj/(1+tj^2), 0<=tj<=1.

Thus a,d,b,e are in (0,1), r^2<min(ad,(1-a)(1-d)), and z^2<min(be,(1-b)(1-e)). Set DA=ad-r^2, DB=be-z^2. Define K-=E A E^T and K+=V B V^T. Both endpoints have rank exactly two and are legal positive contractions. Their actual arithmetic midpoint M=(K-+K+)/2 is the only midpoint used.

The ranges intersect in dimension zero when t1,t2>0, in dimension one when exactly one tj is zero, and in dimension two when both vanish. Correspondingly, rank M is 4,3,2. If both cj>0 and at least one sj>0, the endpoints do not commute: the upper-right block of their commutator is A C B S, where C=diag(c1,c2), S=diag(s1,s2); A,C,B are invertible and S is nonzero. DA=0 or DB=0 would leave the stated rank-two domain and is not a new rank-one candidate. At t1=t2=1 the two coordinate supports are orthogonal, an already simple block case.

In the physical coordinate order (1,2,3,4), N=2M is

```
[a+b*c1^2, r+z*c1*c2, b*c1*s1, z*c1*s2]
[r+z*c1*c2, d+e*c2^2, z*c2*s1, e*c2*s2]
[b*c1*s1, z*c2*s1, b*s1^2, z*s1*s2]
[z*c1*s2, e*c2*s2, z*s1*s2, e*s2^2]
```

No observation-basis rotation is invoked.

## 2. All midpoint minors, including the mixed terms

Let Fi=Ni,i, Fij=det N_{ij}, Fijk=det N_{ijk}, F1234=det N. Direct expansion gives

```
F12 = DA + DB*c1^2*c2^2 + a*e*c2^2 + d*b*c1^2 - 2*r*z*c1*c2
F13 = a*b*s1^2
F14 = (a*e + DB*c1^2)*s2^2
F23 = (d*b + DB*c2^2)*s1^2
F24 = d*e*s2^2
F34 = DB*s1^2*s2^2
F123 = s1^2*(b*DA + a*DB*c2^2)
F124 = s2^2*(e*DA + d*DB*c1^2)
F134 = a*DB*s1^2*s2^2
F234 = d*DB*s1^2*s2^2
F1234 = DA*DB*s1^2*s2^2.
```

The new mixed pair discriminant is

chi12=a*e*c2^2+d*b*c1^2-2*r*z*c1*c2.

It is a positive quadratic form in (c2,c1), except when both coordinates vanish, because its coefficient matrix has determinant a*d*b*e-r^2*z^2>0. The interference term cannot be discarded, even though the complete quadratic form is nonnegative. All the triple coefficients and the fourth-order determinant above are nonnegative. The verifier independently expands all eleven displayed minors symbolically; these are not obtained by adding two rank-one midpoint theorems.

Put mi=Fi/2, qij=Fij/4, uijk=Fijk/8 and w=F1234/16. These are inclusion minors, NOT complete atoms. Mobius inversion gives the entire sixteen-event law:

```
p1234 = w
pijk  = uijk-w
pij   = qij-uijk-uijl+w                 ({k,l} is the complement of {i,j})
pi    = mi-sum_{j!=i} qij+sum_{T: |T|=3,i in T} uT-w
pempty= 1-sum_i mi+sum_{i<j} qij-sum_{i<j<k} uijk+w.
```

Consequently H(M) is exactly the sum of eta of these sixteen quantities. For t2=0, coordinate 4 is identically absent: w,u124,u134,u234 and every atom containing 4 vanish, but the genuine triple atom p123=u123 remains positive for t1>0. For t1,t2>0, M and I-M are positive definite and all sixteen atoms are positive. No rare event is truncated.

## 3. Exact endpoint entropy and the full Jensen expression

For K-, the only active atoms are (empty,1,2,12), with probabilities

(1-a-d+DA, a-DA, d-DA, DA).

For K+, the four logical probabilities are (1-b-e+DB,b-DB,e-DB,DB). Given occupancy of logical coordinate 1, independently mark it as physical 1 or 3 with probabilities c1^2,s1^2; do the analogous marking into 2 or 4 for logical coordinate 2. This is checked directly: single masses are (b-DB)c1^2,(e-DB)c2^2,(b-DB)s1^2,(e-DB)s2^2; the four cross-group pair masses are DB times the products of their marking probabilities; pairs 13,24 and all higher atoms vanish. Thus

H(K-)=H(A),
H(K+)=H(B)+b*h(s1^2)+e*h(s2^2).

Here H(A) and H(B) mean the four-event two-coordinate entropies, not spectral entropy. The full expression to decide is therefore

G=sum_{S subset [4]} eta(p_M(S))-[H(A)+H(B)+b*h(s1^2)+e*h(s2^2)]/2.

This expression applies to both support geometries without changing the midpoint.

## 4. Full-parameter sign-alignment theorem

**Theorem.** Fix a,d,b,e,|r|,|z| and the two angles. The aligned choice r*z>=0 has no larger G than the opposite-sign choice. The inequality is strict when |r*z|c1*c2>0.

Proof. Endpoint entropies depend on r,z only through their squares. Among all the midpoint minors, only q12 changes when the product changes from +|rz| to -|rz|. Its increase is delta=|rz|c1*c2. Thus the only changed complete atoms are

(pempty,p1,p2,p12) -> (pempty+delta,p1-delta,p2-delta,p12+delta).

The linear interpolation of these four probabilities is a valid law because its endpoints are valid laws. All four probabilities are strictly positive: M<I4, and its upper-left part dominates A/2>0.

For either endpoint law, put L=M(I-M)^(-1) solely to evaluate a fixed kernel. Factoring det(I-M+ZM) proves p_S=det(I-M)det L_S. In particular

p1*p2-pempty*p12=det(I-M)^2*L12^2>=0.

This is an identity for complete atoms conditioned on absence of 3 and 4, not a claim about unconditional pair marginals. It is not an L-affine path.

Let x be the transfer amount, and let W be the sum of the four probabilities (which is fixed and positive). Along the interpolation, the odds numerator minus denominator equals

R(x)=p1*p2-pempty*p12-W*x.

Since R(delta)>=0, R(x)>0 for 0<=x<delta whenever delta>0. The derivative of the FULL entropy is exactly

log[(p1-x)(p2-x)/((pempty+x)(p12+x))]>0.

All other atoms are unchanged. Integrating proves strictness. If delta=0 the two complete laws agree. QED.

This theorem reduces the dangerous sign choice; it does NOT by itself settle the aligned-sign inequality G>=0.

## 5. A continuous, noncommuting, full-strength rank-two exclusion box

Freeze

```
A=[[2/5,6/25],[6/25,2/5]]
B=[[3/5,9/25],[9/25,3/5]].
```

The nonzero endpoint eigenvalues are (4/25,16/25) and (6/25,24/25), respectively. They are not a common small-intensity scaling assumption.

**Theorem.** For every t1,t2 in [0,1/50], the above real affine three-kernel construction satisfies

G > 19/1000.

The open square gives zero-intersection moving supports; either punctured axis gives a one-dimensional intersection. Every point except (0,0) has noncommuting endpoints. This is an explicit angle box, not a finite grid conclusion or a claim about all moving frames.

Proof. Set T=(A+B)/2, R=(A+C B C)/2, wi=si^2, di=Bii*wi/2, and dz=z*(1-c1*c2)/2. The top-coordinate marginal of the four-coordinate midpoint has kernel R. Dropping any occupied bottom coordinates changes a coupled configuration with probability at most d1+d2, by the expected number of bottom points.

For two-coordinate kernels R and T, let Delta=det R-det T. Their four probabilities show directly

TV(p_R,p_T)<=d1+d2+2|Delta|.

The diagonal product changes by at most d1+d2. Both off-diagonal entries have absolute value at most 1/2 because they belong to positive contractions, so their squares differ by at most |dz|. Hence |Delta|<=d1+d2+|dz|. The triangle inequality, including the dropping step, now gives

TV(p_M,p_{E T E^T})<=4(d1+d2)+2|dz|
 <=(2b+|z|)w1+(2e+|z|)w2,

using 1-c1*c2<=w1+w2 for cj in [0,1]. In the frozen box,

w1,w2<=w*=10000/6255001,
TV<=delta*=31200/6255001<15/16.

For probability laws on sixteen symbols at TV distance at most delta<=15/16,

|H(p)-H(q)|<=omega(delta):=h(delta)+delta log 15.

For completeness, couple the two laws with mismatch probability equal to TV. The chain rule with the mismatch indicator bounds the conditional entropy by h(TV)+TV log 15; reverse the roles and use monotonicity up to 15/16. This proves the needed classical inequality directly.

The exact endpoint marking formula gives

G>=Gbase-omega(delta*)-(3/5)h(w*),

where Gbase=H(T)-[H(A)+H(B)]/2. The four base probabilities are

A: (189,186,186,64)/625;
B: (19,231,231,144)/625;
T: (4/25,17/50,17/50,4/25).

The finite logarithm certificate described below encloses

```
Gbase in [0.071729711441392005498563, 0.071729711441392005498564]
omega(delta*)+(3/5)h(w*) <= 0.052057889467810647642976
G >= 0.019671821973581357855588 > 19/1000.
```

Only these finitely many log bounds are numerical. The bound preceding them holds for every parameter in the entire continuous box. QED.

## 6. A certified failure of the rank-one mixture bridge, not of entropy concavity

Use the fixed A,B from Section 5 and t1=1/100. The two cases t2=0 and t2=1/50 give the two requested geometries. Let q=(p_K-+p_K+)/2. Exact rational reconstruction and bounded logarithms give

| geometry | G=H(M)-avg H(end) | H(M)-H(q) |
|---|---|---|
| common line | [0.071868857724917481384897,0.071868857724917481384898] | [-0.009195850054564499168246,-0.009195850054564499168245] |
| zero intersection | [0.072425117028253334474095,0.072425117028253334474096] | [-0.008881971160429267101924,-0.008881971160429267101923] |

The middle matrices have rank 3 and 4. Their commutator Frobenius squares are positive rationals recorded by the verifier. The script separately reconstructs all sixteen atoms by both Mobius inversion and the full signed event determinant.

Thus the extension `H(p_mid)>=H(average endpoint law)` of the PR62 bridge is **DISPROVED**, even for noncommuting moving rank-two endpoints. The actual entropy-concavity inequality is satisfied with substantial slack. These are not entropy counterexamples.

At the actual affine parameter K(t)=(1-t)K-+tK+, t=1/2, the complete curvature intervals are respectively

[-0.518897417989886784319201,-0.518897417989886784319200],
[-0.522053422072399137511766,-0.522053422072399137511765].

The verifier keeps all p,p',p'', the exact full Fisher sum and the entire acceleration sum. An identically zero event is checked to have both derivatives zero; it is not a deleted rare event. These two curvature values are finite checks, not whole-chord curvature theorems.

## 7. Genuine strict interior lifts and error budget

Apply the same map K^eps=eps I4+(1-2eps)K to all three kernels. Its determinant generating polynomial is the one obtained by independently flipping every bit with probability eps; hence it preserves the actual midpoint and puts all spectra in [eps,1-eps]. Let d_eps=1-(1-eps)^4. Then each entropy changes by at most omega(d_eps). A mixture of the two endpoint laws is acted on by the same classical channel, so the same bound also applies to H(q).

At eps=1/100000, the exact certificate gives 2omega(d_eps)<0.001106757502898981675069. Therefore the two true G values remain positive, while the two mixture-bridge differences remain negative. The bounds are respectively

```
common line: G_eps>0.070762100222018499709828;
             bridge_eps<-0.008089092551665517493176.
zero intersection: G_eps>0.071318359525354352799026;
                   bridge_eps<-0.007775213657530285426855.
```

For every member of the continuous angle box and every 0<eps<=1/100000, the same bound gives G_eps>19/1000-0.001106758>0. No arbitrary large interior lift is asserted.

## 8. Reproduction and exact logarithm errors

Run `python research/N4/I05_30_20260910/certify.py`. The script uses SymPy rational determinants and standard-library rational arithmetic for ALL decisive logarithm bounds; high-precision floating-point diagnostics are not a premise.

For rational x>0, write x=2^k y with 1<=y<2 and v=(y-1)/(y+1) in [0,1/3]. Use

log y = 2 sum_{j=0}^{N-1} v^(2j+1)/(2j+1)+R,
0<=R<=2 v^(2N+1)/[(2N+1)(1-v^2)], N=48.

Compute log 2 by the same formula with v=1/3, reversing interval endpoints when multiplying by a negative k. Entropy and curvature intervals use exact rational interval addition and sign-aware scalar multiplication. Printed 24-place decimals are rounded outwards with integer floor/ceiling. Generated `certificate.json` contains all atoms and all midpoint jets.

## 9. Source and route boundaries

Primary sources personally checked: Hough, Krishnapur, Peres and Virag, *Determinantal Processes and Independence*, Probability Surveys 3 (2006), arXiv:math/0503110, Definition 3 and Theorem 7 (PDF printed pp.209-210); Audenaert, arXiv:quant-ph/0610146, classical equations (11)-(12) on PDF p.3 and logarithm convention on p.1. The first supplies the distinction between complete configurations and a Bernoulli-eigenvalue mixture, not a kernel-affine entropy theorem. The second has TV=(1/2) sum|p-q| and base-2 logs; multiplying consistently by log 2 gives the natural-log inequality used here. We also proved its needed classical specialization directly above. URLs: https://arxiv.org/pdf/math/0503110 and https://arxiv.org/pdf/quant-ph/0610146 .

Route A is exact mixed minors and a four-complete-event odds transfer; it proves the sign comparison and falsifies the universal mixture bridge. Route B is a physical-coordinate marginal/drop coupling plus the classical continuity inequality; it proves an entire explicit angular box and its small common bit-flip lift. Neither invokes spectral entropy or follows a curved frame path instead of a matrix midpoint.

Accepted PR62 is used only for scope/source comparison and the already checked bit-flip identity, not as a rank-two theorem. Source and review gates are recorded in accepted_pr62.md and its SECOND report. The `3+3` multiring job #61 remains a separate compact-middle problem; no execution of that issue is assumed. A subsequent complete-law dilute-chord result will be a separate subtheorem, not a weakening silently substituted for the original target.
