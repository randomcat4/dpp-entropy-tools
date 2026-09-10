# Work after PR70's first checkpoint

All results here are author results, not independently reviewed. They do not depend on PR60's pending Lambda-zero theorem. This continuation is not a proof of the one-sided Shannon-perspective inequality or of general three-point entropy concavity.

## 1. A complement-preserving resolvent rescue is false

Define on a strict three-point kernel, including nearby kernels with nonzero K12,

    Phi_pair(K)=sum_ij Pij^2/pij1 + sum_ij Pij^2/pij0,
    Pij=pij0+pij1.

Both complementary sides and all eight complete atoms occur. The assertion that this function always has nonnegative Hessian at connected missing-edge centers is false.

An exact object is

    K=[[1/25,0,2/15],[0,3/4,1/4],[2/15,1/4,18/25]],
    D=[[1,-7/5,11/9],[-7/5,1/5,0],[11/9,0,-1/7]].       (P1)

Here A=25/54, B=1/3, q=173/900, qbar=31/2700. These positive values establish legality by the arrow Schur complements; q differs from qbar, so Lambda is nonzero.

The exact second derivatives on K+tD are

    Phi0''=-17195245284290193050175018195000
            /102736068486597078628140399487,

    Phi1''=459391680374575413414186538171831635000
            /2825836508547416584007832972390257641,

    Phi_pair''=-125413424484215487448116244468280440113219969455538795750000
                 /26102637294738394550409051443126654598253142521608171454843 < 0. (P2)

In particular the last value lies in

    [-4.804626561987111423025329832575,
     -4.804626561987111423025329832574].

### Complete arithmetic derivation

For each side mass r and marginal P, direct quotient differentiation gives

    (P^2/r)''=2(P'-P r'/r)^2/r+2PP''/r-P^2r''/r^2.     (P3)

Build the eight atoms by (1) of proof.md, and retain their complete jets. The rows below are `(p,p',p'')` in mask order 0,1,2,12,3,13,23,123:

    (31/11250, -109307/9450000, -6137/354375)
    (427/90000, -82393/9450000, -14113/354375)
    (931/3750, -480077/1050000, -128207/39375)
    (727/30000, 651377/1050000, 130457/39375)
    (2669/11250, -4067593/9450000, -1241263/354375)
    (473/90000, 2369293/9450000, 1261513/354375)
    (1769/3750, -105823/1050000, 266807/39375)
    (173/30000, 144523/1050000, -269057/39375).

The marginal jets are obtained by adding rows i and i+4. Substitution into (P3) and summation gives the exact fractions (P2). No logarithmic approximation is needed for the negative resolvent sign.

### What this does and does not refute

For any nearby kernel, every selected mass is affine in K33, with derivative Pij, while each Pij is independent of K33. Thus the exact identity

    partial_K33^2[-H(X3|X1,X2)]=Phi_pair(K)

holds on the strict domain. Differentiating twice in a fixed physical D and commuting the derivatives therefore gives

    partial_K33^2[-H''(K;D)]=Phi_pair''(K;D).            (P4)

The leaf entropy has no K33 dependence. Consequently (P2) also disproves universal Loewner convexity of the full negative entropy Hessian under vertical K33 translation. This is a new complement-preserving sufficient-method obstruction, not a restart of the already disproved fixed-diagonal EDGE-radial monotonicity route.

It does NOT disprove G1''>=0, conditional-entropy concavity, or full entropy concavity. At this exact object both one-sided quantities have the nonnegative sign:

    G0'' in [6.383647726792465053208434312050,
             6.383647726792465053208434312051],
    G1'' in [9.217730038861857449230207862233,
             9.217730038861857449230207862234],
    -Hconditional'' in [15.601377765654322502438642174283,
                        15.601377765654322502438642174284],
    -Hfull'' in [41.856377765654322502438642174283,
                 41.856377765654322502438642174284].   (P5)

For tau=1/100000, the three exact kernels K-tau D,K,K+tau D and their complements have the following positive leading Sylvester minors:

    minus K: (3999/100000,1874526239/62500000000,
              81722984551974671/14175000000000000000)
    minus complement: (96001/100000,15000276239/62500000000,
                        4340182176969481/1575000000000000000)
    center K: (1/25,3/100,173/30000)
    center complement: (24/25,6/25,31/11250)
    plus K: (4001/100000,1875473739/62500000000,
             81762005761973329/14175000000000000000)
    plus complement: (95999/100000,14999723739/62500000000,
                       5579765768960953/2025000000000000000).

Hence the entire affine segment is legal by convexity. Its complete-event Jensen difference has the strictly NEGATIVE enclosure

    [H(K-tau D)+H(K+tau D)]/2-H(K) in
    [-0.000000002092818919276583428073,
     -0.000000002092818919276583428072].               (P6)

