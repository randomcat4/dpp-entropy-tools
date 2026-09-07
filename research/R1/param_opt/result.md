# R1 parameterization and optimization result

STATUS: INCOMPLETE

No positive-Hessian candidate was found. Two completed finite CPU batches evaluated 13,202 objective calls across n=3,...,10, with zero event/Hessian diagnostic failures and zero values exceeding the predetermined candidate threshold 1e-6. These counts include repeated or nearby finite-difference objective calls; they are not counts of distinct kernels or a continuous-domain certificate.

The search kernel is a full dense symmetric spectral sigmoid, described in `derivation.md`. At every evaluated kernel the whole Frobenius-orthonormal real symmetric direction space is represented in the Hessian; its numerical largest eigenvalue and unit eigenvector are computed. There is one best-direction result per objective call, not merely one randomly chosen direction.

## Completed finite batches

| n | Random/ascent calls | Random/ascent best H'' | L-BFGS-B calls | L-BFGS-B best H'' |
|---|---:|---:|---:|---:|
| 3 | 620 | -4.057793427e-7 | 245 | -6.245093782e-15 |
| 4 | 620 | -2.517968258e-5 | 979 | -1.052303340e-10 |
| 5 | 620 | -8.789522570e-6 | 1200 | -4.283334020e-14 |
| 6 | 620 | -6.867985439e-5 | 1018 | -2.870605514e-14 |
| 7 | 620 | -4.702426312e-5 | 1200 | -3.144561289e-9 |
| 8 | 620 | -4.625247457e-5 | 1200 | -2.707334561e-6 |
| 9 | 620 | -9.220362334e-6 | 1200 | -4.869989104e-5 |
| 10 | 620 | -2.416541025e-5 | 1200 | -3.055285627e-4 |

Batch 01: seed 202609081, 160 restarts, 4,960 calls, elapsed 32.6922 seconds, 900-second wall-time ceiling, 960/970-second CPU limits, 10 GiB address-space limit, one BLAS/OpenMP thread. The completion record reports exit code 0.

Batch 02: seed 202609082, 16 restarts, 8,242 calls, elapsed 61.9643 seconds, at most 600 actual objective calls per restart, at most 50 optimizer iterations, 300-second wall-time ceiling, 330/340-second CPU limits, 10 GiB address-space limit, one BLAS/OpenMP thread. The foreground process and program both returned exit code 0. Eleven restarts reached the explicit call budget; five ended on optimizer convergence.

Both batches are complete. No automatic continuation or expansion is configured. Batch 01 saves completed-restart checkpoints and refuses completed-output repeats. Batch 02 saves completed-restart checkpoints and refuses a second launch when its process record exists; it does not implement automatic mid-optimizer resumption. Interrupted partial-restart logs would need explicit reconciliation before a restart. This limitation does not affect these completed runs.

## Best finite object and interpretation

The full best K, normalized V, raw spectral coordinates, eigenvalues, and chord step are saved in `batch02/best.json`. Its numerically estimated H'' is -6.245093781582534e-15. The kernel is close to a 2+1 block decomposition with cross-block entries about 1e-8, and its spectrum is approximately (0.00656599, 0.33660941, 0.99329365). At t=0.00046428538429289177 the event-entropy chord calculation gives Delta=-3.960165528837933e-12. This object is an optimization endpoint near a flat Hessian direction, not a counterexample or a strictly certified inequality.

## Implementation consistency checks

The self-test uses n=1,...,6 and compares the signed determinant exact-event formula with independent inclusion-probability Mobius inversion. The largest absolute probability discrepancy was 1.4572e-16. It checks the analytic Hessian against centered entropy differences at steps 1e-3, 3e-4, 1e-4, checks sum p''=0, and checks diagonal Bernoulli second derivatives. All checks passed; complete values are in `batch01/selftest.json`. These are author-side checks, not independent certification.

Environment: Python 3.12.3, NumPy 2.1.2, SciPy 1.14.1. No dependency changes or GPU were used.

## Files and remaining gap

`search.py` contains exact-event entropy, analytic full Hessian, spectral parameterization, self-tests, and the random/ascent batch. `optimize.py` performs bounded L-BFGS-B optimization. `launch.py` starts the first batch with resource limits and a duplicate-process check. The compact `summary.json` files retain denominators, termination reasons, and the best full object. Full per-evaluation logs are retained only in the private task working directory and are omitted from this public package.

The unresolved objective remains either a robust real positive-Hessian kernel that can be frozen and rationally certified, or a proof excluding an explicitly defined continuous family. This finite search establishes neither. The source author does not certify a candidate, and no candidate was passed onward for certification.
