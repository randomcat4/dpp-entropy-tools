# Review packet: N4 support and lift proof v2

Review target: `support_lift_proof_v2.md`.

Expected verdict scope:

- `CORRECT` or `CRITICAL_GAPS` for the support, full-event deletion,
  analyticity, Hessian-shell formula, and strict-kernel lift.
- Do not review it as a proof of face concavity. The proof explicitly does not
  claim `Hess H_face(A)[V,V] <= 0`.
- Do not treat the continuity gate as a positive candidate. It only applies
  after an independent strict positive face gap lower bound `g>0` is available.

Checklist:

1. Verify the L-ensemble identity from the frozen signed event determinant,
   including the sign after multiplying by `I+L`.
2. Check that `z_i != 0` really implies full row rank for every proper row set
   of the `4 x 3` isometry.
3. Check that the full event and all face derivatives vanish identically, not
   merely to first or second order at one `A`.
4. Check the Hessian formula only sums over the 15 positive proper events and
   uses the derivative cancellations from `sum p_S=1`.
5. Check strict feasibility of `K_j(e)=(1-2e)K_j+eI`, midpoint preservation,
   and positivity of all 16 strict event masses.
6. Check the bit-flip channel proof that `K_e=eI+(1-2e)K` is the kernel of
   the DPP obtained by independently flipping each observed bit with
   probability `e`.
7. Check the entropy increment bound `0<=H(K_e)-H(K)<=4h_b(e)` and the
   resulting gap gate `Delta(e)>=Delta_face-4h_b(e)`.
8. Check that no private handoff material, credentials, server address, or
   non-public conversation content appears in the proof files.

Known limitations:

- No independent non-author review has been completed in this directory.
- No Lean or interval certificate is included.
- Novelty is unconfirmed.
