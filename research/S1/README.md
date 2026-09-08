# S1: fixed scalar stationary DPP entropy rate

Status: ACTIVE_RESEARCH. Baseline: `fa504ec74e16843fafc395880d7ba99b4c1d2129`.

This route studies Lyons–Steif Conjecture 9.2 for fixed scalar symbols on the circle. The first unit uses an even real centre and an odd real, multiharmonic perturbation. Finite-window diagnostics and genuine entropy-rate certificates are recorded separately.

The frozen contract is [frozen_theorem_v1.md](frozen_theorem_v1.md). Public coordination: [issue #19](https://github.com/randomcat4/dpp-entropy-tools/issues/19). Work is restricted to `research/S1/`; phase, rate, and review tasks have separate checkouts and branches.

First bounded computation: exact-event enumeration in floating point for a fixed rational trigonometric symbol, initially at window lengths at most 12, with one BLAS/OpenMP thread. No floating-point result alone is a rigorous certificate.
