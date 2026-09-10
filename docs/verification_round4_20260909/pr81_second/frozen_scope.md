# PR81 SECOND frozen scope

Role: independent SECOND verifier for PR81, static source review only.

Frozen head:

- PR81 head: `92c1b3dfd85c4be4f0ce13b59ffb51e6e0869eac`

Reviewed local inputs:

- `input/proof.md`
- `input/coupled_gram_fixed_shape.md`
- `pr70_source/proof.md`
- `pr70_source/thinning_bridge.md`
- `input_binding.json`

Hash and blob check:

| file | expected git blob | observed git blob | expected SHA256 | observed SHA256 | status |
| --- | --- | --- | --- | --- | --- |
| `input/coupled_gram_fixed_shape.md` | `d4ce531dcbe8aabc6ea0224b0642ac045d829987` | `d4ce531dcbe8aabc6ea0224b0642ac045d829987` | `d50f7cb0af86c26518a8f7dec03f7b98cb01de365853e2ba198c2d4322d130af` | `d50f7cb0af86c26518a8f7dec03f7b98cb01de365853e2ba198c2d4322d130af` | MATCH |
| `input/proof.md` | `ad51fb200fb44e888025507f57189d55ec7dbd1a` | `ad51fb200fb44e888025507f57189d55ec7dbd1a` | `2b6b61248552990bf93e9785b16b9b82656ba2b8aeb51b5bcfe315f4dbed8bfc` | `2b6b61248552990bf93e9785b16b9b82656ba2b8aeb51b5bcfe315f4dbed8bfc` | MATCH |
| `pr70_source/proof.md` | `5732657cd5e5ce87d2d2409a4556379228ae3145` | `5732657cd5e5ce87d2d2409a4556379228ae3145` | `aeab2fd328f922c2c5f19f1c1d11c44ba20ed5cfe88e746ae84b93f7228e1eaf` | `aeab2fd328f922c2c5f19f1c1d11c44ba20ed5cfe88e746ae84b93f7228e1eaf` | MATCH |
| `pr70_source/thinning_bridge.md` | `6e10862d47ca0e66c0fc0b468342688f6648f761` | `6e10862d47ca0e66c0fc0b468342688f6648f761` | `3b664d7872fcf172b7a2971dbaf3bde9db0eab0874f632d9c517ba742fdefa57` | `3b664d7872fcf172b7a2971dbaf3bde9db0eab0874f632d9c517ba742fdefa57` | MATCH |

Scope observed:

- Read only the four listed input/source files and `input_binding.json`.
- Treated the two PR70 files only as formula sources.
- Did not read FIRST reports, other SECOND reports, C3 opinions, public comments, or later live materials.
- Did not read any later p>8/live additions.
- Did not access forbidden private directories.
- Did not run checker code, Python, SymPy, finite enumeration, determinant expansion, or entropy recomputation.
- Did not create or delegate to subagents.

Method:

- Static line-by-line source review.
- Hash and git-blob verification only.
- No new arithmetic certification. Large rational fixed-shape derivative values, relaxed minors/determinants, and diagnostics are classified as `SOURCE_ONLY/PENDING`.

Not assessed:

- NOT_ASSESSED novelty.
- NOT_ASSESSED public-comment status.
- NOT_ASSESSED later live changes.

Not performed:

- NOT_PERFORMED formal verification.
- NOT_PERFORMED independent C2/checker certification.
- NOT_PERFORMED new determinant calculation.

