# C3 mechanism unit: pair-invisible, cycle-active phase shear

Status for the fixed scalar entropy-rate target: **INCOMPLETE**.
Status of the finite identities and weak-coupling obstruction below: **PROVED** by the supplied algebra, pending non-author review.
Status of the n=8 signs: floating diagnostics, not interval certificates.

This unit constructs and tests one fixed scalar chord. It does not scan Hessians, vary observation windows, add harmonics, extrapolate an entropy rate, or claim novelty. Its analytic output is an exact decomposition that separates genuine cycle-phase gain from the radial cost forced by an affine tangent. A finite-window weak-coupling theorem shows why eliminating two-point scores cannot by itself produce a counterexample near independence.

## 1. Definitions and complete-event identity

Let K be an n by n strict Hermitian contraction. Its DPP law on subsets S of [n] has exact probabilities

    p_K(S) = sum_{T superset S} (-1)^(|T|-|S|) det K_T.

All probabilities are positive: writing L=K(I-K)^(-1)>0 gives p_K(S)=det(I-K)det L_S>0. Define H(K)=-sum_S p_K(S)log p_K(S), with natural logarithms. For any Hermitian D,

    H''(K;D) = -F - sum_S p''_S log p_S,
    F = sum_S (p'_S)^2/p_S.

Indeed differentiate the finite sum twice and use sum p'=sum p''=0. There is no event truncation in this identity or in the numerical implementation.

Choose real numbers a_ij=-a_ji on nonzero off-diagonal entries and let

    D_ij = i a_ij K_ij, D_ii=0,
    E_ij = a_ij^2 K_ij, E_ii=0.

The finite-dimensional phase curve Q(u)_ij=K_ij exp(i u a_ij), with unchanged diagonal, remains a strict contraction for sufficiently small |u| by continuity. It satisfies Q'(0)=D and Q''(0)=-E. The ordinary second-order chain rule therefore gives the exact identity

    H''(K;D) = (d^2/du^2) H(Q(u))|_0 + dH_K(E).       (1)

On each complete event,

    p''_affine(S) = p''_phase(S) + dp_K(S)[E],
    p'_affine(S) = p'_phase(S).

Consequently the Fisher term is identical in the two curvatures. Equation (1) does not discard it. Unlike a gauge tangent, a general phase shear has nonzero cycle flux and the first term in (1) need not vanish.

For every pair i,j, det K_{ij}=K_ii K_jj-|K_ij|^2 has zero derivative along D. This proves pair-score invisibility. The second derivative is -2|D_ij|^2. Thus an affine direction that keeps all one- and two-point probabilities constant through second order must be zero: requiring second-order pair invisibility is not a viable way to obtain nonzero cycle acceleration.

## 2. An explicit cycle gain with no missing Fisher term

For a Toeplitz centre with only harmonics 1 and 2, take a1=1 and a2=-1. The gauge condition a_k=k a1 fails because a2 is not 2. The triangle product C=c1^2 conjugate(c2) has phase flux 2 a1-a2=3. Along the affine curve,

    C_affine(t)=C(1+i t)^3,
    C_affine'(0)=3 i C,
    C_affine''(0)=-6 C.

Along the fixed-modulus phase curve C_phase(t)=C exp(3 i t), the second derivative is -9 C. The difference is 3 C, exactly its radial derivative. Since a1^2=a2^2=1, E is the full off-diagonal part of K, not a new anisotropic direction. All translates of the nearest-neighbour triangle have the same flux. This is the intended coherence: their algebraic phase changes agree, although their contributions to entropy remain weighted by the full law.

The positive phase mechanism is real, not just a heuristic. To prove this at the smallest relevant window, set c1=c2=x with 0<x<1/8 and mean 1/2. These coefficients also define a strict scalar symbol by the L1 bound. For the three-site phase curve the eight probabilities occur in four complementary pairs

    u_j + v(t), u_j - v(t),
    v(t)=2x^3 cos(3t),
    u_1=1/8-3x^2/2,
    u_2=u_3=u_4=1/8+x^2/2.

This follows either by expanding the 3 by 3 event determinants or by the centered moment expansion proved below. All these probabilities are strictly positive. Write

    G(v)=-sum_{j=1}^4 [(u_j+v)log(u_j+v)+(u_j-v)log(u_j-v)].

For v>0,

    G'(v)=-sum_j log((u_j+v)/(u_j-v)) < 0.

At t=0 every event score vanishes and v''(0)=-9v(0). Therefore

    (H_phase)''(0)=-9v(0)G'(v(0))>0.

This is a complete-event positive phase curvature statement. It is not an affine entropy counterexample. The unavoidable radial term in (1) has the opposite sign, as established next.

## 3. Exact radial sign obstruction

This paragraph proves only monotonicity, not the stronger radial concavity claim explored separately by the main instance.

Let P have fixed Bernoulli marginals q_i, let pi be their independent product, and independently retain each coordinate with probability r; otherwise replace it by an independent draw with law Bernoulli(q_i). Denote this channel by T_r. Its action on centered joint moments is multiplication by r^|A|. For a DPP with K=diag(q_i)+C and C_ii=0,

    E_P product_{i in A}(X_i-q_i)=det C_A.             (2)

To prove (2), expand the product and substitute DPP inclusion moments. The resulting principal-minor expansion is det(K_A-diag(q_i:i in A)). Hence T_r P is the DPP with kernel diag(q_i)+rC, because all its centered moments equal det(rC_A), and all moments determine a finite binary law.

For 0<=r1<=r2<=1, T_r1=T_(r1/r2) T_r2 when r2>0. A Markov channel preserving pi contracts relative entropy. One direct proof applies Jensen to the density ratio under the reverse kernel of pi: the convex function z log z yields D(TP||pi)<=D(P||pi). Since all marginals remain q_i,

    H(P)=sum_i h(q_i)-D(P||pi).

Thus H(T_r P) is nonincreasing in r. At a strict K, the radial differential dH_K(C) is nonpositive, taking the derivative at r=1 from below, which equals the ordinary derivative by smoothness. In the two-harmonic shear, (1) consequently requires

    H_phase'' > -dH_K(C)

before affine acceleration can even beat its full Fisher cost. The positive phase theorem above supplies one side of this competition; it supplies no inequality comparing the two sides.

## 4. A finite-window weak-coupling theorem

**Statement.** Fix n<infinity, q in (0,1), a Hermitian zero-diagonal matrix C, and real antisymmetric a_ij. Put B_ij=i a_ij C_ij, B_ii=0, and assume B is nonzero. For sufficiently small positive epsilon, define the strict affine curve

    K_epsilon(t)=qI+epsilon(C+tB).

Then, at t=0,

    H''(K_epsilon;epsilon B)
      = -[2 epsilon^4/(q^2(1-q)^2)]
          sum_{i<j} a_ij^2 |C_ij|^4 + O(epsilon^6).  (3)

In particular it is strictly negative for all sufficiently small positive epsilon. The full Fisher information is O(epsilon^6), and the fixed-modulus phase curvature is O(epsilon^6). The constants and the allowed epsilon may depend on n,C,a,q. No volume-uniform assertion is included.

**Proof.** Let v=q(1-q)>0, pi=Bernoulli(q)^n, and Z_i=(X_i-q)/sqrt(v). Products Z_A form an orthonormal basis in L2(pi). By (2), the probability density R_epsilon,t=P_epsilon,t/pi is exactly

    R_epsilon,t = 1 + sum_{|A|>=2}
       epsilon^|A| det(C+tB)_A / v^(|A|/2) * Z_A.

This identity follows by taking every Fourier coefficient against Z_A. The singleton coefficient is zero because the diagonal is fixed. Write R=1+U. On the finite state space U=O(epsilon^2), uniformly for t in a small fixed interval. Positivity at epsilon=0 permits an analytic Taylor expansion and two t derivatives of its remainder. The one-point marginals imply

    H(P_epsilon,t)=n h(q)-D(P_epsilon,t||pi),
    D=E_pi[(1+U)log(1+U)]
     =1/2 E_pi[U^2]-1/6 E_pi[U^3]+O(epsilon^8).

The degree-two part of U is

    U_2=-epsilon^2/v sum_{i<j}|C_ij+tB_ij|^2 Z_i Z_j.

Orthogonality makes the degree-two and degree-three parts orthogonal. Therefore the epsilon^5 term in E U^2 is zero, and

    D=epsilon^4/(2v^2) sum_{i<j}|C_ij+tB_ij|^4
       +O(epsilon^6).

The remainder and its first two t derivatives are O(epsilon^6), since they are analytic functions on a fixed finite state space with the stated vanishing coefficients. Now

    |C_ij+tB_ij|^2=|C_ij|^2(1+a_ij^2 t^2).

Two t derivatives give (3). Its leading coefficient is strictly negative because B nonzero implies some a_ij C_ij nonzero.

For Fisher, all degree-two density derivatives vanish at t=0, so R'_epsilon,0=O(epsilon^3). The positive denominator R=1+O(epsilon^2) yields E_pi[(R')^2/R]=O(epsilon^6). For the phase curve, every |C_ij| is constant, so the degree-four entropy coefficient has zero phase derivative of every order; its phase curvature is O(epsilon^6). This completes the proof.

