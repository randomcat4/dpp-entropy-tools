# Provenance

- T2 main: objective selection, hypothesis ownership, protocol, literature audit, computational helper and integration.
- construction: GPT-6 Astra high, isolated proof author; owns proofs/ in its own checkout.
- boundaries: GPT-6 Astra high, independent failure-family author; owns boundaries/.
- definitions_audit: GPT-5.5 xhigh, independent input/quantifier audit; owns audits/. This role does not certify the final proof.
- Final candidate verifier: fresh_verification, GPT-5.5 xhigh, spawned with fork_turns=none after the three first-stage roles completed. Received the fixed statement, proof, hazards and bounded source files; no creation context, prior audit verdict or social-confidence message. Read-only public candidate 31143e0925f95e1c05b2165a71c0d541a20be3ef. Own verification checkout and report; no source repair. The four named child contexts were sequential role replacement, with at most three active direct children and no grandchildren.

No child agent may delegate. Separate writable checkouts, capped CPU/memory per role, no GPU, no system dependency installation. Shared private launch data and credentials are excluded from this repository.
