STATUS: CORRECT

# Fresh-context verification of revised R3 grouped-count reduction

Fixed commit checked: `f9a9e23d766ff303e3ac0a020e5b9f2299f2b683`.
Parent commit: `19a8271375e457a0fe74c52f880bc32b0a69c2e7`.

Scope: this verifies only the frozen group-count reduction formula and its
revised exact reference tests. It does not certify any real counterexample,
chord gap, family-level concavity or non-concavity statement, T2 transfer, T3
certificate, or coverage of the full real-symmetric domain.

I read only the allowed frozen theorem, proof, hazards, lemma ledger,
`reduction/reference_implementation.py`, `reduction/tests/test_reduction.py`,
fixed self-test/gap summary outputs, and related run logs from the fixed commit.
Files were extracted with `git archive` into an isolated audit directory; the
shared repo was not written.

## Verdict

The v1 critical gap has been repaired. The exact rational reference
implementation now has a separate vector-`a_g` block-exchange path matching the
frozen theorem, and the revised tests include two nonconstant-`a_g` exact
`n=8` checks, one near the spectral boundary. In both cases, direct Mobius
atoms, full L-ensemble atoms, and grouped-count atoms agree exactly for all
`256` events; orbit multiplicities sum to `256`; the minimum atom is strictly
positive.

No new critical gap was found in the revised group-count reduction.

## Mathematical fidelity checks

Frozen theorem target:

- `research/R3/frozen_theorem_v1.md:10-16` defines normalized group indicators,
  group-specific `a_g`, and `K=A+U(C-diag(a))U^T`.
- `research/R3/frozen_theorem_v1.md:16-20` defines
  `ell_g=a_g/(1-a_g)`, `R=C(I-C)^(-1)`, `B=R-diag(ell)`, and
  `D_c=diag(c_g/(m_g ell_g))`.
- `research/R3/frozen_theorem_v1.md:28-37` states the spectrum, exact atom
  formula, orbit multiplicities and entropy formula.
- `research/R3/frozen_theorem_v1.md:48-53` explicitly avoids full-real-domain,
  entropy-concavity, floating gap, T2, and T3 claims.

Proof checks:

- Exact atom law: `research/R3/proofs/group_count_reduction_v1.md:19-36`
  derives the L-ensemble atom formula from the exact DPP generating function and
  identifies it with Mobius inversion. It does not use inclusion minors as atoms.
- Multiplication order: `research/R3/proofs/group_count_reduction_v1.md:20-21`
  uses `L=K(I-K)^(-1)`. Since `I-K` is a polynomial in `K`, the order is legal.
- Spectrum and determinant: `research/R3/proofs/group_count_reduction_v1.md:39-49`
  gives the group-constant / zero-sum decomposition and
  `det(I-K)=det(I-C) prod_g(1-a_g)^(m_g-1)`.
- Vector-`a_g` L formula:
  `research/R3/proofs/group_count_reduction_v1.md:53-60` gives
  `L=D+UBU^T` with group-specific `ell_g`.
- Count formula:
  `research/R3/proofs/group_count_reduction_v1.md:70-87` derives
  `det L_S=prod_g ell_g^{c_g} det(I_q+B D_c)`.
- Zero counts:
  `research/R3/proofs/group_count_reduction_v1.md:90-97` correctly uses
  Sylvester with `W=D_c^(1/2)`, so zero `c_g` entries do not require inverting
  `D_c`.
- Orbit and entropy:
  `research/R3/proofs/group_count_reduction_v1.md:105-114` correctly uses
  `N_c=prod_g binom(m_g,c_g)`, sums orbit sizes to `2^n`, and logs the
  single-event atom `p_c`, not the count-class mass.

## Revised implementation checks

The repaired exact block-exchange code matches the frozen vector-`a_g` formula:

- `research/R3/reduction/reference_implementation.py:375-395` validates
  vector `a_values`, one per group, positive group sizes, square symmetric `C`,
  and `0<a_g<1`.
- `research/R3/reduction/reference_implementation.py:399-425` builds the full
  rational `K` for the Mobius oracle when group sizes are perfect squares. The
  normalized indicator correction is
  `(C[gi,gj]-a_g 1_{gi=gj})/(sqrt(m_g)sqrt(m_h))`, plus `a_g` on the full
  diagonal, matching `A+U(C-diag(a))U^T`.
- The perfect-square restriction at
  `reference_implementation.py:406-415` is only for the full exact Mobius oracle
  with rational normalized indicators. It is not imposed on the theorem or on
  the reduced formula.
- `reference_implementation.py:439-463` implements
  `R=C(I-C)^(-1)`, `B=R-diag(ell)`, and
  `det(I-K)=det(I-C) prod_g(1-a_g)^(m_g-1)`.
