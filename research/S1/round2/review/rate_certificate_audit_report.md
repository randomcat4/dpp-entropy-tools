# S1 round-2 B1 rate certificate audit

Status: **CORRECT for the frozen fixed `S1-R2-B1` negative entropy-rate pair-gap certificate.**

The audited certificate is the rate child artifact frozen at commit `73fce2a45df13831f28415a207179a67715a9550`, under `research/S1/round2/rate/`. I did not modify author files. This report only covers the fixed B1 certificate; it does not expand to new windows, new directions, a family theorem, phase search, or the full Lyons--Steif conjecture.

The certified rate gap is

```text
-3.0348902924818035e-05
<= (h(f_-)+h(f_+))/2 - h(f_0)
<= -7.3460456800473595e-06.
```

The upper endpoint is strictly negative, so this fixed B1 pair is excluded as a positive entropy-rate counterexample. The three symbols `t=-1/8,0,+1/8` are evaluated separately; no endpoint equality, reflection, or conjugation shortcut is used.

## Source and artifact identity

The frozen file hashes match the hashes embedded in the certificate artifacts:

- Candidate: `d92793f7196a4eefaece91b3f37e65dec6744f61711363030cd81259aa1ccf09`.
- Boundary source `r2_variational_boundary.py`: `7174665d976b4e63490696a2dc8b23160c0ad3ab12668ea1b05c02fbd1f9907c`.
- Rate source `r2_rate_certificate.py`: `244dee715d56ea9cabe8873ca140112048a1eda6d0fe07e24e30c0f9123be201`.
- Boundary artifact `r2_boundary_M64.json`: `921b8039baf5464b4c14f07b75cf52ff25a0195cc285a8ff25c7fa20ce26bc47`.
- Rate artifact `r2_rate_n4.json`: `3fe57b224676ea48cd5eaaf772603da2626e921adfc0d13bcc117e30761567d2`.

The review-side replay artifacts have different full-file hashes because their metadata records fresh local PIDs and timings, but their mathematical case fields agree with the frozen artifacts. The replay artifacts were executed and first hashed as CRLF worktree files, then archived by Git as LF blobs; this is only line-ending normalization. The final Git LF archive hashes are the authoritative stored-object hashes:

- Replay boundary artifact, final Git LF archive: `0c210ddd7e93d14639a0c93c660c2c9ff4b2f3d316e1a28b677ceb6ff6123365`; original CRLF execution/worktree hash: `5f2ce8c03d3c37d882df760e584b5b6daa8c92467dfc578135cb140155adb0e4`.
- Replay rate artifact, final Git LF archive: `d23ee8a89d5837e1f23f0b95f6c333911d7ed0b4eb2b6abaf7aff466fa023fa7`; original CRLF execution/worktree hash: `c3993f4a9f314cb67970e0e48b381cef483e9a619ba88d9be355e0c75ab7d1ac`.
- Independent audit script: `e6aa237e12cc13440a8689355481819129a22be59678a19fd4003d9545abe1ea`.

## Spectral margin and symbol gate

The candidate has exact uniform margin `11/400`. The endpoint L1 margins are stronger:

- `t=-1/8`: `7/100`;
- `t=0`: `3/50`;
- `t=+1/8`: `1/20`.

This gives the required strict spectral margin for the finite Toeplitz compressions and the half-line Toeplitz operator, and the same margin applies to the complement symbols.

The endpoints are not equal in disguise. Their means are

- `p_- = 179/400`;
- `p_+ = 181/400`.

Since translations and reflection/conjugation preserve the mean, the certificate cannot be relying on endpoint equality. The rate artifact also contains three separate cases for `-1/8`, `0`, and `+1/8`.

The complex Toeplitz convention is internally consistent. The scripts use `c_k=(a_k-i b_k)/2`, `c_-k=conj(c_k)`, and kernel entries `K(i,j)=c_{i-j}`. In the boundary solve, past rows are ordered as `-1,-2,...`, future columns as `0,1,2`, so `T_{r,s}=c_{s-r}` and `B_{r,j}=c_{-r-1-j}`. In the n=4 rate step, the leading future corner is modified by the extreme-past kernel and the target bit is the last coordinate after the four-bit suffix. This matches the intended stationary time ordering.

## Boundary kernel audit

The boundary artifact contains exactly six cases:

```text
3 t-values x 2 symbols (f and 1-f) = 6.
```

For each case it stores an M64 dyadic solution `X` to the half-line variational problem. My audit recomputed from the saved `X`, without trusting the original solve:

- all residual rows `0,...,M+m-1`, with `M=64`, `m=3`;
- the finite-support tail immediately after those rows;
- `R_norm_bound`;
- `delta = R_norm_bound^2 / epsilon`;
- the variational corner matrix `A_X=C-H_X`.

