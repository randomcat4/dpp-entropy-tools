# T1 prior-art conditions and risk audit

Status: bounded prior-art and condition audit. This file records what the cited literature appears to support, what it does not support, and which T1 claims still need independent proof.

## Sources checked

- Lyons, "Determinantal probability measures" (Publ. Math. IHES, 2003), https://www.numdam.org/item/PMIHES_2003__98__167_0/.
  Supports the finite/infinite determinantal probability framework and the positive-contraction viewpoint for marginal kernels.
- Hough, Krishnapur, Peres, and Virag, "Determinantal processes and independence" (Probab. Surveys, 2006), https://arxiv.org/abs/math/0503110.
  Supports the spectral Bernoulli/projection-process decomposition background for DPPs.
- Lyons, "Determinantal probability: basic properties and conjectures" (2014), https://arxiv.org/abs/1406.2707.
  Supports standard DPP identities, conditional/closure properties, and terminology used in the repo README.
- Kulesza and Taskar, "Determinantal Point Processes for Machine Learning" (FnT ML, 2012), https://arxiv.org/abs/1207.6083.
  Standard accessible reference for finite `K`-DPP and `L`-ensemble formulas; useful for checking atom and conditioning identities. This is a survey/monograph rather than the original source.
- Lyons and Steif, "Stationary determinantal processes: phase multiplicity, Bernoullicity, entropy, and domination" (Duke Math. J., 2003), https://arxiv.org/abs/math/0204324.
  Supports the distinction between stationary DPP process entropy/rate questions and fixed finite-window entropy.
- Hino and Yano, "Duality induced by an embedding structure of determinantal point process" (arXiv 2024), https://arxiv.org/abs/2404.11024; journal title "An embedding structure of determinantal point process", https://link.springer.com/article/10.1007/s41884-024-00156-x.
  Directly relevant to information-geometric prior art. They embed DPPs in log-linear models, study Fisher information/e-curvature, and note non-exponential-family behavior for `m>=3`.
- Brunel, Moitra, Rigollet, and Urschel, "Maximum Likelihood Estimation of Determinantal Point Processes" (COLT 2017), https://proceedings.mlr.press/v65/brunel17a.html.
  Relevant for likelihood/Fisher/identifiability geometry of finite DPPs; not a Shannon-entropy curvature theorem.
- Shannon, "A Mathematical Theory of Communication" (Bell System Technical Journal, 1948), https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf.
  Primary source for the finite entropy functional.
- Amari and Nagaoka, "Methods of Information Geometry" (AMS/Oxford, 2000).
  Standard source for exponential-family dual coordinates, Fisher metric, and Hessian/Legendre structure.
- Efron, "Defining the curvature of a statistical problem" (Annals of Statistics, 1975), https://doi.org/10.1214/aos/1176343282.
  Primary source for statistical curvature in curved exponential-family settings.

## Condition matrix

| Tool or fact | Accurate conditions | What it supports | What it does not support |
| --- | --- | --- | --- |
| Marginal-kernel DPP | finite `E`, Hermitian `0<=K<=I` | inclusion probabilities `Pr[A subset Y]=det(K_A)` | exact atoms are not simply `det(K_S)` except for inclusion/full-set events |
| Exact atom formula | same finite DPP; or `0<K<I` for `L=K(I-K)^(-1)` | `p_S` by Möbius inversion or `L`-ensemble | direct boundary differentiation through `log p_S` |
| Full atom support | finite DPP with `0<=K<=I` | `p_S>0` for all `S` iff `0<K<I` | any boundary claim with zero atoms |
| Interior affine path | `0<K0<I`, `D=D*` | local feasibility for small `|t|` | feasibility for arbitrary boundary directions |
| Boundary affine path | two-sided path requires action only on non-boundary spectral subspace; one-sided path needs tangent-cone checks | prevents illegal perturbations at eigenvalues `0` or `1` | entropy asymptotics without support/leading-order analysis |
| Entropy Hessian on simplex | fixed positive support; smooth probability curve | `H''=-sum (p')^2/p - sum p'' log p` | sign of `H(K+tD)` for nonlinear DPP maps |
| Exponential-family Fisher identity | canonical exponential family, fixed support, natural coordinates | Hessian of log partition equals covariance/Fisher information | Shannon entropy curvature in marginal-kernel affine coordinates |
| Curved exponential-family geometry | smooth embedding into a full exponential family with rank/identifiability conditions | Fisher metric, statistical curvature, local likelihood geometry | automatic concavity/convexity of DPP Shannon entropy |
| Hino-Yano DPP information geometry | finite DPP in their log-linear/exponential-family embedding; mostly real-valued parameterization as stated there | strong prior art for DPP Fisher geometry and curvature language | complex Hermitian pure-imaginary affine `K`-directions, or entropy sign criteria, without extra translation |
| Lyons-Steif entropy | stationary determinantal process setting | process entropy/rate context | fixed-window curvature does not imply entropy-rate curvature without an interchange theorem |

## Identity versus structural content

The following are identities or basic translations:

