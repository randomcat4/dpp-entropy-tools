# Complete tomography kernels and coordinate graph components

Author status: PROVED for the structural theorem and the cross-term cancellation below, pending independent verification. This file alone does not assert the sign of the remaining one-sided coefficients.

The frozen assumptions are those in `../frozen_theorem_v2.md`. All matrices are finite and real, and all exact-event definitions and signs are those of proofs/b_zero_c2_decomposition_v2.md. No assumptions are added to that decision problem.

## 1. Structural theorem

Let U in R^(n by r) have orthonormal columns, with row vectors u_i^T and P=UU^T. Form the coordinate graph on {1,...,n}: distinct i,j are adjacent exactly when P_ij=u_i^T u_j is nonzero. Include isolated vertices. Let its components be E_1,...,E_k, and define

    H_c=span{u_i:i in E_c} subset R^r.

These spaces are mutually orthogonal and their orthogonal direct sum is R^r; a zero row forms an isolated component whose H_c is the zero space. For a real symmetric X, the following are equivalent:

    (i) alpha_R^T X alpha_R=0 for every (r-1)-set R;
    (ii) the compression of X to H_c is zero for every c.

Thus the complete one-hole tomography kernel is exactly the space of symmetric off-block matrices between the H_c. If r_c=dim H_c, its dimension is sum_(c<d)r_c r_d. In particular, a connected nonzero coordinate graph has no nonzero one-hole tomography direction.

## 2. Cofactor polynomial identity

For z=(z_1,...,z_n), let

    G(z)=U^T diag(z) U=sum_i z_i u_i u_i^T.

Expansion by the (r-1)-minors, equivalently the coefficient of a scalar s in det(G(z)+sX), gives

    tr(X adj G(z))
       =sum_(|R|=r-1) z_R alpha_R^T X alpha_R.         (1)

The cofactor vectors have the signed convention fixed in the frozen theorem. One can verify (1) for a rank-(r-1) sum using cofactor expansion and then collect the multilinear coefficients; all terms with repeated row indices vanish. The identity also covers r=1: adj of a scalar is 1, the unique empty-set coefficient is X itself.

Therefore (i) is equivalent to the polynomial on the left being identically zero. For z near the all-ones vector, G(z) is invertible because G(1)=I. Dividing by its determinant gives

    tr(X G(z)^(-1))=0.                                (2)

In particular, replacing z_i by 1-t_i yields the analytic identity

    tr[X(I-sum_i t_i u_i u_i^T)^(-1)]=0               (3)

in a neighborhood of t=0. No formal inverse at a singular matrix is used.

## 3. Every within-component bilinear entry vanishes

The coefficient of t_i in (3) gives u_i^T X u_i=0. Consider distinct vertices i,j in the same component, and choose a shortest graph path

    i=i_0,i_1,...,i_l=j, l>=1.

A shortest path has no repeated vertices and no edge between nonconsecutive vertices in this list; any such edge would shorten the path. Its induced graph is therefore exactly a path. Write P_v=u_v u_v^T. In the Neumann expansion of (3), the coefficient of the squarefree monomial

    t_(i_0)t_(i_1)...t_(i_l)

comes only from the power l+1 and is

    sum_(permutations pi of {i_0,...,i_l})
        tr(X P_(pi_0) P_(pi_1)...P_(pi_l)).             (4)

There are no repeated-index terms in (4): such a term has a repeated variable and cannot contribute to this squarefree monomial. There are no contributions from other powers, because the degree must be exactly l+1.

For an ordered list of distinct vertices,

    tr(X P_(j_0)...P_(j_l))
       =[product_(a=0..l-1)u_(j_a)^T u_(j_(a+1))]
           u_(j_l)^T X u_(j_0).                       (5)

A term can be nonzero only when every consecutive pair is an edge of the induced path. Its only Hamiltonian paths are the forward and reverse orders. Since X is symmetric, these two terms agree. Thus (4) equals

    2[product_(a=0..l-1)u_(i_a)^T u_(i_(a+1))]
           u_j^T X u_i.

Every factor in the product is nonzero by the chosen path. The analytic identity forces u_j^T X u_i=0. This handles paths of length at least two explicitly; no product along a non-shortest path or unaccounted repeated walk is used. Parallel nonzero rows are simply adjacent; zero rows have no neighbors and their bilinear values vanish automatically.

Together with the diagonal case, X vanishes bilinearly on all pairs of rows from the same component, and hence on their span H_c. This proves (i)=>(ii).

## 4. Converse and the low-side graph

