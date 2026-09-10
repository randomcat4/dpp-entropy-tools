# I05-30 addendum — a simultaneous double K / double complement endpoint on a full dense 3+3 chord

Status: **PROVED (author analytic proof / author exact finite certificate); PENDING_REVIEW.** Novelty is not assessed. This is a second continuation after the first I05-30 checkpoint and does not alter PR94 or PR95.

`RESULT.md` proved that arbitrary endpoint multiplicity has favorable complete Shannon curvature asymptotically. `ADDENDUM_TWO_SCALE_STABILITY.md` made that endpoint sign uniform under rank-two splitting. The purpose here is different: exhibit and close an entire maximal chord in which **both** spectral constraints are simultaneously multiple at the same endpoint, while the cross block is dense and outside PR94's exact grouped-channel shape.

## 1. Exact simultaneous-endpoint kernel

Put

`Q=(1/3) 11^T`, `P=I_3-Q`,

and define

`A=(1/5)P+(2/5)Q`,

`C=(4/5)P+(3/5)Q=I-A`,

`B=(2/5)P`.                                                   (1.1)

In the observed coordinate basis,

`A=[[4/15,1/15,1/15],`
`   [1/15,4/15,1/15],`
`   [1/15,1/15,4/15]]`,

`C=[[11/15,-1/15,-1/15],`
`   [-1/15,11/15,-1/15],`
`   [-1/15,-1/15,11/15]]`,

`B=[[4/15,-2/15,-2/15],`
`   [-2/15,4/15,-2/15],`
`   [-2/15,-2/15,4/15]]`.                                    (1.2)

Thus both marginal blocks are internally correlated, every cross entry is nonzero, and `rank B=2`.

Consider the genuine physical path

`K(t)=[[A,tB],[tB,C]]`.                                      (1.3)

Because `A,C,B` commute with P and Q, Schur complementation used **only for legality** gives

`C-s B A^-1 B=(4/5)(1-s)P+(3/5)Q`,                          (1.4)

`A-s B C^-1 B=(1/5)(1-s)P+(2/5)Q`.                          (1.5)

Equation (1.4) proves `K(t)>0` for `|t|<1` and `dim ker K(1)=2`. Equation (1.5) is the corresponding Schur complement for `I-K(t)` (the sign of the off-diagonal block is irrelevant quadratically), so `I-K(t)>0` for `|t|<1` and `dim ker(I-K(1))=2`. The same holds at `t=-1` by block-sign congruence.

Hence the maximal legal chord is exactly

`[-1,1]`,                                                    (1.6)

and at each endpoint both spectral constraints are simultaneously active with multiplicity two.

No entropy is evaluated after diagonalizing P or Q.

## 2. This object is not in PR94's exact three-from-two grouped-channel shape

PR94's actual-coordinate expansion from two base coordinates to three observed coordinates forces a proportional pair among the resulting three cross-block columns; applying the construction on the other side gives a proportional row pair.

For B in (1.2), every pair of columns and every pair of rows is nonproportional. For example the 2x2 minor of rows 0,1 in columns 0,1 is

`(4/15)^2-(-2/15)^2=4/75 !=0`,                               (2.1)

and permutation symmetry gives the same conclusion for each pair after choosing the corresponding two rows/columns.

Thus PR94's exact grouped-channel lift does not produce (1.3). This is only a noncoverage statement for that construction, not a theorem excluding every possible channel representation.

## 3. Exact complete-event compression into thirteen likelihood types

Let `mu=p_A tensor p_C` be the true decoupled complete law and `s=t^2`. Every one of the 64 complete events has

`p_E(t)=mu_E q_E(s)`, `q_E=1-a_E s+b_E s^2`.                (3.1)

Direct reconstruction from the defining Mobius law compresses the 64 events into the following thirteen exact likelihood types. `w` is the sum of the **original** mu weights in that type; no reweighting or event deletion is made.

