# PR53 second independent review

Verdict: **ACCEPTED_SCOPED** for the five-file PR53 checkpoint at frozen author head `e0688fbb713e55f93acf791b83437ddf2cc06b7f`.

This is a second nonauthor analytic review of the PR53 source files only. I did not read C1's first review, code, or conclusions. I did not use PR54, C2 issue #52 work, private author code, or PR41/PR43 theorem black boxes. I did not execute the PR53 diagnostic code; its code and JSON output were read as frozen source artifacts only.

## Files read

Source directory:

`research/I05-DPP-21-20260909/`

Files read in full:

1. `proof.md`
2. `README.md`
3. `sources.md`
4. `code/probe_balanced_beamsplitter.py`
5. `output/balanced_beamsplitter_probe.json`

The README accurately states the checkpoint's status as incomplete author derivations: no whole-legal-interval theorem and no true entropy-rate counterexample are claimed (`README.md:5-18`). The proof likewise says all logarithms are natural, the entropy is complete-configuration Shannon entropy, and spectral entropy is not substituted (`proof.md:1-4`).

## 1. Parity reordering and mutual-information rate normalization

The parity block form is correct. If `c(theta+1/2)=c(theta)` and `g(theta+1/2)=-g(theta)`, then odd Fourier coefficients of `c` and even Fourier coefficients of `g` vanish. After reordering a `2m` window into even sites followed by odd sites, the two diagonal blocks are equal and the off-diagonal block is linear in `t` (`proof.md:7-23`). This is a permutation of observed coordinates, not a spectral rotation.

The finite joining identity

\[
H(K_m(t))=2H(A_m)-I_m(t),\qquad I_m(t)=D(P_m(t)\|P_A\otimes P_A)
\]

follows because the two parity marginals are fixed and equal to `P_A` (`proof.md:27-45`). Boundary cases are handled only by continuity of entropy with `0 log 0=0`.

The rate normalization is also correct. Since the original window has length `2m`,

\[
\frac{I_m(t)}{m}
=2\frac{H_m(a)}{m}-\frac{H_{2m}(f_t)}{m}
\to 2[h(a)-h(f_t)].
\]

This matches `proof.md:46-54`. Therefore concavity of `h(c+tg)` is exactly convexity of the parity mutual-information rate `i(t)` on a legal interval (`proof.md:56-60`). No derivative of the limiting rate is being assumed.

## 2. Complete-event likelihood and finite sign obligation

The complete-event determinant formula is valid. For block kernel

\[
K_t=\begin{pmatrix}A&tC\\tC^*&B\end{pmatrix}
\]

and complete configurations `x,y`, the event matrix is

\[
\begin{pmatrix}A-I_{Z_x}&tC\\tC^*&B-I_{Z_y}\end{pmatrix}.
\]

With `M_x=A-I_{Z_x}`, `N_y=B-I_{Z_y}`, strictness makes the event probabilities positive and the complete-event matrices invertible (`proof.md:62-84`). Taking the Schur complement gives

\[
r_s(x,y)=\frac{p_t(x,y)}{Q(x,y)}
=\det(I-sN_y^{-1}C^*M_x^{-1}C),
\qquad s=t^2
\]

(`proof.md:85-93`). No rank truncation or Hermitian simplification is made.

For `J(s)=E_Q[r_s log r_s]`, normalization `E_Q r_s=1` gives

