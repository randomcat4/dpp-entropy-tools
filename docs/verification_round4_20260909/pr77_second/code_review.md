# Static code and ledger review

## Method

I read the frozen code and frozen JSON outputs statically. I did not run any author script, determinant enumeration, decimal logarithm computation, test, job, or resource probe.

## Summary

The scripts are generally aligned with the mathematical contracts they are meant to certify, but the frozen output ledger is not clean. Several JSON files in `input/output/` and `delta_input/output/` are summaries whose schemas do not match what the frozen scripts would write. The run records also list commands that omit output paths required to create the frozen summary filenames.

This is a CRITICAL_GAPS issue for provenance. It does not prove the mathematical claims false, but it prevents the frozen JSON summaries from serving as independently auditable certificates.

## Static script findings

### `input/code/certify_midpoint_rate_gap.py`

The script structure matches the midpoint certificate contract:

- exact signed complete-event numerators from a width-two determinant automaton (`input/code/certify_midpoint_rate_gap.py:207`-`241`);
- independent small Mobius/direct determinant check through length six (`input/code/certify_midpoint_rate_gap.py:108`-`145`);
- directed entropy intervals using widened correctly rounded decimal logarithms (`input/code/certify_midpoint_rate_gap.py:244`-`281`);
- analytic tail subtraction before the midpoint comparison (`input/code/certify_midpoint_rate_gap.py:303`-`345`).

Ledger issue: the default output path is `output/midpoint_rate_certificate.full.json` (`input/code/certify_midpoint_rate_gap.py:380`-`390`), but the frozen summary is `input/output/midpoint_rate_certificate.json`, and the recorded command in that JSON omits an `--output` argument. The frozen summary also omits the actual `true_midpoint_gap_lower` value that the script's `run()` would emit (`input/code/certify_midpoint_rate_gap.py:356`-`377`).

### `input/code/certify_point_curvatures.py`

The script structure matches the point-curvature certificate contract:

- exact determinant value/first/second jets (`input/code/certify_point_curvatures.py:53`-`146`);
- exact normalization of all three jet layers (`input/code/certify_point_curvatures.py:137`-`145`);
- directed interval enclosure for `H_n''` (`input/code/certify_point_curvatures.py:161`-`195`);
- point-specific comparison data and curvature tail (`input/code/certify_point_curvatures.py:216`-`319`);
- independent small exact polynomial-interpolation jet checks through length six (`input/code/certify_point_curvatures.py:326`-`386`);
- threshold comparison after adding the tail (`input/code/certify_point_curvatures.py:389`-`463`).

Ledger issue: the default output path is `output/point_curvature_certificate.full.json` (`input/code/certify_point_curvatures.py:466`-`476`), but the frozen summary is `input/output/point_curvature_certificate.json`, and the recorded command in `delta_input/output/run_record_round2.json` omits an `--output` argument. The summary lacks the detailed finite and true curvature intervals that the script would emit.

### `input/code/check_analytic_constants.py`

The script checks the rational constants used for legality, comparison residuals, the advertised tail constant, entropy derivative bounds, and Bregman constants (`input/code/check_analytic_constants.py:16`-`87`).

Ledger issue: the script's report schema includes `raw_tail_constant` and `bregman_constants` (`input/code/check_analytic_constants.py:89`-`115`), but the frozen `input/output/analytic_constants_exact.json` uses a different schema and omits those fields. This indicates the frozen JSON is not the direct output of the frozen script as read.

### `input/code/check_band_automaton.py`

The script compares the automaton's complete multiset of event numerators with direct Bareiss determinants through length eight (`input/code/check_band_automaton.py:28`-`64`).

Ledger issue: the script's report schema includes `maximum_length` and detailed `checked_cases` (`input/code/check_band_automaton.py:66`-`75`), but the frozen `input/output/band_automaton_exact.json` contains a shorter summary schema instead.

### `delta_input/code/check_pair_fisher_projection.py`

The script reconstructs local inclusion determinants by exact Fraction polynomial arithmetic in `u=t/16`, checks the covariance polynomials, checks endpoint variance values, and checks the uniform Fisher lower bound (`delta_input/code/check_pair_fisher_projection.py:98`-`151`).

Ledger issue: the script's report schema emits coefficient arrays (`delta_input/code/check_pair_fisher_projection.py:152`-`172`), while `delta_input/output/pair_fisher_exact.json` contains formula strings. The frozen JSON is therefore not the direct output of the frozen script as read.

## Mathematical coverage limits of the scripts

The scripts are finite exact-arithmetic checkers. They do not independently prove the analytic true-rate interfaces by themselves. The analytic proof obligations remain in the markdown sources:

- true-rate midpoint tail: `input/proof.md:222`-`258`;
- curvature derivative tail: `input/proof.md:407`-`538`;
- finite-to-rate Fisher identification: `input/fisher_projection.md:95`-`131`;
- RPF/Poisson response formula: `input/proof.md:319`-`405`.

The scripts also do not prove the whole continuum sign. The source correctly keeps that statement incomplete.

## Minimal ledger repair

For each certificate, freeze either:

1. the full JSON generated by the exact frozen command, including all detailed intervals and fields; or
2. a summary JSON explicitly marked as a derived summary, together with the full generated artifact and the command that generated it.

The run records should include the exact `--output` path whenever the generated file is not the script default.

