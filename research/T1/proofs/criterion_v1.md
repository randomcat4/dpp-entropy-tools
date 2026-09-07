# Bridge-supported imaginary curvature: proof v1

Mathematical status: PROVED by the author under `../frozen_theorem_v1.md`; independent verification PENDING. No premise is added below. No claim of literature novelty or machine-checked proof is made.

## 1. Positivity and local differentiability
Set L = K(I-K)^{-1}. The matrices K and I-K commute and are positive definite, so L is positive definite. The finite DPP has mass det(L_S)/det(I+L) at S; every principal minor in its numerator is positive (the empty determinant is 1). Equivalently this is the signed determinant formula in the frozen statement. One can verify the equivalence by multiplying K-I_{S^c} on the left by I+L: the columns indexed by S become columns of L and those indexed by S^c become negative coordinate columns. Expansion in the latter columns gives the signed principal minor.

The same argument holds for Hermitian strict contractions. If delta is the smaller of the least eigenvalues of K and I-K, then delta > 0 and |t| ||D||_op < delta implies 0 < K+tD < I. Thus all masses are positive near zero; a finite sum of their logarithms is smooth. For D=0 this is immediate.

## 2. Exact two-endpoint reduction for a single bridge
Fix a bridge e={u,v} in G(K), with weight z=K_uv != 0. Removing the bridge partitions its original connected component into sets V_1 containing u and V_2 containing v. Assign all other connected components to either side, obtaining a partition V=V_1 disjoint union V_2 whose only possible cross-entry is (u,v) and its adjoint. Keep all entries except z and its adjoint fixed, allowing z to vary complexly in a neighborhood of its original value that preserves the strict contraction property.

Write U={u,v}, R=V minus U. Fix any event T subset R, meaning X intersect R = T, and put

Q_T = K_R - I_{R minus T},

w_T = (-1)^{|R minus T|} det Q_T.

Marginalizing a DPP restricts its marginal kernel, as follows directly from the defining inclusion probabilities det(K_B) for B subset R and finite inclusion-exclusion. Thus w_T is the probability of the event on R. It is positive by Section 1 applied to K_R. Crucially, K_R and w_T do not involve z. Consequently Q_T is invertible. All these assertions include R empty with determinant 1 and the empty inverse convention.

In the coordinate order R,U, block determinant factorization gives, for every E subset U,

p_{T union E}(K) / w_T
 = (-1)^{|U minus E|} det(M_T - I_{U minus E}),

M_T = K_U - K_{U,R} Q_T^{-1} K_{R,U}.

This is the Schur complement identity applied to the signed event determinant; its signs split into those for R and U. Q_T is block diagonal between R intersect V_1 and R intersect V_2. The u row of K_{U,R} is supported only on the first part, and the v row only on the second. Therefore the correction K_{U,R}Q_T^{-1}K_{R,U} is diagonal. The matrices in that correction are independent of z. We conclude

M_T = [[a_T,z],[conj(z),b_T]],

where a_T,b_T are real and independent of z. This explicitly proves that conditioning does not introduce a hidden z-dependent diagonal or event weight.

Put q=|z|^2. The conditional probabilities for the two endpoint indicators are

r_11 = a_T b_T - q,
r_10 = a_T(1-b_T) + q,
r_01 = (1-a_T)b_T + q,
r_00 = (1-a_T)(1-b_T) - q.

They are all positive because each is the quotient of a positive full event mass and w_T. They sum to one, and the endpoint marginals show 0<a_T,b_T<1. They remain positive in a neighborhood of the original q>0: for instance choose z(q)=sign(z_original) sqrt(q), and use the openness from Section 1. There is no boundary differentiation here.

## 3. Entropy strictly decreases with a nonzero bridge's squared magnitude
Define h_T(q)=-sum_{alpha,beta in {0,1}} r_{alpha beta}(q) log r_{alpha beta}(q). Since the four derivatives in the order (11,10,01,00) are (-1,+1,+1,-1), differentiating gives

h_T'(q) = log[(r_11 r_00)/(r_10 r_01)].

Direct expansion of the four displayed probabilities gives

r_11 r_00 - r_10 r_01 = -q.

For q>0 the ratio is strictly between zero and one; hence h_T'(q)<0. By the entropy chain rule and the z-independent weights from Section 2,

H(K(q)) = H(X intersect R) + sum_{T subset R} w_T h_T(q),

and consequently

partial H / partial q_e = sum_T w_T log[(r_11 r_00)/(r_10 r_01)] < 0.  (1)

The event sum is used to prove the sign. The checking algorithm never evaluates this sum. No conditional entropy inequality or unverified sign assumption is used.

