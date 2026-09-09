# Round-Two Review Run Ledger

All runs used the bundled local Python runtime and wrote only under
`research/N4/round2/review/`. No server compute job was started for this review
unit.

## Completed Runs

| Artifact | PID | Exit | Script SHA-256 | Output SHA-256 | Calls |
|---|---:|---:|---|---|---:|
| `n5_projection_q_certificate.json` | 54680 | 0 | `b5d8cba12817158463c1eb9b0e6dfe7c1d6e87319e727e1ea9ce4f4ffdd07033` | `06080d98eabf5252480a9452190829a075b22b4ebf4ddc7f461bf89950cca4c2` | 10 log intervals |
| `finite_noncommuting_bsc_certificate.json` | 33400 | 0 | `876fb9c4d9a7421da1dc9f0133c85863fbd1464f0d28095f5b43b7ba16fac54b` | `75fdff9e32254630ae838335e28499c897c65f544864343828bac5479864dc1b` | 45 face log intervals; 48 lift log intervals |
| `coarse_identity_check.json` | 12864 | 0 | `3eabceb17c1cacb567e8e2b82849d1a365987a3b9f23063ac5e2c61737901fc5` | `116ae840799a3244aabf5129517a50e036477b7558dbb31f629b320997bf4572` | 16 event-polynomial comparisons |

## Failed Runs

None.

Two preliminary interactive attempts to feed Python through shell aliases failed
before any certificate computation because the default shell did not provide a
`python` executable. They wrote no files and are superseded by the completed
scripted runs above.

## Frozen Sources Reviewed

| File | Commit | Blob | Verdict |
|---|---|---|---|
| `research/N4/round2/coarse_event_candidate.md` | `3eabd9ba71ff24569a7d22ded4c3f159ef2ed89a` | `4c550633176ecd709e48a27a9b73212c6458c5b7` | `CORRECT_IDENTITY_ONLY` |
| `research/N4/round2/top_layer_budget.md` | `629d1fb1030d7d070ae719a0807f974f6a85ec98` | `915f894c28309b340e3112a56ffc5589c5ea8b60` | `CORRECT_BOUND_ONLY` |
| `research/N4/round2/frozen_theorem_v2.md` | `629d1fb1030d7d070ae719a0807f974f6a85ec98` | `6277e4fe5a9527f7714efacbd6e2a8e22de4b3d4` | scope reference only |
| `research/N4/round2/proof/support_lift_proof_v2.md` | `6126b5639e659c4a58710062e86540479614bed9` | `35dad0f51073b8617d01814222629534ccddf007` | `CORRECT` |

## Nonclaims

The finite noncommuting certificate is strictly negative on both the face chord
and the common BSC lift. It is not a counterexample. The n5 projection entropy
gate is only a reason to run the bounded five-point probe. The identity and
budget reviews do not prove face concavity.
