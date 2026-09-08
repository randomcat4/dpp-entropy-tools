# Closed exponential limit and its strict positivity

AUTHOR PROOF CANDIDATE. Independent review is required.

Let l=log2. With the normalization in frozen_problem.md, the claimed answer is

phi(beta)=(beta+l+2)(beta+l)^4/(2 beta^2 l^2), beta>0.       (1)

More precisely, for every compact interval J=[b0,b1] contained in (0,infinity),

sigma(x,exp(-beta/x))=phi(beta)+O_J(sqrt x)                 (2)

uniformly for beta in J. The proof below does not expand two huge cancelling
terms in the original Schur formula. It uses the exact variational meaning
of that same Schur complement, isolates its two positive penalties, and
controls the minimizing direction before taking a limit.

## 1. Exact setup and relation to stable Sherman--Morrison

Write D=[[d,h,k],[h,e,h],[k,h,d]], with coordinate vector z=(d,e,h,k).
Let eta(z)=tr(N^(-1)D), and eta_e=eta(e0)>0. The path reduction has
T0 spanning ker eta and

sigma=min_{eta(z)=eta_e} B(z,z).                            (3)

Indeed z=e0+T0 t and the Hessian on T0 is positive definite by the reviewed
weighted-trace-zero identity, so completing its square gives exactly the
Schur complement. This is also the variational object computed by the
source's stable Sherman--Morrison formula.

For additional algebraic verification, write

F_full=F_rest+(x/s)w_s w_s^T,
w_s=(1+s,1,-2sqrt(2)sqrt(1-s),1-s),
A0=F_rest+det(N)G_N>0,
G_N(z,z)=tr(N^(-1)D N^(-1)D).

Put

T=eta^T A0^(-1)eta
 -(eta^T A0^(-1)w_s)^2/[s/x+w_s^T A0^(-1)w_s].

Then T>0 and exactly

sigma=eta_e^2(1/T-det N).                                  (4)

This is the positive-matrix version of Sherman--Morrison, followed by
minimization with the one linear constraint. It equals (3), and hence the
source's SM formula whenever that source's auxiliary R block is invertible.
The proof of the limit below does not require that auxiliary R block to be
positive or even invertible.

All atoms and forms have the exact event semantics of the reviewed path
reduction. The full atom is F=x^3s and jF=x^2 w_s dot z. No inclusion
probability is substituted for an event probability.

## 2. Uniform coefficient limits

The five other distinct atoms, with multiplicities (1,2,1,2,1), satisfy

E=(1-x)(1-2x+x^2s),
U=x[(1-x)^2+(1-2x)x(1-s)/2],
W=x(1-x)(1-xs),
V=x^2[1+(1-2x)s]/2,
Z=x^2(1-xs).

Thus E->1, U/x->1, W/x->1, V/x^2->1/2, Z/x^2->1 uniformly on J.
After these explicit powers of x are cancelled, all non-full log ratios
are smooth functions near (x,s)=(0,0). In particular

ell=log(EV/(UW))=-l+O_J(x),
kappa=log(EZ/U^2)=O_J(x),
Lambda=log(FU^2W/(EV^2Z))=-beta/x+log4+O_J(x).

Here and below exponentially small s terms are absorbed uniformly into
O_J(x), because s<=exp(-b0/x)=o(x^m) for every fixed m. Therefore

n=-ell-xLambda=beta+l+O_J(x),
m=-kappa-xLambda=beta+O_J(x),
Lambda a=-beta/sqrt2+O_J(x),
q=nm-2Lambda^2a^2=beta l+O_J(x).

The cofactor matrix consequently converges uniformly to

N0=[[beta+l,beta/sqrt2,0],
    [beta/sqrt2,beta,beta/sqrt2],
    [0,beta/sqrt2,beta+l]].                                (5)

It is positive definite: its reflection-odd eigenvalue is beta+l, and
the even two-by-two determinant is beta l>0 with positive diagonal.
Its determinant is beta l(beta+l). On J all its spectral margins are
uniformly positive. Thus N and N^(-1) stay uniformly bounded and strict.

The weighted-trace covector has the uniform limit

eta_d -> (beta+2l)/[l(beta+l)],
eta_e -> (beta+l)/(beta l),
eta_h -> -2sqrt2/l,
eta_k -> beta/[l(beta+l)],                                 (6)

with O_J(x) errors. These factors are for the repeated-entry even coordinates,
not for an orthonormal basis. The h and k offdiagonal factors are essential.

## 3. A bounded trial direction annihilating the full atom exactly

Set d=e=0 and k=2sqrt2 h/sqrt(1-s)=2x h/a. Choose

h=eta_e/[eta_h+2sqrt2 eta_k/sqrt(1-s)].                     (7)

The denominator converges uniformly to -2sqrt2/(beta+l), so it is nonzero
for small enough x uniformly on J. This direction satisfies both
eta(z)=eta_e and w_s dot z=0 exactly. Its limit is

h0=-(beta+l)^2/(2sqrt2 beta l),
k0=2sqrt2 h0=-(beta+l)^2/(beta l),
z0=(0,0,h0,k0).                                           (8)

For this trial the non-full Fisher forms reduce exactly to
jE=-4ah, jU=2ah, jW=4ah, jV=-2ah, jZ=0.
Hence its Fisher coefficient of h^2 is

a^2(16/E+8/U+16/W+8/V) -> 8.

