# I05-31 continuation — rational-kernel reduction before positivity certification

Status: **AUTHOR ANALYTIC CHECKPOINT / PENDING_REVIEW; novelty NOT_ASSESSED.** Complete-configuration Shannon entropy only; the physical path is the true affine kernel path and no event, Fisher term, or acceleration term is deleted.

For the natural exchangeable family

`A=alpha P+beta Q`, `C=I-A`, `B=sqrt(alpha(1-alpha)) P`, `0<alpha,beta<1`,

write for every complete event

`p_E(t)=mu_E q_E(s)`, `s=t^2`, `q_E=1-a_E s+b_E s^2`,

`z_E=(a_E-sb_E)(a_E-6sb_E)`.

Using

`lambda(q)=int_0^1 du/[1+u(q-1)]`,

the normalized complete acceleration is

`A_norm(alpha,beta,s)=2 int_0^1 R(alpha,beta,s,u) du`,

where

`R=sum_E mu_E z_E/[1+u(q_E-1)]`.

## 1. Every denominator is strictly positive on the strict physical chord

For `0<=s<1`, the physical kernel is strict, hence every one of the 64 complete probabilities is positive. Since every decoupled weight `mu_E` is positive in the open alpha-beta square, every likelihood ratio satisfies `q_E(s)>0`.

Therefore, for every `0<=u<=1`,

`d_E:=1+u(q_E-1)=(1-u)+u q_E>0`.

Thus the sign of `R` is exactly the sign of the numerator obtained after clearing the product of these positive denominators. No likelihood floor is inserted. At `s=1,u=1`, some endpoint-zero events make individual denominators vanish; that boundary corner is excluded from this interior rational sign reduction and must be treated by its genuine endpoint order, not by continuity from a fake common floor.

## 2. Symmetry reduction

The 64 complete events form 20 simultaneous-permutation orbits indexed by `(|S|,|T|,|S cap T|)`. Complementing the complete configuration maps

`(alpha,beta) -> (1-alpha,1-beta)`

(up to swapping the two 3-coordinate blocks and a harmless diagonal sign conjugation on the cross block), so the complete entropy and rational-kernel sign problem have the corresponding paired parameter symmetry. Seven pairs of the 20 orbit representatives have identical `q`, leaving 13 generic denominator types. This is the generic two-parameter version of the 13-type alpha=1/10 table; the 11 types at beta=1/3 are additional coincidences.

## 3. Exact polynomial size at alpha=1/10

Specializing only `alpha=1/10`, each of the 13 terms reduces to a rational function whose numerator has degree at most `(4,2,0)` and denominator degree at most `(2,2,1)` in `(beta,s,u)`. Forming the common denominator by exact polynomial multiplication gives degree `(16,26,13)` with 1785 nonzero monomials. The cleared common numerator simplifies to degree `(18,24,11)` with 1932 nonzero monomials.

These counts are structural bookkeeping, not a positivity claim. They show that a direct symbolic factorization is unnecessarily large but an exact tensor Bernstein certificate is finite and moderate. The intended certification coordinates near the singular corner are `(beta, delta=1-s, v=1-u)` so that endpoint order is visible rather than hidden by cancellation.

## 4. Scope

This checkpoint proves denominator positivity and a finite exact reduction only. It does **not** claim `R>=0`, does not infer middle curvature from endpoint concavity, and is not an entropy counterexample. If a negative rational-kernel point is found, it must first be given as an exact rational `(alpha,beta,s,u)` point; then the `u` integral and finally the full Fisher-plus-acceleration curvature must be tested before any entropy conclusion.