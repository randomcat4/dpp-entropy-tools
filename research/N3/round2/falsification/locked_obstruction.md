# Exact Lambda-tangent obstruction to locked-odds dominance

STATUS: DISPROVED for the proposed universal dominance

    g^T D=Lambda'[D]=0  =>  max_k Q_k^lock(D)>=C(D).

This is an author rational-log certificate pending nonauthor review. It
does not refute the Fisher lower bound F>=Q_k^lock, concavity on the
Lambda-tangent hyperplane, the beta-zero implication B0, or global entropy
concavity. The actual full negative-entropy Hessian is strictly positive
on the exhibited direction.

The targeted definition is frozen at inequality author commit
99205d9ac552355c148f011bb053731a8b1349f0, file
research/N3/round2/inequality/lambda_tangent_locked_odds_lemma.md.

## Exact witness

Take the already-existing rational kernel

    K=[[37/700,3/35,9/70],
       [3/35,127/700,9/35],
       [9/70,9/35,277/700]].

Put r=-1553800482972329227/73062036340463040000 and

    D=[[r,-371/1000,-1/100],
       [-371/1000,-89/100,3/125],
       [-1/100,3/125,-1]].

The eigenvalues of K are (1/100,1/100,61/100), since
K=(1/100)I+(3/5)uu^T with u=(1,2,3)/sqrt(14). All three edges are nonzero,
so K is strict, real, symmetric and connected. Exact leading-principal-minor
tests in the certificate verify 0<K+/-D/1000<I. Thus D is an admissible
genuinely affine real direction.

Let p be the exact eight event masses and J their six-coordinate Jacobian,
where the coordinate order is (11,22,33,12+21,13+31,23+32). Define

    g_j=sum_M (-1)^(3-|M|) J_Mj/p_M.

All p,J and g at this K are rational. The five nonpivot entries of D were
rounded once to small rational numbers, and r was then set to

    r=-sum_(j=1)^5 g_j D_j/g_0.

Consequently g^T D=0 is an exact Fraction identity, not a numerical
tolerance. The certificate additionally checks equality of the two
conditional log-odds derivatives separately for all three conditioning
coordinates. Their exact rational values are saved in its output.

All principal minors and Rayleigh covariance squares used here are those
of the actual K+tD. The entire determinantal Rayleigh polynomial therefore
remains a square, including its first and second t derivatives. No
relaxation of the real principal-minor constraints was made.

## Definition and exact evaluation of the new lower bound

For each conditioning coordinate k, the two four-atom slices have masses
x=(a,b,c,d), m=sum x, delta=ad-bc, and tangent dot x=J[D]. Write

    L=dot delta-2delta dot m/m,
    V=ad(a+d)+bc(b+c)-4delta^2/m,
    R=1/a+1/b+1/c+1/d-m^2/V.

The tested locked-odds bound is precisely

    Q_k^lock=D_kk^2/[K_kk(1-K_kk)]
             +L_0^2/V_0+L_1^2/V_1
             +(m_0L_0/V_0-m_1L_1/V_1)^2/(R_0+R_1).

The code retains the last term. It checks V_e>0, R_e>=0 and R_0+R_1>0,
so all displayed divisions are valid for this witness. Exact rational
quadratic forms give the three values approximately

    Q_1^lock=2.06836585318829631785,
    Q_2^lock=5.47939181745841587060,
    Q_3^lock=5.47939708169376931085.

The full event Fisher is retained without any score deletion:

    F=sum_M (J_M[D])^2/p_M
      =59.13613025496833410279... .

All four values are exact rationals in locked_certificate.json. The
certificate checks F>=Q_k^lock for each k, consistent with the valid lower
bound. Only the proposed further comparison to C fails.

## Rigorous log comparison

Let ell=(ell_23,ell_13,ell_12), and let Lambda be the full triple log odds.
For rational adj D the cofactor quantity is

    C=2tr(N adj D)
     =-2sum_i ell_i(adj D)_ii-2Lambda tr(K adj D).

This is a rational linear combination of four logarithms of positive
rational event ratios. The existing 80-term rational atanh-series bounds
and 240-bit outward dyadic arithmetic enclose those logarithms. The
certificate yields the following deliberately widened bounds:

    5.96184755217541028 < C < 5.96184755217541029,
    -0.482450470481640975 < max_k Q_k^lock-C
                           < -0.482450470481640973,
    53.17428270279292381 < B=F-C < 53.17428270279292383.

The negative upper bound proves failure of the dominance claim. It also
rules out every convex combination of the three Q_k^lock as a universal
dominating lower bound at this K,D. It does not rule out adding a genuinely
different Fisher residual.

## Verification binding and remaining scope

The executable proof is locked_certificate.py with its fixed output
locked_certificate.json and source bindings in locked_source_manifest.json.
It executes one rational center and one rational direction. The preliminary
four-center numerical search merely selected the direction; its optimizer
status has no role in the strict sign proof.

This witness is not an H- or A-constrained minimizer claim and is not
asserted to have beta(K)=0. In fact the earlier independent root unit
certifies negative beta at this very K. The original B0 implication and
the broader target F>=C on all Lambda-tangent directions remain unproved.
The locked-odds term alone does not close that remaining Fisher-versus-
cofactor gap. The authorized final bounded unit is complete; no additional
directions, kernels or background jobs are being pursued.
