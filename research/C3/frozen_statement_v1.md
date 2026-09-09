# Frozen statement v1 — I05-C3-20260909

Objects: for a fixed measurable real f on R/Z with 0<=f<=1 a.e., K_f is
its scalar convolution kernel and h(f)=lim H(K_f|[1,n])/n, with natural logs.
The DPP law is specified by P(A subset X)=det K_A and entropy is that of
the entire binary configuration. Entropy rate is defined by stationarity
and the finite-alphabet subadditivity limit. No rate derivative is assumed.

Main problem remains the Lyons–Steif midpoint inequality for all f,g.
This run first attacks structured score-null directions described in CLAIM.md.
An explicit counterexample must give fixed uniformly legal f_-,f_0,f_+
and independent rate enclosures satisfying (L_-+L_+)/2-U_0>0.

Additional precisely scoped candidate T (frozen before verification):
For every p in (0,1) and every fixed bounded measurable real g with integral
zero, define I={t in R: 0<=p+t g<=1 a.e.}. Then t -> h(p+t g) is concave
on I. The analogous finite statement is: for any diagonal P with entries
in (0,1) and any fixed Hermitian zero-diagonal A, t -> H(P+t A) is concave
on the interval where 0<=P+t A<=I. Boundaries are included by continuity
at the finite stage and finite Jensen inequalities before the rate limit.

The proposed proof interface is independent Bernoulli-coordinate resampling,
not affine spectral interpolation. Proving that its output law is exactly
the K-affine DPP family is mandatory. Arbitrary nonradial chords are outside T.
No Fourier bandwidth, evenness, finite dependence, differentiability of g,
or equality of endpoint laws is assumed in T.

Success of T is a continuous-family partial result for the main problem;
it must never be labeled resolution of the full conjecture. Novelty is
unconfirmed. Authors and reviewers may not change its assumptions.
