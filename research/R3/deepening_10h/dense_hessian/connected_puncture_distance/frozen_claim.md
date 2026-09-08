# D10-U5 connected puncture distance

AUTHOR STATUS: PROOF_CANDIDATE_FOR_N4; GENERAL_CONNECTED_INCOMPLETE.

This unit continues U4 without modifying U4.

## Setting

Fix `n>=2`, a strict diagonal kernel

```text
X = diag(x_1,...,x_n),        0 < x_i < 1,
```

and a real symmetric zero-diagonal matrix `A`.  The support graph `G` has edge
`ij` iff `A_ij != 0`.  Along the punctured ray

```text
K_epsilon = X + epsilon A
```

we ask whether the full Shannon entropy Hessian, in all real symmetric
observation-coordinate directions, is negative definite for every sufficiently
small nonzero `epsilon`.

Exact-event probabilities are always DPP atom probabilities obtained from
inclusion determinants by Möbius inversion.

## Frozen candidate added here

For `n=4`, connected support is necessary and sufficient for the punctured-ray
full-Hessian negativity property.

- Necessity is the disconnected flat-direction obstruction from U4.
- If `G` has diameter at most two, sufficiency is the U4 theorem.
- The only new connected case is a four-vertex path `P4`, up to relabelling.
  For every strict diagonal `X` and nonzero path weights
  `A_12=a`, `A_23=b`, `A_34=c`, the Hessian at
  `X+epsilon A` is negative definite on all of `Sym(4)` for all sufficiently
  small nonzero `epsilon`.

This is an author proof candidate and is not self-certified.

## General-distance candidate, not yet a theorem

For a pair `ij` at graph distance `d=d_G(i,j)`, the diagonal coordinate
curvature appears to follow

```text
H_{ij,ij}(X+epsilon A)
  = -6 epsilon^(2d)
      sum_{P in SP_d(i,j)}
        (prod_{v in P} w_v) (prod_{e in P} A_e^2)
    + O(epsilon^(2d+1)),

w_i = 1/(x_i(1-x_i)).
```

Here `SP_d(i,j)` is the set of shortest `i`-to-`j` paths in `G`; if `ij` is a
support edge, `d=1` and the formula gives the U2/U4 supported-edge term.

This formula is strongly supported by exact rational coefficient extraction,
including all connected labelled `n=4` graphs and selected `n=5` graphs with
diameter up to four, but the general diagram proof and the same-distance
off-diagonal block definiteness remain open.

## Scope exclusions

- No claim that every connected support graph works in arbitrary `n`.
- No claim that finite `n<=5` scouts prove the general theorem.
- No boundary kernels or zero edge weights are included.
- No novelty or final correctness certification is made by this author unit.
