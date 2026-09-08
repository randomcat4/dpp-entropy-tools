# D10-S8d fresh nonauthor audit

STATUS: CORRECT for the stated half-open interval `-1 < t <= -29/100`.

This is a fresh verifier audit of the frozen S8d candidate only.  I did not import `negative_probe.py`, the older S8 certificate helper, or any author Hessian/gate module.  The verification script here rebuilds the exact-event probabilities by Möbius inclusion-exclusion and differentiates the full six-coordinate `Sym(3)` Hessian directly.

Non-claimed layers remain non-claimed:

- finite eigenvalue samples are SCOUT only;
- nothing is certified beyond `-1 < t <= -29/100`;
- the endpoint `t=-1` is excluded;
- no uniform neighborhood through `t=-1` is certified.

## Files written by this audit

- `fresh_audit.py`
- `fresh_audit.json`
- `fresh_audit.md`

Final successful command:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research\R3\deepening_10h\dense_hessian\n3_full_hessian_segment\s8d_negative_boundary_asymptotic\verifications\fresh_audit.py
exit code: 0
elapsed: 111.64809656143188 seconds
```

Development-run failures before the final pass were verifier-local only: one exit 1 from Python's big-integer string limit, one exit 1 from float display overflow for huge rational margins, and one interrupted slow trial before caching per-event log intervals.  These did not modify author files or change the mathematical checks.

## Frozen input hashes

| input | SHA256 |
|---|---|
| `frozen_problem.md` | `52c0851ba63169ad60825256f32de1f8bf1d13c7d72db55e44a4b4ec959dcc20` |
| `proof_or_counterexample_candidate.md` | `96a945e0488ce324dd8bb890a104a13fee0b7ca7f6c39b864add31ca77f85ee1` |
| `run_log.md` | `fae293c0fe51d1690a1f96b497f711c221317edb123ae9f5ec5854a7b72b79a4` |
| `verdict.md` | `82fd3fb9d7dbd3cc5f8018b1f8c1ed7cf6977f3c2692525161ca4092c46d8220` |
| `negative_probe.py` | `24912c62694b629f4081a458a6942f895384e51841bcfd6919145914ff9646b1` |
| `negative_results.json` | `7df360071af07b77c1e6ebdac95da5f7ca936a1fffe2b1bac90276cb1e83918d` |

The JSON status is `PROOF_CANDIDATE_PENDING_REVIEW`; this audit supplies the nonauthor check, not author self-certification.

## Feasibility and endpoint

The frozen line has eigen-coefficients

```text
lambda_U(t) = (1+t)/5
lambda_V(t) = 1/2 + t/3
lambda_W(t) = 4/5 + 2t/3
```

Therefore the exact strict feasible interval is

```text
-1 < t < 3/10.
```

The target `-1 < t <= -29/100` is inside this interval.  At `t=-1`, `lambda_U=0`, so strict feasibility fails; the proof correctly excludes that endpoint.

On the bridge interval `s=t+1 in [1/1000,71/100]`, the spectral floor is independently recovered as `1/5000`, attained by the `U` eigenvalue at `s=1/1000`.  On the analytic tail `0<s<=1/1000`, strict feasibility holds pointwise for every `s>0`, but no positive uniform spectral floor through `s=0` is claimed.

## Exact-event/Möbius reconstruction

CORRECT.

The verifier reconstructs all exact atoms from inclusion probabilities by

```text
p_S = sum_{A superset S} (-1)^{|A|-|S|} det K_A.
```

This is the exact-event semantics, not the principal-minor-as-event error.

In mask order `0,...,7`, the independently rebuilt endpoint atoms at `s=0` are

```text
(13/18, 289/3780, 79/945, 1/135, 361/3780, 1/135, 1/135, 0).
```

Orders at `s=0` are

```text
(0,0,0,0,0,0,0,1).
```

Thus only the full-set atom vanishes, and it vanishes linearly.  The full-set atom polynomial is exactly

```text
p_123(s) = s/225 + 7s^2/225 + 2s^3/45.
```

The frozen JSON's `left_kernel`, `direction`, `basis`, `gram`, endpoint atoms, orders, and atom polynomials all match the fresh reconstruction.

## Six-coordinate full Hessian basis

CORRECT.

The fixed basis is the one stated in the proof candidate:

```text
F0=U
F1=(uv^T+vu^T)/7
F2=(uw^T+wu^T)/11
F3=V
F4=W
F5=(vw^T+wv^T)/24
```

Its Frobenius Gram matrix is diagonal with entries

```text
(1, 12/7, 252/121, 1, 1, 49/24),
```

so it is a full basis of real `Sym(3)`.  It is not required to be orthonormal; invertibility is enough for negative definiteness of the quadratic form to be basis-invariant.

For `B=-Hess H`, the verifier uses

```text
B_ij = sum_S (p_{S,i} p_{S,j}/p_S + p_{S,ij} log p_S),
```

with `sum_S p_{S,ij}=0` checked as an exact polynomial identity.  The full-set gradient and Hessian in this basis match the candidate formulas:

```text
g=(ab,0,0,bc,ac,0),
h03=h30=b, h04=h40=a, h34=h43=c,
h11=-2br1, h22=-2ar2, h55=-2cr3.
```

The identity `p_{S,00} == 0` for all eight events is also checked exactly.

## Singular endpoint block

CORRECT.

Removing the full-set atom gives an analytic seven-atom regular part through `s=0`.  The finite endpoint block `C0=G(0)[3:6,3:6]` has independently certified positive Gershgorin margins, approximately

```text
(3.5841579630164317, 4.2480247952119345, 8.374258439972355).
```

This supports the candidate's scaled endpoint picture: one pole coordinate, two logarithmic coordinates, and a positive finite `3x3` block.  The certificate is not a raw eigenvalue bound for unscaled `B` at `s=0`, and the endpoint itself is not claimed.

## Analytic tail `0<s<=1/1000`

CORRECT.

The verifier independently rebuilds the Schur lower model over `[0,h]` using rational interval arithmetic and the same style of rigorous logarithm enclosure, with `N=24` atanh-series terms.  It checks the singular full-set atom separately and treats the other seven atoms as the analytic regular part.

For the certified tail width `h=1/1000`:

- all seven nonvanishing atom interval floors are positive, with minimum `1/135`;
- the logarithmic lower floor satisfies `Lmin > 2`;
- the monotonicity condition for `s`, `s w(s)`, and `s w(s)^2` is satisfied;
- the stored rational `5x5` preconditioner has positive diagonal and is upper triangular;
- exact interval congruence gives minimum transformed Gershgorin row margin approximately `0.20009961668473455`.

The proof's Schur logic checks out: `A=B00 >= (1/9)/s`; the row-zero coupling is bounded only after multiplying by the vanishing `s` from `1/A`; favorable full-set diagonal terms in the remaining block are kept only where lower-bounded and otherwise discarded as nonnegative diagonal remainder; the `(V,W)` full-set off-diagonal term is widened symmetrically.  Thus the interval model is a valid lower model, not a false bounded enclosure of the singular positive diagonal terms.

The wider `h=1/100` attempt has no accepted `P` and is recorded only as a coarse lower-model/proposal failure.  It is not a counterexample.  The narrower `h=1/10000` also passes, with minimum transformed margin approximately `0.9297282756099975`, but is unnecessary once `h=1/1000` passes.

## Bridge `1/1000 <= s <= 71/100`

CORRECT.

The verifier independently rebuilds the full eight-event interval Hessian on every accepted leaf, then applies the frozen rational `6x6` upper-triangular preconditioner `P` for that leaf.  It does not use midpoint floating eigenvalues to decide signs.

Bridge ledger:

```text
accepted leaves: 162
rejected internal nodes retained: 161
failed final leaves: 0
processed nodes: 323
coverage: [1/1000, 71/100] exactly, no gaps at shared endpoints
```

Independent exact checks:

```text
P invertibility failures: 0
fresh interval margin failures: 0
fresh atom-floor failures: 0
stored atom-floor mismatches vs fresh interval evaluation: 0
minimum fresh transformed row margin ≈ 0.009384781967274894
minimum exact atom lower bound = 11189/2500000000
bridge spectral floor = 1/5000
```

Since every leaf has all six transformed Gershgorin row margins positive and every `P` is invertible, each interval certifies positive definiteness of `B=-Hess H` throughout that leaf.  The exact no-gap cover then certifies the full bridge.

## Interior collision at `t=-9/10`

CORRECT.

At `t=-9/10`, `s=1/10`, the spectral coefficients satisfy

```text
lambda_U = 1/50,
lambda_V = lambda_W = 1/5.
```

The observation diagonals are all equal.  This does not invalidate the certificate: the proof uses a fixed full `Sym(3)` basis, not a moving distinct-eigenvalue chart.  The point is also inside accepted bridge leaf 35:

```text
[25071/256000, 1289/12800],
depth 8,
fresh transformed row margin ≈ 0.4069640894734083.
```

So the repeated spectrum/equal diagonal point is covered by the same fixed-basis interval certificate.

## Layered verdict

- Frozen input hashes: CORRECT.
- Exact feasible interval and excluded left endpoint: CORRECT.
- Exact-event/Möbius atoms and full-set linear vanishing: CORRECT.
- Six-coordinate full `Sym(3)` Hessian reconstruction: CORRECT.
- Singular endpoint jet and scaled endpoint sign model: CORRECT.
- Analytic tail `-1<t<=-999/1000`: CORRECT.
- Bridge `-999/1000<=t<=-29/100`: CORRECT.
- The combined half-open interval `-1<t<=-29/100`: CORRECT.
- Finite eigenvalue scouts: SCOUT only.
- Any theorem beyond the stated S8d interval: INCOMPLETE / not claimed.

No critical gap found.  The failed `h=.01` lower-model attempt is correctly classified as a method failure, not as evidence of positive curvature or a counterexample.
