# D10-M4 run log

AUTHOR STATUS: N2_PROVED_N3_BLOCKER_IDENTIFIED, pending non-author verification.

## Scope

- Work unit: D10-M4 low-dimensional fixed-eigenvector PSD spectral rates.
- Writable directory:
  `research/R3/deepening_10h/dense_hessian/commuting_spectral/low_dim_exact/`.
- No subagents.
- No server or GPU.
- No dependency installation.
- No modification of shared README files.

## Work performed

1. Derived the exact \(n=2\) atom formulas from the DPP exact-event identities:

   \[
   p_{12}=\det K,\quad p_i=K_{ii}-\det K,\quad
   p_\emptyset=\det(I-K).
   \]

2. Proved \(n=2\) strict negative curvature for every nonzero PSD spectral-rate
   direction \(v_i\ge0\) by splitting entropy into:

   - count entropy \(H(|Y|)\), strictly concave along nonzero nonnegative
     spectral-rate directions;
   - singleton split entropy \(\Phi(p_1,p_2)\), concave by perspective entropy
     plus \(p_1''=p_2''\le0\).

3. Identified the \(n=3\) minimal blocker: singleton atom second derivatives no
   longer have a fixed sign under PSD spectral rates.

4. Ran a finite scout before final proof polishing:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research/R3/deepening_10h/dense_hessian/commuting_spectral/low_dim_exact/n2_probe.py
```

Exit code: `0`; trials `200000`; positive `H2>1e-12` count `0`.  This is
scout evidence only and is not used in the proof.

## Pending sanity

5. Ran exact-event sanity:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research/R3/deepening_10h/dense_hessian/commuting_spectral/low_dim_exact/n2_exact_check.py
```

Exit code: `0`; status `PASS`.

Outputs:

- `n2_exact_check.json`
- 4 rational n=2 exact-event cases, all atom sums exactly `1`, all
  \(\sum p'=0\), all \(\sum p''=0\), all float \(H''<0\)
- n=3 rational Householder blocker:
  \(p_{\{1\}}''=2339/2450>0\)
