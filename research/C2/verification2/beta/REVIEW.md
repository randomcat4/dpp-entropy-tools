ACCEPTED_SCOPED

# C2 verification2 beta=0 scoped review

## Scope verdict

I accept PR30 head `94d67909bf8c1ea06da6350cf7907d6665cb166a` only for the frozen partial beta=0 near-family claim:

- For `lambda=7/10`, `s=2/5`, `K(epsilon,kappa)=epsilon I+lambda uu^T` with `u=(sqrt(s(1-kappa epsilon)),sqrt((1-s)(1-kappa epsilon)),sqrt(kappa epsilon))`, the proof establishes, for sufficiently small `epsilon`, at least one exact beta zero with `kappa in (1,10)`.
- Every beta zero in the compact interval `[1,10]` obeys `kappa=(3/7)(exp(40/21)-1)+O(1/L)` and `det(N) alpha=1-10/(7L)+O(L^-2)<1`, where `L=log(1/epsilon)`.
- The result excludes a uniform positive safety margin on the connected strict beta-zero set. It does not prove global B0, uniqueness, an explicit epsilon threshold, a violating zero, PR31, or original entropy concavity.

No source files were modified. I did not read old author reviews/audits or PR31 work.

## Source and dependency binding

Primary files reviewed from `verification2/sources/pr30_api/`:

- `research/C1/frozen_partial_statement.md`
- `research/C1/proof.md`
- `research/C1/geometry/sparse_proof.md`
- `research/C1/main/core.py`
- `research/C1/main/reconstruction.md`
- `research/C1/main/interval_soundness.md`
- `research/C1/main/sparse_limit_algebra.py`
- `research/C1/mechanism/scripts/sparse_rational_certificate.py`
- `research/C1/mechanism/scripts/mechanism_probe.py`

Dependency files reviewed/bound:

- `research/N3/inequality/optimizer_sherman_morrison_lemma.md`
- `research/N3/inequality/slice_fisher_covariance_lemma.md`
- `research/N3/round2/inequality/rayleigh_beta_zero_obstruction.md`

The PR24 dependency binding is satisfactory for this PR30 review. `verification2/dependency_binding.json` records all three named PR24 blobs as `identical_to_pr30: true`, with PR24 head `e988aa3003484f6368133b8bc0c668331629e369`. I did not rerun the PR24 fixed checkers because C3 reported PR24 merged to `main` and separately reran those checkers with PASS.

## Analytic proof audit

The frozen statement is correctly scoped. `frozen_partial_statement.md` states that the eight-event definitions and all Hessian derivatives remain in the six genuine symmetric `K` entries, and excludes uniqueness, explicit epsilon0, a global B0 proof, and novelty. This matches `geometry/sparse_proof.md:11-30`.

The reconstruction layer uses the full eight-event atom map and all six actual symmetric coordinates. The determinant atom formula and derivative convention are in `main/reconstruction.md:7-23`; the Hessian/N identity and `M=Fpair+dG` reconstruction are in `main/reconstruction.md:27-47`; full Fisher decomposition and positive definiteness of `M` are in `main/reconstruction.md:48-65`. The implementation independently follows the same six-coordinate convention in `main/core.py:11-58`.

For the normalized sparse family, the event and log expansions are internally consistent. The proof gives exact atom formulas in `geometry/sparse_proof.md:53-64`, strictness/connectivity in `geometry/sparse_proof.md:75-77`, and the required `N`, `det(N)`, `Z`, and `eta` asymptotics in `geometry/sparse_proof.md:86-107`. I independently rebuilt the same eight-atom Jacobian with high-precision arithmetic in `evidence/analytic_sparse_check.py`; the output `evidence/analytic_sparse_check.json` matches these leading terms at `epsilon=1e-8`, `1e-10`, and `1e-20` within the stated `O(epsilon)`, `O(1/L)`, or `O(1/L^2)` scales.

The proof does not replace the six-coordinate Hessian by epsilon/kappa path derivatives. The six directions `U,T,Q,V,W,Z0` are declared in `geometry/sparse_proof.md:111-118`, and Section 4 controls the unused `T,Q,W` directions before solving the optimizer system in `geometry/sparse_proof.md:177-229`. The local check records bounded scaled quantities for `T,Q,W`, including `M(T,T)/(2L)`, `epsilon M(Q,Q)/lambda`, `M(W,W)`, and the scaled cross terms; this supports, but does not replace, the text proof's finite-dimensional Schur argument.

