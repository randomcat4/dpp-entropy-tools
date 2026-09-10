# Independent reconstruction, a small-edge theorem, and the residual-only obstruction

Status: **NEW AUTHOR-SESSION RECONSTRUCTION / PENDING EXTERNAL REVIEW**. This file was derived after the first PR124 checkpoint. It does not turn the same GitHub account into an independent reviewer, and it does not inherit acceptance from PR81, PR104, or PR70. The two short checkers named below are new and do not execute or import the existing PR124 checker.

The conclusions are split deliberately:

1. the exact pointwise-resolvent counterexample in `proof.md` is independently reconstructed from all eight Möbius events;
2. the equal-strength theorem in `equal_strength_halfleaf_theorem.md` survives a separate algebraic audit;
3. a new punctured single-edge-face theorem is proved for arbitrary fixed strength on the other edge; and
4. a tempting residual-only proof of the unequal-strength case is disproved as a method, not as an entropy statement.

Throughout, the path is the true affine path `K+tD`, all six real-symmetric physical coordinates are retained, and no occupied event, vacant event, Fisher term, acceleration, or leaf marginal is omitted.

## 1. Independent eight-event reconstruction of the resolvent obstruction

Take

```text
A=1/4, B=16/25, q=109/1000, qbar=1/1000,
r=1/50000,
D=(d11,d22,d33,d12,d13,d23)=(-18,-72,40,146,108,5).
```

The new standard-library checker `code/verify_independent_event_fraction.py` starts only from the inclusion minors of `K+tD`. It applies Möbius inversion to obtain all eight complete-event polynomials

```text
p_X(t)=sum_(Y superset X) (-1)^(|Y|-|X|) det((K+tD)_Y),
```

checks positivity at the center and the polynomial normalization, groups the four leaf marginals `P_ij=p_ij0+p_ij1`, and differentiates

```text
Phi_r(t)=sum_ij P_ij(t)^2/[p_ij1(t)+r P_ij(t)]
```

directly as a quotient of exact rational polynomials. It does not use conditional Schur jets. The result is

```text
Phi_r''(0)=
-47488558049748267993080620088778228551027375300000000000
/2044542058422113103788725284171055940635901533282467 < 0.
```

This exactly agrees with the separate Schur-derivative route in `proof.md`. Therefore the universal pointwise claim `Phi_r''>=0` is genuinely false. The conclusion remains only a certificate-method obstruction: the integrated `G1''` and the full Shannon curvature are positive at this witness.

## 2. Audit of the equal-strength theorem

The following load-bearing steps of `equal_strength_halfleaf_theorem.md` were rederived rather than assumed.

First, scaling the third coordinate by `q^(-1/2)` sends the occupied conditional corners to

```text
1, 1+a, 1+a, 1+2a,  a=lambda/q,
```

and gives

```text
G1_normalized''=G1''/q.
```

The additional `log(q) K33/q` term is affine, so the scaling preserves the sign and strictness of the Hessian.

Second, direct differentiation of the four selected complete events gives the exact edge/cell identity (7) in that file. Leaf exchange splits it into a two-dimensional antisymmetric block and a four-dimensional symmetric block. With

```text
u=log(1+a), v=log(1+2a),
```

the antisymmetric matrix is exactly

```text
[ 2(a+1)(2u-v),                    (2u-v)/2 ]
[ (2u-v)/2, (a v+4a+v)/(8a(a+1))              ],
```

and its determinant is

```text
(2u-v)[4a+v+2a(v-u)]/(4a)>0.
```

Third, on the symmetric block, exact inversion of the retained three-node endpoint chain gives

```text
kappa_chain-J/(32a^2)=(1-r)N(r)/[32r^2D(r)],
r=a/(1+a).
```

The formulas for `N` and `D` agree identically with those printed in the theorem file. The denominator is positive because it is a positive multiple of `c^T adj(M)c` for the positive chain matrix. For the numerator, putting `x=r^2`,

```text
A(x)=atanh(sqrt(x))/sqrt(x),
C(x)=-log(1-x)/x,
E(x)=2A(x)-C(x)
```

gives the same identities

```text
N=x^2 F,
F'=C L/(2x).
```

The coefficient calculation was also independently checked. For every `n>=1`,

```text
[x^n]L
=24/(2n+1)-4/n-12H_(2n)/(2n+1)
 +4H_(2n-2)/(2n-1)+8H_n/(n+1)-4H_(n-1)/n,
```

and the decomposition used there yields

```text
[x^n]L
>=6(10n^2-5n-3)/[n(n+1)(2n-1)(2n+1)]>0.
```

