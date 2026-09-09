# N3 round2 independent review v2

Reviewer: `N3/children/review`, branch `research/N3-review-20260909`.

Status summary:

- `CORRECT`, within stated scope, for the round2 definition rebuild and exact formula checks in `round2_review_v1.md`.
- `CORRECT`, within stated scope, for the fixed dense weak-edge beta-nonzero mechanism at `3087eb189237ec0a2d60127d0c35128f0cbcd91c`.
- `CORRECT`, within stated scope, for the beta-zero root bracket certificate at `ab914ec2f73577907314ab3119c4d9f499b17e10`.
- `CORRECT`, within stated scope, for the locked-odds dominance obstruction at `c6568dfe1c0c57aaf0b627e84601c35b79b22434`.
- `CORRECT`, within stated scope, for the auxiliary Lambda-tangent acceleration-sign shortcut obstruction at `2af6538`.
- `CORRECT_WITH_ADDENDUM` for the locked-odds Fisher lower-bound degeneracy convention: use the addendum `0b6c89ef15db01385a37302e78509e0203838a74` rather than the superseded degeneracy wording in `99205d9ac552355c148f011bb053731a8b1349f0`.
- `CRITICAL_GAPS` remain for the global B0 implication and the full N3 theorem. None of the audited auxiliary obstructions proves the main target.

## 1. Definition rebuild and weak-edge candidate

The first round2 unit is frozen in this review branch at commit `89d3542`. The report and scripts are:

- `round2_review_v1.md`
- `verify_round2_definitions.py`
- `verify_weak_edge_candidate.py`
- `round2_definition_audit_results.json`
- `weak_edge_audit_results.json`

The definition rebuild independently reconstructed the eight event probabilities, the six-coordinate Jacobian, full Fisher `F`, projected `F_pair`, `v_score`, `N`, `H`, `alpha`, `beta`, and `gamma`. It also checked:

- `beta=0` means `grad(Lambda)^T H^-1 c=0`, because `Z=sum 1/p_M>0`;
- the real principal-minor identities `u=a^2`, `v=b^2`, `w=c^2`, `T=2abc`, `T^2=4uvw`;
- affine first and second derivatives of those polynomial identities;
- the full Rayleigh square polynomial, including zero-edge branches, without division by an edge or by `T`.

The weak-edge audit targets `research/N3/round2/main/dense_weak_edge_beta_v1.md` at `3087eb189237ec0a2d60127d0c35128f0cbcd91c`, blob `6a69ce2ba0ecc0f0826489501f126356708778f5`. I checked the exact density identity

```text
p/mu = 1 - t^2 sum edge^2 chi_i chi_j + 2t^3abc chi_123
```

for both `abc` signs, and independently checked the off-diagonal factor two in `eta_off`, the `Htilde` scaling, the degenerating block solve consistency, and the stated leading terms against fixed small rational `t` values `1/100`, `1/200`, and `1/400`.

This weak-edge verdict should be read narrowly. The exact density and coordinate/factor checks are algebraic; the `F_do=O(t^3)`, `H_do=O(t^3)`, block inverse, and remainder behavior were checked by formula reconstruction plus deterministic fixed probes, not by a uniform symbolic remainder theorem. Thus I accept the candidate as a bounded fixed-object review of the displayed local mechanism, not as a standalone global asymptotic theorem and not as evidence for B0.

## 2. Beta-zero root certificate

Frozen object:

- Commit: `ab914ec2f73577907314ab3119c4d9f499b17e10`
- Main text: `research/N3/round2/falsification/beta_zero_existence.md`, blob `d06a87b9bc5b063a569990637aa704348845228f`
- Script: `research/N3/round2/falsification/beta_root_certificate.py`, blob `09ec56673a10bbd66bfab8e073ab387a4fa32fa7`
- Certificate: `research/N3/round2/falsification/root_certificate.json`, blob `e9866bd449bdad849a832dea76d679303b74b108`

Verdict: `CORRECT` for existence of at least one beta-zero point in the certified bracket with `d alpha < 1`.

