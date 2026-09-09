# PR59 Second Verification Report

Overall status: CORRECT within the frozen PR59 scope. I found no critical mathematical gap in the five requested units, provided the accepted PR34 radial quartic theorem and the accepted PR53/EW event-inverse/RPF machinery are used only in the precise scopes recorded in `frozen_scope.md`.

The general whole-legal-interval problem for arbitrary strict exponentially local centers remains INCOMPLETE, exactly as PR59 states in `input/frozen_statement.md:138-140`, `input/RESULT.md:62-71`, and `input/proof.md:625-627`.

## Unit 1 - Compact Radial Tube

Verdict: CORRECT.

Accepted scope: fixed `beta>0`, `0<mu<1`, real half-period-odd nonzero `g in A_beta`, an odd `k` with `g_hat(k)!=0`, and any preassigned compact interval `[-T,T]` strictly legal for the constant-centered chord `mu+t g`. The accepted conclusion is the existence of a center radius `rho>0` for half-period-even mean-`mu` centers near the constant symbol, with concavity of `h(c+t g)+(2/3)|g_hat(k)|^4t^4` on the whole prescribed compact interval. This is the statement in `input/frozen_statement.md:11-68` and `input/proof.md:42-67`.

The weighted inverse step is sound. `input/proof.md:102-169` proves a uniform weighted Schur bound for every complete-event inverse along the compact constant-centered chord. The signed accretivity estimate includes every zero set (`input/proof.md:108-122`), and `input/clarifications.md:7-46` supplies the missing norm estimate needed for the polynomial inverse. There is no small-Wiener-norm assumption: the proof uses Fourier truncation plus a weighted Neumann restoration (`input/proof.md:124-169`).

The joint analytic rate step is also sound in the stated scope. The center perturbation and complex parameter enter the event matrix linearly (`input/proof.md:189-205`), the inverse radius is word- and volume-independent (`input/proof.md:201-207`), and the finite conditionals converge in one fixed weaker Holder norm with derivative control (`input/proof.md:217-247`). The true entropy-rate formula is established before differentiation (`input/proof.md:241-249`), matching the accepted PR53 rate-theorem scope in `runs/C3/integration/docs/verification_round3_20260909/accepted_pr53.md:29-39`.

The proof does not rely on evenness alone to remove the quadratic term. It uses parity block independence and fixed parity marginals to obtain the relative-entropy identity (`input/proof.md:253-273`), then differentiates the normalized `s=t^2` RPF formula at `s=0`, where normalization forces the first `s` derivative to vanish (`input/proof.md:275-291`). This justifies analytic divisibility of `F_tt(u,t)` by `t^2` (`input/proof.md:293-300`).

The imported radial margin is within accepted scope. The W2/PR34 audit accepts the constant-centered radial quartic correction on the whole feasible interval (`runs/C3/integration/docs/verification_20260909/w2/radial_quartic_audit.md:6-28`) with the constant `(4/3)|c_k|^4` checked at `lines 85-109`. Applying it to `mu+t g` is a rescaling of that radial statement. PR59 then obtains `Psi(0,t)<=-16 lambda_k` (`input/proof.md:304-320`) and transports half the margin by compactness in the center variable (`input/proof.md:323-343`). The final `rho` uses `||u||_infinity<=||u||_beta` from `input/proof.md:20`, so the legality reduction at `input/proof.md:329-343` is coherent.

Excluded scope: no arbitrary-center theorem, no endpoint-uniform radius, no re-centering at nonzero `t_*`, no PR39 full interval, and no arbitrary measurable-symbol transverse tube.

## Unit 2 - Exact RPF Hessian

Verdict: CORRECT.

Accepted scope: a positive normalized Holder `g`-function family with the usual simple isolated RPF eigenvalue/spectral gap, evaluated at an arbitrary strict parameter where the displayed derivatives exist. This is the frozen statement in `input/frozen_statement.md:72-105`.

The algebra checks out. From normalization, `L psi=0`, `nu(psi)=0`, and `dot L(A)=L(psi A)` (`input/proof.md:400-419`). The linear-response identity `d nu(A)=nu(dot A)+nu(psi R A)` follows from differentiating `nu L=nu` on the centered subspace (`input/proof.md:421-427`). The first and second derivatives of `B=-L phi` retain the local conditional Fisher term (`input/proof.md:429-446`). Differentiating the Poisson equation and using `R(LA)=RA-Pi A` gives exactly the five terms in `input/proof.md:448-476`, matching `input/frozen_statement.md:96-105`.

The variable-name confusion in the display near `B` is handled by the frozen clarification: the operative definitions are just `B_t=-L_t phi_t`, `h(t)=nu_t(B_t)`, and `u_t=R_tB_t` (`input/clarifications.md:64-83`).

The author symbolic checker in `input/code/check_rpf_hessian.py:21-109` and recorded output `input/output/rpf_hessian_exact.json:1-20` are consistent with the formula, but I did not rerun them. They are an author finite-memory algebra cross-check only, not a proof of Theorem CT or a DPP curvature certificate.

Excluded scope: the sufficient bound in `input/proof.md:478-495` is only a one-sided checkable condition and is not a universal sign theorem.

