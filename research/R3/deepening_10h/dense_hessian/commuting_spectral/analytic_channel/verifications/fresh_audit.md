# D10-M3 fresh non-author audit: commuting spectral analytic channel

STATUS: **CORRECT**

This audit verifies the frozen `analytic_channel/` author materials as a
reduction and as a collection of stated sufficient subclasses.  It does not
upgrade the unresolved generic fixed-\(Q\) commuting-spectral PSD/NSD problem
to a theorem.  The Shepp--Olkin concavity of Poisson-binomial count entropy is
accepted here as the author-labelled imported theorem; I did not reprove that
external theorem in this audit.

## Files and scope checked

Author files read:

- `frozen_claim.md`
- `derivation.md`
- `lemma_ledger.md`
- `hazards.md`
- `sanity_report.md`
- `verdict.md`
- `channel_sanity.py`
- `channel_sanity_results.json`

New independent verification files:

- `verifications/fresh_channel_audit.py`
- `verifications/fresh_channel_audit_results.json`

No author file or main README was modified.

## 1. Spectral-subset / projection-DPP channel representation

The mixture representation is exact.

For \(K(t)=Q\Theta(t)Q^\top\), let the latent spectral subset \(R\) have
independent Bernoulli law
\[
\mu_t(R)=\prod_{i\in R}\theta_i(t)\prod_{i\notin R}(1-\theta_i(t)).
\]
Conditional on \(R\), the projection kernel is
\[
P_R=Q_RQ_R^\top .
\]
Its exact atom probability is
\[
T_Q(S\mid R)=\det(Q_{S,R})^2
\]
when \(|S|=|R|\), and zero otherwise.  This is normalized by Cauchy--Binet:
\[
\sum_{|S|=|R|}\det(Q_{S,R})^2=\det(Q_R^\top Q_R)=1.
\]

For any inclusion event \(A\subseteq Y\), the mixture gives
\[
\sum_R\mu_t(R)\det(P_R[A,A])
=\sum_{|L|=|A|}\det(Q_{A,L})^2\prod_{i\in L}\theta_i(t)
=\det(Q_A\Theta(t)Q_A^\top)=\det K(t)_A .
\]
Finite Möbius inversion then identifies the exact atom law with the DPP atom
law.  This checks the author route from inclusion probabilities to exact
events; it is not merely a heuristic spectral sampling statement.

The strict interior assumption \(0<\theta_i(t)<1\) implies \(0<K(t)<I\).  Hence
all exact atoms are positive, for example from the equivalent \(L\)-ensemble
formula \(p(S)=\det(I-K)\det L_S\) with \(L=K(I-K)^{-1}\succ0\).  The logarithms
and entropy derivatives used later are therefore legitimate inside the stated
domain.

## 2. \(p,p',p''\) and \(H''\)

The derivative formulas in the author claim are correct.

Write \(x_i={\bf1}_{i\in R}\) and
\[
s_i(R,t)=v_i\left(\frac{x_i}{\theta_i(t)}
-\frac{1-x_i}{1-\theta_i(t)}\right).
\]
Then
\[
a_R(t)=\sum_i s_i(R,t),\qquad
\mu'_t(R)=\mu_t(R)a_R(t).
\]
Because each Bernoulli factor is affine in \(t\), the diagonal second
derivatives cancel in \(\mu''\), leaving only cross terms:
\[
\mu_t''(R)=2\mu_t(R)\sum_{i<j}s_i(R,t)s_j(R,t).
\]
This is exactly the author's \(b_R(t)\) formula after expanding \(s_i\).

