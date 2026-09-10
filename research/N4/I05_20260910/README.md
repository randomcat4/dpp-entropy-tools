# I05 successor to agent24: moving rank-two support and multiple boundaries

Overall unrestricted target: **INCOMPLETE**. New analytic results below: **PROVED (author proofs), PENDING_REVIEW**. One stronger auxiliary bridge: **DISPROVED (method only, author rational certificate)**. No real-DPP entropy-concavity counterexample is claimed.

Successor research issue: [#83](https://github.com/randomcat4/dpp-entropy-tools/issues/83). Heavy continuous verification: [#87](https://github.com/randomcat4/dpp-entropy-tools/issues/87), **REQUESTED / NOT RUNNING**. Old [#61](https://github.com/randomcat4/dpp-entropy-tools/issues/61) is a different fixture and was not assumed executed. No reviewer, Codex run, or local-agent job is assumed active.

Branch `i05/rank2-moving-support-20260910` starts from main `65e59a46b49cd2dbb5c779a4cfae8cef26441984`. Only this new directory is changed. Main, other authors' branches and old windows 21–25 were not modified or assigned new work. This work stayed in the current author session. Commit identifiers serve only to bind sources, not as mathematical checksums.

## Deliverables and scope

| Unit | Author verdict | Exact conclusion | Not concluded |
|---|---|---|---|
| Full rank-two midpoint expansion | PROVED | All mixed squared minors, pair mixed discriminant bound, triple/quadruple terms and full Mobius atoms | Entropy sign from inclusion minors alone |
| Common dense mode with three-coordinate motion | PROVED | Moving rank-two endpoints with intersecting support have strict true midpoint gap; all cross terms retained by complete conditioning | Arbitrary unrelated rank-two endpoints |
| Coordinate-supported indefinite rank-two difference | PROVED | Any ambient dimension and arbitrary correlated outside blocks; full legal chord strictly concave, explicit quadratic or quartic gap | Replacing actual coordinates by a spectral rotation |
| Fixed affine multiple-boundary approach | PROVED | H''=-beta/h+O(1+abs(log h)); beta>0 for strict inward lines and for moving rank-two ranges | Uniform endpoint neighborhoods under varying angles/scales or a full-chord theorem |
| Rank-two event-mixture entropy bridge | DISPROVED, method only | Dense exact rank-two endpoints, rank-four midpoint, strict-kernel lift; H(mixture)>H(midpoint law) | Entropy counterexample: actual Delta is strictly negative |
| New strong-correlated double-endpoint multiring | PARTLY PROVED / INCOMPLETE | Exact legality, 64 quartics, failure of a conditional sufficient test, beta=6784/16875, three certified finite negative samples | Whole compact-middle sign or a general multiring theorem |
| Independent review / novelty / global conclusion | PENDING_REVIEW / NOT ASSESSED / INCOMPLETE | No upgrade from an upload or author execution | ACCEPTED, independent PASS, novelty or priority |

Read [proof.md](proof.md) for the first uploaded analytic checkpoint. [continuation.md](continuation.md) contains the subsequent coordinate-conditioning theorem, explicit strong margins, and the new double-boundary construction. Thus work continued after the initial upload. [fixtures.md](fixtures.md) specifies all rational inputs and error semantics. [verify.py](verify.py) is the one bounded author check, and [certificate_compact.json](certificate_compact.json) retains every atom or atom-polynomial coefficient, including exact zeros.

### A concrete family in each of n=4,5,6

Take `u=(1,...,n)^T`, `v=(1,-1,1,0,...,0)^T`, `w=(1,2,-1,0,...,0)^T` and

```text
A=uu^T/200+vv^T/12
B=uu^T/200+ww^T/20.
```

For all three dimensions, the Gram matrices are positive semidefinite, `tr B<=151/200<1` and `tr A<=141/200<1`. The ranges intersect exactly in span(u); both endpoints have rank two and the actual midpoint has rank three. Theorem 3 gives, for every common `0<epsilon<1/2` lift,

```text
G_epsilon >= 49*(1-2*epsilon)^2/7200 > 0.
```

This explicit family is not a fixed-five-frame spectral invariance claim. Its nonzero difference acts on three actual coordinates. The six-point member also has the more detailed full-event rational certificate.

## What was read before drawing conclusions

The main `docs/research_status.md` and `docs/route_ledger.md` were checked for current accepted ranges, not treated as proof by themselves. The full accepted PR62 record, original agent24 rank-one theorem, multiring fixture, prior-art file, failure ledger, exact fixture code and PR62 SECOND review were read. The SECOND review explicitly did not execute the author scripts; that limitation was not promoted away. The accepted PR43-E statement and its original three-coordinate proof were read and the conditional four-cycle bridge was rederived in `proof.md`.

Old author's `PROVED` labels and old `RUNNING` issue states are not used as current independent approval. The new results here have no independent approval yet.

## Two different methods and primary-source audit

**Exterior areas / mass comparison.** The actual arithmetic midpoint is analyzed by Cauchy--Binet followed by full Mobius inversion. Nonnegative mixed areas and the two-by-two mixed-discriminant inequality do not force a nonnegative correction relative to the endpoint law mixture. The failed bridge is tested on exact dense moving endpoints, and its failure is separated from the true Jensen sign.

**Conditional configuration laws / complete Fisher and rare events.** Exact outside conditioning preserves a three-coordinate affine direction, allowing a full Fisher-preserving lift of the accepted lemma. Separately, polynomial orders of complete zero atoms yield the fixed-line boundary asymptotic. A cardinality-generating determinant is used only to force some linear emerging mass; it is not substituted for complete configuration entropy. The correlated 3+3 example exhibits extra linear rare atoms absent from that coarse count bound.

Primary texts were inspected, including the relevant PDF pages, in this author session:

- Hough, Krishnapur, Peres and Virag, *Determinantal Processes and Independence*, Probability Surveys 3 (2006), [arXiv:math/0503110v2](https://arxiv.org/abs/math/0503110v2), Theorem 7. It gives the Bernoulli eigenvalue/count and projection-mixture representation. It does not identify configuration entropy after a changing physical frame with the entropy of the count. The needed count derivative was independently derived from `det(I+(z-1)K)` in `proof.md`, so no entropy bridge is imported from that representation.
- Lyons, *Determinantal probability measures*, [arXiv:math/0204325v4](https://arxiv.org/abs/math/0204325v4), Section 6 and Section 8, especially Theorem 8.1 and the complete-event discussion in Remark 8.4 / equation (8.3). These support conditioning, negative dependence and exact event formulas. The decisive conditional formula (20) in `continuation.md` is checked directly by signed Schur determinants; the constancy of its affine direction is proved explicitly rather than inferred just from closure under conditioning.
- Audenaert, *A Sharp Fannes-type Inequality for the von Neumann Entropy*, [arXiv:quant-ph/0610146](https://arxiv.org/abs/quant-ph/0610146), Theorem 1. Only its classical diagonal-distribution specialization is used: alphabet `2^n`, total variation `one-half L1`, and all logs converted consistently to natural logs. The required monotonicity range is stated. A self-contained maximal-coupling proof is also given in `proof.md`; quantum entropy is never substituted for DPP configuration entropy.

For the claimed scoped results there is no unproved external entropy theorem silently assumed. The three-coordinate lemma and rank-one strictness are reproduced; the other key steps are elementary determinant, probability and entropy calculations. This audit does not establish novelty, priority, or completeness of the literature search.

## Failure and limitation ledger

1. **Rank-one reuse by splitting each rank-two endpoint.** Rejected: equations (1)–(5) in `proof.md` expose the missing mixed pair, triple and quadruple terms. No entropy additivity across such modes is assumed.
2. **Extending the rank-one entropy-increasing mixture bridge.** Disproved by the exact four-point fixture. The positive bridge failure is approximately 0.00099723447547, whereas the true Delta is approximately -0.06198846819720. Both signs are rigorous rational-log certificates and remain strict after the specified common bit flips.
3. **Inferring the bridge from nonnegative mixed discriminants.** Invalid: the actual correction is `(C_ij-a_ij^2-b_ij^2)/4`, of mixed sign in the same dense example. All pair signs and full laws are archived.
4. **Closing the multiring middle by a previously accepted conditional test.** The exact complete left configuration `{2}` produces a semidefinite rank-two direction with inconsistent diagonal-anchor ratios. This sufficiency test fails; actual entropy curvature at every certified sample is still negative.
5. **Using a simple-boundary theorem at a multiple endpoint.** Not allowed. A new complete-polynomial asymptotic is supplied instead. It proves existence of endpoint neighborhoods, but the quantitative overlap needed for a full interval certificate is still missing and is assigned only as REQUESTED in #87.
6. **Promoting finite probes, endpoint asymptotics, or count entropy.** None closes the remaining middle. The computed beta includes all linear-zero atoms; the coarse count lower bound is strictly smaller. No generic random scan was run.
7. **Numerical and publication history.** Preliminary ordinary high-precision diagnostics were not used as certificates; the final fixed script uses exact rational event arithmetic and explicit outward log bounds. A container git-clone attempt failed on DNS, but GitHub connector reads and branch writes succeeded; no missing permission or fallback URL was fabricated. There was no interval-family run, no independent rerun, and no CI claim. The failed auxiliary routes remain recorded rather than removed after a successful scoped proof.

## Exact outstanding obligations

The unrestricted statement for two arbitrary moving rank-two endpoint kernels is still undecided. Their difference can have rank four and need not be supported on three actual coordinates. The fixed-line endpoint result does not bound their compact middle or uniform multi-parameter degenerations. A valid disproof would still need legal exact kernels and a positive rigorous true Delta, which this packet does not contain.

The new multiring continuous sign task is specified in #87 with exact input, reconstruction algorithm, full Fisher/error certificates, endpoint remainder, 90-minute/8-GiB initial resource cap, explicit stop conditions and saved-queue recovery. Its status remains REQUESTED, not an assertion that anybody has started. Old #61 remains separate and unexecuted in this session. Independent mathematical review of this packet is PENDING_REVIEW, and no merge or acceptance is requested on the strength of the author run alone.
