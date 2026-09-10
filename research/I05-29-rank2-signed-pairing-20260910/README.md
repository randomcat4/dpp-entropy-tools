# PR80 source and evidence scope

The three mathematical notes give author analytic claims and finite diagnostics. Independent acceptance must distinguish analytic identities/sufficient conditions from fixed arithmetic and from the still-open whole-chord theorem.

Read `RESULT.md` for the signed-pair identity and ratio-cone criterion, `ADDENDUM_S09_SIGNED_FIBERS.md` for the reserve identity and square completion, and `ADDENDUM_FIBER_WINDOW_MOMENT.md` for the fiber-window lower bound. General curvature conclusions from `t^2 I''` are stated for `s=t^2>0` on the corresponding connected physical t-bands. The diagonal strictness witness and the separate off-diagonal reserve test are compatible.

## Author output packaging

Both `output/*.txt` files are edited author summaries, not literal raw stdout from the committed scripts. In particular, importing `verify_s09_signed_fibers.py` emits its top-level output before the window script prints its own section, while the saved window summary omits that prelude. The saved signed summary also edits the minimum-q line and adds explanatory text. These summaries and their PASS labels are not independent numerical certificates; the existing files and code are preserved without a new run.

In the window script, the value named `lo` is a conservative lower bound for the theorem's right side. The value named `hi` uses the same upper delta penalty and is only a companion conservative value; it is not a proved upper enclosure of the theorem's right side. Any saved "lower/upper" label for those window columns is withdrawn as an interval claim. Only the conservative lower endpoint is relevant to the proposed positivity certificate. Independent reconstruction must produce its own valid lower bound or both directed endpoints, with raw rational evidence.

The intended prior fixture is pinned to [PR58's immutable joint-additive source](https://github.com/randomcat4/dpp-entropy-tools/blob/89aa874c24dd5a3ea98f8474826392560b1d0397/research/I05-23-middle-20260909/ADDENDUM_JOINT_ADDITIVE.md). The literal matrices embedded in `code/verify_s09_signed_fibers.py` define the author finite object for this packet. Their equality to the cited fixture, every pair count, all signs and window-moment bounds still require the independent source/arithmetic binding. A previous positive global-curvature certificate does not verify these new per-pair or per-fiber claims.

No new C2 contract is supplied here. No author module is an independent computational implementation. No whole-chord job, PR70/77 budget expansion, formal check or novelty claim follows from this clarification.
