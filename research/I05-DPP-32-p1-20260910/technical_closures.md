# Technical closures for the `p>=1` theorem

Status: **AUTHOR PROOF SUPPLEMENT / PENDING INDEPENDENT REVIEW**.

This note expands two points that are easy to state too quickly: the common
complex envelope over the entire complete-event family, and continuity of the
endpoint two-response formulas.

## 1. Entrywise envelope algebra for the direct sum

For a block-diagonal family matrix `A` on
`Lambda=Z x N`, define its horizontal diagonal envelope

\[
\mathfrak d_A(m)
=\sup_{e\in\mathbb N}\sup_{i\in\mathbb Z}
 |A((i,e),(i-m,e))|.
\tag{1.1}
\]

All off-block entries in the application vanish.  For two such matrices,
absolute multiplication and a change of summation index give

\[
\mathfrak d_{AB}(m)
\le(\mathfrak d_A*\mathfrak d_B)(m).
\tag{1.2}
\]

With `w_r(m)=(1+|m|)^r`, submultiplicativity gives

\[
\|\mathfrak d_A*\mathfrak d_B\|_{\ell^1_r}
\le\|\mathfrak d_A\|_{\ell^1_r}
 \|\mathfrak d_B\|_{\ell^1_r}.
\tag{1.3}
\]

For integer `Lambda`, the `C^{1,r}` norm controls the left side of

\[
\|\mathfrak d_A\|_{\ell^1_r}
\le C_r\|A\|_{C^{1,r}(\Lambda)}
\tag{1.4}
\]

and conversely up to the finite unit-cube multiplicity.  In particular,
Fang--Shin applied to the **single direct sum** gives

\[
\|\mathfrak d_{\mathbb M_0^{-1}}\|_{\ell^1_r}<\infty.
\]

There is no interchange of

```text
sum over displacement
```

with

```text
sup over event matrices.
```

Both operations already occur in the norm of the one direct-sum inverse.

Let

\[
d_0=\mathfrak d_{\mathbb M_0^{-1}},
\qquad b=\mathfrak d_{\mathbb G}.
\]

The complex Neumann series has the explicit common envelope

\[
d_\rho
=\sum_{k\ge0}\rho^k(d_0*b)^{*k}*d_0.
\tag{1.5}
\]

If

\[
\rho\|d_0*b\|_{\ell^1_r}<1,
\]

then (1.3) gives

\[
\|d_\rho\|_{\ell^1_r}
\le\frac{\|d_0\|_{\ell^1_r}}
 {1-\rho\|d_0*b\|_{\ell^1_r}}<\infty.
\tag{1.6}
\]

For every `|z|<=rho`, every block inverse is bounded entrywise by `d_rho`.
This proves the common complex envelope claimed in the main localization file,
including the supremum over `z`.

## 2. Doubled moment after taking all suprema

Let

\[
a(m)=|\widehat c(m)|+\rho|\widehat g(m)|,
\qquad e=a*d_\rho.
\]

Equations (1.2)--(1.6) put the supremum over every window, complete word and
complex parameter below the fixed sequence `e`.  Thus

\[
\sup_{R,x,z}|(u_RM_{R,x}^{-1})_j|\le e(j),
\qquad
\sup_{R,x,z}|(M_{R,x}^{-1}v_R)_j|\le e(j).
\tag{2.1}
\]

The sequence controlling a flip at site `j` is the single fixed sequence

\[
\beta_j=C e(j)^2,
\]

not a configuration-dependent sequence whose norm is bounded only after the
configuration is fixed.  Hence

\[
\sum_j(1+j)^{2r}\beta_j
\le C\left(\sum_j(1+j)^r e(j)\right)^2<\infty.
\tag{2.2}
\]

This closes the only potentially invalid supremum/summation exchange.

## 3. Uniform Poisson time tails in `V_0`

Use the notation of `moment_response_and_entropy.md`.  Let

\[
a_n(F)=\operatorname{osc}(L_s^nF).
\]

The BFG convolution bound has one common summable majorant `a_n^*`, uniformly
in `s`, because both the variation envelope and the renewal sequence are fixed
summable sequences.

For

\[
R_s^{>N}F=\sum_{n>N}L_s^n(F-\nu_sF),
\]

the sup norm tends to zero uniformly by `sum_{n>N}a_n^*`.

For the variation sum, the first-disagreement estimate gives

\[
\begin{aligned}
\sum_m\operatorname{var}_m(R_s^{>N}F)
\le{}&
\sum_m\sum_{n>N}v_{m+n}\\
&+\sum_m\sum_{n>N}\sum_{r<n}
 \Gamma_{m+r}a_{n-r-1}^*.
\end{aligned}
\tag{3.1}
\]

The first line is at most

\[
\sum_{k>N}(k+1)v_k\longrightarrow0.
\tag{3.2}
\]

For the second, put `l=n-r-1` and

\[
G_r=\sum_{m\ge0}\Gamma_{m+r}.
\]

The sequence `G` is summable because `sum(k+1)Gamma_k<infinity`, while `a^*`
is summable by BFG.  The second line of (3.1) is bounded by

\[
\sum_{r,l\ge0:\ r+l\ge N}G_r a_l^*,
\tag{3.3}
\]

the tail of a convolution of two `l^1` sequences.  It tends to zero.  Thus the
Poisson series of a `V_1` observable converges uniformly in `V_0`, not merely
in sup norm.

Finite partial sums depend continuously on `s` in `V_0`, so

\[
s\mapsto R_sF_s
\]

is continuous in `V_0` for every moving family with the fixed first-moment
variation envelope.

## 4. Uniform outer Poisson tail

Let

\[
H_s=A_{1,s}R_sF_s.
\]

The product/prepend estimate and (4.5) of the main response file give one fixed
summable sequence controlling `var_m H_s`.  BFG then yields one fixed summable
majorant for

\[
\operatorname{osc}(L_s^nH_s).
\]

Therefore

\[
R_sH_s=\sum_{n\ge0}L_s^n(H_s-\nu_sH_s)
\]

converges uniformly in sup norm and depends continuously on `s`.  This is all
that the nested term

\[
\nu_s A_{1,s}R_s(A_{1,s}R_sF_s)
\]

requires.  No assertion that the outer Poisson inverse maps `V_0` back to a
summable-variation space is made.

## 5. Endpoint accounting

For `p=1`, the complete-event flip envelopes satisfy

\[
\sum_j(1+j)^2\beta_j^{(k)}<\infty.
\]

Consequently

\[
\sum_n(n+1)\operatorname{var}_n(\partial_z^k\ell_z)
\le
\sum_j\beta_j^{(k)}\sum_{n<j}(n+1)
\le C\sum_j(1+j)^2\beta_j^{(k)}<\infty.
\]

There is no logarithmic or strict-exponent loss.  The first Poisson inverse
lands in `V_0`; BFG summability supplies the second inverse in `C`.  This is why
the theorem includes `p=1`, while the present argument does not extend the
whole `A_p` class to `p<1`.
