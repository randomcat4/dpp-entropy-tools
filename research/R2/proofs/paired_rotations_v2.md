# General paired rotations have the same second-order coefficient

Author status: PROVED as an extension of `paired_frame_C2_v2.md`, pending
independent verification. This is an analytic extension, not a numerical
inference.

## Statement

For each independent coordinate pair i, take fixed real vectors

    u_i=(alpha_i,beta_i),
    v_i=(-beta_i,alpha_i), alpha_i^2+beta_i^2=1.

The i-th columns of U and V are u_i and v_i on that pair and zero elsewhere. Keep the positive diagonal A,C, zero-diagonal symmetric X,Y, and full endpoint feasibility A+/-X>=0,C+/-Y>=0 from `paired_frame_C2_v2.md`. Then the exact same formula holds:

    Delta_e=C2 e^2+O(e^3|log e|),
    C2=-sum_(i<j)
       [G_(a_i a_j)(x_ij^2)+G_(c_i c_j)(y_ij^2)].       (1)

There is no angle-dependent factor. Degenerate angles alpha_i=0 or beta_i=0 are allowed. Both one-flip measurement kernels are still exactly the zero-diagonal symmetric matrices, each of dimension m(m-1)/2.

## Weighted event laws

Let each single-coordinate choice z_i in pair i have probability

    p_i(z_i)=u_i(z_i)^2,
    h_i=-sum_(z_i) p_i(z_i)log p_i(z_i),
    H_P=sum_i h_i.

The supported projection law consists of choosing one coordinate in each pair, with product probability P_z=product_i p_i(z_i), restricted to its positive values. Empty/double-pair events have the same formulas as in `paired_frame_C2_v2.md` except that the uniform powers of 2 are replaced by product weights on the remaining single pairs. Indeed det[u_i,v_i]=1 for every pair; an empty pair deletes its high coordinate, and a double pair has this unit determinant. In particular:

- A one-empty-i event with remaining single weight w has first rate w a_i and second-coefficient difference w sum_(j!=i)x_ij^2.
- A one-double-i event has first rate w c_i and difference w sum_(j!=i)y_ij^2.
- A two-empty-{i,j} event has leading coefficient w(a_i a_j-x_ij^2), compared with w a_i a_j at the center.
- A two-double-{i,j} event has leading coefficient w(c_i c_j-y_ij^2), compared with w c_i c_j.
- A mixed empty-i/double-j event has leading coefficient w a_i c_j, unchanged across the chord.

These facts follow from the full exact spectral mixture and its cofactor/replacement minors, as in the main paired proof. Every nonzero one-hole cofactor is a nonzero multiple of e_i, and every one-particle cofactor is likewise a multiple of e_i. For every i a positive-weight choice of all other coordinates exists. Thus the measurements observe every diagonal entry and no off-diagonal entry, proving the asserted exact kernel dimensions even at degenerate angles.

## The supported cross terms cancel without uniform probabilities

For a supported choice z, define rho_i(z_i)=v_i(z_i)/u_i(z_i). Its replacement matrix is the projection amplitude times diag(rho_i). The endpoint-minus-center second coefficient is

    delta b_z=-P_z[sum_(i<j)(x_ij^2+y_ij^2)
                      +2sum_(i<j)x_ij y_ij rho_i rho_j].  (2)

All sums here are over positive-probability coordinate choices, so these ratios are well-defined. Orthogonality gives

    E_p[rho_i]=sum_(z_i:p_i(z_i)>0)u_i(z_i)v_i(z_i)=0.

At a degenerate angle the excluded terms have u_i=0 and contribute zero to this orthogonality identity. For i!=j, independence and log P_z=sum_k log p_k(z_k) yield

    E_P[rho_i rho_j]=0,
    E_P[rho_i rho_j log P_z]=0.                         (3)

In the second identity, a log factor on i still leaves E[rho_j]=0, a factor on j leaves E[rho_i]=0, and a factor on any other coordinate leaves both zero. The finite sums are over their positive support and have no undefined logarithms.

Since f'(P_z)=-log P_z-1, (2) and (3) eliminate every X/Y cross term. The remaining supported entropy contribution is

    (1-H_P)sum_(i<j)(x_ij^2+y_ij^2).                   (4)

Uniform probabilities were therefore not essential to this cancellation.

## The angle entropies cancel pair by pair

Consider one unordered pair i,j and the high-side quantity z=x_ij^2,D=a_i a_j. One-empty-i events contribute coefficient H_P-h_i-1-log a_i times their sum of squared off-diagonal entries. The contribution at j is analogous. Together with (4), the coefficient multiplying z before the two-hole term is

    [H_P-h_i-h_j-1-log D]z.                            (5)

The weights on the other m-2 pairs have entropy H_P-h_i-h_j and total mass 1. Consequently the finite two-hole difference is

    f(D-z)-f(D)-(H_P-h_i-h_j)z.                        (6)

Combining (5) and (6) gives exactly -G_D(z). The low-side calculation gives -G_(c_i c_j)(y_ij^2). The logarithmic cancellations are unchanged because all remaining-coordinate weights sum to 1. This proves (1) at every nondegenerate set of angles.

## Degenerate angles and zero-event checks

No limit-exchange argument is needed to include alpha_i=0 or beta_i=0. The preceding sums use the actual positive support and remain valid. The additional zero projection events are treated directly:

1. A nominal all-single configuration selecting a zero-U coordinate in exactly one pair k has a replacement matrix with only its (k,k) entry potentially nonzero. Its order-e^2 probability is that entry's square times H_kk L_kk=a_k c_k, unchanged at both endpoints and at the center.
2. If such a configuration uses zero-U coordinates in at least two pairs, every one-column replacement determinant vanishes; it has no order-e^2 probability.
3. In the weighted empty/double formulas, a zero remaining-coordinate weight makes the displayed coefficient zero. A zero one-flip rate cannot acquire a two-flip probability of the same cardinality: the nonnegative spectral mixture makes the one-flip term identically zero and the next allowed flip count is at least three. A zero two-flip coefficient contributes only O(e^3|log e|) entropy or smaller.

Thus no newly zero event adds an ordinary or logarithmic second-order chord term. All event probabilities remain fixed finite polynomials in e, so the same remainder argument as in `paired_frame_C2_v2.md` establishes O(e^3|log e|) for each fixed set of angles, including degenerate ones.

The strict negativity and equality characterization from the main paired proof therefore hold for every fixed paired rotation. There is no asserted uniform remainder as the angles, rates, or direction entries vary with e.

## Execution and provenance

This extension follows analytically from the completed weighted event laws.
It introduces no additional numerical premise.
