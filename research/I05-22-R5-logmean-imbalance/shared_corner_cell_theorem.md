# I05-22 R5 continuation: shared-corner cell completion closes one full nonzero-Lambda shape

Status: **PROVED (author proof; PENDING_REVIEW)** for the one-edge lemma, the shared-corner sufficient theorem, and the fixed-shape corollary below. The proof establishes the actual complete-event full Shannon Hessian sign for one entire legal nonzero-Lambda family; it is not a relaxed-variable or finite-sample statement. General half-leaf arrows, general missing-edge arrows, and general real three-point concavity remain open. Novelty is not assessed.

This unit continues PR81 at source head `92c1b3dfd85c4be4f0ce13b59ffb51e6e0869eac`. The record read before starting contained a scoped C1 FIRST acceptance only for the earlier four-scalar compression/global imbalance unit frozen at `449465e2b424c7f284bf4e8317d95966f6743371`; it contained a successor binding for `92c1b3df...` but no completed delta verdict on `coupled_gram_fixed_shape.md`. Accordingly, all later Gram/placement claims were independently reconstructed here rather than treated as reviewed facts. The accompanying checker is same-author algebra, not independent adjudication.

No PR60 Lambda-zero coefficient certificate is rerun. Issue73's three filaments, 273 points, and shared 2700-second budget are not started or duplicated.

## 1. Complete-event object and the half-leaf coordinates

For a real symmetric three-point kernel with entries `(x,y,z,a,b,c)`, write

```text
Q12=xy-a^2, Q13=xz-b^2, Q23=yz-c^2, R=det K.
```

In mask order `0,1,2,12,3,13,23,123`, the complete atoms are

```text
(1-x-y-z+Q12+Q13+Q23-R,
 x-Q12-Q13+R, y-Q12-Q23+R, Q12-R,
 z-Q13-Q23+R, Q13-R, Q23-R, R).
```

For every true physical line `K+tD`, the complete negative entropy Hessian is

```text
Q_K(D)=-H''(K;D)=sum_S p_S'^2/p_S + sum_S p_S'' log p_S.
```

All eight atoms, the complete Fisher term, every acceleration, and all six real symmetric directions remain in this unit.

Consider the strict connected half-leaf arrow

```text
K=[[1/2,0,b],[0,1/2,c],[b,c,z]],
b^2=A/4, c^2=B/4,
z=q+(A+B)/2,
A,B,q,qbar>0, qbar=1-A-B-q.
```

Signs of `b,c` are restored by diagonal sign conjugation. Put

```text
t_ij=q+A(1-i)+B(1-j),
P_ij=1/4,
f(t)=1/[t(1-t)],
g(t)=log(t/(1-t)),
psi(t)=t log t+(1-t)log(1-t).
```

For a physical direction let `d=D11`, `e=D22` and use the four conditional-score coefficients `U=(m,alpha,beta,gamma)`. At `x=y=1/2` the exact invertible map is

```text
D33=m-Ad-Be,
D13=-b alpha/(2A),
D23=-c beta/(2B),
D12=bc gamma/(2AB).
```

Let `T=(T00,T10,T01,T11)^T=E U`, where

```text
E=[[1,-1/2,-1/2, 1/4],
   [1, 1/2,-1/2,-1/4],
   [1,-1/2, 1/2,-1/4],
   [1, 1/2, 1/2, 1/4]].
```

The determinant of `E` is nonzero, so `(d,e,T)` retains every physical direction.

## 2. The same four corners, not four independent scalar ranges

Define the four actual opposite-edge integrals

```text
a_minus = g(q+A)-g(q),
a_plus  = g(q+A+B)-g(q+B),
b_minus = g(q+B)-g(q),
b_plus  = g(q+A+B)-g(q+A),
```

and the rectangle integral

```text
J=psi(q+A+B)+psi(q)-psi(q+A)-psi(q+B)
 =int_0^A int_0^B f(q+s+t) dt ds >0.
```

They are the PR81 paired quantities through

```text
a_minus=ell-lambda/2, a_plus=ell+lambda/2,
b_minus=k-lambda/2,   b_plus=k+lambda/2.
```

Thus both axes use the same four corner logits. The common cell difference is

```text
lambda=a_plus-a_minus=b_plus-b_minus.
```

At half leaves, the paired acceleration scalar is exactly

```text
n=A k+B ell-J.
```

No `ell,k,lambda,J` variable is relaxed independently below.

## 3. A sharp-enough one-edge Gram lemma

Fix `0<u<u+s<1` and put

```text
h=g(u+s)-g(u)=int_u^(u+s) f(t) dt,
m_edge=h/s.
```

