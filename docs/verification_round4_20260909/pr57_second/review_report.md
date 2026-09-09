# pr57 SECOND Review Report

STATUS: CORRECT

I find the frozen `r=0` candidate proof and its explicit certificates sufficient for the accepted scope. The proof does not infer positive definiteness from determinant positivity alone: it proves global nonsingularity of the real symmetric `Rstar`, combines that with one exact positive seed inside the connected domain, and then uses inertia continuation before applying the accepted Schur lift to the six fixed physical directions.

## Reviewed Inputs

- `frozen_contract.md` lines 7-24 define the exact SECOND obligation: `r=0`, `|mu|<1`, `|nu|<1`, `0<u<1`, starting from the displayed four-by-four `Rstar`, with determinant/P/Q, domain denominators, positive seed, nonvanishing, continuity, connectedness, inertia, and Schur lift all required.
- `inputs/source/structure/STRUCTURE.md` lines 137-160 give the fixed-coordinate derivative bookkeeping; lines 167-200 give the positive eliminated two-dimensional block; lines 207-254 give the four-variable quadratic form and explicit Schur complement; lines 291-310 separate what the structure note did and did not already prove.
- `author_proof.md` lines 27-76 state the `r=0` formulas and the algebraic identities checked by the verifier.
- `author_proof.md` lines 80-145 state the determinant, `P`, `Q`, coefficient, denominator, and nonvanishing chain.
- `author_proof.md` lines 147-177 state the seed and inertia continuation.
- `author_proof.md` lines 179-210 state the Schur lift back to the six fixed physical directions.

## Source-To-Code Binding

The implementation constructs the displayed `r=0` objects directly in `implementation/verify_r0_chain_independent.py` lines 400-491. I checked those formulas against the frozen STRUCTURE source:

- `a=b=1/2`, `v`, `w`, `J`, `L=1`, `d0`, `d1`, `d0'=d1'=2u^3/J^2`, `R`, `n1=n2=4u/J`, and `n3=4u^3/J` match `author_proof.md` lines 27-42 and STRUCTURE lines 137-160 and 287-289.
- The matrix `S` in code lines 415-423 matches STRUCTURE lines 103-115.
- `R0` in code lines 434-441 matches STRUCTURE lines 235-240.
- The simplified coupling rows in code lines 443-444 match STRUCTURE lines 218-224 after setting `r=0`, `a=b=1/2`, and `theta=(mu+nu)/2`.
- The in-script checks in lines 460-465 verify `S D^{-1} S=D`, the null-block identity `u^2(n2*b+n1*a)=n3`, and equality of simplified coupling rows with the unsimplified rows.

The code does not parse STRUCTURE into formulas; it hard-codes the formulas and checks selected source fragments in lines 360-397. That is acceptable for this SECOND review because the hard-coded formulas were explicitly reviewed against the displayed source lines above. It would be a reproducibility improvement, not a mathematical gap, to make future tooling parse a structured formula file.

## Certificate Review

The determinant layer is adequate. The code clears rational denominators in lines 494-518, computes the cleared determinant by fraction-free Bareiss in lines 542-612, and separately computes the 24-term Leibniz determinant in lines 615-624. The equality is checked in lines 655-667. The artifact `determinant_bareiss_certificate.json` records 17 Bareiss records with 5 exact division records and zero nonzero remainders. The artifact `determinant_independent_equality.json` lines 10-17 records exact equality of Bareiss and Leibniz determinants. The Bareiss records are used only as exact polynomial division certificates, matching `author_proof.md` lines 87-90; no domain-wide pivot nonvanishing is assumed.

The `P` layer is adequate. Code lines 672-703 extract `P` by multiplying the determinant by `2J^5/[(1-mu^2)^2(1-nu^2)^2]`, reject residual denominators, coerce to `ZZ[mu,nu,u]`, require degree box `(4,4,16)`, and recheck the rational identity. `P_polynomial.json` lines 1-17 records the polynomial, the degree box, and a zero remainder for the determinant/P identity. The later archived comparison in code lines 712-767 is correctly downstream of fresh `P`; `archived_P_source_factor_comparison.json` lines 7-12 records exact equality over the full degree box.

