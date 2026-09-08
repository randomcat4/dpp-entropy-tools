# Reflection reduction and an entire centered-path proof

AUTHOR PROOF CANDIDATE — pending independent review. The general two-parameter
family remains INCOMPLETE. The centered theorem below has a complete analytic
argument; its numerical checks are not its proof.

## 1. Scope, atoms and invariances

K(x,a) has eigenvalues x,x±sqrt(2)a. Its exact strict domain is

0<x<1, 0<sqrt(2)|a|<min(x,1-x).

Diagonal sign conjugation by diag(1,-1,1) changes a to -a and preserves every
event probability. Complementation sends (x,a) to (1-x,-a) and permutes atoms.
Both operations preserve definiteness of the full Hessian by an invertible
linear transformation on Sym(3), not just curvature in family directions.

Put t=a². In the event order empty,1,2,12,3,13,23,123 the probabilities are

(E,U,W,V,U,Z,V,F), where

E=(1-x)((1-x)²-2t),

F=x(x²-2t),

U=x(1-x)²+(1-2x)t,

W=x(1-x)²+2(1-x)t,

V=x²(1-x)+(2x-1)t,

Z=x²(1-x)+2xt.

These are obtained from q12=q23=x²-t, q13=x² and r=x³-2xt by Möbius
inversion. They are exact events, not inclusion probabilities. All are
positive on the stated strict domain.

Write

ell=log(E V/(U W)), kappa=log(E Z/U²),

Lambda=log(F U² W/(E V² Z)),

n=-ell-Lambda x, m=-kappa-Lambda x.

The reviewed U8 cofactor matrix is

N=[[n,-Lambda a,0],[-Lambda a,m,-Lambda a],[0,-Lambda a,n]].

Connectedness gives N>0. In particular n>0,m>0 and
q:=nm-2Lambda²a²>0. The exact full-Hessian identity is

B(D)=Fisher(D)-2tr(N adj D).                                  (1)

It applies to all real-symmetric directions, including noncommuting and
indefinite directions.

## 2. Reflection: the odd two-dimensional block is always strict

Reflection 1<->3 fixes K and preserves H, so the Hessian has no mixed terms
between the even and odd eigenspaces of this reflection. Write

D_even=[[d,h,k],[h,e,h],[k,h,d]],

D_odd=[[d,h,0],[h,0,-h],[0,-h,-d]].

For the odd block, direct cofactors in (1) give

B(D_odd)=Fisher(D_odd)+2m d²+8Lambda a d h+4n h².              (2)

The last quadratic form has positive first diagonal and determinant
8(nm-2Lambda²a²)>0. Therefore this complete two-dimensional block is strictly
positive for every nonzero odd D throughout the full two-parameter strict
domain. No numerical sign test is used.

All remaining uncertainty is in the four-dimensional even block.

## 3. Entire centered-path theorem

**Theorem candidate.** For x=1/2 and every real nonzero a with 8a²<1,
B_K is positive definite on the whole space Sym(3).

This does not assert a uniform positive lower bound as a tends to zero or
to the spectral boundary.

### 3.1 Additional symmetry and normalized variables

Put r=8a² in (0,1), u=r², L=1-r² and v=2-r². The event probabilities reduce to

E=F=(1-r)/8, U=V=1/8, W=Z=(1+r)/8.

Thus Lambda=0 and N=diag(n,m,n), with

n=log((1+r)/(1-r)), m=-log(1-r²), both positive.

Here r is 8a²; u=r² is NOT a². This distinction matters in every displayed
matrix below.

Let S=diag(1,-1,1). At this centered K, I-K=SKS. The affine entropy symmetry
X -> S(I-X)S fixes K and acts on directions as D -> -SDS. In the reflection
even subspace it sends (d,e,k) to their negatives while leaving h fixed.
Consequently h has no Hessian cross terms with (d,e,k).

The h-only block has B>=4n h²>0 by (1). The odd block is already strict by
(2), now with Lambda=0. It remains to prove a three-dimensional core strict.

### 3.2 Exact core quadratic form

For D=[[d,0,k],[0,e,0],[k,0,d]], the derivatives of the full event, a pair
12 or 23, and the pair 13, respectively, are

[(2-r)d+e+r k]/4,

[r d+e-r k]/4,

[(2+r)d-e-r k]/4.

Complementary events have opposite derivatives. Multiplicities give the
exact Fisher form

F_core = ((2-r)d+e+r k)²/(1-r)
       +2(r d+e-r k)²
       +((2+r)d-e-r k)²/(1+r).

Therefore

B_core=F_core-4n d e-2m d²+2m k².                             (3)

Equivalently B_core=(2/L)(d,e,k) C (d,e,k)^T, where

C=[[4-2u-u²-mL, r v-nL, u²],
   [r v-nL,     v,      r u],
   [u²,         r u,    u v+mL]].                            (4)

This is a congruence calculation in the explicit repeated-entry direction
coordinates, not a claim that those coordinates are Frobenius orthonormal.
Their lack of orthonormality does not affect positive definiteness.

### 3.3 Schur reduction to a two-dimensional determinant

Since C_ee=v>0, eliminate its e coordinate. The remaining Schur matrix on
(d,k) is L T, with

T=[[4+2rn-m-(L/v)n², (r³/v)n],
   [(r³/v)n,         m+4u/v]].                               (5)

The bottom-right entry is positive. Define z=rn-m. Exact expansion gives

