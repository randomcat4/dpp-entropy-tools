# Boundary theorems v2

Status: `PROVED_HERE` for the fixed families below; no new formal verification
gate was run. The unrestricted real-kernel entropy-concavity question remains
`INCOMPLETE`, and no real counterexample is claimed.

Throughout, `H(K)` is the Shannon entropy of the full exact-event DPP law,
not of the principal inclusion minors.

## 1. Mixed longitudinal/transverse blow-up

Fix orthonormal frames `U in R^(n x r)` and `V in R^(n x s)`, with
`[U,V]` orthogonal. For `sigma in {+1,-1}`, set

```text
H_sigma=A-sigma X,        L_sigma=C+sigma Y,
R_H,sigma=H_sigma-BB^T,  R_L,sigma=L_sigma-B^T B,

K_sigma(epsilon)=[U V]
  [[I-epsilon H_sigma, sigma sqrt(epsilon) B],
   [sigma sqrt(epsilon) B^T, epsilon L_sigma]]
  [U V]^T.
```

The exact two-term endpoint is a positive contraction for every sufficiently
small positive `epsilon` exactly when, for both signs,

```text
R_H,sigma>=0, R_L,sigma>=0,
ker R_H,sigma subset ker B^T,
ker R_L,sigma subset ker B.
```

This kernel compatibility is essential at singular Schur limits. Under these
conditions, with `F=||B||_F^2`, define

```text
psi_S=det(U_S),
phi_S=(d/da)det((U+aVB^T)_S)|_(a=0),
Z=sum_(|S|=r,psi_S=0) phi_S^2.
```

Then `0<=Z<=F` and

```text
[H(K_+)+H(K_-)]/2-H((K_++K_-)/2)
  =(Z-2F) epsilon log(1/epsilon)+O(epsilon).
```

Thus every fixed feasible member with `B!=0` has a strictly negative gap for
all sufficiently small `epsilon`. Longitudinal directions `X,Y`, including
feasible singular residuals, cannot change this leading sign.

## 2. The zero-transverse hierarchy

When `B=0`, the logarithmic coefficient above vanishes. Let `M_U` and `M_V`
be the complete one-hole and one-particle cofactor measurement maps defined in
the accompanying proofs. The first finite coefficient is a coordinatewise
entropy Jensen gap and is nonpositive. Equality holds exactly when

```text
M_U(X)=0,  M_V(Y)=0.
```

On this equality kernel, the entire
`epsilon^2 log(1/epsilon)` coefficient also vanishes. The key eventwise fact is
that, for every zero Pluecker coordinate, the one-hole/one-particle
replacement matrix is zero or rank one, and the tomography condition
annihilates that rank-one direction.

Consequently the first unresolved general term is

```text
Delta_epsilon=C_2 epsilon^2+O(epsilon^3 log(1/epsilon)).
```

An exact finite exterior-minor formula for `C_2` is proved in
`proofs/b_zero_c2_decomposition_v2.md`. Its zero-support cross term is always
nonpositive. A positive example, if one exists at this scale, must come from a
nonuniform active-support correlation or from a pure deletion/insertion term
that does not reduce to the small-kernel theorem.

## 3. Families where the remaining term is sealed

Three further complete exclusions are proved.

1. **Small kernels.** For any fixed distinct PSD matrices `A_+,A_-`, with
   `A_0=(A_++A_-)/2`,

   ```text
   [H(epsilon A_+)+H(epsilon A_-)]/2-H(epsilon A_0)<0
   ```

   for every sufficiently small feasible `epsilon`. Different diagonals are
   excluded at order `epsilon`; equal diagonals are excluded at order
   `epsilon^2` by the pair determinant expansion. Singular PSD matrices and
   zero pair determinants are included.

2. **Paired frames.** For paired frames in every dimension, including
   arbitrary independent pair rotations and arbitrary fixed PSD inward
   matrices `A,C`, the tomography-kernel coefficient is

   ```text
   C_2=Gamma(A-X,A+X;A)+Gamma(C-Y,C+Y;C)<=0.
   ```

   It is strictly negative whenever `X` or `Y` is nonzero.  For diagonal
   `A,C`, this reduces to the exact pairwise form

   ```text
   C_2=-sum_(i<j)
       [G_(a_i a_j)(x_ij^2)+G_(c_i c_j)(y_ij^2)],
   G_D(z)=z+(D-z)log(1-z/D).
   ```

   and satisfies the quantitative bound

   ```text
   C_2<=-(1/2)sum_(i<j)
      [x_ij^4/(a_i a_j)+y_ij^4/(c_i c_j)].
   ```

3. **Rank-two one-sided kernels.** If `r=2`, `Y=0`, and
   `0!=X in ker M_U`, the cofactor null-cone forces a disjoint-support frame,
   and `C_2<0`. The complementary statement holds when `s=2`, `X=0`, and
   `0!=Y in ker M_V`.

## 4. Unequal scalar approach rates

The nonzero-transverse exclusion also survives unequal powers. Put

```text
M_epsilon=(1-epsilon^alpha)P+epsilon^beta Q,
t_epsilon=tau epsilon^(m/2),  m=max(alpha,beta),
K_sigma=M_epsilon+sigma t_epsilon D.
```

For fixed `alpha,beta>0` and `tau||B||_op<1`, the endpoints are feasible for
all sufficiently small `epsilon`, and

```text
Delta_epsilon
 =tau^2[mZ-(alpha+beta)F]
    epsilon^m log(1/epsilon)+O(epsilon^m).
```

Since `Z<=F`, the bracket is at most `-min(alpha,beta)F`. Hence every nonzero
transverse direction remains strictly negative, no matter how unbalanced the
two scalar spectral slacks are.

## Remaining exact blocker

The surviving fixed-scale branch is

```text
B=0,
M_U(X)=0,
M_V(Y)=0,
C_2 not covered by a paired-frame or rank-two reduction.
```

The current work neither signs this `C_2` universally nor produces a positive
instance. Moving frames, data that vary with `epsilon`, and still higher
valuation hierarchies remain outside these fixed-family theorems.