| q(s) | w | multiplicity |
|---|---:|---:|
| `(16s^2+248s+361)/361` | `722/46875` | 6 |
| `(4s+1)(4s+361)/361` | `361/46875` | 3 |
| `(4s+1)^2` | `4/15625` | 1 |
| `(64s^2-223s+784)/784` | `6272/46875` | 6 |
| `(8s^2+84s+133)/133` | `4256/46875` | 12 |
| `(s+4)(16s+49)/196` | `3136/46875` | 3 |
| `(s+4)^2/16` | `2304/15625` | 1 |
| `(s-1)(8s-133)/133` | `2128/46875` | 6 |
| `(s-1)^2` | `192/15625` | 2 |
| `-(4s-19)(4s+1)/19` | `76/15625` | 6 |
| `-(s+4)(2s-7)/28` | `5376/15625` | 6 |
| `-(s-1)(8s+7)/7` | `224/15625` | 6 |
| `-(s-1)(s+19)/19` | `1824/15625` | 6 |

The weights sum to one. The checker independently reconstructs all 64 complete probabilities from inclusion principal minors and the defining Mobius sum at rational physical parameters, then matches (3.1).

At `s=1`, twenty complete atoms vanish: eighteen simple and two double. The double atoms are exactly the empty and full configurations, both with

`q=(1-s)^2`.                                                 (3.2)

Their individual acceleration logarithms therefore have the adverse double-root behavior identified in `RESULT.md` Section 3.

The true cardinality probabilities expose the compensating simple groups:

`P(|X|=0)=P(|X|=6)=96(1-s)^2/15625`,                        (3.3)

`P(|X|=1)=P(|X|=5)=16(1-s)(11s+64)/15625`.                 (3.4)

Thus the simultaneous endpoint contains both dangerous double atoms and two neighboring simple cardinality groups.

## 4. Full-curvature formula and a compact interval proof without sampling

For each likelihood type write

`v=a-2sb`, `z=(a-sb)(a-6sb)`,

`lambda(q)=log(q)/(q-1)`, `lambda(1)=1`.                     (4.1)

The exact complete normalized curvature is

`Gamma(s):=-H''(t)/t^2`
` =sum_E mu_E [4v_E^2/q_E+2 z_E lambda(q_E)]`,              (4.2)

with continuous endpoint at zero. Every Fisher and acceleration term is retained.

We use only the elementary scalar facts

`lambda(q)>0`,

`q>=1 => lambda(q)<=1`,

`0<q<=1 => lambda(q)<=1/q`,                                  (4.3)

plus two explicit logarithm comparisons for the double type. The second inequality is `log q<=q-1`; the third follows from the integral representation

`lambda(q)=integral_0^1 [1+theta(q-1)]^-1 dtheta`.           (4.4)

### 4.1 First compact segment: `0<=s<=9/10`

For nine of the thirteen likelihood types, exact quadratic endpoint/vertex checks give `z>=0` throughout this segment. Discarding their nonnegative logarithmic terms and bounding only their positive rational terms gives

`P_good:=sum_good 4 w min(v^2)/max(q) >19/20`.              (4.5)

Only four types can have `z<0`. Their exact negative minima and valid upper bounds for lambda on the respective negative-z regions are:

| q type | lower bound for z | lambda upper bound |
|---|---:|---:|
| `(1-s)^2` | `-187/50` | `5` |
| `-(s-1)(8s+7)/7` | `-25/1176` | `1` |
| `(64s^2-223s+784)/784` | `-506951/15366400` | `5/4` |
| `-(4s-19)(4s+1)/19` | `-20736/9025` | `1` |

For the first row `q>=1/100` and `lambda(1/100)<5`; for the second and fourth, `q>=1` on the actual negative-z region; for the third, `q>4/5` there and (4.3) applies. The weighted magnitude of all four possible negative logarithmic contributions is strictly less than `1/2`:

`sum_bad 2 w |z_-| lambda_+ <1/2`.                           (4.6)

Therefore

`Gamma(s)>19/20-1/2=9/20>1/10`                              (4.7)

on the whole first segment.

### 4.2 Second compact segment: `9/10<=s<=99/100`

Now ten of the thirteen types have `z>=0`. Their rational terms alone give

`P_good>8`.                                                  (4.8)

