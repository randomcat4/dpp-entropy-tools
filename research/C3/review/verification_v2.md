STATUS: CORRECT

JUSTIFICATION:

I checked `frozen_statement_v2.md` against `proof.md` as a non-author verifier. The proof establishes exactly the scoped radial theorem, not the full Lyons-Steif conjecture.

1. Jeffreys identity (proof Section 1, equations (1)-(3)) is valid without assuming the tested law has product-reference one-site marginals. The only marginal equality used is that `nu_r` and `E_i nu_r` have the same `(-i)` marginal. Since `log((E_i nu_r)/pi)` depends only on `x_{-i}`, its integral against `nu_r-E_i nu_r` is zero. This closes the stated risk in (3).

2. The mixed derivative sign in (5) follows from DPI in the correct direction. For `0<a<b<1`, `Q_j(a)=Q_j(a/b)Q_j(b)`, so reducing `r_j` applies an additional Markov channel to both arguments of the Jeffreys divergence. Both relative entropy terms contract, hence `J_i` is nondecreasing in `r_j`. Since `r_i` is fixed when differentiating in `r_j`, `partial_j partial_i F >= 0` follows.

3. The DPP affine channel identification in Section 2 is exact at the level of inclusion moments. Independent replacement gives

   ```text
   E prod_{i in S} Y_i
     = sum_{T subset S} t^{|T|}(1-t)^{|S|-|T|} det K_T prod_{i in S\T} b_i,
   ```

   and determinant multilinearity gives the same expression for `det[tK_S+(1-t)B_S]`. Inclusion moments determine the binary law, so this is the DPP with kernel `B+t(K-B)`.

4. The passage from one-sided rays to the full feasible finite interval in Section 3 is sound. Near `s=0`, all exact event masses are positive polynomials, so entropy is differentiable and the left and right derivatives agree. Concavity on each half plus the matching derivative gives the crossing-secants criterion. Boundary kernels are handled by continuity from the channel proof and do not require boundary differentiability.

5. The stationary entropy-rate step in Section 4 uses only finite Jensen inequalities and pointwise limits. For each fixed `n`, Section 3 applies to `K_{p+s g,n}=pI_n+sA_n`; for each fixed `s`, subadditivity gives `h(f_s)=lim_n H_n(s)/n`. Dividing the finite inequality by `n` and taking the three existing limits proves rate concavity without differentiating under a limit or exchanging an infimum with Jensen.

Residual scope notes, not gaps:

- The theorem covers only affine lines through a constant scalar symbol and finite rays through an interior diagonal kernel.
- It does not imply concavity for arbitrary scalar chords or arbitrary signed multi-parameter directions.
- Novelty remains unaudited.
