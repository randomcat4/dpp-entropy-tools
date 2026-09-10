# Retained preflight mechanical failure 001

- Stage: mandatory preflight, before any formal certification run
- Outcome: mechanical harness crash; no mathematical predicate evaluated
- Process exit: 1
- Failure: `decimal.InvalidOperation` in the independent finite-difference helper when Python Decimal evaluated a zero base to a zero exponent.
- Scope of repair: replace each degree-zero factor by the exact Decimal constant `1`; no certificate formula, interval Jet rule, fixture coefficient, tolerance, or frozen input changes.
- Disposition: retained permanently; it is not a PASS and is not formal-run evidence.