Rows from distinct components are orthogonal, so G(z) is block diagonal with respect to the mutually orthogonal H_c. If every diagonal block of X is zero, then tr(X G(z)^(-1))=0 wherever the inverse exists. Multiplying by det G(z) and using polynomial identity extends the equality to all z, and (1) gives (i). This proves the converse.

For the V frame, Q=VV^T=I-P. Its off-diagonal entries are Q_ij=-P_ij, so its coordinate graph is exactly the same graph, including isolated vertices. Its component spans L_c=span{v_i:i in E_c} are mutually orthogonal, with dimensions s_c. Since the coordinate block W restricted to E_c is orthogonal onto its high and low subspaces,

    r_c+s_c=|E_c|.

The one-particle cofactor measurements beta_T are, up to irrelevant signs, the one-hole cofactor measurements for V on complementary sets E\T. This follows from complementary minors of the orthogonal matrix [U V], or from particle-hole complementation of the exact projection law. Hence the same theorem applies to Y: the full one-particle kernel is exactly Y_cc=0 in the L_c decomposition. Zero high/low ranks cause no exception; their associated blocks have zero dimension.

After reordering physical coordinates by E_c and choosing orthonormal bases within H_c,L_c, the frames U and V are block diagonal in these common components. This is an orthogonal change of the internal frames, not an additional assumption about the original data.

## 5. Product support and active cross cancellation

In this component basis the projection law is a product. For an active global r-set S, write S_c=S intersect E_c. Necessarily |S_c|=r_c and each local amplitude psi_c=det((U_c)_(S_c)) is nonzero. Then

    a_S=product_c a_c, a_c=psi_c^2.

The replacement matrix T_S is block diagonal on active sets: an off-component replacement would remove one column from a component and add a low column in another, contradicting their fixed local row counts. Its c-th block is

    (T_S)_cc=(product_(h!=c)psi_h) T_(c,S_c),           (6)

where T_(c,S_c) is the local one-column replacement matrix. Because X_cc=Y_cc=0, the active q_S(X,Y) is a sum over ordered component pairs c!=d of terms

    (product_(h!=c,d)a_h) psi_c psi_d
        tr(X_cd T_(d,S_d) Y_dc T_(c,S_c)^T).           (7)

For every local component,

    sum_(active S_c) psi_c T_(c,S_c)=0.                (8)

Indeed each entry is the inner product, in exterior coordinates, of the projection state with one orthogonal high-to-low column replacement. Cauchy-Binet evaluates that inner product as zero. Including local zero-amplitude sets changes nothing, so (8) is valid on the active support exactly as written.

Sum (7) against log a_S=sum_h log a_h. If the logarithm belongs to c, the unweighted d factor vanishes by (8). If it belongs to d, the c factor vanishes. If it belongs to any other component, both factors vanish. All sums are finite and all logarithms are taken only on positive local amplitudes. Thus

    sum_(S in active support)(log a_S)q_S(X,Y)=0.       (9)

The same argument without a logarithm gives sum_active q_S(X,Y)=0. Therefore simultaneous nonzero X,Y create no active cross term under the full tomography hypotheses, even when the local projection distributions are nonuniform and non-paired.

## 6. Zero-support cross term is also exactly zero

Here a stronger eventwise fact is useful. If det(U_S)=0, then T_S=adj(U_S)V_S. If rank U_S<=r-2, T_S=0. If rank U_S=r-1, write T_S=a b^T, where a spans ker U_S. A nonzero cofactor vector alpha_R for r-1 independent rows R subset S is proportional to a. Thus a^T X a=0.

Choose a row k outside S with u_k^T a!=0; one exists because U has full column rank. The bordered determinant gives beta_(S union {k}) proportional to b, up to the common nonzero factor u_k^T a and a sign. Hence b^T Y b=0. If b=0 the statement is immediate. This also covers r=1 via the empty cofactor vector.

It follows that, separately for every zero-support set,

    q_S(X,C)=q_S(A,Y)=q_S(X,Y)=0,
    q_S(A-X,C+Y)=q_S(A+X,C-Y)=q_S(A,C).                (10)

Thus C_0UV in the public decomposition is exactly zero, rather than merely nonpositive.

## 7. Precisely what has been reduced

Equations (9)–(10) give the exact split

    C2=C_U(U,A,X)+C_V(V,C,Y),

where

    C_U=(tr X^2/2)sum_active a_S(1+log a_S)+C_1U+C_2U,
    C_V=(tr Y^2/2)sum_active a_S(1+log a_S)+C_1V+C_2V.

This proves the reduction to one-sided problems and removes every simultaneous cross term. It does not, by itself, sign C_U or C_V. A separate eventwise derivation is required for that remaining step; no generic data-processing assertion is being used.
