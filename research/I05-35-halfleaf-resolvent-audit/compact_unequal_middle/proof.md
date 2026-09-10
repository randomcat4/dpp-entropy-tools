# Exact compact unequal-strength middle for the integrated half-leaf core

Status: **AUTHOR PROOF AND EXACT CONTINUUM CERTIFICATE / PENDING INDEPENDENT REVIEW**. The result below is not part of the frozen PR120/PR124 equal-strength or small-edge units and is not covered by PR132. It retains the true kernel-affine path, every complete selected/vacant event in the final Shannon statement, all Fisher terms, every acceleration, the leaf marginal, and all six real-symmetric directions.

## 1. Exact integrated occupied-side form

Consider a strict half-leaf kernel

```text
K=[[1/2,0,b0],[0,1/2,c0],[b0,c0,z]],
b0^2=A/4, c0^2=B/4,
z=q+(A+B)/2,
A,B,q,qbar=1-A-B-q>0.
```

Diagonal sign conjugation covers either sign of `b0,c0`. For the occupied side, scale the third coordinate by `q^(-1/2)` and put

```text
a=A/q, b=B/q.
```

The four normalized conditional selected masses are

```text
t00=1+a+b, t10=1+b, t01=1+a, t11=1.
```

The scale identity for the complete selected perspectives is

```text
G1_normalized''=G1''/q.                              (1)
```

The additional logarithmic normalization term is affine in `K33`, so it has zero second derivative. Thus positivity and strictness may be proved at the normalized object.

Use leaf-diagonal coordinates `delta=(d,e)` and conditional-score coordinates `U=(m,alpha,beta,gamma)`. The invertible physical map is

```text
D11=d, D22=e, D33=m-a d-b e,
D13=-alpha/(4 sqrt(a)),
D23=-beta /(4 sqrt(b)),
D12= gamma/(8 sqrt(a b)).                            (2)
```

Define

```text
nu=log(1+a), v=log(1+b), w=log(1+a+b),
H=nu+v-w=log((1+a)(1+b)/(1+a+b)),
ell=nu-H/2, k=v-H/2,
lambda=-H,
J=(1+a+b)w-(1+a)nu-(1+b)v,
n=(1+(a+b)/2)H.                                      (3)
```

Direct collection of the four complete selected-event jets gives

```text
G1''=U^T Y U+2 delta^T C U+delta^T L delta,          (4)
```

where

```text
L=[[2a ell,J],[J,2b k]],
C=[[-ell,0,-H/4,0],[-k,-H/4,0,0]],                  (5)
```

and, with

```text
E4=[[1,-1/2,-1/2,1/4],
    [1, 1/2,-1/2,-1/4],
    [1,-1/2, 1/2,-1/4],
    [1, 1/2, 1/2,1/4]],
```

```text
F=(1/4) E4^T diag(1/t00,1/t10,1/t01,1) E4,
R=[[0,0,0,0],
   [0,ell/(8a),0,H/(32a)],
   [0,0,k/(8b),H/(32b)],
   [0,H/(32a),H/(32b),n/(32ab)]],
Y=F+R.                                                (6)
```

The reciprocal terms in `F` are the complete selected-event Fisher information. The entire matrix `R`, including its mixed entries, is the retained acceleration contribution. No resolvent integrand appears in (4)-(6).

Put

```text
M(a,b)=[[Y,C^T],[C,L]].                              (7)
```

Then `M(a,b)>0` is exactly positivity of `G1''` in all six physical directions. Equivalently, using the known positive pivot `Y`, the remaining target is

```text
E(a,b)=L-C Y^(-1) C^T>0.                             (8)
```

## 2. Integral variables and why no pointwise kernel is asserted

Two load-bearing logarithmic combinations already have positive integral forms:

```text
H=int_0^a int_0^b (1+x+y)^(-2) dy dx,
J=int_0^a int_0^b (1+x+y)^(-1) dy dx.               (9)
```

They imply the exact monotonicities used below. However `det E` is nonlinear in `H,J,nu,v` and contains products of these integrals. Replacing each integral by one common pointwise rational kernel is therefore not an identity. The previously accepted exact counterexample to pointwise resolvent positivity is respected: this proof makes no pointwise-in-an-auxiliary-variable sign claim.

A direct positive multi-integral factorization of `det E` was not obtained. The compact middle is instead closed by an exact interval proof of the integrated matrix (7).

## 3. Rational compactification and exact box enclosures

Set

```text
r=a/(1+a), s=b/(1+b).                                (10)
```

The target square

```text
1/4<=a,b<=4                                          (11)
```

is exactly

```text
1/5<=r,s<=4/5.                                       (12)
```

Partition both axes at

```text
r_i=s_i=1/5+3i/160,  i=0,...,32.                    (13)
```

This yields 1024 closed rational boxes whose union is (12).

For one box `a0<=a<=a1`, `b0<=b<=b1`, the checker first uses exact monotonicity, before interval evaluation:

```text
H increases in a and b;
ell increases in a and decreases in b;
k decreases in a and increases in b;
J increases in a and b.                              (14)
```

