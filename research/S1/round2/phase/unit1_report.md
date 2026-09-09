# Round 2 phase unit 1: non-even full Hessians

Status: **INCOMPLETE** for the frozen entropy-rate problem. The 12 predeclared centers and 24 finite Hessians were actually evaluated. None had a positive eigenvalue numerically. The first-round eventwise evenness has genuinely been removed, but the remaining full Hessians were negative in the tested points. This is not a family exclusion or an entropy-rate result.

## Frozen objects and nonremovable phases

`centers.json` was committed before the program was executed, in commit `28ef713e4b7f54f14f558a629061bb20fba28aa0`. It contains six degree-three and six degree-four centers. For each degree, the means are 1/5, 7/20, 1/2, 3/10, 9/20, 1/4. The cosine and sine coefficient lists are exact rational multiples of the stored integer patterns:

    a_k=s A_k, b_k=s B_k,
    s=p*budget_fraction/sum_k(|A_k|+|B_k|).

The explicit expanded rational coefficients are also retained in `results.json`. The spectrum is strictly interior because

    |f_0-p|<=p*budget_fraction,
    epsilon=p*(1-budget_fraction)>0,
    epsilon<=f_0<=1-epsilon.

All p<=1/2, so the lower triangle margin is also a valid upper margin. For a direction in the full coefficient space with l1 norm at most 1, |t|<=epsilon/2 gives an affine chord with uniform margin epsilon/2. Thus the full Hessian directions are locally feasible; the center and its perturbation neighborhood are independent of n. The numerical eigenvectors themselves are not claimed as rational, frozen, rate-ready chords.

Every center has a_1>0,b_1=0,b_2>0. Consequently c_1=a_1/2 is positive real and

    Im(c_1^2 conjugate(c_2))=a_1^2 b_2/8>0.

A translation that makes c_1 real has phase 0 or pi; neither can make c_2 real. More generally diagonal unitary conjugation preserves this cycle product, so the center cannot be made fully real by a gauge. The centers are not translated old even centers. The convention c_1>0 fixes translation uniquely when comparing two canonical centers; conjugation reverses the displayed invariant's imaginary part and leaves the canonical convention. Thus no two centers here are conjugates up to translation. Distinct (p,m) distinguish the listed centers; the highest coefficient in each degree is nonzero. These checks concern gauge, conjugation and translation, not a classification of every possible accidental equality of DPP laws. No random selection or post-result deletion occurred.

## Full derivative formula and retained data

Coordinate order is (mean,a_1,...,a_m,b_1,...,b_m), dimension 2m+1. For each exact event omega let

    q=(-1)^number_of_zeros det M, M=K-diag(zeros),
    s_r=tr(M^-1 D_r),
    q_rs=q[s_r s_s-tr(M^-1 D_r M^-1 D_s)].

These expressions are real; numerical imaginary residuals are recorded. Strict feasibility makes every q positive and M invertible. Define

    F_rs=sum q s_r s_s,
    A_rs=-sum q_rs log q,
    Q=A-F.

The event mass sum and its first and second derivatives cancel exactly in the entropy differentiation. This gives the full affine-kernel Hessian without suppressing the Fisher term. `results.json` retains all F,A,Q matrices, their spectra, gradients, the leading Q and A eigenvectors, and the decomposition on those directions. It does not only retain a best score.

## A Fisher null direction remains even at non-even centers

For theta-parametrized translations f_theta(x)=f_0(x+theta/(2*pi)), the coefficient velocity and acceleration at zero are

    v=(0,k b_k,-k a_k),
    w=(0,-k^2 a_k,-k^2 b_k).

Every exact DPP event is constant on this translated path by diagonal unitary invariance. Hence each event score annihilates v, giving Fv=0, and

    v^T Q v + gradient(H_n) dot w = 0.

These identities hold at every strictly interior trigonometric symbol, not only at even centers. A straight affine chord with tangent v omits the acceleration w of the translation orbit. It is therefore incorrect to infer v^T Q v=0 merely from translation invariance. In this batch the affine tangent curvature is negative, although its Fisher cost is zero to rounding error. The exact score-null direction is retained in the full direction space, not removed by gauge fixing the center.

