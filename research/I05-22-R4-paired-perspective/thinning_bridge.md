# A sharp logical distinction obtained after the computation handoff

Status: **PROVED (author proof; not independently reviewed)**. This note gives no actual negative G1'' point. It explains precisely what such a point would and would not settle. It uses the new event identities and quadratic-perspective theorem of this packet, not PR60's pending theorem.

## 1. Global conditional concavity and the one-sided statement are equivalent

Let A1 denote the assertion `G1''(K;D)>=0` for every strict connected missing-edge real three-point center K and every real symmetric D. Let AC denote `-H(X3|X1,X2)''(K;D)>=0` for exactly the same universally quantified centers and directions. Then

    A1 if and only if AC.                            (R1)

This is a GLOBAL assertion over all these centers. At a fixed center, the paired matrix can be positive even if one side is not; the parallel-sum compensation remains necessary. Neither assertion here is proved true. Full entropy concavity is a different, weaker target because it retains the leaf marginal Fisher.

Proof. A1 implies AC by complementation and the exact identity `-Hconditional=G1(K)+G1(I-K)`.

For the converse fix an arbitrary strict arrow K and physical D. For 0<lambda<=1 set

    S_lambda=diag(1,1,sqrt(lambda)),
    K_lambda=S_lambda K S_lambda,
    D_lambda=S_lambda D S_lambda.

Both strictness and connectedness are preserved. For EACH fixed lambda the entropy is differentiated on the true affine line

    K_lambda+t D_lambda=S_lambda(K+tD)S_lambda.

The lambda comparison path is not substituted for that entropy line. The scaling identity in proof.md gives `G1''(K_lambda;D_lambda)=lambda G1''(K;D)`.

For the other side the scalar Taylor series is

    (1-s)log(1-s)=-s+s^2/2+s^3/6+... .

Write r_ij=pij1 and P_ij=pij0+pij1 at K+tD. Their thinned values are lambda r_ij and unchanged P_ij. On a sufficiently small fixed neighborhood of t=0 all r_ij/P_ij and their first two t-derivatives are bounded, so the Taylor series can be differentiated there. Since sum r_ij=K33+tD33 is affine, its second derivative vanishes. Thus

    G0''(K_lambda;D_lambda)
       =lambda^2 J2''(K;D)/2+O(lambda^3),            (R2)

with J2=sum r_ij^2/P_ij. Therefore

    -Hconditional''(K_lambda;D_lambda)
       =lambda G1''(K;D)+lambda^2 J2''(K;D)/2
         +O(lambda^3).                              (R3)

If AC holds, divide the nonnegative left side by lambda and let lambda decrease to zero. This yields G1''(K;D)>=0 for the arbitrary K,D, proving (R1). The endpoint is used only as a limit; no strict-boundary Hessian value is substituted.

Consequently a proof of the general-arrow CONDITIONAL Schur sign would also prove the universal one-sided claim. The full-entropy core E_H avoids this strengthening. A pending theorem only on the Lambda-zero subfamily cannot supply AC, since the thinned K_lambda generally leave that subfamily.

## 2. Exact, event-complete error in the thinning expansion

At a fixed strict arrow and direction write

    t_i=r_i/P_i, T_i=(r_i/P_i)', a_i=r_i'', b_i=P_i'',
    C3=2 sum_i P_i t_i T_i^2
         +sum_i |a_i|t_i^2+(2/3)sum_i |b_i|t_i^3.     (R4)

The index i here labels all FOUR leaf configurations, and each P_i includes BOTH third-bit outcomes. The derivatives are from all eight exact event jets. In particular b_i need not vanish.

For 0<lambda<=1/2,

    |G0''(K_lambda;D_lambda)-lambda^2 J2''(K;D)/2|
       <=C3 lambda^3.                               (R5)

To prove this, the general perspective derivative (7) gives exactly, after summing sum a_i=0,

    G0''=lambda^2 sum_i P_i T_i^2/(1-lambda t_i)
         -lambda sum_i a_i log(1-lambda t_i)
         +sum_i b_i[log(1-lambda t_i)+lambda t_i].     (R6)

For 0<=s<=1/2, geometric and logarithmic series give

    |(1-s)^(-1)-1|<=2s,
    |-log(1-s)-s|<=s^2,
    |log(1-s)+s+s^2/2|<=(2/3)s^3.

Substitute s=lambda t_i, using 0<t_i<1. The coefficient of lambda^2 in (R6) is
`sum P_i T_i^2+sum a_i t_i-(1/2)sum b_i t_i^2=J2''/2` by the scalar perspective formula for t^2. The three remainder bounds give exactly (R4)-(R5).

## 3. A hypothetical negative side has a certified non-counterexample regime

Suppose, but do NOT assert the existence of, a fixed K,D with

    G1''(K;D)=-h<0.

Let beta=J2''(K;D)/2>0, and let

    m0=D11^2/v+D22^2/w.

Then m0>0. Indeed, if D11=D22=0, the side form is U^T Y1 U, strictly positive for every nonzero D by Lemma 2 and the invertible coordinate map in proof.md. A negative G1'' therefore necessarily has a nonzero leaf-diagonal component.

For every

    0<lambda<=min(1/2,
                  h/[2(beta+C3)],
                  m0/[2(h+C3)]),                    (R7)

the SAME exact thinned center and direction satisfy simultaneously

    -Hconditional''(K_lambda;D_lambda)<=-h lambda/2<0,
    -Hfull''(K_lambda;D_lambda)>=m0/2>0.              (R8)

The first inequality follows from (R3)-(R5) and lambda<=1. For the second, leaf marginals and their affine directions are unchanged by thinning the third coordinate. The exact marginal negative Hessian remains m0, including its missing-edge acceleration cancellation. Hence

    -Hfull''=m0-h lambda+beta lambda^2+remainder
            >=m0-(h+C3)lambda>=m0/2.

Thus an actual negative side would refute universal conditional-entropy concavity, but its sufficiently thinned realizations would still have the CONCAVE full-entropy curvature in that corresponding direction. This gives an explicit, DPP-specific reason why a side certificate cannot be relabeled as a full-entropy counterexample. The marginal Fisher is the decisive surviving term, not an optional correction.

The conclusion is directional at the displayed thinned K,D. It does not claim that every direction of the thinned full Hessian is positive. No negative G1 object has been produced in this packet, so (R7) is a conditional construction, not a hidden counterexample claim.

## 4. Consequence for the open target

The appropriate remaining target is the paired E_H determinant in post_checkpoint.md (P12), not the individual E1 determinant or even a universally positive conditional Schur. The latter two are globally equivalent by (R1), and both may be stronger than needed for full entropy.

Small exact post-handoff checks recover the scalar first two lambda derivatives as -r and r^2/P, along with their affine-mass cancellation. They are in the local package's post_checks.py and outputs/post_checks.json. The bound and equivalence are the analytic proofs above; same-session checks are not independent review. Issue73's original bounded inputs and allocation are not expanded by this note.
