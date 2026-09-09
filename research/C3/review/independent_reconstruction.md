# C3 independent formula reconstruction

Status: PARTIAL_FORMULA_RECONSTRUCTION, not a final proof review of any later frozen anonymous proof.

I read only the assigned constraint/claim/task files and reconstructed the finite formula from the DPP definitions. I did not read author code or author derivations. The computation below is a small deterministic precheck, not a scan and not an entropy-rate certificate.

## Main findings

1. The exact-row determinant formula is valid for every finite DPP marginal kernel `0<K<I`, not only Toeplitz kernels. For every event `S`,

   ```text
   p_K(S) = det R_S(K),
   R_S(K)_{ij} = K_ij                  if i in S,
              = delta_ij - K_ij        if i not in S.
   ```

   This is the inclusion-exclusion formula written by row multilinearity. Strict `0<K<I` gives `p_K(S)>0` for every `S`, for example from the L-ensemble identity with `L=K(I-K)^{-1}`:

   ```text
   p_K(S) = det(I-K) det L_S > 0.
   ```

2. For the Toeplitz frequency-translation tangent

   ```text
   D_ij = i (i-j) K_ij,
   E_ij = (i-j)^2 K_ij,
   ```

   all exact event scores vanish:

   ```text
   p'_S(K;D) = 0  for every S.
   ```

   This is a strict score-null direction when `D != 0`: the kernel moves in a nonzero Hermitian K-affine direction, but every one of the `2^n` atom probabilities has zero first derivative. It is not merely a cancellation after summing events.

3. The affine second derivative is exactly tied to the second derivative of the genuine gauge orbit:

   ```text
   p''_S(K;D,D) = p'_S(K;E),
   H''_K(D,D) = dH_K(E).
   ```

   Sign convention check: if `U_a = diag(exp(i a i))`, then

   ```text
   K(a) = U_a K U_a^*
        = K + aD - (a^2/2)E + O(a^3).
   ```

   Since every exact event probability is invariant under this diagonal gauge conjugation, differentiating twice gives

   ```text
   0 = p''_S(K;D,D) - p'_S(K;E).
   ```

   The entropy identity follows because the Fisher term is exactly zero:

   ```text
   H''_K(D,D)
     = -sum_S p''_S(K;D,D) log p_S
     = -sum_S p'_S(K;E) log p_S
     = dH_K(E).
   ```

4. The identity does not determine the sign. It replaces the Fisher-vs-acceleration comparison by a single linear entropy derivative in the direction `E`, but `E` is not a monotone direction and the event derivatives `p'_S(K;E)` have mixed signs in the prechecks below. A positive coherent-cycle mechanism therefore still needs a separate sign argument or a certified counterexample; score-nullness alone is not enough.

5. The two deterministic prechecks below both have negative finite affine acceleration. They verify the formula and sign convention; they do not prove finite or entropy-rate concavity.

## Derivation details

For a K-affine path `K(t)=K+tX`, the row event matrix is affine:

```text
R_S(K+tX) = R_S(K) + t R'_S(X),
R'_S(X)_{ij} =  X_ij   if i in S,
             = -X_ij   if i not in S.
```

When `R_S(K)` is invertible, this gives the usual determinant jet

```text
p'_S = p_S tr(A^{-1}B),
p''_S = p_S[(tr A^{-1}B)^2 - tr((A^{-1}B)^2)],
```

where `A=R_S(K)` and `B=R'_S(X)`. The polynomial row-determinant definition is the safer canonical form because it remains exact without choosing inverses. In the strict interior all atom probabilities are positive, so the entropy jet is

```text
H'  = -sum_S p'_S log p_S,
H'' = -sum_S (p'_S)^2/p_S - sum_S p''_S log p_S.
```

For the gauge tangent `D`, the first sum in `H''` vanishes term-by-term.

The gauge proof of score-nullness is also event-row level. For `K(a)=U_a K U_a^*`,

```text
R_S(K(a)) = U_a R_S(K) U_a^*,
```

because the rows outside `S` are `delta_ij-K_ij` and the diagonal delta term is unchanged by `u_i conjugate(u_i)=1`. Therefore `det R_S(K(a))=det R_S(K)` for every event.

## Symbolic/rational precheck

