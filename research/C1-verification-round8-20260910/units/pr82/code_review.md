# PR82 C1 FIRST static source/evidence review

Line references use the public-clean aliases in `frozen_scope.md`.

Scoped status: one-document source checkpoint reviewed. There is no author code in the frozen PR82 scope, and no computation was run.

## Binding and source coverage

`source-snapshots/pr82/SOURCE_BINDING.json` binds PR82 to:

- head `2e21cc4abd67f5b8ab486d1f61a43b4b4fb1ba9e`;
- base `65e59a46b49cd2dbb5c779a4cfae8cef26441984`;
- exactly one file, `source-snapshots/pr82/research/I05-DPP-31-20260910/README.md`;
- 230 lines, blob `7c744e1ebde320bdd7519b4b78ce31d36d1ff5c4`.

The later live commit `5e0861` and later low-regularity files were not included.

## Evidence actually checked

The README's Dobrushin import discussion was checked against the primary Dobrushin 1974 source only for the load-bearing A1/A2 hypotheses. The public source is:

- `https://www.mathnet.ru/eng/sm3631`
- `https://www.mathnet.ru/links/65f76350e7e8dd7f8420ad19db2ee8af/sm3631_eng.pdf`

The source PDF hash was verified as `91D79D372CF4B574DB400E06AD081D38EEF793F576BB94D40C3DBE74A411C1EF`. Standard text extraction was used for printed pp. 14--18 and 24--25. No mathematical computation was performed, and no full source text is reproduced.

Old PR66 reviews and C3 opinions were not opened. The old review path mentioned at `README.md:L21` and `README.md:L47` was treated only as provenance/background.

## Static review notes

`README.md:L15-L47` has enough direct mathematical content to preserve the Dobrushin applicability gap without relying on old review conclusions. For public portability, it would be cleaner to make the Dobrushin page facts the direct support and leave the old-review citation as provenance.

`README.md:L51-L96` is a finite determinant identity/candidate route, not a complete implementation. Its own text correctly lists the two missing load-bearing bridges at `README.md:L91-L94`.

`README.md:L104-L184` is a source proof, not an executable artifact. The proof is accepted only as a localization mechanism obstruction; it does not run a finite check and does not claim an entropy-rate counterexample.

`README.md:L186-L210` is a conditional response-theorem target. The cited source families are not imported as a completed response theorem, which is the correct static evidence posture.

## C2 contract status

No necessary finite C2 task is required for the scoped FIRST verdict.

If later assigned, an independent finite check should:

1. choose small finite positive definite L-ensemble matrices satisfying `mI <= L <= MI`;
2. compute finite Boolean Mobius coefficients directly from `log det L_S`;
3. compute the corresponding connected closed-walk aggregate from the trace expansion;
4. compare the two with a clearly fixed Hamiltonian sign convention;
5. record that this checks only the finite determinant identity and not the infinite-volume Dobrushin A2 bridge.

This is only a future contract suggestion. It is not authorized or executed here.

## Final static-source status

No blocking code defect exists because PR82 contains no code in scope. The README is acceptable as a scoped method/localization checkpoint, with the original PR66 theorem and all infinite-volume/absolute-norm/response bridges still incomplete.
