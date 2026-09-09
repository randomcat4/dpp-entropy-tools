# I05 DPP21 continuation — entropy-rate concavity away from the parity point

Issue: #48. Branch: `research/I05-DPP-21-nonzero-20260909`.

Base: `main@9dcb6e9079ca57f94e0e30d63161cda89ca61fae`.

## Status

**PROVED (AUTHOR PROOF), NOT INDEPENDENTLY REVIEWED:** a compact radial-tube theorem, an exact arbitrary-center RPF Hessian identity, and a beam-splitter second-order obstruction.

**INCOMPLETE:** whole-legal-interval concavity for every strict exponentially local half-period center, legal endpoints, arbitrary measurable symbols, and a true entropy-rate counterexample.

The old `RUNNING` text on issue #48 is historical. The accepted input is the final main-scoped PR53 theorem recorded in `docs/verification_round3_20260909/accepted_pr53.md`.

## Main new theorem

Fix `0<mu<1`, a real exponentially weighted Fourier symbol `g` with

```text
g(theta+1/2)=-g(theta),
g!=0,
```

an odd `k` with `g_hat(k)!=0`, and any prescribed `T>0` for which

```text
mu+t g(theta)
```

stays uniformly inside `(0,1)` for every `|t|<=T`.

Then there is a center radius `rho>0` such that every real half-period-invariant center `c` with mean `mu` and

```text
||c-mu||_beta<rho
```

satisfies

```text
t -> h(c+t g)+(2/3)|g_hat(k)|^4 t^4
```

concave on the **whole prescribed interval** `[-T,T]`. Hence `h(c+t g)` is strictly concave there.

The result is not a re-centering argument. At nonzero `t_*`, the symbol `c+t_*g` is generally not half-period invariant. The proof instead forms the normalized curvature `h''(c+t g)/t^2`, extends it analytically through `t=0`, uses the accepted `(4/3)|g_hat(k)|^4t^4` radial margin at the constant center, and transports that margin to nearby nonconstant centers uniformly over `[-T,T]`.

A fixed explicit family has mean `1/3`, nonconstant center, and covers `[-2,2]`, so it lies outside PR39's mean-`1/2` scope and includes neighborhoods far from zero.

## Other exact outputs

`proof.md` derives the complete prediction-potential Hessian at an arbitrary strict parameter:

```text
h''=nu(Bddot)+nu(xi u)
    +2nu(psi R Bdot)
    +2nu(psi R(psi u))
    -nu(psi^2 u).
```

The local conditional Fisher term is retained inside `Bddot`; the other terms are the conditional acceleration and stationary-law response. A finite-state transfer approximation comes with a volume-independent exponentially decaying error, giving a rigorous interval-certificate interface rather than a finite-window extrapolation.

The balanced fermionic beam-splitter route is compared exactly. Its output occupation mutual information is only `O(u^4)` around a midpoint, so it contributes zero to quadratic curvature. The entire second-order sign is in the still-unproved occupation-entropy gain; a von-Neumann entropy inequality does not replace it.

## Files

- `frozen_statement.md`: exact quantifiers and status.
- `proof.md`: complete proof, RPF Hessian, finite-state bridge, beam-splitter obstruction, explicit family, and remaining gap.
- `sources.md`: primary literature and exact roles.
- `attempts.md`: failed shortcuts and why they do not settle the sign.
- `verification.md`: author self-audit and independent-review checklist.
- `code/check_explicit_family.py`: dependency-free exact arithmetic for the displayed example only.
- `output/explicit_family_exact.json`: expected exact output; not an entropy computation.

No heavy computation is used by the theorem. No finite entropy or floating-point curvature is promoted to a rate statement.