# I05-31 — exact fixed-parameter endpoint phase diagram for integrated acceleration

Status: **AUTHOR ANALYTIC PROOF / PENDING_INDEPENDENT_REVIEW; novelty NOT_ASSESSED.** This note concerns the complete-configuration Shannon law of the true affine physical kernel. Every complete event, Fisher term and acceleration term is retained. The endpoint calculation below is used only to classify a boundary layer; it is not used to infer a compact-middle sign.

Let

`Q=11^T/3`, `P=I_3-Q`,

`A=alpha P+beta Q`, `C=I-A`,

`B=sqrt(alpha(1-alpha)) P`, `0<alpha,beta<1`,

and `K(t)=[[A,tB],[tB,C]]`. Put `s=t^2`, `delta=1-s`, and

`r=alpha(1-alpha)`, `B0=beta(1-beta)`, `d=beta-alpha`.

For every complete event write

`p_E(t)=mu_E q_E(s)`, `q_E=1-a_E s+b_E s^2`,

`v_E=a_E-2s b_E`, `z_E=(a_E-sb_E)(a_E-6sb_E)`.

The normalized complete acceleration and Fisher terms are

`A_norm(s)=2 sum_E mu_E z_E lambda(q_E)`,

`F_norm(s)=4 sum_E mu_E v_E^2/q_E`,

where `lambda(q)=log(q)/(q-1)`.

## 1. Endpoint-zero event groups

The one-block exchangeable DPP with kernel `A` assigns the same probability to every subset of a fixed size. Per subset these probabilities are

`m0=(1-alpha)^2(1-beta)`,

`m1=(1-alpha)(2alpha+beta-3alpha beta)/3`,

`m2=alpha(alpha+2beta-3alpha beta)/3`,

`m3=alpha^2 beta`.

For the complementary block `C=I-A`, the per-subset size-`k` probability is `m_(3-k)`.

At `s=1`, exactly the following complete-event groups vanish for strict `alpha,beta`:

1. the empty and full configurations, both with `q=(1-s)^2`; their total decoupled weight is
   `M2=2 m0 m3=2 r^2 B0`;
2. the twelve cardinality-one/cardinality-five configurations, split between total decoupled weights `6m3m1` and `6m0m2`;
3. six aligned middle configurations (an aligned singleton pair and its complement-swapped aligned co-singleton pair), with total decoupled weight `6m1m2`.

The first group has double order. All eighteen events in the other groups have simple order.

Let `C1=sum_(simple E) mu_E c_E`, where

`q_E(1-delta)=c_E delta+O(delta^2)`.

The cardinality-one and cardinality-five groups can be summed from the true cardinality generating determinant. The two active `P` modes have small eigenvalue `r delta+O(delta^2)` and large-eigenvalue deficit `r delta+O(delta^2)`, while the two `Q` eigenvalues are `beta,1-beta`. Hence their combined simple leading mass is

`C_ext=4 r B0`.

For one aligned singleton pair, decompose the three physical coordinates into the distinguished coordinate, the symmetric vector on the other two coordinates, and their antisymmetric difference. The antisymmetric left/right block contributes exactly `r(1-s)`. The remaining four-dimensional determinant at `s=1` is

`2[(beta-alpha)^2+r]/9`.

There are six complement-swapped aligned events. Therefore their combined leading mass is

`C_mid=(4r/3)[d^2+r]`.

Consequently

`C1=(4r/3)[3B0+d^2+r]`.                                      (1.1)

This is strictly positive throughout the open parameter square.

## 2. Exact logarithmic coefficient of the integrated acceleration

For a simple endpoint zero,

`q(1-delta)=c delta+b delta^2`, `c=1-b`,

and

`z(1)=1-5b=5c-4`.

For a double zero `q=(1-s)^2`, `z(1)=-4`, while

`lambda(q)=2 log(1/delta)+O(1)`.

Let `MZ` be the total decoupled weight of all endpoint-zero atoms. From the groups above,

`MZ=6m3m1+6m0m2+6m1m2+2m0m3`

`  =2r^2+4rB0(1-r)+(4r/3)d^2`.

The coefficient of `log(1/delta)` in `A_norm` is therefore

`L=2[5 C1-4 MZ-4 M2]`.

Substitution and simplification give the closed form

`L(alpha,beta)`

` = (8r/3)[d^2-r+3(1+2r)B0]`.                                (2.1)

Thus, for every fixed strict `(alpha,beta)`,

`A_norm(alpha,beta,1-delta)`

` = L(alpha,beta) log(1/delta)+O(1)`.                         (2.2)

This gives a genuine acceleration phase diagram. Define

`G_alpha(beta)=(beta-alpha)^2-r+3(1+2r)beta(1-beta)`.

Then `sign L=sign G_alpha`. The polynomial is a strictly concave quadratic in `beta`:

`G_alpha(beta)`

` = -2(1+3r) beta^2+(3+6r-2alpha) beta+alpha(2alpha-1)`.       (2.3)

For `0<alpha<1/2`, it is negative at `beta=0` and positive at `beta=1`, so it has exactly one root in `(0,1)` and the complete integrated acceleration tends to `-infinity` logarithmically below that root. For `1/2<alpha<1`, the complement-reflected statement holds near `beta=1`. At `alpha=1/2`, the endpoint values vanish and the interior coefficient is positive.

The symmetry is exact:

`G_(1-alpha)(1-beta)=G_alpha(beta)`.

At `alpha=1/10`, (2.1) becomes

`L(1/10,beta)=-3(127 beta^2-167 beta+4)/625`,

whose unique root in `(0,1)` is

`beta_*=(167-sqrt(25857))/254`.

This explains the previously found negative integrated-acceleration witnesses without treating them as entropy counterexamples.

## 3. The complete Fisher pole is stronger everywhere

For a simple zero, `v(1)=c`, hence

`4 mu v^2/q = 4 mu c/delta+O(1)`.

A double zero contributes only `O(1)` to this normalized Fisher scale. Summing the full simple group and using (1.1) gives

`delta F_norm(alpha,beta,1-delta)`

` -> 4 C1`

` = (16r/3)[3B0+d^2+r] >0.                                  (3.1)

Therefore, even in the open phase where `L<0`,

`Gamma=F_norm+A_norm`

has a positive `delta^(-1)` Fisher pole and only a negative logarithmic acceleration divergence. For every fixed strict `(alpha,beta)`, the true complete Shannon curvature is consequently negative sufficiently close to `s=1`.

This comparison keeps every event. It does not use a single sampled point, a probability floor, or an endpoint theorem to assert anything about the compact middle.

## 4. Consequence for the remaining proof target

The integrated acceleration is not globally nonnegative on the natural family. Its failure occupies an explicit open boundary phase, not merely an isolated rational witness. The viable whole-chord target is therefore the joint Fisher–acceleration quantity

`Gamma=integral_0^1 sum_E mu_E [4v_E^2/d_E(u)^2+2z_E/d_E(u)] du`,

`d_E(u)=(1-u)+u q_E`,

or an equivalent direct complete-curvature certificate. Pointwise acceleration positivity and pointwise rational-kernel positivity are both too strong.