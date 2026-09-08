# D10-U3/S9 independent non-author audit

STATUS: **CORRECT**, for the frozen pointwise punctured-dense-cone theorem,
its fixed-dimension compact uniform version, and its pointwise open-neighborhood
consequence. No critical gap requiring a repair was found.

This does not certify global concavity, a sparse-support extension, an explicit
epsilon threshold, or a uniform-radius neighborhood including epsilon=0.

## 1. Hash binding and verified dependency

The following author SHA256 values were identical before and after the audit's
independent exact calculation:

| File | SHA256 |
| --- | --- |
| frozen_problem.md | 111f6786d6a0abae754a6264e26e53ae56831de7163cfd2e34266adae4458fff |
| proof_candidate.md | fa21a6076b90c835cd2222931bcceeb1ce55090efaa2b4a4b7a4808f204b451f |
| verdict.md | 46b91a5835cec3e72f9ef7162297e62d66c74bbfba467eb84fc7b84726ae4350 |

The supplied U2 dependency is the corrected `diagonal_flat_ridge/proof.md`,
SHA256 `e3bc5a365a56801fdd192e909656b4b8167b77c773eee24e516f081a3a3c5e22`,
matching its revised independent audit. Its quantified fourth-order identity
is available for every strict diagonal x and every real zero-diagonal symmetric
Z, not merely one preselected line.

## 2. Does a radial formula determine the whole fourth-order tensor?

Yes, with the actual U2 quantifiers. At a fixed x let T_k=D_z^k F(x,0).
Analyticity makes T_k a symmetric k-linear tensor. The homogeneous polynomial
P_k(z)=T_k[z,...,z] determines every tensor component: the coefficient of a
monomial z^alpha with |alpha|=k is (k!/alpha!) times the corresponding
component. The nonzero combinatorial factors can be divided out over the
reals. Equivalently one can use the polarization identity.

Thus a polynomial zero for EVERY z has every component zero. Applied for
k=1,2,3, the U2 radial zeros give T_k=0. For k=4, the U2 polynomial

    T_4[z,z,z,z] = -12 sum_e c_e(x) z_e^4

forces T_4[e,e,e,e]=-12c_e and every mixed-edge component to vanish.
The quartic Taylor term is T_4[z^4]/4! = -(1/2)sum_e c_e z_e^4.
It is not an inference from negativity of a radial fourth derivative alone;
it uses the complete explicit polynomial identity for all z. This distinction
is the central load-bearing step, and the author has the stronger input needed.

The coordinate e represents K_ij once, while its matrix direction is
E_ij+E_ji. U2 uses that same matrix entry Z_ij. Hence no factor 2 or sqrt(2)
is lost in translating its -12 to the Taylor coefficient -1/2 or the
off-diagonal-coordinate Hessian coefficient -6.

## 3. x derivatives and the differentiated remainder

The identities T_1(x)=T_2(x)=T_3(x)=0 hold throughout the open diagonal domain
(0,1)^n. Their component functions are analytic in x; every x derivative of
each such zero component is consequently zero. They are not zeros restricted
to a single x, so mixed derivatives such as D_x D_z^2 F do vanish as used.

For a neighborhood of a fixed strict x, a convergent parameterized Taylor
expansion has the form

    F(x,z)=h(x)-(1/2)sum_e c_e(x)z_e^4
                +sum_{|alpha|>=5}r_alpha(x)z^alpha.

The coefficient functions and required derivatives are analytic. On a smaller
compact neighborhood the series and its relevant derivatives converge uniformly.
Differentiating in x does not reduce z degree; differentiating once or twice
in z reduces it by at most one or two. Therefore

    R_xx=O(||z||^5), R_xz=O(||z||^4), R_zz=O(||z||^3)

in finite-dimensional operator norm, locally uniformly in x. Differentiating
a bare scalar O(||z||^5) assertion would not by itself justify this conclusion,
but the analytic parameterized expansion explicitly supplied here does.

