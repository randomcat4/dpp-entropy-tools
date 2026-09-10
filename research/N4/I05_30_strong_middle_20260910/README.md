# I05-30 successor: repaired evidence and a strong-middle full-chord family

Base: `main@8f4acd31d0ce4d37defafbfcff22fa2b21356f72`. This successor does not alter the frozen PR86 head `bd12e6094e098499fae7e01729a4b29f021a14e2` or frozen PR88 head `6c8ad2eaedcc93c7dfc5417b2d71b4e826d9be5c`.

All entropies are natural-log Shannon entropies of the complete finite DPP law

\[
p_K(S)=\sum_{T\supseteq S}(-1)^{|T|-|S|}\det K_T,
\qquad\det K_\varnothing=1,
\qquad0\log0=0.
\]

Every chord and midpoint is affine in the physical kernel `K`. Every curvature statement keeps

\[
H''=-\sum_S(p'_S)^2/p_S-\sum_Sp''_S\log p_S.
\]

## Current review boundary

The latest bounded PR88 review accepts, within its restricted analytic scope, the full rank-two mixed-minor bookkeeping, the whole-chord theorem for an indefinite rank-two direction supported on three actual coordinates, the common-mode specialization and the fixed-affine multiple-boundary asymptotic. PR88 finite values remain source-only/pending machine review.

The latest PR86 FIRST accepts its analytic complete-event/sign identities, qualitative fixed-pair dilute theorem, thinning-star theorem and disjoint actual-coordinate-block theorem. Its angular, edge, diagonal, fixed-square, fixture, Fisher and lift values remain source-only pending independent arithmetic. The review also identified one absent promised output and a stale top-level map.

All new mathematics in this successor is **author proof, PENDING_INDEPENDENT_REVIEW** unless an inherited reviewed result is explicitly named. No novelty or priority claim is made.

## 1. PR86 evidence and navigation repair

`pr86_evidence_repair.md` maps every one of the 18 frozen PR86 files to its theorem, verifier, certificate and review gate. This successor also supplies:

- `certify_full_square.py`, copied from the frozen source;
- `full_square_certificate.json`, the previously absent generated result;
- `full_square_stdout.txt`, the bounded author execution record.

The exact 4096-box rerun reports

```text
minimum G lower = 0.012067200390564330
minimum box = (63,63)
```

and therefore supports the source-level fixed-family claim `G>1/100`. It remains an author certificate; the missing-file repair does not substitute for the requested independent server reconstruction.

## 2. Axis-to-wedge publication after comparison with PR88

`axis_wedge_extension.md` corrects the scope of the previously local packet. Its matched-Schur common-coordinate statement is a specialization of PR88's broader reviewed three-actual-coordinate theorem, not a new main result. The new quantitative specialization is

\[
G\ge b^2s^4/2.
\]

The genuinely additional author result opens away from that codimension-one surface using exact complete-event diagonal transfer and finite Möbius total variation. For its fixed rational rank-two endpoints it proves:

- common-line rank-three directions, `|q|<=3/100`: `G>3/100`;
- zero-intersection rank-four directions, `0<=t_2<=1/10`: `G>3/100`;
- `|q|<=1/5000`, `0<=t_2<=1/10`: `G>1/100`;
- `|q|<=1/1000`, `0<=t_2<=1/20`: `G>3/50`.

The proof, script, exact certificate and stdout are all present. This result is still a continuity opening around a reviewed safe axis and does not settle a strongly mismatched middle.

## 3. Exact strong-correlated full chord

`strong_middle_full_chord.md` moves outside the matched-Schur, three-coordinate, small-angle and dilute regions. It fixes two rank-two endpoint kernels with

- disjoint moving support planes;
- direction rank four and inertia `(2,2)`;
- endpoint spectra `(3/100,9/10)` and `(3/20,17/20)`;
- Schur mismatch `8485397/29294395`, approximately `0.28965`.

At the full-rank midpoint, the affine acceleration is rigorously positive:

\[
\mathcal A(1/2)\in
[0.091509816433464862273171837567186173,
 0.091509816433464862273171837567255234].
\]

The singleton layer alone contributes about `+4.82927` to acceleration, so the dangerous mechanism is real and is not produced by deleting high-cardinality events. Nevertheless, exact endpoint factorization and 32 rational boxes on each half give

\[
\mathcal A(t)<41/20.
\]

A physical-coordinate occupancy bit gives the complete-Fisher lower bound

\[
\mathcal F(t)>57/20.
\]

Therefore the entire true chord satisfies

\[
\boxed{H''(t)<-4/5\quad(0<t<1).}
\]

This is a whole-chord exclusion, not a collection of negative samples. The direct all-event midpoint gap is about `0.8552870432`, but the theorem already follows from the curvature bound.

## 4. A full strong endpoint-strength family

`strong_middle_family.md` then varies the second endpoint's high logical eigenvalue over

\[
\lambda\in[4/5,9/10]
\]

while retaining the same disjoint support geometry, low eigenvalue, rotations and first endpoint. Across this interval:

- every endpoint remains rank two and strongly anisotropic;
- every direction remains rank four with inertia `(2,2)`;
- the Schur mismatch remains above `0.287`;
- the full-rank midpoint acceleration remains strictly positive:

\[
0.0193877652773012600<\mathcal A(1/2,\lambda)
<0.166254091468359866.
\]

All complete event determinants are affine in `lambda` because the endpoint change is rank one. Exact tensor-product Bernstein arithmetic covers 512 boxes on each half of the chord. It proves

\[
\mathcal A(t,\lambda)<239/100,
\qquad
\mathcal F(t,\lambda)>289/100,
\]

and hence

\[
\boxed{H''(t,\lambda)<-1/2}
\]

for every `0<t<1` and every `4/5<=lambda<=9/10`. Thus every member has true midpoint gap greater than `1/16`.

This answers the natural-family branch of the strong-middle question: positive acceleration persists on a nontrivial endpoint interval, but complete Fisher controls the full chord uniformly.

## 5. Exact files and reproduction

| File | Role | Present status |
|---|---|---|
| `pr86_evidence_repair.md` | complete frozen-PR86 theorem/evidence map | publication repair |
| `certify_full_square.py` | frozen fixed-square generator | author source |
| `full_square_certificate.json` | formerly missing 4096-box output | PENDING_SERVER_REVIEW |
| `full_square_stdout.txt` | bounded repair run | author output |
| `axis_wedge_extension.md` | rank3/rank4 continuity regions | PROVED_BY_AUTHOR |
| `audit_axis_wedge.py` | exact all-event checker | author source |
| `audit_axis_wedge_certificate.json` | exact wedge and local audit values | author output |
| `audit_axis_wedge_stdout.txt` | bounded wedge run | author output |
| `strong_middle_full_chord.md` | one exact strong full-chord theorem | PROVED_BY_AUTHOR |
| `certify_strong_chord.py` | exact endpoint-factor/full-Fisher checker | author source |
| `strong_middle_certificate.json` | all 16 event polynomials, layers and boxes | author output |
| `strong_middle_stdout.txt` | bounded fixed-chord run | author output |
| `strong_middle_family.md` | complete endpoint-strength interval theorem | PROVED_BY_AUTHOR |
| `certify_strong_family.py` | two-parameter Bernstein checker | author source |
| `strong_family_certificate.json` | family factors, margins and row summaries | author output |
| `strong_family_stdout.txt` | bounded family run | author output |
| `failure_ledger.md` | stopped routes, implementation failures and remaining mechanism | preserved limitations |

Run, without Python `-O`:

```sh
python certify_full_square.py
python audit_axis_wedge.py
python certify_strong_chord.py
python certify_strong_family.py
```

The scripts use exact SymPy determinants and rational interval arithmetic. The strong-family checker uses tensor-product Bernstein coefficients and 192-bit directed fixed-point `atanh` logarithms with an explicit tail. There is no numerical probability floor, random optimization, omitted event, spectral-entropy substitution, `L`-affine path or quantum entropy.

## 6. Final scope of this unit

The following are now **PROVED by author, PENDING_REVIEW**:

1. explicit rank3/rank4 regions opening away from a reviewed three-coordinate rank-two axis;
2. one strongly correlated, substantially Schur-mismatched disjoint-support rank-two chord with `H''<-4/5` everywhere;
3. a nontrivial endpoint-strength interval of such chords with `H''<-1/2` everywhere, even though midpoint acceleration is positive throughout the family.

The unrestricted moving-rank-two problem remains **INCOMPLETE**. The present family has a large visible diagonal direction entry, so one actual occupancy bit forces a large Fisher lower bound. The remaining serious freedom is a strong rank-four direction whose diagonal entries—and ideally all midpoint derivatives of low-order inclusion statistics—are simultaneously small. No entropy counterexample has been obtained. The PR62-style endpoint-law mixture bridge remains a method counterexample only. Novelty remains unassessed.
