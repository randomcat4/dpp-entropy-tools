# S2 finite-evidence backlog closeout

Date: 2026-09-11 (Asia/Singapore).  This report is arithmetic/evidence review
only.  It does not reassess analytic proofs, novelty, or merge suitability.

All new executions were local because the remote runner was unavailable.
Heavy checks were serialized.  Each ran at Windows `BelowNormal` priority on
one logical CPU unless explicitly stated otherwise; BLAS/OMP helper threads
were limited to one and GPU use was disabled.  Peak working sets remained far
below 8 GiB.

## Verdict table

| PR | Exact reviewed head | Primary status | Precise scope |
|---|---|---|---|
| 136 | `39098dac760cea2d27f2955bed31f80c87913810` | **PASS** | Fresh 128-node finite certificate plus frozen and independent exact audits; analytic C2 proof excluded. |
| 112 | `2ea07741114aa7cd20210dfc84becda378381e7b` | **FAIL** for historical checker | Earliest defect is the retired recurrence at `t=1/2,n=4,mask=1`; separate new reconstructions below do not rehabilitate the historical artifact. |
| 98 | `55649309437a78d9e5174386d8d260a4ee9c02a1` | **PASS: DATA_RESTORATION_ONLY** | Exact parsing and write/read equality of archived trials; no curvature or residual certificate. |
| 97 | `03e0313a5802bfe52fba18fa01bf5ad97ab20d2f` | **PASS** | Fresh full-square, strong-chord, strong-family, and axis/wedge arithmetic runs. |
| 86 | `bd12e6094e098499fae7e01729a4b29f021a14e2` | **SUPERSEDED** | Exact successor is PR97 head `03e0313a5802bfe52fba18fa01bf5ad97ab20d2f`, which restores and freshly passes the missing full-square evidence. |
| 120 | `83b89e8b9b4c542e5d1cd8b38b64b7ff2449ad41` | **PASS** | Fresh 1024-box compact unequal-middle exact fixed-point certificate. |
| 124 | `344723af6affab240c9f87c395d4e8c1b7b19f6d` | **SUPERSEDED** for requested correspondence check | Exact merged successor PR132 head `6370ca1ae64cfc9e58c491568445f02fadcf0a71`; no duplicate rerun. |
| 94 | `a9db9f98dc6dac766dd9b214f056ee9b30109b23` | **PASS** | New independent standard-library reconstruction of the explicit 3+3 local-channel arithmetic only; whole-chord scope excluded. |
| 104 | `d980dbb04840bd21e6c62cf88ffd45a9b0d1b4f8` | **PASS** | New independent rational reconstruction of the displayed half-leaf witness and both method criteria. |
| 116 | `3f276c09fe4da3aded2ab6cf457adb7fdc4254d8` | **FAIL** for one frozen checker; bounded subunits split below | Two frozen checkers and the independent finite/light units pass; `check_endpoint_phase.py` exits 1 at a structural-equality assertion; the missing Bernstein certificate remains evidence-insufficient after a capped attempt. |

## PR136 continuation

The detailed continuation is in the preceding PR139 commit
`6069e0a30c82bc4cb4044ed0d01af55650a062bd`.  The fresh production output has
128 unique rows, each with `4^9` future words and all four current outcomes.
It ran with two threads on two logical CPUs in 66.315 seconds wall / 109.359
seconds CPU, peak working set 5,799,936 bytes, and reported
`stopped=0 failed=0`.

The frozen author checker and the independent Fraction audit both passed.  The
independent audit made 512 saved/fresh interval-intersection checks.  The four
true curvature upper bounds are

```text
-0.0003746944028546811
-0.0010306469749631383
-0.0019577212125145367
-0.0031712104741915452
```

all strictly below `-1/3000`.

## PR112 historical failure and new bounded reconstructions

The current exact-head entry point has blob
`41a1b4cdcc40b49359ff8ec0a8e8a422eb270cc1` and deliberately exits 1 as
`RETIRED_KNOWN_FAILING`.  The fresh diagnostic at blob
`b77eed233f1db0d4bb37b29070cd14704d4877be` reproduced the earliest defect:

```text
old recurrence       65823/1048576
signed determinant   65055/1048576
Mobius reconstruction 65055/1048576
old error             3/4096
```

Changing only the exchanged first-component labels gives the direct mass, but
this one case is not a repaired full checker.  The withdrawn wide certificate
therefore remains withdrawn.

Two genuinely new and separately labelled results are available:

1. PR136 proves the stronger same-family interval `[1/2,3/2]`, which contains
   the old `[49/40,51/40]` target.  This is a new mathematical reproduction,
   not recovery of the historical PR112 run.  The previously accepted narrow
   PR112 scope is also recorded at merged PR134 head
   `4bf6e3adc940816d3f8b925addb45e1a58f11c99`.
2. `independent_section6.py` reconstructs formulas (1)--(2) directly with
   Fraction jets.  It verifies the first shortcut derivative
   `34799/67076100>0`; exactly matches displayed second derivative (19) and
   finite gap (20); and proves both epsilon endpoints are in the exact cone
   interior with all four branch weights positive.  The historical cited
   `exact_lift_check.py` is absent at the reviewed head, so this result is
   explicitly `PASS_NEW_RECONSTRUCTION_HISTORICAL_CHECKER_ABSENT`.

