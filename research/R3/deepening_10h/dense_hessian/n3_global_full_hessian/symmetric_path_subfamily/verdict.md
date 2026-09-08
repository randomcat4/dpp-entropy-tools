# U10d verdict

General symmetric-path family: **INCOMPLETE**.

Centered line x=1/2, all 0<8a²<1: **CORRECT / INDEPENDENTLY AUDITED**.
The proof concerns the full six-dimensional real-symmetric Hessian. A fresh
implementation reconstructed the exact events, both symmetry reductions, the
Schur determinant identity, and the strict logarithmic bounds.

Also obtained: an explicit positive reflection-odd block for the whole
family; a uniform existential neighborhood around every compact nonzero
piece of the centered line; and the explicit scalar sigma(x,a) that exactly
captures the remaining general-x question.

Sanity only: 16 fully recorded rational centers, exact event/Hessian jets,
exact kernel feasibility pivots, and 120-digit log calculations. Every
sampled full B passed its LDL check. The determinant simplification was
verified separately as a formal polynomial identity, with zero residual.
Neither these samples nor the formal identity alone proves the theorem;
the positivity argument is in derivation.md.

The smallest unresolved issue is the sign of equation (10) away from the
centered-line neighborhood, not an omitted symmetry block. No positive
entropy-curvature candidate was found or certified.