No algebraic discrepancy was found. Thus the equal-strength conclusion is **CORRECT WITHIN THE RECONSTRUCTED SCOPE**: for every strict `A=B` half-leaf, both `G1''` and `G0''` are separately positive definite, and the complete Shannon Hessian has the strict concave sign. This remains an author theorem pending a genuinely separate reviewer or formal verification.

The new checker `code/verify_small_edge_algebra.py` records the antisymmetric determinant and exact chain-gap algebra. Its finite execution is supporting algebra only; the all-`n` coefficient inequality above is the analytic proof.

## 3. Exact unequal-strength one-sided core

Normalize the occupied rare corner to one. Put

```text
t00=1+a+b, t10=1+b, t01=1+a, t11=1,
u=log(1+a), v=log(1+b), w=log(1+a+b),
ell=(u+w-v)/2, k=(v+w-u)/2,
lambda=w-u-v<0,
J=(1+a+b)w-(1+a)u-(1+b)v,
n=-(1+(a+b)/2) lambda.
```

Use the four conditional-score coordinates `U=(m,alpha,beta,gamma)` and leaf-diagonal coordinates `delta=(d,e)`. Direct collection of the complete selected-event Hessian gives

```text
G1''=delta^T L delta+2 delta^T C U+U^T Y U,          (1)
```

where

```text
L=[[2a ell, J],
   [J, 2b k]],

C=[[-ell, 0,        lambda/4, 0],
   [-k,   lambda/4, 0,        0]].                  (2)
```

Let

```text
E4=[[1,-1/2,-1/2, 1/4],
    [1, 1/2,-1/2,-1/4],
    [1,-1/2, 1/2,-1/4],
    [1, 1/2, 1/2, 1/4]].
```

Then the complete Fisher block and retained acceleration block are

```text
F=(1/4) E4^T diag(1/t00,1/t10,1/t01,1) E4,

R=[[0,0,0,0],
   [0,ell/(8a),0,-lambda/(32a)],
   [0,0,k/(8b),-lambda/(32b)],
   [0,-lambda/(32a),-lambda/(32b),n/(32ab)]],
Y=F+R>0.                                               (3)
```

Thus all six-direction occupied-side positivity is exactly the two-dimensional condition

```text
E(a,b)=L-C Y^(-1) C^T>0.                              (4)
```

Equations (1)--(4) are an exact full-event Schur complement, not a sampled or relaxed criterion. They are also the correct object for continuing away from `a=b`; deleting the completed leaf-diagonal squares before forming (4) is too strong, as Section 5 shows.

## 4. New theorem: arbitrary fixed strong edge and a vanishing second edge

### Theorem 4.1: normalized occupied side

For every fixed `a>0`, there exists `epsilon(a)>0` such that

```text
G1''>0
```

in every nonzero six-coordinate physical direction whenever

```text
0<b<epsilon(a).
```

The choice can be made uniformly when `a` ranges over a compact subset of `(0,infinity)`.

### Proof

Every apparent quotient by `b` in (3) has a removable real-analytic limit at `b=0`. Write `u=log(1+a)` and order `U` as `(m,alpha | beta,gamma)`. The limiting positive pivot is block diagonal:

```text
Y(0)=diag(Y_A,Y_B),

Y_A=[[ (a+2)/(2(a+1)),                  a/(4(a+1)) ],
     [ a/(4(a+1)), u/(8a)+(a+2)/(8(a+1))          ]],

Y_B=3/[64(a+1)] [[4(a+2),2a],
                  [2a,a+2]].                         (5)
```

Both blocks are positive definite because

```text
det Y_A=[(a+2)u+4a]/[16a(a+1)]>0,
det Y_B=9/[256(a+1)]>0.                              (6)
```

At `b=0`, the Schur core (4) is

```text
E(a,0)=diag(E_A,0),

E_A=2u[4a^2-(a+1)u^2]/[(a+2)u+4a].                  (7)
```

This first pivot is strictly positive. Indeed, with `x=sqrt(1+a)>1`,

```text
u=2 log x < 2(x-1/x)=2a/sqrt(1+a),
```

because `x-1/x-log x` vanishes at one and has derivative
`(x^2-x+1)/x^2>0`.

It remains to resolve the zero pivot. Let `e_1=(1,0,0,0)^T` and set

```text
y00=(a+2)/(2(a+1)).
```

The small-`b` limits from (2)--(3) are

```text
C_e/b -> -e_1^T Y(0),
L_ee/b^2 -> 2 y00,
L_de/b -> u,
C_d(0)=-u e_1^T.                                     (8)
```

Consequently

