# Addendum — conditional-centering compensation from fixed block marginals

Status: **PROVED (author complete proof), not independently reviewed**.

This strengthens Theorem 3.1 of `RESULT.md` without any new computation.  It uses a piece of structure that the global Cauchy estimate does not exploit: both block marginals are fixed for every radial parameter, so the first and second exterior coefficients vanish **on every conditional fiber**, not only after averaging over both blocks.

All notation is as in `RESULT.md`:

`q_s(S,T)=1-s a(S,T)+s^2 b(S,T)`, `u=q_s-1`, `y=s^2b`,

`P=E Phi(u)`, `A2=4E[y^2/q]`.

The reference law is `mu=p_A tensor p_C`.

## 1. Fiberwise coefficient cancellations

### Lemma 1.1

For every left configuration `S`,

`E_{p_C}[a(S,T)]=0`, `E_{p_C}[b(S,T)]=0`.                (1.1)

For every right configuration `T`,

`E_{p_A}[a(S,T)]=0`, `E_{p_A}[b(S,T)]=0`.                (1.2)

Hence

`E[y|S]=0`, `E[y|T]=0` under the product reference law.   (1.3)

### Proof

The left complete marginal of the true DPP is exactly `p_A` for every legal `s`. Therefore for each fixed `S`,

`sum_T p_C(T) q_s(S,T)=1`.                                 (1.4)

The left side is the polynomial

`1 - s E_{p_C} a(S,T) + s^2 E_{p_C} b(S,T)`.

It equals one on a nonempty legal interval in `s`, so both nonconstant coefficients vanish. This proves (1.1). The right marginal is fixed at `p_C`, giving (1.2) identically. Multiplication by `s^2` gives (1.3). ∎

No Markov kernel, stochastic covering, or spectral rotation is used here.

## 2. Optimal conditional centering

For a fixed strict legal `s`, define the true conditional law of the right configuration given `S` by

`P_s(T|S)=p_C(T) q_s(S,T)`.                                (2.1)

This is normalized by (1.4). Put

`m_S = E_{P_s(.|S)}[psi(u_s(S,T))]`.                        (2.2)

Similarly define

`n_T = E_{P_s(.|T)}[psi(u_s(S,T))]`.                        (2.3)

Define the two conditional fluctuation budgets

`R_S = E_mu[ q_s (psi(u_s)-m_S)^2 ]`,                       (2.4)

`R_T = E_mu[ q_s (psi(u_s)-n_T)^2 ]`.                       (2.5)

For comparison, the uncentered budget in Theorem 3.1 is

`R_0 = E_mu[q_s psi(u_s)^2]`.                               (2.6)

### Theorem 2.1 (fiber-centered full-law compensation)

At every strict legal rank-two point,

`t^2 I''(t) >= P + A2 - (1/2) sqrt(A2 R_S)`,                (2.7)

and also

`t^2 I''(t) >= P + A2 - (1/2) sqrt(A2 R_T)`.                (2.8)

Consequently

`t^2 I''(t) >= P + A2 - (1/2) sqrt(A2 R_*)`,                (2.9)

where

`R_* = min(R_S,R_T,R_0)`.                                   (2.10)

Moreover

`R_S <= R_0`, `R_T <= R_0`;                                 (2.11)

thus (2.9) is never weaker than the global Cauchy criterion in `RESULT.md`.

### Proof

By (1.3), for every function `c(S)`,

`E_mu[y psi(u)] = E_mu[y(psi(u)-c(S))]`.                    (2.12)

Weighted Cauchy--Schwarz gives

`|E[y(psi-c)]|`

` <= sqrt( E[y^2/q] E[q(psi-c)^2] )`

` = (1/2) sqrt( A2 E[q(psi-c)^2] )`.                        (2.13)

For each fixed `S`, the value of `c(S)` minimizing

`E_{p_C}[q(S,T)(psi-c)^2]`

is its mean under the normalized weight `p_C(T)q(S,T)`, namely `m_S`. Therefore the smallest budget obtainable from (2.13) by left-fiber centering is exactly `R_S`. Substitution into the accepted outer-wedge normal form proves (2.7).

The right-fiber argument is identical and proves (2.8). Taking the better valid lower bound yields (2.9)--(2.10).

Finally, conditional centering is an orthogonal projection in the finite weighted `L^2(P_s)` space, so subtracting the optimal conditional mean cannot increase the squared norm. Equivalently, expanding the square gives the finite conditional-variance identity

`R_0-R_S = E_{p_A}[m_S^2] >=0`,                              (2.14)

because `sum_T p_C q=1`; similarly

`R_0-R_T = E_{p_C}[n_T^2] >=0`.                              (2.15)

This proves (2.11). ∎

## 3. Exact checkable form

Everything in (2.4)--(2.10) is a finite complete-event expectation.  For rational `A,B,C` and rational `s`, every `q_s` is rational; only `psi` introduces logarithms, which can be outward-enclosed by the same rational atanh series used in `verify_middle_compensation.py`.

For a parameter interval, one may bound the conditional means and variances by interval arithmetic without dropping any event.  If such a full interval enclosure is expected to require long subdivision, it belongs in a bounded C2 handoff rather than an unbounded web calculation.

## 4. Why this is structurally useful

The accepted determinant-sign four-ring criterion reorganizes `W=E[b psi]` by signs of the second exterior features.  The present theorem instead exploits the **fixed marginal constraints of the actual joint DPP law**.  It therefore remains applicable when the sign rings do not stochastically order and when `W<0`.

It is also distinct from the nonreversible-generator route: (2.7)--(2.9) are identities/inequalities on the observed complete law itself and require no visible or hidden semigroup.

The theorem is still only a sufficient curvature criterion.  It does not prove the general whole chord by itself, and failure of (2.9) would not be an entropy counterexample.
