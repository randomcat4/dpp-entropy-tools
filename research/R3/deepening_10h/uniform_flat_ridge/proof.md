# Proof of the uniform-flat-ridge claim

For an exact subset event (S\subseteq[n]), put (z_i=1) when (i\in S)
and (z_i=-1) otherwise, and let (Z_S=\operatorname{diag}(z_1,\ldots,z_n)).
The signed event-determinant formula gives

\[
\begin{aligned}
p_S(t)
&=(-1)^{|S^c|}\det\bigl(K(t)-I_{S^c}\bigr)\\
&=\det(Z_S)\det\bigl(\tfrac12Z_S+tD\bigr)\\
&=2^{-n}\det(I+2tZ_SD).
\end{aligned}
\]

At (t=0), all (2^n) exact atoms equal (u=2^{-n}).  Differentiating the
determinant at zero gives

\[
\frac{p'_S(0)}{u}=2\operatorname{tr}(Z_SD)
=2\sum_i z_iD_{ii}.
\]

The general entropy second derivative is

\[
H''=-\sum_S\frac{(p'_S)^2}{p_S}-\sum_Sp''_S\log p_S.
\]

At the uniform law the second sum vanishes because `log(p_S)` is constant and
(\sum_Sp''_S=0).  Averaging the first sum over independent uniform Rademacher
signs (z_i) yields

\[
H''(\tfrac12I)[D,D]
=-4\mathbb E\left(\sum_i z_iD_{ii}\right)^2
=-4\sum_iD_{ii}^2.
\]

This proves the Hessian formula and its exact nullspace.

Now assume `diag(D)=0`.  The second-order determinant expansion is

\[
\det(I+2tZ_SD)
=1-2t^2\operatorname{tr}(Z_SDZ_SD)+O(t^3)
=1-4t^2\sum_{i<j}z_iz_jD_{ij}^2+O(t^3).
\]

Write (p_S(t)=u(1+r_S(t))).  Then

\[
r_S(t)=-4t^2\sum_{i<j}z_iz_jD_{ij}^2+O(t^3).
\]

Since (H(p)=n\log2-\mathrm{KL}(p\|u)) and

\[
\mathrm{KL}(p\|u)
=\mathbb E_u[(1+r)\log(1+r)]
=\tfrac12\mathbb E_u[r^2]+O(t^5),
\]

orthogonality of the distinct Rademacher characters (z_iz_j) gives

\[
\mathbb E_u[r^2]
=16t^4\sum_{i<j}D_{ij}^4+O(t^5).
\]

The complement of a DPP with kernel (K) is a DPP with kernel (I-K).
Complementation is a bijection of exact subsets and preserves entropy, so

\[
H(\tfrac12I+tD)=H(\tfrac12I-tD).
\]

Analyticity in the strict interior removes all odd Taylor terms.  Therefore

\[
H(\tfrac12I+tD)
=n\log2-8t^4\sum_{i<j}D_{ij}^4+O(t^6).
\]

For nonzero zero-diagonal (D), the displayed quartic coefficient is strictly
negative.  Differentiating the even analytic expansion twice gives the stated
strictly negative radial curvature for all sufficiently small nonzero (t).

Finally, (n\log2) is the maximum entropy of any law on (2^n) outcomes.  If
a DPP law is uniform, then

\[
K_{ii}=\Pr(i\in Y)=\tfrac12
\]

and, for every (i\ne j),

\[
\tfrac14=\Pr(i,j\in Y)=K_{ii}K_{jj}-K_{ij}^2
=\tfrac14-K_{ij}^2.
\]

Thus every off-diagonal entry vanishes and (K=I/2).  Conversely (I/2)
gives the uniform subset law, proving uniqueness.
