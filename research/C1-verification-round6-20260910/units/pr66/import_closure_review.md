# PR66 Dobrushin Import Closure

Verdict: **NEEDS_FIX/CRITICAL_GAPS for the load-bearing Dobrushin import as written**.

The full Dobrushin primary text does not support PR66's compressed import as a generic theorem for arbitrary one-dimensional finite-alphabet block interactions with only an unnormalized finite first moment. The internal PR66 localization, conditional, equilibrium, parity, and quartic-curvature lemmas remain conditionally accepted from my original FIRST review; the gap is specifically the external response theorem used to turn the constructed interaction into analytic pressure/local response for `P(lambda U_s)` near `(s, lambda) = (0, 1)`.

## Primary Theorem Pins

Source: R. L. Dobrushin, "Analyticity of the correlation functions for one-dimensional classical systems with power law decay of the potential," Math. USSR-Sb. 23:1 (1974), 13-44. Public PDF: <https://www.mathnet.ru/links/65f76350e7e8dd7f8420ad19db2ee8af/sm3631_eng.pdf>. Canonical page: <https://www.mathnet.ru/eng/sm3631>. Local supplied SHA256: `91d79d372cf4b574db400e06ad081d38eef793f576bb94d40c3dbe74a411c1ef`.

Dobrushin's printed pages 14-15 define the two relevant potential classes. `A1` assumes translation invariance, a uniform lower bound, a positive-measure boundedness condition C1, and D2, whose summability includes an exponential factor in `|V|`. `A2` assumes translation invariance, a uniform lower bound, the stronger null-state condition C2/(2.5), and D1, a first-moment cross-bound without that exponential cardinality factor. Printed pages 17-18 state Theorems 1-2, giving multiparameter holomorphic free energy when the perturbation lies in the theorem's class. Printed pages 24-25 state Theorem 6, a Banach-space analytic free-energy reformulation for `A1`; the same discussion gives the analogous uniformly bounded `A2` norm only in the linear space satisfying translation invariance and C2.

## Map To PR66

PR66 constructs translation-invariant interval interactions

```text
U_{z,[i,i+n]} = -psi_{n,z}(x_i,...,x_{i+n})
```

with `||psi_n||_infty = O(n^(-2q))` and proves

```text
sum_{A contains 0} diam(A) ||U_A||_infty < infinity
```

because there are `n+1` intervals of diameter `n` through the origin and `q>3/2` (`source-snapshots/pr66/proof.md:335-387`). This is a strong ordinary finite-first-moment estimate for the submitted interval representation.

That estimate is still not enough to fit either available Dobrushin class as stated in the actual primary text:

- **A1/D2 route is unsupported as written.** PR66's interval sizes grow as `|V|=n+1`, while the A1 Banach norm and D2 condition include `exp(alpha |V|)`. The proved polynomial upper estimate `O(n^(-2q))` does not establish the required exponential-cardinality summability. I do not claim a lower bound excluding faster actual decay of these particular interactions; the point is that PR66 has not proved the A1/D2 norm needed for Theorem 6's A1 branch.
- **A2/D1 route is not established as written.** The A2 branch removes the exponential cardinality factor for uniformly bounded potentials, but it requires condition C2/(2.5): a distinguished positive-measure state set `C` such that each interaction vanishes whenever any coordinate in its support lies in `C`. PR66's `psi_{n,z}` are arbitrary bounded binary block functions produced by telescoping a log conditional; the packet does not prove that they vanish when any coordinate equals a fixed state, nor does it give a controlled null-state normalization preserving the Dobrushin A2 norm.

The usual finite-alphabet way to force a null-state convention would require a decomposition of each block function into interactions indexed by subsets and vanishing when a reference state occurs. PR66 does not provide such a decomposition. A naive subset or monomial expansion can lose an exponential factor in block length, exactly the issue the author flags when refusing to use Cassandro-Olivieri as a sole arbitrary-block citation (`source-snapshots/pr66/sources.md:28-30`, `source-snapshots/pr66/attempts.md:73-79`). Without a new controlled decomposition, the proved polynomial interval norm does not imply Dobrushin's A2 Banach norm.

## Consequence For `P(lambda U_s)`

If PR66 supplied an interaction representation lying in Dobrushin's applicable Banach space, then Theorem 2/Theorem 6 would be structurally adequate for the intended pressure step: Theorem 2 gives holomorphic dependence for finite-dimensional complex parameters, and Theorem 6 gives analytic free energy as a function of the potential in a Banach neighborhood. Since PR66 proves `s -> U_s` Banach-holomorphic and wants `F(s,lambda)=P(lambda U_s)` near `(s, lambda) = (0, 1)`, the pressure analyticity would follow by composition inside such a neighborhood.

The blocker is prior to that composition step: the submitted `U_s` has not been shown to belong to an available Dobrushin class. Therefore the true-rate analytic bridge in `source-snapshots/pr66/proof.md:457-513` remains unsupported by the cited primary theorem.

## Cassandro-Olivieri Scope

The accessible Cassandro-Olivieri publisher page says the paper treats one-dimensional systems described by many-body potentials with finite first moment and proves analytic dependence of correlation functions on interaction parameters. PR66, however, explicitly does not use Cassandro-Olivieri as the sole arbitrary-block-function theorem because its concrete lattice-gas coordinates would require a representation conversion that may cost exponentially in block size (`source-snapshots/pr66/sources.md:28-30`, `source-snapshots/pr66/attempts.md:73-79`). I did not use Cassandro-Olivieri to close the Dobrushin mismatch.

## Minimal Repair

PR66 needs one of the following precise repairs:

1. Prove a controlled null-state/gauge decomposition of the telescoped interval interaction into Dobrushin A2 potentials, with `sum d(V) g(d(V)) sup |U_V| < infinity` for some `g(d) -> infinity`, uniformly on the needed complex neighborhood and for `lambda U_s` near `(s, lambda) = (0, 1)`.
2. Prove enough additional decay or structure to establish an A1/D2 exponential-cardinality norm; the current polynomial `O(n^(-2q))` interval upper bound does not establish it.
3. Cite and pin a different primary theorem that genuinely covers arbitrary finite-alphabet one-dimensional block interactions under the unnormalized first-moment condition PR66 proves, including Banach-holomorphic pressure/local-response for the two-parameter family `lambda U_s`.

Until one of these is supplied, the PR66 theorem is not ready under the actual Dobrushin assumptions, even though the conditional internal proof chain remains coherent.
