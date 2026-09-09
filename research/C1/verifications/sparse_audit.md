# C1 sparse proof review

Reviewer: C1 independent non-author reviewer.

Reviewed frozen file: `runs/C1/children/geometry/sparse_proof.md`.

SHA256 checked: `B096A9986D123652849704ED001439B63373591153F4BBD321F8023D9AB98E9F`.

STATUS: CORRECT within the restricted sparse rank-one boundary theorem stated in Section 1.

This is not a proof of B0 on the full beta-zero set. It proves that exact beta zeros exist in the specified sparse family for all sufficiently small epsilon, and that along those zeros `d alpha -> 1` from below.

## Scope checked

I checked the frozen statement and its consequences in:

- Section 1, lines 9-49: statement, `(S1)`, uniform `(S2)-(S4)`, and the no-uniform-margin consequence.
- Section 2, lines 51-107: exact atom formulas `(S5)`, strictness, log data, `N` block asymptotics `(S6)`, and eta scales.
- Section 3, lines 109-175: six genuine directions, rare/common event derivatives, `g`, Fisher constants, and the common-event `F(U,V)` correction.
- Section 4, lines 177-229: cofactor blocks, unused directions, uniform remainders, Schur elimination, and rank-one projection feedback.
- Section 5, lines 231-266: the exact leading two-dimensional solve `(S11)`, positive determinant, closed coefficient `C(kappa)`, and final simplification.
- Section 6, lines 268-290: `d alpha` from below.
- Section 7, lines 292-318: endpoint signs, IVT exact zero, localization near `kappa_*`, and absence of a uniform safety margin.

I did not read unfrozen geometry drafts or other reviewers' conclusions.

## Uniform asymptotics

The exact atom formulas `(S5)` are correct for `K=epsilon I+lambda uu^T`. In the sparse parameterization `u_3^2=kappa epsilon`, they give the stated scale split:

```text
p0,p1,p2 = O(1),
p3,p12,p13,p23 = O(epsilon),
p123 = O(epsilon^2).
```

The log matrix expansion `(S6)` follows uniformly for `kappa` in a compact positive interval:

```text
ell13,ell23=-m+O(epsilon),  Lambda=m+O(epsilon),  ell12=-L+c12+O(epsilon),
N = block [[ma,0,-m lambda sqrt(kappa epsilon)], [0,m,0], [...,0,L-c12]] + lower order.
```

Here `m=log((a+lambda kappa)/a)` is bounded above and below away from zero on `[1,10]`; all probability denominators retain fixed leading signs. This is enough for the uniform inverse and eta scales used later.

## Fisher, common events, and rank feedback

The Section 3 derivative table `(S7)` correctly uses six actual K-coordinate directions, not epsilon or kappa derivatives. The rare log derivative `g` in `(S8)` keeps the triple atom and all pair atoms; the leading cancellations for `Q` and the `epsilon^-1/2` scale for `W` are consistent.

The dangerous `F(U,V)` cross term is handled correctly. The rare events alone give

```text
Fav_rare = -2 lambda sqrt(kappa) R (1/A+1/lambda).
```

The common events `p0,p1,p2` add

```text
Fav_common = 2 lambda sqrt(kappa)/a + 2 sqrt(kappa) = 2 sqrt(kappa)/a.
```

So the total coefficient `(S10)` is the one used in `(S11)`. Omitting this common contribution changes the sign mechanism; the current proof does not omit it.

The `gg^T/Z` subtraction is uniformly lower order for the leading displayed Fisher constants:

```text
VV: O(epsilon),  VZ0: O(sqrt(epsilon)),  UV: O(epsilon^(3/2)).
```

Thus the rank-one score projection cannot change the leading signs in `(S9)-(S11)`.

## M inverse and unused directions

Section 4 gives enough uniform control of all six directions. The leading positive blocks are:

```text
M(T,T)=2L+O(1),
M(Q,Q)=lambda/epsilon+O(L),
M(W,W)->4lambda kappa+2ma>0,
```

and the scaled `V,Z0` block is the positive two-by-two matrix in `(S11)`. The determinant

```text
2(2 lambda kappa + m(a+lambda^2 kappa))/(a+lambda kappa)
```

is positive and bounded below on `[1,10]`. The Schur eliminations therefore use uniformly bounded inverses after the displayed scalings.

