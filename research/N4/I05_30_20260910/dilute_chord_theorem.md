# Every fixed nonconstant real PSD chord is midpoint-safe at sufficiently small common intensity

Status: **PROVED (author proof), PENDING_REVIEW**. This file was developed and added after opening checkpoint PR86, in the same research task. It is a separately stated restricted subproblem, not a replacement for unrestricted moving-rank-two concavity. No novelty claim.

## The precise quantifiers

Let n be finite, let X,Y be distinct real symmetric positive contractions on the ORIGINAL n coordinates, and let M=(X+Y)/2. There exists lambda_*(X,Y)>0 such that for every 0<lambda<=lambda_*,

G(lambda)=H(lambda M)-[H(lambda X)+H(lambda Y)]/2>0.

This includes arbitrary fixed rank-two endpoints, disjoint or intersecting ranges, and n=4,5,6. It does not assert a radius uniform over all X,Y, does not cover pairs themselves changing with lambda, and does not establish concavity at arbitrary intensity. The true chord for each lambda is (1-t)lambda X+t lambda Y. No moving-frame curve, spectral entropy, or L-affine curve appears.

The proof gives a finite explicit remainder procedure and handles the difficult case diag X=diag Y, where the first-order Jensen coefficient is exactly zero.

## 1. Complete atoms and removal of the logarithmic singularity

For a PSD matrix Z, write d_S=det Z_S, d_empty=1. Its scaled complete atom is

p_{lambda Z}(S)=lambda^m q_S(lambda), m=|S|,
q_S(lambda)=sum_{T superset S}(-1)^(|T|-m) lambda^(|T|-m) d_T.

If d_S=0, then every d_T with T superset S is zero. Indeed, represent Z as the Gram matrix of row vectors: dependence of the vectors indexed by S persists in every larger set. Hence this atom is identically zero, not a small event discarded in an approximation.

Otherwise q_S(0)=d_S>0, so q_S is positive in a neighborhood of zero. The expected cardinality identity, derived by summing the one-coordinate inclusion probabilities, is EXACT:

sum_S |S| p_{lambda Z}(S)=lambda tr Z.

Consequently the function

F_Z(lambda)=H(lambda Z)+lambda tr Z log lambda
          =-sum_{S:d_S>0} lambda^|S| q_S(lambda) log q_S(lambda)

extends to a real analytic function at lambda=0. This includes all active events of every cardinality. In particular, there is no unaccounted lambda^2 log lambda or lambda^3 log lambda remainder. The cardinality-weighted cancellation uses the complete law, not a pair truncation.

## 2. Exact first and second coefficients

Put a_i=Z_ii, d_ij=a_i a_j-Z_ij^2 and b_i=sum_{j!=i}d_ij. Expanding the analytic F_Z gives

H(lambda Z)=-lambda tr Z log lambda+lambda A(Z)+lambda^2 C(Z)+R_Z(lambda),

A(Z)=sum_i a_i(1-log a_i), with 0(1-log0)=0,

C(Z)=E2-(tr Z)^2/2+sum_i b_i log a_i-sum_{i<j}d_ij log d_ij,
E2=sum_{i<j}d_ij.

Terms whose coefficient is zero are interpreted by continuity; if a_i=0 then its whole row and b_i vanish.

To check the coefficient rather than cite it: p_empty=1-lambda tr Z+lambda^2 E2+O(lambda^3); its contribution to F has second coefficient -E2-(tr Z)^2/2. The singleton contribution is lambda^2 sum_i b_i(1+log a_i). The pair contribution is -lambda^2 sum d_ij log d_ij. The sum of b_i is 2E2. All size>=3 terms are included in R and in the explicit bound below. Adding these quantities gives exactly C(Z).

Equivalently, define for u>0 and |v|<=sqrt(u),

Psi_u(v)=v^2+(u-v^2) log(1-v^2/u),
Psi_u(+-sqrt(u))=u, Psi_0(0)=0.

Then

C(Z)=-1/2 sum_i a_i^2-sum_{i<j}Psi_{a_i a_j}(Z_ij).

This follows from b_i's definition and E2-(tr Z)^2/2=-1/2 sum a_i^2-sum Z_ij^2. It is an expression in the physical matrix entries, not the nonzero eigenvalues.

## 3. Strict sign of the first nonzero Jensen coefficient

Let alpha=A(M)-[A(X)+A(Y)]/2 and beta=C(M)-[C(X)+C(Y)]/2. The lambda log lambda terms cancel by linearity of trace, so

G(lambda)=alpha lambda+beta lambda^2+O(lambda^3).

The scalar function x(1-log x) is strictly concave on [0,1]. Thus alpha>=0, with equality exactly when diag X=diag Y. If the diagonals differ, alpha>0 and the first-order coefficient gives the desired strict sign for sufficiently small lambda.

Now suppose diag X=diag Y=a. The diagonal square terms in C cancel, and

beta=sum_{i<j} { [Psi_{a_i a_j}(X_ij)+Psi_{a_i a_j}(Y_ij)]/2
                 -Psi_{a_i a_j}((X_ij+Y_ij)/2) }.

Each summand is nonnegative. On the open interval |v|<sqrt(u),

Psi'_u(v)=-2v log(1-v^2/u),
Psi''_u(v)=-2 log(1-v^2/u)+4v^2/(u-v^2).

The second derivative is positive except at v=0. It follows that Psi' is strictly increasing on any nondegenerate subinterval, and therefore Psi is strictly convex on its closed domain by continuity at the two endpoints. If a_i a_j=0, PSD forces both corresponding matrix entries to vanish. Since X!=Y and their diagonals agree, at least one pair has different entries with a_i a_j>0. That pair gives a strictly positive contribution. Hence beta>0.

