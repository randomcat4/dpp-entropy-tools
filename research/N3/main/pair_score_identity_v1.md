# Keeping all one- and two-point statistics

Author status: EXACT_IDENTITY_PENDING_NONAUTHOR_REVIEW.

Let p be any strictly positive probability law on three bits. Let s=p'/p be
a mass-preserving score. Put epsilon_S=(-1)^(3-|S|), h_S=epsilon_S/p_S, and
Z=sum_S 1/p_S. In the p-weighted inner product, h is orthogonal to every
polynomial in the bits of degree at most two: each corresponding alternating
sum vanishes. This seven-dimensional polynomial space includes the constant,
and h spans its one-dimensional orthogonal complement.

For T=(X1,X2,X3,X1X2,X1X3,X2X3), the covariance matrix Sigma=Cov(T) is
positive definite: no nonconstant multilinear polynomial of degree <=2 is
constant on all eight atoms. The squared norm of the projection of the
centered score s onto the centered T space is

    F_pair = m'^T Sigma^-1 m',  m=E T.

The missing component has squared norm <s,h>_p^2/<h,h>_p. Consequently

    F = F_pair + (Lambda')^2/Z,
    Lambda=log(p123 p1 p2 p3/(p0 p12 p13 p23)).                (P1)

All these are identities for positive three-bit laws. For the DPP path,
m consists of the diagonal entries and pair inclusion minors, so both m'
and Sigma are determined by the exact event formulas. P1 identifies the
single score term omitted by this richer projection. It is not a proof of
the target inequality F>=2tr(N adj D).

Equivalently,

    F_pair = min_c sum_S (p'_S-c epsilon_S)^2/p_S,
    c=Lambda'/Z.                                            (P2)

This variational version makes exact cancellation of a rare atom's Fisher
pole transparent. The falsification branch studies a nonexchange-symmetric
rank-two boundary family where F_pair stays bounded, the cofactor term grows
logarithmically, and the omitted term diverges faster. Its proof is a separate
author object; P1 alone does not assert those asymptotics.

The one-shot probe reused 36 previously recorded centers. It found one
all-direction failure of F_pair>=cofactor and zero failures at the actual
A trace optimizer. These counts are exploratory only. The all-direction
failure is independently explained by the analytic boundary obstruction.
