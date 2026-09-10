# PR88 static code and certificate review

## Boundary

I did not execute, import, or compile `verify.py`. I inspected it statically and parsed `certificate_compact.json` only for schema, short metadata, and array sizes. All script and JSON material is `SOURCE_ONLY`.

## `verify.py`

The script is a fixed-input author checker, not a generic search framework. It uses exact SymPy rationals for determinants and atom laws, plus dyadic outward enclosures for logarithms.

Key static structure:

- Lines 17-19 set dyadic scale `2^192` and `TERMS=80`.
- Lines 40-71 implement range-reduced atanh logarithm bounds with an explicit positive tail.
- Lines 73-91 compute entropy intervals and outward decimal display bounds, requiring internal width below `10^-45`.
- Lines 96-116 compute inclusion minors and complete atom laws in two equivalent ways.
- Lines 139-182 implement the dense rank-two method-obstruction fixture and pair inclusion corrections.
- Lines 184-217 implement the six-point common dense-mode fixture and exact conditional identity checks.
- Lines 219-290 implement the multiring law, atom polynomial checks, beta accumulation, three sample Hessian/Jensen probes, and conditional-anchor obstruction data.
- Lines 292-311 write a certificate JSON and print a short summary only when run as `__main__`.

Static limitations:

- The script is author code and shares the author's implementation choices. It is not an independent C2 implementation.
- The finite signs depend on exact event enumeration, determinant identities, logarithm intervals, and rational beta arithmetic that this review did not recompute.
- The stored compact JSON is an output artifact; `verify.py` generates a certificate target rather than independently validating the delivered compact JSON as input.
- No PID/start/end transcript or independent CI run is present in the packet; `fixtures.md` records Python 3.13.5 / SymPy 1.14.0 and about 0.616 seconds as author runtime only.

Verdict: `SOURCE_ONLY` for all finite arithmetic conclusions.

## `certificate_compact.json`

The delivered JSON parses successfully. Top-level keys are `status`, `python`, `sympy`, log/display parameters, `method`, `common_mode`, `multiring`, `author_runtime_seconds`, and `array_index`. It reports status `AUTHOR_RATIONAL_CERTIFICATES; PENDING_REVIEW`, Python `3.13.5`, SymPy `1.14.0`, `log_scale_bits=192`, `atanh_terms=80`, and 36 outward display digits.

Schema/short-field inspection found:

- `method`: ranks `[2,2,4]`, epsilon `1/1000000`, three 16-atom arrays, and six pair-inclusion corrections.
- `common_mode`: ranks `[2,2,3]`, `r=77/200`, epsilon `1/100000`, three 64-atom arrays, and the symbolic all-epsilon lower-bound label.
- `multiring`: beta label `6784/16875`, count-layer lower-bound label `128/625`, six zero-layer categories, 64 atom-polynomial records, and three probe labels at `t=1/2,3/4,9/10`.

I did not dump or validate the large rational atom payloads. The JSON remains an author certificate, not an independently reviewed proof object.

## Code review conclusion

`verify.py` is consistent with the paper text about what the author intended to check, including full event laws, full Fisher/acceleration terms, outward log bounds, and exact zeros. It does not close the review gates for finite fixture signs, beta arithmetic, interval displays, or 64-event enumeration. Those require an independent C2 reconstruction if they are to be promoted beyond `SOURCE_ONLY`.
