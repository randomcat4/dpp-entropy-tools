# PR88 independent bounded SECOND review

## Executive verdict

The PR88 packet is internally careful about scope. The analytic parts prove restricted mechanisms, not the unrestricted rank-two midpoint conjecture. I find the main symbolic proof structure `CORRECT` within the stated boundaries: full rank-two Cauchy--Binet/Mobius expansion, the three-coordinate indefinite direction mechanism, the common dense-mode conditional decomposition, coordinate-supported whole-chord Fisher strictness, fixed affine boundary asymptotics, and common bit-flip continuity.

The finite certificates are not independently closed here. The method bridge fixture, six-point numerical certificates, multiring 64 atoms, beta `6784/16875`, conditional obstruction matrix/ratios, and displayed interval signs are author computations only. They remain `SOURCE_ONLY` without a C2 reconstruction.

## Binding and redaction status

The frozen head is `6c8ad2eaedcc93c7dfc5417b2d71b4e826d9be5c`. All six delivered files match their delivered SHA-256, line counts, and byte counts. Three markdown files have delivered SHA values different from original SHA values because six nonmathematical review-history/status snippets are withheld or adjusted by the binding. The delivered lines are: `README.md:42`, `proof.md:83,186`, and `continuation.md:21,86,166`.

The local packet is not a git repository, so I could not independently verify `original_git_blob -> original_sha256`. The redaction claim that mathematics was preserved is therefore a binding statement, not something rederived from original blobs inside this review.

## Full rank-two Cauchy--Binet, Mobius, and mixed areas

`proof.md:15-79` correctly treats a rank-two endpoint pair as a genuine four-column Cauchy--Binet expansion. The determinant identity retains all pair mixed terms, and it explicitly records the triple and quadruple terms that a rank-one splitting argument would lose. The midpoint atom formula uses full Boolean Mobius inversion, including the empty event and all alternating containing minors.

The pair mixed-discriminant inequality at `proof.md:55-61` is used only as an inclusion-minor fact. The proof correctly warns that it does not imply the sign of `C_ij-a_ij^2-b_ij^2` and therefore cannot by itself produce an entropy bridge. This gate is `CORRECT`.

## Three-coordinate indefinite direction and rank-one strictness

`proof.md:81-101` reproduces the three-coordinate indefinite rank-two mechanism. The coefficient law in (6) is pinned by total, singleton, pair, and triple Mobius moments; the nonpositive two-coordinate DPP covariance gives the sign of the log pairing; the full Hessian keeps both Fisher and acceleration terms. Boundary kernels are handled by common bit-flip regularization rather than by rotating observed coordinates.

The rank-one strictness mechanism at `proof.md:169-186` is also coherent: it gives an explicit path from the endpoint mixture law to the rank-two midpoint law, computes the entropy derivative, and uses Lagrange's identity to get strict positivity on the active interval. This is `CORRECT` as a reproduced mechanism, not a novelty claim.

## Common dense mode with complete conditioning

Theorem 1 in `proof.md:103-168` is correctly limited. It assumes a common dense mode plus two moving directions supported on three actual coordinates. The outside law is independent of the moving rank-one component, the empty-outside branch keeps the full common-mode interaction through a Schur complement, and the occupied-outside branch cancels the common mode exactly. The entropy chain rule then separates a nonnegative three-coordinate branch and a strict rank-one branch.

The stated support condition matters. This does not prove anything for arbitrary unrelated rank-two endpoints, and it does not authorize spectral-coordinate replacement. The six-point numerical values in `fixtures.md:96-130` are `SOURCE_ONLY`; the later all-epsilon analytic bound in `continuation.md:84-118` follows instead from Theorem 3.

## Coordinate-supported whole chord and Fisher strictness

