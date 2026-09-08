# Eight-event identity and the remaining matrix inequality

Write K with diagonal (a,b,c), edges (x,y,z)=(K12,K13,K23). For each sign
triple s in {-1,1}^3 let d_i equal Kii when s_i=1 and 1-Kii otherwise.
The exact full-event probability is

    p_s=d1*d2*d3-s1*s2*x²*d3-s1*s3*y²*d2-s2*s3*z²*d1
        +2*s1*s2*s3*x*y*z.

It follows by expanding (-1)^(number of excluded sites) det(K-I_excluded),
or by inclusion-exclusion. `probe.py` differentiates this polynomial with
second-order arithmetic, independently checks its probabilities against
principal-minor inclusion-exclusion, and forms the full Hessian

    D²H = -Gᵀ diag(1/p) G - sum_s log(p_s) D²p_s = -F+B.

Define q12=sum_s s1*s2*d3*log(p_s), and q13,q23 analogously. Put
L=sum_s s1*s2*s3*log(p_s). In coordinate order (a,b,c,x,y,z), the
probability acceleration matrix B has:

- B_aa=B_bb=B_cc=0; B_ab=-q12, B_ac=-q13, B_bc=-q23;
- B_xx=2q12, B_yy=2q13, B_zz=2q23;
- B_cx=2xL, B_by=2yL, B_az=2zL; all other diagonal-edge entries zero;
- B_xy=-2zL, B_xz=-2yL, B_yz=-2xL; symmetric counterparts understood.

These entries follow by direct polynomial differentiation; no conditioning
acceleration has been omitted. The 512 diagnostic checks are a numerical
implementation check of this exact identity, not its proof.

Each qij is a weighted sum of log odds ratios for the two conditional
two-point DPPs, with weights Kkk and 1-Kkk. For a two-point DPP with
offdiagonal r, p11*p00-p10*p01=-r², so those log odds ratios are <=0.
Consequently qij<=0. This controls the diagonal entries of the edge block
but does not, by itself, control its offdiagonal cyclic L terms, nor the
full six-dimensional Hessian. The remaining full inequality F-B>=0 is
equivalent to the Hessian target and is labeled EQUIVALENT_BLOCKER.

This decomposition is independent of R1 implementation. It must not be
confused with the different conditional-kernel acceleration obstruction in
`proof.md`.
