# Moving rank-one endpoints are midpoint-safe

**Status: PROVED (author proof; independent review pending).**

All entropies below are the Shannon entropy of the complete DPP atom law

\[
p_K(S)=\sum_{T\supseteq S}(-1)^{|T|-|S|}\det K_T,
\qquad H(K)=-\sum_{S\subseteq[n]}p_K(S)\log p_K(S).
\]

No inclusion probability is substituted for an exact atom.  The midpoint is
the actual arithmetic midpoint in `K`-space.

## Theorem 1: arbitrary moving rank-one chord

Let `n>=2`, let `x,y in R^n` be unit vectors, and let `0<a,b<1`.  Put

\[
K_-=a xx^{\mathsf T},\qquad K_+=b yy^{\mathsf T},\qquad
K_0={K_-+K_+\over2}.
\]

Then all three matrices are legal real DPP kernels and

\[
H(K_0)\ge {H(K_-)+H(K_+)\over2}.                 \tag{1}
\]

Equality holds if and only if `K_-=K_+`.  Thus every nonconstant chord is
strictly midpoint-concave, even though both the physical rank-one direction
and its nonzero eigenvalue may change between endpoints.

### Step 1: exact endpoint laws

A rank-one kernel `K=a xx^T` has the complete atom law

\[
p_K(\varnothing)=1-a,\qquad p_K(\{i\})=a x_i^2,
\qquad p_K(S)=0\quad(|S|\ge2).                    \tag{2}
\]

This follows directly by expanding
`det(I-K+ZK)` or by finite Mobius inversion.  Let

\[
q={p_{K_-}+p_{K_+}\over2}.
\]

Writing `s=tr K_0=(a+b)/2`, (2) gives

\[
q(\varnothing)=1-s,\qquad q(\{i\})=(K_0)_{ii},
\qquad q(S)=0\quad(|S|\ge2).                      \tag{3}
\]

Shannon entropy is concave on the probability simplex, hence

\[
H(q)\ge {H(K_-)+H(K_+)\over2}.                   \tag{4}
\]

The remaining point is that replacing the mixture law `q` by the DPP law of
the matrix midpoint cannot lower entropy.

### Step 2: the complete midpoint law

Let the nonzero spectral decomposition of `K_0` be

\[
K_0=\alpha uu^{\mathsf T}+\beta ww^{\mathsf T},
\qquad u^{\mathsf T}w=0,
\]

where `0<=alpha,beta<1`.  Set

\[
s=\alpha+\beta,\qquad m=\alpha\beta,
\qquad b_{ij}=(u_iw_j-u_jw_i)^2.
\]

Cauchy--Binet gives

\[
\sum_{i<j}b_{ij}=1,
\qquad \sum_{j\ne i}b_{ij}=u_i^2+w_i^2=:c_i.      \tag{5}
\]

A direct expansion of the complete generating polynomial gives all midpoint
atoms:

\[
\begin{aligned}
p_{K_0}(\varnothing)&=(1-\alpha)(1-\beta)=1-s+m,\\
p_{K_0}(\{i\})&=(\alpha-m)u_i^2+(\beta-m)w_i^2,\\
p_{K_0}(\{i,j\})&=m b_{ij},\\
p_{K_0}(S)&=0\quad(|S|\ge3).
\end{aligned}                                      \tag{6}
\]

These are the complete event probabilities.  In particular, the rank-two
midpoint opens genuine pair events that are absent at both rank-one
endpoints.

### Step 3: an entropy-increasing mass-transfer bridge

For `0<=r<=m`, define a probability law supported on sets of size at most two:

\[
\begin{aligned}
p_r(\varnothing)&=1-s+r,\\
p_r(\{i\})&=\alpha u_i^2+\beta w_i^2-r c_i
            =(\alpha-r)u_i^2+(\beta-r)w_i^2,\\
p_r(\{i,j\})&=r b_{ij}.
\end{aligned}                                      \tag{7}
\]

Because `m=alpha beta<=min(alpha,beta)`, every term is nonnegative.  Equations
(3), (5), and (6) show

\[
p_0=q,\qquad p_m=p_{K_0}.                         \tag{8}
\]

For `0<r<m`, differentiating the full entropy and using (5) yields

\[
{d\over dr}H(p_r)
 =\sum_{i<j}b_{ij}
   \log {p_r(\{i\})p_r(\{j\})
          \over p_r(\varnothing)\,r b_{ij}},        \tag{9}
\]

where pairs with `b_ij=0` contribute zero.  Put `A_r=alpha-r` and
`B_r=beta-r`.  Lagrange's identity gives, for every pair,

\[
\begin{aligned}
p_r(\{i\})p_r(\{j\})
 &=\bigl(A_r u_i u_j+B_r w_iw_j\bigr)^2
   +A_rB_r b_{ij},\\
A_rB_r-rp_r(\varnothing)
 &=(\alpha-r)(\beta-r)-r(1-s+r)=m-r.               \tag{10}
\end{aligned}
\]

Consequently, whenever `b_ij>0`,

\[
p_r(\{i\})p_r(\{j\})
 >p_r(\varnothing)\,r b_{ij}
 \quad(0<r<m).                                      \tag{11}
\]

