INCOMPLETE

# P4-02 n=3 event-coordinate second variation

## Inputs read first

- `phase4_scope.md`
- `frozen_n3_concavity_v1.md`

No R2 or R3 directory was entered. No remote job was run, no dependency was
installed, and no GPU was used.

## Status

I did not find a counterexample, but I also did not obtain a PSD/SOS
certificate or complete proof for the frozen `3x3` concavity statement.

The useful output of this work unit is an explicit eight-event tangent-space
second-variation formula. It reduces the proof obligation to a concrete
six-variable logarithmic quadratic inequality for each strict feasible `K`.

## Explicit event coordinates

Write

```text
K = [[a, x, y],
     [x, b, z],
     [y, z, c]]
```

and a real symmetric direction as

```text
V = [[A, X, Y],
     [X, B, Z],
     [Y, Z, C]].
```

The DPP inclusion probabilities are

```text
q_0   = 1
q_1   = a
q_2   = b
q_3   = c
q_12  = ab - x^2
q_13  = ac - y^2
q_23  = bc - z^2
q_123 = abc + 2xyz - az^2 - by^2 - cx^2.
```

The full event probabilities are obtained by Boolean Mobius inversion:

```text
p_111 = q_123
p_110 = q_12 - q_123
p_101 = q_13 - q_123
p_011 = q_23 - q_123
p_100 = q_1 - q_12 - q_13 + q_123
p_010 = q_2 - q_12 - q_23 + q_123
p_001 = q_3 - q_13 - q_23 + q_123
p_000 = 1 - q_1 - q_2 - q_3 + q_12 + q_13 + q_23 - q_123.
```

This is the complete event law; no principal minor is used as an exact event
probability.

## First and second inclusion jets

Along `K(t)=K+tV`, define

```text
r_1   = A
r_2   = B
r_3   = C
r_12  = Ab + aB - 2xX
r_13  = Ac + aC - 2yY
r_23  = Bc + bC - 2zZ
r_123 = Abc + aBc + abC
        + 2(Xyz + xYz + xyZ)
        - Az^2 - 2azZ
        - By^2 - 2byY
        - Cx^2 - 2cxX.
```

The second inclusion jets are

```text
s_1   = s_2 = s_3 = 0
s_12  = 2AB - 2X^2
s_13  = 2AC - 2Y^2
s_23  = 2BC - 2Z^2
s_123 = 2(ABc + ACb + BCa)
        + 4(XYz + XZy + YZx)
        - 2aZ^2 - 4AzZ
        - 2bY^2 - 4ByY
        - 2cX^2 - 4CxX.
```

Applying the same Mobius map gives event first derivatives `u=p'`:

```text
u_111 = r_123
u_110 = r_12 - r_123
u_101 = r_13 - r_123
u_011 = r_23 - r_123
u_100 = r_1 - r_12 - r_13 + r_123
u_010 = r_2 - r_12 - r_23 + r_123
u_001 = r_3 - r_13 - r_23 + r_123
u_000 = -r_1 - r_2 - r_3 + r_12 + r_13 + r_23 - r_123.
```

The event second derivatives `w=p''` are:

```text
w_111 = s_123
w_110 = s_12 - s_123
w_101 = s_13 - s_123
w_011 = s_23 - s_123
w_100 = -s_12 - s_13 + s_123
w_010 = -s_12 - s_23 + s_123
w_001 = -s_13 - s_23 + s_123
w_000 = s_12 + s_13 + s_23 - s_123.
```

These satisfy

```text
sum_s u_s = 0,    sum_s w_s = 0.
```

## Exact entropy second variation

For a strict interior `K`, all `p_s>0`, so entropy is smooth in a neighborhood
of `K`. Using `sum_s w_s=0`, the second derivative is exactly

```text
D^2 H(K)[V,V]
 = - sum_s u_s^2 / p_s - sum_s w_s log(p_s).
```

Therefore the frozen `n=3` concavity candidate is equivalent to the following
explicit residual inequality:

```text
R(K,V) := sum_s u_s^2 / p_s + sum_s w_s log(p_s) >= 0
```

for every strict `3x3` real symmetric DPP kernel `K` and every real symmetric
direction `V` for which the considered chord stays feasible.

This is a smaller, fully explicit event-coordinate obligation, but I did not
complete a proof that `R(K,V)>=0` for the full six-dimensional direction
space.

## Conditional entropy trap checked

The conditional-entropy route cannot directly invoke the two-dimensional
candidate. For example, conditioning on `X_3=1` gives a two-point conditional
kernel involving a Schur-complement term of the form

```text
K_{12} - K_{12,3} K_{3,12}/K_33.
```

Along an affine line `K+tV`, entries such as

```text
(y+tY)(z+tZ)/(c+tC)
```

are not affine in `t`. Conditioning on `X_3=0` similarly introduces a
non-affine complement-side kernel and non-affine mixture weights. Thus
two-dimensional concavity, even if true, cannot be applied directly to these
conditional kernels without an additional argument controlling the non-affine
parameterization and the changing mixture weights.

## Bounded falsification probe

Replay command from this directory:

```text
python n3_formula_probe.py
```

Recorded log:

```text
n3_probe_summary.json
```

The probe computed the full-event Hessian matrix using inclusion determinant
derivatives followed by Boolean Mobius inversion. It then sampled random
strict `3x3` kernels and tested the largest Hessian eigenvalue.

Finite scan denominator:

```text
20,000 Hessian samples
seed = 2026090842
failures = 0
positive samples > 1e-8 = 0
positive samples > 1e-10 = 0
```

Best sampled Hessian value:

```text
call = 17780
max Hessian eigenvalue = -1.710572103104059e-08
eigen residual = 8.737839634152166e-16
spectral margin = 0.1432240385824012
minimum event probability = 0.0031224014398169514
small feasible chord gap = -1.3492219386179727e-06
```

This scan is only a probe. It is not a proof of the frozen statement.

## Exact rational sanity

The script also checked one exact-rational `3x3` chord with full event
probabilities computed exactly by Mobius inversion.

Probability sums:

```text
minus  = 1
center = 1
plus   = 1
```

Minimum exact event probabilities:

```text
minus  = 568434484087/18162144000000
center = 11471/360000
plus   = 45234508541/1397088000000
```

Numerical entropy midpoint gap from exact probabilities:

```text
-0.00014667330940332235
```

Again, this is only a sanity check.

## Failures and exit codes

- A check for `sympy` failed because it is not installed. No dependency was
  installed; the formulas above were derived and implemented directly.
- `n3_formula_probe.py` exit code: `0`.

## Next proof obligation

The next useful target is to prove or refute the explicit residual inequality

```text
sum_s u_s^2 / p_s + sum_s w_s log(p_s) >= 0
```

under the strict DPP feasibility constraints for the eight Mobius event
probabilities listed above. A valid completion would be a PSD/SOS certificate,
a monotonicity argument for the logarithmic term, or an explicit feasible
`K,V` making this residual negative.