## 4. Several bridge phases produce no second-order cross term
Let B be the collection of all bridges of G(K), and keep the nonbridge entries fixed. In the permutation expansion of any event determinant det(K-I_{S^c}), an occurrence of a bridge entry K_uv in a nonzero term must be paired with K_vu in the same permutation cycle of length two. Indeed a permutation cycle of length at least three containing {u,v} would give an undirected simple cycle in G(K) containing that edge, contradicting the bridge property. Diagonal changes do not affect this argument.

Thus every event mass is a polynomial in the real variables q_e=|K_uv|^2 for e in B, with coefficients depending only on the fixed nonbridge entries and the diagonal. Individual bridge phases disappear, and no bridge can appear to a higher power than one in a determinant term. The latter degree observation is not needed for the sign proof.

Every q_e at the center is strictly positive. Replacing each bridge weight by its original sign times sqrt(q_e) constructs real symmetric matrices continuously in an open neighborhood of the center q. Shrink this neighborhood so all are strict contractions. Therefore H is a smooth function F(q) there. Section 3, applied separately to every bridge with all other entries fixed, proves partial_e F(q)<0 at the center.

On the frozen affine path K+t iA, the nonbridge entries are fixed and

q_e(t)=K_uv^2+t^2 A_uv^2.

The preceding determinant argument gives H(K+t iA)=F(q(t)) near zero. The chain rule, using q_e'(0)=0, yields

H''(K)[iA] = 2 sum_{e={u,v} in B, u<v} A_uv^2 partial_e F(q).  (2)

Each summand is nonpositive by (1). If A != 0, its skew-symmetry and allowed support ensure some A_uv != 0 on a bridge, and that summand is strictly negative. If A=0 all summands vanish. This proves exactly the frozen theorem.

## 5. Non-enumerative decision procedure
Input exact K,A. Verify their dimensions, K=K^T, A=-A^T, and strict positivity of K and I-K. Build G(K) using exact zero tests. Find all bridges by a depth-first low-link algorithm. Reject applicability if any nonzero upper-triangular A entry lies outside the bridge set. Otherwise output curvature zero when A=0 and strictly negative when A != 0.

Dense matrix input requires O(n^2) reading and zero checks. Strict positive definiteness takes O(n^3) arithmetic operations by LDL^T elimination; bridge detection takes O(n+m), where m is the number of nonzero off-diagonal entries above the diagonal. Storage is O(n^2). These are arithmetic counts, not a bound independent of coefficient bit length. The supplied rational implementation uses exact fractions, no thresholds or logarithms. Positive LDL pivots certify both strict inequalities. A rejected input is outside this sufficient test, not a disproved curvature statement. For nonrational measured input, a rigorous enclosure and exact support information would be required; no floating-point support certificate is claimed.

## 6. Unbounded application family
Take any finite collection of vertex-disjoint dense real symmetric blocks and connect them by one nonzero weighted edge for each edge of a tree on the blocks. There are no other interblock entries. Let W be the resulting symmetric weighted adjacency matrix with zero diagonal, and R_*=max_u sum_{v != u}|W_uv|. For any 0<epsilon R_*<1/2, set K=(1/2)I+epsilon W. Gershgorin's bound gives all eigenvalues in (0,1). Every interblock link is a bridge, independently of cycles within each dense block. Therefore every nonzero imaginary skew direction supported on any selection of those links has strictly negative entropy curvature.

This family allows arbitrarily many blocks and arbitrarily large dense blocks; it is not restricted to a forest kernel, a two-point DPP, or independent blocks. The criterion avoids a 2^n event calculation even when a dense block by itself would be expensive to enumerate. The example generator supplies two triangles linked by one edge as a six-vertex instance, in addition to tree cases.

## 7. Boundaries and dependency ledger
- Strict interior is used in Sections 1-3; this proof does not assert a finite derivative at a zero-probability boundary.
- The nonzero support definition is necessary for strictness: a new imaginary edge at a diagonal center may have zero second derivative.
- On a cyclic edge, a permutation cycle can carry its phase. Also the Schur correction to the endpoint off-diagonal can be nonzero. Hence Sections 2 and 4 no longer apply; failure of this proof is not a counterexample.
- Arbitrary real directions on several bridges have q'(0) != 0, so omitted mixed terms return. No claim about them is made.
- Only the derivative at zero is proved, not global line concavity.
- KNOWN and justified here: finite DPP mass and marginal formulas, Schur determinant identity, entropy chain rule, openness of positive definiteness, elementary determinant cycle expansion.
- PROVED_HERE: the bridge-specific conditional form, its strict squared-magnitude derivative, and their use in (2).
- Independent proof review and literature novelty are separate pending obligations. No Lean project is present in this checkout; no formal verification was performed.
