# PR53 first proof review

Reviewer: `C1 PR53 first reviewer`
Source snapshot: `randomcat4/dpp-entropy-tools` PR53, commit `e0688fbb713e55f93acf791b83437ddf2cc06b7f`
Frozen scope: `frozen_scope.md`

## Verdict

Overall verdict: `ACCEPTED_SCOPED`.

The four exact bridges claimed in the frozen scope check out. I found no critical gap in the parity joining identity, determinant likelihood and curvature identity, uniform event inverse decay lemma, or balanced beam-splitter reduction. The global sign theorem remains unproved exactly where the author marks it unproved, so this review does not certify whole-legal-interval entropy-rate concavity.

| Scoped claim | Status | Review result |
| --- | --- | --- |
| Parity joining identity and MI-rate equivalence | `CORRECT` | Fourier parity, fixed marginals, joining identity, and the factor-two rate normalization are consistent. |
| Complete-event determinant likelihood and Fisher-plus-acceleration sign obligation | `CORRECT` | The signed event determinant, Schur-complement likelihood, derivative formulas, and finite sign obligation are correct on strict legal intervals. |
| Uniform inverse and finite-range inverse decay | `CORRECT` | The `J M_Z` coercivity proof and Neumann/bandwidth decay argument give configuration- and volume-uniform constants. |
| Balanced fermionic beam-splitter reduction and occupation-entropy remainder | `CORRECT` | The quasifree covariance transform, DPP occupation marginals, entropy decomposition, and distinction from quantum/spectral entropy are correct. |

## Claim 1: parity joining and MI rate

Status: `CORRECT`.

The block form in `proof.md` lines 14-23 follows from the half-period Fourier selection rule: the even Fourier coefficients of `g` vanish and the odd Fourier coefficients of `c` vanish. Reordering `{0,...,2m-1}` into even and odd sites is only a coordinate permutation, so no spectral-basis entropy substitution is introduced.

The parity marginals are fixed and equal to the DPP law of `A_m` (`proof.md` line 23). Therefore the finite identity

```text
H(K_m(t)) = 2H(A_m)-D(P_m(t)||P_A tensor P_A)
```

is just the standard mutual-information identity for the two parity strings (`proof.md` lines 27-44). Boundary events with zero probability are handled by continuity and the `0 log 0=0` convention (`proof.md` line 44).

The rate normalization is also right. Since `K_m(t)` is the `2m`-site window of `f_t`, while `A_m` is the `m`-site window of the decimated symbol `a`, dividing `I_m=2H_m(a)-H_{2m}(f_t)` by `m` gives `2h(a)-2h(f_t)`, exactly the displayed `2[h(a)-h(f_t)]` in `proof.md` lines 46-54. Thus convexity of `i(t)` is equivalent to concavity of `h(f_t)` (`proof.md` lines 56-60).

Boundary attack: no factor-of-two or parity-indexing error found. Entropy-rate existence is only used after finite identities; for stationary finite-alphabet processes it follows from subadditivity, and the cited Lyons-Steif stationary DPP paper supplies the relevant process background without claiming the needed affine concavity.

## Claim 2: determinant likelihood and sign obligation

Status: `CORRECT`.

For strict finite two-block kernels, every marginal complete event has positive probability, so `M_x` and `N_y` are invertible (`proof.md` lines 71-78). The signed complete-event determinant formula (`proof.md` lines 77-83) is the usual inclusion-exclusion form of a marginal-kernel DPP complete event.

The Schur complement gives

```text
r_s(x,y)=det(I-s N_y^{-1} C* M_x^{-1} C)
```

with no rank truncation (`proof.md` lines 85-92). The event matrix in the determinant need not be Hermitian or normal, but this is not a gap: the determinant is the ratio of two strictly positive complete-event probabilities on the legal interval (`proof.md` line 92). No inverse-norm estimate is being smuggled into this identity.

The differentiation formulas for `J(s)=E_Q[r_s log r_s]` are correct in the finite strict setting (`proof.md` lines 94-105). The terms `E_Q r_s'=0` and `E_Q r_s''=0` come from differentiating `E_Q r_s=1`, which is why the formulas contain the Fisher term plus the acceleration term and no extra normalization term. From `H=H(A)+H(B)-J(t^2)`, the finite curvature identity `H''(t)=-2J'(s)-4sJ''(s)` follows (`proof.md` lines 107-111), so finite concavity is equivalent to `J'(s)+2sJ''(s)>=0` (`proof.md` lines 113-119).

