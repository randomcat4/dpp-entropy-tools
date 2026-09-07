# R3 false-positive and failure-mode audit

Conclusion: **CRITICAL_GAPS** if any listed failure can affect the final sign
and is not excluded by an exact certificate. **INCOMPLETE** if the failure is
plausible but not yet investigated. **CORRECT** only after each applicable check
has been run or proved unnecessary.

## 1. Wrong probability law

Failure: treating principal minors `det K_S` as exact event probabilities.

Why it creates false positives: principal minors are inclusion probabilities
`P(S subset X)`. Entropy uses exact atoms `P(X=S)`. For two sites,

```text
K = [[a,z],[z,b]], q=|z|^2
p_11 = ab-q
p_10 = a(1-b)+q
p_01 = (1-a)b+q
p_00 = (1-a)(1-b)-q.
```

These are not `[1,a,b,ab-q]`. A determinant-minor entropy can have a completely
wrong value and sign.

Executable check: for every candidate, recompute all exact atoms by Mobius
inversion and by mixed-row determinants. Require equality, nonnegativity and
sum one.

## 2. Sign convention reversal

Failure: reporting a positive `H(M)-[H(K_-)+H(K_+)]/2` as a positive R3 gap.

R3 uses

```text
Delta = [H(K_-)+H(K_+)]/2 - H(M).
```

A T3-style positive chord gap is `-Delta`. Any certificate must state which sign
is requested and should store both names if both conventions appear.

Executable check: recompute `Delta_lo=(H_-^lo+H_+^lo)/2-H_0^hi`; accept only if
`Delta_lo>0`.

## 3. Spectral feasibility from floats

Failure: accepting `0<K<I` from ordinary floating eigenvalues, approximate
Cholesky, or printed residuals.

False-positive path: a tiny negative eigenvalue may be rounded positive; an
endpoint near 0 or 1 may make atoms negative or logs singular. Strictness must
be quantitative.

Executable check: require rational `delta>0` and exact/interval witnesses for
`K_r-delta I >=0` and `I-K_r-delta I>=0` at endpoints. Record the same chord
margin or prove it by convexity.

## 4. Near-zero probability and `epsilon` patches

Failure: replacing zero or unresolved atoms by `epsilon`, clipping negatives, or
dropping tiny masses.

False-positive path: `-p log p` can dominate a tiny gap. A term that looks
smaller than machine precision may still decide the sign.

Executable check: exact atom classification. Exact zero contributes `0` by
limit. Positive atoms must retain rigorous log intervals. Unresolved sign means
`INCOMPLETE`, not certified.

## 5. Log and entropy interval mistakes

Failure: using `math.log`, decimal strings, ball midpoints without outward
conversion, or interval multiplication with the wrong direction.

False-positive path: the final lower gap uses endpoint lower bounds and midpoint
upper bound. Reversing any endpoint can flip a tiny result.

Executable check:

```text
H_lo = sum lower(-p log p),
H_hi = sum upper(-p log p),
Delta_lo = (H_-^lo+H_+^lo)/2 - H_0^hi.
```

For interval probabilities, split around the maximum of `-p log p` at `p=e^-1`
or use monotonic subintervals. For rational atoms, use rigorous log enclosures.

## 6. Determinant and logdet instability

Failure: computing determinants through floating `det`, `slogdet`, eigenvalue
products, or matrix determinant lemma denominators near singularity.

False-positive path: Mobius inversion subtracts many principal minors. Small
relative determinant errors can become large absolute atom errors after
cancellation.

Executable check: exact rational determinants for small `n`; otherwise
outward-rounded determinant intervals with a proof that Mobius sums are enclosed.
Record determinant method and residual bounds. Any atom interval crossing a
negative value must be refused or refined.

## 7. Grouping and orbit aggregation errors

Failure: compressing subsets by a guessed type without proving invariance, or
forgetting orbit sizes.

False-positive path: a few representative atoms can look normalized while the
full `2^n` distribution is not. Missing events bias entropy and gap.

