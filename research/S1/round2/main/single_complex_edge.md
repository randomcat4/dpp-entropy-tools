# One complex affine edge at a general Hermitian centre

Status: author proof, independent audit pending. Finite-kernel statement, strictly weaker than the scalar entropy-rate conjecture. The centre need not be real. This refines the interpretation of a negative single-edge cost in the new non-even regime.

## Statement

Let K(t) be a finite Hermitian DPP kernel on an open real interval I, with 0<K(t)<I. Every entry is fixed except K_ab(t)=z+t v and its conjugate, for one unordered pair {a,b}, with z,v complex. Then the full configuration entropy H(K(t)) is concave on I. If v is nonzero, it is strictly concave as a function on I, although its second derivative may vanish at isolated degenerate points. No assertion about a sum of edges or entropy rates is made.

## Conditional proof, with Fisher retained

Condition on the exact configuration gamma on R=V\{a,b}. The weight w_gamma is positive and independent of t. The conditional kernel on {a,b} is

    [[r_gamma, z_gamma+t v], [conj(z_gamma+t v),s_gamma]],

where r_gamma,s_gamma are real, z_gamma may be complex, and all three are independent of t. This follows from the exact-event Schur complement: the R matrix and the cross rows are fixed. Its four masses in order 11,10,01,00 are

    rs-q, r(1-s)+q, (1-r)s+q, (1-r)(1-s)-q,
    q=|z_gamma+t v|^2.

All are positive. Write F_gamma(q) for this four-event entropy. Differentiating the exact masses gives

    F_gamma'(q)=log[(p11 p00)/(p10 p01)] <= 0,
    F_gamma''(q)=-(1/p11+1/p10+1/p01+1/p00) < 0.

The first sign follows from p11 p00-p10 p01=-q. For the affine complex edge,

    q'=2 Re(conj(z_gamma+t v) v),  q''=2|v|^2,
    d²F_gamma(q(t))/dt²=F_gamma''(q)(q')²+2|v|² F_gamma'(q) <= 0.

The first displayed contribution is the exact nonpositive Fisher term for this conditional pair. It is generally nonzero at a complex centre; dropping it would not be a valid formula. The second is the entropy acceleration term. Neither can be positive for one affine edge.

Finally, H(K(t))=H(X_R)+sum_gamma w_gamma F_gamma(q_gamma(t)), so the same sign holds for the full entropy. When v!=0, each q_gamma(t)>0 except at at most one t, and then F_gamma'(q)<0. Thus H''<0 except possibly a finite set (there are finitely many gamma). Integrating along any nontrivial interval gives strict concavity. A possible zero H'' at a point does not imply an affine segment.

## Implication and limitation

Allowing a non-even centre and a real/imaginary mixed direction does not create a one-edge loophole. A positive full Fourier-direction Hessian must involve interactions between distinct kernel edges or changes of diagonal/marginal data. It is not enough to find a negative or complex cycle phase on one modified edge. Toeplitz harmonic directions change multiple edges at once and therefore remain outside this lemma's sign conclusion.

The proof uses only the already reviewed finite exact-event Schur complement, positivity and entropy chain rule. It does not require a graph bridge, gauge fixing, conjugate endpoints, finite dependence or mixing.
