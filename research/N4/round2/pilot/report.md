# First four-point face pilot

Status: SCOUT_COMPLETE; 12 centers, 12 six-direction full face Hessians,
36 retained affine chords and 12 directional finite differences. All four
frames are rational Householder frames with no zero null-vector coordinate.
Three A families: unequal diagonal spectrum, a fixed rational rotation of
(1/20,2/5,19/20), and scalar 2I/5 as a geometric control. All 192 event masses
were also evaluated rationally: 15 proper masses positive, full mass zero,
sum exactly one at every center. V is unrestricted symmetric in the fixed face.

Maximum curvature -0.0233703280190 occurs at the scalar control, so it is not
a noncommuting near-positive signal. Its Fisher and acceleration are both
negative. The unequal-spectrum cases include noncommuting top directions.
Maximum finite chord gap -0.0000552935263509. The largest finite-difference
discrepancy is about 2.93e-6; it is only a smoke diagnostic, not a sign certificate.

PID160788 ended with shell exit0; one thread, no GPU. The exact source hash and
environment are in results/manifest.json. The initial manifest's entropy_calls
field has a bookkeeping error: it says 120, but the executed code calls entropy
12 times per center (nine for three chords and three for the finite difference),
hence **144 actual calls**. This static count correction preserves the original
manifest/source bytes and does not invent an additional run. The per-center
Hessian itself uses direct proper-event masses rather than the entropy wrapper.

The full-event determinant is not evaluated in floating-point curvature. Its
omission follows from the fixed-U rank constraint, also verified by exact
mass checks. No large-Fisher matrix subtraction occurs. This is finite evidence
only and does not establish concavity on any full face.
