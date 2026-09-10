# Fresh recheck and two complete edges of the moving-rank-two square

Status: **PROVED (fresh same-session derivation and exact certificate), PENDING_EXTERNAL_REVIEW** for Theorems 1 and 2 below. This is not an external reviewer report and does not approve PR86. The unrestricted moving-rank-two endpoint problem remains **INCOMPLETE**. No novelty or priority claim is made.

This continuation uses the same fixed matrices as PR86,
\[
 A=\begin{pmatrix}2/5&6/25\\6/25&2/5\end{pmatrix},\qquad
 B=\begin{pmatrix}3/5&9/25\\9/25&3/5\end{pmatrix},
\]
and the actual endpoint kernels
\[
 K_-=EAE^\top,\qquad K_+=VBV^\top,\qquad
 K_0=(K_-+K_+)/2,
\]
where
\[
 E=(e_1,e_2),\qquad
 V=(c_1e_1+s_1e_3,c_2e_2+s_2e_4),\qquad c_i^2+s_i^2=1,\quad c_i,s_i\ge0.
\]
Every entropy below is the Shannon entropy of the complete event law. The parameter used to compare different endpoint pairs is not called a `K`-affine entropy path: for each parameter value, the only Jensen midpoint is the genuine arithmetic matrix midpoint above.

## 1. Independent disposition of the existing PR86 claims

I did not treat the PR description, stored JSON, or earlier author labels as evidence. A new script, `extend_edges.py`, imports none of the PR86 author scripts. It reconstructs event probabilities from signed determinants and also checks the relevant Möbius laws.

The following bridges were rederived.

1. In the relative-sign theorem, changing `rz` from positive to negative changes only the complete events
\[
(p_\varnothing,p_1,p_2,p_{12})
 \mapsto(p_\varnothing+\delta,p_1-\delta,p_2-\delta,p_{12}+\delta).
\]
For either endpoint of this transfer,
\[
p_1p_2-p_\varnothing p_{12}
 =\det(I-K)^2L_{12}^2\ge0,\qquad L=K(I-K)^{-1}.
\]
Thus the odds-ratio derivative used in PR86 is a complete-event identity with coordinates 3 and 4 absent. No marginal event was substituted. I found no sign error in that theorem.

2. In the continuous small-angle box, deterministic deletion of the two bottom coordinates costs at most their expected number, and the remaining two-coordinate law obeys
\[
\operatorname{TV}(p_R,p_T)\le d_1+d_2+2|\det R-\det T|.
\]
The determinant bound and \(1-c_1c_2\le s_1^2+s_2^2\) reproduce exactly
\[
\operatorname{TV}\le\frac{31200}{6255001}.
\]
A separate rational-log calculation reproduces
\[
G_{\rm base}\in
[0.071729711441392005498563,\,
 0.071729711441392005498564],
\]
and the full continuity/marking error is at most
\(0.052057889467810647642976\). Hence the stated \(G>19/1000\) bound survives this recheck.

3. For the two method witnesses, the fresh determinant/Möbius implementation reproduces:
\[
\begin{array}{c|c|c}
& G& H(p_{K_0})-H((p_-+p_+)/2)\\ \hline
c_2=1&
[0.071868857724917481384897,\,
 0.071868857724917481384898]&
[-0.009195850054564499168246,\,
 -0.009195850054564499168245]\\
t_2=1/50&
[0.072425117028253334474095,\,
 0.072425117028253334474096]&
[-0.008881971160429267101924,\,
 -0.008881971160429267101923].
\end{array}
\]
Here the first row is the PR notation \(t_2=0\), hence \(c_2=1\). Full midpoint Fisher and acceleration independently reproduce the two strictly negative curvature intervals in PR86. They remain method counterexamples only.

