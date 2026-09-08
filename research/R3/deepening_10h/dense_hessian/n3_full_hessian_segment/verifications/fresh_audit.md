STATUS: CORRECT

Scope: non-author audit of `research/R3/deepening_10h/dense_hessian/n3_full_hessian_segment/`.
This certifies the continuous segment certificate for this explicit `n=3`
line only.  It does not certify global dense-Hessian concavity, every M8
product-region point, or the failed extension radii.

## Author files read

- `frozen_problem.md`
- `proof_algorithm.md`
- `segment_hessian_certificate.py`
- `segment_certificate.json`
- `run_log.md`
- `verdict.md`

Main frozen claim checked:

- `frozen_problem.md:52-69`: interval `t in [-6/25,6/25]`, strict real DPP kernel, connected graph, heterogeneous diagonal, distinct spectrum, and full `Sym(3)` strict negative Hessian.
- `frozen_problem.md:85-96`: accepted certificate route: exact-event signed determinant, `6 x 6` Hessian, rational subdivisions, rational log intervals, Gershgorin, with `49/200` and `1/4` retained as certificate failures only.

Main proof-algorithm lines checked:

- `proof_algorithm.md:7-14`: spectral coordinates and `1/25` strict margin.
- `proof_algorithm.md:22-31`: off-diagonal zero roots, diagonal equality root, and spectral collision exclusions.
- `proof_algorithm.md:33-70`: exact-event Hessian formula and six-coordinate basis.
- `proof_algorithm.md:79-101`: rational interval/log certificate.
- `proof_algorithm.md:124-148`: `173` subdivision leaves, atom lower bound `63029/5000000`, and failed expansion radii.
- `proof_algorithm.md:153-158`: limited scope; not a grid theorem and not a global theorem.

## Independent command

Working directory:

`C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo`

Command:

```text
$env:OMP_NUM_THREADS='1'; $env:OPENBLAS_NUM_THREADS='1'; $env:MKL_NUM_THREADS='1'; $env:NUMEXPR_NUM_THREADS='1'; $py='C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'; & $py 'C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo\research\R3\deepening_10h\dense_hessian\n3_full_hessian_segment\verifications\fresh_s8_audit.py'; exit $LASTEXITCODE
```

Exit code: `0`.  Script elapsed time: `70.03948450088501` seconds.

Independent outputs:

- `verifications/fresh_s8_audit.py`
- `verifications/fresh_s8_audit.json`

The independent script does not import `segment_hessian_certificate.py` or any author certificate module.  It reconstructs exact atoms by Möbius inversion from inclusion determinants, separately checks the signed-determinant identity, builds the six-coordinate Hessian, and then reruns rational interval logarithms and Gershgorin subdivision.

## Structure and feasibility

The independent exact checks confirm:

- `U,V,W` are pairwise orthogonal projectors and sum to `I`.
- Reconstructed `K0` and `R` match the frozen matrices.
- Spectral coordinates are
  `(1/5+t/5, 1/2+t/3, 4/5+2t/3)`.
- On `|t|<=6/25`, the minimum spectral/complement margin is exactly `1/25`.
- Off-diagonal zero roots are `-153/128`, `-171/106`, `-45/8`, all outside the certified interval.
- Diagonal equality roots are all `-9/10`, outside the certified interval.
- Spectral collision roots are `-9/4`, `-9/7`, `-9/10`, outside the certified interval.

Thus strictness, connected observation graph, heterogeneous diagonal, and distinct spectrum all hold on the closed interval.

## Exact-event and Hessian semantics

I rebuilt all event atoms by Möbius inversion:

`p_S(K)=sum_{T superset S} (-1)^{|T|-|S|} det K_T`.

For all eight events and every coordinate-direction jet used in the Hessian,
the script separately checked equality with

`p_S(K)=(-1)^{|S^c|}det(K-I_{S^c})`.

Mass identities were exact polynomial identities in `t`:

- `sum_S p_S(t) = 1`;
- all first total-mass derivatives vanish;
- all bilinear second total-mass derivatives vanish.

So the constant term in

`D^2H = -sum p_E p_F/p - sum (1+log p)p_EF`

is legitimately dropped, giving

`B=-D^2H = sum p_E p_F/p + sum p_EF log p`.

Coordinate order checked:

`(11,22,33,12,13,23)` with off-diagonal basis matrices `E_ij+E_ji`.

