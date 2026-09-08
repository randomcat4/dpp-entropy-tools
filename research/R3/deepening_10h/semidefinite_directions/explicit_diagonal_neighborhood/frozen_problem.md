# D10-S6 frozen problem

STATUS: CORRECT_AFTER_INDEPENDENT_REVIEW.

Fix `n>=2` and a compact diagonal box

\[
\mathcal X_{a,b}=\{\operatorname{diag}(x_1,\ldots,x_n):
0<a\le x_i\le b<1\}.
\]

The already verified D10-S4 theorem proves that some uniform open
neighborhood of this box has strictly negative DPP entropy curvature in every
nonzero PSD or NSD direction.  It does not give a numerical radius.

The candidate here is an explicit, intentionally conservative radius.  Put

\[
s=\min(a,1-b),\quad q=s^n,\quad m=q/2,
\]
\[
\ell=\max\{1,|1+\log m|\},
\]
\[
L=2^n\left(\frac{n^3}{m^2}
 +\frac{3n^2(n-1)}m+n(n-1)(n-2)\ell\right),
\]
and

\[
\delta_{n,a,b}=\min\left\{\frac{q}{2n},\frac{2}{nL}\right\}.
\]

For every `X` in the box, every strict real DPP kernel `0<K<I` satisfying
`||K-X||_F<=delta_{n,a,b}`, and every nonzero real symmetric PSD or NSD `D`,
the claimed bound is

\[
H''_K[D,D]\le-\frac2n\|D\|_F^2<0.
\]

This is a local exclusion theorem, not a global PSD/NSD theorem.  Its radius
is expected to be extremely small because it uses only worst-case determinant
and atom bounds.  No numerical experiment may replace the analytic estimate.
