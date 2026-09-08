STATUS: CORRECT

# Fresh verification of `uniform_flat_ridge`

Role: non-author verifier.  I did not modify the author files.

## Files read and checks run

Read:

- `research/R3/deepening_10h/uniform_flat_ridge/frozen_claim.md`
- `research/R3/deepening_10h/uniform_flat_ridge/proof.md`
- `research/R3/deepening_10h/uniform_flat_ridge/sanity.py`
- `research/R3/deepening_10h/uniform_flat_ridge/verdict.md`

Ran:

```text
python uniform_flat_ridge/sanity.py
```

Current author sanity result:

```text
{'status': 'PASS', 'events': 16, 'quartic_coefficient': '112683008881/315059220000'}
exit code: 0
```

I also added and ran an independent standard-library n=3 exact symbolic check
inside this verification directory:

```text
python uniform_flat_ridge/verifications/fresh_symbolic_check.py
```

Result:

```text
status: PASS
exit code: 0
```

The independent script wrote `fresh_symbolic_check.json`.

## 1. Uniform exact-event formula

For \(S\subseteq[n]\), define

\[
z_i=\begin{cases}
1,&i\in S,\\
-1,&i\notin S,
\end{cases}
\qquad
Z_S=\operatorname{diag}(z_i).
\]

The exact DPP atom formula is

\[
p_S(t)=(-1)^{|S^c|}\det(K(t)-I_{S^c}).
\]

For

\[
K(t)=\frac12I+tD,
\]

the diagonal entries of \(K(t)-I_{S^c}\) are \(z_i/2+tD_{ii}\), and the
off-diagonal entries are \(tD_{ij}\).  Since
\(\det Z_S=(-1)^{|S^c|}\),

\[
p_S(t)
=\det Z_S\det\left(\frac12Z_S+tD\right)
=\det\left(\frac12I+tZ_SD\right)
=2^{-n}\det(I+2tZ_SD).
\]

This matches `proof.md` lines 3--13.  It uses exact atoms, not inclusion
probabilities.

## 2. Hessian at \(K=I/2\)

At \(t=0\), every atom is

\[
u=2^{-n}.
\]

From the event formula,

