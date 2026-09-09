# Frozen statement — DPP21 nonzero-parameter continuation

Base: `main@9dcb6e9079ca57f94e0e30d63161cda89ca61fae`.

Status of the new statements: **PROVED (AUTHOR PROOF), NOT INDEPENDENTLY REVIEWED**.

Status of the whole-legal-interval problem for arbitrary strict exponentially local half-period symbols: **INCOMPLETE**.

All entropies below are complete-configuration Shannon entropies with natural logarithms. All paths are affine in the correlation kernel. No event, Fisher term, or conditional acceleration is removed.

## 1. Compact radial-tube theorem

For `beta>0`, write

```text
A_beta={u:T->C : ||u||_beta=sum_{j in Z} exp(beta|j|)|u_hat(j)|<infinity}.
```

Fix

```text
0<mu<1,
g in A_beta real,
g(theta+1/2)=-g(theta),
g!=0.
```

Choose an odd `k` with `g_hat(k)!=0`, and put

```text
lambda_k=|g_hat(k)|^4>0.
```

Let `T0>0` satisfy

```text
delta_T=inf_{theta, |t|<=T0}
        min{mu+t g(theta),1-mu-t g(theta)}>0.         (1.1)
```

Then there exists

```text
rho=rho(beta,mu,g,k,T0)>0                              (1.2)
```

such that every real `c in A_beta` satisfying

```text
c(theta+1/2)=c(theta),
integral c=mu,
||c-mu||_beta<rho                                     (1.3)
```

is strictly legal along `[-T0,T0]`, and

```text
t -> h(c+t g)+(2/3)lambda_k t^4                      (1.4)
```

is concave on that whole interval. Consequently `t -> h(c+t g)` is strictly concave on every nontrivial subchord of `[-T0,T0]`.

Equivalently, for distinct `t_0,t_1 in [-T0,T0]`, `0<q<1`, and `m=(1-q)t_0+q t_1`,

```text
h(c+m g)-(1-q)h(c+t_0g)-q h(c+t_1g)
 >=(2/3)lambda_k[(1-q)t_0^4+q t_1^4-m^4]>0.          (1.5)
```

The theorem controls an arbitrarily prescribed compact subinterval of the legal constant-centered radial chord, including neighborhoods of nonzero parameter values. It is not obtained by re-centering at a nonzero point. The small quantity is the transverse center perturbation `c-mu`, not the parameter interval.

## 2. Exact RPF second-variation identity

On any compact strict `A_beta` symbol chord for which the one-sided complete-event conditional is the positive normalized Holder `g`-function `G_t`, define

```text
phi_t=log G_t,
psi_t=d_t phi_t,
xi_t=d_t^2 phi_t,
(L_t F)(x)=sum_{a=0,1}G_t(ax)F(ax),
nu_t L_t=nu_t,
Pi_t F=F-nu_t(F),
R_t=(I-L_t)^(-1)Pi_t,
B_t=-L_t phi_t,
h(t)=nu_t(B_t),
 u_t=R_t B_t.                                         (2.1)
```

With dots denoting `t` derivatives,

```text
Bdot_t=-L_t(psi_t phi_t),
Bddot_t=-L_t((xi_t+psi_t^2)phi_t+psi_t^2),            (2.2)
```

and the exact curvature is

```text
h''(t)=nu_t(Bddot_t)+nu_t(xi_t u_t)
       +2nu_t(psi_t R_t Bdot_t)
       +2nu_t(psi_t R_t(psi_t u_t))
       -nu_t(psi_t^2 u_t).                            (2.3)
```

Here `R_t` includes centering by `Pi_t`. The term `-L_t(psi_t^2)` inside `Bddot_t` is the local conditional Fisher term; all acceleration and stationary-measure response terms in (2.3) are retained.

## 3. Beam-splitter infinitesimal obstruction

Fix a strict parameter `t_*` and put `K_-=K_{c+(t_*-u)g}`, `K_+=K_{c+(t_*+u)g}`, and `M=K_{c+t_*g}`. The balanced fermionic beam splitter sends the two quasifree inputs to a quasifree output whose two occupation marginals both have kernel `M` and whose doubled covariance is

```text
K_out(u)=[[M,u K_g],[u K_g,M]].                       (3.1)
```

For every finite window, and also per lattice cell at the true stationary rate under the strict `A_beta` hypotheses,

```text
2h(t_*)-h(t_*-u)-h(t_*+u)
 =I_out(u)+E_occ(u),                                  (3.2)
```

where `I_out(u)>=0` is the output occupation mutual-information rate and

```text
E_occ(u)=h_out(u)-h(t_*-u)-h(t_*+u).                  (3.3)
```

The cross-layer law is even and differs from its product law only at order `u^2`; hence

```text
I_out(u)=O(u^4),
I_out''(0)=0,
E_occ''(0)=-2h''(t_*).                                (3.4)
```

Thus nonnegativity of output mutual information cannot determine the quadratic curvature at a nonzero center. The entire second-order sign sits in the still-unproved occupation-entropy gain. A von-Neumann entropy inequality does not replace (3.3).

## 4. Scope not claimed

The statements above do not prove concavity for every center in `A_beta`, at legal endpoints, or on an arbitrary center's entire legal interval. They do not prove the occupation-entropy gain is nonnegative and do not give a true entropy-rate counterexample. The radius `rho` is existential; the main gain is whole prescribed compact-parameter coverage rather than a new small neighborhood of `t=0`.