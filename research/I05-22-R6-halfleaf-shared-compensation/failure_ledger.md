# Failure, execution, and scope ledger

1. The PR81 condition `K_A+K_B>J/(32AB)` is not universal. The failure is realized by the strict physical family `A=a`, `B=epsilon`, `q=rho epsilon`; it is not a relaxation artifact.
2. The reason is a scale mismatch: `J/(32AB)` grows logarithmically while each independently parallelized edge pair has a finite limit. This disproves only the sufficient method.
3. The exact rational witness has a strictly positive complete-event `-H''` matrix. It is therefore not a Shannon entropy counterexample.
4. The repair retains the common leaf-diagonal variable across opposite edges. Its coefficient `C_A` is different from the old endpoint-parallel coefficient and succeeds throughout a punctured boundary wedge.
5. The theorem is local to a boundary scaling, though uniform on compact sets of the fixed coupling and scale ratio. It does not close all half-leaf arrows or any unequal-leaf domain.
6. No PR60 Lambda-zero certificate, PR81 fixed-shape proof, or issue73 filament computation was rerun.
7. The first checker execution completed its mathematical assertions but failed while printing very large exact integers because of Python's integer-to-string digit guard. The final execution changed only output formatting, retained the same 24-term rational arithmetic, and passed once in about 11.22 seconds. No precision escalation, search, subdivision, or silent mathematical retry occurred.
8. The checker and output are same-author evidence. Independent analytic review, independent arithmetic reconstruction, novelty, and formal verification are all pending/not assessed.