Since \(T_Q\) is independent of \(t\),
\[
p_t^{(j)}(S)=\sum_R T_Q(S\mid R)\mu_t^{(j)}(R),\qquad j=0,1,2.
\]
Finally, with \(\sum_Sp'_t(S)=\sum_Sp''_t(S)=0\),
\[
H(Y_t)''
=-\sum_S\frac{p_t'(S)^2}{p_t(S)}
-\sum_Sp_t''(S)\log p_t(S).
\]

The independent script checked a rational \(n=3\) Householder case by comparing
signed exact-event determinant derivatives with the channel derivative formula:

- max signed-vs-channel derivative difference: `0`
- \(\sum p=1\), \(\sum p'=0\), \(\sum p''=0\)
- minimum atom at \(t=0\): `1213/13720`
- \(H''(Y)=-0.247225796743571035801622156686535982796898329941605679648413553054811926262174137465161647\)

## 3. Cardinality split and posterior/channel correction

The cardinality split is correct.  A projection DPP with kernel \(P_R\) has
rank \(|R|\), hence \(|Y|=|R|\) almost surely.  Therefore
\[
H(Y_t)=H(N_t)+H(Y_t\mid N_t),\qquad N_t=|R|=|Y_t|.
\]

The script independently recomputed the split in the same rational \(n=3\)
case:

- \(H(Y)=2.05533698937844874783274106186194068222138153456285506988777403967438291538768283643069582\)
- \(H(N)=1.23772695542779891231569290609742330932845773876383202733864668714228121814825692244244144\)
- \(H(Y\mid N)=0.817610033950649835517048155764517372892923795799023042549127352532101697239425913988254371\)
- split residual: `9E-90`

It also checked the second-derivative split:

- \(H''(Y)=-0.247225796743571035801622156686535982796898329941605679648413553054811926262174137465161647\)
- \(H''(N)=-0.111945815623717782871500624303184300769059944173196201272351189160576675006880946127432436\)
- \(\Psi''=H''(Y)-H''(N)\)
  `=-0.135279981119853252930121532383351682027838385768409478376062363894235251255293191337729211`
- direct \(\Psi''\) formula residual: `0E-90`

Thus the author statement that any positive curvature must pass through
\(\Psi_Q(t)=H(Y_t\mid |Y_t|)\), after the controlled count term, is accurate.

## 4. Cardinality-uniform sufficient condition

The stated sufficient condition is correct and properly limited.

If every same-cardinality squared minor satisfies
\[
\det(Q_{S,R})^2=\binom nk^{-1}\qquad (|S|=|R|=k),
\]
then for fixed \(N=k\) the output \(Y\) is uniform over \(k\)-subsets and is
independent of the spectral posterior inside that layer.  Hence
\[
H(Y_t)=H(N_t)+\mathbb E\log\binom n{N_t}.
\]

More generally, if \(H(Y\mid N=k)=c_k\) is independent of \(t\), then
\[
\frac{d^2}{dt^2}\mathbb E c_{N_t}
=2\sum_{i<j}v_iv_j\,
\mathbb E\!\left[c_{N_{-ij}+2}-2c_{N_{-ij}+1}+c_{N_{-ij}}\right].
\]
For one-sign spectral rates, \(v_iv_j\ge0\).  For
\(c_k=\log\binom nk\),
\[
\Delta^2c_k
=\log\frac{(n-k-1)(k+1)}{(k+2)(n-k)}\le0.
\]
So this conditional term is concave; combined with the imported
Shepp--Olkin count concavity, the total entropy is concave.

The author does not claim generic existence or classification of such channels,
and that limitation is necessary.

Finite sanity used \(n=4\),
\(\lambda=(1/5,2/7,3/8,5/9)\),
\(v=(1/31,2/37,1/41,3/43)\):

- \(H''(N)=-0.0149238012896797026831369958237778729414078994088009577323145349875220690187139523298415707\)
- \((\mathbb E\log\binom nN)''
  =-0.0209166219158422810845284565464955389310770111849930505438751783874649957024209123819392240\)
- total second derivative:
  `-0.0358404232055219837676654523702734118724849105937940082761897133749870647211348647117807947`

This finite check is only a sanity check; the proof is the discrete-concavity
calculation above.

## 5. \(2\times2\) same-sign spectral rates and block direct sums

The \(2\times2\) proof is correct.

For \(n=2\), let
\[
r=\theta_1(1-\theta_2),\qquad s=(1-\theta_1)\theta_2 .
\]
For a real orthogonal \(Q\), the one-point channel has
\[
u=\alpha r+(1-\alpha)s,\qquad
w=(1-\alpha)r+\alpha s.
\]
The conditional singleton entropy is the perspective
\[
G(r,s)=-u\log\frac{u}{r+s}-w\log\frac{w}{r+s},
\]
which is concave in \((r,s)\).  Its partial derivatives are nonnegative
because \(0<u,w\le r+s\).  If \(v_1v_2\ge0\), then
\[
r''=s''=-2v_1v_2\le0.
\]
The chain rule gives \(G''\le0\).  Adding the count entropy \(H(N)\), already
concave, proves the claimed \(2\times2\) fixed spectral block.

The observation-coordinate direct-sum subclass is also closed as stated.  If
\(K\) is block diagonal across observation coordinates, exact DPP atoms
factorize across blocks, so entropy is additive.  A \(1\times1\) block is a
single Bernoulli entropy; a \(2\times2\) block is covered by the preceding
argument.  The author's global PSD/NSD statement, with all spectral rates
nonnegative or all nonpositive, is a safe sufficient hypothesis.  A slightly
broader per-block same-sign variant would also be blockwise concave, but the
author did not need to state it.

Independent direct-sum sanity used a rational \(2\times2\) rotation with entries
\(3/5,4/5\), plus one \(1\times1\) block:

- full \(H''\):
  `-0.0934958311799183099864815441508471953497035306368549176214354122133500982628252021631979213`
- \(2\times2\) block \(H''\):
  `-0.0816768099426145242062414702819644622010424041363932371043532330813094703773219703995783458`
- \(1\times1\) block \(H''\):
  `-0.0118190212373037857802400738688827331486611265004616805170821791320406278855032317636195753`
- full minus block-sum residual: `-2E-91`

## 6. Generic \(Q\) blocker

The generic-blocker wording is accurate.  Each fixed-cardinality channel block
is doubly stochastic, but pointwise entropy increase under a doubly stochastic
map does not imply concavity of \(t\mapsto H(T_{Q,k}\nu_t)\).  The remaining
object is exactly the curvature of the conditional layer law
\[
H(Y_t\mid |Y_t|).
\]

The independent script included a rational Householder matrix
\[
Q=I-\frac{1}{7}(1,2,3)(1,2,3)^\top,
\]
with
\[
\lambda=(3/4,1/2,1/2),\qquad v=(1/100,1,1).
\]
The singleton atom second derivatives were sign-indefinite:

- mask `001`: `2339/2450`
- mask `010`: `-829/2450`
- mask `100`: `-167/1225`

This is not a positive entropy-curvature candidate.  It is a sanity check that
the author was right not to treat doubly stochasticity or generic fixed \(Q\)
as a curvature certificate.

## Commands

Independent verification command:

```text
$env:OMP_NUM_THREADS='1'; $env:OPENBLAS_NUM_THREADS='1'; $env:MKL_NUM_THREADS='1'; $env:NUMEXPR_NUM_THREADS='1'; & 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'research/R3/deepening_10h/dense_hessian/commuting_spectral/analytic_channel/verifications/fresh_channel_audit.py'
```

Exit code: `0`.

I did not rerun the author `channel_sanity.py`, because that script writes its
result JSON beside the author files, and this verification was required not to
modify author materials.

## Final verdict

The D10-M3 `analytic_channel/` materials are correct as an analytic reduction
and as stated sufficient subclasses:

- exact spectral-subset / projection-DPP channel: correct;
- exact \(p,p',p''\) and \(H''\) formulas: correct;
- cardinality entropy split and posterior/channel correction: correct;
- cardinality-uniform sufficient condition under one-sign spectral rates:
  correct and properly restricted;
- \(2\times2\) same-sign spectral blocks and \(1\times1/2\times2\)
  observation-coordinate direct sums: correct as stated;
- generic \(Q\) blocker: accurately stated.

No general fixed-\(Q\), heterogeneous PSD/NSD concavity theorem is proved here,
and the author does not claim one.
