# Independent review contract for PR125

State: **PENDING_REVIEW / no verdict inherited.**

Freeze one exact PR head before review. Author proof, imported accepted matching input, external source checks, and any independent verdict must remain separate.

## U1 — complete-law parity identity

Reproduce at finite volume:

\[
P_{n,0}=P_{E_n}\otimes P_{O_n},\qquad
D(P_{n,t}\|P_{n,0})=H_n(c)-H_n(c+t g),\qquad
P_{n,-t}=P_{n,t}.
\]

Check all statements for complete occupied/vacant laws, not inclusion probabilities alone.

## U2 — occupation measurement bridge

Construct the finite gauge-invariant quasi-free state with covariance `K`, verify its occupation inclusion moments are the DPP principal minors, and use Boolean Mobius inversion to identify the full measured binary law with the complete DPP law. Then check quantum relative-entropy data processing for this fixed measurement.

## U3 — noncommuting quasi-free KL Hessian

Verify the finite-dimensional formula

\[
D_q(\rho_A\|\rho_B)=Tr[A(\log A-\log B)+(I-A)(\log(I-A)-\log(I-B))]
\]

without assuming `[A,B]=0`. Reproduce the Bregman identity and divided-difference Hessian estimate

\[
D_q(\rho_A\|\rho_B)\le [2a(1-a)]^{-1}\|A-B\|_{HS}^2
\]

when the whole segment lies in `[aI,(1-a)I]`.

## U4 — Toeplitz normalization

Check exactly

\[
n^{-1}\|T_n(g)\|_{HS}^2
=\sum_{|j|<n}(1-|j|/n)|\widehat g(j)|^2
\le\|g\|_2^2
\]

and the resulting rate upper bound. No finite-window sign is to be extrapolated.

## U5 — matching lower bound

Bind the exact already-accepted regularity-free matching statement and verify it applies under the present `L^infinity` hypotheses. Do not import response regularity from PR53/117.

## U6 — explicit non-Wiener family

Check the sign-cosine family in `reverse_audit_and_A0_barrier.md`: parity, strict margin, nonzero selected odd coefficient, and failure of Fourier `ell^1`.

## U7 — absolute-loop barrier

For symmetric nonnegative magnitude coefficients `b_j`, reproduce the even closed-loop identity, the `L^{2r}` limit, Fejer-kernel step, and conclusion that a uniform all-length absolute geometric majorant forces `sum_j b_j<infinity`. Confirm this is a method obstruction only.

## U8 — HMM source boundary

Read Han--Marcus `math/0507235` Theorem 1.1 and Tadic--Doucet `1806.09589` Assumptions 2.1--2.4 / Theorem 2.2. Confirm that neither theorem applies until an actual hidden-state Markov representation and its uniform positivity/mixing/analytic conditions have been proved for the DPP path.

## Verdict scope

A passing review may accept only the central second-difference theorem and its stated `L^infinity` scope. It must not promote the result to `C^2`, `C^4`, local concavity away from zero, whole-legal-interval concavity, arbitrary real-kernel concavity, or an entropy counterexample. Novelty is not assessed.