# C4 route: a finite-response lemma and the first closed polynomial threshold

Status: **PROVED AS AN AUTHOR LEMMA / PENDING_REVIEW**.

Scope: this file repairs only the response-regularity step.  It does **not** claim to repair the original PR66 quantifier `p>4`.  The theorem obtained below is a new weaker theorem with threshold `p>8`.  The original `p>4` claim remains INCOMPLETE.

The argument is for the true stationary DPP configuration law, with the physical affine symbol `c+t g`.  No spectral entropy, fermionic entropy, rotated observation basis, or `L`-affine surrogate is used.

## 1. Input already available from PR66

Let

\[
q=(p+2)/4,
\qquad a:=2q-1=p/2.
\]

For a strict-margin half-period-even center `c` and half-period-odd direction `g`, PR66 proves on a common complex `t`-disk:

1. complete-event inverses obey a uniform weighted Schur bound in `S_q`;
2. for a future-bit flip at coordinate `j`, the one-sided conditional satisfies
   \[
   |G_t(\cdot\mid x)-G_t(\cdot\mid y)|\le C(1+j)^{-2q};
   \]
3. if two futures agree through coordinate `n`, then
   \[
   |\log G_t(a\mid x)-\log G_t(a\mid y)|\le C(1+n)^{1-2q}=C(1+n)^{-a}.
   \]

The exponent relevant for one-sided transfer operators is therefore `a=p/2`, not `2q`.

## 2. Parameter derivatives do not worsen the memory exponent

### Lemma 2.1 (derivatives 0..4 retain the two-leg exponent)

For each `r=0,1,2,3,4`, after shrinking the common complex disk if needed,

\[
\sup_{|t|\le t_0}\sup_{x\stackrel{\ne j}=y}
\bigl|\partial_t^r \log G_t(a\mid x)-\partial_t^r \log G_t(a\mid y)\bigr|
\le C_r(1+j)^{-2q},
\tag{2.1}
\]

and hence

\[
\operatorname{var}_n(\partial_t^r\log G_t)
\le C'_r(1+n)^{-a}.
\tag{2.2}
\]

#### Proof

Write the finite-future Schur complement as

\[
Q_t=\mu-u_tM_t^{-1}v_t.
\]

Here `u_t,v_t` are affine in `t`, `M_t=M_0+tT(g)`, and on the common disk `M_t^{-1}` is uniformly bounded in the Banach algebra `S_q`.

For `r>=1`,

\[
\partial_t^r M_t^{-1}=(-1)^r r!\,M_t^{-1}(T(g)M_t^{-1})^r.
\tag{2.3}
\]

Because `S_q` is a Banach algebra and `T(g)` is bounded in `S_q`, every derivative in (2.3) has a uniform `S_q` bound.  A flip of one conditioned bit is still a rank-one diagonal perturbation.  Differentiating the resolvent identity produces a finite sum of terms with one factor propagating from the origin to `j`, one factor propagating back from `j` to the origin, and bounded `S_q` factors between them.  Each long leg is `O((1+j)^{-q})`; therefore every term is `O((1+j)^{-2q})`.  Derivatives falling on `u_t` or `v_t` merely replace one affine Toeplitz row by the corresponding row of `T(g)` and have the same `S_q` decay.  This proves the analogue of the PR66 two-leg estimate for `Q_t`.

Strict non-nullness on a smaller disk makes `z->log z` analytic on a common compact set avoiding zero.  Faà di Bruno therefore expresses `partial_t^r log Q_t` as a polynomial in `Q_t^{-1}` and the derivatives `partial_t^j Q_t`; all factors except the unique remote two-leg difference are uniformly bounded.  This gives (2.1).  Summing single-coordinate flips over `j>n` yields

\[
\sum_{j>n}(1+j)^{-2q}=O(n^{1-2q})=O(n^{-a}),
\]

which is (2.2).  QED.

There is thus **no regularity loss in parameter differentiation through order four**.  All loss below comes from solving Poisson equations.

