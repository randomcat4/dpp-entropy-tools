# Finite `C2` decomposition after the `B=0` tomography gates

Status: INCOMPLETE for a universal proof of `C2<=0`.

Status: PROVED for the event-layer decomposition below and for the resulting
finite-dimensional positive-sign criterion.

This note starts after the already sealed gates

```text
B=0,
M_U(X)=0,
M_V(Y)=0,
L_2=0.
```

It does not use the paired-frame calculation.

## 1. Notation and rates

Work in orthonormal frames `U in R^(n x r)` and `V in R^(n x s)`.  For a
branch write

```text
G=A-sigma X,
R=C+sigma Y,
tau(G,R)=tr G + tr R,
kappa(G,R)=e_2(G)+e_2(R)+(tr G)(tr R),
e_2(H)=((tr H)^2-tr(H^2))/2.
```

Let `f(x)=x log x` for `x>0` and `f(0)=0`; all logarithms are natural.

For an `r`-set `S`, put

```text
a_S = p_P(S) = det(U_S)^2.
```

The active projection support and zero `r`-support are

```text
A_r = { |S|=r : a_S>0 },
Z_r = { |S|=r : a_S=0 }.
```

For `|R|=r-1`, let `alpha_R in R^r` be the one-hole cofactor vector and set

```text
m_R(H)=alpha_R^T H alpha_R.
```

For `|T|=r+1`, let `beta_T in R^s` be the one-particle cofactor vector and set

```text
n_T(L)=beta_T^T L beta_T.
```

For `|S|=r-2`, let `omega^U_S in Lambda^2 R^r` be the signed vector of
two-column deletion cofactors:

```text
(omega^U_S)_{ij} = +/- det(U_{S,[r]\{i,j}}),  i<j.
```

The sign is the exterior-algebra sign consistent with the ordered basis
`e_i wedge e_j`.  Define the two-hole rate

```text
m^{(2)}_S(H)= < omega^U_S, (Lambda^2 H) omega^U_S >.
```

For `|T|=r+2`, let `omega^V_T in Lambda^2 R^s` be the signed vector with
coordinates

```text
(omega^V_T)_{ij} = +/- det([U,v_i,v_j]_T),  i<j,
```

and define the two-particle rate

```text
n^{(2)}_T(L)= < omega^V_T, (Lambda^2 L) omega^V_T >.
```

Finally, for `|S|=r`, define `T_S in R^(r x s)` by one high-column
replacement:

```text
(T_S)_{ij}=det(U with column i replaced by v_j, restricted to rows S),
q_S(H,L)=tr(H T_S L T_S^T).
```

All these rates are invariant under orthogonal changes of basis inside the
`U` and `V` subspaces, with the matrices `H,L` transformed accordingly.  The
definitions are written in a basis only to expose the finite computation.

## 2. Exact-event expansions through order `eps^2`

The following expansions are obtained from the exact spectral event
decomposition, equivalently from the Mobius full-event law.  Principal minors
are not used as exact event probabilities.

For active `r`-events `S in A_r`,

```text
p_{G,R}(S)
 = a_S
   - eps tau(G,R) a_S
   + eps^2 [ kappa(G,R) a_S + q_S(G,R) ]
   + O(eps^3).
```

For zero-support `r`-events `S in Z_r`,

```text
p_{G,R}(S)=eps^2 q_S(G,R)+O(eps^3).
```

For one-hole events `|R_0|=r-1`,

```text
p_{G,R}(R_0)
 = eps m_{R_0}(G)
   + eps^2 [ m_{R_0}(G^2)-tau(G,R)m_{R_0}(G) ]
   + O(eps^3).
```

For one-particle events `|T_0|=r+1`,

```text
p_{G,R}(T_0)
 = eps n_{T_0}(R)
   + eps^2 [ n_{T_0}(R^2)-tau(G,R)n_{T_0}(R) ]
   + O(eps^3).
```

For two-hole and two-particle events,

```text
p_{G,R}(S)=eps^2 m^{(2)}_S(G)+O(eps^3),       |S|=r-2,
p_{G,R}(T)=eps^2 n^{(2)}_T(R)+O(eps^3),       |T|=r+2.
```

