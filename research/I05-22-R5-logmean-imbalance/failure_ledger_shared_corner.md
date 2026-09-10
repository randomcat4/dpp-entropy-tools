# Shared-corner continuation: failure and correction ledger

Status of mathematical files: author proof / same-author checking only; independent delta review is requested separately.

## Preserved failed approaches

1. Independent scalar bounds on `ell,k,lambda,J` do not control the full determinant. The exact relaxed tuple in `coupled_gram_fixed_shape.md` satisfies the two Gram ellipses and has positive `Y`, yet has a negative exact relaxed determinant. It is not DPP-realizable.
2. Adding the two one-axis placement/secant constraints still permits nonrealizable relaxed negatives in a bounded diagnostic. This did not produce an actual DPP point and is not an entropy counterexample.
3. The missing ingredient was the simultaneous shared-four-corner cell mode. Treating horizontal and vertical edges independently loses the exact term `-J Delta^2/(32AB)`.
4. No universal proof of the refined actual condition `KA+KB>=J/(32AB)` is supplied. No general half-leaf or unequal-leaf theorem is claimed.

## Independent reconstruction performed in this unit

Before using the prior author delta as a premise, the following were rebuilt independently from the frozen PR70/PR81 formulas:

- the half-leaf `U <-> T` corner transform;
- the exact `L,C,F,R` corner quadratic;
- the prior rational relaxed determinant, all four printed `Y` leading minors, and the three printed q-derivative fractions;
- the direct original eight-event curvature at three rational physical directions;
- the inverse-root concavity identity used in the new one-edge lemma.

The public checker is still same-author computational evidence and does not replace independent adjudication.

## Publication error and exact restoration

At commit `d50577e1ba760aa5d7607550843096a047f3ffb3`, the existing detailed `proof.md` was mistakenly replaced by a short overview while attempting to add an entry point. This was a publication/editing error, not a mathematical change.

The next repair commit `7231d3d995aadffcdcbe381b90c6016dc8bf1c05` restored the file by reusing its exact prior blob

```text
ad51fb200fb44e888025507f57189d55ec7dbd1a
```

in a new tree based on the then-current branch. No force update was used, and all newly added theorem/checker files were preserved. The mistaken commit remains visible in history; no failure was erased.

## Resource ledger

- No PR60 Lambda-zero 1731-term certificate was rerun.
- No issue73 point, filament, subdivision, or 2700-second budget was started or duplicated.
- No long multivariate elimination was run.
- The exact checker had one recorded successful execution; no precision escalation, repair rerun, or silent retry was used.
- No formal proof assistant or independent arithmetic reviewer is claimed.

Final scope: the fixed shape in `shared_corner_cell_theorem.md` is **PROVED by the author, PENDING_REVIEW** on its complete legal q interval. General claims remain **INCOMPLETE**.