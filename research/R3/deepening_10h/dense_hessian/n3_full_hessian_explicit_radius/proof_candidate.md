# Explicit full-Hessian ball around K_*

STATUS: PROOF_CANDIDATE_PENDING_INDEPENDENT_REVIEW.

The proof transfers the verified S5 Frobenius curvature margin using a fully
explicit determinant third-derivative bound. Every estimate below applies to
arbitrary real symmetric directions. No PSD trace argument is needed.

## 1. Exact-event determinant and its operator norm

For S subset {1,2,3}, let C be its complement and I_C the diagonal projector
onto C. Inclusion-probability Mobius inversion gives

    p_S(K)=sum_{A subset C}(-1)^|A| det K_{S union A}.

Expanding det(K-I_C) in its selected -1 diagonal entries gives

    det(K-I_C)=sum_{A subset C}(-1)^(|C|-|A|)det K_{S union A}.

Therefore the signed determinant is an exact event formula:

    p_S(K)=(-1)^|C| det B_S(K), B_S(K)=K-I_C.              (1)

For 0<K<I and a unit vector z,

    -1 < z^T K z - ||I_C z||^2 < 1.

Since B_S is symmetric, ||B_S||_op<=1. Every column of B_S consequently has
Euclidean norm at most one. This fact concerns the signed atom matrix B_S,
which need not be positive definite.

## 2. Strictness of the whole ball precedes all log estimates

The spectral distance of K_* to the boundary of 0<K<I is at least 1/5.
Write E=K-K_* and K_u=K_*+uE, 0<=u<=1. If ||E||_F<=1/10 then, for every
unit vector z,

    z^T K_u z >= 1/5-||uE||_op >= 1/10,
    z^T (I-K_u)z >= 1/5-||uE||_op >= 1/10.

Here ||E||_op<=||E||_F, including indefinite E. Thus the complete segment,
and indeed the complete closed radius-1/10 ball in Sym(3), is strict. No
circular assumption about atom positivity is used to establish strictness.

## 3. Mixed determinant derivatives, with all factorials

The determinant is multilinear in columns. For its first derivative in E
there are three replaced-column determinants. For a mixed second derivative
in E,D there are 3*2 ordered distinct-column choices. For the third derivative
in E,D,D there are 3*2*1 choices. The two occurrences of D are labelled
derivative slots: their multiplicities are already counted by the six choices.

Hadamard's inequality bounds each term by the product of column norms. Each
unchanged column has norm <=1; a direction column is at most the Frobenius
norm of its full direction matrix. The sign in (1) does not affect absolute
values. Consequently, at every strict K,

    |p_E| <= 3||E||_F,          |p_D| <= 3||D||_F,
    |p_ED| <= 6||E||_F||D||_F,  |p_DD| <= 6||D||_F^2,
    |p_EDD| <= 6||E||_F||D||_F^2.                         (2)

Repeated directions, singular directions, noncommuting directions and
indefinite directions are all included. These bounds do not use coordinate
Euclidean norms, so there is no missing off-diagonal factor or sqrt(2).

If also ||E||_F<=q/6, integrate the first bound along the strict segment:

    p_S(K_u) >= p_S(K_*)-3u||E||_F >= q/2=m=87/2500.    (3)

Every atom is at most one because it is an exact event probability. Thus
m<=p_S(K_u)<=1 uniformly over all eight events and every u in [0,1].

## 4. A fully rational third-derivative constant

For f(p)=-p log p,

    f'=-(1+log p), f''=-1/p, f'''=1/p^2.

On m<=p<=1, |f'|<=3, |f''|<=1/m, |f'''|<=1/m^2. To check the first
constant without a floating logarithm, note

    exp(4) > sum_{j=0}^4 4^j/j! = 103/3 > 2500/87 = 1/m.

Hence log m>-4, so -3<1+log p<=1 and |1+log p|<=3. The generous constant
3 is rational and valid throughout the interval, including p=1.

Differentiate twice in D and once in E:

    D^3(f o p)[E,D,D]
      = f''' p_E p_D^2
        + f''(2 p_ED p_D + p_E p_DD)
        + f' p_EDD.                                     (4)

The coefficient two comes from differentiating the two first-derivative
factors, not from a determinant convention. Combining (2)--(4), one event
contributes in absolute value at most

    (27/m^2 + 54/m + 18)||E||_F||D||_F^2.

There are exactly eight events; the triangle inequality therefore proves

    |D^3 H(K_u)[E,D,D]| <= L||E||_F||D||_F^2,
    L=8(27/m^2+54/m+18)=160561104/841.                   (5)

This estimate deliberately uses no cancellations between events. It is valid
even for D not preserving any spectral basis or cone.

## 5. Uniform Hessian comparison and exact radius

The atoms are polynomials and stay positive by (3), so H is smooth on a
neighborhood of the segment. For a fixed arbitrary symmetric D, the fundamental
theorem of calculus and (5) give

    |H''_K[D,D]-H''_{K_*}[D,D]|
       <= L||K-K_*||_F||D||_F^2.                        (6)

There is a single constant for all E and D. In Frobenius geometry the Hessian
is self-adjoint; the norm of its difference as an operator equals the supremum
of the absolute quadratic form on the Frobenius unit sphere. Thus (6) also
gives the genuine operator estimate

    ||Hess H(K)-Hess H(K_*)||_{F->F} <= L||K-K_*||_F.    (7)

One could use (6) alone; (7) makes explicit that no direction-dependent
continuity radius or coordinate-norm conversion is hidden.

Define

    delta=min{1/10, q/6, 43/(100L)}
         =36163/16056110400
         =0.00000225228894788864929578461294087763621754867853923077...

The rational comparison of these three entries is performed exactly in the
sanity script. For ||K-K_*||_F<=delta, Sections 2--3 apply and the loss in
(6) is at most (43/100)||D||_F^2. The S5 input is the already converted
Frobenius bound H''_{K_*}[D,D]<=-(43/50)||D||_F^2, not the six-coordinate
bound. Subtracting half of this margin yields

    H''_K[D,D] <= -(43/100)||D||_F^2.                    (8)

This proves the frozen conclusion on the entire closed ball. Equality at D=0
is harmless; (8) is strictly negative for every other real symmetric D.

## 6. Chords, scope and conservatism

The Frobenius ball is convex. If a fixed affine segment K+tD, |t|<=h, lies
inside it, integrating (8) twice gives the optional explicit chord consequence

    [H(K-hD)+H(K+hD)]/2-H(K) <= -(43/200)h^2||D||_F^2.

For center K_* it suffices that |h| ||D||_F<=delta. The radius is extremely
conservative: it protects every event independently by its smallest base
probability, uses whole-matrix norms for individual determinant columns,
and discards every possible cancellation in entropy's third derivative.
It is not an estimate of the actual maximal concavity region.

This small ball also stays away from decoupling: every off-diagonal magnitude
is at least 29/175-delta>4/25. Its coordinate diagonals remain distinct since
their minimum base separation is 3/1400>2delta. Its eigenvalues remain distinct
since the minimum base spectral gap is 1/100>2delta. These observations are not
used in the derivative proof, but show the ball is a genuinely connected,
heterogeneous, non-repeated-spectrum region rather than a diagonal limit.

Imported input is only the verified S5 base data and its full-Hessian bound,
not an empirical non-hit. The S6 derivative method motivated the transfer;
its determinant identity, derivative counts, chain rule and constants were
rederived above. The global concavity question remains INCOMPLETE. This author
draft and its finite sanity computations await a non-author correctness review.
