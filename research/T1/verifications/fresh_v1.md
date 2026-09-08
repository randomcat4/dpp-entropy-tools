STATUS: CORRECT

# Fresh v1 frozen verification

Verifier scope: frozen object at commit `a71d52bc8c5b45df9ea4795343c290899a2d1f84`.
I read only the repository instructions/prompts, frozen theorem, proof, hazard ledger,
lemma ledger, checker source, and the two named checker inputs. I did not read
provenance or exploration files. I did not revise the theorem or proof.

## Files and hashes

| File | SHA256 |
| --- | --- |
| `AGENTS.md` | `855fddb5b3a6619a0522d674ae700396fc25d975646eafc38cec5f4981979113` |
| `prompts/COMMON.md` | `f9f6943b811766b8777879c7e2cc2c984e8846f6226e2fcceb365bac3968d522` |
| `prompts/T1.md` | `a8a9a5335311a8bdd088cf7e75a0cc87c1f323d998512053698c1b207dacc7b7` |
| `research/T1/frozen_theorem_v1.md` | `94ebb6017e5e185552806739d29ec40333bfcfae9706fd1965c8a1a3d0da89de` |
| `research/T1/proofs/criterion_v1.md` | `141f626b3ffea65607da9a2ed48fe6235bf1db4f9158751998c90ee23013f416` |
| `research/T1/hazards.md` | `3832ce03d9f0cda17a6b73f6694879e588beb897608283d5673b1928628416e2` |
| `research/T1/lemma_ledger.md` | `4527a2a45b79623c608f351a7177c9f030e9a18fc159e174528488e931c5b842` |
| `research/T1/tools/bridge_check.py` | `cc282e1d5062caa3c77db915ea0de1220814df1dea11dde02182d9d8aad60b92` |
| `research/T1/tools/validate_bridge.py` | `73f2819bb14db30c5f32a812241533c9eaa932c5ca058fe8903d2457cf2797b9` |
| `research/T1/artifacts/triangles_2.json` | `33fc7a4a01efe14b074095d0f3ba07eb43e7c85b443b81052512d42093e903b6` |
| `research/T1/artifacts/triangles_10.json` | `e33f9b047132891205ac7f09f147a4cf431a386fd0e1538b60b3928848c6d08f` |

## Mathematical verification

The frozen theorem in `research/T1/frozen_theorem_v1.md:5-29` quantifies over
strict real symmetric contractions `0 < K < I` and imaginary Hermitian
directions `D=iA` whose support is contained in existing bridge edges of the
off-diagonal support graph. The proof in
`research/T1/proofs/criterion_v1.md` proves the same statement, including the
strict equality case.

For the signed Schur-complement conditioning step, lines 13-28 are valid. For
fixed `T subset R`, `w_T=(-1)^{|R\T|} det Q_T` is the exact probability of
`X intersect R=T` under the marginal kernel `K_R`, hence positive in the strict
interior. Since `R` excludes the two bridge endpoints, both `Q_T` and `w_T` are
independent of the bridge weight `z`. The determinant factorization gives

`p_{T union E}/w_T = (-1)^{|U\E|} det(M_T-I_{U\E})`,

with the stated signs: the sign from `R\T` is absorbed into `w_T`, and the
remaining sign is exactly the endpoint event sign. The bridge partition makes
`Q_T` block diagonal and the `u` and `v` rows meet disjoint blocks, so the
Schur correction is diagonal and independent of `z`. I find no hidden
conditioning dependence on `z`.

The conditional two-endpoint table in lines 34-41 is correct:
`r_11=ab-q`, `r_10=a(1-b)+q`, `r_01=(1-a)b+q`, and
`r_00=(1-a)(1-b)-q`. These four values are positive because they are full
positive event probabilities divided by `w_T`, and they sum to one. Expanding
exactly gives

`r_11 r_00 - r_10 r_01 = -q`.

Since each bridge has original `q=|z|^2>0`, this implies
`0 < (r_11 r_00)/(r_10 r_01) < 1`, so the entropy derivative with respect to
the bridge squared magnitude is strictly negative as claimed in lines 43-60.
This verifies the strict negative sign.

The multi-bridge reduction in lines 62-77 also matches the frozen premises.
In any determinant permutation term, a bridge edge can appear only as the
two-cycle product `K_uv K_vu`; a longer cycle through that edge would be an
undirected support cycle and contradict bridgehood. Thus every event
probability, and therefore entropy, depends on bridge phases only through the
local variables `q_e=|K_uv|^2`. Along the frozen affine path,
`q_e(t)=K_uv^2+t^2 A_uv^2`, so `q'_e(0)=0` and all Hessian-in-`q` cross terms
drop from the second derivative. The chain rule gives

`H''(K)[iA] = 2 sum_e A_uv^2 partial_e F(q)`.

Each nonzero active bridge contributes a strictly negative term, while the zero
direction contributes none. This proves `H'' <= 0` with equality if and only if
`D=0`.

Boundary and zero-direction cases are handled within the stated theorem. The
proof uses strict interior positivity in lines 5-9, 41, and 67; it does not
differentiate through zero event probabilities. The theorem itself excludes
boundary kernels and new edges in `frozen_theorem_v1.md:28-29`. The zero
direction is handled in `criterion_v1.md:77` and by the checker.

The application family in lines 84-87 is covered: Gershgorin gives
`0 < (1/2)I + epsilon W < I` when `epsilon R_* < 1/2`, and the tree of single
interblock links makes each such link a support bridge even when the individual
blocks are dense.

## Checker verification

`research/T1/tools/bridge_check.py` enforces the frozen input domain
conservatively:

- exact rational input only; floats are rejected at lines 7-15;
- real symmetry and real skew-symmetry are checked at lines 77-80;
- strict `K > 0` and `I-K > 0` are checked by exact rational LDL pivots at
  lines 18-32 and 81-84;
- the support graph is built from exact nonzero off-diagonal entries at lines
  35-39;
- active direction entries outside the bridge set are rejected as
  `INCONCLUSIVE` at lines 86-90;
- accepted inputs report only `negative` for nonzero active bridge support and
  `zero` for the zero direction, with zero event probabilities evaluated, at
  lines 91-96.

The checker does not falsely certify cyclic edges, absent edges, non-strict
kernels, floating inputs, nonsymmetric `K`, nonskew `A`, or malformed
dimensions in the tests I ran. These tests are not a mathematical proof of the
theorem; they are a domain-regression audit for the exact checker.

Additional verifier-only outputs:

- `research/T1/verifications/fresh_v1/logs/validate_bridge.stdout.json`:
  copied bundled validator passed, including 75 graph cases and a 64-event
  float64 diagnostic with negative curvature.
- `research/T1/verifications/fresh_v1/logs/adversarial_tests.stdout.json`:
  extra adversarial cases passed, including provided `triangles_2` and
  `triangles_10`, disconnected graphs with isolated vertices, a path with two
  active bridges, zero direction, cyclic active edge rejection, absent active
  edge rejection, malformed inputs, and exhaustive bridge checks for all simple
  graphs on `n <= 5` vertices, 1099 graph cases total.

The bundled validator was run from a copied `fresh_v1/tools/` directory so the
audited source files and audited artifact inputs were not overwritten.

No Lean project files (`lean-toolchain`, `lakefile.*`, or `.lean`) were present
in the pinned checkout. No Lean or other machine-checked formal verification
was performed.

## Limits

This report certifies the frozen-v1 proof and exact applicability checker at
the pinned commit only. It does not certify novelty, cyclic-edge directions,
real directions, boundary kernels, stationary entropy rates, global concavity,
or any nonrational measured-input support certificate.