The theorem rules out the proposed existing-edge phase tangent mechanism near independent finite kernels. It does not cover directions introducing edges at which C_ij=0, arbitrary strong-coupling kernels, or an entropy-rate limit. Those exclusions are part of the theorem statement, not silent assumptions.

## 5. One frozen fixed scalar chord

The analytic decomposition above motivated the only numerical input, recorded before execution in frozen.md and input.json:

    q=1/2, x=3/25, z=(99+20i)/101,
    c1=x, c2=xz, a1=1, a2=-1,
    s=1/4,
    f_t(theta)=1/2+2 Re(sum_{k=1}^2 c_k(1+i t a_k)e^(-2pi i k theta)).

Since 99^2+20^2=101^2, |z|=1. For |t|<=1/4,

    |f_t-1/2| <= 4x sqrt(1+t^2) <= 3 sqrt(17)/25 < 1/2.

The final inequality follows by squaring: 9*17/625=153/625<1/4. Thus the fixed symbols f_-s,f_0,f_s all satisfy tau<=f<=1-tau with

    tau=1/2-3sqrt(17)/25>0.

This is a pointwise proof, not a grid check. The centre is non-even, and C=x^3 conjugate(z) has nonzero imaginary part. Its complete-event scores therefore do not vanish: already the three-point inclusion derivative -6 Im(C) is nonzero. It remains exactly pair-score-invisible.

