# Second-round source conditions

The coordinator's [reassessment, PR #25](https://github.com/randomcat4/dpp-entropy-tools/pull/25) was read before work. This round does not repeat an unrestricted literature search.

- [Lyons–Steif](https://arxiv.org/pdf/math/0204324), Conjecture 9.2 and Section 6: the original target is fixed scalar stationary entropy. Conditional entropy bounds must be applied to f_-tau,f_0,f_tau separately; real-valued does not imply an even symbol or real kernel. Their exact-event/conditioning framework supports complex Hermitian kernels.
- [Fan–Liao–Qiu](https://arxiv.org/pdf/1911.04718), Theorem 1.2: the sufficient bound requires both f in H^(1/2) and a uniform positive contraction margin. Finite trigonometric polynomials meet the tail condition. The bound addresses events in separated half-lines and does not assert a quantitative bound after conditioning on all intervening sites. It is not used as a replacement for the infinite-past residual proof.
- The round-one finite exact-event and variational residual proofs were independently reviewed. They have no evenness premise, but the round-one code's two-endpoint shortcut is a specialization and must be removed in the new three-symbol application.

No claim of new literature status or novelty follows from this targeted check. The one-complex-edge concavity argument is a direct conditional two-point calculation; no priority claim is made.
