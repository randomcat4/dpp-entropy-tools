# D10-U10e general symmetric path / boundary_full_atom fresh audit

STATUS: INCOMPLETE

Audit result: the analytic reductions I checked are internally consistent, but
the global inequality `sigma(x,c)>0` on the full rectangle remains OPEN.  The
boundary profile and author grids remain finite/asymptotic SCOUT evidence, not
a theorem.

## Scope

Target family:

```text
K(x,a) = [[x,a,0],
          [a,x,a],
          [0,a,x]]
```

After sign conjugacy and complementation, the reduced domain is

```text
0 < x <= 1/2,       0 < a < x/sqrt(2).
```

With `c=2a^2/x^2`, this is exactly the rectangle
`0<x<=1/2, 0<c<1`, since the eigenvalues are
`x`, `x±sqrt(2)a = x(1±sqrt(c))`.  Thus
`lambda_min=x(1-sqrt(c))>0` and
`lambda_max=x(1+sqrt(c))<1`.

## Frozen inputs

Full SHA-256 table is in `audit_results.json`.  Key hashes:

- `symmetric_path_global/derivation.md`:
  `6cad0552d08020d0205923225eb48700c12244d95fbfbdd0d592010ced790296`
- `symmetric_path_global/profile.json`:
  `788ced5cabf39bb807dea151f2c598992986f838f8cedcf8f9992ead4512e61e`
- `symmetric_path_global/boundary_full_atom/analysis.md`:
  `be95a21f1111d660221eede703c062e20917cdfc3bcf44653278930588eec928`
- `symmetric_path_global/boundary_full_atom/asymptotic_results.json`:
  `50e58ace9547d2732073810369f2fe82e57b91de23da1606bba5e06b8b177d60`
- reviewed U10d dependency,
  `symmetric_path_subfamily/audit_nonauthor/verdict.md`:
  `95d01060ae54783f1ce3315905c95e0166ea573ae835a32c010ac9f0b7557074`

## Analytic identity checks

I rebuilt the exact-event law from principal-minor inclusion probabilities and
Möbius inversion for independent rational samples.  The atom list

```text
(E,U,W,V,U,Z,V,F)
```

matches exactly, with

```text
E=(1-x)((1-x)^2-cx^2)
F=x^3(1-c)
U=x(1-x)^2+(1-2x)cx^2/2
W=x(1-x)^2+(1-x)cx^2
V=x^2(1-x)-(1-2x)cx^2/2
Z=x^2(1-x)+cx^3.
```

On three independent rational samples, the explicit even-block formula agrees
with exact-event Hessian jets to Decimal residual at most `1.2e-166`.  The
reflection even/odd cross block is zero to residual at most `2e-168`, and the
odd block has positive LDL pivots on all samples.  The full-atom derivative
`jF` was checked exactly against the Möbius event jet.

The reflection-odd strictness argument is sound given the same `N>0` input used
by U10d: the non-Fisher part is the positive quadratic form

```text
2m d^2 + 8 Lambda a d h + 4n h^2,
```

whose determinant is `8(nm-2 Lambda^2 a^2)>0`; the Fisher term is
positive semidefinite.

## Sigma equivalence

For the four-dimensional even block, the covector `eta` has `eta_e=n/q>0`.
The columns

```text
t_d=(1,-eta_d/eta_e,0,0)
t_h=(0,-eta_h/eta_e,1,0)
t_k=(0,-eta_k/eta_e,0,1)
```

span the weighted-trace-zero hyperplane, and `[T0,e0]` is an invertible basis.
In this basis,

```text
M^T B_even M = [[C0,b0],
                [b0^T,d0]]
```

so, conditional on the reviewed `C0>0` input,

```text
B_even > 0  iff  sigma=d0-b0^T C0^{-1}b0 > 0.
```

Equivalently, under `C0>0`, `det B_even>0` has the same sign content as
`sigma>0`.  The audit script checks the Schur determinant identity
`det(block)-det(C0)*sigma=0` to high precision on the rational samples.

This is an exact reduction, but it does not prove `sigma>0` globally.

## Boundary and scout checks

For `c=1-s`, fixed `0<x<1/2`, direct boundary formulas confirm that the only
vanishing atom at `s=0` is

```text
F=x^3 s.
```

The other atoms have positive limits:

```text
E0=(1-x)(1-2x), U0=x(1-3x/2), W0=x(1-x),
V0=x^2/2, Z0=x^2.
```

The full-atom derivative is

```text
jF = x^2((1+s)d + e - 2sqrt(2)sqrt(1-s)h + (1-s)k),
```

hence its Fisher contribution is exactly the positive rank-one pole

```text
(x/s) w_s w_s^T.
```

I independently checked the Sherman--Morrison stable Schur formula by comparing
it to the direct `sigma` computation at moderate boundary samples; the largest
direct-minus-stable residual was below `1e-153`.

Independent samples reproduce the qualitative author boundary picture:

- `c->0`: `sigma` tends to `1/[x(1-x)]`; at `x=1/2`, the limit is `4`.
- Power scales `s=x^p`, sampled at `p=1/2,1,2,4,8`, keep `x*sigma` moving
  toward `1`, hence no sampled polynomial-scale negative mechanism.
- Exponential scale `s=exp(-beta/x)` is the sharp nonuniform valley.  At
  `x=1e-4`, my coarser independent beta grid has best sampled value near
  `beta=0.60`, `sigma≈26.5984`; the author finer table reports
  `beta=0.58`, `sigma≈26.5811`.
- At `beta=0.58`, `x=1e-4`, the limiting diagnostics match the claimed
  asymptotic direction: `Lambda+beta/x` is within about `1e-4` of `log 4`,
  and the `n,m,q,eta` limits have the expected small residuals.

These are asymptotic candidates and finite SCOUT checks.  They do not supply
the missing limiting proof `phi(beta)>0` plus a uniform remainder.

## Author JSON scans

The frozen `profile.json` reports:

- `25,702` high-precision grid evaluations;
- `120,000` deterministic float scout proposals;
- `0` negative hits.

The audit scan of exposed sigma fields found `165` sigma values and no
nonpositive value; the smallest exposed value is the reported
`4.00000000000000000000000000000000000000000000000083`.

The frozen `boundary_full_atom/asymptotic_results.json` scan found `320`
exposed sigma values and no nonpositive value.  This confirms consistency of
the recorded scout tables, not exhaustive coverage of the continuum.

## Final classification

- Analytic identities: PASS under the stated U10d/U8 dependency boundary.
- Full-atom rank-one pole and stable Schur formula: PASS.
- Boundary asymptotics: plausible SCOUT/BLOCKER refinement, not proved.
- Finite profile: SCOUT only.
- Global `sigma(x,c)>0`: OPEN / INCOMPLETE.

No critical gap was found in the reductions as reductions.  The remaining
gap is exactly the advertised two-variable logarithmic inequality, not an
implementation/accounting issue.