All six recomputations exactly matched the frozen artifact, and all six replayed stable fields were identical to the frozen ones. The largest operator-error bound is

```text
4.5184132950619655e-28,
```

well below `epsilon=11/400`.

The variational direction is correct: with `R=B-TX`, `T>=epsilon I`, and `Y=T^{-1}B`,

```text
A_X - C_infty = R* T^{-1} R >= 0,
||A_X-C_infty|| <= ||R||_F^2 / epsilon.
```

The implementation uses a rational sum of componentwise absolute values as an upper bound for `||R||_F`, so the recorded `delta` is outward. This checks the infinite-past evidence used by the finite rate certificate.

## n=4 rate certificate audit

The strict certificate is the n=4 exact/interval computation, not the r=4/6/8/10 floating precheck recorded in the author's run log. I kept those separate.

For n=4, the frozen rate artifact claims

```text
3 symbols x 3 event distributions x 2^(n+1)
= 3 x 3 x 32
= 288 exact determinants.
```

My independent audit rebuilt the ordinary, all-one-boundary, and all-zero-boundary kernels for each of the three symbols. It then recomputed all 288 exact event probabilities using the row convention with selected rows from `K` and unselected rows from `I-K`, rather than the author's signed-diagonal determinant implementation. Every distribution normalized exactly to one and every checked exact mass was positive.

For each of the `3 x 16` suffixes, I recomputed the conditional probability interval

```text
lo = max(epsilon, q_one - e_one),
hi = min(1-epsilon, q_zero + e_zero),
```

with

```text
e = delta * (1 + ((1+delta)/(epsilon-delta))^2).
```

The finite conditional probability lay inside the interval in every suffix case, and the recomputed conditional ranges matched the artifact exactly. The weighted extreme-width values were contained in the artifact's outward intervals.

The replayed interval-log run reproduced the frozen cases and final rational gap exactly. I also recomputed the final gate formulas from the stored interval endpoints:

```text
gap_lower = (L_-^lower + L_+^lower)/2 - U_0^upper
gap_upper = (U_-^upper + U_+^upper)/2 - L_0^lower.
```

The exact rational endpoints are

```text
gap_lower =
-693046426809659199133195853982915230079245
/22835963083295358096932575511191922182123945984

gap_upper =
-167754027957762835391491573705809881363885
/22835963083295358096932575511191922182123945984
```

Both are strictly negative.

## Conditioning and monotonicity scope

The proof uses the previously allowed Lyons--Steif conditioning framework: after fixing a finite suffix, conditional negative association gives the all-one and all-zero earlier pasts as lower and upper one-site prediction extremes. I did not find a step that uses psi-mixing, or a step that tries to control dependence after a middle block by a forbidden mixing estimate.

The all-zero boundary is correctly handled through the complement symbol `1-f`, followed by complementing the finite future kernel. This is necessary; using the all-one boundary of `f` itself for zeros would be the wrong object.

## Run record

Frozen author runs recorded in the artifacts:

- Boundary unit: PID `161244`, exit `0`, `6.794719219207764` seconds, six cases, 1206 residual complex entries.
- Rate unit: PID `161258`, exit `0`, `0.060981035232543945` seconds, 288 exact determinants, classification `NEGATIVE_PAIR_GAP`.

Review-side replay and audit:

- Boundary replay: PID `57080`, exit `0`, `6.8759191036224365` seconds, six cases, 1206 residual complex entries.
- Rate replay: PID `17884`, exit `0`, `0.06266236305236816` seconds, 288 exact determinants, classification `NEGATIVE_PAIR_GAP`.
- Independent exact audit: PID `29660`, exit `0`, `0.4694324999873061` seconds, status `CORRECT`.

An earlier audit-result run, PID `46660` with `0.4844563999795355` seconds, covered the same frozen objects before argv/hash-record cleanup. It is superseded by PID `29660` and is not counted as a separate reviewer, search, or candidate.

The replay used Python `3.12.14` and existing local `mpmath 1.3.0` supplied on `PYTHONPATH`; no dependency was installed. The replayed rate scripts do not depend on NumPy. Thread settings for replay were `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, and `BLIS_NUM_THREADS=1`.

## Limitations

This is one fixed negative-pair certificate. It should be cited as `NEGATIVE_PAIR_GAP` for `S1-R2-B1`, not as a sign theorem for all non-even centers, all mixed cosine/sine directions, or the conjecture's full symbol class. The r=4/6/8/10 floating values in the author's run log are useful prechecks, but only `r2_rate_n4.json` is the strict exact/interval certificate audited here.

No critical gap was found in the audited frozen rate certificate.
