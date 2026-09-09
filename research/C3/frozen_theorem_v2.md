# Frozen statement v2 — I05-C3-20260909

Status: AUTHOR CANDIDATE, independent audit required. This version enlarges only
the precisely scoped radial theorem from v1; the full conjecture stays open.

## Definitions and quantifiers

For every integer n>=1, every diagonal matrix B=diag(b_1,...,b_n) with
0<b_i<1, and every fixed Hermitian matrix A (its diagonal need not vanish),
put J={t in R: 0<=B+tA<=I}. For K in this interval let X_K be the binary
configuration law with P(S subset X_K)=det K_S and
H(K)=-sum_x P(X_K=x) log P(X_K=x), using 0 log 0=0.

**T-finite:** t -> H(B+tA) is concave on the entire interval J, including its
feasible boundary. The matrix A need not commute with B.

For every p in (0,1) and every fixed bounded measurable real function g on
R/Z, let I={t in R: 0<=p+t g<=1 almost everywhere}. Define the scalar
stationary DPP with K_f(i,j)=integral f(theta)exp(2 pi i(i-j)theta)dtheta,
and h(f)=lim_n H(K_f|[1,n])/n in natural logarithms.

**T-rate:** t -> h(p+t g) is concave on I, including feasible boundary symbols.
No zero-mean, evenness, smoothness, bandwidth, finite-dependence, uniform
margin for boundary symbols, or entropy-rate differentiability is assumed.

## Proof interface and prohibited substitutions

The proof must establish that independent replacement of each binary variable
by an independent Bernoulli target is exactly the claimed affine DPP family.
Finite event laws must be used; cardinality entropy and quantum entropy are
not substitutes. Rate Jensen inequalities must pass through pointwise finite
entropy limits, without differentiation under a limit.

## Scope and meaning

This covers fixed scalar chords lying on a line through a constant symbol,
and arbitrary finite rays through an interior diagonal kernel. It does not
cover all scalar chords or all affine directions at an arbitrary finite K.
It is a partial continuous-family theorem, not resolution of Lyons–Steif
Conjecture 9.2. Novelty is unconfirmed. Proof and audit contexts may not change
or supplement these hypotheses.

Proof and verification instances must not change these hypotheses.

## Change from v1

The restrictions diag(A)=0 and integral(g)=0 are removed after the author
derived a general product-reference relative-entropy identity. No assumptions
are silently weakened inside an existing proof. The initial v1 is retained.
