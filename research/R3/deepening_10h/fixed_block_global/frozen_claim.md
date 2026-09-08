# D10-A frozen claim: fixed block marginals maximize entropy at decoupling

STATUS: PROVED

Author status only. This is not a fresh-verifier `CORRECT` certificate.

## Claim FT-A

Let \(E=E_A\sqcup E_B\) be finite, allowing either block to be empty. Let

\[
K=\begin{pmatrix}
A&X\\
X^T&B
\end{pmatrix}
\]

be a real symmetric strict DPP marginal kernel:

\[
0<K<I.
\]

Let \(Y\subseteq E\) be the DPP with inclusion probabilities

\[
\Pr(T\subseteq Y)=\det K_T.
\]

Write

\[
Y_A=Y\cap E_A,\qquad Y_B=Y\cap E_B.
\]

Then the marginal laws of \(Y_A\) and \(Y_B\) are DPPs with kernels \(A\) and \(B\), respectively. With natural-log Shannon entropy,

\[
H(K)=H(Y_A,Y_B),\qquad H(A)=H(Y_A),\qquad H(B)=H(Y_B).
\]

The claim is

\[
H(K)\le H(A)+H(B)=H(A\oplus B),
\]

with equality if and only if

\[
X=0.
\]

Equivalently,

\[
H(A)+H(B)-H(K)=I(Y_A;Y_B)\ge0,
\]

and the mutual information vanishes if and only if the cross block of the marginal kernel vanishes.

## Quantitative corollary

If both blocks are nonempty, then the entropy deficit admits the crude global bound

\[
H(A)+H(B)-H(K)\ge 8\max_{i\in E_A,\;j\in E_B} X_{ij}^4.
\]

This bound uses natural logarithms and is not claimed to be sharp.

## Scope

This result covers the entire feasible fiber with fixed diagonal blocks \(A,B\). It does not prove full real-DPP entropy concavity along arbitrary affine chords, because such chords generally change the marginal blocks.

The information-theoretic inequality is classical. A point-process version for disjoint regions is also explicitly stated, for example, as Lemma III.2 in Baccelli--Woo, "On the entropy and mutual information of point processes", IEEE ISIT 2016. The D10-A contribution should therefore be described only as a DPP-kernel-space global search-exclusion corollary with the strict equality condition \(X=0\), not as a new entropy subadditivity theorem.
