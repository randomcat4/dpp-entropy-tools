# S1 mathematical/source FIRST for PR113

This packet records an independent, version-bound FIRST review of PR113 at author head

`a2bced01cc5de30943b20387b7e1d260c384661e`.

## Verdict

`ACCEPTED_SCOPED`.

Under the stated unweighted small-Wiener condition

\[
r_c=\sum_{m\ne0}|\widehat c(m)|<\min\{\mu,1-\mu\},
\qquad 0<\mu<1,
\]

the author packet correctly proves a nonempty real interval on which the true stationary DPP configuration entropy rate is smooth and

\[
t\longmapsto h(c+t g)
+\frac{|\widehat g(k)|^4}{8\mu^2(1-\mu^2)}t^4
\]

is concave for every odd `k` with `g_hat(k) != 0`, with strictly negative second derivative away from the center after shrinking the interval.

The proof uses the physical affine kernel `K_t=T(c)+tT(g)`, retains every complete occupied/vacant event, and identifies the thermodynamic limit with the classical configuration entropy rate.  It does not use spectral entropy, a finite-window sign extrapolation, or an `L`-affine path.

The same frozen head also proves `C^infinity` real-parameter response on the open small-Wiener interval, one fixed derivative order at a time.  No real or complex analyticity is accepted.

No numerical execution, formal verification, novelty assessment, SECOND, author edit, or merge was performed.
