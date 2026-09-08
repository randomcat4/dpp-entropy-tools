# Fixed-site radial coupling slice proof

STATUS: PROVED_CANDIDATE, pending independent fixed-object review.

We prove exactly `frozen_radial_slice_v1.md`. Write f=H_2 and W=vv^T.

1. The domain is convex and open, since K is affine in (A,s) and strict
   positive contractions form an open convex set. Its complete-event law is
   positive: for any strict contraction L, L(I-L)^(-1)>0 is its L-ensemble
   kernel, and every principal determinant, including the empty one, is
   positive. Thus finite entropy and all derivatives used below are smooth.

2. For b=sv define

       C_1=A-bb^T/c,       C_0=A+bb^T/(1-c).

   Both are strict positive contractions. C_1>0 is the Schur complement of
   c in K, and I-C_0>0 is the Schur complement of 1-c in I-K. Also
   I-C_1=I-A+bb^T/c>0 and C_0=A+bb^T/(1-c)>0, since A and I-A are positive.

3. Conditional on site 3 being present, the inclusion probability of any
   T subset {1,2} is det(K[T union {3}])/c=det(C_1[T]), by the block
   determinant identity. Conditional on site 3 being absent, it is

       [det(A[T])-det(K[T union {3}])]/(1-c) = det(C_0[T]).

   For nonempty T the latter follows from the rank-one determinant lemma
   applied to invertible A[T]; for empty T both sides are 1. Uniqueness of
   finite Mobius inversion identifies the whole conditional distributions,
   not just their inclusion probabilities. Shannon's exact chain rule is

       F(A,s)=h(c)+c f(C_1)+(1-c) f(C_0).                 (1)

4. Take any affine parameter line A(t)=A+tB and s(t)=s+tr lying in the
   domain. A prime means differentiation in t at its current point. Then

       C_1'=B-2sr W/c,       C_1''=-2r^2 W/c,
       C_0'=B+2sr W/(1-c),   C_0''= 2r^2 W/(1-c).

   Twice differentiating (1), with gradients paired by trace, gives

       F'' = c D^2f(C_1)[C_1',C_1']
            +(1-c) D^2f(C_0)[C_0',C_0']
            +2r^2 (Df(C_0)[W]-Df(C_1)[W]).             (2)

   This explicitly includes the nonaffine conditional acceleration. The
   first two terms are nonpositive by the verified two-point theorem.

5. If s=0, C_0=C_1, so the final term of (2) vanishes. If s is nonzero,
   put alpha=-s^2/c and beta=s^2/(1-c), so alpha<beta and
   C_1=A+alpha W, C_0=A+beta W. Convexity of the strict feasible domain
   ensures A+uW is feasible for every u in [alpha,beta]. Scalar concavity
   of phi(u)=f(A+uW) implies phi'(beta)<=phi'(alpha). Hence the last term
   of (2) is nonpositive as well. This proves concavity of F.

6. For strictness we justify a strict version of this derivative comparison.
   Along any feasible rank-one line L+uW, every inclusion determinant is
   affine in u: each principal update has rank at most one and the
   determinant is affine under such an update. Mobius inversion therefore
   makes every complete probability p_T(u) affine as well. They are positive,
   so

       phi''(u) = -sum_T (p_T'(u))^2/p_T(u) < 0.        (3)

   Indeed v is nonzero, so some v_i^2>0. The derivative of the inclusion
   probability P(i in Y) is v_i^2; since that probability is a sum of complete
   event probabilities, at least one p_T' is nonzero. Thus (3) is strict.
   For s nonzero, integration over [alpha,beta] now gives
   Df(C_0)[W]-Df(C_1)[W]<0.

7. If an affine line has r nonzero, s(t) vanishes at at most one point.
   Equation (2) is strictly negative everywhere else on its interval by
   step 6. Consequently its endpoint-average minus midpoint is strictly
   negative on every nondegenerate subinterval. For example this follows by
   integrating F'' against the nonnegative triangular Green kernel, which
   is positive in the interior. If r=0 and the two parameter points differ,
   B is nonzero. Then both conditional kernels vary affinely by B; the
   strict-chord part of the verified two-point theorem makes each conditional
   entropy's midpoint inequality strict. Positive weights c and 1-c in (1)
   preserve strictness. These alternatives cover every distinct parameter
   pair, completing the proof.

The only previous nontrivial theorem used is strict real two-point entropy
concavity. No general matrix-order monotonicity of the entropy gradient is
assumed: step 5 compares derivatives only along the same rank-one line.
