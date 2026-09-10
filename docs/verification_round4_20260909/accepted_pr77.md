# PR77 — accepted scoped fixed-harmonic true-rate certificates

Status: **ACCEPTED_SCOPED**. Original/successor analytic FIRST and isolated SECOND, the exact Section9/output-disclosure narrowing, and actual independent PR89 finite FIRST/isolated SECOND are complete. C3 read the full reports and mathematical/implementation sources, and verified source/output bindings without repeating mathematical computation.

## Frozen sources and exact object

Original author head `6ebe38dc6503120d47e9d644cfac78cfb43666f5` contains18files. Successor `8de8b0007f9374b7a5decb9b0a2f1c939fe897be` adds5files without changing those18. Final `2564e25a8b62a72992b9451988cd42e2d5a81834` changes only README and proof Section9; the other21files remain identical. C2's inputs remain the original frozen object, not a moving successor.

The scalar symbol is

`f_t(theta)=1/2+(1/4)cos(4*pi*theta)+(t/8)cos(2*pi*theta)`.

The Toeplitz kernel has diagonal1/2, first off-diagonal `t/16`, second off-diagonal1/8. The source proves a strict legal spectral margin throughout `|t|<=3/2`. All entropies below are classical Shannon entropy of the complete occupation law with natural logarithms; `h(t)` is its stationary entropy rate. The finite numerical object is exactly `t=1/2,1,3/2`, conditioning depth18 and full event lengths18,19.

## Accepted mathematical units

- Complete-event determinant and conditional Schur formulas, configuration-uniform inverse/locality bounds, entropy-tail comparison and the fixed finite-depth-to-true-rate Jensen bridge. The quantitative constants used in this bridge are separately reconstructed by PR89 PhaseA.
- Normalized one-sided conditional/RPF/Poisson response formulas retaining Fisher, acceleration and measure-response terms. This is an exact interface, not a sign proof obtained by discarding response terms. The finite-memory curvature-tail mechanism and its three point-specific disks/tails are accepted in their stated source scope.
- The fixed true-rate midpoint certificate:
  `h(1)-[h(1/2)+h(3/2)]/2 > 1/10000`.
  The directed lower endpoint recorded in raw evidence begins `0.000274641906326566768831869...`; the exact strict threshold above is the accepted claim. Only the midpoint entropy-tail budget is subtracted for this lower-bound certificate.
- Three fixed true-rate curvature certificates:

  | Parameter | Accepted strict bound |
  | --- | --- |
  | `t=1/2` | `h''(1/2)<-1/2500` |
  | `t=1` | `h''(1)<-1/1000` |
  | `t=3/2` | `h''(3/2)<-1/500` |

  Each uses its own finite interval and point-tail radius. The parity gauge transfers the corresponding fixed statements to negative parameters; this does not interpolate between points.
- The full-Fisher score projection and exact covariance polynomial
  `V(t)=561/2048-17*t^2/4096-3*t^4/65536`, with
  `I(t)>=t^2/[16384*V(t)]>=16/286141` on `1/2<=|t|<=3/2` in the source's Fisher-rate setting. PhaseA independently reconstructs the inclusion/covariance polynomials and constants. This lower bound is not a curvature-sign argument for omitted terms.
- Section9's exact fixed-block beam-splitter identity, `O_n(u^2)` perturbation and `O_n(u^4)` mutual-information estimate, hence `I_out,n''(0)=0` and `E_occ,n''(0)=-2H_n''(t_*)`. The normalized true-rate value identity is retained. The constants may depend on n; no differentiation of the volume limit is accepted here.

Previously accepted PR53 sources supply only their complete-event, parity, locality and normalized conditional/response machinery. They do not certify PR77's fixed amplitude through a local-radius claim; no PR59 tube theorem or unrelated theorem is imported to provide these fixed signs.

## Independent fixed evidence and actual execution

Independent PR89 executable/preparation head is `d68fec7f10f4451dd9a16c19000c35219db33400`; actual raw head is `1d805e094a0faf0018127ee832f5e1ac74996b41`. Implementation and inputs are unchanged between them.

The checker uses exact rational constants and two polynomial determinant routes for the covariance algebra. Complete events have independent width-two frontier, signed pivoted Bareiss, inclusion/Mobius and row-replacement jet routes, with exhaustive small cross-checks at the specified depths. Physical t jets retain first off-diagonal derivative2 in the scaled event matrix. Small coverage is378Mobius cases,1530direct cases and378jet cases.

Production retains all2,359,296events across the six fixed parameter/length pairs. All are strictly positive; exact count, `sum N=32^n`, `sum N'=sum N''=0` and aggregation gates pass. Histograms keep count, first/second jet sums and squared-first-jet sums, permitting complete entropy, Fisher and acceleration reconstruction. Raw gzip histograms and log intervals have deterministic chunk manifests rather than abbreviated PASS summaries.