The quartic term contributes orders z^4 to F_xx, z^3 to F_xz, and the exact
diagonal quadratic matrix -6 diag(c_e z_e^2) to F_zz. Therefore the author's
orders 1, epsilon^3, epsilon^2 with respective errors O(epsilon^4),
O(epsilon^3), O(|epsilon|^3) are correct. There is no missing order-epsilon
or order-epsilon-squared mixed block.

## 4. Schur complement: sign and quantitative dominance

Let P=F_xx, Q=F_xz, R=F_zz. The relevant Schur complement when P is negative
definite is

    S=R-Q^T P^{-1}Q.

Since P^{-1} is negative definite, the correction -Q^T P^{-1}Q is positive
semidefinite, not negative. The phrase "negative Schur complement" in the
author text should be read as a Schur complement shown negative, not a claim
that its correction has negative sign. Equation (7)'s unsigned O(epsilon^6)
is valid with the actual positive correction and suffices for the proof.

For explicit domination, put c0=lambda_min C(x)>0 and
d0=6 min_e c_e(x)a_e^2>0. For fixed x,A, choose finite constants M1,M2,M3
on a sufficiently small analytic tube so that

    ||P+C|| <= M1|epsilon|^4,
    ||Q|| <= M2|epsilon|^3,
    ||R+6epsilon^2 diag(c_e a_e^2)|| <= M3|epsilon|^3.

Choose epsilon small enough to satisfy

    M1|epsilon|^4 <= c0/2,
    M3|epsilon| <= d0/4,
    (2M2^2/c0)|epsilon|^4 <= d0/4.

Then P<=-(c0/2)I, ||P^{-1}||<=2/c0, and

    S <= -d0 epsilon^2 I + (d0/4)epsilon^2 I
                           + (d0/4)epsilon^2 I
      = -(d0/2)epsilon^2 I < 0

for either sign of nonzero epsilon. These inequalities remain meaningful if
one of the M's is zero. Negative P and negative S imply full negative
definiteness by the standard block congruence. Thus the O(epsilon^6) correction
cannot reverse the conclusion. The inverse bound is uniform as epsilon tends
to zero because only the nondegenerate x block is inverted.

This proves negativity for every real coordinate vector (diagonal and
off-diagonal variations together), not merely for the original radial A or
for variations preserving x. The coordinate map to Sym(n) is an invertible
linear map, so negative definiteness transfers to arbitrary symmetric D even
though this coordinate norm is not the Frobenius norm.

## 5. Full edge support: what is and is not necessary

The hypothesis a_e!=0 for every edge is exactly what makes the leading
epsilon^2 matrix in F_zz positive definite after sign reversal. If one a_e
is zero, d0 becomes zero and THIS dominance proof stops. The supplied U2
quartic term cannot decide the curvature of that edge coordinate at the
sparse ray; higher terms would be needed.

This is a sufficient nondegeneracy premise for the theorem and a needed premise
for this leading-order proof. It has not been proved to be a necessary condition
for full-Hessian negativity itself. The author correctly makes no such iff
claim and explicitly excludes sparse A. No sparse-case counterexample is
required to justify that scope boundary.

## 6. Uniform compact quantifiers and nonvacuity

For the uniform version n is FIXED, 0<a<=b<1 is FIXED, and eta>0 is FIXED.
The set of zero-diagonal symmetric A with ||A||_F=1 and all |A_ij|>=eta is
closed and bounded. It can have several sign components; compactness does not
require connectedness. In edge coordinates ||(A_ij)_{i<j}||_2=1/sqrt(2), not 1,
which is harmless for uniform boundedness and Taylor constants.

The parameter set is nonempty exactly when eta<=1/sqrt(n(n-1)): necessity
follows from 1=2sum_{i<j}A_ij^2>=n(n-1)eta^2; sufficiency follows by choosing
all edge magnitudes 1/sqrt(n(n-1)). If eta exceeds this value, the stated
universal claim is vacuous, not false. An optional editorial improvement is
to display the nonempty range, but this is not a critical gap.

