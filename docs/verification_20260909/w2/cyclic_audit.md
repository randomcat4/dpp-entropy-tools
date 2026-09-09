# W2 cyclic averaging strictness audit

Verdict: ACCEPTED_SCOPED.

This audit is bound to public PR 34, head `838c20b12907d94a9d6e023cc03f48c3f3b36c5c`, branch
`research/W2-nonconstant-orbit-20260909`, file
`research/W2/nonconstant_orbit/previous_proof.md`.

Frozen mathematical source: [PR34 proof at the reviewed head](https://github.com/randomcat4/dpp-entropy-tools/blob/838c20b12907d94a9d6e023cc03f48c3f3b36c5c/research/W2/nonconstant_orbit/previous_proof.md). This public copy changes only the local-source inventory into the immutable public link. Scope accepted:

For a real measurable symbol `f:T -> [0,1]`, integer `q >= 2`, and
`A_q f(theta)=q^{-1} sum_{r=0}^{q-1} f(theta+r/q)`, the proof establishes

```text
h(A_q f) >= h(f),
h(A_q f)=h(f) iff A_q f=f a.e.,
```

and more quantitatively, for every removed Fourier coefficient
`q` not dividing `k` with

```text
gamma = |hat f(k)|^2 > 0,
```

it establishes

```text
h(A_q f)-h(f) >= gamma^2.
```

Here `gamma^2=|hat f(k)|^4`. This matches the user's requested convention.

## Proof-step audit

1. Finite block decoupling is correct. Lines 370-381 prove that deleting
cross-block kernel entries gives the product of the true block marginals and
that

```text
D(P_K || P_{K^circ}) = H(K^circ)-H(K).
```

The absolute-continuity check on line 378 is sufficient: if a full
configuration has positive `P` mass, then every block marginal appearing in
the product has positive mass.

2. The cyclic average is exactly the block decoupling. Lines 385-401 use the
finite geometric-series identity

```text
hat(A_q f)(k)=1_{q|k} hat f(k)
```

so the finite Toeplitz kernel for `A_q f` is the mod-`q` block-decoupled
kernel of `K_f`. Thus line 401 gives

```text
H_n(A_q f)-H_n(f)=D(P_{f,[1,n]} || P_{A_q f,[1,n]}) >= 0.
```

3. The negative-association input is adequate. Line 27 cites Lyons, Theorem
8.1, for finite Hermitian positive-contraction DPPs. This applies to
`Q=P_{K^circ}` because `K^circ` is again a Hermitian positive contraction.
The proof uses only ordinary negative association for functions of disjoint
coordinate sets, which is within that theorem's scope. I checked this against
Lyons' primary paper; Borcea-Branden-Liggett is also consistent but is not
needed for the proof.

4. The exponential-moment inequality is valid. Lines 409-428 extend pairwise
negative association to a finite product of nonnegative decreasing functions
on disjoint coordinate sets by induction. For a matching edge
`e=(i,j)`, `Z_e=X_i X_j` is increasing, hence
`V_e=exp(t_e Z_e)` is decreasing for `t_e <= 0`. Since the edges are vertex
disjoint, the functions depend on disjoint coordinate sets. This justifies

```text
log E_Q exp(sum_e t_e Z_e)
  <= sum_e log(1-a_e+a_e exp(t_e)).
```

No false independence of the edge variables is used.

5. The variational entropy step is correct. Lines 431-439 use the standard
Gibbs variational inequality

```text
D(P||Q) >= E_P F - log E_Q exp(F)
```

under `P << Q`, already established in the block step. Substituting
`F=sum_e t_e Z_e` and optimizing each scalar `t_e <= 0` gives the Bernoulli
relative entropy term on lines 441-450:

```text
d(p_i p_j-|K_ij|^2 || p_i p_j).
```

The boundary convention on line 453 is sound. If `p_i p_j=0` or `1`, positivity
of `K` or `I-K` forces `K_ij=0`, so the corresponding term is zero by
continuity.

6. The complement-process lower bound is valid. Line 455 correctly uses that
the complement of a finite DPP with kernel `K` has kernel `I-K`. Applying the
same bound to complements replaces `p_i` by `1-p_i` while keeping the
cross-block magnitude `|K_ij|^2`. Because each bound is a lower bound for the
same entropy difference, taking the larger of the two whole matching sums is
legitimate.

7. The matching density is correct. Lines 463-469 decompose `[1,n]` into
chains of step `k` and use alternating pairings. The matching size satisfies

```text
m_n=sum_r floor(L_r/2),    (n-k)/2 <= m_n <= n/2,    m_n/n -> 1/2.
```

The lower bound follows since at most `k` nonempty chains each lose at most one
vertex. If `q` does not divide `k`, every length-`k` edge crosses distinct
mod-`q` blocks, as required for the block-decoupling comparison.

8. The stationary specialization is correct. For every matched length-`k`
edge in the Toeplitz kernel,

```text
p_i=p_j=p=int f,    |K_ij|^2=|c_k|^2=gamma.
```

Lines 472-478 therefore give

```text
H_n(A_q f)-H_n(f)
 >= m_n max{ d(p^2-gamma || p^2),
             d((1-p)^2-gamma || (1-p)^2) }.
```

The first arguments are nonnegative because the two-by-two principal minors
of `K_f` and `I-K_f` are nonnegative.

9. The entropy-rate passage is justified. The proof earlier establishes the
subadditive entropy-rate limit for every stationary symbol, and no derivative
or curvature limit is exchanged. Dividing the finite-window inequality by `n`
and using `m_n/n -> 1/2` gives lines 481-487.

10. The constant in the explicit gap is correct. Lines 490-496 use

```text
d''(r || a)=1/(r(1-r)) >= 4
```

on `(0,1)`, with endpoint continuity. Hence

```text
d(a-gamma || a) >= 2 gamma^2.
```

After the factor `1/2` from matching density, the entropy-rate gap is at least
`gamma^2`. Since `gamma=|hat f(k)|^2`, this is `|hat f(k)|^4`.

11. The equality characterization is complete. Lines 461-462 cover
`p=0` or `p=1`, where `0 <= f <= 1` forces `f` to be a.e. constant. If
`f != A_q f` a.e., then `f-A_q f` is nonzero in `L^2`, so some Fourier
coefficient is nonzero. By line 394, every nonzero coefficient of
`f-A_q f` has index not divisible by `q`; choosing its absolute index gives
the positive `gamma` required by the strict gap. Conversely, if `f=A_q f`
a.e., the Toeplitz kernels and entropy rates are identical.

## Checked hazards

- Non-strict contractions and zero-probability configurations: handled by
finite DPP negative association without a full-support assumption and by
`P << Q` for the variational formula.
- Complex non-even symbols: real-valued `f` gives Hermitian Toeplitz kernels;
the proof only uses `|K_ij|^2`.
- Boundary means `p=0,1`: force constant symbols, so no hidden strict case is
lost.
- Edge overlap: avoided by matching construction; no independence of different
edge statistics under `P` or `Q` is asserted.
- Per-edge max between occupied and vacant tests: not asserted. The proof
takes the max only between two global lower bounds, which is valid.
- Entropy-rate limits: obtained through subadditivity and bounded entropy;
strictness uses fixed `k` before taking `n -> infinity`.

## External primary-source check

- Russell Lyons, "Determinantal Probability Measures",
  arXiv:math/0204325v4, Theorem 8.1:
  https://arxiv.org/pdf/math/0204325
- Julius Borcea, Petter Branden, Thomas M. Liggett,
  "Negative dependence and the geometry of polynomials",
  arXiv:0707.2340:
  https://arxiv.org/abs/0707.2340

Final status: ACCEPTED_SCOPED for the stationary scalar DPP cyclic averaging
strictness theorem and the explicit `gamma^2` gap. This does not certify any
claim about arbitrary entropy concavity along unrelated DPP symbol chords.