This proves the qualitative theorem. The following remainder estimate makes the sufficiently small interval explicit rather than leaving it as an unbounded O-term.

## 4. An explicit finite all-event remainder bound

For each of Z=X,Y,M and each active S, write q_S(lambda)=sum_{k=0}^{n-m} c_{S,k}lambda^k, d=c_{S,0}>0, m=|S|. Let

rho=min(1/2, all d/[2 sum_{k>=1}|c_{S,k}|]),

where terms with zero denominator are omitted. This is a positive minimum over a finite list. For |lambda|<=rho, q_S lies in [d/2,3d/2]. Because Z is a contraction, d<=1.

For j=0,1,2,3 define finite nonnegative coefficient bounds

Q_j=sum_{k>=j} (k)_j |c_{S,k}| rho^(k-j),
P_j=sum_{m+k>=j} (m+k)_j |c_{S,k}| rho^(m+k-j),

where (k)_j=k!/(k-j)!. Q_j bounds |q_S^(j)|, and P_j bounds |(lambda^m q_S)^(j)|. Set

L0=log(2/d),
L1=2 Q1/d,
L2=2 Q2/d+4 Q1^2/d^2,
L3=2 Q3/d+12 Q1 Q2/d^2+16 Q1^3/d^3.

These respectively bound log q_S and its first three derivatives in absolute value. The L0 bound follows from q_S in [d/2,3d/2] and d<=1. The remaining bounds follow by explicitly differentiating log q_S.

Define

M_Z=sum_{S active} sum_{j=0}^3 binom(3,j) P_j L_(3-j),
B=[M_M+(M_X+M_Y)/2]/6.

Leibniz's rule and Taylor's theorem give, for 0<=lambda<=rho,

|R_Z(lambda)|<=M_Z lambda^3/6,
|G(lambda)-alpha lambda-beta lambda^2|<=B lambda^3.

Every active triple, quadruple and higher event appears in M_Z. Only identically zero events are excluded after their exact algebraic zero has been proved.

For unequal diagonals an explicit sufficient radius is

lambda_* = min(rho, alpha/[4(|beta|+1)], sqrt(alpha/[4(B+1)])).

Then G(lambda)>=alpha lambda/2>0. For equal diagonals use

lambda_* = min(rho, beta/[2(B+1)]),

which gives G(lambda)>=beta lambda^2/2>0. For rational input, any rigorously enclosed positive lower bounds on alpha or beta and upper bounds on the other constants give a rational smaller radius. There is no unproved exchange of limits, derivatives, or event summation: all sums are finite.

## 5. Two dense equal-diagonal rank-two checks, not coordinate-rotated entropy surrogates

The separate fixed-input script `dilute.py` uses

```
F=[[1,0],[0,1],[3/5,4/5],[5/13,12/13]]
G1=[[1,0],[0,1],[3/5,4/5],[5/13,-12/13]]
G0=[[1,0],[0,1],[5/13,12/13],[8/17,15/17]].
X=F F^T/4, Y_j=G_j G_j^T/4.
```

All actual kernel diagonals equal 1/4. All kernels have rank two and trace one, hence their nonzero eigenvalues lie strictly between zero and one. No matrix is replaced by a diagonalized equivalent for entropy. F and G1 share their first column, while the concatenated column ranks are 3 and 4 for G1 and G0 respectively; the script verifies these ranks exactly. Both commutators are nonzero.

Executed exact-log certificates:

| case | beta interval | common rho | integer B upper bound | a certified whole intensity interval |
|---|---|---|---|---|
| one-dimensional intersection | [0.060684530887951208035148,0.060684530887951208035149] | 1352/3587 | 32 | (0,1/10000] |
| zero intersection | [0.003482764639508454401382,0.003482764639508454401383] | 625164800/1489794489 | 25 | (0,1/100000] |

At the upper endpoint of those intervals, direct complete-atom G lies respectively in

[0.000000000606875261215902926935112965,0.000000000606875261215902926935112966],
[0.000000000000348278085597162431775109,0.000000000000348278085597162431775110].

The theoretical lower bounds beta_lower*lambda^2/2 are strictly positive and lie below these direct intervals. The direct evaluation is a consistency check; the all-lambda proof is the explicit Taylor remainder above.

The full-intensity values at lambda=1 are also positive in these TWO fixed examples, respectively [0.112791827525133146694754,0.112791827525133146694755] and [0.005449388298622989765710,0.005449388298622989765711]. They do not extend the theorem's intensity interval or prove other full-intensity chords.

Run `python research/N4/I05_30_20260910/dilute.py`. It imports the adjacent exact logarithm and complete-event primitives from `certify.py`, keeps every q polynomial, and emits `dilute_certificate.json`. All decisive arithmetic uses rational log enclosures, not decimal sampling. This is author execution, not independent review.

## Scope and comparison with the earlier checkpoint

The explicit angular-box theorem fixes two strong nonzero endpoint spectra and permits a continuous two-angle motion. The present theorem instead fixes arbitrary actual endpoint matrices, including equal-diagonal dense examples outside that canonical angular box, and proves a sufficiently small common-intensity interval. Neither theorem implies the other with its stated quantitative scope. Neither settles the aligned-sign canonical family at all angles, arbitrary moving rank-two endpoints at full intensity, or the multiring intermediate-coupling question.

The proof is self-contained from the complete-event definition. The DPP mixture representation of HKPV, arXiv:math/0503110, is background only and does not supply the entropy expansion or its sign. The sign is proved above from exact coefficients and the displayed strict convexity calculation. The continuity source audited in the companion file does not prove this second-order equal-diagonal result. Novelty/priority remain unassessed.
