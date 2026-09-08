# D10-U10a scalar_direct fresh non-author audit

STATUS: CORRECT for the stated identities, sufficient-condition
classifications, and exact rational path blocker.

STATUS: INCOMPLETE for the global conjecture `rho(K)<=1`.

STATUS: SCOUT for the 29-row finite sanity denominator.

I did not import or execute the author `sanity.py`, `self_review`, or any U8
gate.  The audit script implements its own n=3 exact-event arithmetic and only
reads author JSON/text as frozen data.

## 1. Lemma 1: connected support implies `F>0`

The proof is correct.  If `F(D)=0`, then every atom derivative vanishes, hence
by invertible Mobius transform every inclusion determinant derivative
vanishes.  The singleton moments give `D_ii=0`.  Every nonzero edge `K_ij`
then gives

```text
d det K_{ij} = -2 K_ij D_ij = 0,
```

so all present-edge coordinates vanish.  In the only remaining connected
three-vertex case, exactly one edge is missing; if `K_12=0` and
`K_13 K_23 != 0`, the full determinant derivative in the missing coordinate
is `2 K_13 K_23 D_12`, forcing `D_12=0`.  The other paths are relabelings.

Independent exact Fraction LDL pivots of the Fisher matrix:

```text
dense exchangeable edge 1/10:
29675/7392, 20093125/5013888, 5224375/1305744, 5596/8359, 12096/18187, 125/189

centered path edge 3/10:
902512/188125, 289375/56407, 4, 66672/7525, 1296/463, 3600/463
```

These checks supplement but do not replace the symbolic argument.

## 2. `rho = min_g Q(g)`

The regularized projection identity is correct.  In the notation of the author
file, after the congruence `D=N^{1/2} E N^{1/2}`, the positive part before the
negative trace update is

```text
||E||_F^2 + sum_S <C_S,E>^2,
```

where `C_S=N^{1/2}W_SN^{1/2}/sqrt(delta p_S)`.  The squared dual norm of
`E -> tr(E)` is therefore

```text
<I,(I+T*T)^-1 I>,
```

and completing the square gives the ridge form

```text
rho = min_g [
  ||I - N^{1/2}(sum_S g_S W_S)N^{1/2}||_F^2
  + delta sum_S p_S g_S^2
].
```

Constants in `g` only add cost because `sum_S W_S=0`; the mean-zero convention
is harmless.

Independent Decimal minimization:

| point | `min Q` | `rho` | difference |
| --- | ---: | ---: | ---: |
| dense edge `1/10` | `0.1208954524942181943...` | same | `-4e-99` |
| path edge `3/10` | `0.5132681842709295321...` | same | `1.2e-99` |

## 3. Unregularized `V` and the path branch

The inclusion-statistic formula is correct.  The seven nonempty inclusion
indicators span functions modulo constants; their covariance matrix is
positive definite because a zero-variance linear combination must be constant
on all eight atoms and Boolean Mobius inversion kills all nonempty
coefficients.  With inclusion Jacobian `J`,

```text
V = min_{J^T beta=eta} beta^T C beta
  = eta^T F^{-1} eta.
```

The dense explicit line formula is valid only when `abc != 0`; the author
correctly separates the path branch and avoids division by the missing edge.
For a path with `a=0, bc!=0`, the `D_12` constraint fixes `beta_r=eta_12/(2bc)`,
the two present-edge constraints solve `beta_13,beta_23`, and `beta_12`
remains the one free parameter before the three diagonal equations determine
`beta_x,beta_y,beta_z`.

Independent KKT solves agree with the Fisher inverse:

```text
dense V difference = 2e-98
path V difference  = -5e-100
```

## 4. Five-category Fisher, complement, and exact loss

The five-category formula is correct as a sufficient certificate, not a
necessary condition.  For `T={empty,12,13,23}` and `R` its complement,

```text
F - F_T = sum_{s in R} p_s
          (dot p_s/p_s - dot p_R/p_R)^2 >= 0
```

as a quadratic form.  Therefore `B>=B_T`; if the Schur scalar of `B_T` is
subunit, full `B` is positive.  The converse is not valid and is explicitly
not claimed after the rational blocker.

The complement orientation is also classified correctly: it is a second
sufficient test obtained through `p_{I-K}(S)=p_K(S^c)` and sign of affine
derivatives.  It is not a new equivalence.

