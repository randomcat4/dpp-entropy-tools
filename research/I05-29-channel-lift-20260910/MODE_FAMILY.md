# An explicit dense 3+3 whole chord with a genuinely negative complete fiber

Status: PROVED (author proof), with executed author rational checks; PENDING_REVIEW. This is a specialization of `CHANNEL_LIFT.md`, not an assertion of arbitrary observed-basis entropy invariance or a new proof of the already accepted m-by-2 theorem.

## 1. Exact observed kernel and full maximal interval

Start with the four-coordinate base

    A0=[[1/3,1/6],[1/6,1/3]],
    C0=[[2/5,1/48],[1/48,3/5]],
    B0=(1/12)[[1,1],[2,-1]],
    W=[[3/5,0],[4/5,0],[0,1]].

Expand the first coordinate of each block into two observed coordinates with half-filled complement, exactly as in the channel theorem. The actual observed matrices are

    A=[[11/25,-2/25,1/10],
       [-2/25,59/150,2/15],
       [1/10,2/15,1/3]],
    C=[[58/125,-6/125,1/80],
       [-6/125,109/250,1/60],
       [1/80,1/60,3/5]],
    B=[[3/100,1/25,1/20],
       [1/25,4/75,1/15],
       [1/10,2/15,-1/12]].

Both three-coordinate blocks are fully correlated, every cross entry is nonzero, and B has rank two. The two nonzero repeated-direction rows or columns are actual observed coordinates and are never deleted from the entropy.

The Schur polynomials in the base coordinates are

    det(C0-s B0^T A0^-1 B0)
      =(300s^2-4900s+13799)/57600,
    det(I-C0-s B0^T (I-A0)^-1 B0)
      =(60s^2-2092s+13799)/57600.

The first roots are respectively

    s_star=49/6-sqrt(4657)/15 in (3,4),
    s_complement=523/30-2sqrt(4159)/15 in (8,9).

Thus the whole maximal legal interval, in both base and observed kernels, is `[-sqrt(s_star),sqrt(s_star)]`. The background adds only fixed eigenvalues 1/2 for legality; the entropy relation follows from the channel law, not this eigenvalue observation.

On a two-coordinate expanded group the complement-pair selector has theta=1 or 7/25, each with probability 1/2. Writing K0 for the complete four-coordinate base and D=diag(sqrt(theta_left),1,sqrt(theta_right),1), the exact full entropy formula is

    H(K_observed(t))=2log2+(1/4)sum_{theta_left,theta_right in {1,7/25}}
                        H(I4/2+D(K0(t)-I4/2)D).             (1)

It retains all 64 events in the observed basis. Every term on the right is truly K-affine and has two coordinates on each side, so the accepted theorem proves whole-chord concavity. The explicit quantitative channel bound, choosing base B0[2,1]=1/6, gives

    H_observed''(t) <= -(337/202500)t^2                     (2)

throughout the strict maximal chord. This is a nonperturbative observed 3+3 family result, not only a neighborhood of a decoupled center.

## 2. Negative complete conditional-relative-entropy fiber

Condition on actual left mask 3: both coordinates in the first group occupied, third coordinate absent. This reveals base left mask 1. Direct Schur calculation gives

    B0^T(A0-diag(0,1))^-1 B0=(1/24)[[0,1],[1,0]].

With r=1/48 and D0=diag(2/5,3/5), the conditional base right kernel is

    D0+r(1-2s)[[0,1],[1,0]].

Its observed expansion has complete probabilities

    p_T(s)=p_star(T)+(1-2s)^2 d_T.                           (3)

Here for the two-coordinate-group mask define h=2sum_{a in T}v_a^2-1 with v=(3/5,4/5), and let z record occupation of the third coordinate. All eight atoms have the explicit rational form

    p_star(T)=[(3/5 if z=1 else 2/5)/4]*(1-h/5),
    d_T=(r^2/2)(1-2z)h.

The reference p_C equals p_star+d, every p_star and p_C is positive, sum d=0, and d is not zero. At s=1/2 the conditional first derivative vanishes on every event. Hence every term of this fiber's full Fisher contribution vanishes exactly; its full relative-entropy curvature is

    C_mask3(1/2)=-8 sum_T d_T log(1+d_T/p_star(T)) < 0.      (4)

Each d_T log(1+d_T/p_star)>=0 by monotonicity of log, with strict inequality for a nonzero d_T. This is an exact sign proof, independently of decimal evaluation. The rational log enclosure also gives

    C_mask3(1/2) in
      [-0.00001406768643518482,-0.00001406768643518472].

As in PR80, this fiber is t^2 times the second derivative of conditional KL to the fixed right marginal. It must not be identified with minus conditional Shannon curvature in isolation. Equation (2) and the negative (4) coexist on the same fully correlated observed 3+3 kernel. Thus even within a proved whole-chord family, the required global compensation is not equivalent to every complete fiber being positive.

## 3. Parameter family and exact representation limit

More generally keep A0 and D0 above, take `B0=k[[1,1],[2,-1]]` and `C0=D0+3k^2 X` with `0<k<=1/12`, and make the same observed expansion. The conditional kernel becomes `D0+3k^2(1-2s)X`, so the negative-fiber proof persists. The Schur lower bound `2/5-39k^2>0` ensures at least |t|<=1 is strict. The channel theorem proves concavity on each member's entire maximal legal interval, which can be larger. The curvature bound is `H''<=-64(337/625)k^4 t^2`.

This family does not explain the original PR58 difficult fixture by a hidden rotation. A three-coordinate observed block derived from two disjoint-supported modes necessarily has two proportional B rows or columns. For the original fixture the three U-row pair determinants are

    17191/250000, -121/500000, -90217/500000,

and the three V-row pair determinants are

    655143/1000000, -327003/1000000, -536007/1000000.

All are nonzero. Therefore the original fixture is outside this grouped representation. Its full-chord theorem in `WHOLE_CHORD.md` is a separate direct-curvature result, not a consequence of (1).

## 4. Checks and preserved failures

`code/verify_channels.py` checks all 64 observed event polynomials for the half background and for the genuinely asymmetric backgrounds eta_left=1/4, eta_right=2/3. It also checks a general asymmetric ternary channel, the exact refined joint probabilities, and the complete second derivative along a two-coordinate affine path whose diagonals move. The latter uses rational Fisher coefficients and exact prime-factor decompositions of all rational logarithm arguments, not finite differences or numerical agreement.

The naive extension of uniform complement selectors away from half filling is explicitly refuted: for eta=1/3 the empty/full pair has probabilities 2/3 and 1/3 for the two inputs. The general selector-refinement theorem instead includes its necessary affine entropy correction.

Two author development stops were preserved. The first used the wrong SymPy Poly derivative signature and failed before the Hessian comparison. The second chose eta_left=1/3, exactly matching A0[1,1], while also asserting every observed internal edge was nonzero; that particular edge cancels. The final asymmetric fixture uses eta_left=1/4. This changes no theorem assumption, and no original PR58 fixture is changed. The final run returned exit 0 with all exact checks passed. See the failure ledger and literal attempt outputs.