The review script `verify_beta_root_certificate.py` extracted the fixed source into a temporary review-owned tree and reran the author script exactly. The author rerun exited `0` and recorded PID `47096`; the review script PID was `37660`. Critical certificate fields matched the frozen JSON.

Independent checks:

- event probabilities and six-coordinate Jacobian matched the Mobius/principal-minor rebuild exactly on five rational samples;
- 120 off-diagonal derivative checks confirmed the symmetric-coordinate factor two;
- `Htilde=d*F_pair+T` and `d alpha = ae^T Htilde^-1 ae` matched the unscaled `H=F_pair+T/d` formulation;
- all log bounds enclosed high-precision logarithms;
- the interval Gaussian pivots excluded zero, interval residuals contained zero, and high-precision left/mid/right solves lay inside the bracket interval solve enclosure;
- the whole bracket, not just a single point, satisfies `dalpha < 1`;
- the kernel is strict, connected, and nonexchangeable throughout the bracket by exact endpoint feasibility and fixed nonzero edges.

Certified root bracket:

```text
L = 39791754487/17592186044416
U = 79583508975/35184372088832
```

Endpoint signs and bracket bound:

```text
beta_times_sqrtZ(L) < -1.2060485881542082e-13
beta_times_sqrtZ(U) >  8.448079036569667e-14
0.6615279258817643 < d alpha < 0.6615279260967083 < 1
```

This proves existence by continuity on the certified strict bracket. It does not prove uniqueness of the beta zero, describe the rest of the zero set, or prove B0 globally.

## 3. Locked-odds dominance obstruction

Frozen object:

- Commit: `c6568dfe1c0c57aaf0b627e84601c35b79b22434`
- Main text: `research/N3/round2/falsification/locked_obstruction.md`, blob `58b4370e2ff182b784c74f36df44ee72d97704e7`
- Script: `research/N3/round2/falsification/locked_certificate.py`, blob `96cef39412aa31bbcdd833293e95fb690462ef2f`
- Certificate: `research/N3/round2/falsification/locked_certificate.json`, blob `39fbc8fd65d8b7eb624b8a40f2fd2c1bd97c2d04`

Verdict: `CORRECT` for the stated disproof of the proposed dominance condition

```text
Lambda'[D]=0  =>  max_k Q_k^lock(D) >= C(D).
```

The review script `verify_locked_obstruction.py` reran the frozen certificate in a temporary review tree. The author rerun exited `0` and recorded PID `42080`; the review script PID was `23608`. Critical fields matched the frozen JSON.

Independent exact checks:

- the rational direction has exact `g^T D=0`;
- the two conditional log-odds derivatives agree in each of the three conditioning coordinates;
- all three `Q_k^lock(D)` values and the full event Fisher value match the certificate exactly;
- the valid lower bound `F >= Q_k^lock` is retained for all three `k`;
- the certificate's log interval comparison encloses `C`;
- feasibility of `K +/- D/1000` holds by exact leading-principal-minor tests for both `M` and `I-M`;
- the witness kernel is strict and connected.

Numerical scale:

```text
Qlock = 2.0683658531882963,
        5.479391817458416,
        5.479397081693769
F     = 59.136130254968334
max Qlock - C < -0.48245047048164097
B=F-C > 53.17428270279292
```

This refutes the `max Qlock >= C` closure and also any convex combination using only the same three `Q_k^lock` terms at this `K,D`. It does not refute the Fisher lower bound itself and does not decide B0.

## 4. Lambda-tangent signshortcut and locked-odds degeneracy

Signshortcut frozen object:

- Commit: `2af6538`
- Main text: `research/N3/round2/main/lambda_tangent_sign_obstruction_v1.md`, blob `32cf1fab49584098f5b52794a7da128b4f090894`
- Script: `research/N3/round2/main/lambda_tangent_certificate.py`, blob `057a98709e54a5cac5ec8a77b7f29167bdecc1a2`
- Certificate: `research/N3/round2/main/lambda_tangent_certificate.json`, blob `5693bd52ec97b6b5f9b5be9532e0fc9d267fa33c`

