# Independent S1 FIRST report for PR136

## Verdict

**ACCEPTED_SCOPED_ANALYTIC_INTERFACE** at exact author head
`39098dac760cea2d27f2955bed31f80c87913810`.

No critical gap was found in the analytic implication from the accepted PR91
representation plus the supplied finite-node hypotheses to the claimed true
entropy-rate curvature.  The saved finite evidence itself was not recomputed
or independently certified by S1; that separate gate remains with S2.

## 1. Exact complete-law increment — pass

Grouping original sites into ordered two-site cells, the source defines

`h_r=(1/2)H(Y_0|Y_1,...,Y_r)`.

For `delta_n=2(h_(n-1)-h_n)`, conditional mutual information gives the exact
complete-law identity

`delta_n=sum_w p_n(w) KL(g_n(w)||g_(n-1)(w_1,...,w_(n-1)))`.

Here `p_n` is the changing law of every complete four-letter future word and
each `g` contains all four current-cell occupied/vacant outcomes.  Twice
differentiating therefore produces

`delta_n''=sum_w[p_n F_w''+2p_n'F_w'+p_n''F_w]`.

Neither derivative of the future-word law is dropped.

## 2. Full finite-word Fisher and acceleration budgets — pass

The accepted PR91 state-jet bounds, combined with the explicit quadratic
four-branch weights, give total conditional jets `gamma` and `gamma2` with

`sum gamma^2/g<3`, `sum|gamma2|<3`.

The complete word score is a sum of reverse-martingale differences.  Hence

`sum_w (p_n')^2/p_n<=3n` and `sum_w|p_n'|<=sqrt(3n)`.

Writing

`p_n''/p_n=S_n^2+sum_j(log g_j)''`

and retaining both `gamma2/g` and `(gamma/g)^2` gives

`sum_w|p_n''|<=9n`.

This is a full complete-word acceleration estimate, not a fixed-state Fisher
fragment.

## 3. Finite predictor-jet forgetting — pass

The two conditionals in the KL increment share `m=n-1` near-cell maps.  Their
terminal discrepancies include value, first derivative, and second derivative.
Solving the triangular recurrence

`dQ_new<=k dQ`,

`dJ_new<=k dJ+(3/2)dQ`,

`dH_new<=k dH+3dJ+10dQ`,

with `k=34/81` yields exactly the displayed `k^m` times constant, linear, and
quadratic polynomial bounds.  No limiting coding derivative or third
parameter derivative is inserted.

## 4. Differentiated quadratic KL — pass

For the four-component probability vectors, normalization gives `sum d_i=0`
and the Bregman representation

`KL(a||b)=sum_i d_i^2 int_0^1 (1-v)/(b_i+v d_i) dv`.

All denominators are at least `epsilon=81/1024`.  Differentiating this identity
twice, rather than differentiating a value inequality, gives the stated
`F0`, `F1(m)`, and `F2(m)` bounds.  The coefficients in the first- and
second-jet differences correctly include the state Hessian, mixed `t,Q`
derivative, and state acceleration.

Combining these estimates with the complete future-law bounds and
`2sqrt(3n)<=n+3` gives

`|delta_n''|<=lambda^(n-1)P(n-1)`,

where `lambda=(34/81)^2` and `P` is the displayed positive quadratic.

## 5. Genuine `C^2` entropy-rate passage — pass

The value, first-derivative, and second-derivative increment series are all
uniformly absolutely summable.  The uniform derivative-series theorem thus
proves an actual `C^2` limit and

`|h_r''-h''|<=E_r=(1/2)sum_(m=r)^infinity lambda^mP(m)`.

The indexing agrees with
`h_r-h=(1/2)sum_(n=r+1)^infinity delta_n`.  This is a true rate-derivative
tail; no finite `H_N''/N` sequence is extrapolated.  The exact geometric-sum
formula makes the claimed finite gate `E_9<115/10^6` directly auditable.

## 6. `r=9` complete conditional curvature — pass at the interface level

Stationarity and the two-site grouping give

`h_9=(H_20-H_18)/2`.

The production source enumerates `4^9` complete future words and all four
current outcomes, hence `4^10` current/future atoms per node.  Its jet variable
stores the quadratic Taylor coefficient; the factor two converting that
coefficient to a second derivative cancels the factor `1/2` returning from a
cell to an original coordinate.  The entropy leaf also retains the changing
future probability through all three product-jet terms.

S1 checked this formula and enumeration interface statically.  S1 did not
certify that the supplied row endpoints are the output of a correct execution.

## 7. Zero-free complex neighborhood — pass

The four closed parameter cells have centers
`5/8,7/8,9/8,11/8` and half-width `1/8`.  Their Bernstein ellipse with
parameter `rho=3` lies within complex distance `5/24` of its center.

At a real center `t_0`, the symmetric signed complete-event matrix has

`sigma_min M_N(t_0)>=(2-t_0)/8>=5/64`,

while `||K_N'||<=1/8`.  Therefore

`||(z-t_0)M_N(t_0)^(-1)K_N'||<=1/3<1`.

