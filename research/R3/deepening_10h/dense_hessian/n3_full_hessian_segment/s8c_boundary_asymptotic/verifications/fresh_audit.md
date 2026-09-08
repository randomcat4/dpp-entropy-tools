# D10-S8c boundary-asymptotic fresh non-author audit

STATUS: CORRECT.

Scope of this verdict: the D10-S8c candidate proves strict positive
definiteness of `B=-Hess H(K(t))` on the full six-dimensional `Sym(3)` basis,
equivalently strict negative definiteness of the full observation-coordinate
entropy Hessian, for every

```text
t in [29/100, 3/10).
```

The endpoint `t=3/10` is correctly excluded.  I found no critical gap.

I did not import `boundary_probe.py`, the S8/S8b author gate, or an author
Hessian module.  The independent script here reconstructs the n=3 event atoms
and Hessian jets from inclusion determinants and uses the JSON matrices only
as rational certificate witnesses.

Artifacts added:

- `fresh_s8c_audit.py`
- `fresh_s8c_audit.json`

## Files and hashes

Author files read:

| file | SHA-256 |
|---|---|
| `frozen_problem.md` | `39347ADA7E8A645736015F4CF23202786FFC83FF3319AFC6DE9783236DFCBBEF` |
| `proof_candidate.md` | `513C93B7CCC561A0E2C1630963C450147726EB8DBD7B1F1C8DC19FB981C5CB45` |
| `verdict.md` | `F5C60B7F43F08E8E223D2E67B8AE77F4F039C85DF3DCBC0440F4623F1FA762E3` |
| `boundary_probe.py` | `FCDBA3F63661F4F20143F9267B652635C8571F291E7C5F88CC508577849A545A` |
| `boundary_probe_results.json` | `2C257777B29D33B38C1AE5DE9C2E0ABA775BF43E13AB5038DFBF41C361EE45DA` |

New verification files:

| file | SHA-256 |
|---|---|
| `fresh_s8c_audit.py` | `0BAB46893F4F8B4D27C87E9C5C7A35AA259732783B2D252409A3A4171B4D9D30` |
| `fresh_s8c_audit.json` | `C236EEE25CE38DACF96D1163E05E78AEBCF54521937B2273962C86D5AA1F82AD` |

Command run from the repository root:

```text
python research/R3/deepening_10h/dense_hessian/n3_full_hessian_segment/s8c_boundary_asymptotic/verifications/fresh_s8c_audit.py
```

Exit code: `0`.

## 1. Strict feasibility and endpoint atom structure

The frozen line is

```text
K(t)=(1/5+t/5)U + (1/2+t/3)V + (4/5+2t/3)W,
```

where `U,V,W` are mutually orthogonal rank-one projections summing to `I`.
For `t in [29/100,3/10)`, all three eigenvalues lie in `(0,1)`.  At
`t=3/10`, the `W` eigenvalue reaches `1`, so the strict DPP domain ends there.
The half-open endpoint exclusion is therefore necessary.

Writing `s=3/10-t`, the complementary eigenvalues are

```text
a = 37/50 + s/5,
b = 2/5   + s/3,
c = (2/3)s.
```

The independent exact-event reconstruction gives endpoint atoms in mask order
`0,...,7`:

```text
(0, 37/210, 296/2625, 188/875, 37/5250, 311/1750, 136/875, 39/250).
```

Thus exactly the empty atom vanishes at `s=0`; all other seven atoms are
strictly positive, with minimum `37/5250`.

The empty atom polynomial in `s` is independently recovered as

```text
p_empty = (74/375)s + (49/225)s^2 + (2/45)s^3.
```

This verifies that the singularity is a single first-order empty-event
singularity.

## 2. Basis, scaling, and empty singular summand

The six frozen directions are checked entrywise against the JSON witness:

```text
F=(W, UW, VW, U, V, UV),
```

with the stated rational normalizations.  The Frobenius Gram matrix is diagonal:

```text
diag(1, 252/121, 49/24, 1, 1, 12/7).
```

Therefore these six directions form a basis of `Sym(3)`.  No Frobenius-gradient
conversion or restricted-direction argument is hidden here; positivity of
`B` in this coordinate basis is full `Sym(3)` positivity.

For `B=-Hess H`, the independent exact-event jets give the empty atom gradient

```text
g=(-ab,0,0,-bc,-ac,0)
```

and the only nonzero empty atom Hessian entries

```text
h03=h30=b,  h04=h40=a,  h34=h43=c,
h11=-2b*(126/121), h22=-2a*(49/48), h55=-2c*(6/7).
```

I also checked exactly that

```text
p_{S,00}=0 for every exact event S.
```

This is the load-bearing rank-one/affine fact that makes `G00` in the regular
seven-atom block nonnegative rather than logarithmically singular.

The singular decomposition

```text
B = gg^T/(abc) + h log(abc) + G
```

is consistent with the entropy Hessian identity

```text
B_ij = sum_S (p_{S,i}p_{S,j}/p_S + p_{S,ij} log p_S),
```

using `sum_S p_{S,ij}=0`.  This formula uses exact atoms obtained by Möbius
inversion of inclusion determinants, not `det(K_S)` as event probabilities.

Under the congruence scaling

```text
S(s)=diag(sqrt(s), ell^(-1/2), ell^(-1/2), 1, 1, 1),
ell=log(1/s),
```

the three singular diagonal coefficients checked are

```text
111/250, 504/605, 1813/1200,
```

and the finite `C0=G(0)[3:6,3:6]` block has exact rational interval
Gershgorin margins all positive; the minimum margin is approximately
`0.9885840928424285`.

