# I05 DPP 21 — fixed scalar entropy rate beyond the PR39 Wiener neighbourhood

Issue: #48. Branch: `research/I05-DPP-21-20260909`.

## Status

**INCOMPLETE — AUTHOR DERIVATIONS, NOT INDEPENDENTLY REVIEWED.**

No whole-legal-interval theorem and no true entropy-rate counterexample is claimed here. The accepted main results are used only within their frozen scope: PR29/34 cover lines through a constant symbol; PR39 covers the half-period-even/odd orbit only in its explicit small Wiener interval. Open-PR author claims are not treated as theorems.

This checkpoint contributes four exact interfaces that do not assume a small Wiener norm:

1. the parity joining identity and an exact mutual-information-rate reformulation;
2. a complete-event determinant likelihood and its full Fisher-plus-acceleration curvature formula;
3. a uniform inverse and off-diagonal decay lemma for strict finite-range event matrices;
4. a fermionic balanced-beam-splitter reduction that isolates a single occupation-entropy inequality sufficient for finite DPP midpoint concavity, together with the reason existing quantum entropy-power results do not prove it.

The selected analytic route is the finite-range/quasilocal prediction route, with the balanced-beam-splitter formulation retained as an independent operator route. Neither has yet supplied the missing global sign.

## Object and target

For a fixed real measurable symbol `f:T=R/Z->[0,1]`,

```text
K_f(i,j) = integral_T f(theta) exp(2 pi i (i-j) theta) dtheta,
H_n(f)   = Shannon entropy of the complete DPP configuration on [1,n],
h(f)     = lim_n H_n(f)/n.
```

The test orbit is `f_t=c+t g`, where `c(theta+1/2)=c(theta)`,
`g(theta+1/2)=-g(theta)`, and `c` is nonconstant. Every occurrence of `t`
means the genuine affine path in `K_f`; no affine `L`-ensemble path and no
rotation of the observed coordinate basis is substituted.

## Files

- `proof.md`: exact derivations, route comparison, proved lemmas, and the remaining sign.
- `sources.md`: primary sources and the precise statement actually used from each.
- `code/probe_balanced_beamsplitter.py`: bounded diagnostic only; it enumerates every configuration and explicitly labels its floating output as non-proof.

## Current conclusion

The half-period problem is equivalent to convexity of a parity mutual-information rate. In strict finite-range families, every complete-event conditional inverse is uniformly exponentially local with constants independent of the configuration and volume. This removes the particular PR39 obstruction that ordinary Fourier-square tails do not control all event inverses, and gives a rigorous entry point for a volume-uniform prediction/cluster expansion outside the condition `2||c-1/2||_W<1`.

What remains is a sign theorem, not a convergence theorem: either prove

```text
J_m'(s) + 2 s J_m''(s) >= -o(m)
```

uniformly on the legal interval for the exact determinant likelihood in `proof.md`, or prove the balanced-beam-splitter occupation-entropy inequality stated there. Until one of these is closed, the requested whole-interval concavity is not established.
