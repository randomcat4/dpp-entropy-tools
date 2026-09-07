# Finite block entropy-gap transfer: definition contract audit

Status: prerequisite audit only. No theorem, proof, implementation, entropy-gap claim, real-kernel claim, or finite-to-rate transfer is certified by this note.

This audit concerns the selected T2 target only: a finite block entropy-gap transfer tool for determinantal point processes. It does not address the alternative T2 targets except where they create hazards for this tool.

## 1. Core object contract

The tool must work with a finite ground set `E = [n]` and a fixed partition

```text
Pi = {I_1, ..., I_m}.
```

A kernel is admissible only when:

1. `K` is an `n x n` Hermitian matrix.
2. `0 <= K <= I` in Loewner order.
3. The DPP is the marginal-kernel DPP defined by

```text
P(A subset X) = det K_A
```

for every `A subset [n]`.

The exact atom probabilities used in entropy are

```text
p_K(S) = P(X = S)
       = sum_{T: S subset T subset [n]} (-1)^{|T|-|S|} det K_T.
```

The entropy is the full-subset Shannon entropy

```text
H(K) = - sum_{S subset [n]} p_K(S) log p_K(S),
```

with natural logarithms and the convention `0 log 0 = 0`. This is not `tr h(K)` and is not the entropy of the independent Bernoulli eigenvalue sampling stage.

For the partition `Pi`, define

```text
B = blockdiag_Pi(K)
```

by keeping the within-block principal submatrices and zeroing all off-block entries. If `K` is feasible, then `B` is feasible. The DPP with kernel `B` is the product of the DPPs on the blocks with kernels `K_{I_j}`.

The comparison between `H(K)` and `H(B)` has an exact information-theoretic meaning:

```text
H(B) = sum_j H(K_{I_j}),
H(B) - H(K) = I_Pi(X_{I_1}; ...; X_{I_m}) >= 0.
```

Any proof that treats `H(K) - H(B)` as an unsigned perturbation error is using a weaker and potentially sign-confusing version of the available fact. The exact identity above should be part of the tool contract or explicitly replaced by a stronger proved estimate.

## 2. Jensen gap convention

The tool must freeze one sign convention. Recommended:

```text
K_theta = (1 - theta) K_0 + theta K_1,  0 < theta < 1,
J_theta(K_0, K_1)
  = H(K_theta) - (1 - theta) H(K_0) - theta H(K_1).
```

Under this convention:

1. `J_theta >= 0` is the sign predicted by concavity.
2. `J_theta < 0` is a concavity violation.

If the author instead uses the convexity-defect convention

```text
G_theta = (1 - theta) H(K_0) + theta H(K_1) - H(K_theta),
```

then all signs in the transfer statement must be reversed. The artifact must not use both conventions without a conversion line.

For `B_i = blockdiag_Pi(K_i)` and `B_theta = blockdiag_Pi(K_theta)`, blockdiag linearity gives

```text
B_theta = (1 - theta) B_0 + theta B_1.
```

Define the block mutual information losses

```text
M_i     = H(B_i)     - H(K_i)     >= 0,
M_theta = H(B_theta) - H(K_theta) >= 0.
```

Then the exact transfer identity is

```text
J_theta(K_0, K_1)
  = J_theta(B_0, B_1) - M_theta + (1 - theta) M_0 + theta M_1.
```

For midpoint gaps, the endpoint coefficients are exactly `1/2` and `1/2`; the midpoint coefficient is exactly `-1`.

Minimum sign obligations:

1. To transfer a negative block Jensen gap `J_theta(B_0,B_1) <= -gamma`, it is enough, and directionally sharp, to prove

```text
(1 - theta) M_0 + theta M_1 - M_theta < gamma.
```

A cruder sufficient condition is `(1 - theta) M_0 + theta M_1 < gamma`, since `M_theta >= 0`.

2. To transfer a positive block Jensen gap `J_theta(B_0,B_1) >= gamma`, it is enough to prove

```text
M_theta - (1 - theta) M_0 - theta M_1 < gamma.
```

A cruder sufficient condition is `M_theta < gamma`.

3. If only absolute entropy errors `|H(K_i)-H(B_i)| <= eps_i` are proved, then the fallback bound is

```text
|J_theta(K_0,K_1) - J_theta(B_0,B_1)|
  <= eps_theta + (1 - theta) eps_0 + theta eps_1.
```

For midpoint and uniform `eps`, this gives `2 eps`, but it loses the useful one-sided information above.

## 3. Feasibility checks

The feasible set of marginal kernels is convex. Thus if `K_0` and `K_1` are both Hermitian and satisfy `0 <= K_i <= I`, then `K_theta` is feasible. This does not remove the need to prove feasibility of the proposed endpoints.

