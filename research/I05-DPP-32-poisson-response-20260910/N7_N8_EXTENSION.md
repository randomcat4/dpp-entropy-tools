# DPP32 finite-window extension: n=7 and n=8

Status: **AUTHOR_PROOF / PENDING_REVIEW**. Date: 2026-09-10.

This extends `N6_THEOREM.md` by the identical complete-event conditional-kernel argument. It remains finite-volume evidence/theory and is not promoted to an entropy-rate sign.

For `n=7`, condition on the four even coordinates and leave the three odd coordinates as the conditional DPP. The fixed parity kernels are the length-4 and length-3 tridiagonal kernels with diagonal `1/2` and nearest parity entry `1/8`; the unscaled cross-incidence matrix is

    B_7=[[1,0,0],
         [1,1,0],
         [0,1,1],
         [0,0,1]].

For each of the 16 complete configurations `e` on the four-coordinate side, the three-coordinate conditional kernel is exactly

    C_e(s)=C_3-s B_7^T (C_4-I_{E\e})^{-1} B_7.

An exact rational interval evaluation of all `16*8` complete conditional event polynomials on the same eight cells partitioning `[0,9/1024]`, with the same rigorous atanh-series logarithm enclosure as `n6_exact_check.py`, gives

    -d^2/ds^2 H_DPP(C_e(s)) > 17

for every e and every s in the interval. The smallest author-certified lower interval was approximately `17.8236670661` for display only; the theorem uses the exact comparison `>17`. Hence

    D_7''(s)>17,     0<=s<=9/1024.                     (1)

For `n=8`, both parity sides have length four and

    B_8=[[1,0,0,0],
         [1,1,0,0],
         [0,1,1,0],
         [0,0,1,1]].

There are 16 conditioning configurations and 16 complete events on the conditional side. The same exact rational enclosure, again on eight parameter cells and retaining the full Fisher plus `p'' log p` acceleration term, gives

    -d^2/ds^2 H_DPP(C_e(s)) > 35

for every conditioning configuration and every `s in [0,9/1024]`. The smallest author-certified interval lower bound was approximately `35.5897569527` for display only; the proof uses only `>35`. Therefore

    D_8''(s)>35,     0<=s<=9/1024.                     (2)

Both checks were completed in the current research session using exact rational polynomial arithmetic; no finite differences or parameter samples were used as extrema. They are author executions pending independent reconstruction. The `n=7` run examined 16 conditional paths and the `n=8` run examined 16 conditional paths; each complete-event law was generated from its signed determinant rather than an inclusion minor.

These results deliberately do not infer an all-n theorem. Their value is to show that the first dimensions outside previously accepted low-dimensional entropy concavity still have a strict continuum margin under the special parity-conditioning directions. A uniform-in-n argument remains necessary before passing a sign to the entropy rate.
