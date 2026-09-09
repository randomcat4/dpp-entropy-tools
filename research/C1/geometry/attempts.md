# Attempts and retained failures

1. Fixed full-support rank-one degeneration. The cofactor metric grows
logarithmically and the rare pair Fisher cost constrains the optimizer to
the rank-one tangent. This explains d alpha approaching 1. The stronger
beta calculation gives a uniformly negative first coefficient, independently
of any fixed positive soft shape. This cannot supply beta zeros.

2. Complement-signed affine perturbation, including every t/epsilon ratio.
Using tau=epsilon+t and r=t/tau makes the soft shapes a compact uniformly
positive family. The same negative coefficient excludes the entire joint
corner; it does not exclude roots with t tending to a positive value.

3. Joint support loss, u3^2=kappa epsilon. The old uniform constants fail:
the pair-normal isomorphism loses coercivity as u3 tends to zero; the
logarithmic N limit becomes diag(m(1-lambda),m,L) in a fixed basis. Six
predeclared diagnostic points showed opposite beta signs at kappa=1 and
10, with d alpha close to 1. No scan expansion followed.

4. Failed first sparse two-dimensional reduction. It included only rare
events in F(U,V), yielding Fav=-2sqrt(kappa)R^2/A. This missed the common
atom cross contribution +2sqrt(kappa)/(1-lambda), although the common
atoms' V,V self-cost is smaller. sparse_detail.py and its output retain
the failed theory_v/theory_z values; those fields are explicitly NOT
accepted predictions. The actual reconstructed F/M entries exposed the
error, and the parent independently found the same missing atom term.
Adding it produces the coefficient in sparse_proof.md and reverses the
incorrect large-positive coefficient. All eight events are now retained.

5. The exact sparse leading coefficient has a unique positive root for
lambda>1/2, but only the fixed lambda=7/10 and split=2/5 family is promoted
as the principal candidate. No finite-epsilon uniqueness or smooth branch
claim is made. Uniform asymptotic sign plus continuity supplies exact
zeros; numeric near-zero conventions are never used.

No conditional-projection or locked-odds dominance mechanism was revived.
No new global B0 proof or counterexample was obtained. The old complete
rho boundary asymptotic is not claimed as a new result. Novelty remains
uncertified. This unit stops after producing a reviewable exact-zero
candidate rather than expanding the search.
