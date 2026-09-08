# Generated certificate artifact

`segment_hessian_certificate.py` deterministically regenerates
`segment_certificate.json`.  The expanded file is 14,575,244 bytes and is
kept out of Git to avoid committing a large mechanical interval trace.  Its
audited local SHA-256 is

```text
f7279f823b8931bf474c4b9036f7ccfafadac59ad2c6c8d8c019120a86a5c169
```

The independently generated compact record
`verifications/fresh_s8_audit.json` is tracked.  It contains the certified
interval, all independent leaf summaries needed for the verdict, exact
structural checks, and hashes.  The non-author report records the matching
locations and hash of the expanded author artifact.

The S8b independent checker likewise regenerates an expanded 6,542,798-byte
leaf-by-leaf interval trace, which is excluded from Git.  Its audited local
SHA-256 is

```text
0b8e9a81a242a501801c01c95b7839687ce4d3de9653ed4c6b509f1e2751e157
```

The tracked `s8b_preconditioned_certificate.json`, independent checker, and
fresh audit report retain the complete reproducible inputs, author leaf data,
summary counts, and verification method.
