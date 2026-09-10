# I05-22 R5: paired logit compression and global q/qbar imbalance curvature

Status: **PROVED (author proof; PENDING_REVIEW)** for the exact paired-logit compression and the global imbalance lemmas below. **INCOMPLETE** for `det E_H>=0`, general Lambda-nonzero missing-edge entropy concavity, and general real three-point concavity. No entropy counterexample is claimed. Novelty is unassessed.

This unit starts from reviewed `main` commit `65e59a46b49cd2dbb5c779a4cfae8cef26441984`. It reads, but does not modify or rerun, the PR70 frozen source `f7be60759fd4d65184803b6585965dc7e5ccd624`. PR70's analytic FIRST is scoped-accepted in PR78; its fixed auxiliary paired-resolvent witness was still `PENDING_C2` in the records read at the start of this unit. Issue73 remains a frozen `REQUESTED` 273-point/three-filament computation contract and is not executed or duplicated here. The accepted PR60 Lambda=0 theorem is used only as an already-reviewed boundary of scope; its 1731-term certificate is not rerun.

## 1. Domain and inherited exact full target

Use the connected real missing-edge arrow

```text
K=[[x,0,b],[0,y,c],[b,c,z]],
v=x(1-x), w=y(1-y),
b^2=A v, c^2=B w,
z=q+A(1-x)+B(1-y),
qbar=1-A-B-q,
0<x,y<1, A,B,q,qbar>0.
```

For `i,j in {0,1}` put

```text
t_ij = q + A(1-i) + B(1-j),
P_ij = Bern_x(i) Bern_y(j).
```

The complete eight-event entropy and all six true physical directions are those in PR70 proof.md. The already-FIRST-accepted positive pivot reduction is

```text
E_H = L0+L1+diag(1/v,1/w)
      -(C0+C1)(Y0+Y1)^(-1)(C0+C1)^T,
Y_s=F_s+R_s>0.
```

At least one eigenvalue of this `2x2` matrix is positive, so the unresolved full target is exactly `det E_H>=0`. Nothing below assumes this sign.

## 2. Exact complement-paired scalar compression

Define the binary negative-entropy potential and its first two derivatives

```text
psi(t)=t log t+(1-t)log(1-t),
g(t)=psi'(t)=log(t/(1-t)),
f(t)=psi''(t)=1/[t(1-t)].
```

Define four paired scalar quantities

```text
ell_j = g(t_0j)-g(t_1j),
ell   = (1-y) ell_0 + y ell_1,

k_i   = g(t_i0)-g(t_i1),
k     = (1-x) k_0 + x k_1,

lambda = ell_0-ell_1,
J      = psi(t_00)+psi(t_11)-psi(t_10)-psi(t_01).
```

These are exactly the sums of the side-0 and side-1 scalars in PR70:

```text
ell=ell_0side+ell_1side,
k=k_0side+k_1side,
lambda=lambda_0+lambda_1=V0-V1,
J=J0+J1.
```

Therefore the paired matrices do not require side-specific logarithms. With `mu=2x-1`, `nu=2y-1`,

```text
L=L0+L1 = [[A ell/(2v), J],
           [J, B k/(2w)]],

C=C0+C1 = [[-ell, mu ell/2, w lambda, -w lambda mu/2],
           [-k, v lambda, nu k/2, -v lambda nu/2]].
```

Let `R=R0+R1`. Its lower `3x3` block is

```text
[[v ell/(2A), 0, -vw lambda/(2A)],
 [0, w k/(2B), -vw lambda/(2B)],
 [-vw lambda/(2A), -vw lambda/(2B), vw n/(2AB)]],
```

where the apparent remaining side quantity also collapses:

```text
n = A k + B ell - J + lambda(A mu+B nu).            (1)
```

Proof of (1): sum the already-derived side identities
`J_s=A k_s+B ell_s-n_s+lambda_s(A mu+B nu)`.
Thus `L,C,R` are functions only of `(ell,k,lambda,J)` and rational parameters. The paired Fisher is

