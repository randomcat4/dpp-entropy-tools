# Frozen computation specification

The target is the complete-configuration Shannon entropy of finite DPPs and
the one-site entropy increment of fixed scalar Toeplitz symbols.  Spectral,
von Neumann, and point-count entropies are diagnostics only and never replace
the complete DPP law.

1. **C4.** Use three frozen two/three/four-interval reflection candidates from
   the upstream seed `2026090701` scan.  Count eigenvalues in the five stated
   transition windows through `n=2048`; compare a log-only fit with
   `a n+b log n+c`.  Align the finite increment Hessian, spectral increment,
   coherence correction, and transition count through `n=22`.
2. **C1a.** Orthogonally project the canonical n=5 and larger-gap n=5,6 exact
   examples onto Hermitian Toeplitz matrices.  Record distances, feasibility,
   a dense `(s,r)` deformation landscape, and nearest points found in one
   explicitly bounded finite trigonometric-polynomial class.  This is not an
   exact distance to the bounded moment body.
3. **C3.** Extend four fixed objects without a new family search.  Read each
   increment directly from the conditional-DPP recursion.  Stop when stable
   negative increments and the measured `2^n` cost satisfy the frozen stop
   rule.
4. **C2.** Search only intrinsic finite Fourier coordinates at n=5,6.  Retain
   all `2^n` event determinant jets.  Run the even-f/odd-g and general complex
   Toeplitz classes, normalize `||T_n(g)||_F=1`, impose a nondegenerate base
   Fourier-amplitude floor, and certify whole-circle legality by a global
   Fourier-amplitude condition plus an independent grid/Lipschitz bound.

Positive floating candidates would require 100-digit independent recomputation
and a directed interval enclosure.  None occurred.

