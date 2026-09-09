# W4 compute plan

This plan fixes the independent computation before any certificate run.

## Independent implementation rule

The verifier will not import the author's evaluator. The independent checker will reconstruct the eight event probabilities from

\[
q_{ij}=x_ix_j-K_{ij}^2,\qquad
r=xyz+2abc-xc^2-yb^2-za^2,
\]

then derive \(p'\), \(p''\), Fisher, \(A_K\), \(H''\), \(\mathcal S,\mathcal U,\mathcal V\), and all residual matrices from these eight probabilities.

The author's code and outputs are read only as reviewed material, not reused as a certificate engine.

## Exact inputs

- Epsilon: \(\epsilon=1/4\).
- Coercivity target: \(7/10\).
- Event order: `0, 1, 2, 12, 3, 13, 23, 123`.
- Author exact-input file: `inputs/exact_inputs.json`.
- Arithmetic target: rational arithmetic for symbolic identities and rational centers; high-precision interval or directed decimal diagnostics only for logs and eigenvalue-style probes.

## Planned directed centers

At most 32 fixed centers will be used. They are diagnostic and certificate-oriented, not a random scan. The list may be shortened if a critical gap is found early.

1. Balanced zero-edge center: \(x=y=z=1/2\), \(a=b=c=0\).
2. Balanced all-edge positive center: \(x=y=z=1/2\), \(e_{12}=e_{13}=e_{23}=1/4\).
3. Balanced mixed-sign cycle: \(x=y=z=1/2\), \(e_{12}=1/4,e_{13}=1/4,e_{23}=-1/4\).
4. Balanced one-edge center: only \(e_{12}=1/4\).
5. Balanced two-edge connected path: \(e_{12}=e_{13}=1/4,e_{23}=0\).
6. Balanced two-edge path with mixed signs: \(e_{12}=1/4,e_{13}=-1/4,e_{23}=0\).
7. Author noncommuting interior example.
8. Strong rare-event center: \(x=1/64,y=1/3,z=63/64\) with boundary-scale mixed signs.
9. Rare two-small center: \(x=1/64,y=1/32,z=1/2\) with mixed signs.
10. Rare near-one center: \(x=63/64,y=31/32,z=1/2\) with mixed signs.
11. Asymmetric interior center \(x=1/5,y=2/5,z=3/5\), all edges at \(1/4\).
12. Asymmetric interior center \(x=1/5,y=2/5,z=3/5\), signs \(+,+,-\).
13. Edge-boundary center with \(x=1/3,y=1/2,z=2/3\), only \(e_{23}=1/4\).
14. Connected center with \(e_{12}=0,e_{13}=1/4,e_{23}=1/4\).
15. Connected center with \(e_{13}=0,e_{12}=1/4,e_{23}=-1/4\).
16. All-edge tiny interaction center \(x=1/7,y=2/7,z=3/7\), \(e=(1/16,-1/16,1/32)\).
17--32. If no gap is found, repeat 1--16 under the six coordinate basis and mixed directions already encoded in the exact residual matrix tests rather than adding stochastic centers.

## Certificate computations

1. Symbolically verify all eight \(p,p',p''\) formulas and mass conservation.
2. Symbolically verify \(R\), \(g\), and \(p''/P_0\) against the eight probabilities.
3. Symbolically verify the Rayleigh square identity.
4. Symbolically verify the fixed-center acceleration identity by expanding the finite differences.
5. Build exact residual expressions for the author's algebraic inequalities where feasible:
   - strict contraction margin from diagonal dominance after normalization;
   - Fisher lower-bound constants;
   - \(C^2\) lower bound after using the stated \(|w_ew_f|\) estimate;
   - \(P T_*\) and \(Q T_*\) inequalities for representative edge pairs;
   - edge-diagonal Cauchy bound;
   - final rational coefficients and excess over \(7/10\).
6. For each directed rational center, compute the full \(6\times6\) Hessian matrix from the eight probabilities using interval logs; compare it with the \(7/10(\mathcal S+\mathcal U+\mathcal V)\) matrix when this is computationally practical. Otherwise record exact rational non-log pieces and high-precision diagnostic eigenvalues, with no global conclusion based on diagnostics alone.
7. Separately verify degeneration claims at all-zero, one-edge, and connected two-edge centers using exact symbolic specialization.

## Runtime and resources

- Remote working directory: the verifier's assigned isolated W4 directory under the C1 verification tree.
- Python: `/opt/venv/bin/python`.
- Target versions: Python 3.12.3, NumPy 2.1.2, mpmath 1.3.0, SymPy 1.13.3.
- One process, one computational thread, no GPU, initial wall-clock limit 600 seconds, memory limit 8 GiB.
- Save script, command, PID, environment versions, exit status, stdout/stderr, and copied-back artifacts.

Connection details are private and are not recorded in public artifacts.

## Stop conditions

Stop immediately and report `REFUTED` if a center and direction satisfies the frozen assumptions and violates T1, T2, or T3.

Stop and report `NEEDS_FIX` if a proof step needed for the universal theorem lacks a valid inequality, uses division by a possibly zero edge or probability, omits a six-dimensional direction, or proves only a non-affine path claim.

Report `ACCEPTED_SCOPED` only if the analytic proof chain survives line-by-line review and the independent certificate covers the stated high-risk identities and degeneracies.

Report `INCOMPLETE` if computation or time limits prevent resolving a承重 identity or degeneration claim.
