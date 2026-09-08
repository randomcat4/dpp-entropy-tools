# D10-M8 n3_complement_barrier_refine fresh non-author audit

STATUS: CORRECT

Scope of this status: the analytic sufficient-region refinement and the copied exact rational sanity/segment certificates.  The six-center computation remains SCOUT evidence, and the original global fixed-\(Q\) target remains INCOMPLETE when the \(C_i\) signs are not assumed.

I did not modify author materials.  I added only:

- `verifications/fresh_m8_audit.py`
- `verifications/fresh_m8_audit.json`
- `verifications/fresh_audit.md`

No server was used.  No `C:\canglan\` path was accessed.

## Files and statements checked

The frozen problem states the objects and scope at `frozen_problem.md:8-16`, including \(P_{ai}=q_{ai}^2\), \(r_i\), \(s_i\), \(R,T\), \(\alpha=Pr/R\), \(\beta=Ps/T\), exact-event entropy, and the unresolved global target.

The candidate fixed-base claims are at `frozen_problem.md:18-29`:

- \(A=2\sum_{j<k}v_jv_k C_i\), with \(i\) the remaining index;
- \(\min_i C_i>0\Rightarrow B=-H''>0\) for every nonzero \(v\ge0\);
- \(m=\min_a\alpha_a\beta_a>1/27\Rightarrow C_i\ge\log(27m)>0\);
- the quantitative compact-margin lower bound.

Boundary exclusions are correctly stated at `frozen_problem.md:31-41`: opposite one-sign rates by sign reversal, zero rate \(B=0\), single nonzero rates included, fixed-\(Q\) commuting PSD/NSD only, no strictness at \(m=1/27\), and no uniform constant without spectral/product margin.

The proof’s vulnerable formulas appear at:

- event/channel setup and exact-event warning: `proof_or_blocker.md:8-14`;
- imported count entropy concavity and decomposition: `proof_or_blocker.md:25-31`;
- complementary-index acceleration identity: `proof_or_blocker.md:35-50`;
- fixed-base \(A\ge0\iff C_i\ge0\) on the nonnegative cone: `proof_or_blocker.md:57-60`;
- product condition and AM--GM signs: `proof_or_blocker.md:64-79`;
- single-rate boundary and one-fifth normalization logic: `proof_or_blocker.md:80-87`;
- quantitative bound: `proof_or_blocker.md:99-118`;
- pointwise/segment/global scope: `proof_or_blocker.md:130-133` and `proof_or_blocker.md:177-190`;
- exact examples and exponent-clearing certificate: `proof_or_blocker.md:140-171`.

The count theorem imported in `proof_or_blocker.md:28-31` is used only for the count distribution \(N=\sum_i \mathrm{Bernoulli}(\theta_i+t v_i)\).  I checked the cited primary source, Hillion--Johnson, arXiv:1503.01570, Theorem 1.2: it gives concavity of the entropy of sums of independent Bernoulli random variables in their parameters.  That supports \(-h''\ge0\) for the count layer only; it does not by itself control the full DPP event entropy.

## Command run

From repo root:

```powershell
$env:OMP_NUM_THREADS='1'; $env:OPENBLAS_NUM_THREADS='1'; $env:MKL_NUM_THREADS='1'; $env:NUMEXPR_NUM_THREADS='1'; & 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'research\R3\deepening_10h\dense_hessian\commuting_spectral\n3_complement_barrier_refine\verifications\fresh_m8_audit.py'
```

Exit code: `0`.

The independent verifier did not import or run author `sanity.py`.

## Analytic identity audit

Status: CORRECT.

For \(n=3\), if the spectral pair of varied coordinates is \(\{j,k\}\) and the remaining index is \(i\), then

\[
r''_{\{j,k\}}=2v_jv_k\{\theta_i e_i-(1-\theta_i)(e_j+e_k)\},
\]

\[
s''_{\{j,k\}}=2v_jv_k\{(1-\theta_i)e_i-\theta_i(e_j+e_k)\}.
\]

The pair layer is indexed by the missing observation coordinate \(a\).  For a real orthogonal \(3\times3\) matrix, the complementary \(2\times2\) minor squared equals \(q_{ai}^2\), so the same \(P\) sends both the singleton spectral layer \(r\) and pair-missing spectral layer \(s\) to observed layers.

Using row stochasticity,

\[
P(e_j+e_k)=\mathbf 1-Pe_i,
\]

the output coefficients are \(P_{ai}-(1-\theta_i)\) in the singleton layer and \(P_{ai}-\theta_i\) in the pair-missing layer.  Therefore

\[
A=2\sum_{j<k}v_jv_k C_i,
\]

where

\[
C_i=\sum_aP_{ai}\log(\alpha_a\beta_a)
-(1-\theta_i)\log\prod_a\alpha_a
-\theta_i\log\prod_a\beta_a .
\]

The \((1-\theta_i)\) factor belongs to \(\prod\alpha\), and \(\theta_i\) belongs to \(\prod\beta\).  Reversing those two would be the wrong complement identification.  The independent Decimal check recomputed \(C_i\) both from this closed form and from the direct paired acceleration; discrepancies were below `1e-80`.

Because \(v_jv_k\ge0\), \(A\ge0\) on the whole nonnegative cone iff all \(C_i\ge0\).  Necessity is obtained by setting exactly the complementary two rates positive and the remaining rate zero.  This equivalence is only for \(A\), not for total \(B\).

## Product barrier and boundary audit

Status: CORRECT.

For fixed \(i\), the weights \(P_{ai}\) are column weights and sum to one; the verifier checked every stored \(P\) is both row and column stochastic.  If

\[
m=\min_a\alpha_a\beta_a,
\]

then

\[
\sum_aP_{ai}\log(\alpha_a\beta_a)\ge\log m.
\]

Since \(\alpha,\beta\) are probability triples, AM--GM gives

\[
\prod_a\alpha_a\le1/27,\qquad \prod_a\beta_a\le1/27.
\]

The minus signs in \(C_i\) therefore go in the useful direction:

\[
C_i\ge \log m+\log 27=\log(27m).
\]

Thus \(m>1/27\) gives \(C_i>0\) for all \(i\).  This proves \(B>0\) for all nonzero \(v\ge0\): if at least two rates are positive, \(A>0\); if exactly one rate is positive, the count law is affine in that coordinate and the count Fisher term is strictly positive.  The verifier checked the single-rate boundary by exact count-polynomial Fisher computations for all three one-rate directions at all six centers.

The simpler one-fifth condition is also correctly stated.  If all entries of both \(\alpha\) and \(\beta\) are at least \(1/5\), then \(m\ge1/25>1/27\).  Since each layer is a probability triple, any entry is automatically at most \(1-2/5=3/5\).  This is a normalization consequence, not an extra hidden assumption.

No strict conclusion is claimed at \(m=1/27\), and I found no place where the proof relies on a non-strict boundary as if it were strict.

## Quantitative bound

Status: CORRECT.

For \(\theta_i\in[\epsilon,1-\epsilon]\), the proof sets \(L=1/[\epsilon(1-\epsilon)]\).  The count Hessian \(C=-\mathrm{Hess}\,h\) is PSD by the imported Bernoulli-sum entropy concavity theorem.  Its diagonal entries obey:

- lower bound \(C_{jj}\ge4/3\), because the count score has covariance \(1\) with \(N\), while \(\mathrm{Var}(N)\le3/4\);
- upper bound \(C_{jj}\le L\), by conditioning/data-processing from the latent Bernoulli score;
- hence \(|C_{ij}|\le L\) by PSD Cauchy.

For unit \(v\ge0\), let \(a=\max_jv_j\) and \(s=\sum_{i\ne j}v_i\).  The two-case split in `proof_or_blocker.md:104-112` is sound:

- if \(s\le a/(3L)\), the count term gives at least \(2/9\);
- otherwise \(\sum_{i<j}v_iv_j>1/(9L)\), and \(A\ge2\mu/(9L)\).

With \(\mu=\log(27m_0)\), this yields

\[
B\ge \frac{2\log(27m_0)\epsilon(1-\epsilon)}9\|v\|^2
\]

for \(m\ge m_0>1/27\).  This is a pointwise sufficient-region bound.  Along an entire affine segment it applies only if the segment stays in the same strict spectral/product-margin family.

## Independent exact computation

Status: CORRECT for exact sanity; SCOUT as finite evidence.

The verifier read `sanity_results.json` as data and independently rebuilt:

- exact-event polynomials from the listed rational \(K+tD\) via inclusion determinants and Möbius inversion;
- singleton layer \(y=Pr\) and pair-missing layer \(z=Ps\);
- \(\alpha=y/R\), \(\beta=z/T\);
- all three \(C_i\) from the closed formula and from direct complementary acceleration;
- \(A=2\sum v_jv_kC_i\);
- direct \(B=-H''\) from all eight exact events and the decomposition \(-h''+D_P(r)+D_P(s)+A\);
- exact exponent-clearing rational signs for all \(C_i\);
- degree-six interval polynomials \(27y_a(t)z_a(t)-R(t)T(t)\), their coefficient lists, lower bounds, pass/fail flags, and spectral margins.

Counts:

| item | count |
|---|---:|
| centers | 6 |
| exact event polynomials | 48 |
| scalar coefficients compared | 192 |
| interval attempts | 12 |
| interval constraints | 36 |
| passed interval attempts | 10 |
| failed interval attempts | 2 |
| failed interval constraints | 2 |
| product-condition centers | 5 |
| one-fifth centers | 1 |
| exact \(C_i>0\) centers | 6 |

Case summary:

| case | product condition | one-fifth condition | exact \(C_i>0\) | direct \(B\) |
|---:|---|---|---|---:|
| 0 | yes | no | yes | 2.536537494892062364311334600 |
| 1 | yes | no | yes | 2.523657615059543175803248863 |
| 2 | yes | no | yes | 2.668260556584140707736396471 |
| 3 | yes | no | yes | 2.587435885387028772774066073 |
| 4 | no | no | yes | 4.411105527021803854296339157 |
| 5 | yes | yes | yes | 2.535277859866233175084237612 |

The two failed interval constraints are exactly retained:

- case 4, step `1/100`, constraint `a=2`, lower bound `-2039981670550277/24806250000000000`;
- case 4, step `1/1000`, constraint `a=2`, lower bound `-980398129879087187791/12403125000000000000000`.

This matches the author denominator: 12 attempts, 10 pass, 2 fail.  The failures are not mathematical counterexamples to the sufficient theorem; they are failed product-segment certificates at a center already failing the product condition.

## Scope and quantifiers

Status: SCOUT/INCOMPLETE outside the sufficient subclass.

Correct scope:

- fixed \(Q\), \(n=3\);
- one-sign spectral rates \(v\ge0\) or \(v\le0\), equivalently commuting PSD/NSD directions;
- pointwise claims at a fixed base unless an interval certificate explicitly checks a whole segment;
- strict total curvature from \(m>1/27\) or \(\min_iC_i>0\), plus single-rate count strictness.

Not proved:

- arbitrary noncommuting PSD/NSD directions;
- all fixed-\(Q\) spectral directions when some \(C_i<0\);
- a global theorem from the six finite rational centers;
- novelty or prior-art uniqueness.

The global blocker stated in `proof_or_blocker.md:177-190` is real and remains INCOMPLETE: if some \(C_i<0\), the count and within-layer Fisher terms may compensate, but no general domination proof is supplied.

## Final layered verdict

- Analytic sufficient refinement \(m>1/27\) and \(\min_iC_i>0\): CORRECT.
- Pair-missing index convention, \(P\) row/column stochastic uses, and \(A=2\sum v_jv_kC_i\): CORRECT.
- One-fifth implication and single-rate boundary strictness: CORRECT.
- Six rational examples and interval certificates: SCOUT / exact sanity, internally CORRECT.
- Full seed/search/global fixed-\(Q\) problem beyond the sufficient conditions: INCOMPLETE.

No critical error was found in the stated sufficient theorem or copied exact certificates.
