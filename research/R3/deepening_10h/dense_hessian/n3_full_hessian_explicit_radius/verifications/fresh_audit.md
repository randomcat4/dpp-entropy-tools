STATUS: CORRECT

Scope: this is a non-author audit of the S7 explicit-radius transfer proof in
`research/R3/deepening_10h/dense_hessian/n3_full_hessian_explicit_radius/`.
It certifies the S7 derivation conditional on the already reviewed S5 base
full-Hessian certificate.  It does not certify global DPP entropy concavity,
optimality of the radius, or any result outside this closed `n=3` Frobenius ball.

## Files and author claims checked

Author files read:

- `frozen_problem.md`
- `proof_candidate.md`
- `sanity.py`
- `sanity_results.json`
- `run_log.md`
- `verdict.md`

Relevant frozen statement lines:

- `frozen_problem.md:13-19`: imported S5 inputs, exact-event entropy semantics, and the warning that inclusion determinants are not atoms.
- `frozen_problem.md:25-35`: `L=160561104/841`, `delta=36163/16056110400`, strict contraction, atom floor, and `H''_K[D,D] <= -(43/100)||D||_F^2`.
- `frozen_problem.md:42-43`: closed Frobenius ball in `Sym(3)` and Frobenius inner product, not unweighted six-coordinate norm.

Relevant proof lines:

- `proof_candidate.md:14-22`: Mobius exact atom equals the signed determinant `p_S(K)=(-1)^|C| det(K-I_C)`.
- `proof_candidate.md:32-43`: strictness is established before log estimates.
- `proof_candidate.md:45-64`: determinant derivative counts and Frobenius column bounds.
- `proof_candidate.md:66-71`: atom floor transfer.
- `proof_candidate.md:77-83`: rational bound for `|f'|`.
- `proof_candidate.md:89-98`: third-order chain rule and constants per event.
- `proof_candidate.md:100-103`: eight-event factor and `L`.
- `proof_candidate.md:108-139`: Hessian comparison and final radius.
- `proof_candidate.md:141-167`: equality, chord consequence, structure/scope cautions.

S5 provenance:

- `research/R3/deepening_10h/dense_hessian/n3_full_psd_local/verifications/fresh_audit.md:105-106` gives the prior full-space Frobenius conversion.
- `research/R3/deepening_10h/dense_hessian/n3_full_psd_local/verifications/revision_recheck.md:53-59` rechecks the S5 minimum Gershgorin margin and states
  `H''_{K_*}[D,D] <= -(43/50)||D||_F^2` for every real symmetric `D`.

I did not re-certify S5 from scratch here; I treated it as the frozen verified input promised by S7, while independently recomputing the base atoms/eigenvalues and a high-precision Hessian sanity check.

## Independent command

Working directory:

`C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo`

Command:

```text
$env:OMP_NUM_THREADS='1'; $env:OPENBLAS_NUM_THREADS='1'; $env:MKL_NUM_THREADS='1'; $env:NUMEXPR_NUM_THREADS='1'; $py='C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'; & $py 'C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo\research\R3\deepening_10h\dense_hessian\n3_full_hessian_explicit_radius\verifications\fresh_s7_audit.py'; exit $LASTEXITCODE
```

Exit code: `0`.

Independent outputs:

- `verifications/fresh_s7_audit.py`
- `verifications/fresh_s7_audit.json`

The script does not import the author script.  It uses an independently written `n=3` determinant formula, Fraction polynomial arithmetic in two jet variables, and Decimal only for displayed/log sanity quantities.

## Exact constants

All exact rational checks passed:

- `q = 87/1250`.
- `m = 87/2500 = q/2`.
- `L = 8(27/m^2 + 54/m + 18) = 160561104/841`.
- `delta = min(1/10, q/6, 43/(100L)) = 36163/16056110400`.
- `L delta = 43/100`.
- `q - 3 delta = 9311639957/133800920000 > m`.
- `1/5 - delta = 3211185917/16056110400 > 1/10`.
- `71/100 + delta = 11399874547/16056110400 < 9/10`.
- `sum_{j=0}^4 4^j/j! = 103/3 > 2500/87 = 1/m`, so the proof's rational `log` bound is valid.

This verifies the requested `delta`, `L`, spectral strictness margin, atom-floor margin, and curvature-loss arithmetic.

## Exact-event semantics

I independently reconstructed atoms by Mobius inversion from inclusion determinants:

`p_S(K)=sum_{T superset S} (-1)^{|T|-|S|} det K_T`.

For the same polynomial input I separately evaluated the signed determinant

`(-1)^|C| det(K-I_C)`, `C=S^c`,

and checked equality for all `8` events in the base case and in the boundary mixed-jet samples below.  The atom polynomials sum exactly to one, so the proof does not confuse principal minors with exact atoms.

Base exact atoms, in bitmask order:

`87/1250, 4159/35000, 4099/35000, 5631/35000, 3999/35000, 2803/17500, 5591/35000, 497/5000`.

The minimum is exactly `87/1250`, as frozen.

The stated eigenvalues `(1/5, 7/10, 71/100)` were checked exactly by evaluating the characteristic determinant at the three rational roots; they are distinct.