Verdict: `CORRECT` for the auxiliary claim that the pure acceleration-sign shortcut fails on an exact Lambda-tangent direction.

The review script `verify_signshortcut_and_degeneracy.py` reran the frozen signshortcut certificate. The author rerun exited `0` and recorded PID `29592`; the review script PID was `65244`. I independently checked exact strictness, `Lambda'[D]=0`, Fisher, positive `C`, positive true `B`, log enclosures, and all three Rayleigh square coefficient records. The certified scale is:

```text
0.376241571363 <= C(D) <= 0.376241571364
12.007687710971 <= B(D,D) <= 12.007687710972
```

This refutes only the shortcut `full real square identities + Lambda'[D]=0 => C(D)<=0`. It is not a beta-zero witness and not a B0 counterexample.

Locked-odds lemma and addendum:

- Historical lemma commit: `99205d9ac552355c148f011bb053731a8b1349f0`, `lambda_tangent_locked_odds_lemma.md`, blob `16aeb3460135815e5d8a4df61bc07941a5d58348`
- Degeneracy addendum commit: `0b6c89ef15db01385a37302e78509e0203838a74`, `locked_odds_degeneracy_addendum.md`, blob `4727ad8271fe00f17655779d1fe764ab8d0843fc`

Verdict: `CORRECT_WITH_ADDENDUM`.

The original locked-odds Fisher lower bound `F >= Q_k^lock` is preserved. The addendum correctly supersedes the old degeneracy explanation:

- `V>0` and `R>=0`;
- `R=0` implies `psi=(m/V)g`, not that the covariance root is zero;
- if `R0+R1=0` and the Lambda lock holds, then `A0=A1`, so the final locked residual term is defined as `0` for the lower bound;
- no path-independent limiting value is claimed for arbitrary approaches to the degenerate point.

I checked the exact example `a=d=3`, `b=c=1`: here `delta=8`, `R=0`, and `psi=(m/V)g`. This confirms the important correction: `R=0` can occur with nonzero covariance root.

Pairing notation should be read as follows. In `L=<g, dot x - x dot m/m>`, the pairing is the ordinary bilinear pairing against the probability tangent. In the Fisher Gram discussion, the score is `s_r=dot x_r/x_r-dot m/m`, and the Fisher pairing uses the weights `x_r`. The two descriptions agree only after this score conversion; one should not multiply by `x` twice.

## 5. Failures and noncoverage

The failed runs were environment/setup failures, not mathematical counterevidence:

- `python verify_beta_root_certificate.py` exited `1` because the Windows `python` alias points to the Microsoft Store stub.
- The bundled Codex Python exited `1` on the same script because `mpmath` was unavailable.
- A manual author-rerun shell draft using recursive cleanup was rejected by automatic command safety before execution.
- Empty-directory cleanup for an accidental temporary path was also rejected by automatic command safety; the misplaced file itself was moved into the review checkout and no source file remains there.
- `verify_signshortcut_and_degeneracy.py` first exited `1` because the temporary signshortcut tree omitted the old `research/R3/.../rank_one_recheck.py` dependency.
- Its second run exited `1` because extracting the full old R3 directory hit the Windows path-length limit; the final run extracted only the two needed R3 files and passed.
- Earlier weak-edge verification had one failed JSON serialization run before the `numpy.bool_` conversion patch; the patched deterministic rerun passed.

No GPU was used, no package was installed, and no system dependency was changed. All successful proof-bearing reruns used one-thread environment settings.

Uncovered objects and limits:

- no Lean/formal proof audit;
- no uniqueness or full classification of beta zeros;
- no global B0 proof;
- no expanded kernel family search beyond the fixed frozen objects;
- no elevation of finite probes or boundary checks into a full theorem.

The public background source I used for the real principal-minor/Rayleigh-square context was Al Ahmadieh--Vinzant, arXiv:2105.13444; all certificate-bearing computations above were direct local reconstructions from the frozen files.
