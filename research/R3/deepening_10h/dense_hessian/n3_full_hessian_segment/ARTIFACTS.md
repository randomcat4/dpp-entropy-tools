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

The S8c author probe deterministically regenerates
`s8c_boundary_asymptotic/boundary_probe_results.json`. The expanded bridge and
endpoint-asymptotic trace is 4,802,765 bytes and is excluded from Git. Its
audited local SHA-256 is

```text
2c257777b29d33b38c1ae5de9c2e0aba775bf43e13ab5038dfbf41c361ee45da
```

The tracked independent checker and its compact JSON record reconstruct the
eight exact-event atoms, the six-coordinate Hessian, all bridge leaves and the
tail majorant without importing the author module. The fresh audit also binds
the expanded author artifact by the same hash.

The S8d author probe deterministically regenerates
`s8d_negative_boundary_asymptotic/negative_results.json`. Its full negative
bridge and endpoint-asymptotic trace is 44,894,276 bytes and is excluded from
Git. Its audited local SHA-256 is

```text
7df360071af07b77c1e6ebdac95da5f7ca936a1fffe2b1bac90276cb1e83918d
```

The fresh S8d verifier independently regenerates a 3,993,227-byte expanded
record at
`s8d_negative_boundary_asymptotic/verifications/fresh_audit.json`, also
excluded from Git. Its SHA-256 is

```text
f74269354c971ca1979a7abfe6318ce2680d23e026975e3d2304986eeeb026eb
```

The tracked author/verifier scripts and audit report retain the exact
construction, accepted/rejected leaf counts, minimum margins, dependency
hashes and reproduction commands.