```text
F=F0+F1=sum_ij P_ij f(t_ij) a_ij a_ij^T,
a_ij=(1,i-x,j-y,(i-x)(j-y))^T,
```

and its inverse remains the short rational identity from PR70 (19), because `1/f(t)=t(1-t)`. Hence **all transcendental dependence of the full paired core is contained in the four scalar logit/rectangle quantities above**. No one-sided sign assumption is used.

This is the preferred object for any logarithmic-mean attack on `det E_H`: applying matrix-perspective convexity to a side separately is strictly stronger than the full problem and, for kernel-affine paths, does not remove the event accelerations.

## 3. Rectangle-integral representation

Writing `a in [0,A]`, `b in [0,B]`, direct FTC gives

```text
ell_0 = int_0^A f(q+a+B) da,
ell_1 = int_0^A f(q+a) da,

k_0   = int_0^B f(q+A+b) db,
k_1   = int_0^B f(q+b) db,

J(q)  = int_0^A int_0^B f(q+a+b) db da,            (2)

lambda(q)
      = int_0^A int_0^B f'(q+a+b) db da
      = J'(q).                                      (3)
```

In particular `ell,k,J>0` everywhere. Equation (3) is the key imbalance identity: the mixed paired logarithm is the derivative of the positive rectangle integral, not an independent sign-indefinite logarithmic remainder.

## 4. Global q/qbar imbalance theorem

Set

```text
r=1-A-B,
q0=r/2,
qbar=r-q.
```

The complement-balanced surface is `q=qbar=q0`, i.e. the accepted Lambda=0 surface.

### Lemma 4.1: exact symmetry

For all `0<q<r`,

```text
J(r-q)=J(q),
lambda(r-q)=-lambda(q).                             (4)
```

Proof. In (2), replace `(a,b)` by `(A-a,B-b)` and use
`f(1-t)=f(t)`. This sends `q+a+b` to
`1-(r-q+(A-a)+(B-b))`. Differentiate the first identity to get the second.

### Lemma 4.2: strict global convexity and a uniform curvature floor

On `(0,r)`,

```text
J''(q)=int_0^A int_0^B f''(q+a+b) db da >0.         (5)
```

Moreover

```text
f''(t) >= 32,  0<t<1,                               (6)
J''(q) >= 32 A B.                                   (7)
```

Proof. Put `u=t(1-t) in (0,1/4]`. Since `f=1/u`,

```text
f''(t)=2[(1-2t)^2+u]/u^3
      =2(1-3u)/u^3.
```

The last expression is decreasing in `u` on `(0,1/4]`, hence minimized at `u=1/4`, where it equals `32`. Integrating over the `A x B` rectangle proves (7).

### Theorem 4.3: sign and quantitative growth away from Lambda=0

For the whole legal interval `0<q<r`,

```text
sign lambda(q) = sign(q-q0),                        (8)
```

with equality only at `q=q0`. More quantitatively,

```text
|lambda(q)| >= 32 A B |q-q0|,                       (9)

J(q) >= J(q0) + 16 A B (q-q0)^2.                   (10)
```

Hence on the full fundamental domain `0<q<=qbar`,

```text
lambda<=0,
```

strictly negative off the balanced surface.

Proof. From (4), `lambda(q0)=0`. Integrating (7) once from `q0` gives (8)-(9), and integrating the strong-convexity inequality a second time gives (10).

This is a genuinely global imbalance statement: it covers the entire open `q/qbar` range for every fixed legal `A,B`, including arbitrarily large imbalance. It is not a small-neighborhood continuation from PR60.

### Coarse endpoint envelope retained for later determinant work

For `q<=qbar`, every `t_ij` and every point of the rectangle in (2) satisfies
`t>=q` and `1-t>=qbar`. Hence

```text
4 <= f(t) <= 1/(q qbar),
4AB <= J(q) <= AB/(q qbar).                         (11)
```

Also `f''(t)<=2/(q qbar)^3`, so

```text
32AB <= J''(q) <= 2AB/(q qbar)^3.                  (12)
```

The upper bounds are deliberately coarse but explicit and valid throughout the full fundamental domain; they record the exact rare-event blow-up rather than discarding it.

