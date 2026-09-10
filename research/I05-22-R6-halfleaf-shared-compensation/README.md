# I05-22 R6: actual failure of the parallel-edge criterion and shared-diagonal boundary compensation

Status: **DISPROVED** for universal validity of the PR81 strict parallel-edge criterion, by an actual strict half-leaf DPP family rather than a relaxed four-scalar point. **PROVED (author proof; PENDING_REVIEW)** for the common-leaf-diagonal sufficient criterion and the punctured boundary-wedge theorem in `proof.md`. The exact rational witness is author-certified from all eight complete events; its execution is not an independent computation. General half-leaf concavity, unequal leaf diagonals, general missing-edge concavity, and general real three-point concavity remain **INCOMPLETE**. Novelty is **NOT_ASSESSED**.

This successor starts from reviewed `main` commit `8f4acd31d0ce4d37defafbfcff22fa2b21356f72`. It uses PR81 only in its accepted scope: the exact shared-corner quadratic, the actual optimal one-edge coefficient, and the strict sufficient criterion. It does not alter or rerun the merged PR81 proof or the PR60 Lambda-zero certificate. Issue73 is still a separate requested/not-running calculation and is not consumed or expanded here.

## Main outcome

For a strict half-leaf arrow, write the four actual corner parameters as

```text
t11=q, t10=q+B, t01=q+A, t00=q+A+B,
```

and let `J` be the actual paired rectangle integral. PR81 combines the four optimal edge residuals into `K_A+K_B`; its sufficient test is

```text
K_A+K_B > J/(32AB).
```

That test is not universal. For every fixed `a in (0,1)` and fixed ratio `rho>0`, along the actual legal family

```text
A=a, B=epsilon, q=rho*epsilon, epsilon -> 0+,
```

the left side has a finite limit while the right side grows like `log(1/epsilon)/(32a)`.

The lost compensation is the fact that the same leaf-diagonal direction `d` occurs on both horizontal edges. Retaining it gives a new actual coefficient `C_A`. On the same family,

```text
C_A - J/(32AB)
  -> kappa_0(a) + D(rho)/(32a) > 0,
```

where

```text
kappa_0(a)=1/[32a(1-a)(1-3a(1-a))],
D(rho)=integral_rho^(rho+1) log u du
       -[log rho+log(rho+1)]/2 >0.
```

Thus the old parallel criterion eventually fails while the complete eight-event Shannon Hessian remains strictly negative in every nonzero real symmetric physical direction. The result is locally uniform for `a` and `rho` in compact subsets of `(0,1)` and `(0,infinity)`.

## Exact actual witness

```text
A=1/9, B=q=1/10000, qbar=39991/45000,
K=[[1/2,0,1/6],
   [0,1/2,1/200],
   [1/6,1/200,10027/180000]].
```

The standard-library checker reconstructs every inclusion minor and all eight complete-event jets by Möbius inversion. It proves exact equality with the shared-corner six-coordinate quadratic, encloses all logarithms by a fixed 24-term rational atanh series, and obtains

```text
K_A+K_B-J/(32AB) < -0.8407635409,
C_A-J/(32AB)     >  0.3743163926.
```

All six leading Sylvester minors of the complete-event `-H''` matrix have strict positive rational intervals. Therefore this is a failure of the sufficient method only, not an entropy counterexample.

## Files

- `proof.md`: self-contained asymptotic obstruction, common-diagonal theorem, compact-uniform boundary family, and scope ledger.
- `code/verify_halfleaf_boundary.py`: exact rational input, Möbius jets, exact event/corner comparison, rational log intervals, and Sylvester test.
- `output/verify_halfleaf_boundary.txt`: literal successful output from one author execution.
- `failure_ledger.md`: method failures, execution boundary, and unclosed quantifiers.

Execution used one process under Python 3.13.5, standard library only, with one successful run in about 11.22 seconds and peak RSS about 95,780 KiB. There was an earlier output-format attempt that exceeded Python's integer-to-string digit guard after completing the mathematics; the final run only changed reporting, not arithmetic or precision. No long computation, scan, interval subdivision, formal proof, or independent review is claimed.
