# D10-S8e stitched full-line dependency audit

STATUS: CORRECT.

This is a short non-author dependency audit of `full_feasible_line.md`.  I did
not rerun the large interval arithmetic; I checked the stitched statement
against the already fresh-audited S8/S8b/S8c/S8d certificates, their hashes,
their interval endpoints, and their stated quantifiers.

## Frozen dependency hashes

| dependency | SHA256 |
| --- | --- |
| `full_feasible_line.md` | `8C22CCE5E0319402928A04BF22A215D2AF7A418070712D76E8D9DAC2B0129B06` |
| `verifications/fresh_audit.md` | `6187BAE5E504A9AFB1E8A9483F28FEACB58DF5F832B1F96A61B58DDC60772E57` |
| `s8b_verifications/fresh_audit.md` | `633F3D1F618C272BFEF5F7C78D29608338E2AE6985F8C5FA139B47ED1142486E` |
| `s8c_boundary_asymptotic/verifications/fresh_audit.md` | `68EFA6DBE070C61A22D5F3B77FD8546B2CDB74DA4831AF6A86CF6D0CB523C2DC` |
| `s8d_negative_boundary_asymptotic/verifications/fresh_audit.md` | `40CD7D6795D6957320C00524B446C7690091FA68334D2C8F97CE1E80DADAEC19` |
| `ARTIFACTS.md` | `8CC52566E95621A31BA314C5D61B0020BD677F12FC1DB1EAF7FFB3D7D85A7B17` |

Only this `full_line_verifications/` directory was written.

## 1. Maximal strict feasible interval

The frozen line is

```text
K(t)=(1/5+t/5)U + (1/2+t/3)V + (4/5+2t/3)W,
```

where `U,V,W` are mutually orthogonal rank-one projections summing to `I`.
Therefore the three eigenvalues are

```text
lambda_U=(1+t)/5,
lambda_V=1/2+t/3,
lambda_W=4/5+2t/3.
```

Strict feasibility `0<K(t)<I` gives:

- `lambda_U>0` iff `t>-1`, and `lambda_U<1` iff `t<4`;
- `lambda_V>0` iff `t>-3/2`, and `lambda_V<1` iff `t<3/2`;
- `lambda_W>0` iff `t>-6/5`, and `lambda_W<1` iff `t<3/10`.

The intersection is exactly

```text
(-1, 3/10).
```

Thus `full_feasible_line.md` correctly identifies the maximal strict feasible
interval.  The endpoint `-1` is excluded because `lambda_U=0`; the endpoint
`3/10` is excluded because `lambda_W=1`.

## 2. Interval stitching

The three reviewed certificates state:

- S8d fresh audit: CORRECT for `-1 < t <= -29/100`;
- S8b fresh audit: CORRECT for `[-29/100, 29/100]`;
- S8c fresh audit: CORRECT for `[29/100, 3/10)`.

The seams are covered:

```text
-29/100 is included by S8d and S8b,
 29/100 is included by S8b and S8c.
```

Hence the union is exactly

```text
(-1, -29/100] union [-29/100, 29/100] union [29/100, 3/10)
= (-1, 3/10).
```

There is no gap, no open seam, and no accidental inclusion of either strict
feasibility endpoint.

## 3. Full Hessian scope, not merely line curvature

The dependency audits certify the full six-dimensional observation-coordinate
matrix `B=-Hess H` in a basis of `Sym(3)`:

- S8 base audit explicitly checks coordinates `(11,22,33,12,13,23)` and
  positive definiteness of the raw six-coordinate `B`.
- S8b audit checks the same exact-event full Hessian under leafwise rational
  congruences and states that it covers every nonzero real symmetric direction,
  including noncommuting PSD/NSD and indefinite directions.
- S8c audit checks a six-element basis of `Sym(3)` with diagonal Gram matrix
  and proves `B(t)>0` on the bridge plus right tail.
- S8d audit likewise checks a six-coordinate full `Sym(3)` basis and proves
  `B(t)>0` on the left bridge plus singular tail.

Thus `full_feasible_line.md` correctly says the stitched conclusion is about
the complete full `Sym(3)` entropy Hessian, not merely about the tangent to the
affine line, commuting spectral directions, or a PSD cone.

## 4. Openness and non-claims

At every fixed `t` in `(-1,3/10)`, the kernel is strict and the Hessian is
strictly negative definite.  The DPP exact-event atoms and the Hessian vary
continuously on the strict kernel domain, and the largest Hessian eigenvalue is
strictly negative at that fixed point.  Therefore each point of the line has an
ordinary ambient open neighborhood on which the Hessian remains negative
definite.

This pointwise openness does not supply:

- one uniform ambient radius over the whole open interval `(-1,3/10)`;
- a neighborhood through either endpoint;
- concavity on the whole `n=3` DPP kernel domain;
- a statement for other affine lines.

`full_feasible_line.md` makes exactly these exclusions, so I found no scope
overreach.

## Final verdict

CORRECT.  The feasible interval calculation, interval cover, seam inclusion,
full-`Sym(3)` dependency scope, and local-openness/non-global boundaries are
consistent with the frozen and fresh-audited dependencies.
