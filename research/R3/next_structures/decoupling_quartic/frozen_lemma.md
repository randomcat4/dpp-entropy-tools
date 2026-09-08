# NS-3 frozen lemma: quartic entropy loss at a two-block decoupling face

STATUS: PROVED_CANDIDATE

This file records a local structural lemma only. It is not a certification of a real R3 counterexample, of a block-exchangeable family, or of the full real domain. It also has not yet been checked by a fresh independent verifier.

## Setting

Let \(E=E_A\sqcup E_B\) be finite. Let \(A\in\mathbb R^{E_A\times E_A}\) and \(B\in\mathbb R^{E_B\times E_B}\) be real symmetric strict positive contractions:

\[
0<A<I,\qquad 0<B<I.
\]

Let \(X\in\mathbb R^{E_A\times E_B}\), and define

\[
K_\varepsilon=
\begin{pmatrix}
A&\varepsilon X\\
\varepsilon X^T&B
\end{pmatrix}.
\]

For all sufficiently small \(|\varepsilon|\), \(K_\varepsilon\) is again a real symmetric strict positive contraction. Let \(P_\varepsilon(I,J)\) be the exact atom probability
\[
\Pr_{K_\varepsilon}(Y\cap E_A=I,\;Y\cap E_B=J),
\]
computed from inclusion probabilities by Möbius inversion, not by treating a principal minor as an exact event probability. Let \(p_A(I)\) and \(p_B(J)\) be the exact atom probabilities of the marginal DPPs with kernels \(A\) and \(B\).

All logarithms are natural.

## Frozen statement

For every \(I\subseteq E_A\), \(J\subseteq E_B\), the exact atom probability has an even analytic expansion

\[
P_\varepsilon(I,J)
=p_A(I)p_B(J)+\varepsilon^2 r_{I,J}(X)+\varepsilon^4 s_{I,J}(X)+O(\varepsilon^6).
\]

The coefficient \(r_{I,J}(X)\) is obtained by Möbius inversion from the inclusion-probability second coefficient:

\[
r_{I,J}(X)=
\sum_{\substack{U\supseteq I\\ V\supseteq J}}
(-1)^{|U|-|I|+|V|-|J|}\,q^{(2)}_{U,V}(X),
\]

where, with empty-subset conventions,

\[
q^{(2)}_{U,V}(X)=
\begin{cases}
-\det(A_U)\det(B_V)
\operatorname{tr}\!\left(A_U^{-1}X_{U,V}B_V^{-1}X_{U,V}^T\right),
&U\neq\varnothing,\;V\neq\varnothing,\\[4pt]
0,&U=\varnothing\text{ or }V=\varnothing.
\end{cases}
\]

The two block marginals are fixed for all small \(\varepsilon\):

\[
\sum_J P_\varepsilon(I,J)=p_A(I),\qquad
\sum_I P_\varepsilon(I,J)=p_B(J).
\]

Consequently \(K_0=A\oplus B\) is the independent product law \(p_A\otimes p_B\), and the joint Shannon entropy satisfies

\[
H(K_\varepsilon)
=H(K_0)-c_4(X)\varepsilon^4+O(\varepsilon^6),
\]

with explicit nonnegative coefficient

\[
c_4(X)=
\frac12
\sum_{I\subseteq E_A,\;J\subseteq E_B}
\frac{r_{I,J}(X)^2}{p_A(I)p_B(J)}
\ge 0.
\]

Moreover,

\[
c_4(X)=0\quad\Longleftrightarrow\quad X=0.
\]

Thus every nonzero cross-block coupling direction has a strictly negative quartic entropy variation:

\[
H(K_\varepsilon)-H(K_0)=-c_4(X)\varepsilon^4+O(\varepsilon^6),
\qquad c_4(X)>0.
\]

For the R3 midpoint sign convention, the symmetric chord \(K_{\pm\varepsilon}\) around \(K_0\) has

\[
\Delta(\varepsilon)=\frac{H(K_{-\varepsilon})+H(K_{\varepsilon})}{2}-H(K_0)
=-c_4(X)\varepsilon^4+O(\varepsilon^6).
\]

So this local decoupling structure is a negative-gap mechanism near \(\varepsilon=0\), not a source of positive R3 gaps.

## Multiple coupling parameters

If the cross block is \(X(\theta)=\sum_{\alpha=1}^d\theta_\alpha X_\alpha\), then

\[
r_{I,J}(\theta)=r_{I,J}(X(\theta))
\]

is homogeneous quadratic in \(\theta\), and

\[
c_4(\theta)=\frac12\sum_{I,J}
\frac{r_{I,J}(\theta)^2}{p_A(I)p_B(J)}
\]

is homogeneous quartic. The equality condition is

\[
c_4(\theta)=0
\quad\Longleftrightarrow\quad
X(\theta)=0,
\]

so any parameter-kernel degeneracy is only the trivial one where the aggregate cross block vanishes.