The first three statements follow directly from (3). The last follows from (9). The four Fisher reciprocal weights are also monotone rational functions. These facts give endpoint-sharp scalar intervals for `H,ell,k,J` and the reciprocal weights. All products, quotients, and matrix operations thereafter are enclosed by outward interval arithmetic.

## 4. Exact logarithm and fixed-point error certificate

For every positive rational endpoint `x`, write

```text
x=2^p y, 1<=y<2, z=(y-1)/(y+1), 0<=z<=1/3.
```

The checker uses the exact inequality

```text
2 sum_(j=0)^(N-1) z^(2j+1)/(2j+1)
 <= log y
 <=2 sum_(j=0)^(N-1) z^(2j+1)/(2j+1)
   +2 z^(2N+1)/[(2N+1)(1-z^2)],                     (15)
```

with `N=56`, together with the same enclosure for `log 2`. The remainder is the positive omitted series bounded by a geometric tail.

Every interval endpoint is then rounded outward to an integer multiple of

```text
2^(-140).                                            (16)
```

Addition, multiplication, reciprocal, and division round outward after each operation using exact unbounded Python integers. Thus the computed interval matrix contains `M(a,b)` at every real point of the box; no floating logarithm enters this enclosure.

## 5. Per-box positive-definiteness certificate

At each box midpoint a floating Cholesky factor is used only to propose an upper-triangular dyadic matrix `P`, rounded to denominator `2^44`. The checker verifies exactly that every diagonal entry of `P` is positive and every entry below the diagonal is zero, so `P` is nonsingular. The correctness of the certificate does not depend on the accuracy of the floating proposal.

Let `mathcal M` be the exact interval enclosure of (7) on a box and compute, with the same outward arithmetic,

```text
mathcal B=P^T mathcal M P.                            (17)
```

For every row the checker proves

```text
lower(B_ii)-sum_(j!=i) max(abs(lower(B_ij)),abs(upper(B_ij)))>0.  (18)
```

Every concrete symmetric `B=P^T M(a,b)P` is therefore strictly diagonally dominant with positive diagonal. Gershgorin's theorem gives `B>0`; nonsingularity of `P` gives `M(a,b)>0` throughout that entire box.

All 1024 boxes pass. The smallest exact lower margin in (18) is

```text
164880134291545266513358110774173383066734
/1393796574908163946345982392040522594123776
>0,                                                   (19)
```

on the last box in each coordinate,

```text
25/7<=a<=4, 25/7<=b<=4.                              (20)
```

The decimal `0.118295...` printed by the checker is only a display of the exact positive fraction (19).

### Theorem 5.1: occupied compact unequal-strength middle

For every `a,b` satisfying (11), the integrated complete-event occupied-side form `G1''` is positive definite in all six real-symmetric physical directions.

Proof. Equations (13) cover the whole square. Sections 3-5 prove `M(a,b)>0` on every box. Apply (4), (7), and the invertible map (2). Equation (1) returns to the original unnormalized physical half-leaf. QED.

This is a continuum certificate. Checking one rational interval matrix per box is not sampling the sign at finitely many parameter points.

## 6. Complete Shannon compact-middle theorem

At a half-leaf center the exact complete-law decomposition is

```text
-H''=4(d^2+e^2)+G1''+G0''.                           (21)
```

Full complementation turns `G0''` into the occupied-side form for the complemented kernel and direction `-D`, with normalized strengths `A/qbar` and `B/qbar`.

### Corollary 6.1: two-sided compact middle

Let `A,B,q,qbar>0`, `A+B+q+qbar=1`. If

```text
1/4 <= A/q, B/q, A/qbar, B/qbar <= 4,                (22)
```

then both `G1''` and `G0''` are positive definite and

```text
-H''(K;D)>0                                           (23)
```

for every nonzero real-symmetric physical direction `D` at the corresponding strict half-leaf kernel.

Proof. Apply Theorem 5.1 first with rare selected corner `q`, then to the fully complemented kernel with rare selected corner `qbar`. Insert both strict signs into (21). QED.

The domain (22) is a closed compact subset of the strict physical simplex and contains genuinely unequal strengths. It is disjoint from the logical dependence of the equal-strength proof and does not use a small-edge limiting argument.

## 7. Execution and scope

The retained final run used Python 3.13.5 on Linux x86_64, one process and no GPU. It completed all 1024 boxes in about 3.26 seconds of script wall time; an external wrapper recorded about 4.26 total user-plus-system CPU seconds and peak RSS below 95 MiB. Development checks used only new local test boxes. No PR120/PR124 checker, old issue budget, parameter scan conclusion, or previous arithmetic output was rerun or imported.

The script and output are author evidence pending independent review. The theorem does not cover `a` or `b` outside `[1/4,4]`, arbitrary unequal leaf diagonals, all half-leaf strengths, general missing-edge kernels, general real three-point kernels, or any Toeplitz entropy-rate statement. Novelty and formal verification are not assessed.