Executable check: include the group action, orbit representatives, stabilizer
or orbit sizes, and a sum check. Cross-check at least one nontrivial small case
against full enumeration.

## 8. Confusing spectral entropy with DPP Shannon entropy

Failure: using `tr h(K)` as `H(K)`.

False-positive path: `tr h(K)` is the von Neumann/quasi-free spectral entropy
used in T2's upper bound, not the classical full-subset DPP entropy except in
special diagonal-product cases.

Executable check: every entropy line must name whether it is `H(K)` or
`tr h(K)`. R3 gap may only use `H(K)`.

## 9. T2 transfer misuse

Failures:

- using Claim B without a positive block buffer on `B`;
- using operator norm where Frobenius energy is required;
- omitting endpoint coefficients in the Jensen transfer;
- using the midpoint loss with the wrong sign;
- using T2's positive-gap application as an R3 seed.

Executable check for R3:

```text
Delta(B)^lo - (C_-^hi+C_+^hi)/2 > 0.
```

If that inequality is not proved, T2 is at most diagnostic.

## 10. Boundary and derivative hazards

Failure: applying an interior Hessian formula through zero-probability events or
through endpoints.

False-positive path: `0 log 0=0` makes entropy finite, but derivatives may
diverge or require one-sided asymptotics. A finite-difference sign near a
boundary is not a curvature certificate.

Executable check: curvature claims must list exact event jets
`(p,p',p'')`, prove positivity on the domain or provide a boundary asymptotic,
and verify `sum p=1`, `sum p'=0`, `sum p''=0`.

## 11. Structure overclaim

Failure: treating repeated-row, block-exchange, banded, graph-gluing, Toeplitz or
low-rank families as if they were the full real domain.

False-positive path: a family theorem can be true but irrelevant to generic real
symmetric kernels; a failed family search can be mistaken for evidence of a
universal theorem.

Executable check: every output includes a coverage matrix and a denominator of
families and instances attempted. The final theorem states only the quantified
family it actually proves.

## 12. Direct-sum and rate mistakes

Failure: claiming that direct sums, periodic block processes, or weak couplings
produce a scalar stationary entropy-rate result without a separate construction.

False-positive path: finite gaps can vanish after normalization; randomly
shifting a block process creates a mixture, not automatically a DPP.

Executable check: rate claims require a separate rate theorem with limit order,
gap density, scalar kernel and entropy-rate definition. Otherwise label the
result finite-window only.

## 13. Realification mistakes

Failure: transferring a complex Hermitian gap to real symmetric kernels via the
standard doubled real representation.

False-positive path: doubling changes the ground set and exact atom law. Full
subset entropy is not preserved by default.

Executable check: require a diagonal-unitary gauge proof, a separately
constructed real kernel, or an explicit embedding theorem preserving law,
entropy and gap sign.

## 14. Parser, provenance and coverage fabrication

Failures:

- JSON floats, duplicate keys, NaN/Infinity, unreduced rationals;
- dirty implementation state hidden from the response;
- certificate hash not bound to input hash;
- failed or refused attempts counted as completed;
- interrupted runs resumed without checking hashes;
- planned candidate count inferred after seeing successes.

Executable check: schema validation plus semantic validation before expensive
work. Enforce

```text
0 <= certified <= completed <= started <= planned
completed + failed <= started.
```

The producer may emit `CANDIDATE`, `INCOMPLETE` or `BLOCKED`; only an independent
review may say `VERIFIED` or `CORRECT`.

## 15. Public tool status traps

T2 PR #5 has a public fresh verification report for its finite theorem, but a
R3 candidate must still prove that the T2 hypotheses and sign conversion apply.

T3 PR #6 is public Draft/CANDIDATE. Its own PR notes say it needs fresh-context
verification, that the reference supports both marginal and L-ensemble modes,
and that the frozen v1 claims are marginal-kernel/all-exact-events only. Any R3
certificate using T3 must bind a fresh verifier to the exact commit, request,
certificate hash and checker.

No public `CANDIDATE` artifact is a theorem merely because it passed author-run
tests.
