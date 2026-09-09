# PR60 C1 static code review

Status: `CORRECT` for static consistency with the packet formulas, with finite arithmetic still `INCOMPLETE_PENDING_C2` or a separate exact check as described below. I did not run any script, SymPy job, entropy computation, polynomial expansion, or certificate reconstruction.

## Binding and packaging

`SOURCE_BINDING.json` binds the public packet to PR60 head `f869fd251c0d6fdad737b6d5efa287307795a87d`, base `9dcb6e9079ca57f94e0e30d63161cda89ca61fae`, and eight added files under `research/I05-22-R3-lambda-zero-global/` (`source-snapshots/pr60/SOURCE_BINDING.json:2-8`). Read-only local blob hashes matched all eight recorded file blobs (`source-snapshots/pr60/SOURCE_BINDING.json:10-65`).

The scripts import only Python standard-library modules plus SymPy. I found no private path, network dependency, credential use, hidden input file, or dependency on the archived r=0 coefficient chain.

## `certificate.py`

Verdict: `CORRECT` as an author exact verifier; not an independent reconstruction.

The literal residual polynomial is fully stored in the script as six coefficient blocks (`source-snapshots/pr60/certificate.py:20-27`). The reduced matrix uses exactly the ingredients displayed in `proof.md` section 4: `a,b,v,w`, `J,L,C`, `Delta`, `S`, `G`, `la`, `lb`, the diagonal positive term, and both rank-one subtractions (`source-snapshots/pr60/certificate.py:29-40`; compare `source-snapshots/pr60/proof.md:167-176`).

The determinant check constructs `Ahat` by multiplying each row of `Rbar` by `Delta^{-1}` and clearing denominators with `2 J^2 L^2 C`; it asserts no symbolic denominator remains (`source-snapshots/pr60/certificate.py:65-75`). It then enumerates all 24 determinant products in a rational polynomial ring and compares the result with `8 t (1-t)^3 (1-r^2 t)^3 (1-r^2 t^2)^3 P` (`source-snapshots/pr60/certificate.py:76-83`). This matches the determinant identity claimed in `proof.md` (`source-snapshots/pr60/proof.md:190-203`).

The chart transform implements the stated bounded binomial substitution rule (`source-snapshots/pr60/certificate.py:42-56`; compare `source-snapshots/pr60/proof.md:207-235`). The run function checks degree `(4,4,10,6)`, 279 P terms, the two stated symmetries, positive seed minors, 1731 transformed nonzero terms, minimum positive coefficient 192, constant 432, and positivity of every stored nonzero Q coefficient (`source-snapshots/pr60/certificate.py:58-101`).

Static limitation: these checks are implemented with Python `assert` statements (`source-snapshots/pr60/certificate.py:61-93`). The documented command uses ordinary `python`, so this is not a mathematical defect in the recorded author run, but a public verifier should not be run with optimization (`python -O`) because that would suppress the gates.

## `bridge_checks.py`

Verdict: `CORRECT` as a bridge-consistency checker; not independent of `certificate.py`'s `reduced_matrix()`.

The script reconstructs the product-Bernoulli Gram identity `S Delta^{-1} S = Delta` and the four-event weighted Gram matrix (`source-snapshots/pr60/bridge_checks.py:7-24`). It then rebuilds the `Q` terms, the post-derivative change of variables, the two positive eliminated diagonal entries, the alpha/beta couplings, the lower block `R0`, and the square-completed `RS` (`source-snapshots/pr60/bridge_checks.py:26-51`).

The final comparison checks `u RS / 4` against `reduced_matrix().subs(t,u^4)` (`source-snapshots/pr60/bridge_checks.py:52-53`). This is useful evidence that the markdown bridge formulas and `certificate.py` matrix agree, but because it imports `certificate.reduced_matrix` (`source-snapshots/pr60/bridge_checks.py:5`), it is not a separate determinant or coefficient reconstruction.

Static limitation: this script also relies on `assert` for all zero checks (`source-snapshots/pr60/bridge_checks.py:13-17`, `:47-53`), so optimized Python would not be a valid verification mode.

## `continuation_exact.py`

Verdict: `CORRECT` as a static encoding of the radial obstruction checks; finite signs still need an independent exact run outside the current C2 determinant contract.

The script stores the rational `K*`, `D*`, and `C*` used in `continuation.md` (`source-snapshots/pr60/continuation_exact.py:11-16`; compare `source-snapshots/pr60/continuation.md:76-86`). It defines rational interval arithmetic for the atanh/log2 enclosure and outward decimal rounding (`source-snapshots/pr60/continuation_exact.py:18-47`; compare `source-snapshots/pr60/continuation.md:135-140`). The atom constructor loops over all eight complete events by inclusion-exclusion (`source-snapshots/pr60/continuation_exact.py:49-58`), and legality uses rational Sylvester checks for both `K` and `I-K` (`source-snapshots/pr60/continuation_exact.py:60-65`).

The run function reconstructs all eight two-parameter event polynomials, extracts `p`, `p_e`, `p_ee`, `p_d`, `p_ed`, and `p_eed`, accumulates the true entropy curvature and radial derivative formula, checks the Jensen triple, checks radial endpoint legality, computes the legal radius and `exp(Lambda)` ratio, and emits the full jet table and intervals (`source-snapshots/pr60/continuation_exact.py:73-100`). It does not import the main certificate script.

Static limitation: the sign and legality gates are again Python `assert` statements (`source-snapshots/pr60/continuation_exact.py:84-93`). More importantly, C1 did not run this file or independently reconstruct its rational intervals. The radial obstruction should remain pending a separate exact check.

## Required independent computations

Covered by the active C2 same-head contract: the main Lambda-zero determinant/chart certificate from displayed `Rstar/Rbar` through exact `det/P/Q`, including all 1925 chart positions, symmetries, and seed.

Not covered by that C2 contract: `continuation_exact.py`'s finite radial-obstruction claims, namely the exact legality radius, eight-event jet table, log enclosures, negative radial derivative, positive negative-Hessian quantity `-H''(K*;D*)`, hence concave actual entropy curvature, and negative complete-entropy Jensen interval.

No code edits are required for the mathematical packet to be reviewable, provided reviewers run the scripts exactly as documented. For robustness, replacing verification `assert`s with explicit exceptions would make accidental optimized-Python runs fail closed.
