# The entire fixed strong rank-two angle square is midpoint-safe

Status: **PROVED (author proof plus exact finite covering), PENDING_EXTERNAL_REVIEW**. This is a fixed-family theorem obtained after the edge, thinning, and diagonal checkpoints. It is not a theorem for arbitrary rank-two endpoints, and it makes no novelty or priority claim.

Let
\[
 A=\begin{pmatrix}2/5&6/25\\6/25&2/5\end{pmatrix},\qquad
 B=\begin{pmatrix}3/5&9/25\\9/25&3/5\end{pmatrix}.
\]
For arbitrary `c1,c2 in [0,1]`, set `sj=sqrt(1-cj^2)` and
\[
E=(e_1,e_2),\qquad
V=(c_1e_1+s_1e_3,\ c_2e_2+s_2e_4),
\]
\[
K_-=EAE^\top,\qquad K_+=VBV^\top,\qquad
M={K_-+K_+\over2}.
\]
Equivalently, this is the complete rational-angle square
`0<=t1,t2<=1`, with `cj=(1-tj^2)/(1+tj^2)`. The only midpoint used is the true arithmetic midpoint in `K`-space.

Both endpoints have rank two and fixed nonzero eigenvalues
`(4/25,16/25)` and `(6/25,24/25)`. In the open square their ranges have zero intersection and `rank M=4`; on a punctured coordinate edge they intersect in one dimension and `rank M=3`; at `(c1,c2)=(1,1)` they have the same range and `rank M=2`. Triple and quadruple midpoint events are retained in all nondegenerate cases.

Define
\[
G(c_1,c_2)=H(M)-{H(K_-)+H(K_+)\over2},
\]
where `H` is the Shannon entropy of all sixteen complete configurations.

## Theorem

For every `c1,c2 in [0,1]`,
\[
\boxed{G(c_1,c_2)>{1\over100}.} \tag{1}
\]
Hence this entire two-parameter family of moving, generally noncommuting rank-two endpoint pairs is strictly midpoint-safe. This includes the one-dimensional-intersection and zero-intersection geometries, without a small-angle or small-intensity assumption.

## 1. Full-event regularization, with both rare-event faces retained

For a complete configuration `S`, put
\[
m_1(S)=1_{\{3\in S\}},\qquad m_2(S)=1_{\{4\in S\}}.
\]
A direct signed-determinant expansion gives the exact factorization
\[
p_M(S)=(1-c_1^2)^{m_1(S)}(1-c_2^2)^{m_2(S)}q_S(c_1,c_2), \tag{2}
\]
where all sixteen `q_S` are rational polynomials. They are listed in the certificate and regenerated from the determinant by the checker; no event is supplied from a fitted formula.

The two bottom inclusion probabilities are exact:
\[
\sum_Sm_1(S)p_M(S)={3\over10}(1-c_1^2),\qquad
\sum_Sm_2(S)p_M(S)={3\over10}(1-c_2^2). \tag{3}
\]
The plus endpoint is the logical two-coordinate `B` process followed by independent physical marking. Therefore
\[
H(K_+)=H(B)+{3\over5}h(1-c_1^2)+{3\over5}h(1-c_2^2), \tag{4}
\]
while `H(K_-)=H(A)`.

Substituting (2)--(4), both potentially singular rare-event logarithms cancel **exactly**, leaving the regular identity
\[
\boxed{
G=-\sum_{S\subseteq[4]}p_M(S)\log q_S
 +{3\over10}c_1^2\log(c_1^2)
 +{3\over10}c_2^2\log(c_2^2)
 -{H(A)+H(B)\over2}.} \tag{5}
\]
As usual `0 log 0=0`. Formula (5) is an identity for the complete event law, not an asymptotic truncation. In particular, configurations containing both moving bottom coordinates occur in the first sum and carry the exact product `(1-c1^2)(1-c2^2)`.