The `W` direction is the subtle one because `g[W]=O(epsilon^-1/2)`. The proof's vanishing leading couplings are sufficient: the actual `M(T,W)` leading coefficient is `O(sqrt(epsilon))`, while `M(U,W)` and the `V,Z0` couplings do not create a larger source. This gives `h_W=O(sqrt(epsilon)/L^2)+O(epsilon^(3/2)L^2)`, so `g[W]h_W=O(L^-2)+o(L^-1)`. It cannot alter `(S2)`.

## Closed coefficient and exact zeros

The leading two-dimensional system `(S11)` is the actual optimizer system after the `h_U` source cancellation, not an arbitrary `Lambda'` tangent condition. Solving it gives the closed coefficient

```text
C(kappa)=kappa[(2lambda-1)-lambda(1-lambda)m] /
         ((1-lambda)[2lambda kappa+m((1-lambda)+lambda^2 kappa)]).
```

For `lambda=7/10`,

```text
C(1)  > 0,
C(10) < 0,
kappa_*=(3/7)(exp(40/21)-1).
```

At `kappa_*`, the derivative is

```text
C'(kappa_*)=-kappa_* lambda^2/(A(kappa_*)J(kappa_*))<0.
```

The uniform error in `(S3)` preserves endpoint signs for sufficiently small epsilon. Since beta is continuous on `[1,10]` in that regime, IVT gives an exact zero in `(1,10)`. Localization `kappa_epsilon=kappa_*+O(1/L)` follows from uniqueness of the zero of `C` and the nonzero derivative at that point; the proof does not claim finite-epsilon uniqueness.

## d alpha and no uniform margin

The rank-one identity in Section 6 is exact:

```text
G(U,U)=eta(U)^2
```

for `U=ww^T`, because `U` is rank one. Therefore the one-dimensional restricted value has

```text
d alpha_U = 1 - 1/(lambda L)+O(L^-2).
```

The remaining directions contribute only `O(epsilon L)+O(L^-2)` after multiplication by `d=O(L)`. Since `epsilon L` is smaller than any inverse power of `L`, `(S4)` is uniform and gives

```text
d alpha = 1 - 1/(lambda L)+O(L^-2).
```

At the exact beta zeros from Section 7, this proves `d alpha<1` for sufficiently small epsilon and `d alpha -> 1`. Hence the conclusion that no fixed `delta>0` can uniformly separate all connected strict beta-zero points from `1` is valid.

## Independent high-precision diagnostics

I added and ran an audit-owned high-precision diagnostic:

- script: `runs/C1/children/audit/sparse_asymptotic_audit.py`
- output: `runs/C1/children/audit/sparse_asymptotic_audit.remote.json`
- exit file: `runs/C1/children/audit/sparse_asymptotic_audit.exit`
- remote work directory: `/root/i05-seven-fronts-20260909/C1/audit`

Final run:

```text
status PASS
pid 165270
exit 0
python 3.12.3
mpmath 1.3.0
digits 100
threads OMP/OPENBLAS/MKL/NUMEXPR = 1
```

The run rebuilt `Fpair`, `M`, `h=M^-1 eta`, `beta`, and `d alpha` from the eight probabilities. It recorded:

```text
C(1)  =  0.208644606469760128020070130055
C(10) = -0.294454310303997556780068145153
kappa_* = 2.45048912533725948929463358161
```

At `epsilon=1e-24`, endpoint beta signs matched the proof:

```text
beta(kappa=1)  =  3.74462592894816879436752979961e-27
beta(kappa=10) = -4.08089452349875831808878068605e-27
```

An 80-step bisection at `epsilon=1e-24` found a numerical root near `kappa=2.82157919338528463644189423312`, with

```text
root beta ~= 3.66725225493074741386729454952e-51
root d alpha = 0.974540167816797356886092080627
lambda L (1-d alpha) = 0.984873624926897246463145055469.
```

The same script split the `F(U,V)` term. For `kappa=1`, `epsilon=1e-24`:

```text
common contribution / sqrt(epsilon) = 6.66666666666666666666666184127
rare contribution / sqrt(epsilon)   = -5.77999999999999999999997719571
total / sqrt(epsilon)               = 0.886666666666666666666683245556
closed total limit                  = 0.886666666666666666666666666667
rank projection contribution        = 1.50733333333333333333336468909e-24
```

These diagnostics support the algebra but are not used as a proof.

## Noncoverage

No critical gap was found in the restricted theorem. The proof correctly does not claim:

- B0 on the full beta-zero set;
- uniqueness of finite-epsilon roots;
- a specified explicit epsilon threshold;
- a certified entropy-chord counterexample;
- coverage when `kappa` leaves a compact positive interval, `lambda` approaches `0` or `1`, or the family is changed;
- novelty certification.
