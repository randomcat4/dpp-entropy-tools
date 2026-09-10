# I05-31 — full two-parameter endpoint phase for acceleration and Fisher

Status: **AUTHOR ANALYTIC PROOF / PENDING_INDEPENDENT_REVIEW; novelty NOT_ASSESSED.** This note concerns the complete-configuration Shannon law of the true affine physical-kernel path. Every complete event, Fisher term and acceleration term is retained. It refines the endpoint mechanism inside the natural two-parameter family; it is not used to infer any compact-middle sign.

Let

`Q=11^T/3`, `P=I_3-Q`,

`A=alpha P+beta Q`, `C=I-A`,

`B=sqrt(alpha(1-alpha)) P`, `0<alpha,beta<1`,

and `K(t)=[[A,tB],[tB,C]]`. Put `s=t^2`, `delta=1-s`, and `r=alpha(1-alpha)`. For every complete event,

`p_E(t)=mu_E q_E(s)`, `q_E=1-a_E s+b_E s^2`,

and write

`A_norm=2 sum_E mu_E (a_E-sb_E)(a_E-6sb_E) lambda(q_E)`,

`F_norm=4 sum_E mu_E (a_E-2sb_E)^2/q_E`,

where `lambda(q)=log(q)/(q-1)`.

## 1. The four endpoint-zero likelihood groups

Set

`L=2 alpha+beta-3 alpha beta`,

`N=alpha+2 beta-3 alpha beta`,

`G=alpha(1-alpha)+(beta-alpha)^2`.

All four quantities `L,N,G,r` are positive in the open parameter square. The complete-event orbit calculation has three simple endpoint-zero groups and one double group. Their total original decoupled weights, with no deletion or renormalization, are

`W_H=2 alpha^2(1-alpha) beta L`,

`W_L=2 alpha(1-alpha)^2(1-beta) N`,

`W_M=(2/3) r L N`,

`W_D=2 r^2 beta(1-beta)`.

The double group has

`q_D=(1-s)^2`.

The three simple groups have

`q_i=(1-s)(1+c_i s)`,

with endpoint slopes `kappa_i=1+c_i` given by

`kappa_H=2(1-beta)/L`,

`kappa_L=2 beta/N`,

`kappa_M=2G/(LN)`.

For completeness, the corresponding second factors are

`c_H=(1-alpha)(2-3beta)/L`,

`c_L=alpha(3beta-1)/N`,

`c_M=r(2-3beta)(1-3beta)/(LN)`.

These formulas follow directly by taking the P-compressions of the shifted complete-event matrices. For example, in a full-versus-size-two group one P direction has product eigenvalue one, while the other has eigenvalue `-(1-alpha)(2-3beta)/L`; the other formulas follow by complementation and by the aligned singleton calculation. The remaining complete likelihoods have positive endpoint limits.

## 2. Exact logarithmic phase of the integrated acceleration

For a simple group, as `delta ->0+`,

`lambda(q_i)=log(1/delta)+O(1)`,

`(a_i-sb_i)(a_i-6sb_i)=5 kappa_i-4+O(delta)`.

For the double group,

`lambda(q_D)=2log(1/delta)+O(1)`,

`(a_D-sb_D)(a_D-6sb_D)=-4+O(delta)`.

Therefore

`A_norm(alpha,beta,1-delta)`

`= C_A(alpha,beta) log(1/delta)+O(1)`,

where

`C_A=2 sum_(i=H,L,M) W_i(5 kappa_i-4)-16W_D`.

Exact simplification gives

`C_A=(r/3) S(x,y)`,

`x=2alpha-1`, `y=2beta-1`,

`S(x,y)=7+x^2-7y^2-4xy+3x^2 y^2`.                 (2.1)

Equivalently,

`C_A=(8r/3) P(alpha,beta)`,

where

`P=2alpha^2-alpha+3beta-2beta^2+4alpha beta`

`  -6alpha^2 beta-6alpha beta^2+6alpha^2 beta^2`.

Thus the complete integrated acceleration is not sign-definite in this natural family. For fixed `alpha<1/2`, it diverges to `-infinity` when `beta` is sufficiently close to zero; for fixed `alpha>1/2`, the complementary negative phase occurs when `beta` is sufficiently close to one. At `alpha=1/2`, `S=7(1-y^2)>0` throughout the strict beta interval.

For fixed `x!=0`, the phase boundary inside the relevant side of `-1<y<1` is the unique admissible root of

`(3x^2-7)y^2-4xy+(7+x^2)=0`.                    (2.2)

The two algebraic roots are

`y=[2x +- sqrt(49-10x^2-3x^4)]/(3x^2-7)`;

exactly one lies in the side adjacent to `y=-1` when `x<0`, or to `y=1` when `x>0`. The complement map `(alpha,beta)->(1-alpha,1-beta)` sends `(x,y)->(-x,-y)` and preserves (2.1).

At `alpha=1/10`, (2.1) reduces to

`C_A=(3/625)(-127 beta^2+167 beta-4)`,

which recovers the explicit sign-loss slice.

## 3. Exact Fisher pole and safety of the true curvature

Only the three simple groups contribute a `delta^-1` Fisher pole. Since `v_i(1)=kappa_i`,

`F_norm(alpha,beta,1-delta)`

`= C_F(alpha,beta)/delta+O(1)`,

with

`C_F=4 sum_(i=H,L,M) W_i kappa_i`.

Substitution gives the strictly positive closed form

`C_F=(16r/3)[3beta(1-beta)+G]`                  (3.1)

`   =(16alpha(1-alpha)/3)`

`     *[3beta(1-beta)+alpha(1-alpha)+(beta-alpha)^2] >0`.

The double group has bounded Fisher and is fully retained; all endpoint-positive groups contribute only `O(1)`.

Consequently, for every fixed strict `(alpha,beta)`,

`Gamma=F_norm+A_norm`

`= C_F/delta+C_A log(1/delta)+O(1) -> +infinity`.             (3.2)

Thus even in the region `C_A<0`, where the **complete integrated acceleration itself** tends to `-infinity`, the true complete Shannon curvature remains favorable because the full Fisher pole is one order stronger. This is a precise acceleration-method counterexample, not an entropy counterexample.

Equation (3.2) is only an endpoint classification. It neither proves nor assumes the sign on a compact strict middle, and it does not replace the general accepted endpoint theorem by an interior assertion.