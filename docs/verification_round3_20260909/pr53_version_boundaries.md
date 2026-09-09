# PR53 immutable version and review boundaries

This is a source-identity and ownership record, not an additional mathematical review.

| Unit | Frozen source | Current review status |
| --- | --- | --- |
| Original parity/likelihood/inverse/beam-splitter packet, five files | `e0688fbb713e55f93acf791b83437ddf2cc06b7f` | C1 FIRST and C3 independent SECOND accepted within scope |
| New finite-range true local entropy-rate theorem, one added 473-line file | `abdd660a6c7761c7a8a53cb8671b4d2543530a5c` | C1 FIRST and C3 separate source-only SECOND ACCEPTED_SCOPED |
| Exponential Wiener extension and six companion changes | `73cdbd09ad9aa975354a116a01f1e0f4955a8c27` | C1 FIRST assigned separately; C3 SECOND reserved after acceptance |

[C1 FR first report](https://github.com/randomcat4/dpp-entropy-tools/blob/a136a57316ce5e866588881b43ce561c0e25657c/research/C1-verification-round4-20260909/units/pr53_fr/review_report.md) and [original independent second](followon/pr53_second/review_report.md) are distinct units. No first report, reviewer code or conclusion is supplied to the new second reviewer. PR53 remains unmerged at this checkpoint.

All bytes in the three frozen prefix snapshots were checked against their declared Git blob hashes. The original-to-FR delta adds only `finite_range_local_theorem.md`; its blob `c65a4e22ed6ee5c69d1b084cfd04d8e77e8d6263` is unchanged in the EW successor. Original `proof.md` and beam-splitter code/output are also unchanged in that successor. The seven EW delta files and exact final blobs are:

| File under research/I05-DPP-21-20260909/ | Blob |
| --- | --- |
| `README.md` | `e37316a3ebbf6567da270dd45f0283ed7f78e79b` |
| `RESULT.md` | `57d2b50386295a9a522bdddeb52887e5affae07b` |
| `code/check_rudin_shapiro_example.py` | `0ebe92fb2ff75999326e6f57e4dbe2239bd19b2e` |
| `exponential_wiener_extension.md` | `3cab8005f6e018b3d02d4e4459b41ca6ba5fc9d6` |
| `output/rudin_shapiro_exact.json` | `4054bc14b0cd4550bc8b6fa88127eb54cd00e138` |
| `sources.md` | `5677092d6e94517a2e741074e313a92ee9e4be52` |
| `verification.md` | `bdb4a3904f06a05905136e64519da1981ff871cf` |

The new theorem claims remain local in the path parameter. Arbitrary measurable symbols, whole-legal-interval concavity and broad novelty remain unaccepted. The exact Rudin-Shapiro script checks finite Fourier constants only; the older floating probe does not prove a rate theorem. A version identity check does not replace a proof audit.

The completed [FR independent second report](followon/pr53_fr_second/review_report.md) confirms the exact local rate scope; its nonblocking source note does not extend the reviewed object.