All other cardinalities have probability `O(eps^3)` and contribute
`O(eps^3 log(1/eps))` to entropy.

## 3. Simplifications under the tomography kernels

Set

```text
G_sigma=A-sigma X,
R_sigma=C+sigma Y,
G_0=A,
R_0=C.
```

The one-flip kernel assumptions imply

```text
m_R(G_sigma)=m_R(A),
n_T(R_sigma)=n_T(C),
tr X=tr Y=0.
```

Therefore `tau(G_sigma,R_sigma)` is independent of `sigma`, and

```text
bar kappa - kappa_0 = -(tr X^2 + tr Y^2)/2,
bar q_S - q_{0,S} = -q_S(X,Y).
```

For zero-support `r`-sets, the adjugate audit gives

```text
q_S(X,Y)=0,             S in Z_r,
```

so `q_S(A,C)` is the endpoint average of
`q_S(A-X,C+Y)` and `q_S(A+X,C-Y)`.

For one-hole and one-particle second coefficients,

```text
bar[ m_R(G_sigma^2)-tau m_R(G_sigma) ]
  - [ m_R(A^2)-tau m_R(A) ]
  = m_R(X^2),

bar[ n_T(R_sigma^2)-tau n_T(R_sigma) ]
  - [ n_T(C^2)-tau n_T(C) ]
  = n_T(Y^2).
```

If `m_R(A)=0`, then positivity of `A+X` and `A-X` gives
`(A+X)alpha_R=(A-X)alpha_R=0`, hence `m_R(X^2)=0`; such events make no
one-flip finite contribution.  The same convention applies to `n_T(C)=0`.

## 4. The `C2` formula

Let

```text
N = tr(X^2)+tr(Y^2).
```

Then

```text
Delta(eps)
 = eps^2 C_2 + O(eps^3 log(1/eps))
```

after the previous logarithmic gates have vanished, with

```text
C_2 = C_act + C_1U + C_1V + C_2U + C_2V + C_0UV.
```

The active-support term is

```text
C_act =
  sum_{S in A_r} (1+log a_S) [ (N/2) a_S + q_S(X,Y) ].
```

Equivalently, since `sum_{S in A_r} q_S(X,Y)=0`,

```text
C_act =
  (N/2) sum_{S in A_r} a_S(1+log a_S)
  + sum_{S in A_r} (log a_S) q_S(X,Y).
```

Here the identity `sum_{S in A_r} q_S(X,Y)=0` follows from
`sum_{|S|=r}q_S(X,Y)=tr X tr Y=0` and from the adjugate audit, which kills
all zero-support summands.

The one-flip correction terms are

```text
C_1U =
  - sum_{|R|=r-1, m_R(A)>0}
      (1+log m_R(A)) m_R(X^2),

C_1V =
  - sum_{|T|=r+1, n_T(C)>0}
      (1+log n_T(C)) n_T(Y^2).
```

The pure two-hole and two-particle finite rare-event terms are

```text
C_2U =
  sum_{|S|=r-2}
    [ f(m^{(2)}_S(A))
      - (1/2)f(m^{(2)}_S(A-X))
      - (1/2)f(m^{(2)}_S(A+X)) ],

C_2V =
  sum_{|T|=r+2}
    [ f(n^{(2)}_T(C))
      - (1/2)f(n^{(2)}_T(C+Y))
      - (1/2)f(n^{(2)}_T(C-Y)) ].
```

The zero projection-support one-hole/one-particle term is

```text
C_0UV =
  sum_{S in Z_r}
    [ f(q_S(A,C))
      - (1/2)f(q_S(A-X,C+Y))
      - (1/2)f(q_S(A+X,C-Y)) ].
```

This is the promised finite, computable criterion: once the PSD endpoint
conditions and one-flip tomography equalities hold, `C_2>0` is sufficient for
a genuine local positive entropy chord,

```text
Delta(eps)>0
```

for all sufficiently small positive `eps`.

## 5. Signed and convex pieces

The zero-support cross term has a definite sign:

```text
C_0UV <= 0.
```

