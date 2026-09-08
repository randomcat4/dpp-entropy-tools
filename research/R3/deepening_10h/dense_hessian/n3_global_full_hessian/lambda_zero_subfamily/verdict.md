# D10-U10g verdict

GLOBAL STATUS: INCOMPLETE.
NEW ANALYTIC RESULTS: PROOF/IDENTITY CANDIDATES PENDING INDEPENDENT REVIEW.
FINITE COMPUTATION: SCOUT / AUTHOR SANITY ONLY.

No entropy nonconcavity counterexample and no full Lambda-zero theorem is
claimed. This is an author research unit, not a non-author audit.

## Delivered progress

1. [Complete parameterization candidate](derivation.md): up to diagonal sign
   conjugation, connected strict Lambda-zero kernels are exactly
   K=L(I+L)^(-1) with Lij=w_i w_j/(z_i+z_j), positive w_i and distinct
   positive z_i. It retains arbitrary external fields, not just centered
   or exchangeable kernels.
2. Exact external-field score identity F^(-1)eta=D_f and capacity
   eta^T F^(-1)eta=f^T Cov(Y)f, f_i=1/Nii.
3. Exact remaining three-by-three test
   T=C-CJC+U^T(Fzz^(-1)+Z^(-1))^(-1)U>0, equivalent to full B>0.
   The equivalent scalar rho is explicitly given in derivation (10).
4. [Explicit neighborhood candidate](proof_or_blocker.md): at
   Kstar=K(1/2,3/10), the closed Frobenius ball of radius
   49/214688160 (about 2.28238e-7) is strictly feasible and has
   B(D,D)>=(1/6)||D||_F^2 for ALL symmetric D. An explicit three-parameter
   external-field box remains exactly on Lambda=0 and contains dense K.
5. Strict analytic shortcut blocker: on the centered path with
   r=8a^2=1-2^(-16), the optimized Fisher-only proxy (2/3)delta V>5/4,
   although the independently reviewed centered theorem gives B>0.
   This refutes only a proposed sufficient test as a universal route;
   it is not a rho>1 or entropy-curvature counterexample.

## Evidence denominator

[sanity.py](sanity.py) uses only the Python standard library, reconstructs
Möbius events and their polynomial jets, and does not import another
research implementation. [sanity.json](sanity.json) freezes all matrices,
atoms, input hashes, and numerical values.

- 15/15 exact rational kernel points: one path base, three Cauchy bases plus
  their three sign conjugates, and eight rational external-field corners.
- 270/270 exact rational entries of F[C;U]=[I;0]; all 15 exact Lambda ratios
  equal one and exact LDL tests certify 0<K<I.
- At all 15 points, 120-digit decimal checks agree on the full direct
  event Hessian, U8 cofactor form, three-by-three Schur, and rho. All have
  B>0 numerically; no positive-curvature candidate was found.
- Five evaluations approaching the centered boundary illustrate the
  separately proved Fisher-proxy divergence. They are not five certified
  intervals or evidence for a global conclusion.
- No rejected point, hidden restart, random search, or failed execution.

At the original path blocker, rho=0.5132681842709295321197418640... . The
earlier coarse-category failure does not persist as a failure of the actual
Hessian; the explicit ball conclusion is analytic, not inferred from the
eight nearby finite corners.

## Exact remaining problem and fragile steps

Prove derivation (9)>0, equivalently (10)<1, for every Cauchy parameter
in (3), or find a rigorously certified violating point. No current bound
controls the retained W term sharply enough over that full domain.

Independent review should prioritize the two branches of the Cauchy
classification, the offdiagonal coordinate factors in Z, the noncommuting
parallel-sum identity for W, the core Frobenius-norm conversion, and the
ordered-column counts in the explicit third-derivative bound. The source
centered theorem is reviewed; the new radius and structural reductions
still require a fresh non-author review.