The script `finite_precheck.py` was copied to the server-side C3 review directory and run there with one-thread BLAS/OpenMP environment variables. It uses exact rational complex arithmetic implemented with the Python standard library. Determinants are computed as polynomials by permutation expansion, so the equalities `p'_S=0` and `p''_S=p'_E` are exact checks. Floating point is used only for the final logarithms in the entropy value.

Objects checked:

- `A_real_symmetric_toeplitz_n3`: `c0=1/2`, `c1=1/10`, `c2=1/20`. Gershgorin L1 row bounds are at most `1/5<1/2`, hence `0<K<I`.
- `B_complex_hermitian_toeplitz_n4`: `c0=1/2`, `c1=1/20+i/30`, `c2=-1/40+i/50`, `c3=1/100-i/120`. Gershgorin L1 row bounds are at most `127/600<1/2`, hence `0<K<I`.

Both have nonzero `D`, all exact event checks pass, and the finite affine accelerations are

```text
A: H''_K(D,D) = dH_K(E) ~= -0.007795653294257826
B: H''_K(D,D) = dH_K(E) ~= -0.0015587620931942874
```

These negative values are useful as a sign-convention guard: if another computation reports the opposite sign on the same objects, it has likely reversed the `E` convention or the entropy interval direction.

## Risks for later true entropy-rate certification

1. Finite jets are diagnostics only. A true counterexample needs three fixed symbols `f_-`, `f_0`, `f_+`, not window-dependent kernels, and rigorous entropy-rate intervals satisfying

   ```text
   (L_- + L_+)/2 - U_0 > 0.
   ```

   The exclusion direction is

   ```text
   (U_- + U_+)/2 - L_0 < 0.
   ```

   Reversing these inequalities reverses the mathematical conclusion.

2. The gauge orbit itself has constant finite distributions and constant entropy rate. A K-affine chord in the tangent direction is a different second-order object because it drops the `-(a^2/2)E` term. Any later mechanism must keep this distinction explicit.

3. To realize the tangent by fixed scalar symbols, one must prove `f_-=f_0-sg` and `f_+=f_0+sg` stay in `[0,1]` uniformly. For trigonometric polynomials this should be done by an explicit margin, such as a rational Fourier L1 bound or sharper interval arithmetic; it cannot be inferred from finite principal minors.

4. Rare events cannot be discarded. Even with spectral margin, atom probabilities are exponentially small in volume, and the entropy derivative weights contain `log p_S`. A volume-uniform argument must control the whole sum, not just common events or low-cardinality layers.

5. The identity `H''=dH(E)` is not a sign theorem. A later positive mechanism needs either a direct lower bound for `-sum p'_E log p`, or a certified finite/rate construction. Mixed signs of `p'_E` in both precheck objects show that simple eventwise monotonicity is unavailable.

6. If a non-gauge coherent-cycle mechanism is used, the Fisher term generally returns. It must compare against the full atom Fisher cost `sum (p'_S)^2/p_S`, not a projection to low-order statistics.

7. Any reuse of an S1-style entropy-rate certificate must recheck its hypotheses for the new complex Hermitian scalar Toeplitz symbols: finite range or truncation assumptions, spectral gap, conditional entropy representation, and volume-uniform residuals.

8. Complex Hermitian Toeplitz kernels from non-even real symbols are within the scalar stationary target, but they are outside any purely real finite concavity theorem. A later proof must not silently substitute the real-symmetric finite target.

## Complete script output

