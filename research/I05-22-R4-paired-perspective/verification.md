# Verification, attempts and source boundary

Everything new in PR70 remains author-level and not independently reviewed.

## Executed exact checks

`verify_bridges.py` ran with SymPy 1.14.0 and reported about 4.12 seconds. It reconstructs the complete eight-event derivatives, the selected-side cofactor grouping, the congruence scale law, generic L/C/R coefficients including all mixed directions, the positive edge congruence, the quadratic perspective sum of squares, the full four-evaluation Gram identities and a noncommuting parallel-sum transport fixture. The universal parallel-sum identity is proved algebraically in the text; one fixture is not its proof. `outputs/bridge_checks.json` in the delivered package records the result. No old PR60 or r=0 script is imported.

`certify_obstruction.py` ran and produced `outputs/obstruction.json`. It uses the NEW event generator in verify_bridges.py, exact rational K,D,tau, all 24 scalar event jets, positive Sylvester minors for the three kernels and their complements, both side perspective curvatures, the full Fisher/acceleration Hessian and the genuine Jensen interval. Its only non-rational function is log, enclosed with the explicit 60-term tail in post_checkpoint.md (P7). Integer floor/ceiling supplies outward decimal bounds. Exact auxiliary signs have zero rounding error. Sharing the new event generator makes this a same-author cross-check, not an independent implementation.

`post_checks.py` ran after issue73 was opened and wrote `outputs/post_checks.json`. It checks the tail 2x2 determinant/trace identity, all four CT Bernoulli moments, and the scalar thinning derivatives -r and r^2/P with exact symbolic arithmetic. The actual analytic bounds and globally quantified equivalence are proved in tail_bound.md and thinning_bridge.md; the finite check is not a substitute.

Ordinary Python is required for all assert-based checks. Optimized `python -O` is not a verification mode. There is no CI run or proof-assistant result.

## Bounded exploration and retained failures

The initial single-side SCOUT used seed22604, 1000 shapes with x,y uniform[.02,.98], log10 A,B uniform[-2,3], q=1. A separate seed2260402 multiscale probe used 4000 shapes with leaf logits in [-7,7] and log10 A,B in [-3,6]. Neither located a surviving negative G1 direction. These are finite, non-rigorous probes; no global positivity conclusion follows. The base implementation is preserved in scout.py; transient complete floating point histories were not saved, and are not certificate inputs.

A q-derivative shortcut produced a floating negative proposal at seed2260403 (x about .6283,y about .4631,A about138.12,B about114.72). It was NOT rationally certified and is not a theorem or entropy counterexample. No q-monotonicity claim is used. A 300-point quadratic-perspective probe used seed2260404 before the exact squares were derived; that probe is not the proof.

The new complement-paired resolvent search used seed2260405, at most500 centers, x,y uniform[.02,.98], and a Dirichlet(.5,.5,.5,.5) partition for (q,A,B,qbar). It stopped at its fifth center. The exact rational reconstruction, not the floating location, is (P1)-(P7). Its negative resolvent sign survives but its one-sided and full-entropy signs do NOT violate the Shannon claim.

A subsequent 16-point diagnostic tested the stronger lower bound obtained by deleting the positive R from Y. Floating negative values showed that this shortcut was not promising; these values were not promoted to an exact method-refutation theorem. The actual argument retains R and the complete Fisher. Its small script is test_core.py in the delivered package. The original fixed-three-diagonal EDGE-radial Loewner route was not restarted.

Two proof obstacles are now explicit rather than recycled assumptions: perspective convexity for affine masses does not handle the r'' and P'' terms on K-affine paths; and independent minimization of the two sides loses the positive parallel-sum mismatch square. Neither issue may be solved by dropping rare events, the triple atom, or marginal Fisher.

## Correction log

The first public proof had face0 instead of face1 only in the unweighted N0 positive decomposition. The weighted N_s and all matrices were correct. Commit8c3f4a145c350645f522cfab0b5841b7d4dcec25 fixes the index and explains k_face0-V0=k_face1. The original checkpoint remains in history. No nonauthor review is claimed for the correction.

## Primary sources and exact bridges

Boyd--Vandenberghe's official book page is https://web.stanford.edu/~boyd/cvxbook/ ; section3.2.6 is the scalar perspective background. The second-derivative formula in proof.md (7) explicitly supplies the otherwise missing acceleration terms for this task.

Djalil Chafai's original paper is https://arxiv.org/abs/math/0211103 , *Entropies, convexity, and functional inequalities*. The author's later account https://djalil.chafai.net/blog/2025/01/25/about-variance-and-entropy/ states the Phi-entropy/inverse-second-derivative convexity conditions. Those results concern their specified fixed-measure function arguments, not automatically the nonlinear event map K to (P,r). No tensorization or matrix-entropy theorem is invoked without that missing bridge.

Anderson--Duffin's original *Series and parallel addition of matrices*, JMAA26(1969)576–594, DOI10.1016/0022-247X(69)90200-5, has publisher entry https://www.sciencedirect.com/science/article/pii/0022247X69902005 . Its nonsingular positive-matrix parallel sum is applicable because both L_s are proved positive. Proof.md (14)-(15) derives the precise DPP compensation rather than claiming the source proves DPP concavity.

The primary-source hypotheses and the new DPP derivations are separate. No novelty claim or Quarez open-domain existence shortcut is used.

## Publication and computation

GitHub accepted the first proof and bridge verifier. Creation of the second, distinct obstruction verifier was blocked by a tool safety-state check; the same code was not submitted via another GitHub API. The specifically authorized Drive fallback was attempted, succeeded and was read back. No sharing permission was changed or bypassed. The complete user-delivered ZIP contains the source and exact outputs; the public post-checkpoint proof provides all values and formulas needed for independent reconstruction. The post-check script is local-package material, not falsely listed as a public repository file.

Issue73 contains actual frozen mathematical files and literal rational inputs, algorithm, independent certificate gates, one shared45-minute ceiling,16GiB/one CPU/no GPU limits, and stopping rules. Its 273 fixed points on three q-filaments were not run in this author session. No new full determinant expansion, heavy interval enumeration, or unbounded process was left running.