## 3. The polynomial-variation scale

Let `X={0,1}^{N}` be the future space.  For `b>0`, define

\[
\operatorname{var}_n F:=\sup\{|F(x)-F(y)|:x_1^n=y_1^n\},
\]

and

\[
\mathcal B_b:=\left\{F\in C(X):
\|F\|_b:=\|F\|_\infty+\sup_{n\ge1}(1+n)^b\operatorname{var}_nF<\infty\right\}.
\tag{3.1}
\]

If `b1>b0`, then `B_{b1}` embeds continuously into `B_{b0}`.

For real small `t`, define the normalized transfer operator

\[
(\mathcal L_tF)(x)=\sum_{a=0}^1G_t(a\mid x)F(ax).
\tag{3.2}
\]

The stationary DPP future law `nu_t` satisfies `nu_t L_t=nu_t` and `L_t 1=1`.

By Lemma 2.1, for every `r<=4`, `partial_t^r G_t` and `partial_t^r log G_t` lie uniformly in `B_a`.

## 4. A coupling estimate and the Poisson loss

The only external mixing input used here is the normalized-chain coupling theorem of Bressaud--Fernandez--Galves (EJP 1999, arXiv:math/9806132).  Their Theorem 1 applies to a normalized finite-alphabet `g`-function with summable variations; their coupling parameter is

\[
\gamma_n=1-e^{-\operatorname{var}_n\phi}
\]

for `phi=log G`, and Proposition 2(iv) gives `gamma_n^*=O(gamma_n)` when `gamma_n` is polynomial.  In our case

\[
\operatorname{var}_n\phi_t=O(n^{-a}),\qquad a>2
\]

uniformly for small real `t`, hence

\[
\gamma_n^*(t)\le C(1+n)^{-a}
\tag{4.1}
\]

with a common constant after shrinking the parameter interval.

We need a slightly more explicit consequence than their displayed correlation inequality.

### Lemma 4.1 (weak relaxation on `B_b`)

Let `1<b<=a`.  There is a common `C_b` such that for every small real `t`, every `F in B_b`, and every `n>=1`,

\[
\|\mathcal L_t^n(F-\nu_tF)\|_\infty
\le C_b\|F\|_b(1+n)^{-b}.
\tag{4.2}
\]

#### Proof

Couple two complete-connection chains started from arbitrary futures using the BFG maximal coupling.  If the most recent disagreement at time `n` lies `k` sites back, the two arguments of `F` agree in their first `k` coordinates, so their `F`-difference is at most `var_k F`.  The BFG domination gives a return/disagreement mass bounded by a convolution of the polynomial continuity sequence and `gamma^*`.  The same calculation as BFG (their proof of (2.12), equations (5.1)--(5.9)) with `var_k F<=||F||_b(1+k)^{-b}` in place of a variation proportional to `var_k phi` gives

\[
\sup_{x,y}|\mathcal L_t^nF(x)-\mathcal L_t^nF(y)|
\le C\|F\|_b\sum_{k=0}^n(1+k)^{-b}(1+n-k)^{-a}
 +C\|F\|_b(1+n)^{-b}.
\]

For `b<=a` and `b>1`, the convolution is `O(n^{-b})`.  Integrating one endpoint against `nu_t` gives (4.2).  QED.

### Lemma 4.2 (Poisson inverse loses two powers)

Let `2<b<=a` and let `Pi_tF=F-nu_tF`.  Define

\[
\mathcal R_tF:=\sum_{n=0}^\infty\mathcal L_t^n\Pi_tF.
\tag{4.3}
\]

Then the series converges uniformly and

\[
\mathcal R_t:\mathcal B_b\longrightarrow\mathcal B_{b-2}
\]

is bounded uniformly for small real `t`:

\[
\|\mathcal R_tF\|_{b-2}\le C_b\|F\|_b.
\tag{4.4}
\]

Moreover `(I-L_t)R_tF=Pi_tF`.

#### Proof

Uniform convergence follows from (4.2) because `b>1`.

