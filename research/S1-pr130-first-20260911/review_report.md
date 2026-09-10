# Independent FIRST report for PR130

## Verdict

**ACCEPTED_SCOPED** at exact author head
`4cae5c29effcf01b1fadc7452780b73a58ec94e7`.

The submitted proof establishes a volume-uniform quartic upper bound for the
true complete-configuration entropy deficit and, using only the accepted
matching floor, its exact `Theta(t^4)` scale.  No entropy-rate derivative is
constructed or used.

## 1. Parity block structure and atomwise evenness — pass

Half-period evenness of `c` eliminates odd Fourier modes, while
half-period oddness of `g` eliminates even modes.  After reordering a finite
interval into even and odd coordinates, every complete-event matrix at the
center is block diagonal,

`M_x(0)=diag(A_u,C_v)`,

and the physical perturbation is purely cross-parity,

`G=[[0,B],[B*,0]]`.

The strict symbol margin gives the signed complete-event coercivity bounds

`||A_u^(-1)||,||C_v^(-1)||<=delta^(-1)`

uniformly in the complete word and volume.  Conjugation by
`diag(I_even,-I_odd)` sends `t` to `-t` and commutes with every vacancy mask.
Therefore every complete atom satisfies `p_x(t)=p_x(-t)`, and in particular
`p_x'(0)=0`.  This is a pointwise complete-law statement, not merely entropy
evenness.

## 2. Exact `s=t^2` complete likelihood — pass

Schur complementation gives, for every occupied/vacant word,

`p_s(x)/p_0(x)=det(I-sQ_x)`,

`Q_x=C_v^(-1)B* A_u^(-1)B`.

The determinant signs from vacant events cancel in the ratio.  The uniform
bound

`||Q_x||<=C0:=delta^(-2)||g||_infinity^2`

is independent of the word and volume.  Normalization of the exact complete
family gives at the center

`E_0 Tr Q=0`,

`E_0(Tr Q)^2=E_0 Tr(Q^2)`.

Thus the full finite-law Fisher information in the parameter `s` is exactly
`E_0 Tr(Q^2)`.  No event or acceleration contribution is removed.

## 3. Finite quartic coefficient and nonnormal trace bound — pass

For an arbitrary, possibly nonnormal matrix,

`|Tr(Q^2)|<=||Q||_HS^2`.

Moreover,

`||Q||_HS<=delta^(-2)||B||_op||B||_HS`.

The cross-parity block is a compression of `T(g)`, so

`||B||_op<=||g||_infinity`,

`||B||_HS^2<=|Lambda|||g||_2^2`.

Consequently the finite `s`-Fisher coefficient is extensive with a constant
uniform in volume.  This validates the initial checkpoint's finite quartic
coefficient statement, while not relying on its nonuniform Taylor remainder
for the rate theorem.

## 4. Rebase at the current physical `s` — pass

For real `s>=0` with `sC0<=1/4`, define

`A_s=Q(I-sQ)^(-1)`.

Then

`I+sA_s=(I-sQ)^(-1)`

and therefore, atom by atom,

`p_0/p_s=det(I+sA_s)`.

Differentiating the original normalized family at the current parameter gives

`E_s Tr A_s=0`,

where the expectation is under the actual current complete law `P_s`, not the
reference law `P_0`.  This current-law cancellation is the load-bearing step
that removes the trace-length-one term uniformly in volume.

## 5. Nonnormal trace-log series and constants — pass

The resolvent bounds are

`||A_s||<=(4/3)C0`,

`||A_s||_HS<=(4/3)||Q||_HS`,

`s||A_s||<=1/3`.

Thus the operator-norm logarithm series converges without assuming normality,
and the desired forward KL is exactly

`D(P_s||P_0)`

`=sum_(m>=2)(-1)^m s^m E_s Tr(A_s^m)/m`.

For every `m>=2`, Hilbert--Schmidt Cauchy--Schwarz and submultiplicativity give

`|Tr(A^m)|<=||A||_op^(m-2)||A||_HS^2`.

The resulting geometric ratio is at most `1/3`.  Since

`sum_(m>=2)r^(m-2)/m<=1/[2(1-r)]<=3/4`,