Reason: for `S in Z_r`, the adjugate audit gives

```text
q_S(A,C)
 = ( q_S(A-X,C+Y) + q_S(A+X,C-Y) )/2,
```

and `f(x)=x log x` is convex on `[0,infty)`.  This remains valid at singular
rates by the convention `f(0)=0`.  If the center rate is zero, nonnegativity
of both endpoint rates forces both endpoint rates to be zero.

The other pieces are finite and basis-invariant but not sign-definite from
convexity alone:

1. `C_act` contains the signed active-support correlation

```text
sum_{S in A_r} (log a_S) q_S(X,Y).
```

This term vanishes if the projection DPP is uniform on its active `r`-support,
but in general it has no fixed sign.

2. `C_1U+C_2U` and `C_1V+C_2V` are the pure deletion and pure insertion
projection-boundary second coefficients.  They reduce to the already proved
small-kernel two-point Jensen gaps in coordinate small-kernel reductions, but
for a general projection frame the channel from latent spectral flips to
coordinate events prevents an immediate reduction to the small-kernel theorem.

3. The factors `m_R(X^2)` and `n_T(Y^2)` are nonnegative, but their weights
`-(1+log m_R(A))` and `-(1+log n_T(C))` are signed.  The two-flip terms are
also not plain Jensen gaps because

```text
m^{(2)}_S(A)
```

is not generally the endpoint average of
`m^{(2)}_S(A-X)` and `m^{(2)}_S(A+X)`; the missing curvature is exactly what
cancels the `eps^2 log` coefficient against the one-flip corrections.

## 6. Minimal remaining positive structure

The gates now force the following necessary structure for a positive example
in the `B=0` scale:

1. `B=0`; otherwise the `eps log(1/eps)` coefficient is strictly negative.
2. `M_U(X)=0` and `M_V(Y)=0`; otherwise the order-`eps` finite Jensen term is
   strictly negative.
3. The `eps^2 log(1/eps)` coefficient is automatically zero by the adjugate
   audit.
4. Therefore a positive gap must satisfy the finite inequality

```text
C_act + C_1U + C_1V + C_2U + C_2V + C_0UV > 0.
```

Since `C_0UV<=0`, positivity must come from at least one of:

```text
C_act,
C_1U+C_2U,
C_1V+C_2V.
```

In particular, a viable non-coordinate escape needs either

- nonuniform active projection weights `a_S` correlated with the signed active
  cross rates `q_S(X,Y)`, or
- a positive pure deletion/insertion projection-boundary second coefficient
  not reducible to the small-kernel two-point theorem.

I do not have a proof that these signed pieces are always nonpositive, nor a
concrete positive instance satisfying all gates.  The decomposition above is
therefore a finite-dimensional certificate: evaluating its finitely many
exterior-minor rates decides the sign of the first still-available coefficient
for any proposed `U,V,A,C,X,Y`.

## 7. Relation to the small-kernel `Gamma` route

There is a natural latent-flip interpretation.  The high holes and low
particles are independent small DPPs in the spectral coordinates, and the
coordinate event is produced by a fixed projection-DPP channel depending only
on `U,V` and on the selected flip pattern.

In paired or disjoint-support frames this channel is block-separable at order
`eps^2`.  In that special situation the formula above collapses to the sum of
two ordinary small-kernel two-point coefficients,

```text
Gamma(A-X,A+X;A) + Gamma(C-Y,C+Y;C),
```

including the diagonal case where it becomes the previously observed negative
sum of pairwise terms.

For general tomography-kernel frames, I do not see a valid one-line data
processing seal.  Data processing controls KL divergence to an endpoint
mixture, but the small-DPP center probability vector is not exactly the
endpoint average at order `eps^2`; the non-affine drift is precisely what the
one-flip and two-flip corrections cancel at the logarithmic level.  A
measurement channel can reduce the negative Jensen/KL part while leaving a
signed drift term, so the desired representation as

```text
small-kernel Gamma + nonpositive information loss
```

requires an additional identity not proved here.

Thus the `Gamma` route remains the most plausible path to a full seal, but at
this point it is a named open subproblem, not a proved consequence of data
processing.


