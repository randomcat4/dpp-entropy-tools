# Provenance and execution ledger

Question and frozen statements: A1 owner. Probe design, independent event
formula implementation, exact rational witness and proof: A1 probe author.
The owner supplied the conditional-acceleration identity and proposed a
bounded transverse diagnostic; the author selected the explicit four
rational centers and certified the signs. No sibling draft was read. The
baseline AGENTS and A1 frozen target, hazards and prior-art audit were read.
R1 source was not imported or executed. No new prior-art search or novelty
certification was performed. Proof remains subject to independent review.

Base commit: e6462caa8f9ec0c9033be376c3c39343a0175e32.
Independent local and compute checkouts; branch research/A1-probe. Only
research/A1/probe artifacts are proposed for commit. No external publishing.

One CPU numerical thread, BLAS/OpenMP/MKL explicitly set to 1; no GPU.
Formal run virtual-address cap: 8388608 KiB. Isolated environment packages:
Python 3.12.3, NumPy 2.5.3, SciPy 1.18.1, mpmath 1.4.1. No global install.

Commands below are portable commands executed from the repository root
using the isolated environment's Python; connection metadata is omitted.

| Operation | Command | Exit | PID | Accounting |
|---|---|---:|---|---|
| Initial local clone with guessed branch | git clone --no-hardlinks --branch research/A1 BASE DEST | 1 | shell not retained | branch absent; no checkout created |
| Local clone retry | git clone --no-hardlinks BASE DEST | 0 | shell not retained | independent clone |
| Remote dependency probe | python3 -c 'import numpy,scipy' | 1 | shell not retained | NumPy absent; no numerical run |
| Isolated environment setup | python3 -m venv VENV; VENV/bin/pip install numpy scipy mpmath | 0 | shell not retained | no global package changes |
| Smoke gate | python research/A1/probe/probe.py smoke | 0 | 144908 | 8 centers, 32 target calls |
| Formal batch | python research/A1/probe/probe.py formal | 0 | 144947 | 512 centers x 4 calls + 3000 refinement calls = 5048 |
| Fixed-center acceleration identity diagnostic | python research/A1/probe/acceleration.py | 0 | not captured | same 512 centers; 512 calls; no new search points |
| Manual conditional diagnostic, initial | python research/A1/probe/conditional.py | 0 | not captured | 4 fixed centers, 8 two-point gradient evaluations |
| Manual certificate with rational outer bounds and full derivative | python research/A1/probe/conditional.py | 0 | recorded in conditional.json | same 4 centers; 8 gradient evaluations + 4 full derivative certificates |

The initial conditional run's four signs and centers are unchanged in the
final artifact. It was repeated only to add rational outer enclosures and
the total second derivative certificate, not to select more centers.

Budget distinctions: 5592 target calls through the fixed-center diagnostic
(32+5048+512). Adding four *unique* manually chosen centers gives 5596
only if centers are counted as diagnostic objects; this is not an objective
call count. Counting all manual numerical/certificate evaluations including
the one certificate refinement gives 20 more evaluations, hence 5612
conservatively counted evaluations in total, below the 6000 cap.
No other center search, optimization, or hidden restart took place.

Smoke RNG seed: 2026090801. Formal centers and Nelder-Mead are deterministic
and have no random seed. Every center, rational denominator, refinement call,
domain rejection and termination is preserved in JSON. Some short auxiliary
process PIDs were not captured; this is an audit limitation, explicitly
retained rather than reconstructed or rerunning beyond the budget.

The output schema was based on math-theorem verdict/provenance templates.
No Lean claim. No non-author validation claim. Connection details, credentials
and private conversational text are absent from proposed artifacts.

Initial commit attempt failed because this independent checkout had no Git
author identity. The successful retry uses per-command author configuration
`Codex A1 Probe <codex-a1-probe@localhost>`, without changing global settings.
