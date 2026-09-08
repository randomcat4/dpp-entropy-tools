# Half-filled symmetric triangle: standard-mode curvature

Author status: PROVED for `frozen_standard_modes_v1.md`, pending an independent
non-author review. The existential target `frozen_theorem_v1.md` is INCOMPLETE.
This document also gives an exact full-six-dimensional reduction; its remaining
two-dimensional sign condition is not asserted.

## 1. Definitions and full-dimensional decomposition

Write K(d,r) for the symmetric matrix with diagonal d and off-diagonal r.
Its strict feasibility domain is

    0 < d-r < 1,       0 < d+2r < 1.

The eight complete-event probabilities, grouped by cardinality, are

    A = (1-d)^3 - 3(1-d)r^2 - 2r^3,
    B = d(1-d)^2 + (2-3d)r^2 + 2r^3,
    C = d^2(1-d) + (3d-1)r^2 - 2r^3,
    D = d^3 - 3dr^2 + 2r^3.

The multiplicities are 1,3,3,1, respectively. These follow by applying the
inclusion-exclusion definition to the principal minors 1,d,d^2-r^2,det K.
All four probabilities are positive on the strict feasibility domain. One
way to verify positivity without a boundary convention is to set
L=K(I-K)^(-1)>0 and use p(S)=det L[S]/det(I+L); this identity follows by
equating coefficients in det(I-K+K diag(z)). Each principal minor of a
positive definite matrix is positive.

Put

    M = (1-d)log A + (3d-2)log B + (1-3d)log C + d log D,
    Lg = log A - 3log B + 3log C - log D.

Here Lg is a scalar; it is unrelated to the matrix L above. For a symmetric
direction V, set x=(V11,V22,V33) and y=(V23,V13,V12). Write

    a = (x1+x2+x3)/3, b = (y1+y2+y3)/3,
    x0=x-a(1,1,1), y0=y-b(1,1,1).

Define two quadratic forms T and S. First let

    a1 = -3((1-d)^2-r^2)u - 6r(1-d+r)v,
    b1 = ((1-d)(1-3d)-3r^2)u + (2r(2-3d)+6r^2)v,
    c1 = (d(2-3d)+3r^2)u + (2r(3d-1)-6r^2)v,
    d1 = 3(d^2-r^2)u + 6r(r-d)v.

Then

    T(u,v) = a1^2/A + 3b1^2/B + 3c1^2/C + d1^2/D
             + 6M u^2 + 12r Lg uv + (-6M-12r Lg)v^2,

    S(u,v) = 2[((1-d)u-2rv)^2/B + (du+2rv)^2/C]
             - 2M u^2 + 8r Lg uv + (-4M+4r Lg)v^2.

If S(u,v)=S11 u^2+2S12 uv+S22 v^2, the exact full-dimensional identity is

    -D^2 H(K(d,r))[V,V]
      = T(a,b) + (S11 ||x0||^2 + 2S12 <x0,y0> + S22 ||y0||^2)/2.   (1)

Thus T is the trivial 2 by 2 block, and S is the standard 2 by 2 block with
multiplicity two. This is an identity on all six real symmetric directions.

For completeness, its representation argument needs no representation-theory
black box. Permuting the three vertices simultaneously permutes x and y and
leaves entropy unchanged. A quadratic form invariant under these permutations
has constant diagonal and constant off-diagonal coefficients in each of its
x-x, y-y and x-y blocks. It therefore splits into the respective means and
zero-sum parts, with no cross term between those parts. On the zero-sum parts
it is a linear combination of ||x0||^2, <x0,y0>, ||y0||^2. Evaluating on
x=u(1,1,1), y=v(1,1,1) determines T; evaluating on x=u(1,-1,0),
y=v(1,-1,0) determines S and the factor 1/2 in (1).

