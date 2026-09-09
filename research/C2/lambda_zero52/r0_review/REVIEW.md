# Fresh r=0 certificate review

Reviewer scope: frozen commit `521e96c6027c14a61d60fea8e031f874ef14f1e0`, all
`|mu|<1`, `|nu|<1`, `0<u<1`, with `r=0` only.  No full-`r` sign claim is
reviewed or accepted here.

Verdict: INCOMPLETE.

I found no analytic sign error in the proposed r=0 continuation argument, but
I did not launch a fresh arithmetic checker.  My UTC clock check returned
`2026-09-09T12:07:36Z`, after the hard deadline
`2026-09-09T12:07:28Z`; the parent then confirmed the arithmetic cutoff.  So
my optional arithmetic record is: no PID launched, no remote process, no
fresh independent expansion, determinant computation, or coefficient count.

## Files read

- `research/C2/lambda_zero52/resume/R0_CANDIDATE.md`
- `research/C2/lambda_zero52/resume/outputs/r0/report.json`
- `research/C2/lambda_zero52/resume/outputs/r0/minor_4_factored.txt`
- `research/C2/lambda_zero52/resume/outputs/r0/minor_4_det.txt`
- `research/C2/lambda_zero52/resume/coefficient_outputs/r0_coefficient_report.json`
- `research/C2/lambda_zero52/resume/coefficient_outputs/r0_coefficient_table.json`
- `research/C2/lambda_zero52/structure/STRUCTURE.md`
- `research/C2/lambda_zero52/structure/POSITIVE_SEED.md`
- supporting source/status text: `resume/continue_saved_rstar.py`,
  `resume/check_det_coefficients.py`, `resume/outputs/manifest.json`,
  `compute/REPORT.md`, `formula_review/FORMULA_REVIEW.md`, and `STATUS.md`.

## What checks out analytically

The fourth determinant factor identity has the right sign once the denominator
is rewritten in terms of `J=1-u^4`.  The saved factorization is

```text
-(mu-1)^2(mu+1)^2(nu-1)^2(nu+1)^2 P
/
(2 (u-1)^5 (u+1)^5 (u^2+1)^5).
```

Since `(u-1)(u+1)(u^2+1)=u^4-1=-J`, the odd fifth power contributes one more
minus sign.  Thus this is exactly

```text
det Rstar = (1-mu^2)^2 (1-nu^2)^2 P / (2 J^5).
```

All displayed denominator and boundary factors used in this r=0 argument are
strictly positive on the open domain: `(1-mu^2)^2`, `(1-nu^2)^2`, `2`, and
`J^5`.  The Cayley substitutions

```text
mu=(X-1)/(X+1),  nu=(Y-1)/(Y+1),  u=U/(1+U)
```

biject `X,Y,U>0` with the required open domain, with positive clearing
multiplier `(1+X)^4(1+Y)^4(1+U)^16`.  Therefore, if the recorded polynomial
`Q` is indeed the exact cleared transform of `P` and all recorded coefficients
are positive, then `Q>0`, hence `P>0`, hence `det Rstar>0` everywhere in the
r=0 domain.

The structural inertia step is also sound conditional on the determinant
certificate.  `STRUCTURE.md` gives a positive two-dimensional eliminated block
and a symmetric four-dimensional Schur complement `Rstar`.  In the r=0 saved
payload, the eliminated pivots reduce to positive expressions on the open
domain, for instance

```text
dalpha = (mu^2 u^3 - u^3)/(4u^4 - 4) > 0,
dbeta  = (nu^2 u^3 - u^3)/(4u^4 - 4) > 0.
```

The domain is connected, the displayed rational matrix entries have no
interior denominator zero, and a nonzero determinant prevents any eigenvalue
of the real symmetric `Rstar` from crossing zero.  The seed file supplies a
strictly positive interior point: its scaled `Rstar` matrix is strictly
diagonally dominant with positive row margins
`10068, 88320, 88320, 40053`; the eliminated block is
`diag(1/30,1/30)`.  Thus a valid global `det Rstar>0` certificate would imply
`Rstar` is positive definite throughout the r=0 domain, and then the Schur
reduction would imply positivity of the original six-direction matrix in this
same r=0 scope.

## What I could not independently certify

The saved coefficient report records degrees `(4,4,16)`, 26 input terms, stage
term counts `85, 91, 389`, and 389 positive nonzero coefficients with minimum
`192`, maximum `99220032`, and zero negative coefficients.  The saved table
visibly lists positive decimal coefficient strings, and I found no textual
negative or zero coefficient entry in that table.  This is a file-content
check only.  It is not an independent recomputation of the Cayley expansion
and not an independent all-entry arithmetic audit.

Likewise, `continue_saved_rstar.py` reads saved `Rstar` strings and factors
their principal determinants.  The script is consistent with the stated scope,
but I did not rebuild the 4x4 Schur complement from the formulas in
`STRUCTURE.md`, nor did I recompute its determinant.  Therefore I cannot
certify, as a fresh nonauthor arithmetic fact, that the saved `Rstar` payload
and the saved residual factor `P` are exactly what the structure formulas
produce.

## Final scope

INCOMPLETE, not ERROR.  The analytic implication chain is correct conditional
on the saved exact determinant and coefficient identities.  The missing piece
for a full CORRECT verdict is a fresh independent arithmetic check of the
saved `Rstar -> det -> P -> Q` chain, especially the integer Cayley expansion
and the complete 389 positive coefficients.  No full-`r` conclusion follows;
the full-`r` transformed polynomial has mixed coefficients and remains open.