Theorem 3 in `continuation.md:5-82` is `CORRECT` within its exact hypothesis: the rank-two indefinite difference must be supported on a set of three actual observation coordinates. For strict chords, the outside complete event law is fixed; Schur factorization gives conditional three-coordinate affine kernels with the same direction; and the weighted conditional Fisher identity recovers the full complete Fisher term. The Cauchy--Schwarz statistic bounds give explicit midpoint margins from a diagonal entry or, when all diagonals vanish, from an occupied-pair statistic.

The boundary extension by common bit flips is also sound in scope. The scaling factors are stated, entropy continuity supplies the limit, and the result remains a coordinate-supported theorem rather than a theorem about arbitrary spectral rank-two directions.

## Fixed affine multiple-boundary theorem

Theorem 2 in `proof.md:188-243` is `CORRECT` for a fixed affine legal line. The expansion separates atoms positive at the boundary, simple zero atoms, higher-order zero atoms, and identically zero atoms. The leading singular Fisher term is exactly `-beta/h`, while acceleration contributes only `O(1+|log h|)`. The count-generating determinant is used only to force positive emerging mass in complete configuration layers; it is not substituted for configuration entropy.

The quantifiers are properly limited. The theorem gives endpoint neighborhoods for each fixed line and shows beta positivity for strict inward directions and fixed moving rank-two chords near endpoints. It does not provide uniform neighborhoods when angles or degeneracy scales vary, and it does not settle the compact middle.

## Strong multiring construction

`continuation.md:120-243` gives a fixed true affine 3+3 construction. The legality formula and the multiple endpoint geometry are stated analytically. The conditional sufficient test failure is also presented as a method failure, not as positive entropy curvature.

The exact 64 atom quartics, beta `6784/16875`, the conditional matrix and offdiagonal ratios, and the three local interval probes are finite author certificates. Under the current instructions they are `SOURCE_ONLY`. The whole compact middle remains `INCOMPLETE`, as the text itself says at `continuation.md:237-243` and `fixtures.md:132-136`.

## Method obstruction versus real entropy counterexample

`fixtures.md:1-94` correctly separates the auxiliary bridge

`H((p_A+p_B)/2)-H(p_(A+B)/2)`

from the true Jensen sign `Delta=(H(A)+H(B))/2-H((A+B)/2)`. The packet claims a bridge failure but also records true Delta as negative, so it does not claim a real DPP entropy-concavity counterexample. The exact signs are still author finite outputs and remain `SOURCE_ONLY`, but the logical distinction is `CORRECT`.

## Common bit-flip continuity

`proof.md:245-265` gives a self-contained finite-alphabet continuity argument. The common bit-flip channel preserves the midpoint relation, bounds total variation by `delta=1-(1-epsilon)^n`, and applies the same two-omega loss to the Jensen gap and the auxiliary bridge comparison. This gate is `CORRECT`; lifted finite numerical signs in the certificate remain `SOURCE_ONLY`.

## External sources

I did not need a new literature lookup. The packet restates the relevant ingredients internally: count generation via `det(I+(z-1)K)`, complete conditioning via signed Schur determinants, and the finite-alphabet continuity proof. HKPV, Lyons, and Audenaert therefore remain background support in this review, not extra unverified dependencies required to close the scoped gates. Novelty is `NOT_ASSESSED`.

## Final gate table

- `CORRECT`: delivered hash/line/byte binding; full rank-two Cauchy--Binet/Mobius/mixed-area bookkeeping; three-coordinate indefinite mechanism; rank-one strictness; common dense-mode conditional decomposition; coordinate-supported whole-chord Fisher strictness; fixed-line multiple-boundary asymptotic; common bit-flip continuity.
- `SOURCE_ONLY`: `verify.py`, `certificate_compact.json`, method fixture signs, six-point finite certificate, multiring 64 atoms, beta rational, conditional obstruction arithmetic, and interval displays.
- `INCOMPLETE`: original blob/redaction equivalence verification; unrestricted moving rank-two midpoint inequality; unrestricted real-kernel conjecture; multiring compact-middle sign; any global theorem from finite probes.
- `NOT_ASSESSED`: novelty / priority.
- `NOT_PERFORMED`: formal verification.