the factors `(16/9)(3/4)=4/3` yield exactly

`D(P_s||P_0)/|Lambda|`

`<= (4/3)delta^(-4)||g||_infinity^2||g||_2^2 s^2`.

This is an equality-based reorganization of the full forward KL before the
estimate; it is not a sign assertion about isolated Fisher or acceleration
summands.

## 6. Entropy deficit and thermodynamic limit — pass

The even and odd finite-coordinate marginals do not depend on `t`; at the
center their joint law is their product.  Hence for every finite interval

`D(P_(Lambda,t)||P_(Lambda,0))`

`=H_Lambda(c)-H_Lambda(c+t g)`.

The right side of the finite bound is uniform in `Lambda`.  For each fixed
small legal `t`, ordinary stationary finite-alphabet entropy-rate convergence
therefore gives

`0<=h(c)-h(c+t g)`

`<= (4/3)delta^(-4)||g||_infinity^2||g||_2^2t^4`.

No derivative is passed through the thermodynamic limit.

## 7. Matching floor and exact quartic order — pass

For nonzero half-period-odd `g in L^infinity`, Parseval supplies a nonzero odd
Fourier coefficient.  The only imported theorem is the accepted
regularity-free matching bound

`h(c)-h(c+t g)`

`>=(1/2)d_Ber(mu^2-|g_hat(k)|^2t^2 || mu^2)`.

Because `delta<=mu<=1-delta`, scalar Taylor expansion at the strict Bernoulli
parameter gives

`(1/2)d_Ber(mu^2-|g_hat(k)|^2t^2 || mu^2)`

`=|g_hat(k)|^4t^4/[4mu^2(1-mu^2)]+O(t^6)`.

Its coefficient is strictly positive.  Combining it with the uniform upper
bound proves `Theta(t^4)`.  No response regularity from PR53 or PR117 is used.

## 8. Maximal-direction and Peano corollaries — pass

If a measurable real direction admits a two-sided legal interval at a strict
center, the two inequalities for `c+tau g` and `c-tau g` imply an essential
bound on `g` (indeed the submitted `(1-delta)/tau` bound is valid, though not
sharp).  Hence the quartic theorem covers every measurable half-period-odd
direction with such an interval.

Atomwise parity conjugacy gives `h(c+t g)=h(c-t g)`.  The `O(t^4)` value bound
then implies

`[h(c+t g)+h(c-t g)-2h(c)]/t^2 ->0`.

The matching floor and upper bound also trap the quartic quotient between
positive finite constants.  Neither fact asserts that an ordinary second or
fourth derivative exists.

## Contract ledger

| Unit | Result | Reason |
|---|---|---|
| Complete atom evenness | PASS | parity conjugacy commutes with vacancy masks |
| Complete-event coercivity | PASS | strict center margin, uniform in word and volume |
| Exact `s` likelihood | PASS | block determinant ratio with correct orientation |
| Center normalization identities | PASS | full `P_0` law and determinant coefficients |
| Current-law rebasing | PASS | exact `E_s Tr A_s=0` under `P_s` |
| Nonnormal logarithm | PASS | operator-norm series with radius at most `1/3` |
| Schatten trace bound | PASS | no diagonalization or normality assumption |
| Hilbert--Schmidt extensivity | PASS | Toeplitz and parity compressions only decrease norm |
| Finite forward KL bound | PASS | all complete atoms and correct `4/3` constant |
| Thermodynamic passage | PASS | value limit with volume-uniform bound |
| Matching floor | PASS | imported floor only, not imported response regularity |
| `Theta(t^4)` | PASS | positive quartic lower coefficient plus uniform upper bound |
| Peano/maximal-direction corollaries | PASS | value statements only |
| `C^2/C^4` or concavity | NOT_CLAIMED | cannot be inferred from the value bound |

## Evidence boundary

No computation was used.  This is not a novelty review.  The verdict is bound
to the exact four author blobs and does not merge PR130.  It does not establish
ordinary `C^2/C^4` entropy-rate response, off-center curvature, punctured-
neighborhood concavity, whole-interval concavity, or a general real-kernel
theorem.

