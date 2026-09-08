# D10-M6 hazards

Author status: **HAZARD_LEDGER**.

1. **Finite scans are not the theorem.**  The scripts remove the random
   \(v\)-choice for sampled base points, but \((Q,\theta)\) remains a continuous
   domain.  A non-hit over `60384` or `83456` base points is only SCOUT.

2. **The first simplex scan is deprecated.**  The original
   `joint_probe_results.json` skipped singular full-support KKT points and must
   not be cited as an exact maximum certificate.  The repaired output is
   `joint_probe_results_v3.json`; it includes relative KKT residual checks, a
   regression check for the verifier matrix with true cone maximum \(0\), and a
   \(10^{14}\)-scaled positive regression case.

3. **Shepp--Olkin is imported only for the count distribution.**  It applies to
   \(N_t=|Y_t|\), the Poisson-binomial sum of independent spectral Bernoulli
   variables.  It does not imply concavity of \(H(Y_t)\) after the
   cardinality-preserving projection-DPP channel, and it does not control
   \(G_P(r)+G_P(s)\).

4. **The conditional term can curve upward.**  Run 1c found sampled points with
   \(\Psi''>0\), and the fresh review reports an interval-certified strict
   positive conditional-curvature example.  Thus \(\Psi''\le0\) is false.  Any
   proof must use the total count barrier.

5. **Componentwise raw-weight concavity is false.**  The D10-M5 singleton
   blocker remains valid.  The formulas for \(r_i''\) and \(s_i''\) do not have
   fixed signs under \(v\ge0\).

6. **Copositivity was checked numerically, not with intervals.**  The 3x3
   criterion is exact as algebra, but the present scan evaluates floating-point
   Hessians and margins.  Near-boundary atoms and logarithms need interval or
   high-precision certification before any candidate or proof step can be
   frozen.

7. **Orthostochastic coverage is not symbolic.**  Random Haar \(Q\)'s and
   structured Euler-angle products do not exhaust \(O(3)\).  A theorem needs an
   analytic parameterization or an invariant argument over the full
   orthostochastic image \(P=q^2\).

8. **Sphere support eigenvectors have degeneracy edge cases.**  For generic
   matrices, enumerating same-sign eigenvectors of all principal submatrices
   captures the positive-orthant sphere extrema.  Exact repeated-eigenvalue
   cases should be handled separately in a formal proof or by interval
   perturbation.

9. **Boundary supports need KKT care.**  For a full orthant-sphere local maximum
   on support \(I\), omitted coordinates must satisfy \((Mv)_j\le0\).  The
   sphere script records omitted gradients for diagnosis.  A positive value
   would still be a valid direction even if the point were not a local maximum,
   but mechanism classification should not ignore the condition.

10. **No strict positive candidate exists here.**  Since no \(H''>0\) point was
   found, this directory contains no high-precision feasible-chord certificate.
   If a future positive point appears, it must pass exact-event Möbius atoms,
   strict spectral feasibility, high-precision entropy, and central-difference
   gap checks before being advertised.

11. **Author-side status only.**  The reductions and scripts in this directory
    are not independently verified.  They should be handed to a fresh verifier
    before being used as a certified exclusion or counterexample claim.
