# PR51 first independent proof review

Verdict: `ACCEPTED_SCOPED`.

I accept the public PR51 proof for the frozen half-filled missing-edge theorem only:

\[
K(b,c)=\begin{pmatrix}1/2&0&b\\0&1/2&c\\b&c&1/2\end{pmatrix},\qquad bc\ne0,\quad 4(b^2+c^2)<1,
\]

and every nonzero real symmetric `3 x 3` direction `D`, with

\[
\left.{d^2\over dt^2}H(K(b,c)+tD)\right|_{t=0}<0.
\]

This is not an acceptance of general real three-point entropy concavity, unequal-diagonal missing-edge centers, arbitrary chords outside the stated family, novelty, CI status, or proof-assistant formalization.

## Sources read

Frozen public head: `4baebc317896278dcb8f0947d308fdce037c87cf`.

I read these files in full:

- `research/I05-22-missing-edge-20260909/proof_half_filled.md`
- `research/I05-22-missing-edge-20260909/sources_and_routes.md`
- `research/I05-22-missing-edge-20260909/verification.md`

The source itself marks the work as author proof, not independent review (`proof_half_filled.md:3`; `verification.md:1-3`), and says the private author verifier is not public proof evidence (`verification.md:35-39`). I did not fetch or use the private Drive code.

## Per-claim review matrix

| Claim | Source lines | Review result |
|---|---|---|
| Exact theorem statement, legal center, full six-direction quantifier | `proof_half_filled.md:7-23` | Accepted in scope. The domain gives eigenvalues `1/2, 1/2±sqrt(b²+c²)` and strict legality for `4(b²+c²)<1`. The strict claim is only for `bc!=0`; axes receive only non-strict continuity, and arbitrary chords are excluded. |
| Eight complete-event probabilities and cofactor acceleration identity | `proof_half_filled.md:25-52` | Accepted. I independently reconstructed the eight atoms by determinant inclusion-exclusion and checked the identity `B=F+2 sum l_ij det(D_ij)+2 Lambda tr(K adj D)` symbolically. |
| Sign reduction, half-filled atoms, `Lambda=0`, and positive `N` | `proof_half_filled.md:54-83` | Accepted. Diagonal sign conjugation preserves principal minors and gives a bijection on real symmetric directions. The atom formula is exact; `|d|<s` gives the stated log-weight signs. |
| Complement/sign involution and exact `2+4` Hessian decomposition | `proof_half_filled.md:84-91` | Accepted. I checked the cross-sector Hessian entries vanish in the complete quadratic form; this is a real symmetry decomposition, not a deletion of mixed directions. |
| Two-dimensional sector positivity | `proof_half_filled.md:93-99` | Accepted. The sector formula matches the complete event/Fisher expression, and `g(s)±g(d)>0` for `0<s<1`, `|d|<s`. |
| Four-dimensional sector scores, Fisher denominators, and acceleration | `proof_half_filled.md:101-138` | Accepted. I checked the displayed scores, complementary score pairing, full Fisher formula with denominators `1-s²` and `1-d²`, and acceleration formula. Rare-event denominators are retained. |
| Shape-continuation certificate: `dot G`, determinant, `r=0` seed, inertia, and integration from singular `G0` | `proof_half_filled.md:140-195` | Accepted. I independently checked the rational derivative matrix determinant, all four `r=0` leading principal minors, and `G_0=diag(2,2,4,0)`. The logic is sound: for fixed `s`, determinant nonzero on connected `r∈(-1,1)` keeps inertia constant from the positive `r=0` seed; then for fixed `r`, integrating positive definite `dot G_u(r)` over `u∈(0,s)` makes `G_s(r)` positive definite despite singular `G0`. |
| Illustrative Jensen calculation | `proof_half_filled.md:197-223` | Accepted only as an illustration. I checked the rational atoms, legality of the three kernels, and the 60-term atanh log enclosure. The computed interval is contained in the declared negative interval. It is not theorem evidence and not a counterexample. |
| Dependency and scope statements | `proof_half_filled.md:224-228`; `sources_and_routes.md:55-71`; `verification.md:41-45` | Accepted as boundary text. PR51 re-derives what it needs and does not use PR41/PR43 as accepted theorem black boxes. General unequal diagonals and general real three-point concavity remain outside scope. |

## Independent exact checks

Files in this review directory:

- `frozen_scope.md`
- `COMPUTE_PLAN.md`
- `independent_pr51_symbolic_checks.py`
- `independent_pr51_symbolic_checks.json`

Execution record, sanitized:

- Existing checker process checked before run.
- Arithmetic threads capped with `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`.
- No GPU used.
- Python `3.12.14`, SymPy `1.14.0`.
- Final sanitized run elapsed `82.806639` seconds.
- Result: `PASS_EXACT_PUBLIC_IDENTITY_CHECKS`.

The checker imports no author verifier and no PR41/PR43 code. It checks:

- general eight-event formulas from principal minors and Möbius inversion;
- the cofactor acceleration identity;
- half-filled atom weights and the `2+4` cross-block vanishing;
- the two-sector and four-sector formulas;
- the rational `dot G` determinant and `r=0` seed minors;
- `G0=diag(2,2,4,0)`;
- the declared negative Jensen interval using exact rational log bounds.

## Counterexample and gap attempts

I specifically attacked the places where this proof could have hidden a scope error:

- sign changes of `b,c`: no gap; diagonal sign conjugation is invertible on directions and preserves event probabilities;
- missing-edge direction `D12`: no gap; it remains in the four-dimensional sector through `R`/`T`;
- cross-sector mixed terms: no gap; symbolic cross derivatives vanish in the full quadratic form;
- rare probabilities near `s=1`: no gap inside the strict domain; the proof retains the exact denominators and does not claim the endpoint;
- near axes `r→±1`: no gap in stated scope; strictness is not claimed at `bc=0`;
- singular seed at `s=0`: no gap; positive definite derivative for every `u>0` makes the integrated block strict for `s>0`;
- Jensen illustration: no counterexample; the checked gap is strictly negative and explicitly not used as proof.

I found no material gap in the public proof within the frozen PR51 scope.

## Limitations

This review does not certify:

- unequal diagonal missing-edge centers;
- all strict real three-point kernels;
- dimensions above three;
- complex Hermitian kernels;
- stationary entropy-rate claims;
- arbitrary chords leaving the half-filled family;
- novelty or publication priority;
- the private author verifier or any non-public artifact.

The acceptance is scoped to the public analytic proof at PR51 head `4baebc317896278dcb8f0947d308fdce037c87cf`.
