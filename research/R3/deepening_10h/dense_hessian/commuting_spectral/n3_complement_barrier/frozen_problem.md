# D10-M7 frozen problem

STATUS: INCOMPLETE_GLOBAL / SUBCLASS_CORRECT_AFTER_INDEPENDENT_REVIEW.

Let Q∈O(3), θ∈(0,1)^3, and v∈R_+^3. The affine kernel line is
K(t)=Q diag(θ+t v)Q^T on its strict feasible interval. Negative semidefinite
directions are equivalent by t↦−t. The target is the Shannon entropy of all
eight exact events, not the inclusion determinants.

Write P_ai=q_ai², r_i=θ_i∏_{j≠i}(1−θ_j),
s_i=(1−θ_i)∏_{j≠i}θ_j, and
G_P(x)=−Σ_a(Px)_a log((Px)_a/Σ_i x_i). The verified identity is
H(Y)=H(N)+G_P(r)+G_P(s), N=|Y|.

The unchanged global question is whether
B(θ,Q;v)=−H(N)''−[G_P(r)+G_P(s)]''≥0 for every Q,θ,v≥0.
No finite non-hit may answer this universal question. The assertion Ψ''≤0,
Ψ=G_P(r)+G_P(s), is already false in general and is not an available lemma.

Authorized subsidiary target: prove a nontrivial continuous subclass if the
global target does not close. This work freezes the following candidate:

1. At a strict base point where the three singleton probabilities are equal
   and the three pair probabilities are equal, B>0 for every nonzero v≥0.
2. If all θ_i∈[ε,1−ε], 0<ε<1/2, then at these base points
   B≥c_ε||v||_2², c_ε=2ε(1−ε)log(3)/9.
3. The fully connected such real kernels are signed exchangeable kernels
   K=S[bI+(a−b)J/3]S, S diagonal with entries ±1, a,b∈(0,1), a≠b.
   Directions need only commute with K and be nonzero PSD; they need not
   preserve the repeated eigenvalue or the observation symmetry.
4. On compact strict, separated portions of this base family, a uniform open
   spectral-parameter neighborhood has B>0 for all nonzero one-sign rates.

Analytic strengthening derived during this work (same global target): no
symmetry is needed if both conditional layers obey
|log(3(Pr)_a/R)|≤δ and |log(3(Ps)_a/T)|≤δ for a common δ<log3/3.
Then B≥−H(N)''+D_P(r)+D_P(s)+(2log3−6δ)Σ_{i<j}v_iv_j, hence B>0
for every nonzero one-sign rate. In particular the entirely rational condition
1/4≤(Pr)_a/R,(Ps)_a/T≤4/9 is a sufficient continuous subclass.
This stronger candidate has no repeated-spectrum or exchangeability premise.

These are distinct from the unresolved global claim. No claim is made about
noncommuting directions, strict boundary kernels, arbitrary real directions,
or certification of an explicit numerical neighborhood radius.

The author artifacts are accompanied by a fresh non-author exact-event review
in `verifications/`. That review certifies only the stated subsidiary results;
the global question remains incomplete. No general random search is run.
