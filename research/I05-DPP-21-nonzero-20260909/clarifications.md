# Proof clarifications before independent review

These are non-substantive corrections to the current `proof.md`; they do not change any theorem hypothesis, conclusion, or constant.

## 1. Norm bound in Lemma 2.1

Immediately before equation (2.9), the statement `||B_{t,Z}||<1` uses the following omitted one-line estimate.

For every complete zero set `Z`,

```text
M_{t,Lambda,Z}=K_{mu+t g}|_Lambda-I_Z
```

is Hermitian and, from

```text
delta_T I<=K_{mu+t g}|_Lambda<=(1-delta_T)I,
```

one has

```text
-(1-delta_T)I<=M_{t,Lambda,Z}<=(1-delta_T)I.          (C.1)
```

Indeed, the upper bound uses `-I_Z<=0`; the lower bound uses `-I_Z>=-I`. Hence

```text
||M_{t,Lambda,Z}||<=1-delta_T.                        (C.2)
```

The Fourier truncation error has norm below `delta_T/4`, so

```text
||B_{t,Z}||<=1-delta_T+delta_T/4
             =1-3delta_T/4<1.                         (C.3)
```

Thus the unscaled polynomial inverse

```text
B_{t,Z}^{-1}=sum_{r>=0}B_{t,Z}(I-B_{t,Z}^2)^r
```

is valid exactly as written. No rescaling or new assumption is needed.

## 2. Variable name in equation (2.15)

The first symbol in the code block following equation (2.14) reads

```text
nu in E_beta
```

and is a typographical error. It means

```text
u replaced by u:  u in E_beta.                        (C.4)
```

The preceding definition `F(u,t)=h(mu+u+t g)` and every subsequent formula already use `u`; there is no second measure or variable named `nu` in Lemma 2.2.

## 3. Frozen definitions

The clean RPF notation in `frozen_statement.md` is authoritative:

```text
B_t=-L_t phi_t,
h(t)=nu_t(B_t),
u_t(B_t)=h(t),
 u_t=R_tB_t.
```

Equivalently, without the redundant identity in the display, the operative definitions are simply

```text
B_t=-L_t phi_t,
h(t)=nu_t(B_t),
 u_t=R_tB_t.
```

The exact Hessian remains equation (6.9) of `proof.md` and equation (2.3) of `frozen_statement.md`.