- exact atom probabilities from inclusion probabilities;
- the `L`-ensemble atom formula on `0<K<I`;
- `p_S>0` for all atoms iff `0<K<I`;
- the open-simplex entropy second derivative decomposition;
- evenness of `p_S(t)` at a real center in a pure-imaginary Hermitian direction;
- `p'_S(0)=0` under that real/pure-imaginary symmetry.

The following would be structural and still require proof:

- a checkable sufficient condition on `(K0,D)` implying a sign for `H''(0)`;
- a criterion that avoids summing all `2^n` atoms while still giving new sign information;
- a boundary curvature rule that includes zero atoms with correct leading terms;
- a theorem transferring finite-window curvature to stationary entropy rate;
- an information-geometric theorem showing that an existing Fisher/curved-family result implies the desired Shannon-entropy curvature statement in the repo's coordinates.

## Domain risk list

1. Exact-event/inclusion-event confusion. `det(K_S)` is an inclusion probability, not the atom `Pr[Y=S]` unless `S=E` or extra conditioning is present.
2. Coordinate confusion. DPP literature moves between `K`, `L`, projection kernels, quality/diversity decompositions, and log-linear parameters. Curvature signs are not invariant under arbitrary nonlinear reparameterization.
3. Boundary misuse. The term `-p log p` is continuous at `p=0`, but its derivatives are not obtained by plugging `p=0` into the interior formula.
4. Illegal boundary directions. A Hermitian `D` is not enough at boundary kernels; feasibility must be checked against both `K>=0` and `I-K>=0`.
5. Pure-imaginary overclaim. Real-center conjugation symmetry kills first derivatives but does not fix second-derivative signs.
6. Fisher-versus-entropy mismatch. Fisher information controls the negative square term for the induced probability curve; the DPP atom acceleration term can dominate.
7. Exponential-family overclaim. Existing exponential-family Hessian identities apply in natural/expectation coordinates under fixed-support assumptions. T1's affine marginal-kernel path is a different coordinate choice.
8. Identifiability/gauge issues. DPP parameterizations can have sign or rank non-identifiability. A Hessian degeneracy may reflect parameterization rather than entropy behavior.
9. Complex Hermitian scope. Several information-geometry references are stated for real DPP parameterizations. Extension to complex Hermitian kernels should be marked unconfirmed unless proved.
10. Entropy rate slippage. Fixed `n` entropy and stationary entropy rate are different objects; limit and differentiation cannot be interchanged by notation.
11. Log base normalization. Curvature constants depend on whether logs are natural or base two, though signs do not.
12. Finite computation scope. Small `n` symbolic or interval checks can find examples and test formulas, but cannot certify a universal theorem without a proof or formal certificate.

## Literature implications for T1

The information-geometry literature is relevant but does not appear to close T1 by itself. Hino-Yano gives a direct warning: finite DPPs have a rich information-geometric embedding and are not simply a full exponential family in the ordinary sense once the ground set has at least three elements. That means a T1 proof cannot cite "entropy Hessian of exponential families" as a black box unless it first proves the DPP entropy objective and affine `K`-path match the coordinates and functional covered by the theorem.

The strongest reusable facts from classical information geometry are local differential identities: Fisher information as a covariance/Hessian of log partition, Legendre duality between natural and expectation coordinates, and curvature terms for embedded families. These can organize the calculation, but the sign problem remains in the second fundamental/acceleration part of the atom map.

For finite-window DPP entropy, the safe route is to keep all statements finite-dimensional until a separate stationary-process lemma is proved. Lyons-Steif and later stationary DPP entropy work belong to the entropy-rate side; they are not automatic support for a fixed-window Hessian criterion, and fixed-window experiments are not automatic support for entropy-rate claims.

## UNCONFIRMED placeholders

- `UNCONFIRMED`: I did not find, in this bounded pass, a primary theorem giving a nontrivial global sign criterion for Shannon entropy curvature of all finite Hermitian DPPs along affine marginal-kernel paths.
- `UNCONFIRMED`: I did not verify a source that transfers Hino-Yano's real/log-linear DPP Fisher geometry directly to complex Hermitian pure-imaginary affine directions.
- `UNCONFIRMED`: I did not verify a boundary theorem classifying all possible leading orders of `p_S(K0+tD)` for one-sided feasible DPP paths.
- `UNCONFIRMED`: I did not verify an interchange theorem allowing `d^2/dt^2 lim_n H_n(t)/n = lim_n d^2H_n(t)/dt^2 / n` for the stationary kernels relevant to this project.
- `UNCONFIRMED`: I did not check private or sibling-route drafts, by design. Any candidate proof using this audit still needs a fresh proof-verification context.

## Audit verdict on prior art

Current status: `INCOMPLETE` for any T1 structural criterion.

The definitions and differential setup are sound under the interior finite assumptions stated in `definitions.md`. The entropy Hessian decomposition and pure-imaginary first-order cancellation are useful simplifications, but they are not novel criteria. Existing DPP information geometry is strong prior art for language and tools, and it raises conditions that a T1 proof must satisfy; it does not, from this audit alone, certify the target Shannon-entropy curvature sign problem.
