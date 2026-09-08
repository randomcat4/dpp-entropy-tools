# Moving physical frame, frozen A2 v2

STATUS: PROVED (author proof; independent review pending).

This proves claims (1)--(3) of `repo/research/A2/frozen_theorem_v2.md`.
It does not prove a positive entropy gap or global entropy concavity.
No numerical computation, parameter search, or external theorem is used.

## 1. Explicit geometry and feasibility

Write q=1-t, d=1-2t, a=tq, and

    c=(1-t^2)/(1+t^2), s=2t/(1+t^2), z=cs,
    U=2^(-1/2) [[1,0],[c,-s],[s,c],[0,1]].

Then U^T U=I_2. Let X=[[0,x],[x,0]], where x is the fixed frozen
parameter in (0,1). On range(U), the two endpoint kernels have eigenvalues
q+tx and q-tx; on its orthogonal complement both eigenvalues are t.
For 0<t<1/2 these four numbers lie strictly between zero and one:
q+tx=1-t(1-x)<1 and q-tx> (1-x)/2>0.
The midpoint has eigenvalues q,q,t,t, and the opposite direction terms
cancel exactly. Thus all three kernels are strict positive contractions
and the claimed midpoint is the actual arithmetic midpoint.

The physical projection is

    P(t)=1/2 [[1,c,s,0],[c,1,0,-s],[s,0,1,c],[0,-s,c,1]].

Its ordered two-row minors psi_ij=det U_{ij}, in order
12,13,14,23,24,34, are

    (-s,c,1,1,c,s)/2.

In particular the two previously absent projection events 12 and 34
open with squared mass s^2/4. This is movement of the physical projection,
not a change of basis inside a fixed high or low space.

## 2. No direct old fixed-data representation

Define the fixed real symmetric matrices

    A=[[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]],
    B=[[0,0,1,0],[0,0,0,-1],[1,0,0,0],[0,-1,0,0]].

They satisfy A^2=B^2=I and AB=-BA, and

    M(t)=I/2+(d/2)(cA+sB).

For distinct t,u in (0,1/2), direct multiplication gives

    [M(t),M(u)]
      = (1-2t)(1-2u)(u-t)(1+tu)
        /((1+t^2)(1+u^2)) AB != 0.

The R2 fixed-data mixed two-term family's midpoint has the form
P+lambda L with fixed L commuting with P. Its midpoint matrices commute
pairwise, since [P+lambda L,P+mu L]=0. The unequal scalar-slack family's
midpoints have the form alpha(lambda)P+beta(lambda)(I-P), so also commute
pairwise. A fixed physical orthogonal representation preserves all these
commutators, and any common scalar reparameterization retains pairwise
commutativity. Every interval (0,t0) within the domain contains distinct
t,u with the nonzero commutator above. Hence no direct representation of
the entire endpoint/midpoint path by either old family is possible there.
No entropy-invariance assertion under general orthogonal conjugation is used.

## 3. A determinant identity for every exact event

The following formulas hold more generally for any real c,s with c^2+s^2=1,
with the same U, t and x. They will then be specialized to the frozen
rational c,s. Define

    b=a(1-2a)/2,
    mu_1=b+t^2*x^2*q*d/2,
    mu_3=b-t^3*x^2*d/2,
    w_12=w_34=s^2/4,
    w_13=w_24=c^2/4,
    w_14=w_23=1/4,
    F(w)=a^2+(d^2-t^2*x^2)w+t^2*x^2*a.

Here b is just a scalar probability abbreviation, not a direction matrix.
All 16 endpoint event probabilities are:

| Event S | p_sigma(S) |
|---|---|
| empty | a^2(1-x^2) |
| 1 | mu_1 |
| 2 | mu_1-sigma*t*x*z*q^2 |
| 3 | mu_1+sigma*t*x*z*q^2 |
| 4 | mu_1 |
| 12 | F(s^2/4)-sigma*t^2*q*x*z |
| 34 | F(s^2/4)+sigma*t^2*q*x*z |
| 13 | F(c^2/4)+sigma*t^2*q*x*z |
| 24 | F(c^2/4)-sigma*t^2*q*x*z |
| 14 | F(1/4) |
| 23 | F(1/4) |
| 234 (omit 1) | mu_3 |
| 134 (omit 2) | mu_3+sigma*t^3*x*z |
| 124 (omit 3) | mu_3-sigma*t^3*x*z |
| 123 (omit 4) | mu_3 |
| 1234 | a^2-t^4*x^2 |

Every midpoint probability is obtained from this table by setting x=0.
In particular the midpoint has mass a^2 at empty/full, b at every singleton
and triple, and a^2+d^2*w_ij at pair ij.

Here is a derivation directly tied to the full event law. Put
C_sigma=d I+sigma t X and R_sigma=U C_sigma U^T, so K_sigma=tI+R_sigma.
For formal variables y_i and Z=diag(y_i), the probability generating
polynomial of the inclusion-exclusion law is

    det(I-K+ZK)
      = sum_J det((R_sigma)_J)
          product_(j in J)(y_j-1)
          product_(i not in J)(q+t y_i).

One can verify the first equality by summing the given inclusion-exclusion
definition against product_(i in S)y_i, obtaining
sum_T det(K_T) product_(i in T)(y_i-1); determinant multilinearity yields
det(I+(Z-I)K). The displayed expansion around the diagonal qI+tZ is
another application of multilinearity. Because rank(R_sigma)<=2, only
|J|<=2 occur. Its relevant minors are

    det((R_sigma)_empty)=1,
    (R_sigma)_ii=d/2+sigma*t*x*h_i,
    (h_1,h_2,h_3,h_4)=(0,-z,z,0),
    det((R_sigma)_{ij})=(d^2-t^2*x^2)w_ij.

