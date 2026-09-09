# C1 geometry proof review

Reviewer: C1 independent non-author reviewer.

Reviewed frozen file: `runs/C1/children/geometry/proof.md`.

SHA256 checked: `7C7082A59D695EF87C9549337F8722D98513D401AA872A9E86EACA3DF766717E`.

STATUS: CORRECT within the restricted partial theorem stated in Section 1.

This is not a proof of B0 on the full beta-zero set. It proves a uniform beta-negative collar near the specified full-support rank-one face, and the affine corner corollary in Section 8, under the fixed-parameter restrictions stated by the author.

## Scope checked

I checked the proof against its own frozen statement only:

- Section 1, lines 5-32: fixed full-support `u`, fixed `lambda in (0,1)`, compact `C`, uniform lower bound on `(PCP)|u-perp`, and uniformly bounded `R`.
- Section 4, lines 135-175: tangent-normal splitting, Fisher block orders, and the `g` block.
- Section 5, lines 176-213: singular block inverse for the true six-dimensional `M` system.
- Section 6, lines 214-245: exact `dG` rank-one identity on `T` and first Fisher correction.
- Section 8, lines 256-280: complement-signed affine family and uniform coverage for all `t/epsilon` ratios.

I did not read or rely on any unfrozen geometry draft. I did read `CLAIM.md`, `probe_output.json`, and the fixed `proof.md`.

## Section 4

The tangent-normal split is correct. `T={u w^T+w u^T}` and `V={E:Eu=0}` are complementary three-dimensional spaces. The forms

```text
k_ij(E)=u_i^2 E_jj+u_j^2 E_ii-2u_i u_j E_ij
```

vanish on `T`, and on `V` they form an isomorphism because all `u_i` are nonzero. The identity

```text
sum_ij k_ij(E)=tr E-u^T E u=tr E,  E in V,
```

is also correct.

The Fisher orders in (7) are consistent with the atom scales from Section 3:

- for `E in V`, pair atom derivatives are `lambda k_ij(E)+O(tau)` while pair masses are `tau lambda h_ij+O(tau^2)`, giving the `(lambda/tau) H_B` leading `VV` block;
- triple contributions to `VV` are only `O(1)`;
- `T` directions annihilate the leading pair and triple differentials, giving `F_TT=O(1)` and `F_TV=O(1)`;
- `g[E]=tau^-1 ell_B(E)+O(1)` keeps both the triple log term and all three pair log terms.

The subtraction `gg^T/Z` has orders `O(1)` on `VV`, `O(tau)` on `TV`, and `O(tau^2)` on `TT`, since `Z=(tau^2 lambda Delta)^-1[1+O(tau)]`. Thus the same leading `VV` coercivity remains for `Fpair`.

## Section 5

The block inverse argument is correct. From `N=L A+O(1)`, with `A=I-lambda uu^T`, one gets

```text
dG=L Q0+O(1),  Q0(D,E)=(1-lambda)tr(A^-1 D A^-1 E),
eta(D)=L^-1 tr(A^-1D)+O(L^-2).
```

The leading `TV` block of `Q0` vanishes because `A` preserves `span(u)` and `u-perp`. Therefore

```text
M_TT=L Q0_TT+O(1), M_TV=O(1), M_VV=(lambda/tau)H_B+O(L).
```

The leading coefficients in (10) follow:

- on `T`, `Q0(uu^T,D)=tr(A^-1D)`, so `h_T=uu^T/L^2+O(L^-3)`;
- on `V`, `H_B(B,E)=tr E`, so `h_V=tau B/(lambda L)+O(tau L^-2)`.

The two feedback estimates are small enough uniformly: the `VV` inverse correction gives `O(tau^2)`, absorbed by `O(tau/L^2)`, and the `TV` feedback into `T` gives `O(tau/L^2)`, absorbed by `O(L^-3)` because `tau L^3 -> 0`.

Substitution into `g^T h` gives the advertised coefficient:

```text
ell_B(B)=tr(I_2)-3=2-3=-1,
g^T M^-1 eta = -1/(lambda L)+O(L^-2).
```

