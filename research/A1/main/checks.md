# Exact checks

`conditional_check.py` verifies eight generic symbolic full-event identities
against independent inclusion-exclusion, normalization, both conditional
acceleration formulas, and four rank-one affine-event identities. It also
checks all three rational kernels of a nontrivial connected triangular chord
by exact Sylvester minors and exact positive normalized event probabilities.

`conditional_checks.json` retains the result, interpreter/library versions,
PID and elapsed time. Its 80-digit negative gap is explicitly a diagnostic,
not an interval certificate; the structural theorem supplies the sign after
independent review. No random search was used.

The first invocation's mathematical script passed, but shell interpolation
made its separate wrapper exit-code file blank. A corrected fixed script
replayed the same bounded check and saved the actual exit code. This wrapper
failure was retained rather than counted as a new mathematical trial.

The remote direct public clone initially failed certificate verification.
The independent checkout was instead made from a public-content Git bundle;
TLS verification was not disabled and no authentication was transferred.
