# A parity obstruction for the sparse-centre phase unit

Status: author-derived finite and entropy-value identities; independent review pending. This is a restricted symmetry statement, not a sign theorem for entropy-rate curvature.

Let

    f_0(x)=1/2+sum_(k odd) a_k cos(2 pi k x),
    f_t(x)=f_0(x)+sum_(k>=1) t_k b_k sin(2 pi k x),

where the sums are finite and parameters range in any open neighbourhood of zero on which the symbols remain strictly between zero and one. The coefficients are fixed independently of the observation window. Write R(t)_k=(-1)^(k+1)t_k.

Then for every finite window n,

    H_n(f_t)=H_n(f_(R(t))),

and the corresponding entropy values satisfy h(f_t)=h(f_(R(t))). In particular, every finite-window entropy Hessian at t=0 has zero entries between an even-harmonic direction and an odd-harmonic direction.

Proof. The shift x->x+1/2 sends f_0 to 1-f_0 and sends the kth sine to (-1)^k times itself. Thus

    1-f_t(x+1/2)=f_0(x)+sum_k (-1)^(k+1)t_k b_k sin(2 pi k x).

A symbol shift multiplies K(i,j) by a diagonal unitary factor and its adjoint; every inclusion determinant is unchanged, so its entire DPP law is unchanged. The symbol 1-f corresponds to the complemented occupation process, which has the same finite entropy. Applying these two facts proves the finite identity. Division by n and passage to the entropy limit proves the value identity. No derivative is passed through this limit.

Finite event probabilities are strictly positive near t=0, so H_n is smooth there. Differentiate the finite identity once in an even-harmonic parameter and once in an odd-harmonic parameter. Their signs under R are opposite, forcing that mixed derivative to be its negative and hence zero. This establishes the finite Hessian assertion. If an entropy-rate Hessian is separately known to exist, it obeys the same parity restriction, but its existence is not asserted here.

For the nearest-neighbour centre (only a_1 nonzero), testing absent harmonics 2 and 3 together cannot reveal a mixed second-order mechanism at p=1/2. The second unit should test absent harmonics of the same parity (for example 2 and 4), or a centre lacking this complement/shift symmetry. This changes the tested mechanism rather than merely increasing the first scan.