The gauge identity residual was at most 1.21431e-16, and the maximum eventwise gauge first derivative was 8.34394e-19. The n=8 normalized gauge-direction Fisher costs had absolute value at most 4.29472e-17. Small negative reported Fisher values at that scale are roundoff in a positive semidefinite matrix.

## What actually dominates

At n=8 the following table reports the normalized top Q eigenvector's full curvature and F/A decomposition; the final columns report A and F on A's own normalized top eigenvector.

|Center|top Q|F on top Q|A on top Q|top A|F on top A|
|---|---:|---:|---:|---:|---:|
|C3_1|-0.0108734420|0.00142193861|-0.00945150343|1.10069028|51.1415543|
|C3_2|-0.0660172632|0.00262424378|-0.0633930194|1.67353902|36.8739874|
|C3_3|-0.131443443|0.00978508175|-0.121658361|5.23189424|37.5670457|
|C3_4|-0.0584332853|0.00402782100|-0.0544054643|1.57762771|39.7086503|
|C3_5|-0.129612785|0.00885297697|-0.120759808|2.42289787|34.7936923|
|C3_6|-0.0193079463|0.00101270494|-0.0182952413|1.85033351|44.6039426|
|C4_1|-0.00663457638|0.000609743407|-0.00602483297|0.744770495|50.7615726|
|C4_2|-0.0301746732|0.000955811623|-0.0292188616|1.09083497|36.2683719|
|C4_3|-0.0315392904|0.000833981217|-0.0307053091|4.25458288|36.4912062|
|C4_4|-0.0291084058|0.00170397417|-0.0274044316|0.967036428|39.0731758|
|C4_5|-0.0322240320|0.00371291653|-0.0285111155|1.72550773|34.0704464|
|C4_6|-0.0132650218|0.00110488408|-0.0121601377|1.30737947|44.0125813|

Thus the numerically best curvature directions do **not** lose only because of Fisher: their acceleration terms are already negative. Conversely, the positive acceleration eigendirections incur a much larger Fisher cost. Both mechanisms matter, and it would be misleading to label the whole failure as 'Fisher dominance'.

For C4_1, the n=8 top direction has coordinate vector approximately

    (-2.53896e-8, -0.000246059,0.008756388,-0.715719705,-0.030802775,
                  -0.001431587,-0.010700773,-0.697269299,-0.020462816).

It mixes third-harmonic cosine and sine heavily and has only 0.31024 absolute alignment with the normalized gauge tangent. The selected top directions are not simply the omitted gauge direction. All other directions and alignments are in the result file.

The old symmetry restrictions are genuinely absent: every center has a nonreal cycle invariant, and the cosine-sine mixed Hessian block maximum is between 0.0126745 and 0.118395 across the 24 evaluations. Event scores are not zero (maximum absolute coordinate score at each matrix between 13.7629 and 43.5380). No endpoint conjugation or equal-entropy shortcut was used. No finite affine endpoint pair was evaluated in this unit.

## Coverage, failures and remaining obligation

Actual coverage is 12 centers times n=6,8, for 24 full Hessians and 3840 exact event mass/inverse evaluations. There were no retries, failed numerical calls, adaptive additions, extra windows or omitted center results. All 24 Q spectra were negative numerically. Maximum residuals were: probability mass 1.33227e-15, first mass derivative 2.23866e-15, second mass derivative 7.27196e-15, imaginary part 6.38378e-16. These internal consistency checks are not interval bounds or independent review.

The first-unit hypothesis—that removing the real-center symmetry would expose an easy positive mixed direction—has no supporting numerical witness here. This does not disprove it globally. The triangle-bound construction may keep these symbols in a restricted low-amplitude region despite the nominally small triangle margin. A genuinely different next unit, if assigned, would use an exact nonnegative spectral-factor construction to exploit cancellation beyond this coefficient l1 ball. Merely increasing n or inserting more centers from the same family is not proposed.

The remaining target is still a fixed feasible scalar chord with rigorous rate bounds for all three distinct symbols. This report provides no entropy-rate certificate and makes no derivative-limit exchange. Its gauge and feasibility arguments are author derivations awaiting independent review; its Hessian signs are floating point diagnostics only.