\[
J'(s)=E_Q[r_s'\log r_s],\qquad
J''(s)=E_Q[(r_s')^2/r_s+r_s''\log r_s]
\]

(`proof.md:94-107`). This keeps both the full Fisher term and the complete acceleration term. Since `H(K_t)=H(A)+H(B)-J(t^2)`, the exact finite sign obligation is

\[
J'(s)+2sJ''(s)\ge0
\]

(`proof.md:107-119`). The proof correctly states that a volume-uniform version up to `o(m)` boundary error would be needed for rate concavity; it does not claim that sign.

The conditional version is also properly scoped. Conditioning on a complete second-block configuration gives `A+sD_y`, with `D_y=-C(B-I_{Z_y})^{-1}C^*`; the second-block law is independent of `t`; and averaging the inverse identity gives `sum_y P_B(y)D_y=0`, hence `Phi'(0)=0` (`proof.md:121-145`). Away from zero, the missing claim is an averaged sign, not pointwise concavity for each generally high-rank indefinite `D_y`.

## 3. Uniform finite-range inverse and exponential decay

Lemma 4.1 is correct. If `delta I <= A <= (1-delta)I`, then for `M_Z=A-I_Z` and `J=I_S direct-sum (-I_Z)`, the cross terms in `v*J M_Z v` are purely imaginary, while

\[
\operatorname{Re} v^*JM_Zv
=v_S^*A_{SS}v_S+v_Z^*(I-A_{ZZ})v_Z
\ge \delta\|v\|^2.
\]

Since `J` is unitary, the least singular value of `M_Z` is at least `delta` (`proof.md:147-183`). This bound is configuration-uniform and does not use lower bounds on rare event probabilities.

Lemma 4.2's decay estimate is also valid for finite range. `M_Z` is Hermitian, `||M_Z||<=1`, and Lemma 4.1 gives `M_Z^2>=delta^2 I`. Thus

\[
M_Z^{-1}=M_Z\sum_{k\ge0}(I-M_Z^2)^k,
\]

with `||I-M_Z^2||<=q=1-delta^2`. Bandwidth support shows entries vanish until `k0(|i-j|)=max(0,ceil((|i-j|/w-1)/2))`, giving

\[
|(M_Z^{-1})_{ij}|\le \delta^{-2}q^{k0(|i-j|)}
\]

(`proof.md:185-215`). The constants depend on the strict spectral margin and finite bandwidth, not on configuration or volume.

The stated consequence for trigonometric-polynomial half-period families is sound as an interface: strict spectral margin on a compact legal parameter interval gives the needed finite-compression margin; finite Fourier support gives volume-independent bandwidth; and the conditional matrices `D_y` become exponentially quasilocal uniformly in `m,y,t` (`proof.md:217-227`). This genuinely removes the PR39-style dependence on small absolute Wiener row sums, but it still gives only locality/convergence control, not the sign of (3.9) or (3.12). The README states that boundary correctly (`README.md:11-18`, `README.md:41-51`).

## 4. Balanced fermionic beam-splitter reduction

The quasifree bridge is correctly stated. For strict `K`, the gauge-invariant quasifree state

\[
\rho_K=\det(I-K)\bigoplus_r \wedge^r L,\qquad L=K(I-K)^{-1}
\]

has occupation diagonal equal to the complete DPP law (`proof.md:229-245`). The balanced one-particle unitary

\[
W=2^{-1/2}\begin{pmatrix}I&I\\-I&I\end{pmatrix}
\]

transforms the covariance of `rho_{K0}\otimes rho_{K1}` into

\[
\begin{pmatrix}M&D\\D&M\end{pmatrix},\qquad
M=(K_0+K_1)/2,\quad D=(K_1-K_0)/2
\]

up to the stated sign convention (`proof.md:246-268`). Hence both output occupation marginals are the DPP law for `M`.

For the measured occupation distribution `q`, classical subadditivity gives `H(q)<=2H(M)` (`proof.md:270-274`). Therefore the occupation inequality

\[
H(q)\ge H(K_0)+H(K_1)
\]

would imply finite DPP midpoint concavity (`proof.md:276-282`). The proof is careful that the known quantum inequality is instead

\[
2S(\rho_M)\ge S(\rho_{K_0})+S(\rho_{K_1}),
\]

where `S(rho_K)=Tr b(K)` is von Neumann/spectral entropy (`proof.md:284-297`). DPP Shannon entropy is `S(Delta rho_K)`, so an extra coherence-loss term is needed. This distinction is also supported by the source boundary in `sources.md:19-31`.

The midpoint gap decomposition

\[
2H(M)-H(K_0)-H(K_1)
=I_q(X:Y)+[H(q)-H(K_0)-H(K_1)]
\]

is an exact add-and-subtract identity (`proof.md:299-306`). It correctly shows that the occupation inequality is sufficient and stronger than midpoint concavity. The proof also properly notes that a quasifree channel need not preserve the occupation diagonal algebra when the fixed block is correlated, so quantum data processing does not automatically yield a classical channel between DPP laws (`proof.md:308-309`).

## 5. Diagnostic code and output

The diagnostic script explicitly labels itself as non-proof, finite, and double-precision only (`code/probe_balanced_beamsplitter.py:1-12`). It constructs complete DPP probabilities by signed event determinants, builds the quasifree density, constructs the fermionic second quantization by exterior minors, and checks finite beam-splitter entropy quantities for four `n=4` cases (`code/probe_balanced_beamsplitter.py:38-79`, `code/probe_balanced_beamsplitter.py:120-192`).

The JSON output is correctly labeled `FINITE_FLOAT_DIAGNOSTIC_ONLY_NOT_A_PROOF` (`output/balanced_beamsplitter_probe.json:87-90`). The listed cases show small probability, diagonal, marginal, unitarity, and decomposition errors at floating precision, but they are not certificates and are not used to prove a rate theorem (`output/balanced_beamsplitter_probe.json:1-90`). This matches the proof's explicit warning that finite probes cannot upgrade the status (`proof.md:335-341`) and the sources boundary (`sources.md:43-45`).

## 6. Source-use boundaries

The sources file is properly scoped. The stationary DPP references are used for background and entropy-rate/prediction framing, not for affine-symbol concavity (`sources.md:5-17`). The quasifree references are used for the standard state/map bridge and explicitly do not prove the occupation-measurement inequality needed here (`sources.md:19-31`). The inverse-decay constants are proved directly from the Neumann series and bandwidth support, with no external inverse-decay theorem required (`sources.md:33-41`). No cited source is claimed to prove whole-legal-interval concavity (`sources.md:43-45`).

## Attacks and exclusions checked

- **Rate normalization:** the factor is `I_m/m=2[h(a)-h(f_t)]`, because the original window has length `2m`; no hidden factor-of-two error.
- **Finite-to-rate passage:** the proof requires finite Jensen or finite signed curvature first, then division by `m`; it does not differentiate a limiting entropy rate (`proof.md:119`, `proof.md:326-333`).
- **Complete-event likelihood:** the determinant density keeps all complete configurations and does not replace Shannon entropy with spectral entropy (`proof.md:1-4`, `proof.md:62-119`).
- **Uniform constants:** inverse and decay constants depend on `delta`, finite bandwidth, and symbols, not on event configuration or volume (`proof.md:147-227`).
- **Endpoint limits:** strict spectral margin and compact legal intervals are required for the inverse lemmas. Endpoints where the margin vanishes are not covered.
- **General nonconstant centers:** the checkpoint gives interfaces beyond PR39's small-Wiener neighborhood, but not global concavity for arbitrary nonconstant centers (`README.md:7-18`, `README.md:45-51`).
- **Phase loss under measurement:** the proof distinguishes von Neumann entropy from occupation-basis Shannon entropy and keeps the extra coherence term explicit (`proof.md:284-309`).
- **Floating diagnostics:** the probe is finite double precision and does not certify any parameter domain or entropy-rate claim (`code/probe_balanced_beamsplitter.py:1-12`, `output/balanced_beamsplitter_probe.json:87-90`).

## Accepted scope

Accepted as correct scoped derivations/interfaces:

- parity block form for half-period-even/odd symbols on even windows;
- mutual-information rate reformulation with the correct factor `2`;
- complete-event determinant likelihood and the exact finite sign obligation `J'(s)+2sJ''(s)>=0`;
- conditional Schur formula and averaged inverse identity at `s=0`;
- configuration-uniform inverse bound and finite-range exponential decay under strict spectral margin;
- balanced fermionic beam-splitter reduction to the occupation inequality `(BS-occ)`;
- distinction between quantum von Neumann entropy and measured occupation Shannon entropy;
- finite diagnostic code/output as diagnostic only.

Not accepted here:

- global rate concavity;
- whole-legal-interval concavity for the PR39 example;
- the missing volume-uniform signed-curvature estimate;
- the occupation inequality `(BS-occ)`;
- a classical-channel proof from quantum data processing;
- endpoint cases without strict spectral margin;
- general nonconstant centers outside the stated interfaces;
- any conclusion from PR54, C2 issue #52, C1's first review, or finite floating diagnostics.

## Final verdict

**ACCEPTED_SCOPED.** PR53 is a valid scoped checkpoint of exact bridges and route reductions beyond the PR39 small-Wiener argument. It correctly leaves the load-bearing sign problems open: the finite/volume-uniform `J'(s)+2sJ''(s)` inequality and the balanced-beam-splitter occupation-entropy inequality.