For reference, the regular factors are
\[
\begin{aligned}
q_\varnothing&=(1152c_1^2c_2^2-33027c_1^2-33750c_1c_2-33027c_2^2+223652)/781250,\\
q_1&=-(10152c_1^2c_2^2-184527c_1^2-33750c_1c_2+4848c_2^2-62348)/781250,\\
q_2&=q_1(c_2,c_1),\\
q_{12}&=(64152c_1^2c_2^2+42723c_1^2-33750c_1c_2+42723c_2^2+9152)/781250,\\
q_3&=3(39491-2616c_2^2)/781250,\\
q_{13}&=3(11009-384c_2^2)/781250,\\
q_{23}&=3(14616c_2^2+11009)/781250,\\
q_{123}&=12(423c_2^2+202)/390625,
\end{aligned} \tag{6}
\]
with the four corresponding `4`-event factors obtained by exchanging indices `1<->2`, `3<->4`, and
\[
q_{34}=14076/390625,\quad
q_{134}=q_{234}=3924/390625,\quad
q_{1234}=576/390625. \tag{7}
\]
The machine record contains the unambiguous set-by-set dictionary.

## 2. Rigorous two-dimensional lower cover

Partition the physical parameter square into the 4096 closed rational boxes
\[
[i/64,(i+1)/64]\times[j/64,(j+1)/64]. \tag{8}
\]
For each complete atom and each regular factor, the checker expands the exact polynomial in nonnegative variables `c1,c2`. Every monomial is bounded at the rational box endpoints with sign-aware rational interval addition. Since `K_-`, `K_+`, and their midpoint are legal throughout, each complete atom is nonnegative; a negative algebraic interval lower endpoint may therefore safely be replaced by zero, never by a positive floor.

On every box the independently computed regular-factor enclosure satisfies
\[
0<{576\over390625}\le q_S
\le {558671015947\over1638400000000}<1. \tag{9}
\]
Hence `-p log q` is increasing in `p>=0` and decreasing in `q`, and its lower bound uses only the atom lower endpoint and regular-factor upper endpoint.

For
\[
f(c)=c^2\log(c^2),
\]
the checker proves `f` decreases on `[0,3/5]` and increases on `[61/100,1]` using outward logarithm bounds:
\[
\log(9/25)+1<-0.021651247531981366411028,
\]
\[
\log(3721/10000)+1>0.011407356370439761430812.
\]
A box intersecting the narrow remaining strip uses the elementary global bound
\[
f(c)\ge-1/e>-3/8, \tag{10}
\]
because `e>1+1+1/2+1/6=8/3`.

Every logarithm of a rational endpoint is enclosed by
\[
\log y=k\log2+2\sum_{r=0}^{31}{z^{2r+1}\over2r+1}+R,
\qquad
0\le R\le {2z^{65}\over65(1-z^2)},\quad0\le z\le1/3. \tag{11}
\]
All operations after (11) are exact rational interval operations.

All 4096 lower bounds from (5) are strictly positive. The weakest is the box
`[63/64,1]^2`, where
\[
G>0.012067200390564330>{1\over100}. \tag{12}
\]
The checker asserts the simple rational lower bound `1/100` directly. The compact certificate stores the minimum in every one of the 64 rows and the minimizing column; all row minima are positive and all occur in the final column. The full box loop, not that observed monotonic pattern, is the proof.

## 3. Strict-kernel lift

The accepted independent-bit-flip map
\[
K^\varepsilon=\varepsilon I+(1-2\varepsilon)K
\]
preserves the actual arithmetic midpoint. At `epsilon=1/100000`, the exact finite-alphabet continuity calculation gives
\[
2\omega_4(\varepsilon)<0.001106757502899.
\]
Thus every member of the square has the strict-interior bound
\[
G_\varepsilon>{1\over100}-0.001106758
>0.008893242. \tag{13}
\]
This uses the same `epsilon` for both endpoints and the midpoint. It is not a nonlinear frame path or an arbitrary-large lift claim.

## 4. Execution and scope

Run

```sh
python research/N4/I05_30_20260910/certify_full_square.py
```

The author run used Python 3.13.5 and SymPy 1.14.0 and completed the fixed 4096-box certificate in about 33 seconds. A harmless unrelated spreadsheet-runtime warm-up warning was printed by the surrounding environment after the mathematical process had already exited zero; the script itself imports no spreadsheet package. The stored result is `full_square_certificate.json`. This is an author execution, not external arithmetic review.

The theorem supersedes the earlier small-angle restriction **only for this frozen `A,B` family**. The full-edge and equal-angle files remain useful independent derivations and cross-check the most degenerate faces. Nothing here proves the sign for arbitrary `A,B`, for a general canonical pair with unequal diagonal data, for dense spectral ranges outside paired coordinate planes, or for the strong-correlated multiring line. The unrestricted moving-rank-two question remains INCOMPLETE.
