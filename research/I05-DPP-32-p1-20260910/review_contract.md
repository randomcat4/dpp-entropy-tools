# Independent audit contract for I05-DPP-32

State: **UNCLAIMED / PENDING_REVIEW**.

A request or this file does not start an audit.  A reviewer must explicitly
claim a frozen commit in the GitHub issue.

## Claims to decide

### T1 — local corrected concavity

For every `p>=1`, strict-margin real half-period-even `c in A_p`, nonzero real
half-period-odd `g in A_p`, and every odd `k` with `g_hat(k)!=0`, decide whether
there is a nonempty symmetric interval on which

```text
h(c+t g)+|g_hat(k)|^4 t^4/[8 mu^2(1-mu^2)]
```

is concave for the true stationary DPP configuration entropy rate of the
physical affine kernel.

### T2 — centered Fisher expansion

For every `p>=1/2` under the same hypotheses, decide whether

```text
h(c+t g)=h(c)-I_s(0)t^4/2+o(t^4)
```

with `I_s(0)` equal to the full one-sided conditional Fisher information in
`s=t^2`.

T2 is not a local-concavity claim for `p<1`.

## Required units

### U1 — norm-controlled family inversion

Check Fang--Shin Theorem 2 with

```text
Lambda=Z x N, p_alg=1, q_alg=2, d=2, r=p>0.
```

Verify relative separation, the direct-sum BGS norm, uniform `l^2` inverse
bound for every complete-event block, and that applying the theorem once to
the direct sum really yields

```text
sum_m (1+|m|)^p sup_event |M_event^{-1}(i,i-m)| < infinity.
```

Do not interchange a post-hoc supremum with an infinite sum.

### U2 — complex disk and two-leg moment

Reproduce the algebra Neumann disk, the leg convolution, rank-one flip, and

```text
sum_j (1+j)^(2p) beta_j < infinity.
```

Check the corrected terminal-site effective coupling `a+a*d*a`, non-null
logarithm, full-future Schur limit, Cauchy derivatives and parity factorization.

### U3 — BFG and moment Poisson maps

Use the printed BFG ratio condition, matched-suffix inequality and first-return
law.  Reproduce the defective renewal summability and the first-disagreement
estimate proving

```text
R:V_1 -> V_0,
R:V_0 -> C.
```

No generic “summable variation implies C2 response” citation is acceptable.

### U4 — second response

Starting from

```text
(nu_u-nu_s)F=nu_u(L_u-L_s)R_sF,
```

rederive both response orders and moving-observable terms.  Check uniform time
tails and continuity at the endpoint `p=1`, including the outer Poisson term.

### U5 — true entropy bridge

Check DPP cylinder continuity, invariance of the full-future conditional,
`h_s=-nu_s log G_s`, fixed parity marginals, `D'(0)=0`, and the accepted PR53
matching coefficient.  Verify the calculus yielding

```text
h''(t)=-12 A t^2+o(t^2).
```

### U6 — one-response Fisher theorem

For `p>=1/2`, check `V_0` membership, the formula

```text
D'(s)=nu_s[U_s R_s(ell_s-ell_0)],
```

normalization `L_sU_s=0`, collapse `R_0U_0=U_0`, and the coefficient
`I_s(0)=nu_0(U_0^2)`.  Confirm that no neighborhood concavity is inferred for
`1/2<=p<1`.

### U7 — exact method obstruction

Check the constant-center complete-event score calculation and the sparse odd
Fourier examples.  Classify it only as a moment-space mechanism obstruction,
not an entropy counterexample.

### U8 — source and evidence separation

Confirm that PR82's old FIRST/SECOND do not transfer, Dobrushin A1/A2 is not
used, Fernandez--Maillard and Tanaka are scope checks only, numerical evidence
is absent, and novelty is not assessed.

## Stop and resume conditions

At the earliest load-bearing failure, stop dependent units and report the exact
equation, whether a local repair is possible, and the last passed unit.  If all
units pass, publish a version-bound `ACCEPTED_SCOPED` report with exact
quantifiers and exclusions.  This is a source/proof audit; no arithmetic server
job is required.  A changed head must be rebound explicitly.
