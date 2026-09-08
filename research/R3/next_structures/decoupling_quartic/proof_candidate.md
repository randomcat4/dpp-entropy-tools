# Proof candidate for the NS-3 decoupling quartic lemma

STATUS: PROVED_CANDIDATE

This proof is intended as a frozen candidate argument. It uses only exact-event probabilities derived from inclusion probabilities by Möbius inversion.

## 1. Feasibility and positivity of atoms

Because \(A\) and \(B\) are strict positive contractions, \(K_0=A\oplus B\) has positive distance from both spectral walls \(0\) and \(I\). If

\[
E_X=\begin{pmatrix}0&X\\X^T&0\end{pmatrix},
\]

then \(K_\varepsilon=K_0+\varepsilon E_X\). Hence for sufficiently small \(|\varepsilon|\),

\[
0<K_\varepsilon<I.
\]

For every such \(\varepsilon\), the \(L\)-ensemble kernel

\[
L_\varepsilon=K_\varepsilon(I-K_\varepsilon)^{-1}
\]

is positive definite, and

\[
P_\varepsilon(S)=\det(I-K_\varepsilon)\det((L_\varepsilon)_S)>0
\]

for all exact atoms \(S\subseteq E\). Thus all logarithms below are taken of strictly positive analytic functions near \(\varepsilon=0\).

## 2. Inclusion minors have no odd powers

For \(U\subseteq E_A\), \(V\subseteq E_B\), write

\[
Q_{U,V}(\varepsilon)=
\Pr(U\cup V\subseteq Y)
=
\det
\begin{pmatrix}
A_U&\varepsilon X_{U,V}\\
\varepsilon X_{U,V}^T&B_V
\end{pmatrix}.
\]

Principal submatrices of \(A\) and \(B\) are positive definite, hence invertible when nonempty. If both \(U\) and \(V\) are nonempty, the block determinant identity gives

\[
Q_{U,V}(\varepsilon)
=\det(A_U)\det(B_V)
\det\!\left(I-\varepsilon^2B_V^{-1}X_{U,V}^TA_U^{-1}X_{U,V}\right).
\]

Equivalently,

\[
Q_{U,V}(\varepsilon)
=\det(A_U)\det(B_V)
+\left[
-\det(A_U)\det(B_V)
\operatorname{tr}(A_U^{-1}X_{U,V}B_V^{-1}X_{U,V}^T)
\right]\varepsilon^2
+O(\varepsilon^4).
\]

If \(U=\varnothing\) or \(V=\varnothing\), then \(Q_{U,V}(\varepsilon)=\det(A_U)\det(B_V)\) is independent of \(\varepsilon\). Therefore every inclusion probability is an even polynomial in \(\varepsilon\).

The same parity follows globally from sign conjugacy: with \(D=\operatorname{diag}(I_{E_A},-I_{E_B})\),

\[
K_{-\varepsilon}=DK_\varepsilon D,
\]

and every principal determinant is unchanged by this congruence.

## 3. Exact atoms by Möbius inversion

The exact atom for \(I\subseteq E_A\), \(J\subseteq E_B\) is

\[
P_\varepsilon(I,J)=
\sum_{\substack{U\supseteq I\\V\supseteq J}}
(-1)^{|U|-|I|+|V|-|J|}
Q_{U,V}(\varepsilon).
\]

Substituting the previous expansion yields

\[
P_\varepsilon(I,J)
=P_0(I,J)+\varepsilon^2r_{I,J}(X)+\varepsilon^4s_{I,J}(X)+O(\varepsilon^6),
\]

where \(r_{I,J}\) is the formula stated in `frozen_lemma.md`.

At \(\varepsilon=0\),

\[
Q_{U,V}(0)=\det(A_U)\det(B_V),
\]

so the two Möbius sums factor:

\[
P_0(I,J)=p_A(I)p_B(J).
\]

This proves that \(K_0=A\oplus B\) is exactly the independent product law.

## 4. Fixed marginals force cancellation of the apparent quadratic entropy term

The marginal DPP on \(E_A\) has kernel \(A\) for every \(\varepsilon\), because the principal block of \(K_\varepsilon\) on \(E_A\) is \(A\). Similarly the marginal on \(E_B\) has kernel \(B\). Hence

\[
\sum_J P_\varepsilon(I,J)=p_A(I),\qquad
\sum_I P_\varepsilon(I,J)=p_B(J)
\]

