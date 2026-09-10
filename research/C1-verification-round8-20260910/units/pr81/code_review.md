# PR81 code and evidence review

Verdict: NO_CODE_CHANGES_IN_SCOPE. PR81 supplies one Markdown proof file and no executable source file. The code review therefore reduces to source-binding, evidence-status, and documentation-claim review.

Reviewed source:

- `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md`
- Lines: 279
- Blob: `ad51fb200fb44e888025507f57189d55ec7dbd1a`
- Immutable URL base: `https://github.com/randomcat4/dpp-entropy-tools/blob/449465e2b424c7f284bf4e8317d95966f6743371/`

Scoped predecessor evidence:

- `source-snapshots/pr70/proof.md`, blob `5732657cd5e5ce87d2d2409a4556379228ae3145`
- `source-snapshots/pr70/post_checkpoint.md`, blob `37206206cb83cfb948832ac731d34eaf966a26da`
- Immutable URL base: `https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/`

Checks performed:

- Read the frozen PR81 binding metadata and the one frozen PR81 proof file.
- Read the scoped PR70 predecessor proof, post-checkpoint, and binding metadata.
- Confirmed the blob identities above by metadata/hash check.
- Performed static analytic review only.

Checks not performed:

- No PR81 tests exist in this source scope.
- No author checker, Python, SymPy, interval arithmetic, finite witness, entropy reconstruction, formal verification, or CI was run.
- No live PR head or linked review report was used.

Evidence classification:

- ANALYTIC_ACCEPTED_SCOPED: PR81 Sections 2-4, specifically the side-sum compression at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:39-104`, rectangle identities at `:106-124`, complement symmetry at `:126-150`, and curvature/sign theorem at `:151-200`.
- FULL_CORE_RETAINED: the source keeps the full Fisher/acceleration/marginal structure through the inherited PR70 reduction and PR81's full-core statements at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:95-104` and `:242-267`.
- PENDING_C2: the finite paired-resolvent obstruction in `source-snapshots/pr70/post_checkpoint.md:5-35` and `:100-109` remains pending independent certification.
- OPEN: `det E_H>=0` remains unresolved at `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:248-267`.
- NOT_ASSESSED: novelty.
- NOT_PERFORMED: formal verification.

Code findings:

- No executable-code finding: PR81 has no code file in the frozen one-file source scope.

Documentation/evidence finding:

- NEEDS_FIX, `source-snapshots/pr81/research/I05-22-R5-logmean-imbalance/proof.md:273`: the phrase "PR70 already refutes that auxiliary route" should be qualified because the finite paired-resolvent witness is still independently pending C2. The bounded fix is to state that PR70 records an author finite obstruction pending independent C2 certification. This keeps PR81 consistent with its own scope note at `:5` and does not affect the accepted analytic Sections 2-4.

Bounded C2 obligation if the categorical "refutes" wording is retained:

- Independently certify the PR70 post-checkpoint finite paired-resolvent object from `source-snapshots/pr70/post_checkpoint.md:5-35`, including legality, exact second-derivative sign, and the stated error-enclosed reproduction path at `:100-109`.
- This C1 review did not perform that obligation and does not treat the finite witness as proved.
