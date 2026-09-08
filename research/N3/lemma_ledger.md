# Lemma ledger

| ID | Statement | Status |
|---|---|---|
| Background | B=F-2 tr(N adj D), N>0 at connected strict K | Inherited reviewed reduction |
| L1 | F>=Q_k, conditional determinant-score projection | PROVED; independent review CORRECT at 424b4ef |
| L2 | Exact nonnegative residual F-Q_k | PROVED; independent review CORRECT at 424b4ef |
| X1 | max_k Q_k(D)>=2 tr(N adj D) for all D | DISPROVED; rational/log-interval witness independently reviewed |
| X2 | The same bound only at the true A trace optimizer | DISPROVED; interval certificate at 449221b; independent review CORRECT |
| P1 | F=F_pair+(Lambda')^2/Z | Exact projection identity; independent review CORRECT |
| X3 | F_pair(D)>=2tr(N adj D) for all D | DISPROVED; analytic rank-two family and exact point; independent review CORRECT |
| S2 | F_pair alone suffices at the true A optimizer | Unproved stronger sufficient condition; finite non-hits only |
| SM | Retained triple-score alignment closes the trace deficit | EQUIVALENT_BLOCKER; no new DPP lower bound proved |
| Target | B>=0 for all strict real 3 by 3 K and directions | INCOMPLETE |

The discarded X1, X2, X3 do not refute the target. Replacing F by a smaller projected
form is a strengthening; neither positivity of F nor the residual alone closes
the global proof.

相对原命题: X1/X2/X3/S2 are stronger sufficient conditions, while SM-close
is equivalent to the target. L1/L2/P1 are auxiliary identities and bounds.
外部定理条件核验: weighted projection and positive-definite Sherman-Morrison
are used with their domain conditions checked in the independent reports.