Here is a direct check of the derivative calculation. For any affine kernel
line, differentiating entropy twice and using sum p''=0 gives

    -H'' = sum_S (p'_S)^2/p_S + sum_S p''_S log p_S.               (2)

For the trivial direction the first derivatives are a1,b1,c1,d1, with
multiplicities 1,3,3,1. The second derivatives summed within cardinalities
0,1,2,3 have the following coefficients of (u^2,uv,v^2):

    0: (6-6d,    12r,  6d-12r-6),
    1: (18d-12, -36r, -18d+36r+12),
    2: (6-18d,   36r,  18d-36r-6),
    3: (6d,     -12r, -6d+12r).

For the standard test direction the first derivatives vanish for cardinality
0 and 3; among singletons they are ((1-d)u-2rv), its negative, and zero;
among pairs they are (du+2rv), its negative, and zero. The corresponding
second-derivative coefficient rows are

    0: (2d-2,   8r,   4d+4r-4),
    1: (4-6d, -24r, -12d-12r+8),
    2: (6d-2,  24r,  12d+12r-4),
    3: (-2d,   -8r,  -4d-4r).

Substitution into (2) gives precisely T and S. The accompanying finite
symbolic replay checks these polynomial derivative tables and the general
six-dimensional identity; it is supplementary to the displayed derivation.

## 2. Half-filled standard block

Take d=1/2 and initially 0<r<1/4. Set q=2r, so 0<q<1/2. Factoring the
probabilities gives

    8A=(1+q)^2(1-2q),       8D=(1-q)^2(1+2q),
    8B=(1+q)(1-q+2q^2),    8C=(1-q)(1+q+2q^2).

In particular all displayed logarithms have positive arguments. Define

    m=-M=-1/2 log[(1-q^2)(1-4q^2)/(1+3q^2+4q^4)],
    ell=-r Lg=-q Lg/2,
    Lg=log[(1-q)(1-2q)(1+q+2q^2)^3 /
           ((1+q)(1+2q)(1-q+2q^2)^3)].

We will prove

    m > 2 ell > 0.                                               (3)

Let

    E(q)=(1-q^2)(1-4q^2)(1+3q^2+4q^4)>0.

Direct differentiation gives

    M'(q)=8q(2q^2-1)(2q^2+1)/E(q)<0,
    Lg'(q)=48q^2(2q^2-1)/E(q)<0,
    Lg'(q)/M'(q)=6q/(1+2q^2).                                   (4)

Both M and Lg vanish at zero. Put w(s)=-M'(s)>0 for 0<s<1/2 and
g(s)=6s/(1+2s^2). Then

    m(q)=integral_0^q w(s) ds,
    -Lg(q)=integral_0^q g(s) w(s) ds.

The derivative g'(s)=6(1-2s^2)/(1+2s^2)^2 is positive on this interval.
Consequently

    0 < 2 ell(q) = q integral_0^q g(s)w(s) ds
                  <= [6q^2/(1+2q^2)] m(q) < m(q),

where the last inequality is exactly 4q^2<1. This proves (3) for every
point in the open interval, including arbitrarily near its endpoints.

At half filling, the non-Fisher part of S is

    R(u,v)=2m u^2 - 8ell uv + (4m-4ell)v^2.

Its matrix has upper-left entry 2m>0 and determinant

    (2m)(4m-4ell)-16ell^2 = 8(m-2ell)(m+ell)>0.

It is therefore positive definite. The remaining part of S is a sum of
nonnegative squares divided by positive B,C. Thus S is positive definite.

If r<0, complementation of events gives H(K)=H(I-K). Since
I-K(1/2,r)=K(1/2,-r), the Hessian at r on V equals that at -r on -V, which
equals that at -r on V by quadraticity. This transfers the result from
positive r without using an inadmissible change of basis or altering the
triangle sign product.

At r=0, A=B=C=D=1/8 and M=Lg=0. Hence S(u,v)=8u^2.

## 3. Conclusion and exact remaining blocker

Under the frozen standard-mode constraints tr V=0 and
V12+V13+V23=0, we have a=b=0, x0=x, y0=y. Formula (1) and the positive
definiteness of S prove

    D^2 H(K(1/2,r))[V,V] < 0   if 0<|r|<1/4 and V is nonzero.

At r=0, (1) gives exactly -4 sum_i Vii^2. In every case the asserted weak
inequality follows. All directions are real symmetric, and strict spectral
feasibility ensures a sufficiently short affine line around each center.
There is no claim about an entire finite chord with a non-symmetric center.

For these half-filled symmetric centers, full-six-dimensional nonpositivity
is now equivalent to the 2 by 2 matrix of T being positive semidefinite:

    T11 >= 0,  T22 >= 0,  T11*T22-T12^2 >= 0.                     (5)

These explicit one-variable inequalities remain UNPROVED here. They are an
equivalent blocker for the local full-Hessian assertion at this restricted
one-parameter family, and a strictly restricted scope relative to the
original general-connected-center existential question. For arbitrary d,r,
both T and S must be positive semidefinite; the displayed reduction alone
does not establish either sign.

No conditioning argument is used, so no nonaffine conditional-kernel
acceleration is omitted. No numerical sample is used as a sign proof.
