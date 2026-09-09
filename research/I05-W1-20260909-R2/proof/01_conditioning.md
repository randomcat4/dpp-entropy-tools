# Proof I — complete-event Schur conditioning

All logarithms are natural. For a strict real DPP kernel `0<K<I` and a complete configuration `S`, let `E_{S^c}` be diagonal with ones on `S^c`. Expanding the selected diagonal entries gives

\[
p_K(S)=(-1)^{|S^c|}\det(K-E_{S^c}). \tag{1}
\]

This is exactly the Möbius-inversion event probability. It is positive: after ordering `S,S^c`, the Schur complement is

\[
\det(K-E_{S^c})=\det K_{SS}\det\!\left(K_{S^cS^c}-I-K_{S^cS}K_{SS}^{-1}K_{SS^c}\right),
\]

whose second factor has sign `(-1)^{|S^c|}` because the displayed matrix is negative definite. Thus all event matrices below are invertible.

Split the coordinates into blocks of sizes `m,ell` and set

\[
K(t)=\begin{pmatrix}A&tB\\tB^{\mathsf T}&C\end{pmatrix},
\qquad 0<K(t)<I.
\]

For complete configurations `S subseteq [m]`, `T subseteq [ell]`, write

\[
X_S=A-E_{S^c},\qquad Y_T=C-E_{T^c},\qquad M_S=B^{\mathsf T}X_S^{-1}B,\qquad s=t^2.
\]

Applying (1) and the Schur determinant formula yields, without approximation,

\[
\begin{aligned}
p_{K(t)}(S,T)
&=(-1)^{m-|S|+\ell-|T|}
  \det\begin{pmatrix}X_S&tB\\tB^{\mathsf T}&Y_T\end{pmatrix}\\
&=(-1)^{m-|S|}\det X_S\;(-1)^{\ell-|T|}
  \det(Y_T-sM_S)\\
&=p_A(S)p_{C-sM_S}(T). \tag{2}
\end{aligned}
\]

Hence the conditional law of the right block given the exact left configuration `S` is determinantal with kernel

\[
C_S(s)=C-sM_S. \tag{3}
\]

It is a genuine strict contraction. Indeed (2) makes all complete-event masses `p_{C_S(s)}(T)` positive and summing to one. Möbius inversion then gives, for every `U`,

\[
\det(C_S(s))_U=\sum_{T\supseteq U}p_{C_S(s)}(T)>0,
\]

and the probability that no point of `U` appears gives

\[
\det(I-C_S(s))_U=\sum_{T:T\cap U=\varnothing}p_{C_S(s)}(T)>0.
\]

All principal minors of `C_S(s)` and `I-C_S(s)` are positive, so Sylvester's criterion gives `0<C_S(s)<I`.

The left marginal is the fixed DPP `p_A`; therefore Shannon's chain rule gives the exact entropy identity

\[
G(s):=H(K(\sqrt s))
 =H(A)+\sum_{S\subseteq[m]}p_A(S)H(C-sM_S). \tag{4}
\]

There is also a matrix zero-mean identity. Differentiating (1) along an arbitrary symmetric direction `D` at `A` gives

\[
\left.\partial_z p_{A+zD}(S)\right|_{0}
=p_A(S)\operatorname{tr}(X_S^{-1}D).
\]

Since total mass is one for every `z`,

\[
\sum_Sp_A(S)X_S^{-1}=0,
\qquad
\sum_Sp_A(S)M_S=0. \tag{5}
\]

Equations (2)–(5) retain every complete event and the true affine kernel directions `C-sM_S`. They are the bridge used in the round-two theorem; no Fisher projection or coordinate rotation is involved.