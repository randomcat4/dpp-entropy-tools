# T1 criterion exploration: one bounded work unit

Result: a complete author proof under main-instance-frozen theorem v1, plus an exact rational structural checker. Mathematical status is PROVED by author; independent review and novelty remain pending. This route did not read another route's proof during its first round and did not spawn descendants.

## Candidate denominator and decisions

| Candidate | Outcome | Precise reason |
|---|---|---|
| Rank-one affine directions | REJECTED as target | Determinants are affine on a rank-one line, so ordinary entropy concavity applies; this is already Theorem 7 in Gu's report below. |
| Block-diagonal center Hessian locality | HOLD, not formally pursued | At an independent-block center, the candidate identity is H''_K[D]=sum_B H''_{K_B}[D_BB]; it would reduce enumeration to the largest block. Retained as a candidate only; no second theorem was frozen here. |
| Forest center with existing-edge imaginary directions | PROMOTED through bridge formulation | Determinant phases vanish on bridges, and conditional two-endpoint reduction gives a strict sign. The final frozen theorem permits arbitrary dense cyclic blocks connected by bridges. |
| Arbitrary cyclic-edge phase directions | INCOMPLETE / outside target | A cycle in the determinant can carry phase; after conditioning the endpoint off-diagonal has a nonzero correction. No unsupported sign inference is made. |

Main-instance frozen premises: real symmetric strict K, D=iA with A real skew and supported on existing graph bridges. Only the main instance selected and froze this version. The proof does not treat an arbitrary real center's vanishing p' as enough to settle H''.

## Concrete output and checking cost

- `../frozen_theorem_v1.md`: exact statement and exclusions.
- `../proofs/criterion_v1.md`: complete conditional reduction and multibridge derivative proof.
- `criterion/bridge_certificate.py`: no-third-party rational premise checker.
- `criterion/examples/two_triangles.json`: dense cyclic blocks linked by a bridge, outside the forest-only starting idea.
- `criterion/artifacts/`: exact certificate, test log, fixed diagnostics, failed attempt, and run record.

Dense rational checking uses O(n^3) arithmetic operations and O(n^2) storage, plus O(n+m) graph processing; rational bit growth is not hidden inside a claimed unit-cost bit bound. The sign checker evaluates zero event probabilities and does not evaluate entropy or logarithms. A failed support test is not a counterexample.

## Bounded checks and actual coverage

Completed 11 unit tests: two-point nonzero, several tree edges, dense blocks plus bridge, cyclic-edge rejection, absent-edge rejection, zero direction on disconnected graph, strict-boundary rejection, nonsymmetric rejection, nonskew rejection, float rejection, and a 2000-vertex path for recursion-free graph traversal. The long-path case tests graph code only, not a dense 2000 by 2000 LDL calculation.

Completed four predetermined derivative diagnostics with n=2,3,6,3, respectively 4,8,64,8 full events (84 total). Determinants, inverse matrices, masses, zero scores, and Schur complements are exact rational computations; logarithms and final curvature sums are floating point. Direct and conditional formulas differ by at most 6.4e-16. These numbers do not prove the general theorem and are not strict interval certificates.

The six-vertex application gives approximately -0.0800356541182764 for the stated unit bridge direction. The theorem also covers an unbounded dense-block tree family by a Gershgorin strict-interior bound; finite testing is not used to infer this unbounded coverage.

First diagnostic execution failed because NumPy was unavailable. No package was installed: the diagnostic was rewritten in the standard library and the failed attempt retained. No mathematical counterexample was found or searched for globally. All calculations used a single remote process with all BLAS/OpenMP thread settings 1, address-space limit 8 GiB, and no GPU. The final four-case derivative diagnostic took about 0.05 seconds; exact time/PID/version are in its JSON. No external jobs or global configuration were altered.

## Scoped prior-art audit, not a novelty certificate

1. Yuzhou Gu, *Entropy of Determinantal Point Processes*, Theorem 7: concavity along rank-one kernel differences. This occupies the elementary rank-one candidate. Source: https://sevenkplus.com/data/dpp.pdf (read 2026-09-07).
2. Hino and Yano, *An embedding structure of determinantal point process*, Information Geometry 7 (2024), 523-542: Theorem 1 embeds DPPs in log-linear models, and Corollary 1 concerns vanishing e-embedding curvature in item-quality parameters. This is a different curvature and parameterization from the affine marginal-kernel Shannon Hessian. Source: https://link.springer.com/article/10.1007/s41884-024-00156-x (read 2026-09-07).
3. Tadić, *Graphical structure of conditional independencies in determinantal point processes*: the abstract reports kernel-based conditional independence structure, including L-ensemble graphs. This is an application-neighbor lead, not a checked theorem implying the bridge-curvature result. Source: https://arxiv.org/abs/1406.5577 (abstract read 2026-09-07).
4. Bufetov, Qiu and Shamov, *Kernels of conditional determinantal measures and the Lyons-Peres completeness conjecture*: the published abstract identifies preservation of determinantal structure under conditioning. The finite conditioning formula needed here is proved directly rather than imported with unverified hypotheses. Source: https://ems.press/journals/jems/articles/17429 (abstract read 2026-09-07).

Searches included DPP entropy monotonicity/off-diagonal bridge, conditional kernel entropy concavity, and information geometry. No primary-source identity matching the exact bridge-supported theorem was established in this bounded audit. That is not evidence of firstness; novelty status is UNCONFIRMED. The result is presently a structural auxiliary tool, not a claimed paper-core theorem.

## Minimal remaining obligation and next falsifiable action

A new context must review the fixed statement and proof, especially the exact conditioning signs, the z-independent Schur complement diagonal, bridge phases in permutation cycles, and strictness. The author has not independently verified their own proof. No Lean project is present; no formal proof was executed. The main instance owns any subsequent premise repair and final integration.