Natural logs use precision100 correctly rounded nearest Decimal.ln followed by fixed `1e-90` widening; interval assembly uses floor/ceiling arithmetic and exact sign reversal. The recorded log-range/ulp argument and `1e-40` width gates, midpoint-only entropy tail and three distinct curvature tails all pass.

There was one C2-owned guarded run: start `2026-09-10T02:28:39Z`, original deadline `03:13:39Z`, finish `02:30:30Z`, elapsed110.48600431345403s. PR70 PID absence was checked before launch; PR77 PID175737 was absent at02:31:00Z. One CPU,16GiB cap,noGPU, zero prior arithmetic attempts and zero repairs. All2772ordered gates passed. C3 and reviewers did not run a second mathematical implementation or repeat the computation.

C3 checked all199immutable public Git blobs,77JSON artifacts and178public entries of the original output manifest. The isolated SECOND checked196raw files plus its binding digest, all12gzip manifests/102chunks/2,363,904rows, and2772check rows. Top interpretation files were intentionally withheld from that packet; C3 separately bound the full public source. The original output manifest retains one private invocation entry whose content is omitted publicly. This packaging distinction does not hide missing computational artifacts.

## Remaining boundaries

Whole-interval curvature on `1/2<=|t|<=3/2` remains **INCOMPLETE**. Three points and one midpoint chord do not prove the intervening sign, a general-symbol theorem, or general DPP entropy concavity.

Section9 true-rate claims `I_out''(0)=0` and `E_occ''(0)=-2h''(t_*)` remain **INCOMPLETE**. They require an additional volume-uniform remainder or response bridge for the doubled output process. They are explicitly not premises of the accepted midpoint/point certificates.

Original author JSON remains curated/abbreviated evidence, not literal raw checker output. Historical reports preserve their then-pending finite findings; later PR89 evidence closes only the fixed numerical obligations listed above. No depth/precision/resource expansion, continuum scan or new computation contract was performed. Novelty is **NOT_ASSESSED**; formal verification is **NOT_PERFORMED**.

## Reports and source links

- Author [proof](../../research/I05-DPP-21-fixed-harmonic-20260909/proof.md), [fixed point bounds](../../research/I05-DPP-21-fixed-harmonic-20260909/point_curvature.md), [Fisher projection](../../research/I05-DPP-21-fixed-harmonic-20260909/fisher_projection.md), and [evidence disclosure](../../research/I05-DPP-21-fixed-harmonic-20260909/README.md).
- C1 [original FIRST](../../research/C1-verification-round7-20260910/units/pr77/review_report.md), [successor FIRST](../../research/C1-verification-round7-20260910/units/pr77/successor_8de8_review.md), [scope narrowing FIRST](../../research/C1-verification-round7-20260910/units/pr77/finite_scope_2564_review.md), [actual finite FIRST](../../research/C1-verification-round7-20260910/units/pr77/machine_pr89_review.md), and [finite code FIRST](../../research/C1-verification-round7-20260910/units/pr77/machine_pr89_code.md). Complete37-file archive is frozen at `80c8a616f8e7644afbe92b5b9b0a4172730825c7`.
- Isolated [original/successor SECOND](pr77_second/review_report.md), [scope](pr77_second/frozen_scope.md), [code review](pr77_second/code_review.md), [source binding](pr77_second/source_binding.json), [scope narrowing closure](pr77_second/scope_repair_review.md), and [exact patch encoding record](pr77_second/scope_repair_encoding.md).
- Isolated [finite SECOND](pr77_second/machine_review.md), [finite scope](pr77_second/machine_scope.md), [finite code review](pr77_second/machine_code_review.md), [finite source binding](pr77_second/machine_source_binding.json), and [packet scope/publication note](pr77_second/machine_packet_scope_note.md).
- Independent [implementation](../../research/C2/pr77_fixed52/implementation/independent_pr77_checker.py), [run ledger](../../research/C2/pr77_fixed52/execution/RUN_LEDGER.json), [raw output manifest](../../research/C2/pr77_fixed52/outputs/run01/output_hashes.json), [midpoint bound](../../research/C2/pr77_fixed52/outputs/run01/D/true_rate_Jensen.json), and [three-point bound example](../../research/C2/pr77_fixed52/outputs/run01/D/true_curvature_t3.json).

Merge record: PR89 `ac497154151506831e7d3d04d321910dfe7ea70e`, PR78 `10c0835e04b43c3e4920fa61aed6bc219dd90bb0`, PR77 `88b0026b76ede02d5b8c5c7a354423771a2d1b28`. All exact reviewed source heads are verified second parents.
