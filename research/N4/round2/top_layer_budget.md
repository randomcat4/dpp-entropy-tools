# Maximum-cardinality geometric entropy versus its own Fisher cost

Status: PROOF_CANDIDATE_PENDING_REVIEW. Main-authored auxiliary bound;
not an entropy-concavity theorem.

For a fixed real n by r isometry U and 0<A<I, every maximum-cardinality
event S, |S|=r, has probability p_S=q_S d, where q_S=det(U_S)^2 and d=detA.
Cauchy-Binet gives sum q_S=1. Let c=H(q); zero q terms have their continuous
zero entropy convention. Merging these events into one symbol of mass d gives
H_face=H_coarse+c d. The additional geometric curvature is c d''.

For any real symmetric direction V let X=A^(-1/2)V A^(-1/2). Determinant
differentiation yields d'=d trX and d''=d[(trX)^2-tr(X^2)]. The eigenvalue
Cauchy-Schwarz inequality gives tr(X^2)>=(trX)^2/r, hence

`c d'' <= ((r-1)/r)c (d')^2/d`.

The quantity F_top=(d')^2/d is exactly the sum of Fisher costs of the
maximum-cardinality events; no term is discarded. This inequality also holds
when d'=0, since then d''=-d tr(X^2)<=0. It is sharp for scalar X. It says
only that the **additional geometric entropy** c d has this Fisher bound:
the other curvature of -d log d, especially -d''logd, is still present.

In n=4,r=3 with the noncoordinate null vector, q has four positive entries.
Thus c<=log4 and ((r-1)/r)c<1 because log4<3/2 (e^(3/2)>1+3/2+9/8+27/48>4).
The extra term consumes at most (2/3)log4≈0.924196 of F_top. Consequently

`H_face'' <= -(1-(2/3)H(q))F_top
              -sum_(non-top) p'^2/p -sum_(coarse symbols) p''logp`.

The last logarithmic acceleration sum remains unsigned; this does not settle
the fixed-face question. It excludes only an unbalanced use of the extra
top-configuration entropy as a free source of positive curvature.

## Concrete change in five-point rank-three geometry
Let H(w)=I-2ww^T/(w^Tw), a=(1,2,3,4,5), b=(2,-1,3,-2,1), and let U be
the first three columns of H(a)H(b). U is rational and orthonormal exactly.
An initial arithmetic probe finds all ten squared 3-row minors positive and
their entropy approximately 1.90016187646, exceeding 3/2. Exact support and
a rigorous entropy comparison are delegated to the independent reviewer.

If confirmed, the bound's coefficient (2/3)H(q) exceeds one for a real
full-support frame. This is a concrete reason for a small n=5,r=3 follow-up;
it is a failure of this sufficient cost bound, not a concavity counterexample.
Scalar A,V directions are known thinning controls; genuine testing must keep
general noncommuting directions and all lower-event contributions.
