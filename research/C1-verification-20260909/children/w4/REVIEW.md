# W4 independent review verdict

Verdict: `ACCEPTED_SCOPED`.

I certify the PR33 frozen T1--T3 theorem in the scope stated in `frozen_statement.md` lines 28--59, with the exclusions in lines 61--68. This review does not certify the original all-kernel three-dimensional target in lines 5--26, novelty, PR30, the checkpoint-only PR33 update, or any second-round conjectural plan.

## Scope reviewed

The accepted statement is exactly:

- \(0<x_i<1\) and \(|K_{ij}|\le (1/4)\sqrt{x_i(1-x_i)x_j(1-x_j)}\);
- all real symmetric six-coordinate directions \(D\) along the true \(K+tD\) affine path;
- the coercive bound
  \[
  -H''(K;D)\ge {7\over10}(\mathcal S+\mathcal U+\mathcal V);
  \]
- convexity and closure chord concavity for this \(\Omega\);
- full Hessian negative definiteness when the nonzero edge graph is connected.

## Analytic review

The eight event formulas and K-affine derivatives in `proof.md` lines 7--75 are consistent with the inclusion-probability determinant formulas. The off-diagonal coordinate convention in line 17 is used consistently: \(h_{ij}\) is the derivative of the matrix entry \(K_{ij}\), not a doubled basis coefficient. The displayed \(r'\) and \(r''\) formulas in lines 48--56 include the diagonal-edge and edge-edge mixed terms needed for a true \(K+tD\) path.

The proof of strict interior validity in lines 112--156 is sound. The normalization \(e_{ij}=K_{ij}/\sqrt{v_iv_j}\) is harmless because \(0<x_i<1\). The quadratic-form comparison in lines 120--130 gives both \(K>0\) and \(I-K>0\) with no uniform spectral margin assumption. The density formula (5) in lines 133--141 reconstructs all eight probabilities against the Bernoulli product law, and the uniform lower bound \(R\ge25/32\) in lines 143--153 controls rare events without dividing by \(\min x_i\), \(\min(1-x_i)\), or a nonzero edge.

The full Fisher lower bound in lines 158--229 retains the three-point coefficient. The term \(2C-\lambda\cdot t\) in (8) includes the \(-d_iK_{jk}^2\) coupling, so the proof is not using a reduced two-point Fisher projection. The estimates \(|w_ew_f|\le(\varepsilon^2/4)|u_eu_f|\), \(C^2\ge\mathcal V-(\varepsilon^2/2)\mathcal U\), and \(\|\lambda\|^2\le3\varepsilon^4/16\) are valid also when some edge is zero, because they do not divide by \(u_e,w_e\), or the cycle product.

The conditional Rayleigh square in lines 231--275 is valid as a real-square identity. Since \(R\ge m>0\), the logarithmic comparison uses only \(\log(1+q)\le q\) with \(q\ge0\); no sign or edge nonvanishing assumption is hidden. The three-point log-ratio bound in lines 277--335 is also sound: differentiating \(\log R\) on the continuous rectangle is legitimate under \(R\ge m\), and the constants \(C_P=81408/15625<6\), \(C_Q=63488/15625<5\) match the rational recomputation.

The acceleration identity (19), lines 337--369, correctly follows from the fixed-center second density derivative and finite differences. The diagonal coupling estimate (20), the two-edge estimates (21)--(22), and the edge-diagonal estimate (23) in lines 371--447 all keep the signs and absolute values in the right direction. In particular, the \(Q T_*\) estimate in lines 409--420 is acceptable: for each edge pair, the first \(Q\)-term is split between \(|u_ew_f|\) and \(|u_fw_e|\), the other two terms use the corresponding single representation, and the final sum uses the spectral norm \(2\) of \(J-I\).

The coefficient merge in lines 451--485 is correct:

- \(c_S=3643291/4992000=7/10+148891/4992000\);
- \(c_U=25029/13312=7/10+78553/66560\);
- \(c_V=439/624=7/10+11/3120\).

Thus T1 follows for all six real symmetric directions. T2 follows from the convexity argument and continuity passage in lines 487--508; the closure claim is only the chord inequality, not a boundary Hessian claim. T3 follows from lines 510--514: if the edge graph is connected, \(\mathcal S+\mathcal U+\mathcal V\) is positive for every nonzero six-coordinate direction; with exactly two nonzero edges, the missing edge direction is controlled by the \(\mathcal V\) term.

## Computation record

The planned scope and computation plan were frozen before running certificates:

- `frozen_scope.md`
- `COMPUTE_PLAN.md`

The first full exact-fraction interval attempt is not accepted as a completed certificate. It is preserved in `REMOTE_TIMEOUT_001.md` and `timeout_full_attempt/`: recorded PID `167814`, one thread, `ulimit -v 8388608`, command `timeout 600 /opt/venv/bin/python independent_w4_certificate.py`, exit status `124`. This was a certificate-engine timeout, not a theorem refutation.

The first minimized decimal interval attempt is also not accepted as a strict interval certificate. It is preserved in `REJECTED_INTERVAL_ATTEMPT.md` and `rejected_interval_attempt_default_reciprocal/`. The defect was only in the verifier implementation: reciprocal endpoints in decimal interval division used the default Decimal context instead of directed 90-digit rounding.

The corrected minimized certificate is accepted as supporting evidence. It used remote PID `169057`, one thread, `ulimit -v 8388608`, command `timeout 240 /opt/venv/bin/python -u minimal_w4_certificate.py`, Python 3.12.3, NumPy 2.1.2, SymPy 1.13.3, and exit status `0`. The script reconstructs the eight probabilities from \(q_{ij}\) and \(r\), forms the six-dimensional Hessian matrix from the eight probabilities, wraps rational logs by an atanh series, converts the rational log intervals to 90-digit directed decimal intervals, and applies interval LDL on the active residual matrix.

The seven fixed centers all passed:

- balanced all-zero edge center, with symbolic zero rows for all three edge directions;
- balanced three-edge positive boundary;
- balanced three-edge mixed-sign boundary;
- balanced one-edge center, with symbolic zero rows for the two isolated-connection directions;
- balanced two-edge connected path, where the missing edge direction is active through \(\mathcal V\);
- rare opposite-diagonal boundary-scale center;
- the author's noncommuting interior example.

The smallest strict interval LDL lower pivot among connected or active blocks was positive: `0.00517864165181461157193428676228294516959633625481198690899752267875646883842690859259974011` for the balanced two-edge path. The stage files and summary are:

- `minimal_run_metadata.txt`
- `minimal_exit_status.txt`
- `minimal_run_stdout.txt`
- `minimal_run_stderr.txt`
- `minimal_certificate_summary.json`
- `minimal_stage_*.json`

## Remaining obligations

No remaining obligation blocks acceptance of frozen T1--T3 on \(\Omega\).

The following remain outside this scoped acceptance:

- the original general real three-dimensional strict contraction claim outside \(\Omega\);
- \(n>3\), complex Hermitian kernels, and scalar stationary entropy-rate claims;
- novelty or literature priority;
- PR30 self-acceptance;
- any theorem not present in the PR33 frozen statement/proof body, including checkpoint-only second-round plans.

READY for C3 integration.
