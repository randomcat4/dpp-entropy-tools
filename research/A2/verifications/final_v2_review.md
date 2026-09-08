# A2 final v2 independent review

STATUS: CORRECT

## Commit binding

Candidate commit: `ab4d57cdbdc782fd033178795da9873db01bf7be`

All mathematical review below is bound to git blob contents read from that
commit, not to mutable working-tree files.

| Role | Commit path | SHA256 |
| --- | --- | --- |
| frozen v2 | `research/A2/frozen_theorem_v2.md` | `44ef4afbffb63d06b343f2c5e6186a73f80e50b6091d3005a8c4f3dfc2650fca` |
| anonymous proof | `research/A2/proofs/rational_frame_v2.md` | `d1b337a3043a483e0f7414c8252d8257dc1cb60ec7f4ad4301f027923323aa5a` |
| hazards | `research/A2/hazards.md` | `cf1b4faf792efa054d20312312bc2eb8da8d2631d1bfbdc7dae3557135148440` |
| audit tool | `research/A2/artifacts/moving_frame_check.py` | `38b82d9df1b8efb6b9b7d33018d21169ef0591c508c5dcddea765c6d99046b8a` |
| smoke output | `research/A2/artifacts/smoke.json` | `efa556c7ab31483ae63284b5dc72c6ff52b972270ca4bf3c7203a001bb5b6383` |
| certified output | `research/A2/artifacts/certified.json` | `162e25261530f78e46b5a476701da2dab54c09a51da81ea872cbfb6e2e2c5abb` |
| symbolic output | `research/A2/artifacts/symbolic.json` | `f21ee81116fb44c85c90c979e897131335b935a5ec745359dadf22bfec3f4300` |

The old-family facts used for Claim 2 are only the necessary public R2
definitions and verified scope boundary: fixed-data two-term mixed midpoints
are block diagonal relative to one fixed projection, and unequal scalar-slack
midpoints are scalar combinations of one fixed projection and its complement.
No new R2 theorem is asserted here.

## Claim 1: geometry, feasibility, midpoint

The proof establishes the frozen objects in the fixed physical coordinates.
The displayed `U(t)` has orthonormal columns because it is obtained from the
fixed two-column frame by a physical coordinate rotation on coordinates 2 and
3. On `range(U(t))`, the endpoint kernels are represented by
`(1-t)I + sigma t X`, so their eigenvalues are `1-t+tx` and `1-t-tx`;
on the orthogonal complement the eigenvalues are both `t`.

For `0<t<1/2` and `0<x<1`, all these eigenvalues lie strictly between `0`
and `1`. Thus `K_-(t)`, `K_+(t)`, and `K_0(t)` are strict real positive
contractions. The sigma terms cancel exactly, so the midpoint is the actual
arithmetic midpoint `(K_-(t)+K_+(t))/2`, not a nonlinear curve center.

No critical gap found for Claim 1.

## Claim 2: exclusion from direct old fixed-data paths

The proof gives a physical-coordinate midpoint identity

```text
M(t)=I/2+((1-2t)/2)(c(t)A+s(t)B),
```

with fixed real symmetric matrices satisfying `A^2=B^2=I` and `AB=-BA`.
For distinct `t,u in (0,1/2)`, the computed commutator is

```text
[M(t),M(u)]
 = (1-2t)(1-2u)(u-t)(1+tu)
   /((1+t^2)(1+u^2)) AB,
```

which is nonzero throughout the stated domain.

By contrast, the relevant R2 fixed-data midpoint families are pairwise
commuting: the mixed two-term family has the form `P+lambda L` with fixed
block-diagonal `L` commuting with `P`, and the unequal scalar-slack family has
the form `alpha(lambda)P+beta(lambda)(I-P)`. A single fixed orthogonal
representation conjugates all midpoint matrices together and therefore
preserves pairwise commutativity. A common scalar reparameterization cannot
turn a noncommuting physical midpoint family into a commuting one; if it
identified two distinct parameters, it would force identical old midpoints,
while the displayed nonzero commutator already shows the corresponding
physical midpoints are distinct.

This is an invariant obstruction to direct old-family representation of the
entire endpoint/midpoint path on every interval `(0,t0)`. It does not rely on
orthogonal entropy invariance.

No critical gap found for Claim 2.

## Claim 3: exact-event law and uniform asymptotic sign

The proof derives the event table from the full inclusion-exclusion DPP law
through the generating polynomial

```text
det(I-K+ZK)=sum_S p_K(S) product_(i in S) y_i.
```

The rank-two expansion around the diagonal part accounts for all `16` events.
This avoids the inclusion-minor pitfall. The table includes the two opening
Pluecker-zero pair events `12` and `34`, the empty and full events, all
singletons, all triples, and all four active pair events.

For fixed `x` in a compact interval `J=[ell,h] subset (0,1)`, the event
valuations in the proof give uniform positive lower bounds of the form
`c_J t^v` for the relevant Taylor segments. The empty event is handled exactly,
which is necessary because its relative displacement is not uniformly small
near `x=1`; the compact assumption `h<1` keeps `log(1-x^2)` bounded. The
singleton, active-pair, opened-pair, triple, and full-event estimates have
remainders bounded by `O_J(t^3 log(1/t))` or smaller.

The `t^2 log(1/t)` terms cancel between the empty event and the four
singletons. The remaining finite coefficient is

```text
-G(x^2),  where G(v)=v+(1-v)log(1-v).
```

Since `G(0)=0` and `G'(v)=-log(1-v)>0` on `0<v<1`, the coefficient is
strictly negative for every fixed `x in (0,1)`. On each compact `J`, it is
bounded away from zero by `G(ell^2)`, so the uniform remainder gives a common
small-`t` interval on which `Delta(t,x)<0` for all `x in J`.

The proof explicitly does not cover `x=x(t)` tending to `0` or `1`, faster
physical rotations, all finite `t`, or arbitrary moving frames. These are
outside the frozen v2 claim and are not gaps.

No critical gap found for Claim 3.

## Bounded computational cross-check

The provided audit script blob was hashed and its archived JSON outputs are
hash-bound above. Its archived `source_sha256` equals the script blob SHA256.
Attempting to run the script locally through the bundled Python runtime failed
because `sympy` was unavailable in that runtime; no mathematical conclusion is
drawn from that failed run.

As a separate bounded check, I used a standard-library-only rational 4x4
implementation for the submitted family. It reconstructed the kernels, checked
the arithmetic midpoint, computed all principal minors of `K` and `I-K`,
computed the full inclusion-exclusion event law, and evaluated high-precision
entropy differences at the same seven rational chords appearing in the archived
smoke/certified outputs. This used one local process, no GPU, and no search.

The check matched the archived minimum event masses and negative delta values
for:

```text
(t,x)=(1/8,1/2),
(1/16,1/4), (1/64,1/4),
(1/16,1/2), (1/64,1/2),
(1/16,3/4), (1/64,3/4).
```

This is only a cross-check of formulas and certificates at finitely many
rational chords. The `CORRECT` verdict rests on the symbolic proof of the three
frozen claims, not on finite sampling.

## Verdict

The anonymous proof proves all three frozen v2 claims against the stated
hazards: exact physical-coordinate feasibility, actual arithmetic midpoint,
non-reducibility to the old fixed-data midpoint hierarchy by a commutator
invariant, complete exact-event accounting, opening zero events, cancellation
of the logarithmic leading terms, and a uniform compact-in-`x` remainder for
the first nonzero negative asymptotic term.
