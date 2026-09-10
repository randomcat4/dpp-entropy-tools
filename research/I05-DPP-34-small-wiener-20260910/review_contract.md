# Independent review contract

State: **UNCLAIMED / PENDING_REVIEW until an explicit issue claim or assignment appears.**

A reviewer must freeze one exact PR head before starting. Earlier PR39/PR53/PR82/PR106 review labels do not transfer to the new proof.

## U1 — theorem scope and legal interval

Verify

```text
r_c=sum_{m!=0}|c_hat(m)| < delta=min(mu,1-mu)
```

and the choice of `tau` with `R=r_c+tau||g_hat||_1<delta`. Check the pointwise/spectral margin for every real `|t|<=tau`, including real non-even symbols.

## U2 — complete atom factorization

For every finite coordinate set and complete word, reproduce

```text
p_t(x)=q_mu(x) det(I+B_x A_t)
```

with the correct vacant-site signs. Verify `A_t` has zero diagonal, `||B_xA_t||<=R/delta<1`, the trace-log branch, disappearance of the `m=1` term, and the uniform volume/event bound.

## U3 — local complete-event derivatives

Audit the complete-event coercivity and Jacobi/Bell-polynomial bound

```text
|partial_t^r p_{J,t}(x)|
 <= p_{J,t}(x) K_r |J|^r,
0<=r<=4.
```

Check that summing against a bounded local observable uses `sum_x p_x=1` and does not introduce `2^|J|`. Confirm that rare atoms and both Fisher/acceleration contributions remain present.

## U4 — closed-walk derivative majorant

Expand each trace into closed walks. Reproduce the anchored convolution estimate for derivatives placed on edge coefficients and the local-expectation derivative estimate. Verify a uniform majorant of the form

```text
C_r m^(2r) rho^(m-r), rho<1,
```

including repeated vertices, supports of size at most `m`, all index shifts, and the finitely many cases `m<r`.

## U5 — differentiated thermodynamic limit

For interval restrictions of the infinite stationary DPP, verify that each fixed translated walk expectation is exactly the corresponding marginal expectation, the proportion of allowed anchors tends to one, and dominated convergence applies through derivative order four. Check that the resulting series is the actual entropy-rate KL to the product Bernoulli law.

## U6 — parity mutual information

Verify complete-event evenness, fixed even/odd marginals, center independence, and

```text
h(c)-h(c+t g)=d(P_t||P_0)=I_t(E;O)>=0.
```

This must be an entropy-rate identity for complete laws, not an inclusion-probability statement.

## U7 — matching and two-case calculus

Check the exact accepted PR53 matching coefficient and both cases:

```text
J''(0)>0,
J''(0)=0 with J(t)=A t^4+o(t^4), A>=2 alpha_k.
```

Verify local strict negativity of the corrected second derivative and no assumption that the quadratic coefficient vanishes.

## U8 — explicit no-positive-moment family

Check convergence of

```text
w_n=1/[n(log(n+2))^2],
```

divergence of every positive weighted moment, parity support, strict mean-`1/3` norm margin, failure of all `A_p`, `p>0`, and separation from the accepted mean-one-half and exponential scopes.

## Alternative-source audit

Read Bressaud--Fernandez--Galves and Fernandez--Maillard only to confirm the packet's non-application claim: their coupling/uniqueness mechanisms do not by themselves supply the required `C^4` entropy response under a zero-moment `A_0` tail. Confirm that the rejected Dobrushin A1/A2 import is not reintroduced.

## Budget, stop, and recovery

This source/proof audit may exceed 60 minutes. Suggested budget: 120 minutes, no numerical work. At the earliest invalid load-bearing step, stop dependent conclusions and publish:

- exact frozen head;
- earliest failed equation or theorem premise;
- whether the defect is local or fatal;
- last completed unit and exact next equation for recovery.

If all units pass, issue an `ACCEPTED_SCOPED` report with exact quantifiers and exclusions. Separate author proof, accepted imported matching lemma, external source checks, machine evidence (none), universal theorem, and novelty. Novelty is **NOT_ASSESSED**. Creating the issue alone is not a review start.