The common-event Fisher cross term is present and used. The proof identifies the common-event contribution to `F(U,V)` in `geometry/sparse_proof.md:157-165`, warns that omitting it changes the sign mechanism in `geometry/sparse_proof.md:167-170`, and carries the corrected term into the two-dimensional solve in `geometry/sparse_proof.md:231-266`. The symbolic check `sparse_limit_algebra.py` reran on the server with exit 0 and confirmed the displayed coefficient
`kappa[(2lambda-1)-lambda(1-lambda)m]/((1-lambda)J)`.

The root existence and localization argument is sound within the stated asymptotic scope. The determinant of the leading two-dimensional system is positive in `geometry/sparse_proof.md:244-249`; the closed coefficient `C(kappa)` is derived in `geometry/sparse_proof.md:255-266`; the `det(N) alpha=1-1/(lambda L)+O(L^-2)` estimate is justified in `geometry/sparse_proof.md:268-290`; endpoint signs, IVT existence, and all-zero localization in `[1,10]` are handled in `geometry/sparse_proof.md:292-318`.

## Finite certificate audit

The finite certificate is accepted, but only for its distinct rational finite kernel. It is not the normalized `s=2/5` analytic family. The script itself says the certified family is
`K=epsilon I+(7/10)uu^T`, `u=(3/5,4/5,q sqrt(epsilon))` in `mechanism/scripts/sparse_rational_certificate.py:4-12`, and the JSON explicitly notes that this is not the unit-normalized PR30 Part III family.

The interval arithmetic design is adequate for the finite claim. Fractions are rounded outward on a dyadic grid, division excludes zero, logarithms use rational atanh-series enclosures, and the interval solve records pivots excluding zero; see `main/interval_soundness.md:7-56` and `proof.md:857-914`. The script implements those checks in `mechanism/scripts/sparse_rational_certificate.py:124-232` and `:274-366`, with the command-line `--cert-steps` control in `:373-456`.

I reran the finite certificate on the authorized server area with `--cert-steps 60`, one thread, no GPU use, and the provided virtual environment.

- Output JSON: `/root/i05-seven-fronts-20260909/C2/verification2/beta/outputs/sparse_rational_certificate_cert60.json`
- Local copy: `evidence/server_cert60/sparse_rational_certificate_cert60.json`
- Exit file: `evidence/server_cert60/sparse_rational_certificate_cert60.exit`
- Stderr: zero bytes
- Owned PID: `166322`
- Exit status: `0`
- Runtime: `25.97435212135315` seconds
- Python: `3.12.3`, mpmath `1.3.0`
- Thread env recorded as `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`
- Script SHA256: `5ef212fafa0ce3b8f9f5c13768b8aea9bc59c1077bb8d2b669e0c561599f74e8`
- `mechanism_probe.py` SHA256: `13191b5147f5e1f14132ba5a2c54a71fde097f71feb575b418af3dfc21f07236`

The rerun status was `CERTIFIED_RATIONAL_SPARSE_ROOT_DALPHA_LT_ONE`. The certified q bracket is
`[4418854248579277079/2305843009213693952, 8837708497158554159/4611686018427387904]`.
The endpoint signs are strictly enclosed:

- left `beta sqrt(Z)` lower bound: `4.67407989657799e-22`
- right `beta sqrt(Z)` upper bound: `-2.493935158520791e-21`

The whole bracket satisfies:

- `det(N) alpha <= 0.925806704946127239064572716414179284 < 1`
- `min p_M >= 7.0000003569096650512e-17`
- `det(N) >= 27.239469784153905029728592116166290683`
- `N` leading minors positive
- all interval Gaussian pivots exclude zero
- residual intervals contain zero

This proves an exact beta zero in the displayed finite q bracket and a whole-bracket `det(N) alpha < 1` bound for that rational kernel family. It is a finite kernel certificate, not an analytic proof of the normalized root tube.

## Remaining limits

I found no PR30-scoped critical gap requiring a fix. The accepted scope is narrow: it does not certify PR31, global B0, uniqueness of finite-epsilon roots, an explicit epsilon threshold, or any counterexample to B0. The analytic proof is still a natural-language asymptotic proof, not a machine-checked theorem, but the dangerous points requested for this review were addressed: full Fisher, all six directions, K-affine derivatives, common-event cross term, uniform finite-dimensional remainders, and the PR24 N-dependency binding.
