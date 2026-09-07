# Provenance

- T2 main: objective selection, hypothesis ownership, protocol, literature audit, computational helper and integration.
- construction: GPT-6 Astra high, isolated proof author; owns proofs/ in its own checkout.
- boundaries: GPT-6 Astra high, independent failure-family author; owns boundaries/.
- definitions_audit: GPT-5.5 xhigh, independent input/quantifier audit; owns audits/. This role does not certify the final proof.
- Final candidate verifier: not yet started; must receive a fixed statement and anonymous proof in a fresh context.

No child agent may delegate. Separate writable checkouts, capped CPU/memory per role, no GPU, no system dependency installation. Shared private launch data and credentials are excluded from this repository.