I found no dropped six-dimensional component or substitution of an arbitrary `Lambda'` tangent.

## Section 6

The exact `dG` rank-one identity on `T` is valid for the actual `N`, not merely for the leading model. If `W=N^-1`, `a=u^T W u`, and `D=u w^T+w u^T`, then

```text
dG(uu^T,D)=d tr(W uu^T W D)=d a eta(D).
```

Hence `Q_TT^-1 eta_T=uu^T/(d a)` for `Q=dG`, and `eta_T^T Q_TT^-1 eta_T=1/d`.

The Neumann correction for `M_TT=Q_TT+Fpair_TT` has the displayed first term

```text
d alpha_T=1-Fpair(uu^T,uu^T)/(d a^2)+O(L^-2).
```

The leading Fisher value along `uu^T` is

```text
Fpair(uu^T,uu^T)=1/[lambda(1-lambda)]+O(tau),
```

because only the limiting empty and singleton atoms contribute at leading order; the projected rank-one subtraction is `O(tau^2)`. Since `d a^2=L/(1-lambda)[1+O(L^-1)]`, the first correction is exactly `-1/(lambda L)`.

The positive Schur complement contribution from `V` is `O(tau/L^2)`, and multiplying by `d=O(L^3)` gives `O(tau L)=o(L^-2)`. Thus (3) is supported:

```text
d alpha = 1 - 1/(lambda L) + O(L^-2).
```

## Section 8

The complement-signed affine algebra is correct. With `v=Su`, `tau=epsilon+t`, and `r=t/tau`,

```text
K(epsilon,t)=lambda uu^T + tau[I-lambda r(uu^T+vv^T)] - 2 epsilon t I.
```

The last term is `tau^2 R` with `||R||` uniformly bounded. On `u-perp`,

```text
B_r=I-lambda r(Pv)(Pv)^T,
Delta_r=1-lambda r[1-(u^T v)^2] >= 1-lambda > 0.
```

As `r in [0,1]`, the family `C_r` is compact and satisfies the Section 1 hypotheses uniformly. Therefore one `delta>0` covers `t/epsilon -> 0`, finite positive ratios, and `t/epsilon -> infinity`, as long as `u` and `lambda` are fixed and full-support/nonboundary. The proof correctly does not cover roots with `t` tending to a positive value, or sequences where `u`, `lambda`, or the soft block degenerates.

## Independent finite diagnostics

I added and ran an audit-owned diagnostic:

- script: `runs/C1/children/audit/geometry_asymptotic_audit.py`
- output: `runs/C1/children/audit/geometry_asymptotic_audit.remote.json`
- exit file: `runs/C1/children/audit/geometry_asymptotic_audit.exit`
- remote work directory: `/root/i05-seven-fronts-20260909/C1/audit`

Final run:

```text
status PASS
pid 164365
exit 0
python 3.12.3
numpy 2.1.2
threads OMP/OPENBLAS/MKL/NUMEXPR = 1
```

For `lambda=0.7`, `u_i^2=(0.2,0.3,0.5)`, and `C=I`, the independent double-precision reconstruction gave negative beta and `d alpha<1` at `tau=1e-4,1e-6,1e-8`. At `tau=1e-8`, it recorded:

```text
beta = -4.966507540514656e-10
d alpha = 0.9220148549442788
raw g^T h ratio to -1/(lambda L) = 0.7687934974957442
gap ratio to 1/(lambda L) = 1.0055776218895784
```

For the Section 8 affine family at `tau=1e-6` and ratios `r=0,0.25,0.75,1`, all beta values were negative and all `d alpha` values were below one. These are finite diagnostics only; the analytic uniform proof above is the reviewed object.

## Noncoverage

No critical gap was found in this restricted proof. The following limits remain outside the theorem and are correctly excluded by the author:

- full B0 on the entire beta-zero set;
- loss of full support in `u`;
- `lambda -> 0` or `lambda -> 1`;
- degeneration of the normalized soft block `B`;
- exact numerical collar radius or interval certificate;
- novelty certification.