### Lemma 3.1

For every real `X,Y,delta`,

```text
s h delta^2-h delta(X+Y)/2+h(X-Y)^2/(16s)
 +(f(u+s)X^2+f(u)Y^2)/8

>= s h [delta-(X+Y)/(4s)]^2 + 3(X-Y)^2/8.       (1)
```

The inequality is strict in the residual two-endpoint matrix away from the zero vector.

### Proof

Set

```text
r(t)=f(t)-3=(1-3t(1-t))/[t(1-t)]>0,
w(t)=r(t)^(-1/2)=sqrt(t(1-t)/[1-3t(1-t)]).
```

Writing `v=t(1-t)`, direct differentiation gives

```text
w''(t)=-(1-6v)^2/[4 v^(3/2)(1-3v)^(5/2)] <=0.       (2)
```

It is not affine on a nontrivial interval, hence is strictly concave. The chord inequality for `w`, followed by the decreasing map `x -> x^(-2)`, gives

```text
(1/s) int_u^(u+s) r(t) dt
 < sqrt(r(u)r(u+s)).                                 (3)
```

Indeed the normalized integral of the reciprocal square of the affine chord is exactly `1/[w(u)w(u+s)]`.

After completing the first square in (1), eight times the residual minus `3(X-Y)^2/8` is the quadratic with matrix

```text
[[f(u+s)-3, 3-m_edge],
 [3-m_edge, f(u)-3]].                                (4)
```

Its diagonal entries are positive, while (3) says

```text
(m_edge-3)^2 < [f(u)-3][f(u+s)-3].
```

Thus (4) is positive definite, proving the lemma. This is an actual endpoint/integral Gram inequality for the binary-logit rectangle, not a free endpoint relaxation.

## 4. Exact four-corner cell decomposition

Put

```text
Delta=T00-T10-T01+T11.
```

For an edge of length `s`, integral `h`, endpoint scores `X,Y`, leaf direction `delta`, and endpoint Fisher weights `p,r`, define

```text
E_s(h;X,Y,delta;p,r)
 =s h delta^2-h delta(X+Y)/2+h(X-Y)^2/(16s)
  +(p X^2+r Y^2)/8.                                  (5)
```

A direct transformation of the complete paired matrices gives the exact identity

```text
Q_K(D)
 =4d^2+4e^2+2Jde-J Delta^2/(32AB)

  +E_A(a_plus ;T00,T10,d;f(t00),f(t10))
  +E_A(a_minus;T01,T11,d;f(t01),f(t11))
  +E_B(b_plus ;T00,T01,e;f(t00),f(t01))
  +E_B(b_minus;T10,T11,e;f(t10),f(t11)).             (6)
```

For transparency, the non-Fisher acceleration block in corner coordinates is

```text
 a_plus (T00-T10)^2/(16A)
+a_minus(T01-T11)^2/(16A)
+b_plus (T00-T01)^2/(16B)
+b_minus(T10-T11)^2/(16B)
-J Delta^2/(32AB).                                   (7)
```

The final negative cell term in (7) is exactly what is lost if the two axes or the four paired scalars are bounded independently. Formula (6) retains it.

Apply Lemma 3.1 to all four edges. The elementary identities

```text
(T00-T10)^2+(T01-T11)^2 >= Delta^2/2,
(T00-T01)^2+(T10-T11)^2 >= Delta^2/2
```

give the load-bearing shared-corner estimate

```text
Q_K(D)
 >= sum_edges s h [delta-(X+Y)/(4s)]^2
    +4d^2+4e^2+2Jde
    +[3/8-J/(32AB)] Delta^2.                         (8)
```

Unlike the earlier two separate Gram ellipses, (8) couples all four edges and `J` through the same alternating cell mode.

## 5. A genuine sufficient family

### Theorem 5.1

For every strict connected half-leaf arrow above, if its actual rectangle integral satisfies

```text
J < 12 A B,                                           (9)
```

then

```text
-H''(K;D)>0
```

for every nonzero real symmetric physical direction `D`. Equivalently the full six-direction Shannon Hessian is strictly negative definite. In the inherited positive-pivot representation this implies

```text
E_H>0 and det E_H>0.                                  (10)
```

### Proof

Condition (9) makes the last coefficient in (8) strictly positive. Since `A+B<1`, AM-GM gives `AB<1/4`, hence `J<12AB<3<4`. Therefore

```text
4d^2+4e^2+2Jde >= (4-J)(d^2+e^2)>0
```

unless `d=e=0`.

If equality held in the full lower bound, then `d=e=0`, `Delta=0`, and the four completed edge squares would force

