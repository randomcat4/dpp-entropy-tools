# PR82 p4/p8 finite-response SECOND scope

Reviewer role: independent SECOND mathematical source reviewer, not an author and not a FIRST/C3 adjudicator.

Frozen PR head reviewed: `6ecc004a3f99f97369ea5af53f1136b59cf2129c`.

Allowed local packet root:

`docs/verification_round4_20260909/pr82_p4_second`

Only the following local files were read:

| File | Binding head | SHA-256 status |
|---|---:|---|
| `input/I05-DPP-31-20260910/README.md` | `6ecc004a3f99f97369ea5af53f1136b59cf2129c` | MATCH |
| `input/I05-DPP-31-pr66-lowreg-20260910/c4_response_p4_boundary_correction.md` | `6ecc004a3f99f97369ea5af53f1136b59cf2129c` | MATCH |
| `input/I05-DPP-31-pr66-lowreg-20260910/c4_response_p4_repair.md` | `6ecc004a3f99f97369ea5af53f1136b59cf2129c` | MATCH |
| `input/I05-DPP-31-pr66-lowreg-20260910/c4_response_p4_source_audit.md` | `6ecc004a3f99f97369ea5af53f1136b59cf2129c` | MATCH |
| `input/I05-DPP-31-pr66-lowreg-20260910/c4_response_p8.md` | `6ecc004a3f99f97369ea5af53f1136b59cf2129c` | MATCH |
| `input/I05-DPP-31-pr66-lowreg-20260910/c4_response_p8_correction.md` | `6ecc004a3f99f97369ea5af53f1136b59cf2129c` | MATCH |
| `pr66_source/equilibrium_bridge.md` | `af1edaad69c4e1f5e4bbd1239b8463b56bf64075` | MATCH |
| `pr66_source/frozen_statement.md` | `af1edaad69c4e1f5e4bbd1239b8463b56bf64075` | MATCH |
| `pr66_source/proof.md` | `af1edaad69c4e1f5e4bbd1239b8463b56bf64075` | MATCH |
| `pr53_source/proof.md` | `65e59a46b49cd2dbb5c779a4cfae8cef26441984` | MATCH |
| `pr53_source/finite_range_local_theorem.md` | `65e59a46b49cd2dbb5c779a4cfae8cef26441984` | MATCH |
| `pr53_source/exponential_wiener_extension.md` | `65e59a46b49cd2dbb5c779a4cfae8cef26441984` | MATCH |
| `input_binding.json` | packet binding | MATCH as local packet file |

The `git_blob` identifiers listed in `input_binding.json` were also checked against the frozen local files and matched the bound paths.

Direct primary sources checked by web/arXiv only:

- Bressaud--Fernandez--Galves, *Decay of correlations for non Holderian dynamics. A coupling approach*, arXiv:`math/9806132`.
- H. Tanaka, *General asymptotic perturbation theory in transfer operators*, arXiv:`2205.12561`.

No primary PDF/text was copied into the public report. No FIRST report, other SECOND report, C3 adjudication, public comments, later live PR82 material, or private directory was opened. The author `source_audit` file was read only as an author-side proof note and was not treated as independent verification.

No Python/SymPy/authorchecker/finite enumeration/entropy recomputation/log/determinant arithmetic was run. The only computation used was binding/hash/blob checking and static file reading.

Review target:

- Check the p>4 finite-response repair against its actual source premises.
- Preserve the p>8 checkpoint's strictly narrower extra claims, especially the old `(6.7)` finite-memory derivative convergence and the stronger analytic framing.
- Verify the exact primary-source role of BFG 1999 and Tanaka 2022.
- Do not upgrade a method barrier, finite identity, or source bibliography entry into an independently proved global entropy theorem or entropy counterexample.
