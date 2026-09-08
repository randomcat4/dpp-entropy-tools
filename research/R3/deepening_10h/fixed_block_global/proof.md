# Proof of FT-A: fixed block marginals maximize entropy at decoupling

STATUS: PROVED

Author proof. A fresh verifier must still audit this before it can be marked `CORRECT`.

## 1. Marginal block kernels

Let

\[
K=\begin{pmatrix}A&X\\X^T&B\end{pmatrix}
\]

be a finite real symmetric strict positive contraction, \(0<K<I\), indexed by the disjoint union \(E_A\sqcup E_B\).

Because \(K>0\), every principal submatrix is positive definite, so \(A>0\) and \(B>0\). Because \(I-K>0\), the principal submatrices \(I-A\) and \(I-B\) are positive definite, so \(A<I\) and \(B<I\). Thus \(A\) and \(B\) are themselves strict DPP marginal kernels.

For any \(U\subseteq E_A\),

\[
\Pr(U\subseteq Y_A)=\Pr(U\subseteq Y)=\det K_U=\det A_U.
\]

Therefore \(Y_A\) is the DPP with kernel \(A\). Similarly, for any \(V\subseteq E_B\),

\[
\Pr(V\subseteq Y_B)=\det B_V,
\]

so \(Y_B\) is the DPP with kernel \(B\).

Hence

\[
H(K)=H(Y_A,Y_B),\qquad H(A)=H(Y_A),\qquad H(B)=H(Y_B).
\]

This step uses only the inclusion-probability definition of a DPP and does not identify \(\det K_S\) with an exact event probability.

## 2. Entropy subadditivity

Let \(P\) be the joint law of the finite random variables \((Y_A,Y_B)\), and let \(P_A,P_B\) be its marginals. Then

\[
H(A)+H(B)-H(K)
=H(Y_A)+H(Y_B)-H(Y_A,Y_B).
\]

Expanding finite Shannon entropy gives

\[
H(Y_A)+H(Y_B)-H(Y_A,Y_B)
=
\sum_{I\subseteq E_A,\;J\subseteq E_B}
P(I,J)\log\frac{P(I,J)}{P_A(I)P_B(J)}.
\]

The right-hand side is the Kullback--Leibler divergence

\[
D(P\|P_A\otimes P_B)=I(Y_A;Y_B).
\]

For completeness, here is the standard finite proof of nonnegativity. For positive \(p,q\),
\[
p\log(p/q)\ge p-q,
\]
which is equivalent to \(\log u\le u-1\) with \(u=q/p\). Summing over all atoms gives

\[
D(P\|Q)\ge \sum_\omega (P(\omega)-Q(\omega))=0.
\]

Equality holds if and only if \(P(\omega)=Q(\omega)\) for every atom \(\omega\). In the present strict DPP setting all exact atoms are positive: \(L=K(I-K)^{-1}\) is positive definite and

\[
P(Y=S)=\det(I-K)\det L_S>0.
\]

Thus the equality condition is exactly

\[
P=P_A\otimes P_B,
\]

that is, \(Y_A\) and \(Y_B\) are independent.

Therefore

\[
H(K)\le H(A)+H(B),
\]

with equality if and only if the two block configurations are independent.

## 3. \(X=0\) implies independence

Assume \(X=0\). Then \(K=A\oplus B\). For \(U\subseteq E_A\), \(V\subseteq E_B\),

\[
\Pr(U\cup V\subseteq Y)
=\det K_{U\cup V}
=\det A_U\,\det B_V.
\]

These are exactly the inclusion probabilities of the product of the DPP with kernel \(A\) and the DPP with kernel \(B\). Since inclusion probabilities determine the finite DPP law, the exact event law factors:

\[
P(Y_A=I,Y_B=J)=P_A(I)P_B(J).
\]

Hence \(Y_A\) and \(Y_B\) are independent, and equality holds:

\[
H(K)=H(A)+H(B)=H(A\oplus B).
\]

## 4. Independence implies \(X=0\)

Conversely assume \(Y_A\) and \(Y_B\) are independent. Then every event measurable with respect to \(Y_A\) is independent of every event measurable with respect to \(Y_B\). In particular, for any \(i\in E_A\), \(j\in E_B\),

\[
\Pr(i\in Y,\;j\in Y)=\Pr(i\in Y)\Pr(j\in Y).
\]

The one-point inclusion probabilities are