## PR98 data integrity

The frozen parser blob is `3e5b11d95712294762ec5bfb358e5a1cf4b93096`.
A new parse/write/parse run exited 0 in 0.346 seconds with a 16,130,048-byte
peak working set.  Degree 6, 8, and 10 records contain 83, 164, and 285
monomials and 252, 495, and 858 reported coefficient slots, respectively.
The source ZIP was unavailable and therefore `original_zip_numeric_equality`
is `NOT_CHECKED`.  No NumPy scout was rerun, and the result remains data
restoration rather than a mathematical certificate.

## PR97 and PR86 repair

Fresh source-bound runs at PR97 head passed:

- `certify_full_square.py`, blob
  `3f10ea554718be34fb5161f2046bc1d08a83f520`: 4096 rational boxes,
  minimum lower bound `0.012067200390564330`, 23.195 seconds wall,
  81,285,120-byte peak working set.
- `certify_strong_chord.py`, blob
  `a12e60ac83b231bb6bbec669ada3cc49a3b14819`: 32 boxes on each half,
  global `H''` upper bound about `-0.8592619332`, 7.029 seconds wall,
  74,477,568-byte peak working set.
- `certify_strong_family.py`, blob
  `553ac1fee9d729524f812a0620b8083bed74db65`: 512 boxes on each half
  (1024 total), `H''<-1/2`, 12.951 seconds wall, 78,938,112-byte peak
  working set.
- `audit_axis_wedge.py`, blob
  `dec3f77f9d561ce928ba1479b4a9ec343813ad41`: fixed cases, exact angular
  replay, rank-3/4 rectangle, and direct complete laws passed in 2.304 seconds.

PR86 omitted the generated full-square certificate.  PR97 states and enforces
that its restored full-square checker is copied from frozen PR86 and adds the
missing evidence, so the PR86 evidence status is superseded rather than
retroactively passed.

## PR120 compact unequal-middle square

The exact checker blob is `23c63f99c59ce97f130fcc1ba6d2c65561c29c5d`.
A fresh run covered all `32 x 32 = 1024` boxes using 140-bit outward
fixed-point arithmetic, 44-bit rational preconditioners, and 56-term positive
atanh log tails.  It exited 0 in 3.802 seconds wall / 2.969 seconds CPU with a
16,310,272-byte peak working set.  The exact scaled minimum Gershgorin margin
was positive and its decimal value was `0.11829569483797094`.

## PR94 explicit 3+3 channel arithmetic

Author source blobs were bound as follows:

- `exact_core.py`: `d9dcdcd013e4928c66daf4a6cfdfd3dea479d592`;
- `fixtures.py`: `eee0398b45a10c81cab57eaeaa8409ed2ea9e9ab`;
- `verify_channels.py`: `9594dd6f9c547b3c33914b29bed808044a1f1a4e`.

The new `independent_pr94.py` uses only standard-library Fraction arithmetic,
its own polynomial determinant and matrix routines, and no author import.  It
exited 0 in 4.671 seconds wall / 3.953 seconds CPU with a 14,483,456-byte peak
working set.  It checked:

- asymmetric selectors `(5/8,1/5,2/5)` and `(3/8,1/9,2/9)`;
- all 16 refined affine polynomial identities;
- both sets of 64 actual observed-mode event laws;
- every entry of the displayed 3+3 matrices;
- exact determinant polynomials and the maximal endpoint
  `49/6-sqrt(4657)/15` strictly in `(3,4)`, with the other constraint still
  positive at 4;
- all eight conditional laws at `s=1/2`, zero conditional Fisher derivatives,
  and a rigorous negative fiber interval (upper endpoint approximately
  `-1.4067686435e-5`);
- the coefficient `337/202500`;
- the six nonzero original-frame pair minors
  `[[17191/250000,-121/500000,-90217/500000],`
  `[655143/1000000,-327003/1000000,-536007/1000000]]`.

This closes only the explicit local-channel arithmetic identified by the prior
structural review.  PR95 whole-chord evidence was not rerun.

## PR104 half-leaf method witness

The author source blob is `2fd4998b94987f3e35a84e93f0a25c9419dc19b4`.
The new independent script reconstructs the complete-event determinant
polynomials without author imports.  It checked 168 eight-event jets across
the six basis and fifteen pair directions, including exact normalization;
proved strict `K` and `I-K`; obtained an old parallel-gap upper bound about
`-0.8407635409`; obtained a common-diagonal-gap lower bound about
`0.3743163927`; and proved all six leading Sylvester determinant lower bounds
strictly positive.  The successful run took 20.567 seconds wall / 17.938
seconds CPU with a 14,843,904-byte peak working set.

The first attempt reached all mathematical assertions but exited 1 only while
serializing exact fractions larger than Python's default 4300-digit display
limit.  The retry changed only output summarization and passed.  Both attempts
are retained.