- `reference_implementation.py:466-484` implements
  `D_c` with `diag_counts[j]=c_j/(m_j ell_j)` and applies it on the right:
  `small[i][j] += B[i][j] * diag_counts[j]`.
- `reference_implementation.py:506-534` compares direct Mobius atoms, full
  L-ensemble atoms, reduced atoms, normalization, orbit-size sum, and minimum
  atom.

I also checked the perfect-square boundary directly. For sizes `(2,3)`, the
reduced vector-`a_g` formula produced `12` count states and exact probability
sum `1`; the full Mobius oracle refused with
`exact full K construction requires perfect-square group sizes`. That confirms
the restriction is local to the exact full-K oracle.

## Test coverage and denominators

The revised exact tests check the previous scalar/repeated-row cases plus the
new frozen-family vector-`a_g` cases.

Relevant test lines:

- `research/R3/reduction/tests/test_reduction.py:120-131` defines the
  block-exchange exact verifier helper: it checks `C>0`, `I-C>0`, exact Mobius /
  L-ensemble / reduced equality, three sums equal to `1`, orbit-size sum
  `2^n`, and positive minimum atom.
- `test_reduction.py:133-138` is nonconstant `a_g=(1/5,3/4)`, sizes `(4,4)`.
- `test_reduction.py:140-145` is near-boundary nonconstant
  `a_g=(1/100,99/100)`, sizes `(4,4)`.

Independent rerun results:

```text
python -m unittest reduction.tests.test_reduction -v
exit code: 0
tests: 8/8 passed
```

```text
python -m unittest discover -s research/R3/reduction/tests -v
exit code: 0
tests: 8/8 passed
```

Thread caps used:

```text
OPENBLAS_NUM_THREADS=2
OMP_NUM_THREADS=2
MKL_NUM_THREADS=2
NUMEXPR_NUM_THREADS=2
```

Exact denominator summary:

- Scalar exact Mobius/reduced cases: `n=6` gives `64` events vs `24` count
  states; near-boundary scalar `n=8` gives `256` events vs `81` count states;
  scalar block-exchange `n=8` gives `256` events vs `48` count states.
- Scalar compatible chord check: three `n=6` direct Mobius entropy
  distributions, total `192` atom evaluations.
- Reduced-only scalar `n=12`: `4096` events represented by `256` count states,
  exact probability sum `1`, no full Mobius enumeration.
- New vector-`a_g` frozen-family exact case:
  `n=8`, `events=256`, `count_states=25`, `orbit_size_sum=256`,
  `mismatch_count=0`, all three sums equal `1`, minimum atom `13/640000`.
- New vector-`a_g` near-boundary exact case:
  `n=8`, `events=256`, `count_states=25`, `orbit_size_sum=256`,
  `mismatch_count=0`, all three sums equal `1`, minimum atom
  `401/1000000000000000000`.

Thus all `256` events in both new vector-`a_g` cases are compared against the
orbit reduction, and the orbit denominators match the full event denominator.

## Run logs and v1 denial retention

The revised run log preserves the earlier v1 rejection context:

- `research/R3/reduction/run_log.md:16-24` describes the eight-test revised
  suite and explicitly includes two nonconstant-`a_g` exact frozen-family
  checks.
- `research/R3/reduction/run_log.md:32-34` records the reduced-only `n=12`
  denominator.
- `research/R3/reduction/run_log.md:39-41` says the v1 verifier found the
  group-specific coverage mismatch, then records the revised eight-test runs
  exiting `0`.
- `research/R3/reduction/run_log.md:43-49` keeps the old failure ledger about a
  Decimal equality test; exact rational atom equality remains the real check.

The v1 gap/search summary remains diagnostic only:

- `research/R3/artifacts/out/search_smoke.summary.json:35` classification
  `NO_HIT`.
- `search_smoke.summary.json:68` best displayed
  `gap_endpoint_average_minus_midpoint=-0.006842470469982764`, not a positive
  R3 gap.
- `search_smoke.summary.json:81-90` records `float_candidate_count_new=0`,
  `trials_executed=120`, and warning that floating search is diagnostic only.

No new gap certificate, counterexample, or full-domain claim is introduced by
the revision.

## Remaining nonclaims

The following remain outside this `CORRECT` verdict:

- no proof of a positive R3 chord violation;
- no certification of any floating search result;
- no entropy interval / rigorous log certificate for a gap sign;
- no claim that grouped block-exchange families cover all real symmetric
  contractions;
- no T2/T3 certification.

Within those limits, the revised fixed commit satisfies the frozen v1
group-count reduction and repairs the previous vector-`a_g` coverage mismatch.