The three remaining bad types are

| q type | lower bound for z | lambda upper bound |
|---|---:|---:|
| `(1-s)^2` | `-19897/5000` | `10` |
| `(64s^2-223s+784)/784` | `-15680639/384160000` | `4/3` |
| `-(4s-19)(4s+1)/19` | `-808704/225625` | `1` |

Here `(1-s)^2>=10^-4`, the second q is `>3/4`, and the third is `>1`. The exact weighted negative budget is `<11/10`. Hence

`Gamma(s)>8-11/10=69/10>1/10`.                              (4.9)

All minima/maxima in (4.5)-(4.9) are extrema of explicit quadratics on rational intervals; no temporal grid is used.

## 5. Final simultaneous endpoint band: both adjacent cardinalities contribute Fisher

Let

`delta=1-s`, `0<delta<=1/100`.                               (5.1)

From (3.4), write

`R(s)=P(|X|=1)=P(|X|=5)=16 delta(11s+64)/15625`.             (5.2)

For either group, weighted Cauchy on the true complete events gives

`sum_(|E|=1) (p_E')^2/p_E >=(R')^2/R`,

and identically for `|E|=5`. Since `s>=9/10`, direct differentiation of (5.2) gives the two-group bound

`F_1+F_5 >1/(2 delta)`.                                      (5.3)

Every other Fisher term, including the two double atoms, remains nonnegative and is retained by discarding only after (5.3).

The complete-event table also gives, on all `0<=s<=1`,

`q_E(s)>=(1-s)^2=delta^2`,                                  (5.4)

and

`min_E mu_E=4/15625>1/4000`.                                (5.5)

Thus every one of the 64 probabilities satisfies

`p_E>=delta^2/4000`,

`|log p_E|<=log 4000+2log(1/delta)`.                         (5.6)

The exact coefficients give

`sum_E |p_E''(t)|=sum_E mu_E|-2a_E+12s b_E|`
` <=2E_mu|a|+12E_mu|b|=101408/46875<11/5`.                  (5.7)

Therefore the full exact curvature obeys

`-H''(t)`
` >1/(2delta)-(11/5)[log4000+2log(1/delta)].                 (5.8)

For `delta<=1/100`, the right side is decreasing as delta increases because

`d/delta =-1/(2delta^2)+(22/5)/delta<0`.                     (5.9)

At `delta=1/100`, the rational logarithm comparisons

`log4000<9`, `log100<14/3`                                  (5.10)

give

`-H''(t)>50-(11/5)(55/3)=29/3>1/10`.                        (5.11)

Thus the two adverse double atoms are not hidden: their logarithmic acceleration loss is included in (5.6)-(5.8), while the **two true simple cardinality groups** supply the dominating Fisher term.

## 6. Whole maximal-chord theorem

Combining (4.7), (4.9), and (5.11), for every `0<|t|<1`,

`H''(t)<=-(1/10)t^2`.                                       (6.1)

At `t=0`, analyticity gives `H''(0)=0`. Consequently

`H(t)+t^4/120`                                               (6.2)

is concave on the full closed maximal legal chord `[-1,1]`, and H itself is strictly Jensen-concave for distinct points of that chord.

This is an explicit simultaneous-multiplicity example: at each endpoint both K and I-K have two-dimensional kernels, the empty and full complete events are both double zeros with adverse logarithmic acceleration divergence, and the full entropy remains quantitatively concave because the neighboring complete cardinality groups carry the stronger Fisher singularity.

## 7. Scope

This addendum does not prove general dense correlated rank-two whole-chord concavity. It proves a substantially different exact family member from the PR95 simple-endpoint fixture and directly exercises the simultaneous-activity case of the new endpoint mechanism.

Together with `ADDENDUM_TWO_SCALE_STABILITY.md`, it also yields a relative-open rank-two neighborhood of this simultaneous seed whose members retain a fixed fraction of (6.1) on their **own** maximal chords, even when the fourfold spectral boundary splits into one-sided or simple endpoint clusters. The neighborhood radius is existential; no new tiny numerical ball is presented as the main result.
