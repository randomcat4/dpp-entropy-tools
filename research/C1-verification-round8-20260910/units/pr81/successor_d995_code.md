# PR81 successor d995 code and evidence review

Verdict: NO_CODE_CHANGES_IN_DELTA. The d995 delta adds one Markdown proof/evidence file and no executable code.

Reviewed delta source:

- `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md`
- Lines: 373
- Git blob: `a45186d74f8ea9e512d46bc7ea30380149ec9a33`
- SHA256: `8b5f34ee7c10b51044110e786a4dba8422bab6ba4f0b37ab9887edce4d73422c`
- Immutable URL base: `https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/`

Checks performed:

- Read the frozen d995 source binding and compare metadata.
- Read the full 373-line added Markdown source.
- Statically reconstructed the key analytic dependencies from the allowed PR81/PR70 source context.
- Checked that the report text uses public source aliases rather than private operational paths.

Checks not performed:

- No Python, SymPy, checker, import, compile, test, arithmetic reconstruction, entropy run, interval run, finite job, or formal/proof-assistant check.
- No later live head and no external review report.
- No C2 contract expansion.
- No author source edit.

Code findings:

- No executable-code finding: the delta contains no code file.

Evidence findings:

- ANALYTIC_ACCEPTED_SCOPED: complete-event/full-direction setup and half-leaf coordinate map at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:9-70`.
- ANALYTIC_ACCEPTED_SCOPED: shared-corner PR81 variable identification and half-leaf `n=A k+B ell-J` at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:72-109`.
- ANALYTIC_ACCEPTED_SCOPED: one-edge Gram Lemma 3.1 at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:111-170`.
- ANALYTIC_ACCEPTED_SCOPED: exact four-corner cell decomposition and shared-corner lower bound at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:172-228`.
- ANALYTIC_ACCEPTED_SCOPED: Theorem 5.1 sufficient condition `J<12AB` and strictness proof at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:230-270`.
- ANALYTIC_ACCEPTED_SCOPED: fixed-shape closure for `A=1/4`, `B=4/9`, `0<q<11/36` at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:280-327`.
- SOURCE_ONLY_ARITHMETIC: printed Gram-minor fractions at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:340-349`; not independently reconstructed.
- SOURCE_ONLY_CHECKER: checker description and claimed pass at `source-snapshots/pr81_delta_d995/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md:353-364`; not run.

Evidence boundary:

- The fixed half-leaf shape is accepted as closed by analytic proof, not by finite search or numerical determinant sampling.
- General half-leaf arrows failing `J<12AB`, unequal leaf diagonals, general missing-edge arrows, and general real three-point concavity remain open.
- Novelty is not assessed and formal verification was not performed.
