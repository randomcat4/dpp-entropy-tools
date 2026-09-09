# Verification and publication boundary

Status: author-side exact algebra and rational interval computation completed. **Not independently reviewed.** No CI run or proof-assistant certification is claimed.

## Entry points

- `proof_half_filled.md`: exact quantified theorem and complete proof.
- `sources_and_routes.md`: repository freeze, primary literature, load-bearing identity audit, failed routes and remaining gap.
- Python verifier: [actual uploaded Drive file](https://drive.google.com/file/d/1Me4juAQJSyA3PZvYwzHm05iBfdr2-Vo1/view?usp=drivesdk).

The attempted GitHub creation of `verify_exact.py` was blocked with: “OpenAI could not determine the request's safety state.” The code was **not** pushed using a different GitHub API as a workaround. Following the user's explicit fallback instruction, `I05-22_verify_exact.py` was actually uploaded to the connected Drive account. Read-back confirmed file ID `1Me4juAQJSyA3PZvYwzHm05iBfdr2-Vo1`, MIME `text/x-python`, size 5996 bytes, and `shared=false`. No permissions were changed. Reviewers without access to that account will need the task's local artifact package; this private Drive link is not claimed to be publicly accessible.

Save the uploaded file as `verify_exact.py`. Requirements: Python >=3.10 and `sympy==1.14.0`. Run without Python's `-O` option:

```sh
python -m pip install sympy==1.14.0
python verify_exact.py
```

## Actual author output

```text
Python 3.13.5 SymPy 1.14.0
PASS full eight-event cofactor identity and PR43 rank-two carrier
PASS PR41 general missing-edge score map and nonzero Jacobian
PASS half-filled probabilities, odd scores and complete Fisher
PASS full 4x4 derivative determinant, seed minors and G(0)
PASS exact three-kernel legality and negative Jensen illustration
Delta in [ -0.00413603603307918499086949813852939 , -0.00413603603307918499086949813852938 ]
ALL EXACT CHECKS PASSED
```

The run completed within the short local computation budget. There is no outstanding heavy computation or claimed server job.

## What was independently reconstructed within this author session

The verifier imports no PR41/43 code. It enumerates inclusion determinants, performs complete Möbius inversion, and obtains each first/second affine coefficient. It checks the general cofactor/cycle carrier, the symmetrized rank-two adjugate identity, the missing-edge conditional quotient derivatives and Jacobian, half-filled atoms, odd scores, full Fisher, the four-dimensional derivative determinant and seed principal minors. These symbolic checks support algebraic identities on their formal domains, not independent review of the analytic proof.

The legal three-kernel example is rational and its natural logarithms are enclosed using 60 terms of an atanh series with a rational geometric-tail bound, power-of-two reduction, sign-aware interval operations and outward decimal rounding. The example's Jensen gap is strictly **negative**, not a counterexample. Its sign is not used as evidence for the universal theorem.

## Requested independent review scope

First verify (3), (6), (8)–(10), the change T=sqrt(1-r^2)R, and the determinant/seed identities (14)–(15). Then review the order of quantifiers in the inertia argument: for each fixed s, move r through (-1,1); only afterward fix r and integrate in s. Check strictness, the connected-center requirement bc!=0, the axis continuity statement, and the absence of any arbitrary-chord claim.

A nonauthor implementation should reconstruct the eight events afresh and check the explicit rational matrix (13), rather than only rerun the author script. Finite test kernels do not establish the two-parameter theorem. Ordinary review coordination belongs on PR/issue #20, not cross-thread messages.
