# I05-31 result — a dense correlated rank-two whole chord with aggregate acceleration positivity

Status: **AUTHOR PROOF / PENDING_REVIEW; novelty NOT_ASSESSED.** This is a direct proof for a new exact physical-coordinate chord. It does not use PR102's local endpoint-stability neighborhood, does not inherit any PR94/95/97/102 review, and does not rerun an earlier computation.

All entropy is complete-configuration Shannon entropy with natural logarithms. The path is genuinely affine in the observed kernel and all 64 events, Fisher terms and acceleration terms are retained.

## 1. Exact candidate and maximal legal chord

Put

`Q=(1/3) 11^T`, `P=I_3-Q`,

and define

`A=(1/10)P+(1/3)Q`,

`C=(9/10)P+(2/3)Q=I-A`,

`B=(3/10)P`.

Thus in the observed coordinates

`B=[[1/5,-1/10,-1/10],[-1/10,1/5,-1/10],[-1/10,-1/10,1/5]]`,

so `rank(B)=2`, every cross entry is nonzero, and both marginal blocks are internally correlated. Consider

`K(t)=[[A,tB],[tB,C]]`.                                      (1.1)

On the two-dimensional `P` subspace, each logical mode has the 2x2 block

`[[1/10,3t/10],[3t/10,9/10]]`,

whose trace is one and determinant is `9(1-t^2)/100`. On the `Q` subspace the two uncoupled eigenvalues are `1/3,2/3`. Hence, using spectral coordinates only to establish legality,

`0<K(t)<I` exactly for `|t|<1`,

and the maximal legal chord is `[-1,1]`. At either endpoint

`dim ker K = dim ker(I-K)=2`.                                (1.2)

No entropy is evaluated after this diagonalization.

This cross block is outside PR94's exact three-from-two grouped-channel shape: every pair of rows and every pair of columns is nonproportional. For example the 2x2 minor on rows/columns 0,1 is

`(1/5)^2-(-1/10)^2=3/100 !=0`,

and permutation symmetry supplies the corresponding witnesses for the other pairs.

## 2. Exact complete-event likelihood table

Let `mu=p_A tensor p_C` be the true decoupled complete law and put `s=t^2`. Direct signed-determinant reconstruction of every complete event gives

`p_E(t)=mu_E q_E(s)`, `q_E=1-a_E s+b_E s^2`.

Equal `(q,a,b)` types combine to the following eleven rows. The listed weight is the sum of the original `mu_E` over that type; no event is deleted or reweighted.

| multiplicity | weight | a | b | q(s) |
|---:|---:|---:|---:|---|
| 12 | `13/375` | `-17/13` | `0` | `(17s+13)/13` |
| 6 | `507/5000` | `302/1521` | `9/169` | `(81s^2-302s+1521)/1521` |
| 1 | `1/90000` | `-18` | `81` | `(9s+1)^2` |
| 6 | `2/675` | `-9/4` | `0` | `(9s+4)/4` |
| 2 | `9/2500` | `2` | `1` | `(1-s)^2` |
| 3 | `507/10000` | `-898/1521` | `9/169` | `(s+9)(81s+169)/1521` |
| 1 | `729/2500` | `-2/9` | `1/81` | `(s+9)^2/81` |
| 12 | `67/750` | `1` | `0` | `1-s` |
| 6 | `13/5000` | `-14/13` | `-27/13` | `(1-s)(27s+13)/13` |
| 6 | `1053/2500` | `14/117` | `-1/39` | `(s+9)(13-3s)/117` |
| 9 | `13/6750` | `-9` | `0` | `9s+1` |

The weights sum to one and the exact normalization cancellations are

`E_mu a=E_mu b=0`.                                           (2.1)

A fresh exact checker in `code/verify_exchangeable.py` reconstructs all 64 signed determinants before grouping and verifies the table and the rational inequalities below. That checker is author evidence, not independent review.

## 3. Full normalized curvature and the three adverse types

Set

`v=a-2sb`, `z=(a-sb)(a-6sb)`,

`lambda(q)=log(q)/(q-1)`, `lambda(1)=1`.

For `0<s<1`, the exact complete Shannon curvature is

