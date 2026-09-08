# Frozen theorem: real `2 x 2` DPP entropy concavity

Version: v1 (2026-09-08)

Let `K_0,V` be real symmetric `2 x 2` matrices, let `t>0`, and assume

```text
K_- = K_0-tV,   K_+ = K_0+tV
```

both satisfy `0<K_±<I`.  The midpoint is then strictly feasible.  Let `H(K)`
be the Shannon entropy of the complete DPP event law, where exact event
probabilities are defined from the inclusion probabilities
`P(A subset Y)=det(K_A)` by Mobius inversion.  Prove

```text
[H(K_-)+H(K_+)]/2-H(K_0) <= 0.
```

Finite Shannon-entropy differentiation, the `2 x 2` Sylvester criterion, and
elementary logarithm inequalities are allowed.  Finite numerical scanning is
not a proof, and principal minors must not be treated as exact event
probabilities.  The premises may not be weakened or supplemented; if the
claim is false, an explicit counterexample satisfying every strict-feasibility
condition is required.