At window n=8, all 256 events were retained. The following numbers are diagnostics in nats:

| Quantity | Value |
|---|---:|
| Complete Fisher F | 0.001763694568746871 |
| Affine event acceleration -sum p''log p | -0.06922497827885540 |
| Affine H'' | -0.07098867284760227 |
| Radial dH(E) | -0.11200845606788071 |
| Phase event acceleration | +0.04278347778902532 |
| Phase H'' | +0.04101978322027845 |
| Fixed finite-window midpoint gap | -0.002403635340833432 |

The intended phase gain survives the complete Fisher cost: phase acceleration is positive and larger than F. However, the radial term is still larger in magnitude and makes the affine acceleration itself negative. This identifies the obstruction more precisely than a missing positive Hessian eigenvalue. It does not rigorously exclude the fixed chord at the true entropy rate.

The three finite entropies were evaluated separately:
H_-=5.517833093408155, H_0=5.519657475320029, H_+=5.516674586550236. Endpoint equality was not assumed. The code also checks the affine and phase second derivatives by independent small determinant evaluations; these are stability checks, not interval bounds and not extra candidate searches.

## 6. Computation, limitations, and handoff

The implementation uses the exact-event row matrix M_S with row K_i if i is occupied and row (I-K)_i otherwise. Multilinearity shows det M_S=p_K(S). Its derivative row matrices V and W give

    p'=p tr(M^-1 V),
    p''=p[(tr(M^-1 V))^2-tr((M^-1 V)^2)],
    p_E'=p tr(M^-1 W).

These identities hold because p>0 makes M invertible. All event probabilities, two affine derivatives, radial derivatives, and endpoint probabilities are stored in events_n8.csv. Exact rational three-site event polynomials and normalization identities are separately stored in exact_n3.json. The n=8 values use double precision and contain no rigorous rounding enclosure. No test sign is promoted to a mathematical counterexample or certified exclusion.

The execution used one CPU thread, no GPU, and no global dependency changes. The supplied check.py, input.json, output.json, run.log and exit_status.txt suffice for replay with Python, NumPy and SymPy. Versions and the actual process identifier are recorded in output.json. The successful exit status is 0. An initial default-interpreter dependency probe failed because NumPy was absent; the authorized route-specific environment was then used. No background job remains in this child unit.

Author checks are complete; non-author review is **not yet performed**. No Lean or other proof assistant was run. Literature novelty is **unverified**. No three-symbol entropy-rate intervals were computed, so neither the positive gate (L_-+L_+)/2-U_0>0 nor the strict exclusion gate (U_-+U_+)/2-L_0<0 is asserted.

The minimal remaining obligation for this mechanism is a controlled strong-coupling inequality or a fixed example where H_phase'' exceeds the full radial cost. Increasing a phase Hessian scan does not address that obligation. One alternative is to make the remainder in (3) uniform per site for a fixed finite-band symbol; that would yield an actual weak-coupling entropy-rate theorem, but such a remainder is not established here. This bounded unit stops with these explicit gaps.