## Derivative counts and chain rule

I rechecked the determinant derivative counts from column multilinearity:

- one `E` derivative: `3` column choices;
- one `E` and one `D`: `3*2=6` ordered distinct-column choices;
- one `E` and two labelled `D` derivative slots: `3*2*1=6` choices.

Hadamard then gives the proof's bounds

`|p_E| <= 3||E||_F`, `|p_D| <= 3||D||_F`,
`|p_ED| <= 6||E||_F||D||_F`,
`|p_DD| <= 6||D||_F^2`,
`|p_EDD| <= 6||E||_F||D||_F^2`.

The chain rule line is also correct:

`D^3(f∘p)[E,D,D] = f''' p_E p_D^2 + f''(2p_ED p_D + p_E p_DD) + f' p_EDD`.

The factor `2` belongs to differentiating the two first-derivative factors, not to a determinant convention.  With `|f'|<=3`, `|f''|<=1/m`, `|f'''|<=1/m^2`, the per-event bound is

`27/m^2 + 54/m + 18`,

and multiplying by eight events gives exactly the claimed `L`.

## Independent finite checks

My independent script checked more mixed-jet samples than the author sanity:

- perturbation directions: `6`;
- boundary points: `12`;
- directions per point: `7`;
- mixed-jet cases: `84`;
- event-jet checks: `672`;
- failures: `0`.

For these samples:

- all Mobius atoms matched the signed-determinant formula;
- all `p_E`, `p_D`, `p_ED`, `p_DD`, `p_EDD` bounds passed by exact Fraction inequalities;
- all sample atoms stayed in `[m,1]`;
- max observed `|H3|/bound` was about `0.0000673002768982468`;
- max observed `H2 + (43/100)||D||_F^2` was
  `-0.55560925023779481985395724702219355585027934486730081164875570256569412367238655`.

These are sanity checks only; the continuum result follows from the analytic Lipschitz proof plus the S5 base Hessian certificate.

I also independently reconstructed the base Hessian from exact atoms.  In a Frobenius-orthonormal symmetric basis the approximate eigenvalues were

`[-4.193743459777824, -4.158735276026037, -4.151201160463633, -2.2286484229911823, -1.2895466136115992, -1.226348381627505]`.

Thus the largest numerical eigenvalue is well below `-43/50=-0.86`, consistent with the imported S5 certificate and with no sign/norm conversion warning.

## Author sanity artifact checks

I did not rerun `sanity.py`, because it writes `sanity_results.json` in the author directory.  Instead I parsed the existing result and verified the hashes recorded in `run_log.md`.

Author run-log lines:

- `run_log.md:7-13`: command and exit code `0`.
- `run_log.md:15-22`: 48 mixed-jet cases, 384 exact event-jet comparisons, and the `u*t^2` factor-two note.
- `run_log.md:33-36`: script/result SHA records.

Parsed author result:

- `sanity_results.json:7`, `:13`, `:16-19`: constants, atom floor, spectral floor, and curvature loss.
- `sanity_results.json:21-31`: base atoms and eigenvalues.
- `sanity_results.json:6134-6147`: counts, exit code, and script hash.

Computed hashes:

- author `sanity.py`: `4d22c13059f3e19d13e83f3c0a46101293629cd13a966b73e9763ef446618941`;
- author `sanity_results.json`: `e0ef92ca240a6076167d06bfb8ec036f08f2c71cb68d986f95e45a445d1d4ebf`.

Both hashes match `run_log.md`.

## Closed-ball proof audit

The proof of the final closed ball is valid:

1. If `||K-K_*||_F<=delta`, Weyl/operator norm gives the whole segment `K_*+u(K-K_*)` strict, even on the closed ball boundary.
2. The atom Lipschitz estimate gives every atom at least `q-3delta >= m`; logs are therefore uniformly controlled before using derivative estimates.
3. For fixed symmetric `D`,

   `|H''_K[D,D]-H''_{K_*}[D,D]| <= L||K-K_*||_F||D||_F^2`.

4. Since `L delta = 43/100` and imported S5 gives

   `H''_{K_*}[D,D] <= -(43/50)||D||_F^2`,

   the conclusion follows:

   `H''_K[D,D] <= -(43/100)||D||_F^2`.

5. Equality is possible only at `D=0`; every nonzero symmetric direction has strictly negative upper bound.

The Frobenius operator discussion is harmless and correctly scoped; the proof could use only the quadratic-form estimate, and it never switches to the unweighted six-coordinate norm.

## Verdict

No critical gap found.

- S7 exact constants: CORRECT.
- Signed determinant exact-event formula: CORRECT.
- Spectral strictness and atom-floor transfer: CORRECT.
- Third-order chain rule, `3/6/6` determinant counts, and eight-event `L`: CORRECT.
- Frobenius Hessian comparison and closed-ball `H''<=-43/100||D||_F^2`: CORRECT, conditional on the already independently reviewed S5 base bound.
- Author finite sanity artifacts: consistent; independent bounded sanity passed.

No repair is required before sending this S7 proof to a second reviewer, if the project wants another layer.
