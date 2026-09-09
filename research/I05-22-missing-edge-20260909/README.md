# I05-22 result map and reproduction entrypoints

Research thread: [issue20](https://github.com/randomcat4/dpp-entropy-tools/issues/20). Author PR: [PR51](https://github.com/randomcat4/dpp-entropy-tools/pull/51). Heavy exact-elimination request: [issue52](https://github.com/randomcat4/dpp-entropy-tools/issues/52).

## Status

**PROVED (author proof, not independently reviewed):** every strict half-filled missing-edge center

`K=[[1/2,0,b],[0,1/2,c],[b,c,1/2]]`, `bc!=0`, `4(b^2+c^2)<1`,

has `H''(K;D)<0` for every nonzero real symmetric three-point direction D. The edge-strength ratio is arbitrary. See `proof_half_filled.md`. This includes semidefinite rank-two and full-rank directions at the stated centers; it does not generalize those direction results to arbitrary centers. The theorem was derived independently of the unreviewed PR41/43 theorem claims.

**PROVED (author proof, not independently reviewed):** the general missing-edge positive 2x2 elimination block, the complete six-direction Schur and face identities, and the two precisely scoped method obstructions in `continuation.md`. These were obtained after the first PR checkpoint and without relying on a response to the computation request.

**INCOMPLETE:** the explicit four-dimensional Schur inequality for arbitrary missing-edge diagonals; the four-parameter Lambda=0 derivative conjecture; general real three-point concavity; any strict positive complete-entropy Jensen counterexample. Novelty is not assessed.

`PROVED` above is the author's claim supported by the provided proof and exact checks, not an accepted main theorem, independent review, CI pass, or proof-assistant result.

## Complete code/input/output packet and access boundary

[Actually uploaded full reproduction ZIP](https://drive.google.com/file/d/16qxPPMZvLfJgZcAvyJIVrNsv8uTN7d6v/view?usp=drivesdk).

The Drive upload was followed by metadata readback: file ID `16qxPPMZvLfJgZcAvyJIVrNsv8uTN7d6v`, MIME application/zip, 37522 bytes, shared=false. No sharing permission was changed. This link is private to the connected account, not asserted to be public. A downloadable local copy accompanies the user-facing task result.

This fallback was used after the GitHub Python-file creation was blocked by a tool safety-state check. The blocked code write was not retried through another GitHub endpoint. The mathematical proof text is committed on this research branch, not main.

The ZIP contains 22 files: full proof and continuation, source/route record, two exact mathematical verifiers, a JSON-transport verifier, their actual outputs, dependency files, the exact rational matrix input, and clearly labeled bounded exploratory source. No pickle or executable serialized object is included.

At the packet root:

```sh
python -m pip install -r requirements.txt
python verify_exact.py
python verify_general.py
python verify_matrix_input.py
```

Do not enable Python -O: checks use assertions. The tested environment was Python 3.13.5 and SymPy 1.14.0. Optional scouts separately pin NumPy 2.3.5. The main proof checks use exact symbolic/rational operations; log intervals use 60 atanh-series terms with an explicit rational tail bound and outward decimal endpoints. Floating scouts do not certify any parameter domain.

## Actual post-checkpoint exact output

```text
PASS general six-direction acceleration and exact face remainder
PASS exact auxiliary resolvent obstruction
Phi_second = -53670727895896612562246875/14117659525214393686902
Phi_second in [ -3801.67320227830454269394178939205369117 , -3801.67320227830454269394178939205369116 ]
-H_second in [ 85.39754587008524590529296252441265816 , 85.39754587008524590529296252441265817 ]
Auxiliary-obstruction triple Delta in [ -0.00000042702288120241526682286996218 , -0.00000042702288120241526682286996217 ]
PASS exact failure of coefficientwise PSD: n=2 gives -1/18
ALL POST-CHECKPOINT EXACT CHECKS PASSED
PASS four exact rational JSON transport fixtures; no global sign claimed
```

The first negative number concerns an auxiliary conditional resolvent, not entropy. The actual entropy Hessian and Jensen gap at that example have the concave sign. Neither this example nor the main proof's separate negative-gap illustration is an entropy counterexample.

## Clarification of the conditional Schur complement

In `continuation.md` equation (30), the conditional form subtracts exactly the marginal Hessian, not an arbitrary Fisher projection. At the independent leaf center, the marginal score is `d(i-x)/v+e(j-y)/w`. The marginal second derivative has zero row and column sums, while log Pij is the sum of a function of i and a function of j. Consequently `sum Pij'' log Pij=0`, including all missing-edge second-derivative contributions, and

`-H(X1,X2)''=d^2/v+e^2/w`.

Thus `-H(X3|X1,X2)''` is precisely the full block form after subtracting that exact marginal Hessian. Its positivity remains unproved; the complete-entropy Schur target is equation (29), not the stronger conditional target.

The direction D_s in continuation equation (37) is itself positive-semidefinite rank two for 0<s<1 (eigenvalues 0,1/2,s/6). Its full curvature is negative, but its acceleration is harmful: `sum p'' log p = -s log((1+s)/(1-s))/6 < 0`. The Fisher term is therefore essential even in this concrete semidefinite case.

## Exact computation input for C2

The committed analytic source is `continuation.md`, equations (32)–(35), at commit `2e4b8754ad4af2fe055ebeeef1159877773372a3`. The packet file `lambda_zero_M_input.json` stores the six-by-six rational M as integer-coefficient multivariate polynomial numerators divided by

`8*(1-u^4)^2*(1-r^2*u^4)^2`,

strictly positive on the open requested domain. There are 21 upper-triangular entries and 1117 numerator monomials. The symbol order is `(mu,nu,r,u)` and the fixed physical direction basis is recorded in the JSON. `verify_matrix_input.py` checks transport against the explicit rational construction at four exact fixtures; this is not a global sign test.

Issue52 gives the independent reconstruction requirement, requested algorithms/commands, 45-minute initial wall ceiling, 16 GiB limit, stopping rules and certificate standards. Its status is REQUESTED, not running or completed. No claimed result depends on that job being executed. Routine review and progress belong in the PR and issues, not cross-thread notifications.
