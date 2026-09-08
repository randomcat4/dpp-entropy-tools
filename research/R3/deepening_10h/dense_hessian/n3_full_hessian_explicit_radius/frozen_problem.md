# D10-S7 frozen explicit-radius claim

AUTHOR STATUS: PROOF_CANDIDATE_PENDING_INDEPENDENT_REVIEW.

## Objects and verified input

Let K_* be the strict real symmetric three-dimensional kernel

    [[151/280, -6/35, -47/280],
     [-6/35, 94/175, -29/175],
     [-47/280, -29/175, 747/1400]].

The verified S5 inputs are: eigenvalues (1/5,7/10,71/100); all eight exact
event probabilities at least q=87/1250; and

    H''_{K_*}[D,D] <= -(43/50)||D||_F^2

for every real symmetric D. H is the Shannon entropy of the full exact-event
DPP law, with natural logarithms. Inclusion determinants are not exact atoms.

## Candidate conclusion

Put m=87/2500 and

    L = 8(27/m^2 + 54/m + 18) = 160561104/841,
    delta = 36163/16056110400.

For every real symmetric K with ||K-K_*||_F<=delta:

1. K is automatically a strict positive contraction, with eigenvalues in
   [1/10,9/10]; strict feasibility is a conclusion, not an extra premise.
2. Every exact event probability is at least m.
3. For every real symmetric D,

       H''_K[D,D] <= -(43/100)||D||_F^2.

No commutation, PSD, rank or direction-normalization restriction is imposed.
The inequality is strict for every D!=0 and equality at D=0 is allowed.

## Scope and interfaces

The ball is a CLOSED Frobenius ball in Sym(3). The tangent space uses the
Frobenius inner product, not the unweighted norm of six independent entries.
All computations are bounded sanity, not evidence of global coverage. The
general global DPP entropy-concavity question remains INCOMPLETE. No claim is
made that this radius is maximal, close to sharp, or practically representative.
The author cannot assign CORRECT; a new non-author context must review it.