This is not an entropy-counterexample candidate for C2.

### Error and reproduction contract

`certify_obstruction.py` constructs the jets from (P1), calculates (P2) with exact fractions, checks all six sets of Sylvester minors, and independently evaluates the two perspectives and the full entropy Hessian. For each positive rational logarithm argument, normalize it to 2^k y with 1<=y<2 and set w=(y-1)/(y+1). At N=60,

    0 <= log y-2 sum_(j=0)^(N-1) w^(2j+1)/(2j+1)
       <= 2w^(2N+1)/[(2N+1)(1-w^2)].                (P7)

The log2 enclosure uses the same series at w=1/3. All interval sums use rational endpoints; multiplication by negative k reverses endpoints; final decimals are rounded outward with integer floor/ceiling. The actual new run ended `ALL EXACT PAIRED-OBSTRUCTION CHECKS PASSED`. This is author self-check, not independent review.

GitHub creation of this second verifier was blocked by the tool safety-state check. It was not retried through another GitHub endpoint. The user-authorized existing Drive fallback succeeded and metadata was read back. The complete local package contains the script and output. No public sharing or permission change is claimed; the public mathematical reproduction above does not require downloading the script.

## 2. Exact symmetry of the paired two-dimensional core

The reduction in proof.md (16) can be placed on a smaller parameter domain without an entropy-invariant spectral rotation.

For a complemented kernel, use primed leaves i'=1-i,j'=1-j, x'=1-x,y'=1-y. Then A'=A,B'=B,q'=qbar and qbar'=q. Along its true direction D'=-D, the conditional polynomial coordinates transform by

    delta'=-delta, U'=J4 U, J4=diag(-1,1,1,-1).       (P8)

This follows by expanding T'_(i'j')=-T_(ij). Equality of the FULL conditional entropy functions implies, by polarization in all six directions,

    L'=L, C'=-C J4, Y'=J4 Y J4, M'=M,
    E_H(1-x,1-y,A,B,qbar)=E_H(x,y,A,B,q).          (P9)

In particular the two-dimensional determinant is unchanged under complement. The single-side E1 instead maps to E0: it may not be treated as separately complement invariant.

Physical exchange of leaves 1 and 2 gives, with J2swap=[[0,1],[1,0]],

    E_H(y,x,B,A,q)=J2swap E_H(x,y,A,B,q) J2swap.   (P10)

Equations (P9)-(P10) preserve inertia and determinant. The two operations commute on the shape domain, so the full paired problem can be studied on

    0<x,y<1, A>=B>0, 0<q<=qbar, A+B+q+qbar=1.   (P11)

Equality surfaces A=B and q=qbar are included, not deleted. Every strict connected missing-edge center is represented. This reduces redundant sign work but does not establish determinant nonvanishing or positivity.

## 3. Remaining claim and fastest falsification

The stronger single-sided inequality remains INCOMPLETE: (P2) is not its counterexample. The weaker, complement-retaining full-entropy core is precisely

    det[L0+L1+diag(1/v,1/w)
         -(C0+C1)(Y0+Y1)^(-1)(C0+C1)^T] >= 0.    (P12)

All matrices have explicit formulas in proof.md; Y0+Y1 is proved positive definite, and the remaining 2x2 matrix has at least one positive eigenvalue. Thus (P12) is an exact pointwise equivalence, not merely a sufficient numerical test or a claimed solution. Compared with separate one-sided nonnegativity, the positive parallel-sum compensation and marginal Fisher are explicitly retained.

The fastest structured falsification is to follow q/(q+qbar) on a fixed rational leaf/edge shape, evaluate the 2x2 core, lift its bad vector through U=-Y^(-1)C^T delta, and rationally reconstruct a physical D. Only an exact negative FULL -H'' followed by a positive, error-enclosed legal Jensen triple may be called an entropy counterexample. If only E1 is negative, stop at a single-side method certificate and check E_H separately. A bounded independent contract is recorded on the linked calculation issue; no run or outcome is assumed.

## 4. Corrected index and review boundary

After the first PR70 checkpoint, the author caught an index typo in Lemma 2's unweighted positive decomposition of N0: its diagonal uses absent-side FACE1, not face0. The weighted N_s and matrices L_s,C_s,R_s were unchanged and the generic exact coefficient checker already used the correct matrices. The correction is retained in commit 8c3f4a145c350645f522cfab0b5841b7d4dcec25 and in proof.md; it does not silently inherit independent review.

During the continuation, PR60's public comments were re-read. C1 had announced FIRST review and C2 its distinct reconstruction contract, but neither comment supplied a completed verdict or a requested correction. No pending theorem was promoted to accepted, no old certificate was rerun, and the new PR70 scope is separate.
