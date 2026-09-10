# Reverse audit and independent-review contract for the strict L-infinity quartic-rate theorem

Status: **AUTHOR SELF-AUDIT / PENDING INDEPENDENT REVIEW.**

This file audits `quartic_rate_theorem.md` backwards from the `Theta(t^4)` conclusion. It does not constitute an independent verdict.

## A. Thermodynamic step

The theorem does not differentiate an entropy-rate limit. For each fixed sufficiently small real `t`, the finite parity identity is exact:

```text
D(P_(Lambda,t)||P_(Lambda,0))
 = H_Lambda(c)-H_Lambda(c+t g).
```

The even- and odd-coordinate marginals are fixed in `t`, and at `t=0` the parity blocks are independent. Divide by `|Lambda|` and take the ordinary stationary entropy-rate limit. The finite bound is uniform in volume, so the `O(t^4)` constant passes directly.

Review obligation A1: verify that no derivative/limit interchange is hidden here.

## B. Forward, not reverse, KL

At a current physical `s=t^2`, define

```text
A_s=Q(I-sQ)^-1.
```

The exact identity

```text
I+sA_s=(I-sQ)^-1
```

gives

```text
p_0/p_s=det(I+sA_s).
```

Therefore

```text
D(P_s||P_0)=-E_s log det(I+sA_s).
```

The expectation is under the current full complete law `P_s`; this is the desired forward KL. No inequality reversing the KL arguments is used.

Review obligation B1: check the determinant orientation and signs, including vacant-event determinant signs.

## C. Current-law score cancellation

The original exact family is

```text
p_u/p_0=det(I-uQ).
```

Differentiating at `u=s`,

```text
partial_u log p_u|_s=-Tr[Q(I-sQ)^-1]=-Tr A_s.
```

Since `sum_x p_u(x)=1`,

```text
E_s Tr A_s=0.
```

Thus when the trace-log for `log det(I+sA_s)` is inserted into the forward KL, the entire `m=1` term cancels under the actual current law.

Review obligation C1: verify that this uses `P_s`, not `P_0`, and that differentiation is finite-dimensional before any thermodynamic passage.

## D. Nonnormal matrices

Neither `Q` nor `A_s` is assumed normal. The proof uses only:

```text
||Q|| <= delta^-2 ||B||_op^2,
||(I-sQ)^-1|| <= (1-s||Q||)^-1,
```

and, when `||sA_s||<1`, the operator-norm power series for `log(I+sA_s)`. The branch is the one continued from the identity; for real physical `s`, the exact determinant ratio `p_0/p_s` is positive, so its trace equals the ordinary real logarithm of that likelihood ratio.

For `m>=2`,

```text
|Tr(A^m)|
 <= ||A^(m-1)||_HS ||A||_HS
 <= ||A||_op^(m-2)||A||_HS^2.
```

No eigenvalue ordering, simultaneous diagonalization, or absolute spatial walk expansion is used.

Review obligations D1-D2: reproduce the nonnormal log branch and Schatten inequality.

## E. Hilbert--Schmidt extensivity

For every complete word,

```text
Q=C_v^-1 B* A_u^-1 B.
```

Thus

```text
||Q||_HS
 <= ||C_v^-1|| ||B||_op ||A_u^-1|| ||B||_HS
 <= delta^-2 ||g||_infinity ||B||_HS.
```

Toeplitz compression gives

```text
||B||_HS^2
 <= sum_(i,j in Lambda) |g_hat(i-j)|^2
 <= |Lambda| sum_d |g_hat(d)|^2
 = |Lambda| ||g||_2^2.
```

This uses Parseval (`g in L^infinity subset L^2`) and not the Wiener sum `sum |g_hat(d)|`.

Review obligation E1: verify the parity compression cannot increase this Hilbert--Schmidt sum.

## F. Uniform physical interval and constants

Set

```text
C0=delta^-2 ||g||_infinity^2.
```

Require both physical legality and

```text
sC0<=1/4.
```

Then

```text
||A_s|| <= (4/3)C0,
||A_s||_HS <= (4/3)||Q||_HS,
s||A_s||<=1/3.
```

Consequently the trace-length sum starts at `m=2` and is bounded by one geometric series with constants independent of the complete word and volume. The displayed coefficient `(4/3)delta^-4 ||g||_infinity^2||g||_2^2` is sufficient, not claimed optimal.

Review obligation F1: check every numerical factor `4/3`, `16/9`, and `3/4` in the final bound.

## G. Lower bound and exact order

For nonzero half-period-odd `g in L^infinity`, Parseval implies some odd Fourier coefficient is nonzero. The only imported theorem is the already accepted regularity-free parity matching floor

```text
h(c)-h(c+t g)
 >= (1/2)d_Ber(mu^2-|g_hat(k)|^2t^2 || mu^2).
```

Its Taylor coefficient is strictly positive. Combined with the new `O(t^4)` upper bound, this gives `Theta(t^4)`.

Review obligation G1: independently check the binary-KL coefficient and that no response regularity from PR53/117 is imported.

## H. Fisher and acceleration boundary

The finite Shannon curvature identity remains

```text
H''(t)
 = -sum_x (p_x'(t))^2/p_x(t)
   -sum_x p_x''(t) log p_x(t).
```

At `t=0`, every `p_x'(0)=0` pointwise, but the theorem does not infer the rate result by deleting the acceleration term. Instead it uses the exact full KL likelihood and current-law normalization before taking any limit. Thus Fisher and acceleration are retained in their exact net contribution.

Review obligation H1: confirm that the trace-log reorganization is an equality of the complete forward KL and not a sign claim about either curvature summand.

## I. Source boundary

Dierckx--Fannes--Pogorzelska, arXiv:0709.1061, is relevant background for fermionic quasi-free states and information-theoretic quantities. It is not load-bearing for the new quartic theorem. PR125's quantum-relative-entropy data-processing upper bound is likewise not used to prove `O(t^4)` here.

Review obligation I1: do not substitute quantum/spectral entropy for occupation Shannon entropy when auditing this PR.

## J. Exact nonclaims

No claim is made of:

- `C^2` or `C^4` entropy-rate response outside `A_0`;
- a punctured-neighborhood curvature sign or local concavity from the value bound;
- whole-legal-interval concavity;
- general real finite-kernel concavity;
- a finite-HMM representation;
- novelty, optimal constants, machine verification, or computation.

A review should stop at the earliest failed load-bearing equation and report whether the defect is local or fatal. No numerical work is required.