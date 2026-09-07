# T3 Core Notes: Candidate Strict Reference Loop

Status: CANDIDATE / math conclusion INCOMPLETE.

This core is a small reference prototype for rational paths `M(t)=K+tD`.  It is meant to be auditable before it is fast.

Implemented loop:

1. Parse rational `K`, rational `D`, and a rational interval `[a,b]`.
2. Enumerate every subset `S` of `{0,...,n-1}` and compute the exact inclusion polynomial `det(M(t)_S)` in the power basis using `fractions.Fraction`.
3. Mobius-invert the inclusion polynomials to exact outcome masses
   `q(S)=sum_{T superset S} (-1)^(|T|-|S|) det(M(t)_T)`.
4. Certify exact outcome-mass nonnegativity on `[a,b]` with exact Bernstein coefficients, recursively subdividing up to a caller-set depth.  Principal-minor nonnegativity is retained as an audit.  A Gershgorin fallback may be recorded for symmetric affine inputs, but it does not replace the required exact outcome-mass checks.
5. Select an event family for entropy.  The default is all exact outcomes, which sum to the constant polynomial `1`.  Entropy certification is refused unless the selected exact mass polynomial is exactly `1`, unless the caller explicitly disables that precondition.
6. Bound `-p log(p)` by exact rational intervals.  For `p=0`, the term is exactly the mathematical limit `0`, not an epsilon.  For `p>0`, logs are bounded by power-of-two range reduction and the rational series
   `log(x)=2 atanh((x-1)/(x+1))`, with a rational geometric tail bound.
7. Certify a chord gap at a rational point `t` and/or point curvature `H''(t)`.  Curvature is evaluated only when every non-identically-zero exact outcome mass is positive at `t`; a nontrivial zero probability makes the curvature certificate refuse until a separate local zero-order argument is added.

Worked rational example:

```text
K = [[1/5, 1/15], [1/15, 2/5]]
D = [[2/5, 1/30], [1/30, -1/5]]
t in [0, 1]
```

The inclusion principal minors are

```text
det K_{}    = 1
det K_{0}   = 1/5 + 2t/5
det K_{1}   = 2/5 - t/5
det K_{0,1} = 17/225 + 26t/225 - 73t^2/900
```

The exact outcome masses used by entropy are their Mobius inversion:

```text
q({})    = 107/225 - 19t/225 - 73t^2/900
q({0})   = 28/225 + 64t/225 + 73t^2/900
q({1})   = 73/225 - 71t/225 + 73t^2/900
q({0,1}) = 17/225 + 26t/225 - 73t^2/900
```

These are nonnegative on `[0,1]` and sum exactly to `1`.  The example asks for the chord gap and curvature at `t=1/2`.

Commands:

```powershell
python research\T3\core\dpp_core.py --example
python research\T3\core\dpp_core.py --input research\T3\core\tiny_example.json
python -m unittest discover -s research\T3\core -p "test_*.py"
```

Known limits:

- This is not a theorem prover for global entropy concavity and does not claim any result outside the supplied finite rational path.
- Exact Sturm/root isolation is not implemented.  Bernstein subdivision and the optional Gershgorin fallback are sufficient methods only; unresolved cases are refused.
- Determinants use permutation expansion, so the intended range is small `n` only.
- The code does not normalize event weights.  If the selected exact outcomes do not already form an exact probability simplex, entropy certification is refused by default.
- The public seed values from `research/T3/artifacts/seed_chord_case.json` are embedded in the owned tiny example.  The test suite also exercises that artifact directly when it is present in the integration checkout.