4. The qualitative dilute theorem was rederived from
\[
p_{\lambda Z}(S)=\lambda^{|S|}q_S(\lambda),\qquad
\sum_S|S|p_{\lambda Z}(S)=\lambda\operatorname{tr}Z.
\]
For positive semidefinite \(Z\), \(\det Z_S=0\) indeed forces all larger principal determinants containing \(S\) to vanish. Therefore the cancellation of every apparent higher-order \(\lambda^m\log\lambda\) term is exact. I also rechecked the coefficient
\[
C(Z)=-\frac12\sum_i Z_{ii}^2
-\sum_{i<j}\Psi_{Z_{ii}Z_{jj}}(Z_{ij})
\]
and the displayed third-derivative bounds term by term. I found no blocking logical gap. The two stored dense-example remainder totals were not promoted to independent execution here; their external arithmetic review remains pending.

These findings justify continuing from the formulas, but they do not change the PR review state: there is still no external reviewer submission.

## 2. Full common-one-dimensional-support edge

Set \(c_2=1,s_2=0\), and write \(c=c_1\in[0,1]\). The effective coordinate set is \(\{1,2,3\}\). For \(0\le c<1\), the endpoint ranges intersect in exactly one dimension and the true midpoint has rank three.

Fresh signed-determinant expansion gives all eight midpoint atoms, in mask order:
\[
\begin{aligned}
p_\varnothing&=(305-54c-51c^2)/1250,\\
p_1&=(92+54c+279c^2)/1250,\\
p_2&=(395+54c-24c^2)/1250,\\
p_{12}&=(83-54c+171c^2)/1250,\\
p_3&=177(1-c^2)/1250,\quad
p_{13}=51(1-c^2)/1250,\\
p_{23}&=123(1-c^2)/1250,\quad
p_{123}=24(1-c^2)/1250.
\end{aligned} \tag{1}
\]
All are nonnegative on the closed interval, and the first four are strictly positive. No triple event is removed.

Let
\[
(\alpha_3,\alpha_{13},\alpha_{23},\alpha_{123})
=(177,51,123,24)/1250,\qquad
C_\alpha=\sum_T\alpha_T\log\alpha_T.
\]
Their total is \(3/10\). The endpoint marking identity is
\[
H(K_+)=H(B)+\frac35h(1-c^2).
\]
Combining the four bottom-event entropies with one half of this marking term removes the apparent \(\log(1-c^2)\) singularity exactly:
\[
\sum_T\eta(\alpha_T(1-c^2))-\frac3{10}h(1-c^2)
=-(1-c^2)C_\alpha+\frac3{10}c^2\log c^2. \tag{2}
\]
Consequently, with the final term interpreted continuously at \(c=0\),
\[
G'(c)=
-\sum_{S\subseteq\{1,2\}}p'_S(c)\log p_S(c)
+2cC_\alpha+\frac35c\log c^2. \tag{3}
\]