## 5. Two structurally different methods and what survives

### Method A: scalar/logarithmic-mean and matrix-perspective inequalities

The paired scalar increments are logarithmic-mean objects because, for `u<v`,

```text
g(v)-g(u)=int_u^v [1/t+1/(1-t)] dt.
```

Classical Hermite-Hadamard/logarithmic-mean bounds can therefore control each increment. Kubo-Ando operator means provide the standard positive-operator framework for logarithmic and harmonic/parallel means, while Effros' matrix perspective theorem explains why a genuinely affine matrix perspective has a convexity mechanism.

However the DPP map from a true kernel-affine line to `(p_ij1,P_ij)` is not affine: the complete-event second accelerations remain. PR70 equation (7) exhibits the exact `r''` and `P''` terms. Therefore neither operator perspective convexity nor an operator-mean order can be substituted for the true DPP Hessian. The usable output here is instead the exact four-scalar compression and the global sign/strong-convexity theorem (8)-(10).

Primary sources checked:

- F. Kubo and T. Ando, *Means of positive linear operators*, Math. Ann. 246 (1980), 205-224, DOI `10.1007/BF01371042`.
- E. G. Effros, *A matrix convexity approach to some celebrated quantum inequalities*, PNAS 106 (2009), 1006-1008, DOI `10.1073/pnas.0807965106`, arXiv `0802.1234`.

These sources motivate inequalities only; they do not state the DPP theorem sought here.

### Method B: complement symmetry plus boundary/imbalance analysis

Instead of ordering side perspectives, pair them first into `psi`, use the exact complement involution `q <-> qbar`, and differentiate the rectangle integral. This yields (4)-(12) without a spectral rotation, without dropping marginal Fisher, without assuming either `G_s''>=0`, and without any finite scan. It also keeps the rare-event divergence explicit through `1/(q qbar)`.

This method gives stronger information about the previously uncontrolled imbalance scalar `lambda`, but it does **not** by itself sign `det E_H`: `lambda` enters both `C` and `R`, while `ell,k,J` and the rational Fisher block co-vary with `q`. Treating the increase of `J` alone as a PSD monotonicity claim would be invalid.

## 6. Exact remaining gap

After this checkpoint, the full problem is still

```text
det E_H(ell(q),k(q),lambda(q),J(q);x,y,A,B) >= 0
```

for all strict legal parameters, where `E_H` is the accepted PR70 `2x2` core and `(ell,k,lambda,J)` are now the paired variables above. The new theorem supplies

```text
ell>0, k>0, J>0,
lambda sign-fixed by q-qbar,
|lambda| >= 16AB |q-qbar|,
J(q) >= J(q0)+4AB(q-qbar)^2,
```

(the last two are (9)-(10) rewritten using `q-q0=(q-qbar)/2`). The missing bridge is a determinant inequality that uses these quantities jointly with the exact positive `Y=F+R`; no claim is made that the displayed scalar bounds alone are sufficient.

A promising next analytic target is to rewrite `det E_H * det Y` in the four paired scalars **without expanding side logs**, then test whether the coefficient of the odd imbalance variable `lambda` combines with the complement symmetry into even powers plus terms controlled by strong convexity (7). Any such proof must retain `F`, `R`, the marginal matrix `diag(1/v,1/w)`, and every mixed direction.

## 7. Failure and scope ledger

- Did not rerun PR60 Lambda=0 arithmetic or the 1731 positive coefficients.
- Did not run or duplicate issue73's 273 points / three filaments / 2700-second allocation.
- Did not revive complement-paired resolvent convexity; PR70 already refutes that auxiliary route.
- Did not rename the stronger one-sided `G1>=0` problem as progress on full entropy.
- Did not infer a universal determinant sign from the new scalar inequalities.
- No strict positive Shannon Jensen counterexample was found or claimed.
- No independent arithmetic or second review was available in this unit; all new results above are `PENDING_REVIEW`.

Final classification for this unit: **PROVED (author)** for Sections 2-4; **INCOMPLETE** for the general entropy target.