The conditional formula is also consistent. Conditioning on the complete second-block event `y` gives `K_{A|y}(t)=A-s C(B-I_{Z_y})^{-1}C*`, written as `A+sD_y` with `D_y=-C(B-I_{Z_y})^{-1}C*` (`proof.md` lines 121-128). The law of `y` is fixed because the second marginal is `B` (`proof.md` line 130). The identity `sum_y P_B(y)(B-I_{Z_y})^{-1}=0` (`proof.md` lines 138-143) follows by differentiating the finite complete-event normalization in an arbitrary matrix direction; the inverse is Hermitian here, so there is no transpose mismatch.

Remaining obligation: this claim identifies the exact sign theorem still needed. It does not prove that sign. The unproved target is stated in `README.md` lines 45-51 and in `proof.md` lines 326-333, while `proof.md` lines 337-339 explicitly say the global sign and `(BS-occ)` are not proved.

## Claim 3: uniform inverse and inverse decay

Status: `CORRECT`.

Lemma 4.1 is sound. For `S=Z^c` and `J=I_S direct-sum (-I_Z)`, the off-diagonal terms in `v*J M_Z v` cancel in real part, leaving

```text
Re(v*J M_Z v)=v_S* A_SS v_S + v_Z*(I-A_ZZ)v_Z >= delta ||v||^2.
```

This is exactly `proof.md` lines 165-181. Since `J` is unitary, the least singular value of `M_Z` is at least `delta`, uniformly over every zero/one pattern and without any lower bound on event probability (`proof.md` lines 175-183).

Lemma 4.2 is also sound. `M_Z` is Hermitian, `||M_Z||<=1`, and Lemma 4.1 gives `M_Z^2>=delta^2 I`, so `R=I-M_Z^2` satisfies `0<=R<=qI` with `q=1-delta^2` (`proof.md` lines 199-206). The expansion

```text
M_Z^{-1}=M_Z sum_{k>=0} R^k
```

is a valid Neumann expansion because `||R||<=q<1`. Bandwidth grows as `(2k+1)w`, so entries vanish until `k>=k0(|i-j|)`, and the remaining tail is bounded by `delta^{-2}q^{k0}` (`proof.md` lines 208-213).

For finite-range half-period families, the spectral margin in `proof.md` lines 219-223 gives the same margin for the parity block because `c` is the half-period average of `f_t`. Since `c` and `g` are trigonometric polynomials, `A_m` and `C_m` have volume-independent bandwidth (`proof.md` line 225). Composing the exponentially decaying inverse with the finite-bandwidth `C_m` gives an exponentially quasilocal `D_y`, uniformly in volume and configuration (`proof.md` lines 225-227). The source compresses the final Schur-test tail estimate, but the needed row-sum bound is standard one-dimensional finite-bandwidth bookkeeping and does not create a critical gap.

Boundary attack: constants depend on the spectral margin, bandwidth, and finite coefficients, not on `m` or the probability of `y`. This addresses the requested non-normal/event-inverse concern for the inverse lemma; the matrices in Lemma 4 are Hermitian even though the determinant likelihood matrix in Claim 2 need not be normal.

## Claim 4: balanced beam splitter

Status: `CORRECT`.

The finite quasifree representation in `proof.md` lines 233-244 is correct: for strict `K`, `rho_K=det(I-K) direct-sum_r wedge^r K(I-K)^{-1}`, so its occupation diagonal gives the complete DPP law. This matches Dierckx-Fannes-Pogorzelska, where a gauge-invariant quasifree state with symbol `Q` is characterized by determinant correlations and `0<=Q<=I`, and its density matrix is written as the determinant-prefactored exterior-power direct sum.

The balanced one-particle unitary `W` in `proof.md` lines 246-266 gives covariance

```text
[ (K_0+K_1)/2   (K_1-K_0)/2 ]
[ (K_1-K_0)/2   (K_0+K_1)/2 ],
```