Every complete event determinant is zero-free on the ellipse and its positive
real logarithm has a consistent analytic continuation.  Determinant and
trace-log bounds give

`sum_X|p_X(z)|<=(4/3)^N`,

`|log p_X(z)|<=3N`,

`|partial_z log p_X(z)|<=(12/5)N`,

`|partial_z^2 log p_X(z)|<=(12/5)^2N`.

These are bounds for complete event determinants, not spectral entropy.

## 8. Chebyshev continuum cover — pass

Differentiating the complete entropy and using `sum_X p_X''=0` yields

`|H_N''(z)|<=(4/3)^N(144/25)(3N^3+4N^2)`.

Thus the submitted rational expression bounds `|h_9''|` by `40000000` on
every ellipse.  For 32 first-kind nodes, the analytic Chebyshev coefficient
bound together with exact high-degree aliasing gives

`||h_9''-P_31||_infinity<=6(40000000)/3^32`.

Consequently the coefficient `l^1` bound plus this interpolation error and
`E_9` covers every point of each closed cell, including shared endpoints.  A
node sign by itself is never promoted to a continuum sign.

## 9. Static certificate-source interface — pass; evidence execution pending

All eight certificate artifacts were inspected.

- `make_inputs.py` constructs Machin bounds for pi, rational cosine Taylor
  enclosures, outward binary64 nodes, and the fixed log-two enclosure.
- `certify_nodes.cpp` uses outward one-neighbor padding after each binary64
  operation, an explicitly tailed atanh logarithm, full value/first/second
  jets, normalization-jet checks, and the exact leaf count.
- `check_certificate.py` reconstructs the KL-tail polynomial and `E_9`, the
  complex bound, the DCT coefficient intervals, all 128 node IDs, all leaf
  counts, and the four strict `-1/3000` gates.
- the four TSV parts expose 128 node rows; the summary is explicitly derived
  rather than represented as literal execution output.

The logical data flow is closed and does not require a hidden production
program.  Because S1 did not execute either source or independently bind the
published rows to the claimed run, the row validity and exact resulting
inequalities remain a finite-evidence question for S2.

## 10. Endpoint, gauge, and corollary audit — pass conditionally

Strict inequalities in the PR91 domain persist on a neighborhood of the
closed target interval, so the rate derivatives at both endpoints are genuine
derivatives, not merely open-cell limits.

The diagonal gauge `U_jj=(-1)^j` commutes with vacancy masks and sends `K_t` to
`K_(-t)`, so every complete atom is even in `t`.  Conditional on the positive
interval theorem, the same bound holds on `[-3/2,-1/2]`.

The boundary identity

`H_(2m)-2mh=2sum_(j=0)^(m-1)(h_j-h)`

and the `C^2` tail give the stated all-volume boundary-response sums.  Under
`s=t^2/256`, the chain rule is

`partial_s^2 Psi=(16384/t^2)Psi''-(16384/t^3)Psi'`.

For the parity relative-entropy rate `D(s)=h(0)-h(t(s))`, the exact physical
combination is

`h_tt=-(1/128)[D'(s)+2sD''(s)]`.

Thus the theorem signs only this combined response.  It does not establish a
separate sign for either term.

## 11. Auxiliary high-order closure — pass within its non-premise role

`HIGH_ORDER_CLOSURE.md` retains changing weights in the triangular `C^3`
state estimate and retains `L''u+2L'v` in the physical response.  Its affine
cancellations use the exact identities `LQ=0` and parameter derivatives of
fixed affine observables.  The resulting long-memory gate is explicitly
declared infeasible by literal enumeration and is not used in the `r=9`
theorem.  Nothing from that auxiliary route is needed to validate Sections
1--10 above.

## Contract ledger

| Unit | S1 result | Boundary |
|---|---|---|
| PR91 dependency | PASS | accepted analytic scope only; no PR91 finite sign |
| Complete KL increment | PASS | all current and future events retained |
| Future-law derivatives | PASS | Fisher and acceleration both retained |
| Predictor-jet forgetting | PASS | uniform in word, depth, and parameter |
| Differentiated KL bound | PASS | quadratic identity differentiated directly |
| True-rate `C^2` tail | PASS | uniformly summable value/first/second series |
| `r=9` entropy formula | PASS | correct cell/original-coordinate factors |
| Complex event cover | PASS | zero-free determinants and analytic logarithms |
| Chebyshev passage | PASS | explicit continuum error, not a grid inference |
| Certificate programs | PASS_STATIC | logical interface only |
| Saved node evidence | PENDING_S2 | not executed or independently rebound by S1 |
| Main positive interval | CONDITIONAL | follows after S2 accepts finite evidence |
| Boundary/gauge corollaries | CONDITIONAL | depend on the main interval theorem |
| Novelty and merge | NOT_REVIEWED | explicitly out of scope |

## Final S1 boundary

This is an analytic FIRST, not a numerical reproduction.  No author program
was run.  No finite PASS was treated as a theorem by itself.  The unconditional
PR136 theorem should be integrated only by combining this report with S2's
independent finite-evidence verdict.