The logarithmic/cofactor quadratic part is

L_N(z)=-4nde+4nh^2-2md^2+2mk^2-8Lambda a h(d-k).           (9)

At the trial, its coefficient of h^2 is
4n+16m/(1-s)+16Lambda x -> 4(beta+l).
Thus the trial has energy

4(beta+l+2)h0^2+O_J(x)=phi(beta)+O_J(x),                    (10)

which proves the upper bound for (2). In particular the constrained minimum
sigma has a uniform finite upper bound on J; this does not presuppose
that sigma is positive.

## 4. Compactness and forcing estimates for the TRUE minimizer

Let z_x be the unique constrained minimizer in (3). On the constraint the
reviewed exact identity becomes

B(z,z)=F_full(z,z)+det(N)G_N(z,z)-det(N)eta_e^2.             (11)

The first two terms are nonnegative. Moreover det(N)G_N controls ||D||_F^2
from below uniformly on J, by the uniform positive eigenvalue bounds for N.
Combining (10) and (11) therefore gives, uniformly on J,

||z_x||=O_J(1),  F_full(z_x,z_x)=O_J(1).                   (12)

This supplies the coercivity/compactness missing from a purely formal
large-Fisher argument. It also proves existence and uniqueness directly:
on the constraint the positive matrix F_full+det(N)G_N has a strictly
convex coercive quadratic form, less only a constant.

The singleton forms satisfy jU=d+O_J(x)||z|| and
jW=e+O_J(x)||z||, with U,W comparable to x. Since their Fisher terms are
nonnegative and bounded by (12),

d_x=O_J(sqrt x), e_x=O_J(sqrt x).

Likewise the full-atom term gives

|w_s dot z_x|=O_J(sqrt(s/x)).                              (13)

Use the exact constraint eta(z_x)=eta_e together with (13). The two-by-two
linear system for h_x,k_x has a uniformly invertible coefficient matrix:
its limiting determinant is -2sqrt2/(beta+l), as in (7).
The coefficient errors are O_J(x) and d_x,e_x are O_J(sqrt x). It follows
that

z_x=z0+O_J(sqrt x).                                       (14)

No minimizing sequence can escape in a nearly null direction or use an
uncontrolled cancellation to evade these estimates.

## 5. Lower bound and the rigorous o(1) step

Retain only the two V-atom Fisher terms and the cofactor form (9); all other
Fisher terms are nonnegative. Since

jV/x=d+e-sqrt2 sqrt(1-s)h-x(w_s dot z),
V/x^2 -> 1/2,

equation (14) gives

2 jV(z_x)^2/V = 8h0^2+O_J(sqrt x).

The coefficients in (9) converge uniformly with O_J(x) error, and z_x is
bounded and satisfies (14). Therefore

L_N(z_x)=4(beta+l)h0^2+O_J(sqrt x).

The cancellation in the limiting cofactor part is explicit:
2beta k0^2+8(-beta/sqrt2)h0 k0=0 when k0=2sqrt2 h0.
Thus

sigma >= 4(beta+l+2)h0^2-O_J(sqrt x)=phi(beta)-O_J(sqrt x).

Together with (10) this proves (2). This is the precise uniform remainder
argument; no profile limit or termwise inversion of a singular matrix is
being used as a proof.

## 6. Global positivity of the limiting function, endpoints, and minimum

Every factor in (1) is positive for beta>0. More quantitatively,
(beta+l)^2>=4beta l implies

phi(beta)>=8(beta+l+2)>8(l+2)>0.                           (15)

Both ends diverge:

phi(beta) ~ l^2(l+2)/(2beta^2) as beta decreases to zero,
phi(beta) ~ beta^3/(2l^2) as beta tends to infinity.

There is no unresolved middle-beta inequality. The logarithmic derivative
has the sign of

3beta^2+(l+4)beta-2l(l+2).

This polynomial is strictly increasing on beta>0 and has one positive root,
so the unique global minimizer is

beta_star=[sqrt((l+4)^2+24l(l+2))-(l+4)]/6.                 (16)

The square-root expression and substitution in (1) give the exact minimum;
the accompanying decimal values are merely evaluations of this formula.

## 7. What this proves for strict finite kernels, and what remains open

For every compact J contained in (0,infinity), (2) and (15) give an x_J>0
such that sigma>0 for ALL 0<x<x_J and beta in J, with
s=exp(-beta/x). These form a genuine continuous exponential wedge, not a
finite collection of rays. The reviewed transverse/odd-block reductions
then give B_K>0 on the entire Sym(3), including noncommuting and indefinite
directions. All these kernels are strict: their eigenvalues are
x, x(1+sqrt(1-s)), x s/(1+sqrt(1-s)), between zero and one for x<1/2.

This does not settle arbitrary two-scale approaches beta=beta(x) tending
to zero or infinity. The constants in (2) and x_J can deteriorate with the
endpoints of J. Although the closed phi diverges at those ends, that fact
alone does not justify interchanging limits or extending the uniform
remainder to noncompact beta ranges. The full path domain remains unresolved.

Most fragile audit steps: the constrained normalization eta(z)=eta_e;
uniform coercivity in (11); the singleton forcing estimate; the two-by-two
constraint determinant; the factor 8 from the V atoms; and the exact
cofactor cancellation in section 5. The proof of limiting positivity is
elementary once (1)/(2) are established.
