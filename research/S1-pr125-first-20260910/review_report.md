# Independent FIRST review report for PR125

## Verdict

**ACCEPTED_SCOPED** at exact author head
`87897b307818e9eab84ad465b24b4aeb037a1dc1`.

The strict-`L^infinity` classical configuration-KL upper bound, its mixed
Toeplitz thermodynamic limit, and the half-period central second-difference
consequences are supported by the submitted analytic proof.

## 1. Complete occupation measurement and data-processing direction — pass

For every finite strict contraction `K`, a finite gauge-invariant quasi-free
fermionic state with one-particle occupation covariance `K` exists.  Its joint
occupation moments are

`E prod_(i in S) N_i = det K_S`.

These are precisely the DPP inclusion probabilities.  Boolean Möbius
inversion uniquely recovers every occupied/vacant atom, so measurement in the
fixed common occupation basis produces the complete DPP law, not merely a
selected-event law.  The projective measurement is independent of `K`.

Quantum relative entropy is monotone under this measurement channel.  With
the numerator and denominator kept in the same order, the resulting direction
is

`D(P_A||P_B) <= D_q(rho_A||rho_B)`.

The quantum quantity is used only as an upper bound.  No quantum entropy is
identified with the classical configuration entropy.

## 2. Noncommuting quasi-free KL formula — pass

For finite `0<A,B<I`, the density matrix of a gauge-invariant quasi-free state
can be written through second quantization of the one-particle logit.  Taking
the expectation of the difference of the two density-matrix logarithms gives

`D_q(rho_A||rho_B)`

`=Tr[A(log A-log B)+(I-A)(log(I-A)-log(I-B))]`.

This derivation uses linearity of second quantization and the trace identity
for its expectation; it does not require `[A,B]=0`.

For

`Phi(X)=Tr[X log X+(I-X)log(I-X)]`,

the Fréchet derivative is

`D Phi(B)[V]=Tr[(log B-log(I-B))V]`.

Expanding the Bregman difference reproduces the quasi-free formula exactly.
After diagonalizing only the current segment point `X`, the divided-difference
Hessian coefficients of the scalar function are bounded by
`max_[a,1-a] 1/[x(1-x)]`.  Thus, without diagonalizing `A` and `B` together,

`0 <= D^2 Phi(X)[V,V] <= ||V||_HS^2/[a(1-a)]`.

Taylor's integral remainder supplies the factor `1/2`:

`D_q(rho_A||rho_B) <= ||A-B||_HS^2/[2a(1-a)]`.

If both endpoints lie between `aI` and `(1-a)I`, so does their whole affine
segment; the spectral-strip quantifier is therefore satisfied.

## 3. Toeplitz Hilbert--Schmidt normalization — pass

For `T_n(g)_(ij)=g_hat(i-j)`, direct counting of each diagonal gives

`n^(-1)||T_n(g)||_HS^2`

`=sum_(|j|<n)(1-|j|/n)|g_hat(j)|^2 <= ||g||_2^2`.

With `a=delta/2`, the quasi-free Hessian estimate therefore gives the stated
finite-window bound

`n^(-1)D(P_(n,t)||P_(n,0))`

`<=t^2||g||_2^2/[delta(1-delta/2)]`.

This is uniform in `n`; no finite-window sign is extrapolated.

## 4. Mixed bounded-symbol Toeplitz trace lemma — pass

For polynomial `F`, the required limit reduces to fixed powers

`n^(-1)Tr[T_n(u)T_n(v)^r] -> integral u v^r`.

It is exact up to `O(1/n)` for trigonometric-polynomial symbols because only
a fixed number of boundary anchors can leave the finite Toeplitz interval.
For general bounded symbols, bounded Fejér means converge in `L^2` while
preserving a common `L^infinity` bound.  In the telescoping difference, one
symbol error is placed in Hilbert--Schmidt norm and every remaining factor in
operator norm.  Cauchy--Schwarz for the trace gives a uniform error bounded by

`C_r(||u-u_M||_2+||v-v_M||_2)`.

Taking `n->infinity` at fixed `M` and only then `M->infinity` proves the
polynomial case.  For continuous `F`, uniform polynomial approximation on the
fixed spectral interval controls both the normalized matrix trace and scalar
integral.  At no point are `T_n(u)` and `T_n(v)` asserted to commute, and no
Fourier `ell^1` assumption appears.

