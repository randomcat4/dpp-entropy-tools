# Post-launch contract correction

C3 corrected its own request in [issue52 comment5605146225](https://github.com/randomcat4/dpp-entropy-tools/issues/52#issuecomment-5605146225), posted2026-09-09T16:22:08Z, after run01 began16:21:24UTC.

The original request named E_mu[y psi] as W. The author actually defines
W=E_mu[b psi], while V=E_mu[y psi]=s^2 W is the term in the full curvature.
The correct identity is t^2 I''=P0+A2+V=P0+A2+s^2 W.

The original request, frozen checker and run01 outputs are retained unchanged.
Every W field in run01 denotes V under the corrected terminology. Thus run01's
comparison of that value with the author equation(3.6) W bound is a request-caused
scale mismatch and must not be called an author error. The correct author W
literal bound is NOT certified by this run.

The first ordered failed comparison was instead equation(3.5), involving
T=4(P0+A2)^2/A2. P0,A2,L,T and the direct true curvature are unaffected by the
W/V notation. The strict interval for T is above the author's claimed upper
bound, so this is an independent literal-bound discrepancy. Equation(3.4)
passed before it. No continuation or corrected arithmetic was launched after
that first exact discrepancy. Later entries already present in the raw
comparison array are not a new post-stop verification gate.

The corrected request is preserved verbatim in inputs/REQUEST_CORRECTION.md
as post-launch context; it was not an input read by run01. The original
600-second deadline16:31:24UTC was never reset or extended. All arithmetic
stopped16:22:48UTC, and PID174687 was confirmed absent16:24:10UTC.