There is one analytic tube for x in [a,b]^n: first thicken this box slightly
inside (0,1)^n, then use the strictly positive product-law atoms at z=0 and
compactness to choose a single small z radius keeping every atom positive.
Equivalently the finite signed-determinant derivatives give a uniform atom
floor. Smoothness on a smaller compact tube bounds all derivatives required
for the parameterized remainders. This works also when a=b, since the ambient
analytic domain, not the relative interior of the box, defines x derivatives.

On the compact family C(x)>=4I and c_e(x)>=16, so one may use c0=4 and
d0=96eta^2 in the preceding domination argument. Remainder constants M1,M2,M3
are uniform on that tube, and A's norm is fixed. Thus one epsilon_0 depending
only on n,a,b,eta exists and works simultaneously for all base x, all allowed
A, every 0<|epsilon|<epsilon_0, and every nonzero symmetric test direction D.
There is no uniform threshold claimed over all n, all eta approaching zero,
or all unnormalized A.

## 7. Strict kernels, open neighborhoods, and epsilon=0

For fixed X let s=min_i{x_i,1-x_i}>0. Since
||epsilon A||_op<=|epsilon| ||A||_F, strictness follows whenever
|epsilon| ||A||_F<s. In the normalized compact family s>=min(a,1-b), so the
same strict-feasibility restriction can be imposed uniformly. Shrinking
epsilon_0 by it preserves every preceding estimate.

At each nonzero allowed epsilon, the full Hessian has strictly negative maximum
eigenvalue in the finite coordinate space. The kernel remains a positive
distance from the strict boundary at that fixed point, so operator-norm
continuity gives an open strict-kernel neighborhood where the entire Hessian
is still negative definite. This is uniform in test directions at that point;
it is not a collection of unrelated directionwise neighborhoods.

The neighborhood radius may shrink as epsilon tends to zero. No ordinary
neighborhood including the diagonal ridge can have a negative-definite full
Hessian everywhere, since F_zz(x,0)=0. The frozen punctured-ray/cone statement
and individual open neighborhoods do not make that forbidden claim.

## 8. Independent exact multivariate sanity

The new standard-library script `independent_quartic_check.py` imports no
author module. It builds inclusion determinant polynomials in EVERY edge
variable for heterogeneous rational centers in dimensions 2,3,4, then performs
exact Mobius inversion. It verifies all mass and singleton polynomial identities
and the absence of first-order atom terms. Since the base log atom is affine
in singleton indicators, those exact identities cancel every linear entropy
term in the atom perturbation.

The entire surviving quartic polynomial is computed as

    -sum_S [p_{S,degree2}(z)]^2/(2p_S(0)),

and compared coefficientwise with -(1/2)sum_e c_e z_e^4. This checks all mixed
monomials rather than probing a few radial evaluations. Differentiating that
polynomial twice verifies the full leading z-Hessian and its factor -6.

Complete finite denominator: 3 parameter centers, 28 atom polynomials, 10
surviving pure quartic coefficients, and 46 leading edge-Hessian entries.
Every coefficient comparison passed; no random draws or discarded cases.
This is a sanity supplement, not the justification for the general-n proof.

Command from the repository root, bundled Python 3.12:

```
python research/R3/deepening_10h/dense_hessian/punctured_diagonal_full_hessian/verifications/independent_quartic_check.py
```

Exit 0, elapsed 0.007938623428344727 seconds. Full exact denominators and author
hashes are in `independent_quartic_results.json`.

Script SHA256:
`ecbcccdad2ff92968a92d2882c573d211f29a0988a8dcbbc24d17afd0f622853`

Results SHA256:
`c668c7c73e5d94abdebacc6095e41c1ac1b3580de0a60fd5360b5c8e64d0b2db`

No author file or shared index was modified. No submission was made. Final
verdict remains CORRECT in the explicitly frozen local scope; the optional
Schur-sign and eta-nonvacuity clarifications do not require a proof repair.
