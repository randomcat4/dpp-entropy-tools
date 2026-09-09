# Hazards

1. Finite-window entropy gaps are not entropy-rate gaps.  This route uses conditional entropy bounds, not a derivative or finite-window extrapolation.
2. The binary entropy function is not monotone on `[0,1]`; the lower bound must take the minimum over the whole interval `[alpha_w,beta_w]`.
3. The all-zero extreme past must be handled through the complement symbol `1-f`; using `nu_f` directly with zeros gives the wrong boundary object.
4. The outer-factor numerical root calculation is not a strict certificate.  The rational half-line residual certificate can replace it for final proof.
5. No exchange of limits and derivatives is used or needed.
6. The lower bounds need not have a proved convergence rate.  A finite separating gate is enough; a non-separating gate proves nothing.
7. Strict positivity of both `f` and `1-f` is essential for the clean finite-degree outer-factor and stable boundary-kernel certificate used here.