Fix futures `x,y` agreeing through coordinate `m`.  Couple the first `n` generated symbols.  Before the first coupling failure, the generated symbols agree.  At generation step `r`, the discrepancy probability is bounded by `C(m+r)^{-a}`; summing over `r` gives a failure probability at most `C m^{1-a}`.  Conditional on no failure, the arguments of `F` agree through at least `m+n`, so

\[
\operatorname{var}_m(\mathcal L_t^nF)
\le C\|F\|_b\bigl((m+n)^{-b}+m^{1-a}\bigr).
\tag{4.5}
\]

For the centered term we also have from (4.2)

\[
\operatorname{var}_m(\mathcal L_t^n\Pi_tF)
\le 2C_b\|F\|_b(1+n)^{-b}.
\tag{4.6}
\]

Split the Poisson series at `n=m`.  For `n<=m`, use (4.5); since `b<=a`,

\[
\sum_{n=0}^m\bigl((m+n)^{-b}+m^{1-a}\bigr)
=O(m^{1-b})+O(m^{2-a})=O(m^{2-b}).
\]

For `n>m`, use (4.6):

\[
\sum_{n>m}(1+n)^{-b}=O(m^{1-b})=O(m^{2-b}).
\]

Thus `var_m R_tF<=C||F||_b m^{2-b}`, proving (4.4).  The Poisson identity follows by telescoping partial sums and using (4.2).  QED.

The `two-power loss` is the load-bearing quantitative conclusion of this unit.

## 5. Transfer-operator parameter derivatives

Because the half-period symmetry gives

\[
T(c-tg)=D\,T(c+tg)\,D,\qquad D_{jj}=(-1)^j,
\]

all complete configuration probabilities are unchanged by `t -> -t`.  Therefore

\[
\nu_t=\nu_{-t},\qquad G_t=G_{-t}
\tag{5.1}
\]

for real small `t`.  The common analytic continuation from PR66 makes `G_t` an even analytic function of `t`, so there is a `C^2` family in

\[
s=t^2\ge0,
\]

which we denote `G_s`, `L_s`, `nu_s`, `ell_s=log G_s`.

The derivatives `partial_s^j G_s`, `partial_s^j ell_s`, `j=0,1,2`, retain the same `B_a` bound.  This follows either by even power-series coefficients on the common complex disk or directly from Lemma 2.1.

For `j=1,2`, define

\[
A_{j,s}:=\partial_s^j\mathcal L_s.
\]

If `0<b<=a`, multiplication and the one-step prepend map give

\[
A_{j,s}:\mathcal B_b\to\mathcal B_b
\tag{5.2}
\]

uniformly.  Indeed the product of a `B_a` coefficient and a `B_b` observable lies in `B_b` when `b<=a`.

## 6. Finite second-order response lemma

### Lemma 6.1 (C2 response with two Poisson losses)

Assume a normalized, uniformly non-null finite-alphabet kernel family `G_s` satisfies, on `|s|<s0`,

\[
\sup_s\|\partial_s^j\log G_s\|_{\mathcal B_a}<\infty,
\qquad j=0,1,2,
\tag{6.1}
\]

for some `a>4`, and the BFG polynomial relaxation (4.1) holds uniformly.  Then for every `F_s` that is `C^2` as a `B_a`-valued family,

\[
s\mapsto \nu_s(F_s)
\]

is `C^2`.  The first two derivatives are obtained from the absolutely convergent Poisson formulas.  At a fixed `s`, writing `Pi=Pi_s`, `R=R_s`, `A_j=A_{j,s}`, and suppressing the explicit derivatives of `F_s`, the invariant-measure part is

\[
D\nu_s(F)=\nu_s\bigl(A_1 R\Pi F\bigr),
\tag{6.2}
\]

and

\[
D^2\nu_s(F)
=\nu_s\bigl(A_2R\Pi F\bigr)
+2\nu_s\bigl(A_1R\Pi A_1R\Pi F\bigr),
\tag{6.3}
\]

