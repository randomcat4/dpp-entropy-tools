# D10-U4 sparse puncture graph fresh non-author audit

STATUS: CORRECT

Scope of this status: the frozen U4 claims in `sparse_puncture_graph/` are
correct as a proof-candidate package for

- disconnected support giving an exact full-Hessian flat direction;
- connected support with diameter at most two giving full Sym(n) Hessian
  negative definiteness at `K_epsilon=diag(x)+epsilon A` for all sufficiently
  small nonzero `epsilon`;
- the resulting `n=3` connected iff disconnected classification;
- the sixth-jet bridge, including `F5=0` and the displayed two sixth-degree
  classes.

This does not certify the open general connected-support question.  The P4
degree-eight endpoint computation remains SCOUT only, exactly as the author
labels it.

## Files inspected

- `frozen_problem.md`: definitions, exact-event semantics, candidate outcomes,
  and explicit incomplete/P4-scout scope at lines 5-31.
- `proof_candidate.md`: exact likelihood and character expansion at lines 12-40;
  fourth/fifth/sixth jet at lines 47-73; remainder and block orders at lines
  75-106; three-scale congruence and strict/uniform quantifiers at lines
  108-142; `n=3` classification at lines 144-164; disconnected obstruction at
  lines 166-186; P4 scope guard at lines 188-201.
- `verdict.md`: author status and scope at lines 3-5, theorem summary at lines
  7-18, `n=3`/general connected distinction at lines 20-31, F5/F6 mechanism at
  lines 33-39, and P4 SCOUT warning at lines 41-45.
- `run_log.md`: author command/exit and denominator at lines 12-30, targeted
  coefficients at lines 32-40, and author hashes at lines 48-52.
- `sanity.py` and `sanity_results.json`: read only; not imported or rerun.

## Fresh verification commands

Final independent command:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research\R3\deepening_10h\dense_hessian\sparse_puncture_graph\verifications\fresh_u4_audit.py
```

Exit code: 0.

Fresh verifier output:

- script: `verifications/fresh_u4_audit.py`
- JSON: `verifications/fresh_u4_audit.json`
- fresh script SHA256:
  `b0b409e064ec19177787d6b4a2d321720a8b364a31b58e46f33a80290855ca8e`
- no random draws, no failed checks.

Author hash cross-check from `run_log.md`:

- `sanity.py` actual SHA256 =
  `aad8c8f061ebdfa8793515aa993ed0cd4b61c8fccf34b384ff706d1d61e4a07c`
- `sanity_results.json` actual SHA256 =
  `161d4cfe0b67102effb589c64a7dddcef06355cbc783df10d584185b7aef0acc`
- both match the hashes recorded in `run_log.md` lines 48-52.

One draft verifier run of the same fresh script returned exit code 1 before the
final PASS because my verifier had an internal series-power error; the failing
n=2 coefficients exposed the mistake immediately.  I corrected only the fresh
verifier.  No author file was modified.

## Exact-event and entropy-series audit

The likelihood formula is faithful to exact-event semantics.  Starting from
Möbius atoms

```text
p_S(K)=sum_{T superset S} (-1)^(|T|-|S|) det K_T,
```

and equivalently from the signed shifted determinant in
`proof_candidate.md` lines 12-27, at a strict diagonal `X=diag(x)` and
zero-diagonal `Z`,

```text
p_S(X+Z)/a_S = 1 + sum_{|T|>=2} det(Z_T) zeta_T(S).
```

Singleton terms vanish because `Z_ii=0`.  The exact atom mass and singleton
marginals remain fixed, so the linear `log a_S` contribution cancels; since
`log a_S` is affine in the singleton indicators, this justifies the entropy
series in lines 35-40.

I independently checked this by constructing Möbius atoms directly, not by
calling the author script:

- n=2, 4 atom polynomials;
- n=3, 8 atom polynomials;
- n=4, 16 atom polynomials.

Across these 28 general atom polynomials, all degree-5 entropy coefficients
vanished and the complete degree-4/6 polynomial matched the formula in
`proof_candidate.md` lines 69-73.

## F5 and F6 coefficient audit

The claimed `F5=0` is correct.  `R2` has size-2 characters and `R3` has size-3
characters, so `E[R2 R3]=0` for every strict heterogeneous diagonal; no
complement-symmetry assumption is used.

The sixth-degree list is complete:

- `-E[R2 R4]=0` by subset-character orthogonality.
- `-(1/2)E[R3^2]` contributes
  `-2 w_i w_j w_k z_ij^2 z_ik^2 z_jk^2` per triangle.
- `(1/6)E[R2^3]` has exactly two nonzero incidence patterns: three copies of
  one edge, giving `-(1/6)t_i t_j z_ij^6`, and three distinct edges forming a
  triangle, giving the additional `-1` triangle coefficient.

Hence the total triangle coefficient is `-3 w_i w_j w_k`, and the pure-edge
sixth term is exactly `-(1/6)t_i t_j z_ij^6`.  The latter can have either sign,
as the proof notes at lines 75-79, but it is higher order than the supported
edge quartic curvature.

## Missing-edge, mixed-block, and scaling audit

For a missing pair `ij`, differentiating the triangle term with the two present
edges `ik` and `jk` gives

```text
F_{z_ij,z_ij} =
  -6 w_i w_j sum_{k: ik,jk in E} w_k A_ik^2 A_jk^2 epsilon^4
  + O(|epsilon|^5).
