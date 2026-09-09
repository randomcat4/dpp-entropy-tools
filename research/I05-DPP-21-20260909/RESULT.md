# RESULT — scoped proof; global problem incomplete

Date: 2026-09-09.

## PROVED (AUTHOR PROOF), NOT INDEPENDENTLY REVIEWED

Fix `beta>0`. Let real symbols `c,g` satisfy

```text
sum_j exp(beta|j|)(|c_hat(j)|+|g_hat(j)|)<infinity,
c(theta+1/2)=c(theta),
g(theta+1/2)=-g(theta),
g != 0,
delta<=c(theta)<=1-delta
```

for some `delta>0`. Put `mu=integral c`. For every odd `k` with `g_hat(k)!=0`, define

```text
gamma=|g_hat(k)|^2,
alpha_k=gamma^2/[8mu^2(1-mu^2)].
```

Then there exists `epsilon>0` such that `c+tg` is strictly legal and

```text
t -> h(c+t g)+alpha_k t^4
```

is concave on `[-epsilon,epsilon]`. In particular, `h(c+t g)` is strictly concave on that interval.

The proof is in `finite_range_local_theorem.md` and `exponential_wiener_extension.md`. It uses a true entropy-rate KL lower bound and a volume/configuration-uniform analytic prediction formula; it does not differentiate `H_n/n` through the limit.

A fixed mean-`1/2` Rudin-Shapiro center in the finite-range proof satisfies

```text
2||c-1/2||_W=15/8>1,
```

so this domain is strictly outside PR39's Wiener-small hypothesis.

## INCOMPLETE

The following remain open in this work:

- concavity on the entire legal interval even for the stated analytic class;
- the PR39 fixed example on its full legal interval `[-384,384]`;
- arbitrary fixed measurable half-period-even/odd symbols;
- arbitrary fixed scalar symbol chords;
- a true entropy-rate counterexample.

## Review and novelty boundary

No nonauthor has reviewed the new proof. `verification.md` is only an author audit map. Primary sources and their limited roles are listed in `sources.md`. No claim of novelty, publication priority, or main-branch acceptance is made.