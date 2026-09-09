# Provenance and review separation

- Upstream mathematical statements and author verifiers: public PR41 and PR43 at the commits frozen in README.md.
- C2 primary: freezes computational scope, owns issue 45, checks artifact provenance and public hygiene, assigns nonauthor review, publishes only this subtree.
- C2 PR41 child: independent computational reconstruction of upstream claims; owns `pr41/`.
- C2 PR43 event child: independent computational reconstruction of upstream fixtures; owns `pr43_events/`.
- C2 PR43 flow child: authors the single-input LP implementation and any new certificate; owns `pr43_flow/`. Self-check is explicitly not independent acceptance.
- Fresh certificate reviewer: to be assigned after a fixed candidate exists, using a freed child slot.
- C1: independent analytic proof review of the upstream theorem units; C2 does not duplicate or supersede that ownership.
- C3: sole main integrator and risk-based supplemental review coordinator.

Correctness, computational coverage and novelty receive separate status. No new novelty claim is made in this verification packet. Failures and source-version differences are retained.