The `Q` layer is adequate. Code lines 770-792 perform the direct homogeneous substitution, lines 812-842 perform coefficient-wise binomial expansion, and lines 845-883 prove the two transforms equal, require the same `(4,4,16)` box, reject terms outside the box, reject nonpositive nonzero coefficients, and write the full 425-entry box. My JSON check of `Q_polynomial_full_box.json` found 425 box entries, 389 positive entries, 36 zero entries, no negative entries, minimum positive coefficient 192, maximum coefficient 99220032, and an exact zero remainder for direct-vs-combinatorial equality. Since `X,Y,U>0`, every nonzero monomial is strictly positive and at least one exists, so `Q(X,Y,U)>0` throughout the positive orthant.

The domain and denominator layer is adequate. The Cayley substitution in `author_proof.md` lines 108-119 is a bijection between the open original domain and `X,Y,U>0`, and the clearing multiplier in lines 121-126 is strictly positive there. The determinant prefactors in `author_proof.md` lines 141-145 are strictly positive on `|mu|<1`, `|nu|<1`, `0<u<1`. `domain_inertia_certificate.json` lines 15-38 records the same map, positivity of `u`, `J`, `1-mu^2`, `1-nu^2`, `v`, `w`, `d_alpha`, and `d_beta`, and the nonvanishing/inertia/Schur chain.

The seed and inertia layer is adequate. Code lines 1178-1224 evaluates the rebuilt `Rstar` at `mu=nu=0`, `u=1/2`, scales by 14400, checks strict diagonal dominance margins, and also checks positive leading principal minors. `positive_seed_certificate.json` lines 38-80 records leading minors and margins `(10068, 88320, 88320, 40053)`. The domain is the convex product `(-1,1) x (-1,1) x (0,1)`. Since `Rstar` is real symmetric and continuous there, and since `det Rstar` never vanishes there, its inertia is constant along every path from the seed. The seed is positive definite, so `Rstar` is positive definite everywhere in the frozen domain.

The lift to `M` is adequate within the accepted reduction. STRUCTURE lines 167-200 give the positive eliminated block with `d_alpha,d_beta>0`; lines 207-254 identify the exact Schur complement; lines 84-91 give the inverse coordinate map, invertible for `u,a,b>0`; and lines 312-338 record the determinant/congruence bookkeeping. At `r=0`, `a=b=1/2`, so the Schur criterion and congruence preserve positive definiteness for all six fixed physical directions.

## Executed By This SECOND Review

- Read the required math-theorem skill and its verification workflow references.
- Checked that there is no `AGENTS.md` in the target output directory ancestry.
- Used only the provided input package plus local skill files as proof sources; did not read `review_first`, PR57 comments, upstream successor packages, `C:\canglan\`, private author files, or Drive material.
- Matched the author proof's displayed formulas, source STRUCTURE formulas, and implementation formulas by line.
- Reviewed the determinant/P/Q/domain/seed/inertia/Schur proof chain mathematically.
- Performed lightweight SHA256 and JSON structure checks on the local copied inputs and author artifacts.
- Checked the recorded `Q` full box counts and signs from JSON: 425 total entries, 389 positive, 36 zero, 0 negative.
- Checked the recorded Bareiss certificate metadata from JSON: 17 records, 5 exact division records, 0 nonzero remainders.

## Not Executed By This SECOND Review

- I did not rerun the full symbolic determinant/P/Q arithmetic chain.
- I did not launch a new arithmetic process or spend the expired/old arithmetic budget.
- I did not independently rederive the all-eight-event `M=d/du(Fmat)+Q` formula.
- I did not verify general `r`, Lambda-nonzero cases, entropy conclusions, prior art, novelty, or conference value.
- I did not perform Lean or other mechanized formal verification.

## Verdict

Within the frozen accepted scope, there are no critical gaps. The displayed-formula-to-implementation binding is sufficiently checked, the determinant certificate is not misused as a direct positive-definiteness argument, the `P -> Q` positive-orthant certificate proves global nonvanishing on the open domain, the positive seed fixes the inertia, and the accepted Schur/congruence reduction lifts the result to the six fixed physical directions. The correct status for this SECOND review is `CORRECT`.
