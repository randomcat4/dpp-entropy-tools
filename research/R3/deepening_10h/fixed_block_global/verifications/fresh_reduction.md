STATUS: CORRECT

# Fresh verification of FT-A fixed-block proof

Role: non-author verifier for FT-A.  I did not revise the author proof.

## Files read

- `research/R3/deepening_10h/frozen_theorem_v1.md`, FT-A section.
- `research/R3/deepening_10h/hazards.md`.
- `research/R3/deepening_10h/lemma_ledger.md`.
- `research/R3/deepening_10h/fixed_block_global/frozen_claim.md`.
- `research/R3/deepening_10h/fixed_block_global/proof.md`.
- `research/R3/deepening_10h/fixed_block_global/hazards.md`.
- `research/R3/deepening_10h/fixed_block_global/verdict.md`.

No external search was run.  No server was used.

## Verdict

The proof establishes the frozen FT-A claim:

\[
H(K)\le H(A)+H(B)=H(A\oplus B),
\qquad
H(K)=H(A)+H(B) \Longleftrightarrow X=0,
\]

for every finite real symmetric strict DPP marginal kernel

\[
K=\begin{pmatrix}A&X\\X^T&B\end{pmatrix},\qquad 0<K<I.
\]

The optional quantitative corollary

\[
H(A)+H(B)-H(K)\ge 8\max_{i\in E_A,j\in E_B}X_{ij}^4
\]

is also correct with natural logarithms and total variation defined as
\(\operatorname{TV}(P,Q)=\frac12\|P-Q\|_1\).

## Checkpoints

### 1. Block marginal DPP semantics

Author proof lines 17--31 are correct.  Principal submatrices of `K` and
`I-K` show `0<A<I` and `0<B<I` for nonempty blocks.  For
`U subset E_A`,

\[
\Pr(U\subseteq Y_A)=\Pr(U\subseteq Y)=\det K_U=\det A_U,
\]

and similarly for `B`.  This uses inclusion probabilities only, not the
incorrect event-probability reading of \(\det K_S\).

### 2. Entropy/KL/mutual information identity

Author proof lines 43--63 correctly identify

\[
H(A)+H(B)-H(K)
=H(Y_A)+H(Y_B)-H(Y_A,Y_B)
=D(P\|P_A\otimes P_B)
=I(Y_A;Y_B).
\]

The pair \((Y_A,Y_B)\) determines \(Y\) because the blocks are disjoint, so
`H(K)=H(Y_A,Y_B)` is faithful to the full subset law.

### 3. KL nonnegativity and strict equality

Lines 65--95 are correct.  The inequality

\[
p\log(p/q)\ge p-q
\]

with natural logs gives \(D(P\|Q)\ge 0\).  In the strict DPP setting, exact
atoms of the joint law are positive via

\[
\Pr(Y=S)=\det(I-K)\det L_S,\qquad L=K(I-K)^{-1}>0,
\]

so equality in the summed inequality forces \(P(\omega)=Q(\omega)\) for every
atom.  Marginal atoms are positive as sums of positive joint atoms, hence
\(Q=P_A\otimes P_B\) has no hidden zero-support issue.  Therefore equality is
exactly independence of the block configurations.

### 4. \(X=0\Rightarrow\) independence

Lines 97--117 are correct.  When \(X=0\), the kernel is \(A\oplus B\), and
for \(U\subseteq E_A,V\subseteq E_B\),

\[
\Pr(U\cup V\subseteq Y)=\det A_U\,\det B_V.
\]

These are the inclusion probabilities of the product DPP law.  Finite
inclusion probabilities determine exact atoms by Möbius inversion, so the
full event law factors.

### 5. Independence \(\Rightarrow X=0\)

Lines 119--155 are correct.  If \(Y_A\) and \(Y_B\) are independent, then for
each singleton pair \(i\in E_A,j\in E_B\),

\[
\Pr(i,j\in Y)=\Pr(i\in Y)\Pr(j\in Y).
\]