det T=[m(8-Ln²)+8u z+16u-v z²]/v.                            (6)

The standard-library script checks this as a polynomial identity in formal
r,n,m after multiplication by v²; it is not merely a check at selected
logarithm values. It also rederives the core from independent exact-event
Hessian jets at the finite sanity points.

### 3.4 Two elementary inequalities settle the determinant

First, let s=(1/2)log((1+r)/(1-r))>0. Then r=tanh s and

Ln²=4s²/cosh²(s)<4,

because cosh s>=1+s²/2>s for every real s>0. The final inequality follows
from 1+s²/2-s=((s-1)²+1)/2>0.

Second,

z=rn-m=(1+r)log(1+r)+(1-r)log(1-r)
 =sum_(j>=1) u^j/[j(2j-1)].

All coefficients are positive. The sum of the coefficients equals 2log2,
by taking r upward to one (or by summing the absolutely convergent series).
For 0<u<1, therefore

0<z<=2(log2)u<2u.                                            (7)

The strict last bound follows from log2<1. Also u v=u(2-u)<1. Hence

v z²<4u²v<4u,

and the numerator in (6) has the strict lower bound

m(8-Ln²)+8uz+16u-vz² > 4m+12u >0.                            (8)

Thus det T>0 and T_kk>0, so T>0. Since L>0 and v>0, its Schur reconstruction
gives C>0; equation (3) gives B_core>0. Together with the h-only and odd
blocks this proves strict positivity on all six symmetric directions.

This proof covers every 0<8a²<1, arbitrarily close to either excluded
boundary, not just a compact grid. All signs of a are included by the
stated conjugation (or directly because the core depends on a²).

## 4. A rigorously uniform local thickening, with explicit quantifiers

Fix any 0<a_min<=a_max<1/(2sqrt(2)). There exists epsilon>0 such that

|x-1/2|<epsilon, a_min<=|a|<=a_max

implies strict feasibility and full-Hessian positivity.

Proof: take epsilon smaller than half the positive spectral margin
1/2-sqrt(2)a_max. The atom formulas and their logarithms are smooth on a
neighborhood of this compact parameter segment. The theorem makes
B(D)>0 there for every unit Frobenius direction D. Compactness of the
segment times the unit sphere gives a positive minimum at x=1/2.
Uniform continuity then preserves half that minimum for sufficiently
small |x-1/2|. This is an analytic compactness argument, not a grid-to-region
inference. No numerical radius is claimed, and epsilon may depend on both
endpoints. It is not uniform as a_min tends to zero or a_max to the boundary.

## 5. Explicit remaining scalar for general x

For the even direction (d,e,h,k), let the full-event derivative be

jF=2(x²-t)d+x² e-4xa h+2t k,

and put jQ=x(d+e)-2a h. The other distinct event derivatives are

jE=(4x-2)d+(2x-1)e-4a h-jF,

jU=(1-3x)d-x e+2a h+jF,

jW=-2x d+(1-2x)e+4a h+jF,

jV=jQ-jF,

jZ=2x d-jF.

These six linear forms and multiplicities (1,2,1,2,1,1) give

F_even=jE²/E+2jU²/U+jW²/W+2jV²/V+jZ²/Z+jF²/F.

The remaining four-coordinate form is exactly

B_even=F_even-4n d e+4n h²-2m d²+2m k²
                     -8Lambda a h(d-k).                      (9)

This explicitly gives every entry of a four by four matrix from six atom
values and three logs. Let eta be its weighted-trace linear functional.
Writing q=nm-2Lambda²a²>0, its entries in (d,e,h,k) are

eta=(2(nm-Lambda²a²)/(nq), n/q,
     4Lambda a/q, 2Lambda²a²/(nq)).

The e coefficient is positive. Define three column vectors

t_d=(1,-eta_d/eta_e,0,0),
t_h=(0,-eta_h/eta_e,1,0),
t_k=(0,-eta_k/eta_e,0,1),

and let T0 have these columns. Put e0=(0,1,0,0),

C0=T0^T B_even T0,
b0=T0^T B_even e0,
d0=e0^T B_even e0.

C0>0 throughout the entire strict path domain by the reviewed weighted-
trace-zero U8 inequality. Hence the exact remaining scalar is

**sigma(x,a)=d0-b0^T C0^-1 b0.**                             (10)

The full six-dimensional B is positive definite iff sigma>0. Equality
gives one zero direction; sigma<0 gives a genuine positive entropy-curvature
direction. No such sign failure has been proved or frozen in this unit.

The centered proof establishes sigma(1/2,a)>0 for its whole strict range,
and section 4 establishes the stated uniform thickening of compact pieces.
Proving sigma>0 at every other strict pair (x,a) remains unresolved. By
complementation it is enough to settle 0<x<1/2 and 0<a<x/sqrt(2), but this
reduction does not provide the missing sign inequality.

## 6. Review priorities

Most fragile steps: event derivative multiplicities in (3); distinguishing
r=8a² from u=r²; the factor 2/L in (4); the exact Schur matrix (5); the
determinant identity (6); and the use of two commuting symmetry actions to
remove the even h cross terms. General-x eta has off-diagonal coordinate
factors two/four; omitting these would change the residual scalar.

No finite search, projected PSD-only test, or fixed-eigenvector condition
enters the centered theorem. The new proof is awaiting a non-author audit.