up to the sign convention for the off-diagonal block. Both one-copy output marginals are therefore the quasifree state `rho_M`, so their occupation laws are the complete DPP law of `M` (`proof.md` lines 259-270). Classical subadditivity of the measured joint occupation law gives `H(q)<=2H(M)` (`proof.md` lines 270-274).

The reduction is exact: if `(BS-occ)` held, namely `H(q)>=H(K_0)+H(K_1)`, then `2H(M)>=H(K_0)+H(K_1)` follows immediately (`proof.md` lines 276-282). The decomposition in `proof.md` lines 299-306 is algebraic:

```text
2H(M)-H(K_0)-H(K_1)=I_q(X:Y)+[H(q)-H(K_0)-H(K_1)].
```

The first term is nonnegative mutual information; the bracket is exactly the unproved occupation-entropy gain.

The entropy distinction is handled correctly. Dierckx-Fannes-Pogorzelska give the von Neumann entropy of a quasifree state as the one-particle spectral expression. Lyu-Bu define the balanced fermionic convolution through a fermionic beam splitter and prove a von Neumann entropy inequality for the reduced output using quantum subadditivity. That source supports `2S(rho_M)>=S(rho_K0)+S(rho_K1)` but does not imply `(BS-occ)`, because DPP Shannon entropy is the entropy of the occupation-basis dephased state, `S(Delta rho_K)`, as stated in `proof.md` lines 284-297.

Boundary attack: the proof does not confuse the fermionic tensor product with a classical product channel. The marginal statement is only for output occupation measurements after partial trace, and the report does not claim a classical channel from the input DPP laws to `q`. The conceptual sentence in `proof.md` line 308 is not needed for the accepted reduction.

## Floating diagnostics

The probe script explicitly labels itself a bounded diagnostic, not a proof (`code/probe_balanced_beamsplitter.py` lines 3-12). The saved output repeats `FINITE_FLOAT_DIAGNOSTIC_ONLY_NOT_A_PROOF` (`output/balanced_beamsplitter_probe.json` lines 87-89). I did not rerun it and did not use it to certify any theorem.

The diagnostic values are consistent with the finite identities it checks: probability normalization, quasifree diagonal agreement, output marginal agreement, and the gap decomposition are near floating precision in the listed cases (`output/balanced_beamsplitter_probe.json` lines 8-19, 29-40, 50-61, 71-82). They provide no rate theorem and no evidence for the missing global sign beyond finite examples.

## External dependency match

The scoped proof is mostly self-contained finite algebra. External sources match the limited uses stated in `sources.md`.

- Lyons-Steif, arXiv:math/0204324, studies stationary DPPs defined by Toeplitz minors and entropy estimates. This matches background use only and does not supply affine-symbol concavity.
- Mészáros, arXiv:1905.11459, proves limiting entropy results for determinantal processes. This matches comparison/background use only and does not supply a parameter-curvature sign.
- Dierckx-Fannes-Pogorzelska, arXiv:0709.1061, supports the finite gauge-invariant quasifree density and spectral von Neumann entropy formulas used in the beam-splitter section.
- Lyu-Bu, arXiv:2409.08180, supports the balanced fermionic convolution construction and the von Neumann entropy inequality under convolution. It does not prove the occupation-measurement inequality `(BS-occ)`.

Primary-source checks used:

- https://arxiv.org/abs/math/0204324
- https://arxiv.org/abs/1905.11459
- https://arxiv.org/html/0709.1061v1
- https://arxiv.org/html/2409.08180

## Remaining unproved sign

The exact remaining sign is not hidden. It is

```text
J_m'(s)+2sJ_m''(s) >= -o(m)
```

or the stronger bounded-boundary version in `proof.md` lines 326-333, for the exact determinant likelihood of `proof.md` lines 85-98. Equivalently, the operator route needs the occupation inequality `(BS-occ)` in `proof.md` lines 276-280, or enough of the bracket in `proof.md` lines 299-306 to offset the output mutual information.

Until one of those sign statements is proved, the whole-legal-interval entropy-rate concavity problem remains `INCOMPLETE`. This is a limitation acknowledged by the source, not a contradiction in the four scoped bridges.

## Formal and computational status

No new formal proof was run. No numerical or symbolic computation was necessary for this first proof review, so I did not create a `COMPUTE_PLAN.md` and did not request a server run.
