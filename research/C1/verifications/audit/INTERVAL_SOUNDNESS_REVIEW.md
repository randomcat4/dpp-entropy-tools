# C1 non-author audit: interval soundness integration note

STATUS: CORRECT

Reviewed source: `runs/C1/repo/research/C1/main/interval_soundness.md`, SHA256 `28474B6A781255E762661EDDAEC6F6406D53AC99CB24D163331F845363B45899`.

Scope: I checked only whether this short explanatory note matches the actual frozen certificate implementation and the rerun certificate output. I did not treat the note as a new theorem proof and did not modify the main package.

## Code consistency checks

The note's description of exact outward interval arithmetic matches `runs/C1/children/mechanism/scripts/sparse_rational_certificate.py`:

- dyadic outward rounding to multiples of `2^-620` is implemented by `I.DEN=2**620` and floor/ceiling construction at lines 148-160;
- addition, negation, multiplication, and division with denominator-zero exclusion are implemented at lines 162-190;
- the 110-term atanh log enclosure and the tail bound are implemented at lines 124-145;
- positive interval input to log is enforced at lines 228-232;
- decimal fields are outward-rounded by decimal floor/ceiling at lines 193-207;
- interval event probabilities and symmetric coordinate derivatives, including off-diagonal cofactor doubling, are computed at lines 243-253;
- N, its determinant, the adjugate formula, `Htilde=dM`, `a=d eta`, `beta sqrt(Z)=g^T h`, and `d alpha=a^T h` are assembled at lines 274-320;
- the family-level strictness check for `K>0`, `I-K>0`, and connected positive q is at lines 323-333;
- endpoint signs, whole-bracket `d alpha<1`, positive atom lower bound, positive N leading minors, pivot exclusion, and residual containment are required for success at lines 336-365 and 400-417.

The note correctly distinguishes the role of floating bisection: it proposes a rational bracket, while certified endpoint signs and whole-bracket inequalities are recomputed by rational interval arithmetic. It also correctly states that residual containment is only a consistency check; the substantive nonsingularity evidence is pivot exclusion together with the positivity arguments.

## Caveat carried from certificate review

This soundness note is consistent with the certificate arithmetic, but it does not remove the provenance detail found in `SPARSE_CERTIFICATE_REVIEW.md`: the stored certificate corresponds to the narrow `2^-62` q-bracket reproduced with explicit `--cert-steps 60`; the script's current default `--cert-steps 24` does not reproduce the stored certificate. That is a command/provenance caveat, not an interval-soundness flaw.

No critical inconsistency was found between `interval_soundness.md`, the certificate code, and the audited certificate output.
