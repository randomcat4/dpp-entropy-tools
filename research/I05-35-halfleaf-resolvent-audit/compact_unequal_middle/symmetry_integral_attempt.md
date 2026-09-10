# Exchange symmetry, integral variables, and the remaining analytic obstruction

Status: **AUTHOR DERIVATION / PENDING INDEPENDENT REVIEW**. This note records the analytic route attempted before the exact compact-box certificate. It makes no pointwise-kernel positivity claim.

## 1. Exact leaf exchange

Use the six-coordinate order

```text
(m,alpha,beta,gamma,d,e).
```

Let `Pi` be the coordinate permutation

```text
(m,alpha,beta,gamma,d,e)
 ->(m,beta,alpha,gamma,e,d).
```

Directly from the formulas for `F,R,C,L`,

```text
M(b,a)=Pi^T M(a,b) Pi,
E(b,a)=S^T E(a,b) S,
S=[[0,1],[1,0]].
```

Thus `det E`, the two eigenvalues of `E`, and positivity of the full one-sided form are symmetric under `a<->b`. The retained checker certifies all 1024 boxes rather than discarding half of them, so the numerical certificate does not rely on this symmetry; the identity is an analytic cross-check and fixes the correct variable exchange.

## 2. Positive integrated variables

With

```text
r=a/(1+a), s=b/(1+b),
U=-log(1-r)=log(1+a),
V=-log(1-s)=log(1+b),
H=-log(1-rs),
```

one has

```text
ell=U-H/2,
k=V-H/2,
lambda=-H,
J=b U+a V-(1+a+b)H.
```

The two coupled logarithmic quantities have the exact positive integral forms

```text
H=int_0^a int_0^b (1+x+y)^(-2) dy dx,
J=int_0^a int_0^b (1+x+y)^(-1) dy dx.
```

They recover the `a<->b` symmetry and the previously established one-edge asymptotics as either variable tends to zero. Those endpoint asymptotics are not reused as a continuity proof for the compact middle.

## 3. Why the direct pointwise-kernel route was not promoted

After eliminating the positive four-dimensional pivot, `det E` is nonlinear in `U,V,H,J`: it contains products of the two double integrals and products with the one-dimensional logarithms. Consequently, replacing `H` and `J` by their displayed integrands does not produce an identity of the form

```text
det E=int positive_rational_kernel.
```

A valid factorization would require a coupled multi-integral kernel together with all cross terms. No such positive kernel was derived. Since the exact pointwise resolvent counterexample is already accepted on `main`, no unproved pointwise rational sign was used as a surrogate.

The compact certificate instead encloses the already-integrated matrix `M(a,b)` itself. It proves there is no negative one-sided physical direction anywhere on `1/4<=a,b<=4`, but it does not decide the remaining regions outside that square. A true negative direction outside the square, if found later, must be reconstructed through the minimizing Schur vector and then checked against all complete events; a negative auxiliary kernel would not suffice.
