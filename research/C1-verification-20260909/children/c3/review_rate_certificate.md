# C3 review of PR29 fixed C3-M1 rate certificate

Verdict: `ACCEPTED_SCOPED`.

Covered version: PR29 frozen commit `648f1906468e3e548410f98a6b1a53a978f2ea11`.

Inputs used for this part:

- `sources/pr29/rate/certificate_theory.md`
- `sources/pr29/rate/rate_analysis.md`
- `sources/pr29/rate/scripts/c3_m1_variational_boundary.py`
- `sources/pr29/rate/scripts/c3_m1_rate_certificate.py`
- `sources/pr29/rate/scripts/c3_m1_audit.py`
- `sources/pr29/rate/candidate.json`
- `sources/pr29/rate/candidate_true_symbol.json`
- `sources/pr29/rate/artifacts/c3_m1_boundary_M64.json`
- `sources/pr29/rate/artifacts/c3_m1_rate_n4.json`
- `sources/pr29/rate/artifacts/c3_m1_audit_result.json`

This is a fixed-object true entropy-rate certificate review. It is separate from the radial theorem and is not a finite-window entropy substitute, a family theorem, or a positive-counterexample search.

## Theory and source checks

The certificate theory states the separation from the radial theorem (`certificate_theory.md:3-5`) and the fixed-object nature of the conclusion (`certificate_theory.md:123-125`). The rate analysis also states that C3-M1 is a strict fixed-object negative gate, not a solution of the global scalar entropy-rate conjecture and not an independent non-author review by itself (`rate_analysis.md:3-5`, `rate_analysis.md:251`).

For the external conditioning facts, I spot-checked the cited primary source: Russell Lyons and Jeffrey E. Steif, "Stationary Determinantal Processes: Phase Multiplicity, Bernoullicity, Entropy, and Domination", https://rdlyons.pages.iu.edu/pdf/dyn.pdf . In the fetched PDF text, Lemma 2.4 gives the Toeplitz determinant cylinder probabilities (lines 546-567), Theorem 2.1 gives conditional negative association after finite conditioning (lines 416-422), Proposition 2.6 gives the stochastic monotonicity when conditioned bits are changed from `0` to `1` (lines 635-642), equation (6.5) gives the entropy-rate conditional expectation formula (lines 2061-2072), Proposition 6.10 uses the same extreme-boundary entropy bounding method (lines 2073-2121 and 2123-2175), and Theorem 6.12 records the determinantal law for the all-one limiting condition (lines 2222-2240). This supports the direction used in `certificate_theory.md:66-79` and the true-rate enclosure in `certificate_theory.md:81-100`.

## Fixed symbol and convention

The true symbol file declares
`K(i,j)=c_(i-j); c_k=(a_k+i*b_k)/2` (`candidate_true_symbol.json:3-10`). The script input declares the S1 script convention `c_k=(a_k-i*b_k)/2` and stores `b,db` as the negatives of the true values (`candidate.json:4`, `candidate.json:9-12`). The scripts implement exactly that convention (`c3_m1_variational_boundary.py:66-73`, `c3_m1_rate_certificate.py:71-75`, `c3_m1_audit.py:78-85`).

I independently tracked the indices: substituting `b_script=-b_true` and `db_script=-db_true` into `c_k=(a_k-i*b_k)/2` gives exactly `(a_k+i*b_true_k)/2` for `K(i,j)=c_(i-j)` at `t=-1/4,0,1/4`. The retrieved reviewer check records equality for all three values. Therefore `candidate.json:6` is imprecise when it says the negation gives conjugate-transpose Toeplitz kernels; it gives the true coefficients under the script convention. `rate_analysis.md:130` already says this correctly. This is a non-blocking documentation clarification, not a mathematical certificate failure.

The uniform margin is certified by the exact comparison in `rate_analysis.md:132-151`, and the checker confirmed `epsilon=1/200`.

## Residual and boundary enclosure