with the standard additional Leibniz terms `2 Dnu_s(F'_s)+nu_s(F''_s)` for a moving observable.

#### Proof

Take any exponent `b` with

\[
4<b<a.
\tag{6.4}
\]

Then `B_a` embeds into `B_b`.  By Lemma 4.2,

\[
R:B_b\to B_{b-2},
\qquad
R:B_{b-2}\to B_{b-4},
\tag{6.5}
\]

because `b-2>2`.  The derivative operators `A_1,A_2` preserve each of these spaces by (5.2).  Thus every term in (6.2)--(6.3) is well-defined and bounded.

For a difference quotient, subtract `nu_{s+h}L_{s+h}=nu_{s+h}` from `nu_sL_s=nu_s`, apply the identity on centered observables

\[
(I-L_s)R_s\Pi_s=\Pi_s,
\]

and use the `C^2` operator Taylor expansion supplied by (6.1),(5.2).  The first quotient converges to (6.2).  Repeating the same argument once more gives (6.3).  All remainders are dominated in `B_{b-4}` by the uniform bounds in (6.5), so convergence is uniform on a smaller `s`-interval.  This also proves continuity of the second derivative.  No fourth Poisson iterate is needed because the physical parity has reduced the problem to second order in `s=t^2`.  QED.

### Boundary / finite-memory error

Let `G_s^{[N]}` be the canonical memory-`N` truncation obtained by freezing the tail after coordinate `N`.  From (6.1), for every `b<a`,

\[
\|\partial_s^j(\log G_s-\log G_s^{[N]})\|_{B_b}
\le C_{b,j}N^{b-a},\qquad j=0,1,2.
\tag{6.6}
\]

Choose `b=4+eta` with `0<eta<a-4`.  The two Poisson bounds in (6.5), the resolvent identity, and the multilinear formulas (6.2)--(6.3) then give

\[
\max_{j=0,1,2}
\left|\partial_s^j\{\nu_s^{[N]}(F_s^{[N]})-\nu_s(F_s)\}\right|
\le C_{eta,F}N^{-(a-4-eta)}.
\tag{6.7}
\]

Thus the finite-memory boundary error is quantitative and uniform for `s` in a smaller interval.  In particular, no finite-window curvature extrapolation is being assumed.

## 7. Application to DPP entropy rate: a closed `p>8` theorem

For the stationary DPP configuration law,

\[
h(t)=-\nu_t(\ell_t),\qquad \ell_t=\log G_t.
\tag{7.1}
\]

PR66's two-leg estimate gives `a=p/2`.  Therefore Lemma 6.1 applies whenever

\[
p/2>4,
\qquad\text{i.e.}\qquad p>8.
\tag{7.2}
\]

Hence, for `p>8`, the function

\[
H(s):=h(c+\sqrt{s}\,g)
\]

is `C^2` near `s=0` (one-sided in real `s`, with the even analytic kernel giving the natural local extension).

The exact parity/relative-entropy argument already present in PR66 gives

\[
H'(0)=0.
\tag{7.3}
\]

Write

\[
H(s)=H(0)-A s^2+o(s^2).
\tag{7.4}
\]

The regularity-free matching/negative-association bound imported from accepted PR53 gives

\[
A\ge \frac{|\widehat g(k)|^4}{4\mu^2(1-\mu^2)}=2\alpha_k,
\qquad
\alpha_k=\frac{|\widehat g(k)|^4}{8\mu^2(1-\mu^2)}.
\tag{7.5}
\]

Because `H` is `C^2`,

\[
H'(s)=H''(0)s+o(s),
\qquad H''(0)=-2A.
\]

Returning to `t`,

\[
\frac{d^2}{dt^2}h(c+tg)
=2H'(t^2)+4t^2H''(t^2)
=-12A t^2+o(t^2).
\tag{7.6}
\]

Therefore

\[
\frac{d^2}{dt^2}\bigl(h(c+tg)+\alpha_k t^4\bigr)
=12(\alpha_k-A)t^2+o(t^2)
\le -12\alpha_k t^2+o(t^2)<0
\tag{7.7}
\]

