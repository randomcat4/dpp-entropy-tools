# Independent FIRST report for PR112 `explicit_rate_interval.md`

## Verdict

**ACCEPTED_SCOPED** for immutable blob
`b8aab2981230b61d399d9a9411ee8547f8593958` at PR112 head
`2ea07741114aa7cd20210dfc84becda378381e7b`.

The submitted complex complete-event argument establishes a normally
convergent analytic continuation of the true entropy rate, supplies a uniform
third-derivative bound, and propagates the accepted PR77 center curvature to
the exact interval of half-width `2^(-27)`.

## 1. Exact dependency seal — pass

The only external mathematical inputs used are the accepted PR77 facts at its
exact head:

- `h''(1)<-1/1000` for the same complete-occupation entropy rate and the same
  physical affine parameter `t`;
- on `|z-1|<=1/8`, the predictor comparison bound

  `|q_R(z)-q_r(z)| <= C^3 A^2 B^2 rho^(2r-6)`,

  with

  `rho=2/3`, `C=288/85`, `A=11/64`, `B=49/192`.

The four PR77 comparison residuals at this center are respectively
`85/288`, `385/3456`, `25/5184`, and the far residual coefficient
`25/2304`; all are strictly positive.  No PR91 statement enters the proof.

## 2. Complex complete-event predictor disk — pass

For `|z-1|<=1/8`, one has `|z|<=9/8`.  Every signed complete-event matrix has
diagonal modulus `1/2`, first off-diagonal modulus at most `9/128`, and second
off-diagonal modulus `1/8`.  Its row diagonal-dominance margin is therefore

`1/2-2(9/128)-2(1/8)=7/64`.

The complex matrix is invertible for every complete word and every length,
with

`||M(z)^(-1)||_infinity<=64/7`.

The predictor vector has `l^1` norm at most `25/128` and `l^infinity` norm at
most `1/8`.  Consequently

`|q_r(z)-1/2|`

`<= (25/128)(64/7)(1/8)=25/112<1/4`.

The truncations for conditioning lengths zero and one obey the same bound.
Thus both `q_r` and `1-q_r` are nonzero and remain in the right-half-plane
disk centered at `1/2` with radius `1/4`.  The positive real logarithm branches
therefore extend consistently and analytically over the complex parameter
disk.

## 3. Complex complete-event total variation — pass

If `|w-1/2|<=1/4`, ellipse geometry gives

`|w|+|1-w|<=sqrt(5)/2<9/8=:sigma`.

Factoring every complete word one conditional branch at a time and summing
both branches at every step gives

`sum_(words omega of length n)|p_z(omega)|<=sigma^n`.

This is a complex total-variation estimate.  It does not assert positivity of
complex event weights and retains all occupied and vacant events.

## 4. Normally convergent entropy series — pass

Let `F(w)=w log w+(1-w)log(1-w)`.  On the convex predictor disk,

`|F''(w)|=|1/(w(1-w))|<=16/3<8`.

The analytic Bregman formula therefore gives

`|d(a||b)|<=4|a-b|^2`.

The exact PR77 constants satisfy, without decimal approximation,

`C<7/2`, `A<7/40`, `B<13/50`,

and hence

`C^3 A^2 B^2`

`<2840383/32000000<1/10`.

Writing `h_r` for the full conditional entropy
`H(X_0|X_1,...,X_r)` and `d_r=h_r-h_(r+1)`, the complete-event conditional
relative-entropy identity gives

`|d_r(z)| <= (1/25)sigma^(r+1)rho^(4r-12)`, `r>=3`.

The geometric ratio is exactly

`sigma rho^4=(9/8)(2/3)^4=2/9`.

Thus

`h(z)=h_3(z)-sum_(r=3)^infinity d_r(z)`

converges normally and is analytic.  On the real slice, telescoping and the
standard monotone convergence of finite-alphabet conditional entropies show
that this is the true stationary Shannon entropy rate per original
coordinate.  No normalized finite-window Hessian is substituted for it.

## 5. Uniform analytic bound — pass

On the predictor disk, the chosen logarithm branches satisfy
`|log w|,|log(1-w)|<=log 4<3/2`.  Together with the ellipse bound, this gives

`|F(w)|<=27/16`

and therefore

`|h_3(z)|<=(9/8)^3(27/16)=19683/8192`.

The normally convergent tail is bounded by

`(1/25)(9/8)^4 sum_(j=0)^infinity(2/9)^j`

`=59049/716800`.

Hence

`|h(z)|<=3562623/1433600<5/2`.

The last strict inequality has the exact numerator gap `21377`, so no rounded
arithmetic or sampled residual is hidden here.

## 6. Cauchy third-derivative bound — pass

For every real `|t-1|<=1/16`, the radius-`1/16` circle around `t` lies inside
`|z-1|<=1/8`.  Cauchy's formula and the preceding uniform bound give

`|h'''(t)| <= 3!(5/2)16^3 = 61440`.

The complete-event matrices remain strictly diagonally dominant on the closed
larger disk, so the analytic functions exist on an open neighborhood of every
contour used here.

## 7. Exact interval arithmetic and curvature sign — pass

For `|t-1|<=2^(-27)`, integration of the actual third derivative yields

`h''(t)<-1/1000+61440/2^27`

`=-1/1000+15/32768`.

Because `15*2000=30000<32768`, the right side is strictly below
`-1/2000`.  This proves the claimed sign on exactly

`[1-2^(-27),1+2^(-27)]`.

Adding `t^2/4000` changes the second derivative by `1/2000`; the resulting
function is concave.  Expanding its Jensen inequality gives exactly the stated
gap `lambda(1-lambda)(u-v)^2/4000`.

## 8. Parameter and normalization audit — pass

The complex variable `z` is the direct analytic continuation of the physical
parameter `t`.  In the Toeplitz kernel, the nearest-neighbor coefficient is
`t/16`; no auxiliary rescaling or nonlinear parameter replaces it.  The
imported center derivative, the Cauchy derivative, and the final interval are
therefore derivatives in the same affine correlation-kernel direction.

Every conditional entropy sums the complete occupied/vacant event law, and
`h_r=H_(r+1)-H_r` is normalized per original lattice site.  The limiting
object is the true entropy rate with no parity, block-size, or doubled-layer
factor.

## Contract ledger

| Unit | Result | Reason |
|---|---|---|
| PR77 dependency seal | PASS | exact center theorem and exact comparison constants only |
| Complete-event predictor disk | PASS | `7/64` diagonal margin and `25/112` predictor radius |
| Complex event total variation | PASS | full two-branch factorization, ratio `sigma=9/8` |
| Entropy-series convergence | PASS | analytic Bregman bound and net ratio `2/9` |
| True-rate identification | PASS | conditional-entropy telescoping on the real slice |
| Uniform analytic modulus | PASS | exact `h_3` and tail bounds, total below `5/2` |
| Cauchy derivative | PASS | radius `1/16`, third derivative at most `61440` |
| Exact half-width | PASS | `61440/2^27=15/32768<1/2000` |
| Physical direction | PASS | the same affine `t` is used throughout |
| Complete-law normalization | PASS | all events, per original coordinate |

## Evidence boundary

No computation was run.  The prior PR77 theorem is imported as an already
accepted exact result; its finite certificate PASS is not independently
replayed or promoted here.  No S3 conclusion was read or used.  This review
does not inspect or accept PR112 as a package and does not assess novelty.

In particular, it excludes the withdrawn `[49/40,51/40]` interval, the
lifted-cone files, and every assertion on `[1/2,3/2]`.