If the construction starts from block kernels `B_i` and adds off-block Hermitian perturbations `E_i`,

```text
K_i = B_i + E_i,
```

then feasibility of `B_i` is not enough. The proof must include one of the following:

1. A strict interior margin:

```text
rho I <= B_i <= (1 - rho) I
```

and a norm bound such as

```text
||E_i||_op <= rho
```

with strict inequality if the later argument needs interiority.

2. A boundary-compatible argument proving both `B_i + E_i >= 0` and `I - B_i - E_i >= 0`, usually by Schur complements or by showing the perturbation annihilates the boundary eigenspaces.

Boundary hazard: if `B` has a zero eigenvector and `E` couples that vector to another block, then `B + tE` can fail to be positive semidefinite for every nonzero `t`. If `B` has a one eigenvector and `E` couples it, then `I - B - tE` can fail similarly. Endpoint and midpoint feasibility must not be inferred from small entrywise coupling alone.

If the tool is phrased around a center and direction,

```text
K(t) = K_* + t V,
```

the permitted interval of `t` must be part of the input/output. A Hessian calculation at `t=0` does not certify a finite Jensen gap unless the whole segment used by the gap stays feasible.

## 4. Entropy regularity and perturbation obligations

The entropy `H(K)` is continuous on the compact feasible set, but derivative-based estimates require more.

For first and second derivatives, the proof must guarantee

```text
p_K(S) > 0 for every S subset [n]
```

throughout the segment where derivatives are used, and it must provide a quantitative lower bound if constants are claimed. A spectral condition such as

```text
rho I <= K <= (1 - rho) I
```

is qualitative interiority, but the resulting lower bound on all exact atom probabilities can degrade exponentially in `n`. If the proof uses this route, it must state the actual bound and carry the dimension dependence.

One crude route is via the `L`-ensemble representation `L = K(I-K)^{-1}` under strict interiority. The resulting atom lower bounds are exponential in `n`; this is acceptable only if the final error-vs-gap inequality still closes.

If avoiding atom lower bounds, the proof can instead bound total variation between the two exact laws and then use a finite-alphabet entropy continuity inequality. This must use the alphabet size

```text
N = 2^n,
```

so an `n` factor or worse will appear in the entropy error term. Dimension-free wording is not allowed unless a separate dimension-free argument is actually proved.

For an affine path `K(t) = K_* + tV` inside the positive atom region, the Hessian being used is the Hessian of the full atom entropy:

```text
D H_K[V] =
  - sum_S (log p_K(S) + 1) D p_K(S)[V],

D^2 H_K[V,V] =
  - sum_S (D p_K(S)[V])^2 / p_K(S)
  - sum_S (log p_K(S) + 1) D^2 p_K(S)[V,V].
```

It is not the spectral Hessian of `tr h(K)`. Any Hessian-based certificate must specify real coordinates for Hermitian matrices, including how complex off-diagonal entries are represented.

For a symmetric midpoint gap along `f(t)=H(K_*+tV)`,

```text
J_s = f(0) - (f(s) + f(-s))/2
    = -1/2 int_{-s}^{s} (s - |u|) f''(u) du.
```

Thus, under the recommended Jensen sign, a negative second derivative supports a positive concavity gap locally, while a positive second derivative supports a negative concavity violation locally. A local Hessian sign at one point is not a finite gap certificate without a uniform remainder or an interval sign bound.

## 5. Dimension, norm, and scale contract

The transfer theorem must state all scales in one place:

```text
n                  finite ground-set size
Pi                 block partition and block sizes
theta              interpolation parameter
gamma              signed target block gap magnitude
rho                spectral or atom interiority margin, if used
eta                off-block perturbation size
norm               operator, Frobenius, entrywise, or another named norm
C(...)             explicit perturbation or continuity constant
```

The final conclusion must include an inequality of the form

```text
error(n, Pi, theta, rho, eta, norm) < gamma
```

with the sign convention from Section 2. A statement of the form "take the perturbation sufficiently small" is only acceptable for a fixed finite instance; it is not enough for any family, rate, or uniform-scale transfer.

If the tool is meant to work over a sequence of block systems, it must specify which quantities are uniform in the sequence. In particular:

1. `rho_n` approaching zero can destroy derivative estimates.
2. `gamma_n` can be too small compared with entropy continuity losses.
3. `eta_n` chosen after seeing `n` does not give a fixed-scale construction unless that dependence is part of the theorem.
4. A low-rank boundary perturbation does not by itself imply an entropy Hessian area law.

