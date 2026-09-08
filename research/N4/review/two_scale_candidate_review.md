STATUS: CORRECT

# Independent review: separated rare-leaf two-scale candidate

## Object binding

- Reviewed working file: `math/i05-successors-20260909/N4/two_scale_candidate.md`.
- Working-file SHA256: `5c173df8dcc80661d48cf4ea72e33c0dbe90b5778c562e69f8400a9263f008ba`.
- Frozen main-repo commit: `1abc7408b92831fddad6e2defde8daa2529daac3`.
- Frozen main-repo path: `research/N4/proofs/two_scale_candidate.md`.
- Git blob read from that commit: `3971f764b66716445f4df3b3c13499ef0566c7d7`.

I did not author the candidate.  I reviewed the frozen statement as a
conditional local exclusion, not as a proof of unrestricted N4 concavity.

## Verdict

The proof is correct for the stated conditional scope: fixed strict
`A,u,v`, separated leaf scales `d3=r^2`, `d4=r^4`, directions restricted to
the two connection columns, and the explicit premise that both limiting
single-column Hessians `L_u` and `L_v` are strictly negative definite.

No critical gap was found in the Taylor remainders, powers of `r`, mixed-block
coefficient, or final Schur-complement gate.

## Checks

1. The block Schur complements are correct.  The lower complement is exactly
   `A-uu^T-vv^T`; the upper complement tends to `I-A`, with perturbations
   `r^2 uu^T/(1-r^2)` and `r^4 vv^T/(1-r^4)`.  The frozen strict margins
   therefore give `0<K_r<I` for all sufficiently small `r`.
2. The conditional event law factors as `q_t p_{C_t}(U)`.  With
   `m3=r^2` or `r^2-1` and `m4=r^4` or `r^4-1`, the signs from the exact
   complete-event determinant cancel exactly into the Bernoulli leaf mass
   `q_t`.
3. Setting `x=r^2` and `y=r^4`, the conditional sum is analytic in
   `(x,y,w,z)` near `(0,0,u,v)`.  The expansion
   `F=h(A)+x J_A(w)+y J_A(z)+O(x^2+xy+y^2)` follows from the four limiting
   leaf events.  Differentiating after this analytic expansion gives
   `Hess_w F=x Hess J_A(w)+O(x^2+xy)` and
   `Hess_z F=y Hess J_A(z)+O(xy+y^2)`; the `x^2` term has no `z`
   dependence when `y=0`.
4. The mixed block has order `r^6`.  The coefficient
   `q_t/(m3 m4)` is `+1,-1,-1,+1` for `00,10,01,11` up to the ordering used
   in the note, so the displayed discrete second difference of the four
   central Hessians has the right signs.  All four central kernels stay in a
   fixed strict compact neighborhood, hence the Hessian bracket is bounded.
5. From the premise `L_u,L_v<0`, the diagonal costs satisfy
   `N3_r >= a r^2 I` and `N4_r >= b r^4 I` for small `r`.  With
   `M_r=O(r^6)`, the whitened mixed norm is `O(r^3)`, so the Schur
   complement is strictly negative for sufficiently small `r`.

## Scope

The certificate is local in `r` and non-uniform near boundary margins or when
`L_u` or `L_v` approach singularity.  It does not cover arbitrary finite `r`,
directions changing `A` or leaf diagonals, moving frames, or the full
`Sym(4)` direction space.  The reviewed connection-column subspace itself is
four-dimensional through the two free central vectors `(e,f)`.
