# C3 rate analysis: S1 audit, long-tail residual lemma, and C3-M1 certificate

Status: `CERTIFIED_NEGATIVE_PAIR_GAP_SELF_AUDITED` for the single fixed chord `C3-M1`, and `AUXILIARY_PROVED_WITH_MINIMAL_GAP` for the long-range residual analysis.

This file is written by the C3 rate child as an independent audit/auxiliary unit.  It does not claim a solution of the Lyons--Steif scalar entropy-rate concavity conjecture, and it does not claim an independent non-author review of the new C3-M1 certificate.  It does give a strict fixed-object negative rate gate, with all code, inputs and artifacts preserved under this `rate/` directory.

## 1. S1 certificate audit boundary

I read the S1 round-two verdict, checkpoint, provenance, rate proof/certificate, review audit, and the source scripts used for the boundary and rate computations.

The accepted S1 round-two statement is narrow:

- `S1-R2-B1` is a fixed degree-three three-symbol chord with a certified negative true entropy-rate pair gap.
- The certified gap was
  `[-3.0348902924818035e-5, -7.3460456800473595e-6]` nats.
- The certificate computes the three symbols separately and the six extreme-past kernels separately, including complements.  It does not assume endpoint equality.
- The proof relies on the standard Lyons--Steif entropy-rate/conditioning method, exact finite event determinants, interval logarithms, and a rational variational residual enclosure of all-one and all-zero extreme-past kernels.
- The result is only a fixed-pair exclusion.  It is not a family theorem and not a global concavity proof.

The mathematical S1 method is reusable for a new finite multiharmonic symbol only when the following contract is kept:

1. each fixed symbol has a proved uniform spectral margin `epsilon <= f <= 1-epsilon`;
2. endpoint, center, and complements are handled as separate symbols;
3. the finite-suffix upper bound and extreme-past lower bound are formed for each symbol independently;
4. the all-one/all-zero boundary kernels are enclosed by Loewner-valid operator errors, not by extrapolation of finite entropies;
5. finite event probabilities are exact or outward-enclosed, and logarithms are outward interval evaluations;
6. the positive counterexample gate is `(L_-+L_+)/2-U_0>0`, while strict negative exclusion is `(U_-+U_+)/2-L_0<0`.

## 2. Source facts actually used

I checked the relevant original literature rather than relying only on repository summaries.

