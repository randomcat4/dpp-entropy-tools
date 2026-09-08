STATUS: CORRECT

# D10-H2 fresh non-author verification

Scope: this is a fresh verification of the D10-H2 round6 analysis artifacts in
`dense_hessian/results_server_round6/` and `dense_hessian/server_round6_analysis/`.
It does not revise the author's statements, does not certify novelty, and does
not upgrade the finite source ledger to a theorem.

New files written in this verification directory:

- `fresh_h2_audit.py`
- `fresh_h2_audit.json`
- `fresh_reduction.md`

The verification script does not import the author's `recheck.py`,
`decimal_recheck.py`, or `subspace_probe.py`.

## 1. Frozen input and source denominator

The verified frozen file is:

```text
results_server_round6/best_mechanism_case.npz
```

SHA-256:

```text
e614dff920277e60929a6f8e1cfb37bd19d7c8d30a6a61a9488c424a8eb7ff3f
```

The raw kernel has maximum antisymmetric residue
`5.551115123125783e-17`; the direction is symmetric to displayed precision.
I used the same natural frozen input convention as the author analysis:
\((K+K^T)/2\), changing the kernel by at most
`2.7755575615628914e-17`.

The source ledger has exactly 160 rows:

- \(n=12,13\);
- four modes per dimension;
- 20 centers per mode;
- no row has positive `lambda_max`;
- maximum mechanism ratio in the ledger is the \(n=12\), mode 1 value
  `0.5261099452386901`.

This 160-row ledger is only a source statistic.  This verification independently
recomputes the frozen maximum-mechanism point and the commuting subspace at that
point; it does not replay all 160 centers.

## 2. Exact-event semantics

For an exact atom \(Y=S\), I checked the mixed determinant formula

\[
p_S=(-1)^{n-|S|}\det\left(K-\operatorname{diag}(1_{i\notin S})\right).
\]

This follows from the inclusion-to-exact Möbius inversion

\[
p_S=\sum_{T\supseteq S}(-1)^{|T|-|S|}\det K_T
\]

by expanding the determinant after subtracting \(1\) from each absent diagonal
coordinate.

For all \(2^{12}=4096\) atoms at the frozen center, the independent float check
found:

- mixed probabilities sum to exactly `1.0` in the reported float reduction;
- minimum mixed atom probability `3.488201486707941e-14`;
- direct Möbius vs mixed determinant maximum absolute error
  `5.656142040774439e-16`;
- direct Möbius negative atoms: `0`;
- direct Möbius maximum relative error `0.007564734476828637`, occurring only
  because the rarest probabilities are near \(10^{-14}\);
- \(L\)-ensemble formula \(p_S=\det(I-K)\det L_S\) vs mixed determinant maximum
  relative error `4.742747055311838e-12`.

Thus the author's event law is the exact-event law, not an accidental use of
inclusion probabilities as atoms.  The direct double-precision Möbius relative
error is not suitable as a rare-event relative certificate, but the absolute
agreement and independent Decimal mixed-event computation support the event
semantics used in the analysis.

## 3. Curvature and rho scale

I use

\[
F_+=\sum_S \frac{(p'_S)^2}{p_S}\ge0,\qquad
A=-\sum_S p''_S\log p_S,\qquad
H''=A-F_+,\qquad \rho=A/F_+ .
\]

For the frozen direction with operator norm about one, the independent 70-digit
Decimal mixed-event recomputation gives:

```text
F+  = 43.19824944843413487190238082819478306469466408684632762792636186730663
A   = 22.72702865172296624995269324687621419198578139057089395520867742181976
H'' = -20.47122079671116862194968758131856887270888269627543367271768444548687
rho = 0.5261099452386903022235153661915919777542027405282614574971567686582644
```

Normalization identities are also stable:

```text
sum p   = 1.000000000000000000000000000000000000000000000000000000000000000000000
sum p'  = 1.04967E-69
sum p'' = 5.294E-69
```

This verifies that the total curvature is strictly negative at the frozen point.
The counterexample threshold remains \(\rho>1\), not \(\rho>1/2\).

Scale invariance was independently checked by scaling \(D\) by
\(1/\sqrt{F_+}\), \(0.5\), \(-2\), and \(3\).  The ratio \(\rho\) changed by at
most about `4.2e-15`, and \(H''\) scaled by \(c^2\).  Under Fisher
normalization the recomputed values are:

```text
F+ = 0.9999999999999984
A  = 0.5261099452386907
H'' = -0.47389005476130774
```

This matches the author's convention where the Fisher contribution is recorded
as the negative term `-1`.

## 4. Strict feasible chord and PSD direction certificate

Interpreting the symmetrized float64 entries as exact decimal rationals via
`repr(float)`, an exact Fraction LDL check verifies:

- \(D\succ0\), hence \(D\) is PSD and has rank 12;
- all 12 LDL pivots of \(D\) are positive;
- the smallest \(D\) pivot has float value about `0.17893148887934393`;
- for \(t=-10^{-4},0,10^{-4}\),
  \(K+tD-\frac1{20000}I\succ0\);
- for \(t=-10^{-4},0,10^{-4}\),
  \(I-K-tD-\frac1{20000}I\succ0\).

Because these shifted matrices depend affinely on \(t\), convexity of the
positive definite cone gives the same strict margin throughout
\(|t|\le10^{-4}\).  This verifies that the recorded finite chord is a genuine
strictly feasible \(K\)-space chord in a PSD direction.

The 70-digit Decimal entropy chord at \(h=10^{-5}\) is also negative:

```text
midpoint gap = -1.023561041449442714811779092E-9
central H2   = -20.47122082898885429623558184
```

The small discrepancy from analytic \(H''\) has the expected \(O(h^2)\) sign and
does not affect the negative verdict.

## 5. Commuting subspace and the limited "non-commuting not necessary" claim

At the same frozen center, I recomputed the generalized ratio on the subspace
spanned by \(q_iq_i^T\), where \(q_i\) are the orthonormal eigenvectors of
\(K\).  This is exactly the subspace of symmetric directions commuting with
\(K\), up to numerical eigensolver precision.

Independent recomputation gives:

```text
commuting subspace dimension = 12
rho_max = 0.5133580085580273
directional rho recheck = 0.5133580085580286
commutator Frobenius norm = 1.0828958760226503e-15
direction eigenvalue range = [0.13927773579087258, 0.9999999999999996]
H'' along commuting direction = -29.3503630324409
```

Thus the statement "non-commuting is not necessary" is correct only in the
limited diagnostic sense used by the author: a commuting PSD direction already
achieves a mechanism ratio above \(1/2\) at this finite frozen center.  It is
not a counterexample, since \(\rho<1\) and the total curvature remains negative.
It is also not a theorem about all commuting directions or all DPP kernels.

## 6. Verdict

The D10-H2 round6 analysis is correct within its stated scope:

- the maximum-mechanism frozen NPZ uses exact-event atoms;
- the reported \(\rho\) is scale-invariant and matches Fisher normalization;
- independent high-precision Decimal recomputation gives negative total
  curvature;
- exact rational LDL checks certify a strict feasible PSD \(K\)-chord for
  \(|t|\le10^{-4}\);
- the commuting subspace ratio near `0.51336` is reproducible;
- the "non-commuting not necessary" conclusion is properly limited to the
  finite diagnostic mechanism ratio and is not advertised as a positive gap.

No positive R3 counterexample is certified here.  The global real DPP entropy
question remains `INCOMPLETE`.