\[
\Pr(i\in Y)=A_{ii},\qquad \Pr(j\in Y)=B_{jj}.
\]

The two-point cross-block inclusion probability is the \(2\times2\) principal minor

\[
\Pr(\{i,j\}\subseteq Y)
=
\det\begin{pmatrix}
A_{ii}&X_{ij}\\
X_{ij}&B_{jj}
\end{pmatrix}
=A_{ii}B_{jj}-X_{ij}^2.
\]

Independence therefore forces

\[
A_{ii}B_{jj}-X_{ij}^2=A_{ii}B_{jj},
\]

so \(X_{ij}^2=0\), hence \(X_{ij}=0\). Since \(i,j\) were arbitrary, all entries of \(X\) vanish. Thus

\[
Y_A\perp Y_B\quad\Longrightarrow\quad X=0.
\]

Combining Sections 3 and 4,

\[
H(K)=H(A)+H(B)\quad\Longleftrightarrow\quad X=0.
\]

## 5. Empty blocks and \(1\times1\) blocks

If one block is empty, then \(X\) is the unique empty cross block and the statement reduces to \(H(K)=H(K)+0\). The equality condition \(X=0\) is vacuous and correct.

If one or both blocks have size one, the same singleton-inclusion argument above is exactly the relevant case; no separate generic-rank or invertibility assumption is needed.

## 6. Sign conjugacy

Let

\[
D=\operatorname{diag}(I_{E_A},-I_{E_B}).
\]

Then

\[
\begin{pmatrix}A&-X\\-X^T&B\end{pmatrix}=DKD.
\]

Every principal determinant is preserved under this diagonal sign congruence, so the DPP law and entropy are unchanged by \(X\mapsto -X\). The proof above depends on \(X_{ij}^2\), so it is consistent with this symmetry.

## 7. Feasible boundary

The frozen theorem assumes strict feasibility \(0<K<I\). The information-theoretic inequality itself is valid for arbitrary finite distributions, but strictness is useful here because it ensures all DPP atoms and marginal atoms are positive and all logarithms can be handled without boundary conventions.

If a later extension wants to include non-strict kernels, the inequality remains true with the usual \(0\log0=0\) convention, but the equality proof should be restated with support-aware KL conventions. That extension is not needed for FT-A.

## 8. Relation to NS-3

NS-3 proved a local expansion at the decoupling face

\[
K_\varepsilon=
\begin{pmatrix}
A&\varepsilon X\\
\varepsilon X^T&B
\end{pmatrix},
\qquad
H(K_\varepsilon)=H(A\oplus B)-c_4(X)\varepsilon^4+O(\varepsilon^6),
\]

with \(c_4(X)>0\) for \(X\neq0\).

FT-A strictly strengthens the sign part of NS-3 for fixed \(A,B\): it proves

\[
H(K)\le H(A\oplus B)
\]

for every feasible cross block \(X\), not merely for sufficiently small \(\varepsilon X\). What FT-A does not replace is NS-3's explicit fourth-order coefficient \(c_4\), which remains a sharper local diagnostic for near-decoupling numerical errors.

## 9. Quantitative lower bound

The exact deficit is the mutual information:

\[
H(A)+H(B)-H(K)=I(Y_A;Y_B).
\]

For any \(i\in E_A\), \(j\in E_B\), apply deterministic data processing to the indicator pair

\[
U_i=\mathbf 1_{\{i\in Y\}},\qquad V_j=\mathbf 1_{\{j\in Y\}}.
\]

Then

\[
I(Y_A;Y_B)\ge I(U_i;V_j).
\]

Let \(a=A_{ii}\), \(b=B_{jj}\), and \(c=X_{ij}^2\). The joint law of \((U_i,V_j)\) differs from the product Bernoulli law with marginals \(a,b\) by the signed table

\[
\begin{array}{c|cc}
&V_j=0&V_j=1\\ \hline
U_i=0&-c&+c\\
U_i=1&+c&-c
\end{array}
\]

up to row/column ordering. Hence the total variation distance between this pair law and its product marginals is \(2c\). Pinsker's inequality in natural logarithms gives

\[
I(U_i;V_j)\ge 2(2c)^2=8X_{ij}^4.
\]

Taking the maximum over all cross-block entries gives

\[
H(A)+H(B)-H(K)\ge 8\max_{i,j}X_{ij}^4.
\]

This bound is intentionally crude and is not asserted to be sharp.