For a fixed event S of size k, the coefficient contributed by subset J is

    W_J(S)=(-1)^(|J\S|)
            t^(k-|J intersect S|)
            q^(4-k-|J\S|).

This finite coefficient rule proves the table without treating inclusion
minors as exact events. For clarity, its second-rank coefficient
T_S=sum_(i<j) w_ij W_{ij}(S) equals

    q^2                 for S=empty,
    -qd/2               for |S|=1,
    w_ij-a              for S=ij,
    td/2                for |S|=3,
    t^2                 for S=1234.

These identities use sum_(j!=i)w_ij=1/2,
sum_(i<j)w_ij=1, and w_ij=w_(E\{i,j}). The linear h_i coefficients give
the sign-dependent terms in the table. Endpoint masses are strictly
positive because all eigenvalues are in (0,1): equivalently,
p_K(S)=det(I-K) det((K(I-K)^(-1))_S)>0, an identity also obtained from the
same generating polynomial. No singular inverse is used at t=0.

## 4. First orders of all events and uniform entropy expansion

Fix an arbitrary compact interval J=[ell,h] inside (0,1). All big-O
constants below may depend on J, but are independent of x in J and of
sigma. Put L=log(1/t). For the rational rotation,

    z=2t+O(t^3), s^2/4=t^2+O(t^4), c^2/4=1/4+O(t^2).

The first nonzero probability orders from the exact table are:

| Events | midpoint | each endpoint |
|---|---|---|
| empty | t^2+O(t^3) | (1-x^2)t^2+O_J(t^3) |
| full | t^2+O(t^3) | t^2+O_J(t^3) |
| four singletons | t/2+O(t^2) | t/2+O_J(t^2) |
| four triples | t/2+O(t^2) | t/2+O_J(t^2) |
| 12,34 | 2t^2+O(t^3) | 2t^2+O_J(t^3) |
| 13,24,14,23 | 1/4+O(t) | 1/4+O_J(t) |

Consequently each table entry, and each segment between probabilities used
below, has a positive lower bound c_J*t^v for its displayed valuation v.
These bounds hold for all 0<t<t_J and x in J. This covers every vanishing
event, including the two opened Pluecker-zero events. There are no omitted
events, and no limiting logarithm is evaluated at zero.

Let f(p)=-p log p; f'(p)=-log p-1 and f''(p)=-1/p.
Write each endpoint mass as p_sigma=p_0+delta+sigma*eta. Taylor estimates
on the positive segments just described show that replacing the endpoint
average by f(p_0)+f'(p_0)delta has error
O_J((delta^2+eta^2)/p_0), whenever |delta|+|eta|=o(p_0).
The empty event, whose relative displacement need not be small, is handled
exactly instead. The six groups contribute as follows.

### Empty event

With kappa=x^2, the exact difference is

    f((1-kappa)a^2)-f(a^2)
      = kappa*a^2 log(a^2)
        -(1-kappa)a^2 log(1-kappa)
      = -2kappa*t^2*L
        -(1-kappa)t^2 log(1-kappa)+O_J(t^3 L).

The compact restriction h<1 makes log(1-kappa) uniformly bounded.

### Four singletons

Their common midpoint mass is b=t/2+O(t^2), their common mean displacement
is delta=t^2*kappa*q*d/2=kappa*t^2/2+O_J(t^3), and eta=O_J(t^2).
Thus the Taylor error summed over four events is O_J(t^3), while
f'(b)=L+log 2-1+O(t). The total is

    2kappa*t^2*(L+log 2-1)+O_J(t^3 L).

### Four active pairs 13,24,14,23

For each, p_0=1/4+O(t),
delta=-t^2*kappa*(w-a)=-kappa*t^2/4+O_J(t^3), and
eta=O_J(t^3). Their total contribution is

    -kappa*t^2*(log 4-1)+O_J(t^3).

### Opened pairs 12,34

Here p_0=2t^2+O(t^3), delta=O_J(t^3), eta=O_J(t^3).
The first derivative term is O_J(t^3 L) and Taylor error is O_J(t^4).
Thus these two events contribute O_J(t^3 L), despite their vanishing
limiting projection masses.

### Four triples and the full event

For triples p_0=t/2+O(t^2), delta=O_J(t^3), eta=O_J(t^4), so their
total contribution is O_J(t^3 L). For the full event p_0=a^2,
delta=-t^4*kappa and eta=0, giving O_J(t^4 L).

Summing all 16 events cancels the t^2 L terms exactly and yields

    Delta(t,x)=-G(x^2)t^2+O_J(t^3 log(1/t)),
    G(v)=v+(1-v)log(1-v),  0<=v<1.

Since G(0)=0 and G'(v)=-log(1-v)>0 for 0<v<1, G(x^2)>0 for every
fixed x in (0,1). This is the first nonzero term and is strictly negative.
On each J, min_(x in J)G(x^2)=G(ell^2)>0. The proved uniform remainder
therefore also gives a common t_J'>0 such that Delta(t,x)<0 for every
0<t<t_J' and x in J.

## 5. Scope and unresolved questions

The moving-frame family is outside the direct R2 representations proved
above, but its leading gap agrees with an old paired high-space coefficient.
Thus this is a new explicit path exclusion, not a new positive mechanism.
This proof does not cover x=x(t) tending to zero or one, any faster physical
rotation, all finite t, arbitrary moving frames, or the unrestricted finite
real-kernel question. There is no claim of audited novelty or Lean checking.