- Lyons--Steif, [Stationary determinantal processes: phase multiplicity, Bernoullicity, entropy, and domination](https://arxiv.org/abs/math/0204324), especially the DPP definition and event formula in Section 2, negative association/conditioning facts in Section 2, entropy and finite-symbol bounds in Section 6, the all-one conditioning construction in Theorem 6.12, and Conjecture 9.2.
- Lyons, [Determinantal probability measures](https://arxiv.org/abs/math/0204325), for the finite/infinite DPP conditioning background behind the Schur-complement kernel formula.
- Mészáros, [Limiting entropy of determinantal processes](https://arxiv.org/abs/1905.11459), especially the entropy-density limiting theorem and the role of tightness/local convergence.  I used it only as background for what entropy-density convergence controls; it is not a concavity theorem and not a replacement for the extreme-past certificate.

## 3. Rebuilt extreme-past residual theorem

Let `f` be a fixed scalar symbol with `tau <= f <= 1-tau` a.e. on the circle.  Let `K_f(i,j)=c_{i-j}` be the Toeplitz DPP kernel.  Put the past at `P={-1,-2,...}` and a future test window at `F_N={0,...,N-1}`.  With respect to `l2(P) + C^N`, write

```text
K = [ T   B ]
    [ B*  C ].
```

The margin gives `tau I <= T <= (1-tau)I`, so `T` is invertible.  The all-one extreme-past kernel on `F_N` is

```text
C_infty = C - B* T^(-1) B.
```

This follows by finite-past Schur complements and uniform coercivity, or directly by solving the half-line normal equation `T Y = B` and passing to the energy limit.

For any finitely supported rational matrix `X : C^N -> l2(P)`, define

```text
R   = B - T X,
H_X = B*X + X*B - X*T*X,
A_X = C - H_X.
```

Then the exact identity is

```text
A_X - C_infty = R* T^(-1) R.
```

Therefore

```text
0 <= A_X - C_infty <= (||R||_op^2/tau) I
                 <= (||R||_F^2/tau) I.
```

This is the reusable residual certificate.  It is valid for finite bandwidth and long-range symbols, but the cost of certifying `R` is different.

For a finite bandwidth symbol of degree `m`, `B` has no columns beyond the first `m` future coordinates, and a row-supported `X` has residual supported in the first `M+m` past rows.  The boundary correction is confined to the leading `m by m` future corner, independent of the suffix length.  This is why the S1 scripts can replace only a finite leading corner and still run arbitrary finite suffix lengths.

For a long-range symbol, the same identity holds for each finite `N`, but the boundary correction is an `N by N` object.  One must solve or enclose the residual for the whole future window used in the entropy certificate.  Replacing only a fixed leading corner is no longer justified.

## 4. Long-range square-tail gap

For fixed `N`, ordinary square summability of the Fourier tail is enough to make finite-window residual tails small.  For example,

```text
sum_{r>=0, 0<=j<N, r+j+1>M} |c_{r+j+1}|^2
  = sum_{k>M} min(N,k) |c_k|^2
  <= N sum_{k>M} |c_k|^2.
```

Thus a fixed-window long-range certificate can use a Frobenius residual bound once the needed tail sum is explicitly enclosed.

This is not the same as a volume-uniform operator bound.  Under only `sum |c_k|^2 < infinity`, the needed tail operator norm need not go to zero uniformly in `N`.  A concrete obstruction is the bounded real symbol

```text
f(x)=1/2 + eta * sum_{k>=1} sin(2*pi*k*x)/k
```

with small enough `eta` to keep `tau <= f <= 1-tau`.  Its positive Fourier tail is proportional to `1/k`, hence square-summable.  But the Hankel tail with entries `1/(r+j+1)` does not vanish in operator norm after deleting finitely many anti-diagonals: for columns `0,...,M-1` and rows `M+1,...,2M`, the normalized vector `x_j=M^(-1/2)` gives output norm at least a fixed positive constant.  Therefore ordinary square tail alone cannot support a uniform S1-style operator error `delta_N -> 0` for all future volumes.

The minimal additional condition is an explicit uniform Hankel/operator tail certificate.  A convenient sufficient condition is the weighted square tail

```text
sum_{k>M} k |c_k|^2 -> 0,
```

because the infinite Hankel tail then has Hilbert--Schmidt norm at most the square root of this weighted tail.  An `L_infinity` approximation bound for the whole Toeplitz operator is another sufficient route.  Without one of these stronger controls, long-range finite truncation may still be useful as a fixed-window certificate, but it cannot be advertised as a volume-uniform rate certificate.

## 5. C3-M1 fixed object

The mechanism child froze the true symbol using

```text
K(i,j)=c_(i-j),  c_k=(a_k+i b_k)/2.
```

The true-symbol input is stored in `candidate_true_symbol.json`:

```text
p  = 1/2
a  = [6/25, 594/2525]
b  = [0, 120/2525]
dp = 0
da = [0, 120/2525]
db = [6/25, -594/2525]
step = 1/4
epsilon = 1/200
```

The S1 scripts use the opposite convention `c_k=(a_k-i b_k)/2`. The script input `candidate.json` therefore negates `b` and `db`. Substituting these negated arrays into that code gives exactly `c_k=(a_true+i b_true)/2`, the mechanism's original coefficients at each parameter. This is a convention conversion; it does not change the actual kernel. (If all coefficients were instead conjugated, their event determinants would also be invariant.) The three parameters `t=-1/4,0,1/4` are still computed separately. This paragraph is an editorial correction by the main instance; all numeric input and output bytes remain unchanged.

The margin proof does not use an `L1` cosine/sine bound.  For `|t|<=1/4`, both harmonic Fourier magnitudes satisfy

```text
|c_1(t)| = |c_2(t)| <= (3/25)*sqrt(17)/4.
```

Hence the total oscillation of the real symbol is at most `3*sqrt(17)/25`.  Since

```text
(3*sqrt(17)/25)^2 = 153/625 = 9792/40000
< 9801/40000 = (99/200)^2,
```

we have `3*sqrt(17)/25 < 99/200`, so

```text
1/2 - 3*sqrt(17)/25 > 1/200.
```

The frozen `epsilon=1/200` is valid for all three symbols and their complements.

## 6. C3-M1 computation

The computation was executed once in the C3 private rate directory, single-threaded, using the supplied venv:

```text
Python 3.12.3
mpmath 1.3.0
OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
BLIS_NUM_THREADS=1
```

Sanitized commands, run from the `rate/` directory:

```text
python scripts/c3_m1_variational_boundary.py --candidate candidate.json --output artifacts/c3_m1_boundary_M64.json --M 64 --bits 160
python scripts/c3_m1_rate_certificate.py --candidate candidate.json --boundary artifacts/c3_m1_boundary_M64.json --output artifacts/c3_m1_rate_n4.json --n 4
python scripts/c3_m1_audit.py --candidate candidate.json --true-symbol candidate_true_symbol.json --boundary artifacts/c3_m1_boundary_M64.json --rate artifacts/c3_m1_rate_n4.json --output artifacts/c3_m1_audit_result.json
```

Boundary coverage:

```text
degree m = 2
cases = 3 t-values x 2 complement choices = 6
M = 64
residual rows per case = 66
actual residual complex entries = 792
largest operator-error delta = 9.463653280093224e-08 < 1/200
```

Boundary operator-error floats:

| t | symbol | delta |
|---:|:---|---:|
| -1/4 | f | 5.966985118535407e-25 |
| -1/4 | 1-f | 3.1974331150974e-11 |
| 0 | f | 6.0195420655525785e-34 |
| 0 | 1-f | 4.844511097496308e-10 |
| 1/4 | f | 3.8170478103118223e-29 |
| 1/4 | 1-f | 9.463653280093224e-08 |

Rate coverage:

```text
n = 4
3 symbols x 3 event distributions x 2^(n+1) = 288 exact determinants
all event masses positive Fractions
all distributions exactly normalized
interval log precision = 45 decimal digits
classification = NEGATIVE_PAIR_GAP
```

The true entropy rates satisfy the following certified intervals, in nats:

| t | L | U |
|---:|---:|---:|
| -1/4 | 0.6885543960839915 | 0.6888836396588042 |
| 0 | 0.6887862746339310 | 0.6891526296946623 |
| 1/4 | 0.6878471697215709 | 0.6886872288635815 |

The exact pair-gap enclosure stored in `artifacts/c3_m1_rate_n4.json` is

```text
lower =
-21736338200350506195187245238231755852533113
/22835963083295358096932575511191922182123945984
= -0.0009518467918811257

upper =
-299855012916397501897282364769067397783
/356811923176489970264571492362373784095686656
= -0.0000008403727382396920
```

Thus

```text
(h(f_-)+h(f_+))/2 - h(f_0) < 0.
```

This fixed chord is strictly excluded as a positive Lyons--Steif entropy-rate counterexample.  Since `n=4` already separates the sign, no `n=6` or `n=8` run was performed.

## 7. Self-audit result

The local self-audit `artifacts/c3_m1_audit_result.json` returned `CORRECT_SELF_AUDIT`.  It checked:

- script input is the conjugate of the true mechanism symbol;
- `epsilon=1/200` follows from the exact square comparison above;
- six boundary cases are present;
- every boundary residual, corner, and residual row count recomputes exactly from the saved dyadic `X`;
- every boundary `delta` is below the margin;
- the finite event distributions recompute by an independent Gaussian-elimination determinant implementation;
- all conditional intervals contain the ordinary finite conditional probability;
- the weighted extreme widths match the artifact intervals;
- the final exact pair-gap fractions match the rate artifact and have strictly negative upper endpoint.

This is not a fresh non-author review.  It is an algebraic self-audit by the rate child, useful for handoff and replay.

## 8. Artifact manifest

```text
candidate.json
  sha256 969ea3cdf2c0f2970e17ff4eb915eba2b209114ace5085a7d5f907e504d6f3fa

candidate_true_symbol.json
  sha256 f503d7bfa1e30a5ea30f7fdff2b91474acc158c99cf244c4f8babaaf1307a6a6

scripts/c3_m1_variational_boundary.py
  sha256 c1acb8deb382e35f26fd08209c2858d32d8202a3ac33238a12f659326c3bbaed

scripts/c3_m1_rate_certificate.py
  sha256 946dc35b6311d6bbab7500d1172939b0f1ff6d06a26f728e2089686b4489299e

scripts/c3_m1_audit.py
  sha256 95c1e32d3bdcbf97be9be74b54780ef2e3a59d0a12876ec558273ff4dc18a27d

artifacts/c3_m1_boundary_M64.json
  sha256 3c98ce058bd10e0dcebe7e5cd8a6f095e8fc58e2745b802bbb54f7014fe0b616

artifacts/c3_m1_rate_n4.json
  sha256 e0b09e9265f991b758026fdd4f50dd48a56ac7bb199d92844b2ff0ad7911dc9a

artifacts/c3_m1_audit_result.json
  sha256 09763f4d71b8aad15a4594acb87b407f7aac2a1cc996d164441256cdc51b4224
```

## 9. Handoff

No larger rate computation is needed for C3-M1.  A future independent reviewer can replay the certificate by running the three sanitized commands in Section 6.  If the project later wants long-range symbols rather than finite multiharmonic symbols, the next mathematical obligation is to provide either a fixed-window tail-residual budget for the chosen `n`, or a genuinely volume-uniform Hankel/operator tail certificate stronger than ordinary square summability.