\[
\frac{p'_S(0)}u
=2\operatorname{tr}(Z_SD)
=2\sum_i z_iD_{ii}.
\]

For entropy,

\[
H''(0)
=-\sum_S\frac{(p'_S(0))^2}{p_S(0)}
-\sum_Sp''_S(0)\log p_S(0).
\]

The second sum vanishes because \(\log p_S(0)\) is constant and
\(\sum_Sp''_S(0)=0\).  Averaging over independent Rademacher signs gives

\[
H''(I/2)[D,D]
=-\mathbb E\left(2\sum_i z_iD_{ii}\right)^2
=-4\sum_iD_{ii}^2.
\]

Thus the Hessian nullspace is exactly the set of symmetric directions with
zero diagonal.  This verifies `frozen_claim.md` claim 1 and `proof.md` lines
16--40.

The independent n=3 check used a different general symmetric direction and
found exactly:

```text
general_hessian = -469/900
expected_general_hessian = -469/900
```

## 3. Zero-diagonal quartic coefficient

Assume \(\operatorname{diag}D=0\).  Then

\[
\operatorname{tr}(Z_SD)=0.
\]

Using the second-order determinant expansion,

\[
\det(I+2tZ_SD)
=1-2t^2\operatorname{tr}(Z_SDZ_SD)+O(t^3).
\]

Since \(D\) is symmetric and has zero diagonal,

\[
\operatorname{tr}(Z_SDZ_SD)
=2\sum_{i<j}z_iz_jD_{ij}^2.
\]

Hence

\[
r_S(t):=\frac{p_S(t)}u-1
=-4t^2\sum_{i<j}z_iz_jD_{ij}^2+O(t^3).
\]

Because

\[
H(p)=n\log2-\mathrm{KL}(p\|u),
\qquad
(1+r)\log(1+r)=r+\frac12r^2+O(r^3),
\]

and \(\mathbb E_u r=0\), the quartic coefficient of the KL term is

\[
\frac12\mathbb E_u
\left[
\left(-4\sum_{i<j}z_iz_jD_{ij}^2\right)^2
\right].
\]

The Rademacher characters \(z_iz_j\) are orthogonal for distinct unordered
pairs, so

\[
\mathbb E_u r^2
=16t^4\sum_{i<j}D_{ij}^4+O(t^5).
\]

Therefore

\[
H\left(\frac12I+tD\right)
=n\log2-8t^4\sum_{i<j}D_{ij}^4+O(t^5).
\]

The complement symmetry below removes the possible odd \(t^5\) term, giving
the claimed

\[
H\left(\frac12I+tD\right)
=n\log2-8t^4\sum_{i<j}D_{ij}^4+O(t^6).
\]

This verifies `frozen_claim.md` claim 2 and `proof.md` lines 42--83.

The independent n=3 zero-diagonal check used off-diagonal entries
\(1/3,-2/5,1/7\) and found exactly:

```text
zero_diag_H_t4 = -37303568/121550625
expected_zero_diag_H_t4 = -37303568/121550625
```

## 4. Complement evenness

The complement of a DPP with marginal kernel \(K\) has marginal kernel
\(I-K\).  Here

\[
I-K(t)=\frac12I-tD=K(-t).
\]

Complementation is a bijection on subsets and preserves Shannon entropy, so

\[
H(K(t))=H(K(-t)).
\]

Thus the entropy Taylor expansion at zero is even.  This justifies replacing
the \(O(t^5)\) remainder after the quartic calculation by \(O(t^6)\).

The independent n=3 symbolic check also verified the atom-level parity

\[
p_S(t)=p_{S^c}(-t)
\]

for all eight atoms.

## 5. Punctured radial negative curvature

For nonzero zero-diagonal \(D\),

\[
C=8\sum_{i<j}D_{ij}^4>0.
\]

The expansion is

\[
H(K(t))=n\log2-Ct^4+O(t^6).
\]

Differentiating twice gives

\[
\frac{d^2}{dt^2}H(K(t))
=-12Ct^2+O(t^4)
=-96t^2\sum_{i<j}D_{ij}^4+O(t^4).
\]

For all sufficiently small nonzero \(t\), the negative leading term dominates.
Thus every fixed nonzero zero-diagonal Hessian-null ray has strictly negative
punctured radial curvature.  This verifies `frozen_claim.md` claim 3 and
`proof.md` lines 85--87.

The independent n=3 check found exactly:

```text
zero_diag_radial_second_t2 = -149214272/40516875
expected_zero_diag_radial_second_t2 = -149214272/40516875
```

## 6. Uniform DPP uniqueness

The entropy of any law on \(2^n\) outcomes is at most \(n\log2\), with equality
only for the uniform law.  If a strict real DPP law is uniform, then

\[
\Pr(i\in Y)=\frac12,
\qquad
\Pr(i,j\in Y)=\frac14.
\]

The DPP inclusion probabilities give

\[
K_{ii}=\frac12,
\]

and for \(i\ne j\),

\[
\frac14
=\det
\begin{pmatrix}
K_{ii}&K_{ij}\\
K_{ij}&K_{jj}
\end{pmatrix}
=\frac14-K_{ij}^2.
\]

Therefore \(K_{ij}=0\) for all \(i\ne j\), so \(K=I/2\).  Conversely, \(I/2\)
is the independent fair Bernoulli DPP and has uniform subset law.  This
verifies `frozen_claim.md` claim 4 and `proof.md` lines 89--104.

## 7. Boundary and nonclaims

The proof is local in the strict-feasible interval for \(K(t)\).  Since
\(K(0)=I/2\), such an interval always exists for any fixed symmetric \(D\).
The result is a local/radial exclusion theorem at the uniform kernel; it does
not prove a full-neighborhood Hessian sign theorem and does not settle R3.

No critical gap found.