for all sufficiently small nonzero `t`.  At `t=0` the second derivative is zero, so the corrected entropy is concave on a nonempty symmetric interval and strictly concave away from the center.

### New weak theorem

**Theorem (author proof, pending independent review).**  The frozen PR66 statement is valid with `p>8` in place of `p>4`.

This is a genuine theorem weakening, not a repair of the original quantifier.

## 8. Why Tanaka 2205.12561 does not by itself restore `p>4`

Primary source checked: H. Tanaka, *General asymptotic perturbation theory in transfer operators*, arXiv:2205.12561.

The mapping is as follows.

- Tanaka's Theorem 2.10 requires Banach spaces `B_0 superset ... superset B_{n+1}`, bounded perturbation coefficients `L_j:B_i->B_{i-j}`, and, critically, a reduced resolvent `R_lambda` bounded `B_1->B_0` **and on each stronger `B_j` itself**.
- In the present polynomial-variation scale, the directly proved bound is instead
  \[
  R:B_b\to B_{b-2}.
  \]
  It loses two powers and therefore does not satisfy the same-space resolvent hypothesis of Theorem 2.10.
- Tanaka Section 3.5 explains that the Gouezel--Liverani route supplies the required hypotheses under a strong Lasota--Yorke setup.  Its displayed condition (GL.3) has an exponentially contracting strong term.  No such estimate has been proved for the present polynomial-memory transfer operator, and it must not be inferred from summable variations.
- Tanaka Theorem 2.8 is weaker and pointwise, but it still requires the algebraic reduced inverse on its recursively defined domains and convergence of operator remainders.  Our Lemma 6.1 verifies the needed two-response algebra directly on `B_b -> B_{b-2} -> B_{b-4}` instead of claiming Theorem 2.8 automatically applies.

Thus Tanaka is a useful primary-source check on what a valid higher-order operator argument must contain; it is **not** a citation that closes PR66 at `p>4`.

## 9. Exact status of `p>4`

For `p>4` we have `a=p/2>2`.  Consequently:

- all parameter derivatives through order four retain memory `O(n^{-a})`;
- the first Poisson inverse `R:B_a->B_{a-2}` is controlled;
- the BFG relaxation sequence is summable;
- but a second Poisson inverse at the same level requires `a-2>2`, i.e. `a>4`.

Therefore the present verified C2-in-`s` mechanism does **not** close the range `4<p<=8`.

This is not a proof that the original theorem is false there.  It identifies the precise quantitative bottleneck of this response route: improve the Poisson regularity loss from two powers to less than `a-2`, exploit a DPP-specific cancellation in the second response, or use another response theorem whose assumptions can be mapped without an exponential Lasota--Yorke estimate.

## 10. Sources and page/theorem pins

1. X. Bressaud, R. Fernandez, A. Galves, *Decay of correlations for non Holderian dynamics. A coupling approach*, Electronic Journal of Probability 4 (1999), arXiv:math/9806132.  Definition of variation and normalized kernel: printed pp.2--3; Theorem 1: printed p.3; chain coupling and Corollary 1: printed pp.5--6; proof of the correlation estimate: printed pp.9--10; Proposition 2(iv), polynomial return rate: printed p.13.
2. H. Tanaka, *General asymptotic perturbation theory in transfer operators*, arXiv:2205.12561.  Abstract operator hypotheses (I)--(III): printed pp.5--6; Theorem 2.8: printed pp.12--13; Theorem 2.10 and its bounded reduced-resolvent assumptions: printed pp.13--14; Gouezel--Liverani conditions (GL.1)--(GL.5), including the strong Lasota--Yorke inequality and operator Taylor losses: printed pp.33--34; Theorem 3.20 mapping GL hypotheses to Theorems 2.8/2.10: printed p.35.

No large copyrighted passage is reproduced here; only theorem locations and the assumptions used in the mapping are recorded.