DPP inclusion probabilities give

\[
\Pr(i\in Y)=A_{ii},\quad \Pr(j\in Y)=B_{jj},\quad
\Pr(i,j\in Y)=A_{ii}B_{jj}-X_{ij}^2.
\]

Hence \(X_{ij}^2=0\), so \(X_{ij}=0\).  Since the pair was arbitrary, the
whole cross block vanishes.

### 6. Empty blocks and boundary

Lines 163--189 cover the frozen edge cases.  If one block is empty, the
cross-block matrix is the unique empty zero matrix and the statement reduces
to \(H(K)=H(K)+0\).  The theorem is strict, \(0<K<I\), so the proof does not
need support-aware boundary KL conventions.  The author correctly does not
claim a non-strict extension.

### 7. Sign conjugacy

Lines 169--183 are correct.  With

\[
D=\operatorname{diag}(I_{E_A},-I_{E_B}),
\]

the matrix with cross block \(-X\) is \(DKD\).  Every principal determinant is
preserved because \(\det(D_S K_S D_S)=\det(D_S)^2\det K_S=\det K_S\).  Thus
the DPP law and entropy are unchanged under \(X\mapsto -X\), matching the
\(X_{ij}^2\) obstruction.

## Pinsker constant audit

Let \(U_i=\mathbf1_{\{i\in Y\}}\), \(V_j=\mathbf1_{\{j\in Y\}}\),
\(a=A_{ii}\), \(b=B_{jj}\), and \(c=X_{ij}^2\).  The DPP two-point inclusion
probability is \(ab-c\).  Therefore the joint table differs from the product
Bernoulli table by

\[
\begin{array}{c|cc}
&V=0&V=1\\ \hline
U=0&-c&+c\\
U=1&+c&-c
\end{array}
\]

up to row/column ordering.  Thus

\[
\|P_{UV}-P_U\otimes P_V\|_1=4c,
\qquad
\operatorname{TV}=2c.
\]

Pinsker's inequality with natural logarithms and
\(\operatorname{TV}=\frac12\|\cdot\|_1\) is

\[
D(P\|Q)\ge 2\operatorname{TV}(P,Q)^2.
\]

Hence

\[
I(U_i;V_j)\ge 2(2c)^2=8c^2=8X_{ij}^4.
\]

Data processing for the deterministic maps
\((Y_A,Y_B)\mapsto(U_i,V_j)\) gives

\[
I(Y_A;Y_B)\ge I(U_i;V_j).
\]

Taking the maximum over cross-block entries is valid because the bound holds
for every pair \(i,j\).  The constant `8` is therefore correct under the
stated conventions.

### Minimal 2x2 sanity check

Take

\[
K=\begin{pmatrix}1/2&1/4\\1/4&1/2\end{pmatrix}.
\]

Its eigenvalues are \(1/4,3/4\), so \(0<K<I\).  Here

\[
x=1/4,\quad c=x^2=1/16,
\]

and the exact atom table is

\[
(p_{00},p_{01},p_{10},p_{11})=(3/16,5/16,5/16,3/16).
\]

The product Bernoulli table has all entries \(1/4\), so

\[
\operatorname{TV}=\frac12\left(4\cdot\frac1{16}\right)=\frac18.
\]

The Pinsker lower bound is

\[
8x^4=8/256=1/32=0.03125.
\]

The exact mutual information is

\[
2\cdot\frac{3}{16}\log\frac34
+2\cdot\frac{5}{16}\log\frac54
\approx 0.03158394240196324956,
\]

which is indeed larger than \(1/32\).  This catches the common factor-of-two
TV convention error and supports the stated constant.

## Nonclaims checked

- The proof does not assert full concavity on the whole real DPP domain.
- It does not use finite numerical evidence for the main theorem.
- It does not use \(\det K_S\) as exact event probability.
- It positions the information-theoretic part as classical, not as a novelty
  claim.

No critical gap found.
