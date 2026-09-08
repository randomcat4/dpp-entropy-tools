# D10-U10b scalar-information verdict

STATUS: INCOMPLETE.

Layered result:

- Exact information-space reformulation: `CORRECT_SCOPED` after fresh
  non-author reconstruction.  The U8 scalar is exactly the ridge/Bessel
  minimum in `proof_or_blocker.md`.
- Global `rho(K)<=1`: INCOMPLETE.  No non-circular global construction of atom
  weights `g_S` with energy `<=1` was found.
- Fisher-only score projection proof: REJECTED as a proof route.  A strict
  connected rational DPP has
  `det(N) eta^T F^{-1} eta = 1.6324286014007979... > 1`, while its true
  `rho = 0.6364350521741918... < 1`.
- Positive-curvature counterexample: NONE FOUND.  The blocker point is not a
  `rho>1` candidate.
- Finite sanity: PASS, used only to check exact-event semantics, constants, and
  the shortcut blocker.

The next useful move is either a genuine analytic construction in the
residual-plus-score formula

```text
||I - N^{1/2}(sum_S g_S M_S)N^{1/2}||_F^2
  + det(N) sum_S p_S g_S^2 <= 1,
```

or a targeted search for a strict kernel with `rho>1`.  Simply applying
Fisher-only Cauchy/Bessel is no longer viable.
