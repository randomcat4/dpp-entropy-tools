# Finite-band true entropy-rate certificate: self-contained error argument

This supplements rate_analysis.md and the runnable C3-M1 certificate. It
rebuilds the S1 error argument so no private or source checkout is needed.
It is separate from the proved radial theorem in ../proof.md.

## 1. Exact boundary operator residual

For each of f_t and 1-f_t, epsilon<=f<=1-epsilon gives an infinite Toeplitz
operator epsilon I<=K<= (1-epsilon)I. Split past P={-1,-2,...} and future
F={0,1,...}, writing blocks T,B,C. The all-one conditioned future kernel is
C_inf=C-B* T^{-1}B. Finite-past Schur complements converge to this operator:
the finite Galerkin solutions minimize the coercive quadratic form for
T and converge in its energy norm, since finitely supported past vectors
are dense and T>=epsilon I. For any future vector v, the Schur quadratic
form is inf_z <(z,v),K(z,v)>, hence C_inf>=epsilon I; also C_inf<=C<=
(1-epsilon)I. The all-zero kernel is I minus the corresponding all-one
kernel for 1-f and has the same margin.

Let X be the finitely supported rational proposal stored in the artifact,
R=B-TX, and A=C-B*X-X*B+X*TX. Writing Y=T^{-1}B gives

    A-C_inf=(Y-X)*T(Y-X)=R*T^{-1}R.

Thus 0<=A-C_inf<=delta I with delta=||R||_F^2/epsilon as any certified
upper bound. The implementation uses the larger rational bound
delta=(sum_{r,j}(|Re R_rj|+|Im R_rj|))^2/epsilon.

For degree m=2, B has only its first m future columns nonzero. A proposal
supported on the first M=64 past rows has residual on only M+m=66 past
rows; every other row is exactly zero by bandwidth. The implementation
checks all 66 rows, and the correction A-C is confined to the leading
2 by 2 future corner. This is why the finite suffix matrix uses that corner
replacement. This argument is not transferred to a long-range symbol.

## 2. Uniform conditional-probability error

For a finite suffix pattern gamma on S and target v outside S, put
E=Q_SS-diag(1_{gamma_i=0}). Exact event conditioning gives

    q(Q,gamma)=Q_vv-Q_vS E^{-1} Q_Sv.                     (1)

To justify invertibility uniformly, let J=diag(2gamma_i-1). If Q has
spectral margin a>0, the Hermitian part of JE has diagonal blocks Q_11
and I-Q_00 and zero cross blocks, so it is at least aI. For every z,

    a||z||^2<=Re <z,JEz><=||z|| ||Ez||,

which gives ||E^{-1}||<=1/a. This covers every pattern and every suffix
length without dividing by a tiny event-probability bound.

Interpolate between a true extreme kernel and its approximation A. With
operator error delta<epsilon, every interpolated kernel has margin at least
epsilon-delta and norm at most 1+delta. Differentiating (1) in direction V
gives w*Vw with w_v=1 and w_S=-E^{-1}Q_Sv. Therefore

    |q(A,gamma)-q(C_inf,gamma)|
       <=delta[1+((1+delta)/(epsilon-delta))^2]=:e.        (2)

This is a finite-matrix Lipschitz bound uniform in suffix length. All its
constants are rational in the certificate. Complementing is an isometry
for operator errors, so the same argument applies to the all-zero case.

## 3. Lower and upper bounds for one fixed process

We use the standard conditional negative-association theorem for discrete
Hermitian DPPs, including after any finite exact conditioning. It implies
that the conditional probability of one target decreases when an additionally
observed coordinate is set to one rather than zero. Apply this one
coordinate at a time while keeping gamma fixed; take the extreme all-one
and all-zero limits and the usual entire-past conditional-probability
martingale. This gives, almost surely on the suffix event gamma,

    q_1(gamma)<=P(X_v=1 | entire past)<=q_0(gamma).        (3)

The relevant primary source is Lyons–Steif, Section 2 (conditional negative
association and Proposition 2.6) and Section 6 (Proposition 6.10, equation
(6.5), Theorem 6.12). The uniform margin here makes every finite exact
conditioning legitimate and the one-sided Schur limits coercive.

Let w_gamma be the ordinary stationary suffix probability, and let qtilde_1,
qtilde_0 be the rational conditional values from the two approximate extreme
kernels. Form

    l_gamma=max(epsilon,qtilde_1-e_1),
    u_gamma=min(1-epsilon,qtilde_0+e_0).

The true entire-past probability lies in this interval by (2)-(3). Binary
entropy b(x)=-x log x-(1-x)log(1-x) is concave, so its minimum on an interval
occurs at an endpoint. The stationary conditional-entropy formula yields

    L_n=sum_gamma w_gamma min(b(l_gamma),b(u_gamma)) <= h(f).

Conditioning on only the suffix gives

    h(f)<=U_n=sum_gamma w_gamma b(P(X_v=1 | gamma)).

The three t values require three separate copies of this construction,
and f and 1-f require their own boundary solves. No endpoint identification
or finite-entropy extrapolation is used.

## 4. Exact arithmetic and the sign

Each finite event mass is (-1)^{#zeros} det(Q-diag(1_zero)). The code scales
the rational complex matrix to Gaussian integers, uses fraction-free
Bareiss elimination, verifies each complex division is exact, verifies
zero imaginary determinant part, positive masses and exact normalization.
Every conditional ratio and weight is then rational. The author self-audit
uses a separate exact Gaussian-elimination routine for those masses.

mpmath interval logarithms at 45 decimal digits enclose binary entropies.
Rational inputs enter as interval numerator/denominator divisions. Dyadic
interval endpoints are extracted exactly as Fractions; all products, sums
and minima use outward bounds. The lower true gap uses the lower endpoint
rate bounds minus the upper centre bound. The upper true gap uses the upper
endpoint bounds minus the lower centre bound.

For C3-M1 the upper gate is exactly

    -299855012916397501897282364769067397783
    /356811923176489970264571492362373784095686656 < 0.

This proves the fixed-object negative exclusion, conditional on the standard
DPP conditioning theorem specified above and the separately recorded
implementation audit. It is not a continuous-family exclusion.