Applying the lemma to the four terms of finite quasi-free KL yields

`lim n^(-1)D_q(rho_(T_n(f))||rho_(T_n(c)))`

`=integral d_Ber(f||c)`.

Combining this exact quantum limit with finite data processing proves the
general classical `limsup` inequality.

## 5. Entropy-rate identification and parity symmetry — pass

For the half-period path, even and odd coordinate restrictions are fixed in
`t`; at zero the cross-parity kernel block vanishes.  Therefore the zero law
is the product of the actual two parity marginals, and the finite complete-law
identity is

`D(P_(n,t)||P_(n,0))=H_n(c)-H_n(c+t g)`.

Both normalized finite entropies converge to their stationary entropy rates,
so the normalized classical KL itself has the limit

`J(t)=h(c)-h(c+t g)>=0`.

The diagonal gauge `U_j=(-1)^j` conjugates `K_(n,t)` to `K_(n,-t)` and commutes
with every occupied/vacant diagonal mask.  Hence every complete atom, not just
every inclusion probability, agrees at `t` and `-t`.  Thus `J(-t)=J(t)` and
the central second difference is exactly `-2J(t)`.

## 6. Sharp scalar KL and the center modulus — pass

Applying the general KL-density bound with `f=c+t g` gives

`0<=J(t)<=integral d_Ber(c+t g||c)`.

The exact evenness also permits averaging the `+t` and `-t` upper bounds.  On
the fixed strict strip, scalar Bernoulli KL has a uniform Taylor expansion;
boundedness of `g` supplies a common integrable remainder.  Dividing the
symmetric average by `t^2` and using dominated convergence gives

`limsup_(t->0) J(t)/t^2`

`<= (1/2) integral g^2/[c(1-c)]`.

This is only a center modulus.  It neither constructs nor assumes `h''(0)`.

The accepted PR53 matching floor is imported solely to provide the stated
quartic lower bound for a selected nonzero odd Fourier coefficient.  No
regularity or local-radius conclusion from PR53, PR113, or PR117 is imported.

## 7. Reverse-audit supplements — pass within their stated role

The displayed sign-cosine family has the required half-period parity, a
strict spectral margin, a nonzero first odd coefficient, and harmonic-size
Fourier tails, so it lies genuinely outside `A_0`.

The absolute-loop obstruction is also correct.  For a symmetric nonnegative
finite magnitude sequence, the even closed-loop coefficient is the
`L^(2r)` norm power of its trigonometric polynomial.  A geometric bound
uniform in length and truncation therefore bounds every polynomial in
`L^infinity`; convolution with the positive Fejér kernel and monotone
convergence then forces summability of the magnitudes.  This blocks that
particular all-absolute closed-walk method outside `A_0`, not the entropy
statement itself.

The cited HMM analyticity theorems require an actual hidden Markov model plus
their positivity, mixing, analytic-parameter, and filter-stability
hypotheses.  PR125 correctly does not apply them to a Toeplitz DPP without
first proving such a representation and its hypotheses.

## Contract ledger

| Unit | Result | Reason |
|---|---|---|
| Complete parity law | PASS | fixed marginals, product at zero, full atoms even |
| Occupation measurement | PASS | inclusion moments plus Möbius inversion identify all atoms |
| Data processing | PASS | fixed measurement channel gives the stated KL direction |
| Noncommuting quasi-free KL | PASS | finite second-quantized derivation and Bregman identity |
| Spectral constant | PASS | divided differences and integral Taylor remainder |
| Toeplitz HS density | PASS | exact diagonal count and Parseval |
| Mixed Toeplitz limit | PASS | bounded Fejér `L^2` approximation plus uniform spectral approximation |
| Thermodynamic passage | PASS | quantum limit gives limsup; parity identity gives the classical limit |
| Center difference | PASS | exact evenness and dominated scalar KL expansion |
| PR53 import | PASS | matching lower bound only; no response regularity |
| Non-Wiener/barrier audit | PASS | explicit family and Fejér argument; method-only conclusion |
| HMM boundary | PASS | external hypotheses are not asserted for the DPP |

## Evidence boundary

No computation was performed.  This is not a novelty review.  The verdict is
limited to the exact frozen head and the statements in `frozen_scope.md`.

