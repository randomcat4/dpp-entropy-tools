# D10-M8 author verdict

GLOBAL: INCOMPLETE.

ANALYTIC REFINEMENT: CORRECT_AFTER_INDEPENDENT_REVIEW.
FINITE COMPUTATION: SCOUT / EXACT SANITY.

The candidate refinement combines the singleton/pair accelerations before
bounding them. It yields three explicit base-dependent coefficients C_i,
with A=2 sum_{j<k}v_j v_k C_i. The exact criterion C_i>=0 for all i is
equivalent to nonnegativity of this acceleration on the full nonnegative rate
cone. It is only a sufficient condition for total entropy concavity.

The simple analytic corollary is

    min_a alpha_a beta_a > 1/27  =>  H''<0 for every nonzero one-sign rate.

In particular, two conditional layers with every atom >=1/5 are covered
(each atom is then automatically <=3/5). This strictly extends the M7
[1/4,4/9] subregion and its stated logarithmic sufficient region. It uses
normalization, paired complementary jets and AM--GM, not layerwise L1 bounds.
Quantitative constants and single-rate strictness are proved in the draft.

There are explicit connected, heterogeneous, distinct-spectrum rational
examples outside M7. One has min conditional atom 23/147<1/5 but satisfies
the joint-product criterion throughout an exactly certified |t|<=1/100
segment; its spectral margin is 29/150. Another satisfies the one-fifth
condition but not M7. A third fails the product test but passes the three C_i
sign tests by exact rational exponent clearing, showing a further strict
hierarchy of pointwise sufficient tests.

All direction quantifiers are fixed-Q spectral rates, equivalently commuting
PSD/NSD directions; not arbitrary noncommuting PSD directions. Conditions are
pointwise unless explicitly certified over a segment. Uniform constants require
a strict spectral margin and a uniform positive product/coefficient margin.
No strictness claim is made merely from m=1/27.

The global blocker is unchanged: if some C_i<0, the count and Fisher terms
may compensate, but their general domination has not been proved. The global
Psi''<=0 shortcut remains false. No finite optimizer or finite number of
centers resolves this missing implication.

The fresh non-author audit under `verifications/` independently checked the
complementary-index alignment, row/column stochasticity, AM--GM signs,
single-rate boundary, count-Hessian input, exponent clearing, all six exact
centers and all 12 interval attempts. Ten attempts pass and the two retained
failures match the author denominator; they are failed sufficient-condition
certificates, not positive-curvature cases.

No novelty certification is claimed. The count theorem is known; the result is
an independently checked analytic sufficient-region refinement, not a global
solution.