```

This matches the `B_M` definition in `proof_candidate.md` lines 87-90.  If
`G` is connected with diameter at most two, every missing pair has at least one
common neighbor, so each missing-edge leading coefficient is strictly negative.

The mixed-block orders in lines 94-98 are also consistent with the expansion:

- `F_xx=-C+O(epsilon^4)` because the diagonal entropy Hessian is already
  `-diag(w_i)` and off-diagonal terms begin at degree four.
- `F_xE=O(epsilon^3)` and `F_EE=-epsilon^2 B_E+O(epsilon^4)` come from the
  quartic supported-edge terms.
- Displayed fourth/sixth-degree terms are even in every missing coordinate at
  `z_M=0`, and `F5=0`; therefore a single missing derivative first appears only
  in the analytic degree-seven remainder, giving `xM=O(epsilon^6)` and
  `EM=O(epsilon^5)`.
- Two different missing-edge derivatives vanish in the displayed sixth jet;
  the diagonal missing derivative is the common-neighbor term above.

With

```text
S_epsilon = diag(I_x, |epsilon|^-1 I_E, |epsilon|^-2 I_M),
```

the scaled Hessian converges in operator norm to
`-diag(C,B_E,B_M)` as stated in lines 111-124.  The scaling is invertible for
`epsilon != 0`, so inertia is preserved.  The potentially dangerous supported
edge Schur correction is order `epsilon^8` against a missing block of order
`epsilon^4`, matching lines 127-130.

The strict-kernel condition follows from
`|epsilon| ||A||_op < min_i{x_i,1-x_i}` as in lines 132-134.  The compact
uniform statement at lines 137-142 is also sound: `w_i>=4` gives supported
coefficients at least `96 eta^2`, and a common-neighbor witness gives missing
coefficients at least `384 eta^4` when `||A||_F=1` and
`min_{e in E}|A_e|>=eta`.

## Targeted finite checks

The fresh verifier reproduced the author’s deterministic rational denominator:

- general sixth jets: 28 atoms;
- n=3 single-edge disconnected obstruction: 8 atoms;
- n=4 P4 endpoint scout: 16 atoms;
- total: 52 atom polynomials.

Targeted values:

- n=3 path with `x=(1/5,2/5,4/5)`, `A01=2/5`, `A12=-3/7`:
  supported `epsilon^2` curvature coefficients are `-25` and `-5625/196`;
  missing-edge `epsilon^4` coefficient is `-5625/196`.
- n=3 single-edge-plus-isolated: all exact atom first derivatives in a
  cross-component edge variable vanish, and all block-event marginals are
  constant in that variable.  This supports the exact entropy curvature zero
  proof, not merely a leading-order statement.
- n=4 path endpoint missing-edge probe:
  `x=(1/5,1/3,3/5,3/4)`, weights `(1/3,-2/5,3/7)`, missing edge `03`, curvature
  has no `epsilon^0` through `epsilon^5` term and has coefficient
  `-(600/49)epsilon^6`.  This remains SCOUT only.

## Disconnected obstruction audit

The argument in `proof_candidate.md` lines 166-186 is correct.  If the kernel
is block diagonal over disconnected support components, the DPP law factorizes
over blocks.  For a symmetric direction crossing two components, all exact atom
first derivatives vanish.  The block marginal laws are unchanged by the
cross-component perturbation, so the second-derivative atom sums vanish after
conditioning on any one block event.  Since `log p_S` is a sum of block logs,
both the Fisher part and the acceleration part of `H''` vanish.  The chosen
cross-component direction is nonzero and has a small strict feasible interval,
so the full Hessian cannot be negative definite.

This gives the claimed necessity of connected support in every dimension and
the disconnected half of the `n=3` classification.

## Verdict

No critical gap found.

The package correctly proves the diameter-two sufficient theorem and the `n=3`
connected iff disconnected classification under the frozen strict diagonal
punctured-ray setting.  It also correctly preserves the boundary around the
open problem: connected support with diameter at least three is still
INCOMPLETE, and the P4 calculation is only an exact scout for one entry, not a
full-Hessian certificate or a graph classification.
