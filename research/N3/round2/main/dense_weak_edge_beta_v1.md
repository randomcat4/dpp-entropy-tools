# A positive beta limit on every fixed dense weak-edge ray

Author status: PROVED_CANDIDATE_PENDING_NONAUTHOR_REVIEW.
This is a restricted beta nonvanishing result, not a proof of B0 globally.
It does not claim new local entropy concavity, which was known in round 1.

## Statement

Fix x_i in (0,1) and three nonzero real constants a,b,c. Write

    K(t)=[[x1,ta,tb],[ta,x2,tc],[tb,tc,x3]],  t>0,
    s_i=x_i(1-x_i), S=s1*s2*s3.

For all sufficiently small t the kernel is strict and connected. With the
exact round-2 definitions of H, alpha and beta, retaining the full triple
score, one has

    beta(K(t)) = 4 sqrt(S) + O(t),                         (1)
    det(N)*alpha = t^2 [a^2 b^2/(s1 c^2)
                       +a^2 c^2/(s2 b^2)
                       +b^2 c^2/(s3 a^2)] + O(t^3).       (2)

In particular beta>0 and det(N)*alpha<1 on a sufficiently small interval.
No beta zero is present there. Constants and the interval may depend on all
six fixed parameters. There is no uniform claim as an edge constant or a
Bernoulli variance vanishes, and the proof does not divide on zero-edge strata.
Both signs of abc are covered; the leading beta limit is independent of them.

## 1. Exact real event density and its derivatives

Let mu be the product Bernoulli law with means x_i and
chi_i=(X_i-x_i)/s_i. Relative to mu the DPP has exactly

    p/mu = 1-t^2(a^2 chi1 chi2+b^2 chi1 chi3+c^2 chi2 chi3)
             +2t^3 abc chi1 chi2 chi3.                    (3)

Indeed its centered pair moments are -t^2 a^2, -t^2 b^2, -t^2 c^2,
and its centered triple moment is 2t^3 abc. The seven nonconstant products
of the centered coordinates, together with the constant, are an orthogonal
basis under mu. Matching their moments proves (3) for all eight atoms.
This keeps the real equality T^2=4uvw exactly: u=t^2a^2, v=t^2b^2,
w=t^2c^2, T=2t^3abc. Both its first and second t derivatives hold, and all
six-coordinate derivatives below are taken from the affine K event map.

Product means stay in a compact subinterval of (0,1) in a small neighborhood
of the fixed x, so all expansions here are ordinary finite-dimensional
analytic Taylor expansions with uniform remainders in that neighborhood.
The inverse density in (3) is 1+O(t^2). Orthogonality gives, in diagonal/off-
diagonal coordinate blocks,

    F_dd=diag(1/s_i)+O(t^2),
    F_do=O(t^3),
    F_oo=t^2 diag(4a^2/(s1s2),4b^2/(s1s3),4c^2/(s2s3))+O(t^4).  (4)

For completeness, an off-coordinate derivative of p/mu is
`-2ta chi1chi2+2t^2bc chi1chi2chi3` for the 12 entry, cyclically.
A diagonal derivative divided by mu is chi_i+O(t^2).
The potential O(t) and O(t^2) diagonal/off terms vanish by centering on an
unpaired coordinate. Likewise the off/off cross terms at orders t^2,t^3
vanish. Expansion of the exact finite sums proves (4), without dropping a
score term or replacing the event distribution by a marginal distribution.

The alternating log functional annihilates the constant and pair terms.
From (3),

    Lambda=2t^3abc/S+O(t^4),
    (grad Lambda)_d=O(t^3),
    (grad Lambda)_o=(2t^2/S)(bc,ac,ab)+O(t^3),
    Z=sum 1/p=1/S+O(t^2).                                 (5)

The derivative expansions follow by Taylor expansion in the three actual
edge entries: the omitted terms have total edge degree at least four.
Subtracting the exact rank-one term gradLambda gradLambda^T/Z changes none
of the displayed leading orders in (4). Thus the same block estimates hold
for F_pair, with the full score still represented as F_pair+v_score v_score^T.

## 2. N, its trace covector and H

The absent-conditioned log odds satisfy
ell12=-t^2a^2/(s1s2)+O(t^3), cyclically. This also follows by expanding
the exact covariance square and its positive denominator. Define

    n1=c^2/(s2s3), n2=b^2/(s1s3), n3=a^2/(s1s2).

Then N_ii=t^2 n_i+O(t^3), while its off entries satisfy the sharper formula

    N_12=-(2a^2bc/S)t^4+O(t^5), cyclically.               (6)

Hence d=det(N)=t^6 n1n2n3(1+O(t)), and inversion of (6) gives

    eta_d=t^-2(1/n1,1/n2,1/n3)+O(t^-1),
    eta_o=(4a^2s3/(bc),4b^2s2/(ac),4c^2s1/(ab))+O(t).   (7)

Here off-coordinate eta entries are twice the corresponding entries of
N^-1. For example `(N^-1)_12=2a^2s3/(bc)+O(t)`.
This is where the real cycle product and its sign are retained.

Combining (4) with the exact term d G gives

    H_dd=diag(1/s_i)+O(t^2), H_do=O(t^3),
    H_oo=t^2 diag(6a^2/(s1s2),6b^2/(s1s3),6c^2/(s2s3))+O(t^3). (8)

In particular dG contributes 2t^2a^2/(s1s2) in the 12 off-coordinate.
Its diagonal/off block is O(t^4), so it does not change the bound in (8).
All leading block matrices are positive definite for the frozen parameters.

## 3. Solve the actual H system and retain the triple score

Put h=H^-1 eta, without trace normalization. The block inverse of (8), or
rescaling off coordinates by t, yields

    h_d=t^-2(s1/n1,s2/n2,s3/n3)+O(t^-1),
    h_o=(2S/3)t^-2(1/(bc),1/(ac),1/(ab))+O(t^-1).        (9)

The cross correction H_od h_d is only O(t), whereas eta_o has order one;
its inversion contributes only O(t^-1), as claimed. The diagonal inverse
correction likewise has lower order. These estimates control the inverse
of a degenerating H rather than assuming a nonsingular limit at t=0.

By (5) and (9),

    gradLambda^T h = 0+sum_three_edges 4/3+O(t)=4+O(t).

Dividing by sqrt(Z) proves (1). This strictly positive term comes from the
off-coordinate pieces in eta and h; retaining only the diagonal score would
miss it. In particular Lambda itself has sign abc to leading order, but
beta has the same positive leading limit for either real cycle sign.

Finally alpha=eta^T h has leading term
`t^-4 sum_i s_i/n_i^2+O(t^-3)`. Multiplication by d gives (2).
Continuity of eigenvalues proves strict feasibility for small t, and all
three edges are nonzero, completing the stated restricted result.

## Boundary and evidence limitations

The proof uses fixed nonzero a,b,c and fixed interior means. It covers no
joint limit where edge ratios or means degenerate. It does not resolve
beta=0 away from this regime or the original global entropy question.
The fixed finite weak-edge diagnostic is supporting arithmetic only;
the nonvanishing claim comes from the expansion above and requires review.