**Theorem 1.** For every \(c\in[0,1]\), \(G'(c)<0\) in the one-sided sense at the endpoints. Hence
\[
G(c)\ge G(1)>
0.071729711441392005498563>0. \tag{4}
\]

The sign in (3) is certified on the entire interval, not sampled. Divide \([0,1]\) into the 256 rational boxes
\([j/256,(j+1)/256]\). On each box the exact range of each quadratic in (1) is obtained from its endpoints and, when present, its rational vertex. Every logarithm is enclosed by
\[
\log x=k\log2+
2\sum_{m=0}^{31}\frac{z^{2m+1}}{2m+1}+R,\qquad
0\le R\le\frac{2z^{65}}{65(1-z^2)},\quad 0\le z\le1/3.
\]
Sign-aware rational interval multiplication is then applied directly to (3). All 256 upper bounds are negative. The least negative one is the first box:
\[
G'([0,1/256])<
-0.008169600336597196358228. \tag{5}
\]
The \(c\log c^2\) term is bounded above by zero on that first box, so no numerical lower cutoff at the zero event is used. The full box list is in `edge_extension_certificate.json`.

Since \(c=(1-t_1^2)/(1+t_1^2)\), Theorem 1 proves the midpoint inequality for the **entire**
\[
t_2=0,\qquad 0\le t_1\le1
\]
edge of the original rank-two family. This replaces the previous \(t_1\le1/50\) restriction on the common-line edge.

## 3. Full zero-intersection boundary edge

Now set \(c_2=0,s_2=1\) and put \(u=c_1^2\in[0,1]\). For every \(0\le u<1\), the endpoint supports have zero intersection and the true midpoint has rank four. At \(u=0\) the two coordinate supports are orthogonal; at \(u=1\) the supports share one coordinate.

All sixteen midpoint atoms are affine in \(u\). Eight remain positive at \(u=1\):
\[
\begin{array}{c|c}
S&781250\,p_S(u)\\ \hline
\varnothing&223652-33027u\\
1&62348+184527u\\
2&62348-4848u\\
12&9152+42723u\\
4&118473-7848u\\
14&33027+43848u\\
24&33027-1152u\\
124&4848+10152u .
\end{array} \tag{6}
\]
The other eight equal \(\alpha_S(1-u)\), with numerators over 781250
\[
(118473,33027,33027,4848,28152,7848,7848,1152) \tag{7}
\]
for \(S=(3,13,23,123,34,134,234,1234)\). Their total is again \(3/10\). Thus every quadruple and rare event is retained.

Since the midpoint atoms are affine, their entropy contributes only the complete Fisher term under differentiation in \(u\). The endpoint marking term is \((3/10)h(u)\). The eight terms in (7) contribute exactly \(3/[10(1-u)]\) to the midpoint Fisher, so cancellation gives
\[
G''(u)=\frac3{10u}
-\sum_{S\in\mathcal N}\frac{(p'_S)^2}{p_S(u)}, \tag{8}
\]
where \(\mathcal N\) is the eight-event set in (6).

Put (8) over the positive denominator
\(u\prod_{S\in\mathcal N}p_S(u)\). After removal of the positive integer content 2424, its numerator is a degree-seven polynomial. Its Bernstein coefficients on \([0,1]\) are
\[
\begin{aligned}
&1190084359026333481957347806848,\\
&2410422178182839641414707135880,\\
&30372781715665284826644157551250/7,\\
&48481589390762691536314338718750/7,\\
&68466165955246097536027568359375/7,\\
&12285893689808005587677001953125,\\
&95813767624688854503631591796875/7,\\
&13171187091300690174102783203125.
\end{aligned} \tag{9}
\]
Every coefficient is strictly positive, proving \(G''(u)>0\) on \(0<u\le1\).

The rare-event cancellation also gives a finite derivative at \(u=1\). Rational logarithm enclosures yield
\[
G'(1)\in
[-0.305109681214163582316644,\,
 -0.305109681214163582316643]. \tag{10}
\]
Because \(G'\) is increasing and its largest value is still negative,
\(G'(u)<0\) throughout. Finally,
\[
G(u)\ge G(1)\in
[0.543414410716967635348619,\,
 0.543414410716967635348620]. \tag{11}
\]

**Theorem 2.** The actual midpoint inequality is strict on the entire
\[
t_2=1,\qquad0\le t_1\le1
\]
edge. Except at \(t_1=0\), this is a zero-intersection moving-rank-two family with a rank-four midpoint. It is a continuous family theorem, not a collection of point probes.

## 4. Scope

Theorems 1 and 2 close two full edges of the fixed two-angle square. They do not determine its interior, do not cover arbitrary \(A,B\), and do not imply entropy concavity along the nonlinear frame parameter. The unresolved object is still the Jensen sign of the true arithmetic midpoint for each interior endpoint pair.

`extend_edges.py` is a narrow reconstruction/certificate script, not a scan framework. It imports no author code, reconstructs the laws from determinants, checks the old fixed witnesses and their complete Fisher/acceleration, and emits every interval box and the exact Bernstein data. Its successful execution in this session is a fresh same-session check, not external review.
