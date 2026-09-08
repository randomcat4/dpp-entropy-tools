# Frozen theorem v1

Status: frozen by the route owner. Proof and review tasks may not alter or add assumptions.

## Objects and definitions

The torus is R/Z with normalized Lebesgue measure. Symbols f,g:T->[0,1] are fixed measurable real scalar functions. Write fhat(k)=integral f(x) exp(-2 pi i k x) dx and K_f(i,j)=fhat(i-j). The stationary determinantal law is defined by inclusion probabilities det K_f[A,A]; exact configurations must include the zero constraints as well. Use natural logarithms and 0 log 0=0.

H_n(f) is the Shannon entropy of the exact configuration on {0,...,n-1}. h(f)=lim H_n(f)/n. The target conjecture is h((f+g)/2)>=(h(f)+h(g))/2 for every such pair.

## Intent and source

[Lyons–Steif, Conjecture 9.2](https://arxiv.org/pdf/math/0204324), with Section 6 used only under its stated hypotheses. Fixed scalar symbols, rather than window-dependent circulants or matrix-valued block processes, are required. The independent review task checks the semantic contract.

## First subfamily and assumptions

f_t(x)=p+sum_{k=1}^m [a_k cos(2 pi k x)+t b_k sin(2 pi k x)], with rational p,a_k,b_k and one fixed finite m. Endpoints t=+-tau must admit a proved uniform margin epsilon<=f_t<=1-epsilon. Parameters and tau do not depend on the window length. At least two harmonics and a nontrivial cycle phase are required for a candidate labelled a phase mechanism. Reflection gives f_-t(x)=f_t(-x); equality of endpoint entropies is allowed and expected.

## Information, boundaries, randomness

Only public mathematical sources and route-owned artifacts may enter public evidence. Numerical seeds, versions, actual invocations, coverage, PID and exit status are recorded. Uniform margins are assumptions of the selected diagnostic subfamily, not of the full conjecture. Constant symbols serve only as controls.

## Success criteria

Define Delta=(h(f_-tau)+h(f_tau))/2-h(f_0). A counterexample requires certified rate bounds with (L_-+L_+)/2-U_0>0. A negative-rate exclusion for one pair requires (U_-+U_+)/2-L_0<0. A restricted-family theorem is labelled with its exact scope. Any solution of the open conjecture requires two fresh independent reviewers who did not author that proof.

## Non-claims

Positive finite H_n curvature, convergent-looking increments, or finite scans do not settle the entropy rate. A single gauge-invariant phase is not evidence of a positive rate gap. No exchange of limits and derivatives is assumed. No assertion of novelty or current solved/open status is inferred from an unsuccessful literature search.
