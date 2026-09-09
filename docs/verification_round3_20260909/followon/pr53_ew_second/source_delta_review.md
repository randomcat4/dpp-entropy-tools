# PR53 EW source-delta closure

Prior reviewed head: `73cdbd09ad9aa975354a116a01f1e0f4955a8c27`

New frozen head: `ebecc412467939591e018a295a18c49a0a341ce9`

Delta verdict: `ACCEPTED_SCOPED`.

This is a same-reviewer closure for exposition clarifications only. The earlier mathematical verdict is preserved. I did not read first-review reports, C1 conclusions, issue comments, or other reviewer artifacts. I did not run arithmetic, CAS, scout, formal, or checker jobs.

## Metadata correction

My earlier review report incorrectly said `exponential_wiener_extension.md` had 175 lines. Direct line counting of the frozen author source gives:

- `73cdbd09ad9aa975354a116a01f1e0f4955a8c27`: 268 lines.
- `ebecc412467939591e018a295a18c49a0a341ce9`: 268 lines.

This was a source-record typo only. The line anchors and mathematical verdict are unchanged.

## File delta and hashes

Only the expected three files changed:

| File | Old blob | New blob | Status |
|---|---:|---:|---|
| `research/I05-DPP-21-20260909/exponential_wiener_extension.md` | `3cab8005f6e018b3d02d4e4459b41ca6ba5fc9d6` | `8404d0ec0b36ec70ee2e25b2b7c6539a15aafd1f` | exposition clarification |
| `research/I05-DPP-21-20260909/finite_range_local_theorem.md` | `c65a4e22ed6ee5c69d1b084cfd04d8e77e8d6263` | `e1c014d654d71a89c700dbd12e44fdab95cd2a9d` | exposition clarification |
| `research/I05-DPP-21-20260909/sources.md` | `5677092d6e94517a2e741074e313a92ee9e4be52` | `31f4cd09eaa99aaff4286b057f624daa884d47e0` | citation scope clarification |

The following files are unchanged byte-for-byte: `RESULT.md`, `verification.md`, `README.md`, `code/check_rudin_shapiro_example.py`, and `output/rudin_shapiro_exact.json`. Thus the EW theorem quantifiers, quartic constant, example checker, and recorded output remain the same as in the reviewed `73cdbd09ad9aa975354a116a01f1e0f4955a8c27` snapshot.

## Delta checks

### `exponential_wiener_extension.md`

The new block-inverse sentence at `exponential_wiener_extension.md:209` is correct. With
`S_F=M_F-E_FN M_N^{-1}E_NF`, the standard block inverse formula gives
`S_F^{-1}=[M_R^{-1}]_{FF}` exactly. Taking a principal row/column block cannot increase the weighted Schur norm, so the prior uniform inverse bound applies to `S_F^{-1}`. The added sentence also avoids the ambiguous wording that could have sounded like an extra correction term was added to the `FF` block.

The new Hölder/holomorphy paragraph at `exponential_wiener_extension.md:220` fixes the functional-space bookkeeping. It chooses a fixed weaker exponent `0<b<min(a',1)`, defines the variation norm, combines stronger `a'`-variation control with the sup-norm convergence error, and uses nested disks `|z|<=r_1<r_2<r_0` for Cauchy estimates. This is the right mechanism for Banach-holomorphic convergence in one fixed Hölder space.

No theorem statement, constant, matching/KL step, or scope assertion changed in this file.

### `finite_range_local_theorem.md`

The finite-range dependency now mirrors the same fixed weaker Hölder-space argument at `finite_range_local_theorem.md:276-282`. This is a clarification, not a change of theorem content. The RPF paragraph at `finite_range_local_theorem.md:307-309` now states that the transfer theorem is used in the fixed Hölder space and avoids claiming a spectral gap for the full Walters class. The Section 7 heading was corrected from “quadratic term in `s`” to “linear term in `s`” at `finite_range_local_theorem.md:343`, matching the proof body.

No theorem quantifier, parity identity, matching count, KL coefficient, curvature constant, or example constant changed.

### `sources.md` and primary-source match

The updated source paragraph at `sources.md:33-35` accurately narrows the Cioletti--Silva citation to the Hölder setting. I checked the primary arXiv HTML for Cioletti--Silva, arXiv:1511.01579v2: the paper defines the one-sided compact-alphabet shift, a full-support Borel prior, and the Ruelle operator as an integral over prepended symbols; Theorem 2.1 assumes a Hölder potential with exponent `0<gamma<1` and gives a simple maximal eigenvalue plus a spectral gap; Lemma 2.4, Proposition 2.6, and Corollary 2.7 give the operator/dual analyticity framework on Hölder spaces. See [arXiv:1511.01579v2 HTML](https://arxiv.org/html/1511.01579v2), especially lines 61-80 and 105-139 in the browsed HTML.

For the finite alphabet `{0,1}` with uniform prior and potential `log(2G_s)`, the integral operator is exactly

```text
F -> (1/2) sum_a 2G_s(ax)F(ax) = sum_a G_s(ax)F(ax),
```

which matches `finite_range_local_theorem.md:319-323`. The new source paragraph correctly says this is the Hölder result, not a general Walters-class spectral-gap assertion.

## Closure

The `ebecc412467939591e018a295a18c49a0a341ce9` changes address the requested exposition issues: exact `S_F^{-1}` identification, fixed weaker Hölder/variation norm, interpolation, nested-disk holomorphy, precise RPF citation/normalization, and the `s`-linear heading. They do not alter the accepted scoped EW theorem or the unchanged checker/output.

The closure remains limited to the local EW theorem and its stated dependencies. Whole-legal-interval concavity, the full PR39 interval, arbitrary measurable symbols, arbitrary scalar chords, and entropy-rate counterexamples remain outside this verdict.