## PR116 final frozen head

The final reviewed head is
`3f276c09fe4da3aded2ab6cf457adb7fdc4254d8`.  The three frozen checker blobs
are:

- `verify_exchangeable.py`:
  `cef80d7242b73b026b2acea4f687ea25cbe398ef`;
- `certify_integrated_acceleration_negative.py`:
  `49a34653cffc11d94225dab7a2f54331ff0317c3`;
- `check_endpoint_phase.py`:
  `0466005cdda761220aa76b7f397d1b10dbbbf45e`.

Fresh single-core runs of the first two exited 0.  The exchangeable checker
reconstructed 64 events, 11 groups, and reserve `195191/1755000` in 2.650
seconds wall with a 61,550,592-byte peak working set.  The endpoint-scale
checker proved `-127/1000<A_norm<-126/1000`, `F_norm>10^99`, and positive
`Gamma` for `alpha=1/5,beta=1/200,delta=10^-100` in 0.605 seconds wall with a
15,155,200-byte peak working set.

The third frozen checker exited 1 at line 43.  It compares two algebraically
equal expressions with SymPy structural `==` rather than simplifying their
difference.  This is the precise earliest checker defect.  The source status
is still **FAIL** even though the following independent algebra verifies the
underlying formulas.

`independent_pr116_light.py` rebuilt the 64 events and generic 13 types without
author imports, then passed all of these bounded units in its final source-bound
run in 5.074 seconds wall / 4.531 seconds CPU with a 65,122,304-byte peak
working set:

- 64-event/11-type exchangeable table and reserve `195191/1755000`;
- exact negative rational-kernel point at
  `alpha=1/10,beta=s=999/1000,u=1`, with
  `R=-19828.13763706689...`,
  `6.9381648836224339<A_norm<6.9381648836224341`,
  `F_norm=847.7432215357995...`, and `Gamma>0`;
- two direct 64-signed-determinant cardinality checks at
  `(alpha,beta,s)=(1/10,2/7,1/4)` and `(1/5,3/11,9/16)`, each matching all 16
  bivariate cardinality cells and the equal/unequal formulas for `(1,1)`,
  `(2,2)`, `(1,2)`, and `(2,1)`;
- the full-parameter `C_A` and `C_F` identities and the `alpha=1/10` slice.

`independent_pr116_moments.py` independently rebuilt the general 64 events / 13
types symbolically.  It verified the three closed forms `M_a,M_ab,M_b`, their
`alpha=1/10` specializations, and the exact factor used for `M_b<=1`.  It also
verified all three boundary-ray leading coefficients directly from the type
table, the two-scale acceleration coefficient `612/625`, and the rational
`f0/f1` formulas and endpoint value `36/25`.  Its first attempt failed on the
auditor's own false assumption that a simultaneous two-scale logarithmic limit
equals the fixed-`beta=1` endpoint coefficient.  The retry instead computed
each likelihood's epsilon-vanishing order and passed in 41.651 seconds wall /
37.156 seconds CPU with a 74,899,456-byte peak working set.

The claimed tensor Bernstein certificate is **EVIDENCE_INSUFFICIENT**.  The
reviewed tree has no generator or coefficient artifact.  A new independent
attempt rebuilt the 13 symbolic types and started exact common-numerator
construction, but SymPy had not completed the first expansion when the agreed
600-second wall cap fired.  The process was terminated at 600.298 seconds wall
/ 531.766 seconds CPU; it used one thread and peaked at 1,547,706,368 bytes.
No degree/count/minimum assertion was reached.  The minimum remaining contract
is therefore explicit: materialize the common numerator and independently
check multidegree `(18,24,11)` and 1932 power monomials, transform all 5700
tensor coefficients on the stated affine box, then compare the minimum integer
to
`27030487060546875000000000000000000000000000000000000`.

The separate six-hour joint-kernel Bernstein exploration was not started.

## Failure and nonclaim ledger

- PR136 independent attempt 1 rejected the auditor's own endpoint-monotonicity
  handling at `cos(pi)`; the corrected exact endpoint identity was rerun and
  passed.  This is retained in PR139's first commit.
- PR136 Windows build attempt 1 stopped at POSIX-only `sys/resource.h`.
  The author source stayed byte-identical; a telemetry-only compatibility
  include plus external memory monitoring was used for the passing build.
- PR104 independent attempt 1 failed only during oversized integer-to-string
  output, after all mathematical assertions passed; the retry passed.
- PR112's historical checker remains invalid and its wide certificate remains
  withdrawn.
- PR116's frozen endpoint checker exits 1 at its structural-equality assertion;
  the independent simplification PASS does not overwrite that source failure.
- PR116's independent boundary-ray attempt 1 used an invalid interchange of
  limits; it is retained, and the corrected per-type retry passed.
- PR116's missing Bernstein certificate remains evidence-insufficient after
  the full 600-second bounded reproduction attempt described above.
- PR98 has no original-ZIP comparison in this run and is not a mathematical
  certificate.
- No analytic proof, novelty claim, or merge decision is made anywhere in
  this closeout.
