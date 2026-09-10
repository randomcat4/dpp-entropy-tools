# Lemma ledger

1. Correct extraction: `D_Q^2 r1 = D_Q^2 partial_t(B+Lu) - D_Q^2 v + D_Q^2 Lv`, with the last two terms at t-order zero. Status: independently checked.
2. Fixture hand check: the chosen nonzero polynomial has `v_xx=2`; genuine `Lv` has nonzero parameter derivative. Status: PASS.
3. Independent expression-DAG differentiation agrees with interval Jet for all six `r0` components, all six `r1` components, and `r2`. Status: PASS.
4. Formal fixed-point result: `Q=0,t=5/4` has rigorous gate-expression lower bound `-0.003330007824007023767653501284027148106155`; therefore no point obstruction was found. Status: proved for this point only.
5. Full-state-domain gate certificate: not attempted by the single point executable and not established. Status: unresolved; unit stopped by the one-run scope.