`Gamma(s):=-H''(t)/t^2`
` =sum_E mu_E [4v_E^2/q_E + 2 z_E lambda(q_E)].              (3.1)

The first part is the full Fisher contribution. The second is the full affine-acceleration contribution after the exact cancellations (2.1). Since `lambda(q)>0`, the sign of an individual acceleration row is the sign of `z`.

Nine of the eleven grouped rows have `z>=0` on the whole interval, except that after merging identical types only the following three can be adverse:

1. `q_0=(1-s)^2`, weight `w_0=9/2500`, `a=2,b=1`;
2. `q_4=(1-s)(27s+13)/13`, weight `w_4=13/5000`, `a=-14/13,b=-27/13`;
3. `q_7=(81s^2-302s+1521)/1521`, weight `w_7=507/5000`, `a=302/1521,b=9/169`.

All other rows have either `b=0` or `ab<=0`, hence `(a-sb)(a-6sb)>=0` for every `s>=0`.

## 4. A positive acceleration reserve dominates all three adverse rows

Write `delta=1-s`. The merged `q=1-s`, `a=1,b=0` row has total weight

`W=67/750`,

and contributes exactly

`2W lambda(delta)=67/375 lambda(delta)`                       (4.1)

to the normalized acceleration.

We compare each adverse row to this same positive reserve.

### 4.1 Double endpoint row

For `q_0=delta^2`,

`lambda(delta^2)=2 lambda(delta)/(1+delta) <=2 lambda(delta)`. (4.2)

On `0<=s<=1`, whenever `z_0<0`,

`-z_0=-(2-s)(2-6s)<=4`.                                      (4.3)

Therefore its entire possible negative contribution is bounded below by

`-16 w_0 lambda(delta)=-(36/625) lambda(delta)`.             (4.4)

### 4.2 The `(1-s)(27s+13)/13` row

Here

`q_4=delta(27s+13)/13 >=delta`,

so monotonicity of `lambda` gives `lambda(q_4)<=lambda(delta)`. Moreover

`z_4=2(27s-14)(81s-7)/169`,

whose negative minimum is attained at `s=49/162` and equals

`-1225/1014`.                                                (4.5)

Thus this row contributes at worst

`-(49/7800) lambda(delta)`.                                  (4.6)

### 4.3 The remaining quadratic row

For

`q_7=1-(302/1521)s+(9/169)s^2`,

`q_7-delta=s(1219/1521)+(9/169)s^2 >=0`,

hence again `lambda(q_7)<=lambda(delta)`. Its adverse region begins at `s=151/243`; there

`z_7=2(81s-302)(243s-151)/2313441`.

The vertex lies beyond `s=1`, so on the legal interval

`z_7 >= z_7(1)=-3128/177957`.                                (4.7)

Therefore its possible negative contribution is at worst

`-(782/219375) lambda(delta)`.                               (4.8)

Combining (4.1), (4.4), (4.6), and (4.8), and simply discarding every other nonnegative acceleration row, yields the pointwise full-acceleration bound

`sum_E 2 mu_E z_E lambda(q_E)`
` >= [67/375-36/625-49/7800-782/219375] lambda(delta)`
` = (195191/1755000) lambda(delta) >0`                        (4.9)

for every `0<s<1`.

This is the key mechanism: individual complete-event acceleration terms are genuinely adverse in a strong middle and at the simultaneous double endpoint, but the **aggregate complete acceleration is strictly favorable everywhere**. No Fisher term is used to prove (4.9).

## 5. Fisher gives a quantitative whole-chord margin

Choose a corresponding left/right observed coordinate pair, say coordinates 0 and 3. Its joint occupancy bit has probability

`r(t)=P(X_0=X_3=1)=A_00 C_00-t^2 B_00^2`,

with `B_00=1/5`, hence

`r'(t)=-2t/25`.                                               (5.1)

Data processing for Fisher information under the binary statistic `1_{X_0=X_3=1}` gives

`F_complete(t) >= (r'(t))^2/[r(t)(1-r(t))] >=4(r'(t))^2`
` =16 t^2/625`.                                              (5.2)

Combining (4.9) with (3.1) therefore proves the full true affine chord bound

`Gamma(s) >=16/625`,

or equivalently

`H''(t) <= -(16/625)t^2 <0`, `0<|t|<1`.                     (5.3)

At `t=0`, the exact analytic rank-two expansion gives `H''(0)=0`. By continuity of `x log x`, the conclusion extends to the closed legal chord in Jensen form. In particular

`H(t)+(4/1875)t^4` is concave on `[-1,1]`.                    (5.4)

This is a complete-configuration Shannon theorem, not a finite-sample sign check.

## 6. Scope and what this does not prove

- This is one exact symmetry-defined chord, not the unrestricted dense correlated rank-two theorem.
- The proof is direct across the whole chord; it does not infer the middle from PR102 endpoint asymptotics or an unspecified neighborhood of a prior sample.
- The object shares the broad simultaneous-endpoint phenomenon with PR102 but uses different exact parameters and a different all-middle mechanism: aggregate acceleration positivity plus a physical pair-statistic Fisher margin.
- Failure of the eventwise six-slope cone from `CHECKPOINT.md` is explicit here: the `(1-s)^2` row becomes adverse for `s>1/3`. Thus that cone is not the explanation for this theorem.
- No entropy-rate conclusion is claimed.

The natural next analytic question is whether the same reserve comparison survives for a nontrivial interval in the `Q`-mode marginal parameter in

`A=(1/10)P+beta Q`, `C=I-A`, `B=(3/10)P`,

which would turn this exact chord into a genuine one-parameter whole-chord family rather than a single symmetry point.