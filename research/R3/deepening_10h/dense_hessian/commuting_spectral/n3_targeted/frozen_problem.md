# D10-M5 frozen target: n=3 commuting spectral PSD rates

Author status: **INCOMPLETE / SCOUT**, pending any future non-author review.

## Object

Fix \(Q\in O(3)\).  Let

\[
K(t)=Q\operatorname{diag}(\theta_1(t),\theta_2(t),\theta_3(t))Q^\top,
\qquad
\theta_i(t)=\lambda_i+t v_i,
\]

on an open interval where \(0<\theta_i(t)<1\).  The targeted PSD direction case
has \(v_i\ge0\) and not all zero, so
\[
D=Q\operatorname{diag}(v_1,v_2,v_3)Q^\top\succeq0.
\]

The NSD case is equivalent by replacing \(t\) by \(-t\) and \(v\) by \(-v\).

## Question

For every such strict \(n=3\) fixed-eigenvector path, is

\[
H(K(t))''\le0?
\]

If yes, give a direct proof.  If no, construct and freeze a strict positive
candidate with exact-event \(p,p',p''\), feasible spectral step, and a positive
high-precision chord gap.

## Result of this work unit

No strict positive candidate was found.  A general proof was also not closed.
The precise remaining obstruction is the curvature of the cardinality-layer
conditional entropy

\[
\Psi(t)=H(Y_t\mid |Y_t|).
\]

Individual singleton and pair layers can have positive conditional second
derivative, so the desired proof cannot simply show that each layer is concave.
The finite search suggests cancellation between the two layers, but this
cancellation is not proved here.