for all small \(\varepsilon\). Comparing coefficients in the even expansion gives, for every expansion coefficient after the constant term,

\[
\sum_J r_{I,J}=0,\qquad \sum_I r_{I,J}=0,
\]

and the same row and column cancellations for \(s_{I,J}\) and all higher coefficients.

Set \(p^0_{I,J}=p_A(I)p_B(J)>0\), and write

\[
P_\varepsilon(I,J)=p^0_{I,J}+\varepsilon^2r_{I,J}+\varepsilon^4s_{I,J}+O(\varepsilon^6).
\]

For \(\phi(p)=-p\log p\),

\[
\phi(p^0+\delta)
=\phi(p^0)+\phi'(p^0)\delta+\frac12\phi''(p^0)\delta^2+O(\delta^3),
\]

where

\[
\phi'(p)=-(\log p+1),\qquad \phi''(p)=-1/p.
\]

The coefficient of \(\varepsilon^2\) in entropy is

\[
\sum_{I,J}\phi'(p^0_{I,J})r_{I,J}
=-\sum_{I,J}(\log p_A(I)+\log p_B(J)+1)r_{I,J}=0,
\]

using the row, column, and total-sum cancellations.

The linear contribution of \(s_{I,J}\) to the \(\varepsilon^4\) coefficient cancels by the same argument:

\[
\sum_{I,J}\phi'(p^0_{I,J})s_{I,J}=0.
\]

Thus the entire fourth-order entropy coefficient comes from the quadratic Taylor term:

\[
\frac12\sum_{I,J}\phi''(p^0_{I,J})r_{I,J}^2
=
-\frac12\sum_{I,J}\frac{r_{I,J}^2}{p_A(I)p_B(J)}.
\]

Therefore

\[
H(K_\varepsilon)=H(K_0)-c_4(X)\varepsilon^4+O(\varepsilon^6),
\]

where

\[
c_4(X)=\frac12\sum_{I,J}\frac{r_{I,J}(X)^2}{p_A(I)p_B(J)}\ge 0.
\]

## 5. Equality condition

The formula above immediately gives

\[
c_4(X)=0\quad\Longleftrightarrow\quad r_{I,J}(X)=0
\text{ for all exact atoms }(I,J).
\]

If all exact atom second coefficients vanish, then the second coefficient of every inclusion probability also vanishes, since inclusion probabilities are sums of exact atoms:

\[
q^{(2)}_{U,V}(X)=
\sum_{\substack{I\supseteq U\\J\supseteq V}}r_{I,J}(X)=0.
\]

Taking \(U=\{i\}\subseteq E_A\) and \(V=\{j\}\subseteq E_B\), the inclusion minor is

\[
\det
\begin{pmatrix}
A_{ii}&\varepsilon X_{ij}\\
\varepsilon X_{ij}&B_{jj}
\end{pmatrix}
=A_{ii}B_{jj}-\varepsilon^2X_{ij}^2.
\]

Hence

\[
q^{(2)}_{\{i\},\{j\}}(X)=-X_{ij}^2.
\]

So all these coefficients vanish if and only if every \(X_{ij}=0\). Conversely \(X=0\) makes \(K_\varepsilon=K_0\) and \(c_4=0\). Thus

\[
c_4(X)=0\quad\Longleftrightarrow\quad X=0.
\]

This also rules out a nonzero higher-order escape branch inside the one-parameter family \(K_\varepsilon\): nonzero \(X\) already produces a strictly positive \(c_4\), and zero \(X\) produces no perturbation at all.

## 6. R3 sign consequence

The law and entropy are even in \(\varepsilon\), so \(H(K_{-\varepsilon})=H(K_\varepsilon)\). For the R3 midpoint convention around \(M=K_0\),

\[
\Delta(\varepsilon)
=\frac{H(K_{-\varepsilon})+H(K_\varepsilon)}2-H(K_0)
=H(K_\varepsilon)-H(K_0)
=-c_4(X)\varepsilon^4+O(\varepsilon^6).
\]

If \(X\neq0\), then \(c_4(X)>0\), so \(\Delta(\varepsilon)<0\) for all sufficiently small nonzero \(\varepsilon\). Near a decoupling face, cross-block coupling therefore behaves as a local entropy-loss mechanism, not a local real counterexample mechanism.