Positive definiteness of this raw six-coordinate `B` is sufficient for strict negativity on all of `Sym(3)`, because this is an invertible coordinate basis.  No Frobenius lower-bound constant is claimed here, so there is no missing `sqrt(2)`/factor-two conversion in the theorem.

## Independent interval certificate

Parameters:

- events: `8`;
- Hessian coordinates: `6`;
- log terms: `20`;
- max subdivision depth: `10`;
- attempted radii: `8`.

Independent radius table:

| radius | result | pass leaves | failed leaves | splits | spectral margin | min Gershgorin margin, decimal | min atom lower |
|---:|---|---:|---:|---:|---:|---:|---:|
| `1/100` | certified | 8 | 0 | 7 | `29/150` | `0.0762221649036794304211514178186609183844740337693548831969803` | `17279549/270000000` |
| `1/50` | certified | 16 | 0 | 15 | `14/75` | `0.0690461400207781407802978640878442723966542630216276424803413` | `29419427/472500000` |
| `1/20` | certified | 32 | 0 | 31 | `1/6` | `0.0248453152142261124483071081089636292962284118685829043442376` | `3444139/60480000` |
| `1/10` | certified | 62 | 0 | 61 | `2/15` | `0.0000139140219128599044146216488877128410003079724676063387708492` | `360827/7560000` |
| `1/5` | certified | 142 | 0 | 141 | `1/15` | `0.0000139140219128599044146216488877128410003079724676063387708492` | `487/22500` |
| `6/25` | certified | 173 | 0 | 172 | `1/25` | `0.000266257532470043279039064591135171371973534722446801527310437` | `63029/5000000` |
| `49/200` | certificate failed | 174 | 10 | 183 | `11/300` | `0.00130455096123016876674117240742270277038094149020778204877704` over passed leaves only | `8426922735979/671088640000000` over passed leaves only |
| `1/4` | certificate failed | 175 | 20 | 194 | `1/30` | `0.0000332485968685008771926446666786585584525323989411213660397702` over passed leaves only | `252707947/20132659200` over passed leaves only |

For the certified radius, the independent `6/25` results match `segment_certificate.json:161-170` and the top-level certificate summary at `segment_certificate.json:3571-3577`.

The author run log also records the same successful and failed radii at `run_log.md:43-56`; the final command and exit code appear at `run_log.md:19-27`.

## Failed expansion radii

The failed `49/200` and `1/4` entries are correctly treated as proof-method blockers, not counterexamples:

- `run_log.md:55-64` records them as certificate failures.
- `run_log.md:79-84` records float probes as diagnostics only, not certification.
- My independent 101-point float scouts also found positive sampled minimum eigenvalues of `B=-Hess H` at these failed radii:
  - `49/200`: worst sampled `lambda_min(B) ~= 0.718323636796787`;
  - `1/4`: worst sampled `lambda_min(B) ~= 0.7175799845110842`.

These float probes do not certify the failed radii; they only support the author's statement that the failures are not known positive-curvature examples.

## Author artifact consistency

`segment_certificate.json` contains:

- status at `segment_certificate.json:2`;
- `6/25` certified row at `segment_certificate.json:161-170`;
- failed `49/200` and `1/4` rows at `segment_certificate.json:2943-2946` and `segment_certificate.json:3157-3160`;
- top-level largest certified radius/interval/atom floor at `segment_certificate.json:3571-3577`;
- script hash at `segment_certificate.json:3629`.

Computed current author hashes:

- `segment_hessian_certificate.py`: `4d9cea5e8a8768b15c254caefdccdc5b681afcefbfdde5ebf3f033346567c713`.
- `segment_certificate.json`: `f7279f823b8931bf474c4b9036f7ccfafadac59ad2c6c8d8c019120a86a5c169`.

The current script hash matches the JSON's `script_sha256`.  The run log records the command/output summary but not the SHA line; I did not treat that documentation omission as a mathematical gap because the JSON self-hash linkage and independent reconstruction match.

## Verdict

No critical gap found.

- Continuous coverage of `[-6/25,6/25]`: CORRECT.
- Strict `0<K(t)<I`, connected graph, heterogeneous diagonal, distinct spectrum: CORRECT.
- Exact-event/Möbius semantics and six-coordinate Hessian: CORRECT.
- Rational log intervals and Gershgorin positive-definiteness certificate with `173` leaves: CORRECT.
- Failed expansion points `49/200`, `1/4`: correctly classified as certificate blockers only.

No repair requested.
