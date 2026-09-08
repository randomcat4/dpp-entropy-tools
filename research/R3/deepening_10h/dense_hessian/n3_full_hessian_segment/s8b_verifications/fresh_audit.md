# D10-S8b non-author independent audit

STATUS: **CORRECT for the continuous full-Hessian certificate on
[-29/100,29/100].** The attempted radius 299/1000 remains **INCOMPLETE**.
No critical gap requiring author repair was found.

## 1. Frozen versions and independent implementation boundary

Author hashes were frozen before calculation and checked unchanged afterward:

| File | SHA256 |
| --- | --- |
| s8b_expansion.md | 79e4d5678bc0b237b1bdfd57670ecc4fd6be269db7197079515c8319a7f77881 |
| s8b_verdict.md | b66944993d2b5e38da154062ca21f4016904f8fc943540ec2d1228d420f4da21 |
| s8b_run_log.md | 1b698eea922d7fe7d28e7a44543216c1189b5cfb29300227949b0ab047d972a5 |
| s8b_preconditioned_expansion.py | ea4fdc50244410b926f0edb044a710f3953d41bf6f306207c63e4e6e0612553e |
| s8b_preconditioned_certificate.json | 6f71b1af86f9a51cc74330498278fbcb406158645a6a60d14dfc5309b57dfecd |

The certificate's embedded script hash matches the actual author script.

No author S8 or S8b module was imported or executed. I read and reused only
the already independently audited NON-AUTHOR helper
`verifications/fresh_s8_audit.py`, SHA256
`2eba997abe32602ac1e8139a9ccaa09999a330d9af735dad136a20fd58149e5a`.
It was used to reconstruct all exact-event atom jets and their interval
Hessian from the rational line, not to accept an author Hessian matrix.
The new P^T B P interval transformation, leaf accounting, coverage proof,
and preconditioner checks are independently implemented here. Bytecode writes
were disabled; only the new `s8b_verifications/` directory was written.

## 2. Exact-event Hessian and coordinate semantics

The reconstructed line agrees exactly with the frozen rational matrices:

    K(t)=K0+tR,
    K0=(1/5)U+(1/2)V+(4/5)W,
    R=(1/5)U+(1/3)V+(2/3)W.

Here U=J/3, V=(1,2,-3)(1,2,-3)^T/14 and W=I-U-V. For all eight subsets,
the helper independently constructs principal inclusion determinant polynomials
and Mobius-inverts them. It separately checks the signed exact-event identity
p_S(K)=(-1)^|S^c|det(K-I_{S^c}) for every direction jet used.

Coordinates are (11,22,33,12,13,23), with off-diagonal directions Eij+Eji.
Mass and its first and second coordinate derivative identities hold exactly
as polynomials in t. Therefore

    B_ij(t) = sum_S p_i p_j/p + sum_S p_ij log p

is the full matrix of -Hess H, with the otherwise present constant p_ij term
cancelled by normalization. It is not a spectral-direction projection or a
matrix assembled from inclusion probabilities misread as exact atoms.

Each leaf's polynomial values are enclosed by rational interval Horner
arithmetic. Logarithms are enclosed using the 20-term range-reduced atanh
series with its explicit positive remainder. Products use all four endpoint
products; division by an atom interval is done only after its lower endpoint
has been checked strictly positive. Negative scalar factors reverse the
interval endpoints. These operations preserve inclusion even when dependency
is lost, which can weaken a bound but cannot produce a false positive.

## 3. Leaf coverage and complete denominator accounting

All 67 saved leaf intervals were sorted and checked exactly. Every leaf has
positive rational length, the first begins at -29/100, the last ends at
29/100, and each leaf's right endpoint equals the next leaf's left endpoint.
Thus the union is the full CLOSED interval with neither gaps nor interior
overlap. Shared endpoints are covered by both adjacent certificates.

The 67 leaves comprise precisely:

| Method / rounding cap | Leaves |
| --- | ---: |
| Plain coordinate Gershgorin | 2 |
| Preconditioned, denominator cap 64 | 61 |
| Preconditioned, denominator cap 256 | 3 |
| Preconditioned, denominator cap 4096 | 1 |
| Total | 67 |

Thus there are 65 preconditioned leaves and 2 plain leaves, with 66 splits,
zero failed leaves and a successful root interval, matching the largest-radius
summary. No leaf used the 1024 cap. The caps are limits on each rational
entry's denominator, not assertions that every entry has a common denominator
64, 256, or 4096. Every actual stored denominator was checked against its cap.

The earlier smaller-radius leaf counts were not independently regenerated:
the saved full leaf ledger is for the largest radius. The mathematical claims
on 49/200, 1/4 and 7/25 are nonetheless certified as subintervals of this
independently covered larger interval. This audit does not treat un-replayed
historical run counts as an additional certificate.

## 4. Preconditioner invertibility and interval multiplication

For each of the 65 rational P matrices, I checked dimensions 6 by 6, every
entry below the diagonal exactly zero, every diagonal entry strictly positive,
and equality of the separate saved diagonal list to the matrix diagonal.
Its determinant is the exact product of the six diagonal entries and is
strictly positive. Hence P is invertible without any float singular-value
test or assumption about Cholesky approximation accuracy.