Since the `b_ij` sum to one, (9) is strictly positive throughout `(0,m)`.
Entropy is continuous at both endpoints, so

\[
H(K_0)=H(p_m)>H(p_0)=H(q)\qquad(m>0).               \tag{12}
\]

If `m=0`, the two rank-one ranges are collinear.  Then `p_{K_0}=q`; (4) is
strict unless the two endpoint laws coincide.  In the collinear case they
coincide exactly when `a=b`, which is exactly `K_-=K_+`.  Combining this with
(4) and (12) proves Theorem 1.

## Theorem 2: explicit strict interior lifts

For `0<epsilon<1/2`, define

\[
K_\sigma^{(\epsilon)}
 =\epsilon I+(1-2\epsilon)K_\sigma,
\qquad \sigma\in\{-,0,+\}.                         \tag{13}
\]

Then

\[
K_0^{(\epsilon)}={K_-^{(\epsilon)}+K_+^{(\epsilon)}\over2},
\qquad
\epsilon I\preceq K_\sigma^{(\epsilon)}
              \preceq(1-\epsilon)I.                \tag{14}
\]

Thus this is a genuine affine chord of strict real kernels, not a curved
moving-frame path.

Let

\[
G=H(K_0)-{H(K_-)+H(K_+)\over2}.
\]

For distinct endpoints, Theorem 1 gives `G>0`.  Define

\[
\delta_n(\epsilon)=1-(1-\epsilon)^n,
\]

and, whenever `delta_n(epsilon)<=1-2^{-n}`,

\[
\omega_n(\epsilon)
 =h_2(\delta_n(\epsilon))
  +\delta_n(\epsilon)\log(2^n-1),                  \tag{15}
\]

where `h_2(t)=-t log t-(1-t)log(1-t)`.  Every `epsilon` satisfying

\[
2\omega_n(\epsilon)<G                              \tag{16}
\]

obeys the strict certified bound

\[
H(K_0^{(\epsilon)})
 -{H(K_-^{(\epsilon)})+H(K_+^{(\epsilon)})\over2}
 \ge G-2\omega_n(\epsilon)>0.                      \tag{17}
\]

### Proof of the lift identity and error bound

Independently flip every occupancy bit of a DPP configuration with probability
`epsilon`.  If `Z=diag(z_i)`, put

\[
A_\epsilon=(1-\epsilon)I+\epsilon Z,
\qquad B_\epsilon=\epsilon I+(1-\epsilon)Z.
\]

Using the exact probability generating polynomial,

\[
\begin{aligned}
G_{\rm flip}(z)
 &=\det\bigl(A_\epsilon(I-K)+B_\epsilon K\bigr)\\
 &=\det\bigl(I-K^{(\epsilon)}+ZK^{(\epsilon)}\bigr),
\end{aligned}                                      \tag{18}
\]

with `K^(epsilon)=epsilon I+(1-2epsilon)K`.  Hence the flipped law is exactly
the DPP law of (13).

Under the obvious coupling, the original and flipped configurations differ
with probability at most `delta_n(epsilon)`.  Their total variation distance
is therefore at most this number.  The sharp finite-alphabet
Fannes--Audenaert inequality on an alphabet of size `2^n` gives

\[
|H(K^{(\epsilon)})-H(K)|\le\omega_n(\epsilon).      \tag{19}
\]

Applying (19) once to the midpoint and once to the averaged endpoint entropy
gives (17).

## Six-coordinate rational certificate

The executable fixture uses the Householder matrix

\[
R=I-{2\over91}hh^{\mathsf T},\qquad h=(1,2,3,4,5,6)^{\mathsf T},
\]

and

\[
\begin{aligned}
u&=Re_1=(89,-4,-6,-8,-10,-12)^{\mathsf T}/91,\\
v&=(3Re_1+4Re_2)/5\\
 &= (251/455,64/91,-66/455,-88/455,-22/91,-132/455)^{\mathsf T},\\
a&=7/10,\qquad b=4/5.
\end{aligned}
\]

It reconstructs all 64 exact atoms by the signed determinant formula.  The
boundary gap is

\[
G=0.4268309083189009566163964062281508840\ldots.
\]

For `epsilon=1/1000`, the exact bit-flip channel is checked atom by atom and
(15)--(17) give

\[
G_\epsilon\ge0.3040346752858926646434378892525829032\ldots>0.
\]

The directly evaluated strict-kernel gap is

\[
0.4129143654081063661948531289720084917\ldots.
\]

The proof decision uses the explicit continuity bound, not the latter decimal.
See `code/verify_rank1_midpoint.py` and
`output/verify_rank1_midpoint.txt`.

## Scope

This theorem excludes all chords whose two endpoints are rank-one real DPP
kernels, including moving physical frames, unequal endpoint eigenvalues, zero
coordinates, and dimensions `n=4,5,6`.  It also excludes an explicit strict
interior bit-flip neighborhood of every nonconstant such chord.

It does not cover arbitrary rank-two endpoints, a moving rank-three frame,
large interior lifts, or the unrestricted real-kernel problem.  No novelty or
priority claim is made here; correctness and novelty require separate review.
