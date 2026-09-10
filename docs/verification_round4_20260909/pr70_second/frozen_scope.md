# PR70 frozen scope

Reviewer: independent non-author SECOND mathematical reviewer.

Frozen PR head: `f7be60759fd4d65184803b6585965dc7e5ccd624`, as declared in `input_binding.json`.

Repository: `randomcat4/dpp-entropy-tools`.

Owned output directory:
`docs/verification_round4_20260909/pr70_second`

## Files read

Only the PR70 author input bundle and its binding file were read for the mathematical review:

| File | Observed SHA-256 |
|---|---|
| `input_binding.json` | `5d9bdeae61659ea837ff82298ddbdd3dfd6d77d922b14baea3ea9f65ecec621d7b` |
| `input/README.md` | `c5cd2d02cb9804e040f4bed7fdd6a0c8993dc7a14b5decd648d9a4721b9e7304` |
| `input/inputs.json` | `c8ee511a142b72ef0c794c6eeb6b2ffa8b6cd974f7a6aaaea213ba31d57e4ef4` |
| `input/post_checkpoint.md` | `26e1d39fddf22dd369448777ecc288ae994c283fe8c51711e712bb6bf111084a` |
| `input/proof.md` | `aeab2fd328f922c2c5f19f1c1d11c44ba20ed5cfe88e746ae84b93f7228e1eaf` |
| `input/tail_bound.md` | `cf8ea71fb89dc7364577b8dac2ee60ffc4afb15c4e8097a5b90a923e9e8390ba` |
| `input/thinning_bridge.md` | `3b664d7872fcf172b7a2971dbaf3bde9db0eab0874f632d9c517ba742fdefa57` |
| `input/verification.md` | `1389a48241d2673a7c30ea727740c805d86f7e04a72948cf1a7c2f8eff587cbf` |
| `input/verify_bridges.py` | `3d7dc802ca1313bf9c6c45a09c0dea08f8b5f7d2f13547bdb0dbfd34890631b0` |

The eight author files' observed hashes match the hashes declared in `input_binding.json`.

## Review method

The review used plain source reads, SHA-256 binding, and static mathematical verification. I did not run the author checker, Python, SymPy, determinant rebuilds, entropy jobs, resource tests, or new computations. I did not use PR57/PR60 pending or accepted theorem statements as premises. Novelty is not assessed. Formal proof-assistant verification was not performed.

## Accepted analytic scope

The following are accepted as source-level mathematical identities, reductions, or scoped analytic theorems at PR70 head `f7be60759fd4d65184803b6585965dc7e5ccd624`:

1. Complete eight-atom event formulas, strict connected missing-edge domain, and the full six-physical-direction coordinate map.
2. Perspective second-derivative formula with the `r''` and `P''` acceleration terms retained.
3. One-sided cofactor formula and simultaneous `K,D` scaling law for `G1`.
4. The `L_s,C_s,R_s,Y_s` block decomposition, Lemma 1 positive `L_s`, Lemma 2 positive `Y_s`, and the corrected absent-side `N0` face-1 decomposition.
5. Exact parallel-sum compensation and the full marginal Fisher contribution.
6. The two-dimensional Schur targets, inertia/determinant equivalence, and the back-map from a negative two-vector to a physical six-direction.
7. Complete four-point Fisher inverse identities.
8. Complement and leaf-exchange symmetries of the paired full core, including equality surfaces in the reduced domain.
9. Strict full-six-direction quadratic-perspective sum of squares for `J2`.
10. Fixed-shape large-`q` one-sided tail bound, with its stated limitation that the threshold can lie outside a legal finite filament.
11. Thinning equivalence between global one-sided conditional-side nonnegativity and global conditional-entropy concavity, and the distinction from full Shannon entropy caused by the surviving leaf marginal Fisher.

## Exclusions and pending items

The following are not accepted by this review:

1. The fixed rational signs and decimal enclosures in `post_checkpoint.md`, including the claimed negative paired-resolvent curvature, positive side/full curvatures, legality minors for `tau=1/100000`, and negative Jensen interval. I inspected the specification, but the assignment reserves these numerical signs for a separate independent raw arithmetic owner.
2. Any general proof that `G1'' >= 0` on the full one-sided domain.
3. Any proof or disproof of the full missing-edge Shannon sign, equivalently the general determinant target `det E_H >= 0`.
4. Any finite result for the 273 requested issue73 inputs; `inputs.json` is a request/specification, not an executed or certified run.
5. Any novelty, publication-priority, CI, or formalization claim.