The author proposes P by taking a numerical Cholesky factor B(m)=LL^T and
approximating L^(-T), which is the correct ideal orientation for P^T B P=I.
This numerical proposal is not needed for the proof. An arbitrary fixed
rational invertible P would be acceptable if the subsequent interval test
passes. P is held constant on its whole leaf; it is not silently allowed to
vary with t inside the interval multiplication.

The independent transform computes every entry as

    (P^T B P)_ab = sum_{i,j} P_ia P_jb B_ij.

For each rational coefficient c=P_ia P_jb, [l,u] contributes [cl,cu] if
c>=0 and [cu,cl] if c<0. All 36 transformed entries were independently
computed, including the lower triangle, and exact symmetry was checked.
Negative multipliers are explicitly counted in the output; they occur in the
actual certificate and were not ignored. The two plain leaves use P=I.

For each transformed interval matrix T, the checked row margins are

    lower(T_ii)-sum_{j!=i}max(|lower(T_ij)|,|upper(T_ij)|).

Every row is strictly positive on every leaf. Each leaf's minimum margin
agrees EXACTLY, as a Fraction, with the author-saved value. This equality is
stronger than merely agreeing in the displayed decimals.

## 5. Margins, structure and pushing the congruence back

Across all leaves the minimum transformed/working-coordinate Gershgorin margin is

    0.000409651436370431053043705705589238377820078122848412121550135...

Its exact rational value is retained in the independent JSON, as are all six
row margins for each leaf. The smallest atom lower bound is exactly

    15168331/7680000000 > 0.

The affine eigenvalues are (1/5+t/5,1/2+t/3,4/5+2t/3). Exact endpoint and
root checks on |t|<=29/100 establish:

| Quantity | Uniform lower bound |
| --- | ---: |
| Distance of eigenvalues from {0,1} | 1/150 |
| Absolute off-diagonal entry | 1067/15750 |
| Gap between coordinate diagonal entries | 61/1400 |
| Gap between eigenvalues | 61/300 |

All off-diagonal zero roots (-153/128,-171/106,-45/8), diagonal-equality roots
(-9/10), and spectral-collision roots (-9/4,-9/7,-9/10) lie outside the closed
interval. The whole line segment is therefore strict, genuinely connected,
heterogeneous, and simple-spectrum.

For a fixed leaf and any t in it, interval Gershgorin proves T(t)=P^T B(t)P
positive definite. If x!=0, let y=P^(-1)x; then y!=0 and

    x^T B(t)x = y^T T(t)y > 0.

This is congruence, not similarity. It proves B(t) positive definite in all
six real observation coordinates and hence H''[D,D]<0 for every nonzero
real symmetric D, including noncommuting PSD/NSD and indefinite directions.
There is no Frobenius-gradient or off-diagonal factor conversion in this
negative-definiteness implication.

The minimum displayed preconditioned margin is NOT automatically a lower
bound for the raw B matrix, because the leaves use different P. For clarity,
the independent output also stores a conservative raw-coordinate bound
m_leaf/||P||_F^2 (m_leaf for plain leaves), derived from
||Py||<=||P||_F||y||. All are positive, and their minimum gives a genuine
common positive raw B bound. No unjustified transfer of the numerical margin
is needed in the author's stated strict-definiteness theorem.

For compact display, the independent JSON additionally saves B and P^T B P
intervals rounded OUTWARD to rational multiples of 10^-24. Every leaf also
passes Gershgorin on these enlarged stored intervals, making the display
rounding itself harmless. Original exact row margins and complete rational
P data are retained separately.

## 6. Radius 299/1000 and finite scout boundary

The manual attempt is saved as TIMEOUT_INTERRUPTED with strict spectral margin
1/1500. It has no completed interval certificate in these artifacts, and I
did not rerun that timed-out search. Its correct mathematical status is
INCOMPLETE: neither a failed concavity theorem nor a positive-curvature
counterexample. The 401-point float diagnostics at either radius are not used
anywhere in this proof and do not certify an extension to 299/1000 or to 3/10.

The local line theorem does not imply global entropy concavity, a result on
all M8 product-region points, or an extension toward the negative feasibility
endpoint -1. The author's boundaries are respected.

## 7. Independent execution and evidence

Command from the repository root, local bundled Python 3.12:

```
python research/R3/deepening_10h/dense_hessian/n3_full_hessian_segment/s8b_verifications/independent_s8b_check.py
```

Exit 0; elapsed 16.718987226486206 seconds. No failed checks, author-version
drift, random proposals, or float grid used for proof. The complete denominator
is 67 leaves, 536 atom leaf-intervals, 2412 full Hessian entry leaf-intervals,
65 rational preconditioners and 2 identity preconditioners. Every stored leaf
was checked, not a sample.

Independent script SHA256:
`de4d781ce4245aa253058898a0fc5a7392cddf0b336112c2493c98715f502906`

Independent results SHA256:
`d9ba966a4a37eeb71774a7527046f9ede7005b3711868faf87a1476c4a0a47c1`

Artifacts added only under `s8b_verifications/`: this report, the independent
script and its JSON. No author file or shared index was modified and no
submission was made. Final verdict: CORRECT for the frozen expanded segment;
the timed-out larger radius remains INCOMPLETE.
