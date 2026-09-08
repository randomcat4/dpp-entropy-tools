# D10-M3 lemma ledger

| Item | Status | Role | Notes |
|---|---|---|---|
| Projection-DPP spectral mixture representation | PROVED_HERE | Converts fixed-eigenvector path into latent Bernoulli subset plus fixed channel | Uses Cauchy--Binet and finite DPP inclusion probabilities. |
| Exact atom derivatives through latent scores \(a_R,b_R\) | PROVED_HERE | Gives checkable \(p,p',p''\) and \(H''\) formulas | Requires strict \(0<\theta_i<1\). |
| Cardinality preservation \(|Y|=|Z|\) | PROVED_HERE / STANDARD | Enables \(H(Y)=H(N)+H(Y\mid N)\) | Projection DPP of rank \(|Z|\). |
| Shepp--Olkin concavity for Poisson-binomial count entropy | KNOWN_IMPORTED | Gives \(H(N)''\le0\) | Same theorem family already cited in D10-S derivation; not reproved here. |
| Discrete-concave expectation lemma | PROVED_HERE | If \(c_k\) has \(\Delta^2c_k\le0\) and rates have same sign, then \(E c_N\) is concave | Direct second-difference calculation. |
| Cardinality-uniform channel sufficient class | PROVED_HERE_CONDITIONAL | Closed concavity subcase when all same-size squared minors are uniform | Existence/classification not proved; n=2 Hadamard is an example. |
| Arbitrary 2D fixed spectral block | PROVED_HERE | Non-permutation \(2\times2\) commuting spectral PSD/NSD exclusion | Uses cardinality split plus perspective concavity for the one-point channel. |
| Direct sums of 1D and 2D closed blocks | PROVED_HERE | Arbitrary dimension but block-independent exclusion family | Entropy additivity over block diagonal DPP kernels; not a coupled high-dimensional theorem. |
| Generic fixed-\(Q\) commuting spectral concavity | OPEN / INCOMPLETE | Original target of this route | Reduces to controlling \(H(Y\mid |Y|)\); no general sign proof. |
| Finite small-dimensional sanity checks | COMPUTATIONAL_CHECK | Validates formulas, not theorem | `channel_sanity.py`, exit 0, 20 atom polynomials. |