All determinant perturbation bounds must be translated from inclusion probabilities to exact atom probabilities before they are used in `H(K)`. The Mobius inversion from inclusion events to atoms can amplify constants, so it must be included in the dimension accounting.

## 6. Finite windows versus entropy rate

This audit is for a finite block tool. Any later stationary or rate claim needs an additional contract.

For a finite direct sum of repeated blocks, entropy is additive. After normalizing by total length, a fixed `O(1)` finite gap may vanish. A rate-level claim must prove that the gap scales linearly with the number of sites, or otherwise state the limiting normalized gap.

For a process on `Z` or a large interval, the artifact must distinguish:

```text
H(X_{[1,N]})        finite-window entropy,
lim_N H(X_{[1,N]})/N   entropy rate, when the limit exists.
```

It must also state the order of limits among block size, number of blocks, perturbation strength, and window length. Strong correlations that move with the block size may disappear from every fixed window in the limit.

A block-valued periodic process is not automatically a scalar stationary process. Randomly shifting a periodic construction produces a mixture, and a mixture of DPPs is not automatically a DPP. Any scalar stationary transfer must construct the scalar kernel and recheck the DPP law and entropy quantities directly.

## 7. Real and complex kernel contract

No automatic realification is allowed.

The finite DPP definition here permits Hermitian complex kernels. A complex Hermitian counterexample or gap does not automatically imply a real symmetric one.

Acceptable real-kernel routes include:

1. A diagonal-unitary gauge proof: find a diagonal unitary `D` such that `DKD^*` is real symmetric. This preserves all principal minors and hence the DPP law, but it exists only under phase-cycle constraints that must be checked.
2. A separately constructed real symmetric kernel with its own feasibility, atom probabilities, entropy, and gap estimates.
3. A proved embedding theorem whose output law and entropy relation are explicitly stated.

The standard `2n x 2n` real block representation of a complex matrix changes the ground set and does not preserve the full-subset entropy on `[n]`. It cannot be used as a certification shortcut.

## 8. Fast sanity checks

A minimum audit suite for any proposed statement should include the following hand-checkable cases.

Two singleton blocks:

```text
K = [ a  z  ]
    [ z* b  ],
q = |z|^2.
```

The atom probabilities are

```text
p_11 = ab - q,
p_10 = a(1-b) + q,
p_01 = (1-a)b + q,
p_00 = (1-a)(1-b) - q.
```

Feasibility requires

```text
q <= ab,
q <= (1-a)(1-b).
```

At `q=0`, the blocks are independent. The first derivative of entropy with respect to `q` is zero, and the entropy loss `H(B)-H(K)` begins quadratically in `q`, hence fourth order in `|z|`, with positive leading coefficient when all four atom probabilities are positive. This catches wrong first-order perturbation coefficients and wrong signs.

Boundary perturbation:

```text
B = diag(0, a),  E_12 != 0
```

generically violates `B+tE >= 0` for every nonzero `t`. Similarly, a one eigenvalue creates the dual obstruction for `I-K`.

Rate normalization:

A single finite bad block plus many unrelated sites can keep an unnormalized finite gap while its per-site contribution goes to zero. Any rate claim must fail this test unless it includes repeated density of the gap.

Realification:

Apply the proposed realification to the two-by-two complex case with a nontrivial phase. If the ground set doubles or atom probabilities change, the route does not certify a real symmetric DPP on the original finite set.

## 9. Minimum proof obligations before certification

Before a final verifier can certify a finite block entropy-gap transfer theorem, the main artifact must contain:

1. The exact finite DPP atom definition and full-subset entropy definition.
2. The partition and blockdiag map.
3. A frozen Jensen-gap sign convention.
4. Feasibility proofs for all endpoints and interpolation points.
5. A statement of whether the kernels are on the boundary or in a quantified interior.
6. The exact identity relating full and block Jensen gaps through block mutual informations, or a stronger proved substitute.
7. Perturbation bounds with correct midpoint and endpoint coefficients.
8. Explicit dimension, block-size, norm, margin, and gap dependencies.
9. A derivative or continuity argument that acts on exact atom probabilities, not on eigenvalue entropy.
10. A finite-scale conclusion whose error is strictly smaller than the target gap in the required sign.
11. A clear statement that no finite-window result is being promoted to an entropy-rate result unless a separate rate theorem is proved.
12. A clear statement that complex Hermitian results are not being promoted to real symmetric results unless a separate gauge, construction, or embedding proof is supplied.
13. One applicable example and one boundary-touching example, as required by the T2 prompt.
14. A provenance note separating author, proof, computation, and fresh-context verification.

This audit does not certify that any of these obligations have been met. It is a checklist and contract for the later frozen theorem and independent verification.

