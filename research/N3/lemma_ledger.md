# Lemma ledger

| ID | Statement | Status |
|---|---|---|
| Background | B=F-2 tr(N adj D), N>0 at connected strict K | Inherited reviewed reduction |
| L1 | F>=Q_k, conditional determinant-score projection | PROVED; independent review CORRECT at 424b4ef |
| L2 | Exact nonnegative residual F-Q_k | PROVED; independent review CORRECT at 424b4ef |
| X1 | max_k Q_k(D)>=2 tr(N adj D) for all D | DISPROVED; rational/log-interval witness independently reviewed |
| X2 | The same bound only at the true A trace optimizer | DISPROVED; exact interval linear-solve certificate at 449221b, review pending |
| P1 | F=F_pair+(Lambda')^2/Z | Exact projection identity; independent review pending |
| X3 | F_pair(D)>=2tr(N adj D) for all D | DISPROVED by analytic rank-two boundary family and strict rational/log point; review pending |
| S2 | F_pair alone suffices at the true A optimizer | Unproved stronger sufficient condition; finite non-hits only |
| SM | Retained triple-score alignment closes the trace deficit | EQUIVALENT_BLOCKER; no new DPP lower bound proved |
| Target | B>=0 for all strict real 3 by 3 K and directions | INCOMPLETE |

The discarded X1, X2, X3 do not refute the target. Replacing F by a smaller projected
form is a strengthening; neither positivity of F nor the residual alone closes
the global proof.
