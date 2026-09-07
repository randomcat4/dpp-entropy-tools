# Boundary theorems v3

Status: `PROVED_HERE` for the frozen-v2 general boundary coefficient theorem,
pending one commit-bound verification gate.  Earlier Round-2 extensions retain
their stated status.  The unrestricted real-kernel entropy-concavity question
remains `INCOMPLETE`, and no real counterexample is claimed.

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

The remaining ordinary coefficient is now signed in full.  Form the graph on
physical coordinates with an edge `i--j` when `P_ij!=0`, and let its
connected components be `E_a`.  The complete tomography kernel has the exact
description

```text
M_U(X)=0, M_V(Y)=0
  iff X_aa=0 and Y_aa=0 for every coordinate component a.
```

Thus every invisible direction is off-block between mutually orthogonal
coordinate components.  The projection law factorizes over these components.
The logarithmically weighted active-support cross term cancels by local
Cauchy--Binet orthogonality, and the zero-support cross term vanishes
eventwise.

For local high one-hole cofactors `alpha in E_a`, `beta in E_b`, put

```text
g=alpha^T A_aa alpha, h=beta^T A_bb beta,
u=alpha^T A_ab beta,  x=alpha^T X_ab beta, D=gh,
Phi_D(v)=G_D(v^2),
G_D(z)=z+(D-z)log(1-z/D).
```

Define `gamma_D(u,x)=Phi_D(u)-[Phi_D(u+x)+Phi_D(u-x)]/2`, with the
forced zero value when `D=0`.  The exact coefficient is

```text
C_2 =
  sum_(a<b) sum_(alpha,beta) gamma_(gh)(u,x)
 +sum_(a<b) sum_(eta,theta) gamma_(g_V h_V)(u_V,y).
```

The second sum is the complementary low one-particle formula.  Endpoint
positivity places every argument in `[-sqrt(D),sqrt(D)]`, and `Phi_D` is
strictly convex there.  Consequently

```text
C_2<=0,
C_2<0 whenever (X,Y)!=(0,0).
```

This includes arbitrary non-paired frames, simultaneous high/low directions,
singular inward matrices, singular endpoints, and zero Pluecker coordinates.
The structural proof is in `proofs/tomography_components_v3.md`; the complete
coefficient proof is in `proofs/component_pair_C2_v3.md`.

## 3. Earlier sealed subfamilies

The following earlier exclusions are recovered as special cases or remain
useful independent reductions.

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

## Remaining scope boundary

There is no remaining unsigned coefficient in the frozen fixed-data,
two-term projection-boundary hierarchy treated here.  This does **not** prove
global entropy concavity for arbitrary interior real kernels.  Moving frames,
data that vary with `epsilon`, unrelated approach geometries, and global
chords away from a projection face remain outside these theorems.