## 5. Rational path blocker

For

```text
K = [[1/2, 3/10, 0],
     [3/10, 1/2, 3/10],
     [0, 3/10, 1/2]]

D = [[1, -3/5, 1/3],
     [-3/5, 5/6, -3/5],
     [1/3, -3/5, 1]]
```

the independent exact-event jets are:

```text
p  = (7,25,43,25,25,43,25,7)/200
p' = (-137,-197,-463,197,-197,31,197,569)/600
p''= (197,16,203,-416,16,-229,-416,629)/225
```

The log intervals certify:

```text
proxy B_T(D) < 0
actual B(D) > 0
```

with rounded displays

```text
F(D,D)   = 56578567/1693125
F_T(D,D) = 12487351/3386250
rho      = 0.5132681842709295321...
R_T      = 1.0953535868173425751...
R_T'     = 1.0953535868173425751...
```

The signs are exactly the author's intended signs: the coarse proxy fails, but
the true DPP entropy Hessian is still negative in this direction
(`B=-H''>0`).  This is not a positive-curvature candidate.

The positive direction and whole chord are certified exactly:

```text
D LDL pivots: 1, 71/150, 352/639
K(t)-I/1000 and I-K(t)-I/1000 positive at t=±1/100
```

Convexity of the positive semidefinite cone then covers the entire real
segment `|t|<=1/100` with the stated margin.

The complement/sign-conjugacy transfer is valid here: with
`S=diag(1,-1,1)`, `I-K=SKS`, and `SDS` remains positive definite.

## 6. Three rank-one score contrasts and Sherman-Morrison corrections

The rank-one Fisher splitting is exact.  For disjoint positive groups `A,B`,

```text
j_A j_A^T/p_A + j_B j_B^T/p_B
 - (j_A+j_B)(j_A+j_B)^T/(p_A+p_B)
= (p_B j_A-p_A j_B)(p_B j_A-p_A j_B)^T/[p_A p_B(p_A+p_B)].
```

The chosen three nested splits of `R={1,2,3,123}` telescope to

```text
F = F_T + w1 h1h1^T + w2 h2h2^T + w3 h3h3^T.
```

The audit script verifies all 36 entries exactly for both dense and path
examples.  The Sherman-Morrison corrections are sequential and have positive
denominators because `A_{i-1}>0` and `w_i>0`; using the updated inverse at
each step is essential and is what the author states.

For the path blocker:

```text
R_T = 1.0953535868173425751...
c1  = 0.5475945716632780954...
c2  = 0.0049791631619406727...
c3  = 0.0295116677211942749...
R_T-c1-c2-c3 = rho = 0.5132681842709295321...
```

Thus equation `(27)`,

```text
c1+c2+c3 >= R_T-1 when R_T>1,
```

is correctly identified as equivalent to the remaining scalar problem on that
region, not as a solved sufficient lemma.

## 7. Finite denominator and scope

The frozen `sanity.json` records:

```text
rows = 29
distinct K = 29
families = exchangeable_center 4, centered_path 6,
           rank_one_boundary 15, complement_boundary 4
rho >= 1 rows = 0
trace-capacity passes = 15/29
five-category passes = 23/29
six-category passes = 29/29
```

These are sanity denominators only.  The 29/29 six-category pass is not a
universal theorem, and the author text correctly keeps it as a next candidate
rather than a conclusion.

## Final classification

- Lemma 1 connected `F>0`: CORRECT.
- `rho=min_g Q(g)`: CORRECT exact equivalence.
- Unregularized `V` and path branch: CORRECT; dense formula and path branch
  have the necessary nonzero-edge separation.
- Trace-capacity condition: CORRECT sufficient condition only; non-universal.
- Five-category and complement-adaptive certificates: CORRECT sufficient
  conditions only; non-universal due exact path blocker.
- Rational path blocker: CORRECT and exactly scoped to the proxy, not the
  original DPP Hessian.
- Three rank-one score splits and sequential Sherman-Morrison corrections:
  CORRECT; equation `(27)` remains an equivalent blocker.
- Global `rho<=1`: INCOMPLETE.

No critical gap or hidden range expansion was found in the scalar_direct
claims as they are actually classified.