```text
T00+T10=T01+T11=T00+T01=T10+T11=0.
```

These equations leave only an alternating vector `(t,-t,-t,t)`, but its `Delta` is `4t`; hence `t=0`. Thus `T=0`, then `U=0`, and the invertible physical map gives `D=0`. This proves strictness.

The condition is deliberately weaker than a universal half-leaf theorem. It is, however, an actual DPP condition on one rectangle and cannot be satisfied by choosing relaxed `ell,k,lambda,J` values independently.

A q-uniform shape corollary follows from the independently rederived symmetry and strict convexity of `J(q)`: if

```text
h(A)+h(B)-h(A+B) < 12AB,                              (11)
```

where `h=-psi` is binary entropy, then (9) holds for every `0<q<1-A-B`.

## 6. The requested fixed shape is completely closed

Take

```text
A=1/4, B=4/9, A+B=25/36, 12AB=4/3,
K(q)=[[1/2,0,1/4],
      [0,1/2,1/3],
      [1/4,1/3,q+25/72]],
0<q<11/36.                                            (12)
```

The rectangle function is symmetric under `q <-> 11/36-q` and strictly convex because

```text
J''(q)=int_0^A int_0^B f''(q+s+t) dt ds>0.
```

After continuous extension to the two endpoints, strict convexity gives

```text
J(q)<J(0)=h(1/4)+h(4/9)-h(25/36)
          <h(1/4)+h(4/9).                             (13)
```

The following elementary rational bounds suffice:

```text
log 2 < 7/10,
log(4/3)<1/3,
h(1/4)=log(2)/2+3log(4/3)/4 < 3/5,
h(4/9)<log 2<7/10.
```

For the first logarithm,

```text
exp(7/10)>1+7/10+(7/10)^2/2+(7/10)^3/6
         =12013/6000>2.
```

Therefore

```text
J(q)<13/10<4/3=12AB                              (14)
```

throughout the complete legal q interval. Theorem 5.1 proves (10) for every point of (12), including every nonzero-Lambda point. This is a continuum analytic result, not a filament non-hit or an interval computation.

There is also an explicit uniform coordinate coercivity. Since `f>=4`, every edge has `h>=4s`; from (8) and (14),

```text
Q_K(D) > Qstar,

Qstar=27(d^2+e^2)/10+3 Delta^2/320
 +[(d-T00-T10)^2+(d-T01-T11)^2]/4
 +(64/81)[(e-9(T00+T01)/16)^2
          +(e-9(T10+T11)/16)^2].                    (15)
```

In coordinate order `(d,e,T00,T10,T01,T11)`, the six leading principal minors of the Gram matrix of `Qstar` are

```text
16/5,
27736/2025,
1969009/324000,
11805091/5184000,
261937/345600,
6059/64000.
```

All are positive, so (15) is uniformly positive definite. This supplies a quantitative strictness check independent of any numerical value of `det E_H`.

## 7. Independent reconstruction and method comparison

The exact checker `verify_shared_corner_cell.py` performs the following without importing the prior author checker:

1. reconstructs the half-leaf corner transform from the paired `L,C,F,R` formulas;
2. verifies (6)-(7) as a generic symbolic identity with all six coordinates;
3. verifies the differential identity (2) and the algebraic completion behind (1);
4. independently rebuilds the previous fixed rational relaxed tuple, all four printed Sylvester minors, its exact negative relaxed determinant, and the three printed q-derivative fractions;
5. independently compares (6) with the original eight-event formula at fixed rational physical directions;
6. verifies the exact rational gates and the Sylvester minors in (15).

The checker passed under Python 3 / SymPy 1.14.0. It is supporting same-author evidence only.

Two structurally different routes have now been tested:

- Independent scalar/axis bounds, including the earlier two Gram ellipses and separate secant placement, admit nonrealizable negative relaxed determinants and cannot prove the DPP theorem.
- The shared-corner route keeps the four endpoint Fisher weights, four edge integrals, and the negative alternating cell term in one quadratic. Its `3/8` edge margin yields the actual sufficient condition (9) and closes the full fixed family (12).

No paired-resolvent universal convexity claim is used or revived. No actual entropy counterexample is produced. No finite search establishes the theorem. General half-leaf arrows failing (9), unequal leaf diagonals, general nonzero-Lambda missing-edge arrows, and general real three-point concavity remain **INCOMPLETE**.

Final classification: **PROVED (author; PENDING_REVIEW)** for Lemma 3.1, Theorem 5.1, the q-uniform shape condition (11), and the complete fixed-shape theorem (12)-(15). Novelty and publication priority are **NOT_ASSESSED**.