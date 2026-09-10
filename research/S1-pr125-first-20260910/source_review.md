# Source review for PR125

## Author files read

All four files at the frozen head were read before any outside review verdict:

- `README.md`;
- `sharp_scalar_KL_upper_bound.md`;
- `reverse_audit_and_A0_barrier.md`;
- `review_contract.md`.

No S3 SECOND was read or cited before completion of this FIRST.

## Load-bearing external facts

Petz's finite-dimensional review states monotonicity of quantum relative
entropy under trace-preserving 2-positive coarse grainings and explicitly
derives the classical measurement inequality.  This supports the direction
used by PR125 once the occupation measurement is identified.

Brunetti--Fredenhagen--Pinamonti derive explicit relative-entropy formulas for
gauge-invariant quasi-free states.  Their discussion following Proposition 11
records the compact/finite-dimensional formula used in PR125.  The present
FIRST also reconstructed the finite formula directly from the quasi-free
density matrix, so no infinite-dimensional hypothesis from that paper is
silently imported.

The mixed Toeplitz trace lemma is proved inside PR125; no external Szegő theorem
beyond the supplied polynomial-approximation argument is load-bearing.

## Non-load-bearing comparison sources

Han--Marcus concerns finite-state hidden Markov chains under positivity and
analytic parameter hypotheses.  Tadić--Doucet concerns genuine
continuous-state HMMs with specified transition/observation kernels and
mixing, analytic-continuation, likelihood and integrability hypotheses.
Neither source supplies a DPP-to-HMM representation.  PR125 correctly treats
them as comparison only.

## Primary links

- Petz, *Monotonicity of quantum relative entropy revisited*:
  `https://arxiv.org/abs/quant-ph/0209053`
- Brunetti--Fredenhagen--Pinamonti, *Thermodynamical aspects of fermions in
  external electromagnetic fields*:
  `https://arxiv.org/abs/2505.22413`
- Han--Marcus, *Analyticity of Entropy Rate of Hidden Markov Chains*:
  `https://arxiv.org/abs/math/0507235`
- Tadić--Doucet, *Analyticity of Entropy Rates of Continuous-State Hidden
  Markov Models*:
  `https://arxiv.org/abs/1806.09589`

## Frozen author tree

`https://github.com/randomcat4/dpp-entropy-tools/tree/87897b307818e9eab84ad465b24b4aeb037a1dc1/research/I05-DPP-36-Linf-second-difference-20260910`