## Unit 3 - Finite-State True-Rate Error Bridge

Verdict: CORRECT.

Accepted scope: an analytic existence-level bridge for strict `A_beta` symbol chords on a compact strict interval. The bridge says finite-future conditionals and their first two parameter derivatives approximate the true Holder conditional in one fixed weaker norm with exponentially small error, and therefore finite transfer-operator Hessian computations can become true-rate certificates only after an explicit directed interval bound and the exponential remainder are included.

The bridge is stated and proved at the right level in `input/proof.md:497-528`. The key points are: derivative convergence of finite-future conditionals (`input/proof.md:499-504`), transfer-operator/eigenmeasure/resolvent convergence under a common contour (`input/proof.md:506-511`), substitution into the exact Hessian formula with a volume-independent remainder (`input/proof.md:513-520`), and the required certificate inequality (`input/proof.md:522-528`).

PR59 correctly separates this interface from any executed numerical certificate. `input/proof.md:528`, `input/verification.md:117-124`, and `input/verification.md:198-208` all state that no interval computation was run and that any future certificate must include the explicit geometric tail/resolvent error.

Excluded scope: no finite-window extrapolation, no floating curvature sample, no executed interval certificate, and no displayed numerical constants for a particular future computation.

## Unit 4 - Beam-Splitter Occupation MI Obstruction

Verdict: CORRECT.

Accepted scope: finite windows and the per-cell true rate under strict `A_beta` hypotheses near a fixed strict parameter `t_*`. The statement is in `input/frozen_statement.md:107-136`.

The finite-window algebra is exact. The balanced covariance follows from mixing endpoint kernels `K_-` and `K_+` into the block covariance `[[M,uK_g],[uK_g,M]]` (`input/proof.md:530-545`). The two output marginals are fixed DPP laws with kernel `M`, giving `H(Q)=2H(M)-I_out` and the exact midpoint decomposition (`input/proof.md:547-566`).

The second-order obstruction is correct. At `u=0`, the doubled law is the product law; conjugating one layer by `-I` sends `u` to `-u`, so every complete event probability is even in `u`. Therefore the output law differs from product first at order `u^2`, and the relative-entropy mutual information is `O(u^4)` (`input/proof.md:568-573`). The grouped four-letter RPF argument gives analytic per-cell rates (`input/proof.md:575-587`), hence `i_out''(0)=0` and `e_occ''(0)=-2h''(t_*)` (`input/proof.md:589-595`).

The proof keeps the required Shannon/von-Neumann distinction: `input/proof.md:597-599`, `input/attempts.md:69-77`, and `input/frozen_statement.md:136` all state that known quantum entropy inequalities do not prove the occupation-basis Shannon inequality needed for DPP entropy.

Excluded scope: no nonnegativity of `E_occ`, no second-order sign for `h''(t_*)`, and no true entropy-rate counterexample.

## Unit 5 - Explicit Mean-One-Third Family

Verdict: CORRECT.

Accepted scope: for each fixed `beta>0`, the family

```text
mu=1/3,
g(theta)=cos(2 pi theta)/8,
T=2,
c_epsilon(theta)=1/3+epsilon cos(4 pi theta)
```

has a nonempty nonzero amplitude range for which Theorem CT applies.

The arithmetic in `input/proof.md:351-394` is correct. `g_hat(1)=1/16`, so `lambda_1=1/65536` and `(2/3)lambda_1=1/98304` (`input/proof.md:361-366`). On `|t|<=2`, the constant-centered radial symbols lie in `[1/12,7/12]` (`input/proof.md:368`). The center norm is `||c_epsilon-mu||_beta=|epsilon|exp(2beta)` (`input/proof.md:374-378`). Since Theorem CT supplies `rho(beta)>0`, the interval `0<|epsilon|<min{rho(beta)exp(-2beta),1/24}` is nonempty (`input/proof.md:380-386`). The center is nonconstant for every such nonzero `epsilon`, has mean `1/3`, and the path cannot pass through a constant symbol because the frequency-2 component persists (`input/proof.md:386-392`).

The author exact checker and output (`input/code/check_explicit_family.py:16-60`, `input/output/explicit_family_exact.json:1-21`) match these rational constants and pointwise margins. I did not rerun the script; it is only an author arithmetic check and computes no entropy, curvature, RPF operator, or entropy rate.

Excluded scope: no explicit numerical value for the existential `rho(beta)`, and no claim that this covers PR39's mean-`1/2` fixed interval.

## Code And Output Review Boundary

I inspected the scripts and recorded JSON outputs but did not execute them. The recorded `run_record.json` claims two author runs with exit status zero and `theorem_dependency_on_computation=false` (`input/output/run_record.json:1-26`). That is consistent with the proof structure: the main theorem is analytic, while the scripts check only displayed rational constants and a finite-memory symbolic instance of the Hessian identity.

## Final Verdict

The five PR59 units are CORRECT within the accepted scope described above. There are no CRITICAL GAPS requiring a new machine computation or a request to root. The only INCOMPLETE material is the broader problem that PR59 itself excludes: arbitrary centers, endpoints, arbitrary measurable symbols, beam-splitter occupation-gain nonnegativity, and a true entropy-rate counterexample.
