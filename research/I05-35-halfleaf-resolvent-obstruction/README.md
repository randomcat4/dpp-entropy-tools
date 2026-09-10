# I05-35: exact half-leaf resolvent obstruction and integrated-curvature continuation

Status is deliberately split.

- **DISPROVED:** the old-chat universal pointwise assertion `Phi_r''>=0` for every strict half-leaf, every `r>0`, and every physical six-direction.
- **PROVED BY AUTHOR / PENDING EXTERNAL REVIEW:** the exact lossless two-side-plus-marginal decomposition; separate positivity of `G1''` and `G0''` for every strict equal-strength half-leaf; and a punctured single-edge-face theorem for arbitrary fixed strength on the other edge.
- **INCOMPLETE:** integrated one-sided positivity for every unequal strength pair, the compact unequal-strength middle, a boundary-uniform unequal-leaf radius, general missing-edge concavity, and general real three-point Shannon concavity.

This successor starts from `main@b3ada9f6bb23e3efd2e1a4d2a2977d50b61fb4d7`. It does not modify PR81, PR104, their review records, or any accepted file. Novelty is **NOT_ASSESSED**. The same GitHub account's reconstruction is not represented as an independent reviewer verdict.

## Exact pointwise-resolvent obstruction

For the strict half-leaf

```text
A=1/4, B=16/25, q=109/1000, qbar=1/1000,
K=[[1/2,0,1/4],[0,1/2,2/5],[1/4,2/5,277/500]],
```

at

```text
r=1/50000,
D=(d11,d22,d33,d12,d13,d23)=(-18,-72,40,146,108,5),
```

the true affine line `K+tD` satisfies

```text
Phi_r''(K;D)
=-47488558049748267993080620088778228551027375300000000000
 /2044542058422113103788725284171055940635901533282467
<0,

Phi_r=sum_ij P_ij^2/(p_ij1+r P_ij).
```

Both the original PR124 checker and the shorter independent-session checker reconstruct all eight complete events from principal-minor Möbius inversion and obtain this exact fraction. This is a method/certificate counterexample, not an entropy counterexample and not a counterexample to the integrated quantity `G1''`.

## Lossless repair

With `q_ij=p_ij1/P_ij`,

```text
G1=sum_ij P_ij q_ij log q_ij,
G0=sum_ij P_ij (1-q_ij) log(1-q_ij),
H=H(P)-G1-G0.
```

At the half-leaf center `P_ij=1/4`, every physical direction obeys

```text
-H''=4(d11^2+d22^2)+G1''+G0''.
```

All eight occupied/vacant events, the complete Fisher term, every acceleration, and the leaf marginal are retained. On the displayed pointwise-resolvent witness, the direct eight-event checker proves the full Shannon curvature has the strict concave sign.

## Integrated results after the first checkpoint

`equal_strength_halfleaf_theorem.md` proves that every strict half-leaf with `A=B` has separately positive-definite `G1''` and `G0''`, hence strictly negative complete Shannon Hessian in all six directions through the whole legal `q` interval. The proof uses a leaf-swap decomposition and an exact three-node chain coefficient; it does not restore pointwise positivity of `Phi_r`.

`independent_audit_and_small_edge_theorem.md` records a separate algebraic reconstruction of that theorem and proves a new unequal-strength boundary result. After normalizing the occupied rare corner, for every fixed `a=A/q>0` there is `epsilon(a)>0` such that `G1''>0` whenever `0<B/q<epsilon(a)`. Complementation gives the vacant side, so every compact positive part of the physical face `B=0` has a punctured neighborhood on which

```text
G1''>0, G0''>0, and -H''>0
```

in all six directions. Leaf exchange gives the analogous face near `A=0`.

The same file proves a sharp method obstruction: retaining only the four endpoint residual matrices after completing the edge squares is insufficient in a highly unequal regime. For normalized strong edge `a` and weak edge `b->0`, the residual-only coefficient misses the cell term whenever

```text
(a+2)log(1+a)>6a;
```

in particular this happens at `a=1000`. The complete one-sided Hessian is nevertheless positive there by the new theorem. Thus the completed leaf-diagonal squares and their `2Jde` coupling must remain in the unequal-strength proof.

## Reproduction

From this directory run

```text
python code/verify_resolvent_obstruction.py
python code/verify_independent_event_fraction.py
python code/verify_small_edge_algebra.py
```

The first checker is the original complete PR124 event/logarithm certificate. The second is a new standard-library-only eight-event reconstruction that does not import the first. The third is a new SymPy exact-algebra check for the equal-strength blocks, small-edge Schur asymptotics, and residual-only obstruction.

The two new scripts each had one successful local execution under Python 3.13.5; the SymPy script used 1.14.0. Their retained wall/RSS records are in `output/`. No existing PR81/104/124 computation was rerun, no scan or interval subdivision was opened, and no long-computation contract was used.

## Files

- `proof.md`: exact pointwise-resolvent obstruction, lossless decomposition, and original complete checker contract.
- `equal_strength_halfleaf_theorem.md`: full equal-strength integrated theorem.
- `independent_audit_and_small_edge_theorem.md`: separate audit, exact general one-sided core, punctured small-edge theorem, and residual-only method obstruction.
- `code/verify_resolvent_obstruction.py`, `output/verify_resolvent_obstruction.txt`: original exact complete-event/log certificate.
- `code/verify_independent_event_fraction.py`, `output/verify_independent_event_fraction.txt`: minimal independent-session Möbius reconstruction.
- `code/verify_small_edge_algebra.py`, `output/verify_small_edge_algebra.txt`: exact continuation algebra and execution record.

The next load-bearing target is the sign of the exact two-by-two unequal-strength Schur core, not pointwise resolvent positivity and not the residual-only chain.