This verifies the asymptotic model and the claim that the limiting scaled
matrix is positive definite.

## 3. Tail certificate on `[299/1000,3/10)`

The author uses `h=1/1000`, i.e.

```text
0 < s <= 1/1000,
t in [299/1000,3/10).
```

The independent script rebuilt the regular seven-atom interval matrix `G`,
the log bounds, the scalar Schur correction majorant, and the 5x5
preconditioned lower model.

The scalar split is valid:

- `A=B00 >= (111/250)/s`, because the empty pole contributes `ab/c` and the
  checked regular part has `G00=sum p_0^2/p >= 0`.
- The cross-vector terms satisfy
  `|b_i| <= u_i + v_i w(s)` with `w(s)=-log((74/375)s)` and nonnegative
  coefficients.
- For `k=0,1,2`,

  ```text
  d/ds [s w(s)^k] = w(s)^(k-1)(w(s)-k)
  ```

  with the `k=0` case interpreted as derivative `1`.  The certified lower log
  bound has `w>2`, so `s w(s)^k` is increasing on the tail.  This is exactly
  the needed bound; the proof does not use the false inequality `w(s)<=w(h)`.
- Hence

  ```text
  |b_i b_j / A|
  <= (h/(111/250)) (u_i+v_i w0)(u_j+v_j w0),
  ```

  where `w0` is an upper bound for `w(h)`, and the product monotonicity handles
  the fact that `w(s)` itself grows as `s->0`.

The true Schur complement equals a matrix in the certified interval model plus
a nonnegative diagonal matrix.  Therefore proving every matrix in the interval
model positive definite is sufficient.

Using the JSON's rational 5x5 upper-triangular `P` only as a witness, I checked:

- `P` has positive diagonal and denominator cap at most `4096`;
- exact interval arithmetic for `P^T[M]P` gives positive row-Gershgorin
  margins;
- minimum transformed margin is approximately `0.6499154101790116`.

Thus the tail certificate proves `B(t)>0` for the whole half-open tail
`[299/1000,3/10)`.

The endpoint `3/10` is not included: at `s=0`, `p_empty=0` and the entropy
Hessian is singular/not an interior strict-kernel object.

## 4. The `h=1/100` failure is only a failed bound

The independent recomputation confirms the retained coarse tail attempt
`h=1/100` does not certify positivity:

```text
plain model min margin        ~= -6.375935345981301
preconditioned model min      ~= -4.18852725571386
claimed attempt status        = failed
```

This is a failure of that scalar Schur majorant at the coarse radius, not a
positive-curvature example.  The smaller unused attempt `h=1/10000` also
passes, with transformed margin approximately `0.9600420442814791`, but it is
not needed once `h=1/1000` passes.

## 5. Six bridge leaves cover `[29/100,299/1000]`

For each saved bridge leaf I independently recomputed the full eight-atom
interval `B`, applied the saved rational 6x6 upper-triangular `P` witness, and
checked exact Gershgorin row margins.  All atom floors and all transformed row
margins are positive; every recomputed margin and atom lower bound matches the
JSON.

| leaf | interval | min transformed margin | min atom lower | max denominator in `P` |
|---:|---|---:|---|---:|
| 1 | `[29/100,1169/4000]` | `0.5834696984912537` | `49732931/36000000000` | 4096 |
| 2 | `[1169/4000,589/2000]` | `0.46706260451978204` | `334724951/360000000000` | 3943 |
| 3 | `[589/2000,1187/4000]` | `0.20663148368552395` | `345834859/720000000000` | 4084 |
| 4 | `[1187/4000,2383/8000]` | `0.44876638452330014` | `1949010557/5760000000000` | 4047 |
| 5 | `[2383/8000,191/640]` | `0.6375221550018593` | `19745713/73728000000` | 4072 |
| 6 | `[191/640,299/1000]` | `0.49451109149515343` | `2252609/14400000000` | 3571 |

Bridge accounting matches:

```text
accepted leaves: 6
failed final leaves: 0
rejected internal nodes retained: 5
processed nodes: 11
```

The leaf endpoints match exactly and cover the closed bridge
`[29/100,299/1000]` without gaps or overlaps.

## 6. Full interval conclusion

The bridge proves `B(t)>0` on the closed interval

```text
[29/100,299/1000].
```

The singular Schur majorant proves `B(t)>0` on the half-open tail

```text
[299/1000,3/10).
```

Their union is exactly

```text
[29/100,3/10).
```

Since the six basis directions span all of `Sym(3)`, this proves strict
negative definiteness of the full real-symmetric entropy Hessian throughout
the claimed half-open segment.  The proof is continuous-interval arithmetic,
not a finite grid or sampled scout.

At each interior point, ordinary continuity gives some ambient open
neighborhood with the same Hessian sign.  No uniform endpoint neighborhood,
no endpoint statement at `3/10`, and no global DPP entropy concavity claim is
made.

## Final verdict

STATUS: CORRECT.

The key fragile points requested in the task all pass:

- exact-event/Möbius semantics are used;
- only the empty atom vanishes, linearly in `s`;
- all seven other endpoint atoms are positive;
- the singular scaling and finite block are reconstructed;
- the scalar Schur majorant uses monotonicity of `s*(-log(c0s))^k`, not a
  false monotonic bound on `-log s`;
- the model-matrix plus nonnegative-diagonal argument is sufficient;
- `[299/1000,3/10)` is covered uniformly as a half-open tail;
- six exact rational bridge leaves cover `[29/100,299/1000]`;
- `t=3/10` is excluded;
- `h=1/100` remains only a failed certificate attempt, not a counterexample.
