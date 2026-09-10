# I05-30: moving rank-two endpoints, complete atoms and two exclusion theorems

Research successor: [issue #84](https://github.com/randomcat4/dpp-entropy-tools/issues/84), original #21/agent24/accepted PR62. Submission: [Draft PR #86](https://github.com/randomcat4/dpp-entropy-tools/pull/86).

Branch `i05-30/rank2-atoms-dilute-20260910` was created from main at `65e59a46b49cd2dbb5c779a4cfae8cef26441984`. The pre-existing `i05/rank2-moving-support-20260910` branch was compared to main and had no changes to recover. It was not modified. Only this directory is added; no main file or other author's branch is overwritten.

## Final verdict, separated by object

| Object | Verdict in this author session | Exact scope |
|---|---|---|
| Physical-coordinate rank-two endpoint event formula | PROVED, author proof | Four-coordinate family EAE^T and VBV^T; all sixteen complete atoms, all pair interference, triple and quadruple terms; actual arithmetic midpoint |
| Endpoint relative off-diagonal sign | PROVED, author proof | At fixed diagonals, absolute off-diagonal entries and angles, opposite signs increase midpoint entropy relative to aligned signs; strict if the transfer amount is positive |
| Full-strength continuous two-angle exclusion | PROVED, author proof with executed rational logarithm bounds | Fixed A=[[2/5,6/25],[6/25,2/5]], B=[[3/5,9/25],[9/25,3/5]], every real t1,t2 in [0,1/50]; G>19/1000; both support-intersection geometries; small common bit-flip interiors also covered |
| Rank-two extension of the PR62 mixture-to-midpoint bridge | DISPROVED, method only | Two exact noncommuting moving rank-two pairs have H(p_mid)<H((p_-+p_+)/2) but G>0; both signs persist after common epsilon=1/100000 bit flips |
| Fixed-chord common-intensity exclusion | PROVED, author proof | Every fixed distinct pair of real positive contractions X,Y in finite dimension has G(lambda)>0 for all sufficiently small lambda>0; explicit all-event remainder and equal-diagonal strict second-order coefficient |
| Unrestricted full-intensity moving rank-two endpoints | INCOMPLETE | No proof for all real rank-two endpoint pairs and no strict real entropy counterexample |
| General strong-correlated multiring middle / multiple boundaries | INCOMPLETE | Existing #61 remains a separate computational/theoretical problem |

Here G=H(actual midpoint)-average endpoint entropy. The counterexample-oriented Jensen difference is J=-G. Every entropy is the complete configuration Shannon entropy with natural logarithms, not inclusion-minor entropy, particle-count entropy or quantum entropy.

**Independent review: PENDING_REVIEW / REQUESTED.** These are not accepted main theorems. Local exact arithmetic was executed by the author and is not independent verification. No independent job is called RUNNING without an issue claim. Novelty, priority and formal verification are unassessed.

## Files and proof order

Read `rank2_atoms_and_angular_box.md` first. It gives the legal parameter family, degeneracies, all minors and all complete atoms, exact endpoint entropy, the checked four-event sign-transfer proof, continuous angular box, rigorous method counterexamples and sign-preserving common interior lift. It also compares the two primary-source-backed mechanisms.

Then read `dilute_chord_theorem.md`. This proof was completed and added AFTER PR86 was opened as a checkpoint, in the same task. The new result removes the apparent small-intensity logarithmic singularity using the exact expected-cardinality identity; it proves strictness even when the endpoint diagonals agree and supplies a finite all-event third-derivative bound. This is a new explicitly labeled subtheorem, not a silent weakening of the original target.

`certify.py` verifies the canonical family; `certificate.json` stores the rational inputs, all sixteen atoms of each three-kernel fixture, full affine midpoint jets, complete Fisher and acceleration, and bounded entropies. `certificate_stdout.txt` is an annotated execution record, not a byte-identical raw terminal transcript.

`dilute.py` verifies the two dense equal-diagonal rank-two examples and all-event remainder constants; `dilute_certificate.json` stores their exact q-polynomials and certificates. `dilute_stdout.txt` preserves the corresponding printed result records. In q-polynomial dictionaries, omitted sets are exactly algebraically zero; the program checks every one of the sixteen sets before omitting an identically zero polynomial. In the canonical atom and jet dictionaries, all sixteen sets, including zeros, are stored explicitly. Empty set is encoded by the empty string.

## Reproduce without a search or a new tool project

Author environment: Python 3.13.5, SymPy 1.14.0; only SymPy and standard-library rational arithmetic are needed. From the repository root, run without Python's `-O` flag:

```sh
python research/N4/I05_30_20260910/certify.py
python research/N4/I05_30_20260910/dilute.py
```

Each script regenerates its JSON. To check the archived data, copy the JSON files aside first and compare their parsed JSON objects after regeneration; whitespace formatting is not mathematical content. All decisive logarithms use N=48 rational atanh terms with an explicit geometric remainder, and all printed endpoints use exact integer outward rounding. No mpmath decimal decides a sign. The two scripts are narrow fixture verification, not a reusable scan framework or optimizer.

## What was personally checked

The accepted PR62 statement, its original proof and SECOND review were read; only the rank-one theorem and its recorded small bit-flip scope were treated as accepted. Main `docs/research_status.md` and `docs/route_ledger.md`, plus agent24's original README, source audit, failure ledger, multiring fixture and event code, were read before extending the route.

The two mechanisms in the initial checkpoint are structurally distinct. Mixed-minor algebra followed by a four-COMPLETE-event odds transfer proves the relative-sign theorem and produces the method failure. A physical-coordinate marginal/drop coupling with a classical entropy continuity bound proves the entire explicit angle box. The later dilute proof uses neither bridge: it derives analytic complete-law coefficients and proves strict convexity of their pair penalty.

Primary-source audit: HKPV, *Determinantal Processes and Independence*, arXiv:math/0503110, Definition 3 and Theorem 7; and Audenaert, arXiv:quant-ph/0610146, classical equations (11)-(12), TV normalization and logarithm convention. Relevant PDF pages were read and screenshotted. The former is only DPP mixture background, not an affine-kernel entropy theorem; the latter is used only through the classical probability-vector specialization, also proved directly by a coupling argument here. No quantum entropy substitutes for configuration entropy. These sources do not establish novelty of the new statements.

## Failure ledger and repairs

1. The universal rank-one-style bridge H(p_mid)>=H(average endpoint law) was tested, then rigorously refuted for rank-two endpoints. Both witnesses have positive actual G. Only that method implication is rejected.
2. Splitting each rank-two endpoint into two rank-one terms does not justify adding PR62 inequalities: it loses the mixed pair term and new triple/quadruple events. That purported deduction was not used.
3. First-order dilute analysis alone fails when diag X=diag Y: its Jensen coefficient is exactly zero. The strict second-order Psi coefficient and full Taylor remainder are what close this case.
4. A tentative angular margin target 1/50 failed the exact assertion: the derived bound is about 0.01967182197, below 0.02. The statement was corrected to 19/1000 and rerun. No stronger margin is claimed.
5. An initial diagnostic wrapper summed symbolic Boolean values and raised a BooleanAtom TypeError; it was repaired before obtaining the diagnostic values. All decisive signs were subsequently recomputed with rational log enclosures, not inferred from that failed run.
6. During publication, one stored dilute JSON temporarily acquired a spurious whitespace key, and one canonical empty-event probability temporarily acquired a singleton-array type instead of a scalar string. Both transcription errors were repaired in subsequent visible commits. The generated local certificates were unaffected. Review should compare parsed saved JSON to fresh regeneration, not assume that an upload is automatically a verification.
7. The old agent24 full-multiring rational atanh interval attempt had denominator growth and did not finish; that old failure is not claimed repaired here. Its 110-digit samples are not promoted to interval-family results. No broader random scan was launched.
8. Positive full-intensity G in the two fixed dense equal-diagonal examples does not prove a full-intensity family or permit enlarging their certified all-lambda intervals. The canonical angle box is not all moving physical frames. The dilute radius depends on the fixed endpoint pair and does not exclude pairs changing with lambda.

## Exact remaining obligations and machine contract

The aligned-sign canonical expression for G in `rank2_atoms_and_angular_box.md` remains unresolved outside the stated angle box for general parameters. The rank-four determinant and nonnegative mixed minors alone do not determine the complete logarithmic entropy difference. Arbitrary physical rank-two endpoint pairs not belonging to this canonical family remain unresolved at full intensity, as do n=5,6 full-intensity extensions and multi-scale moving multiple-boundary constructions.

For the independent strong-correlated 3+3 route, the existing [issue #61](https://github.com/randomcat4/dpp-entropy-tools/issues/61#issuecomment-5611722108) now has an explicit resumption request: unchanged exact A,C,B; all 64 atoms and full Fisher; continuous compact-middle coverage plus an explicit simple-endpoint overlap, or a true certified counterexample; 90 CPU minutes / one process / 8 GiB; outward-rounded logs; saved unresolved subdivisions; explicit stop/resume conditions. This is a delegated potentially >60-minute job, not an assertion of execution. It is REQUESTED, not presumed started. No result in this packet depends on that job.