```text
E_ee/b^2
 ->2y00-[e_1^T Y(0)]Y(0)^(-1)[Y(0)e_1]
 =y00>0,                                              (9)

E_de/b
 ->u-[-u e_1^T]Y(0)^(-1)[-Y(0)e_1]
 =0.                                                  (10)
```

Equations (7), (9), and (10) give

```text
det E(a,b)/b^2 -> E_A y00>0.                         (11)
```

For all sufficiently small positive `b`, the first pivot and determinant of `E(a,b)` are therefore positive. Since `Y>0`, the full six-by-six form (1) is positive definite. Joint analyticity and compactness make the choice uniform on compact `a` intervals. This proves the theorem.

### Corollary 4.2: a true Shannon punctured boundary face

Fix

```text
A>0, q>0, qbar_*=1-A-q>0.
```

There exists `B_*(A,q)>0` such that, for every

```text
0<B<B_*(A,q), qbar=qbar_*-B>0,
```

the strict half-leaf kernel with strengths `(A,B)` has

```text
G1''>0, G0''>0, and -H''>0                            (12)
```

in every nonzero real-symmetric physical direction.

For the occupied side, normalize by `q`: `a=A/q` is fixed and `b=B/q` tends to zero, so Theorem 4.1 applies. For the vacant side, full complementation gives the same occupied-side problem with rare corner `qbar`; now `A/qbar` tends to `A/qbar_*` and `B/qbar` tends to zero. The theorem applies again. Finally

```text
-H''=4(d11^2+d22^2)+G1''+G0''.                       (13)
```

This proves (12), retaining all eight events and the leaf marginal. The conclusion is uniform when `(A,q,qbar_*)` ranges over a compact subset of the positive boundary face. Leaf exchange gives the analogous theorem near `A=0`.

For each fixed positive `B` in this punctured face, ordinary continuity also supplies an open neighborhood with genuinely unequal leaf diagonals `x!=1/2` or `y!=1/2`. No radius uniform as `B->0` is claimed: the certified weak-leaf Schur pivot in (9) is of order `(B/q)^2`, so black-box continuity necessarily loses its margin at the boundary.

## 5. Precise obstruction: endpoint residuals alone do not prove the unequal case

After completing each leaf-diagonal square in the four edge terms, one might keep only the four endpoint residual matrices and ask them to absorb the negative cell term. Let `kappa_res(a,b)` be the optimal coefficient of

```text
Delta=T00-T10-T01+T11
```

in that residual-only network. Exact inversion of its `b->0` limit gives

```text
kappa_res(a,0)
=[9a^2-(a+1)u^2]
 /[16a(3a^2+6a-2(a+1)u)], u=log(1+a),               (14)
```

whereas

```text
J/(32ab) -> u/(32a).                                 (15)
```

Their limiting gap is

```text
kappa_res(a,0)-u/(32a)
=-3[(a+2)u-6a]
 /[32(3a^2+6a-2(a+1)u)].                             (16)
```

The denominator is positive; for example `u<a` gives it a lower bound `a^2+4a`. Therefore the residual-only criterion fails whenever

```text
(a+2)log(1+a)>6a.                                    (17)
```

This is not an empty regime. At `a=1000`, `log(1001)>6` because `e<3` implies `e^6<729<1001`; hence the left side of (17) is greater than `6012`, while the right side is `6000`. By continuity, the residual-only gap is strictly negative for every sufficiently small positive `b`.

At exactly the same parameters, Theorem 4.1 proves the complete integrated `G1''` is positive definite. Thus (16) is a genuine **method obstruction**: the unequal-strength proof must retain the completed leaf-diagonal squares and their `2Jde` coupling, equivalently the full core (4). It is not a one-sided entropy counterexample and not a Shannon entropy counterexample.

## 6. Scope after this continuation

Proved at author level and independently reconstructed within this session:

- the exact negative pointwise `Phi_r''` witness from all eight Möbius events;
- correctness within scope of the full equal-strength theorem;
- separate occupied and vacant one-sided positivity on a punctured neighborhood of either single-edge boundary face, for arbitrary fixed strength on the other edge;
- strict complete Shannon concavity there in all six physical directions;
- failure of the residual-only endpoint network as a universal unequal-strength certificate.

Still open:

- integrated one-sided positivity for every pair `a,b>0`;
- complete half-leaf concavity throughout the compact unequal-strength middle;
- a boundary-uniform quantitative radius for unequal leaf diagonals;
- general missing-edge and general real three-point Shannon concavity;
- any genuine Shannon entropy counterexample;
- novelty and formal verification.

The next exact target is the sign of the two-by-two core (4), not pointwise resolvent positivity and not the residual-only chain.