```text
finite_precheck.py 2026-09-09.a
python 3.12.3 (main, Mar  3 2026, 12:15:18) [GCC 13.3.0]
platform Linux-6.8.0-79-generic-x86_64-with-glibc2.39
arithmetic=exact rational complex coefficients; entropy logs=float only

OBJECT A_real_symmetric_toeplitz_n3
n=3
c0=1/2
row_l1_bounds=3/20,1/5,3/20
strict_contraction_by_gershgorin=True
nonzero_D_entries=6
events:
  mask=000 S={} p=451/4000 pD_prime=0 pD_second=-9/250 pE_prime=-9/250 relation_exact=True
  mask=001 S={1} p=509/4000 pD_prime=0 pD_second=2/125 pE_prime=2/125 relation_exact=True
  mask=010 S={2} p=539/4000 pD_prime=0 pD_second=2/125 pE_prime=2/125 relation_exact=True
  mask=011 S={1,2} p=501/4000 pD_prime=0 pD_second=1/250 pE_prime=1/250 relation_exact=True
  mask=100 S={3} p=509/4000 pD_prime=0 pD_second=2/125 pE_prime=2/125 relation_exact=True
  mask=101 S={1,3} p=531/4000 pD_prime=0 pD_second=1/250 pE_prime=1/250 relation_exact=True
  mask=110 S={2,3} p=501/4000 pD_prime=0 pD_second=1/250 pE_prime=1/250 relation_exact=True
  mask=111 S={1,2,3} p=459/4000 pD_prime=0 pD_second=-3/125 pE_prime=-3/125 relation_exact=True
sum_p=1
sum_pD_prime=0
sum_pD_second=0
sum_pE_prime=0
min_p=451/4000 (0.11275)
all_exact_checks_pass=True
Hdd_affine_D_equals_dH_E≈-0.007795653294257826
Hdd_sign=negative

OBJECT B_complex_hermitian_toeplitz_n4
n=4
c0=1/2
row_l1_bounds=11/75,127/600,127/600,11/75
strict_contraction_by_gershgorin=True
nonzero_D_entries=12
events:
  mask=0000 S={} p≈0.0592251936806 pD_prime=0 pD_second≈-0.0100364714815 pE_prime≈-0.0100364714815 relation_exact=True
  mask=0001 S={1} p≈0.0615873063194 pD_prime=0 pD_second≈-0.00166908407407 pE_prime≈-0.00166908407407 relation_exact=True
  mask=0010 S={2} p≈0.0634131396528 pD_prime=0 pD_second≈+0.00137591592593 pE_prime≈+0.00137591592593 relation_exact=True
  mask=0011 S={1,2} p≈0.0621632492361 pD_prime=0 pD_second≈+0.00310741740741 pE_prime≈+0.00310741740741 relation_exact=True
  mask=0100 S={3} p≈0.0634131396528 pD_prime=0 pD_second≈+0.00137591592593 pE_prime≈+0.00137591592593 relation_exact=True
  mask=0101 S={1,3} p≈0.0647493603472 pD_prime=0 pD_second≈+0.00212963962963 pE_prime≈+0.00212963962963 relation_exact=True
  mask=0110 S={2,3} p≈0.0637790825694 pD_prime=0 pD_second≈+0.00423463962963 pE_prime≈+0.00423463962963 relation_exact=True
  mask=0111 S={1,2,3} p≈0.0616695285417 pD_prime=0 pD_second≈-0.000517972962963 pE_prime≈-0.000517972962963 relation_exact=True
  mask=1000 S={4} p≈0.0615873063194 pD_prime=0 pD_second≈-0.00166908407407 pE_prime≈-0.00166908407407 relation_exact=True
  mask=1001 S={1,4} p≈0.0639890825694 pD_prime=0 pD_second≈+0.00615241740741 pE_prime≈+0.00615241740741 relation_exact=True
  mask=1010 S={2,4} p≈0.0647493603472 pD_prime=0 pD_second≈+0.00212963962963 pE_prime≈+0.00212963962963 relation_exact=True
  mask=1011 S={1,2,4} p≈0.063285361875 pD_prime=0 pD_second≈+0.000609249259259 pE_prime≈+0.000609249259259 relation_exact=True
  mask=1100 S={3,4} p≈0.0621632492361 pD_prime=0 pD_second≈+0.00310741740741 pE_prime≈+0.00310741740741 relation_exact=True
  mask=1101 S={1,3,4} p≈0.063285361875 pD_prime=0 pD_second≈+0.000609249259259 pE_prime≈+0.000609249259259 relation_exact=True
  mask=1110 S={2,3,4} p≈0.0616695285417 pD_prime=0 pD_second≈-0.000517972962963 pE_prime≈-0.000517972962963 relation_exact=True
  mask=1111 S={1,2,3,4} p≈0.0592707492361 pD_prime=0 pD_second≈-0.0104209159259 pE_prime≈-0.0104209159259 relation_exact=True
sum_p=1
sum_pD_prime=0
sum_pD_second=0
sum_pE_prime=0
min_p=852842789/14400000000 (0.0592251936806)
all_exact_checks_pass=True
Hdd_affine_D_equals_dH_E≈-0.0015587620931942874
Hdd_sign=negative

SCRIPT_EXIT_CODE=0
```