The theory derives the all-one Schur complement as `C_inf=C-B* T^{-1}B` under a uniform Toeplitz margin and covers finite-past convergence by coercivity (`certificate_theory.md:9-18`). It then proves the variational identity `A-C_inf=R*T^{-1}R` and the operator bound by the residual norm (`certificate_theory.md:20-28`). For this degree-two finite-band symbol, only 66 residual rows are relevant and the correction is confined to the leading `2 by 2` future corner (`certificate_theory.md:29-34`).

The boundary script computes six cases, three `t` values times `f` and `1-f` (`c3_m1_variational_boundary.py:166`), forms the finite residual rows (`c3_m1_variational_boundary.py:88-109`), and stores the corner and residual row count (`c3_m1_variational_boundary.py:119-135`). The audit script checks extra tail rows beyond the claimed support are zero (`c3_m1_audit.py:205-217`) and that the case set and margins are as expected (`c3_m1_audit.py:228-254`).

My replay reproduced all substantive boundary fields against the public artifact. The worst recorded operator error was
`103102734785879936942709491842154416559456555640673507007256125183969655460805281827107601774081/1089460187671460187525580821231780056053109441628010745311488572069723171134415712539211812442000588800`, about `9.463653280093224e-08`, below `1/200`. All six cases had `residual_rows_checked=66`.

## Finite events to true rate

The theory uses the Schur formula for conditional probabilities (`certificate_theory.md:38-50`), an operator-error Lipschitz bound uniform in suffix length (`certificate_theory.md:52-62`), and the all-one/all-zero conditional negative-association sandwich
`q_1(gamma)<=P(X_v=1 | entire past)<=q_0(gamma)` (`certificate_theory.md:66-79`). It then forms suffix-probability weighted lower and upper bounds for the true entropy rate (`certificate_theory.md:81-100`). The lower bound uses the minimum of binary entropy over the certified interval; the upper bound uses the ordinary finite-suffix conditional entropy, which is above the entire-past conditional entropy.

The rate script computes exact finite event masses by integer-scaled Bareiss determinants and checks positivity and exact normalization (`c3_m1_rate_certificate.py:35-68`). It then computes, for each of the three `t` values, the raw finite distribution plus the two boundary distributions, verifies the conditional interval is nonempty and contains the finite conditional probability, and accumulates the lower/upper rate intervals (`c3_m1_rate_certificate.py:126-180`). Finally it forms the negative gate using endpoint upper bounds minus the center lower bound (`c3_m1_rate_certificate.py:221-244`), matching the exact-arithmetic sign rule in `certificate_theory.md:111-121` and `rate_analysis.md:215-235`.

My reviewer checker recomputed the small exact event probabilities with a separate permutation determinant routine rather than the supplied Bareiss routine. It confirmed 288 determinant evaluations, three exact distributions per symbol, exact conditional ranges, and weighted width containment for all three symbols.

## Replay record

Remote replay environment, recorded in `children/c3/compute_replay/logs/version.json`:

- Python `3.12.3`
- numpy `2.1.2`
- mpmath `1.3.0`
- sympy `1.13.3`
- one-thread BLAS/OpenMP environment and no GPU

Replayed commands were the frozen `M=64`, `bits=160`, `n=4` commands only. No larger `n`, larger `M`, precision expansion, or random scan was run.

Replay results:

- Boundary step: exit `0`, 6 cases, peak RSS about 22.6 MiB, worst delta about `9.46e-08`.
- Rate step: exit `0`, 288 determinants, classification `NEGATIVE_PAIR_GAP`.
- Supplied audit replay: exit `0`, status `CORRECT_SELF_AUDIT`.
- Reviewer checker: status `REVIEWER_CHECK_PASS`.

The exact recomputed pair-gap enclosure is:

```text
lower =
-21736338200350506195187245238231755852533113
/22835963083295358096932575511191922182123945984

upper =
-299855012916397501897282364769067397783
/356811923176489970264571492362373784095686656
```

Since the upper endpoint is strictly negative, the fixed C3-M1 true entropy-rate pair gap is certified negative under the stated DPP conditioning theorem and finite-band residual certificate.

## Remaining scope limits

This accepts only the fixed C3-M1 three-symbol negative true-rate certificate. It does not prove scalar entropy-rate concavity for any family, does not provide a positive counterexample, does not certify long-range symbols, and does not certify mathematical novelty.
