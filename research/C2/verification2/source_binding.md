# Frozen source binding

W3 v1.0 was read from the actual harvested first-round result. This directory includes byte-preserving source copies. Git blob identifiers:

| Source | Git blob |
|---|---|
| sources/W3/frozen_statement.md | 6678e3db6e47ef548362fdd6e7ef9626dad6e2da |
| sources/W3/proof.md | e985c56d258c7f08ff159960f59fac57e3c8692d |
| sources/W3/code/verify.py | 485ea7fe663256d40173bef7b272cf0f28a5bdaa |

The W3 target is exactly T1/T2/T3 of this frozen statement. In particular, no available source here claims to prove the full band 1/4 I <= A <= 3/4 I.

PR30 is bound to head 94d67909bf8c1ea06da6350cf7907d6665cb166a. PR24 dependency head is e988aa3003484f6368133b8bc0c668331629e369. The three dependency files in dependency_binding.json are exactly the same bytes at both heads. Sources were obtained from GitHub's API at explicit refs, without relying on a moving branch or an uncommitted author checkout.

This is source-version identification, not a new checksum manifest. No private conversations, server connection details or credentials are included.
