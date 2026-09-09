# Machine notes: PR58 corridor independent source

Prepared an independent finite verifier source at `research/C2/pr58_corridor50/implementation/independent_pr58_certificate.py`.

Scope:

- Frozen source commit: `1770ed29e8487b8f39aebb4c9466406c7493e580`.
- Public claim: `https://github.com/randomcat4/dpp-entropy-tools/issues/50#issuecomment-5604628245`.
- Included objects: original RESULT section 4 fixture, the four rational corridor intervals `[3,9]`, `[8,12]`, `[11,14]`, `[14,15]`, and the `s=10` W/true-curvature sign checks.
- Excluded objects: `a4f05cc` joint-additive material, the different `s=9/10` fixture, issue63 whole-chord work, theorem review, novelty review, and Lean work.

Implementation summary:

- The verifier parses literal rational `A,C,U,V` from `inputs/RESULT.md` and constructs `B=UV^T`.
- It reconstructs all 64 complete-event determinant polynomials directly from the 6x6 kernel `K(t)` over `QQ[t]`, using only standard-library `Fraction` arithmetic and a permutation determinant.
- It derives `pA`, `pC`, `mu=pA*pC`, and each `q(t)=1-a*t^2+b*t^4` from those direct event polynomials, then checks normalization and global/fiber cancellations.
- It verifies Mobius principal and complementary minor identities as exact polynomial equalities, so positivity of all complete events on the corridor certifies legality through exact finite sums.
- It computes corridor extrema by endpoints plus rational vertices and applies the displayed `Psi`, `M2lower`, `left`, and squared-margin inequality with exact rational comparisons.
- At `s=10`, it checks the frozen exact value `min q = 121400093597/249280204050`, encloses each `log(q)` with a one-sided signed rational atanh tail, and sums the W interval and true scaled curvature interval from rational endpoints.
- The true curvature is reconstructed first from derivatives of `p=mu*q`, then checked against the displayed `u,y` normal form. The s10 output also records per-left and per-right derivative log-coefficient cancellations explaining why the `log(mu)` terms drop.

Run boundary:

- I did not run the verifier, Python, SymPy, CAS, or remote arithmetic.
- The source never reads, imports, or executes `author_checker_reference.py`.
- The source reads `author_output_reference.txt` only after independent reconstruction. The downstream exact-fraction comparison requires all 26 frozen corridor values: `Amax`, `Bmax`, and for each of `[3,9]`, `[8,12]`, `[11,14]`, `[14,15]`, the `qminus`, `qplus`, `Psi`, `M2`, `left`, and `squared strict margin` fractions. It also compares the s10 `min q` fraction. The comparison record is written before any mismatch failure is raised.
- Rounded decimal displays are not promoted to exact outward endpoints.
- Runtime options are `--input-root`, `--out`, and `--wall-seconds`; wall time is capped at 2700 seconds and additionally bounded by `C2_ABSOLUTE_DEADLINE_EPOCH` when present.
