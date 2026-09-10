# Failure, scope and evidence ledger

All entries concern author work. No independent review, stopped C2 run, or earlier PR80 evidence is relabeled by this packet.

## Mathematical failures and exact limits

1. **Uniform complement pairing away from half filling: DISPROVED.** For one two-coordinate mode background eta=1/3, the empty/full output pair has probabilities 2/3 and 1/3 conditional on the two input bits. It is not an input-independent selector. The repaired general local-channel theorem refines the output and retains an affine entropy correction; it does not retain the false uniform-weight shortcut.
2. **Every complete conditional fiber nonnegative: DISPROVED as a universal mechanism.** The earlier PR80 examples remain. MODE_FAMILY.md supplies an actual dense, internally correlated 3+3 example with a strictly negative complete conditional-KL curvature fiber, while its entire maximal chord is entropy-concave. This is not an entropy counterexample.
3. **Using the grouped-mode theorem to cover the original PR58 fixture: NOT APPLICABLE.** Nonzero row-pair minors of both original frames exclude the necessary proportional observed-column/row condition. WHOLE_CHORD.md instead proves the original fixture directly.
4. **General dense rank-two whole-chord concavity: INCOMPLETE.** The original fixture, its verified open neighborhood with moving maximal endpoints, and the grouped-channel families do not exhaust the parameter space. In the open-neighborhood theorem the radius is existential, not a matrix-entry error tolerance or a dimension-uniform radius.
5. **Novelty: NOT_ASSESSED.** The already accepted m-by-2 theorem is used as a premise, not claimed anew. Primary DPP and entropy-decay sources supply context only; every new entropy/channel bridge is proved in the packet.

## Author execution history

An early mode-law prototype used a Python integer division `/4` in an otherwise symbolic expression. Some local full/empty cases became binary floats and the intended exact polynomial equality test failed. It was changed to an explicit SymPy Rational(1,4). The repaired prototype checked all 64 polynomial identities. No literal stderr file from that earliest exploratory stop was retained; this is a disclosed development record, not fabricated raw evidence or a numerical entropy counterexample.

The initial exploratory whole-chord driver succeeded with one interval ending near the root and a separate explicit endpoint estimate. Its successful output remains in the local archive. A subsequent version replaced the cut by the simpler fixed rational 9993/10000, added a direct full principal-minor/Mobius reconstruction, separated the Fisher and signed-log budgets, and rounded each reported event lower bound downward. The final `verify_whole_chord.py` run succeeded; its literal stdout, empty stderr, exit0 record and full generated JSON are retained. No source fixture, comparison target or C2 stop-on-mismatch contract was altered.

The channel verifier had two preserved development stops:

- Attempt 1: `Poly.diff(2)` was used as if it meant a second derivative. SymPy interprets it as a generator specification and raised PolynomialError before the Hessian comparison. The fix is `Poly.diff().diff()`. The exact delta, literal stdout/stderr and exit1 are recorded below.
- Attempt 2: the asymmetric example used eta_left=1/3 while A0[1,1]=1/3, but the checker also required every observed internal edge to be nonzero. That edge cancels exactly, so the density assertion failed. The final asymmetric example uses eta_left=1/4, eta_right=2/3. This is a different auxiliary test fixture, explicitly disclosed; the original PR58 input is unchanged. The channel theorem itself does not require every edge to be nonzero.

The final `verify_channels.py` run passed all 16 refined-law polynomial identities, an exact full-Hessian identity with moving diagonals, all 64 half-background and 64 asymmetric-background observed event polynomials, and the explicit negative-fiber and endpoint checks. The reported numerical thread limit is one; there was no remote/server job and no independent arithmetic run.

`output/channel_development.txt` is a labeled concatenation of the two preserved attempts, not claimed to be one literal process stream. `code/development_failures.patch` records the exact source reversions from the final checker. The local artifact additionally contains the two full attempt source files and their separate raw stdout/stderr/exit records. Final `*_stdout.txt` files are literal saved stdout and `*_stderr.txt` are literal empty files, not edited PASS summaries.

## Independent gates

The accepted main W1 m-by-2 review is the only imported concavity theorem. PR80's earlier review freeze and issue93 request are not advanced automatically. PR94's new analytic and arithmetic units require a new explicit frozen review claim. An author executing a second algebra route, comparing exact outputs, or requesting review is not independent certification. No claimed failure of the general entropy conjecture occurs in this packet.
