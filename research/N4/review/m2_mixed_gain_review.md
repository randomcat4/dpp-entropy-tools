STATUS: CORRECT

# Independent review: M2 simultaneous radial columns

## Object binding

- Reviewed repo: `children/mechanism/repo`.
- Reviewed file: `research/N4/mechanism/mixed_gain_attempt.md`.
- Mechanism commit: `03a2424555f599d4cdfcb3f4a2533e5008c56d60`.
- Git blob: `c9e710944f43215a57efcf12a158b272f47cdef5`.
- Working-file SHA256: `b6cf6b0a21600a248ac38befdb46c98349feb3f4e4b9974cf02711f3a256e918`.

I reviewed the claimed restricted theorem and the radial mixed-gain bound.
The file's own `INCOMPLETE` label for arbitrary nonradial two-column
directions is appropriate and is not treated as a proved claim.

## Verdict

The proof is correct for the frozen restricted family `K(A,s)` with fixed
leaf marginals `0<dj<1`, fixed nonzero vectors `vj`, affine central block
`A`, and affine scalar column lengths `sj`.  It also correctly proves strict
finite-chord concavity inside this parameter domain and the radial projected
gain bound in the two-column case.

No critical gap was found in the joint concavity argument, the zero-column
handling, the finite-chord strictness argument, or the radial gain budget.

## Checks

1. The domain `Omega` is open and convex because `K(A,s)` is affine in
   `(A,s)` and strict positive contractions form an open convex set.
2. The event conditioning is exact.  For each leaf pattern `t`,
   `m_j=d_j` or `d_j-1`, and block determinants give
   `p_K(U,t)=q_t p_{C_t}(U)`.  The inequalities
   `C_all1 <= C_t <= C_all0` hold term by term, and the lower and upper
   Schur complements give `0<C_t<I`.
3. Along `A(z)=A+zW`, `s_j(z)=s_j+z h_j`, the derivatives
   `C_t'=W-sum_j 2s_j h_j V_j/m_j` and
   `C_t''=-sum_j 2h_j^2 V_j/m_j` are correct.  Formula (M2.2) keeps the
   full mixed Hessian of the conditional two-site entropies; it is not a
   separate-column inference.
4. Pairing the two values of one leaf gives
   `R_j=2h_j^2 sum q_other (Df(C0)[V_j]-Df(C1)[V_j])`.  If `s_j=0`, then
   `C0=C1` and `R_j=0` exactly.  If `s_j!=0`, the segment from `C1` to `C0`
   is the same rank-one line tested in direction `V_j`.
5. For a strict two-site kernel and nonzero rank-one `V`, every complete
   event probability along `C+uV` is affine in `u`, so
   `D^2 f(C)[V,V] = -sum l_U^2/p_U < 0`.  Integrating this identity along
   the segment proves each nonzero radial acceleration cost has the claimed
   sign.  The displayed lower bound (M2.6) follows from Cauchy-Schwarz on
   event groups with one site present or absent.
6. Strict finite chords are covered.  If some `h_j!=0`, then `s_j(z)` is
   nonzero except at one point, so `F''<0` on a set of positive measure.
   If all `h_j=0`, then `W!=0` and every conditional center moves by the
   same nonzero affine two-site direction; the imported strict two-site
   theorem applies.
7. In the radial two-column subsection, the positive-semidefinite form
   `sum_t q_t Q_{C_t}` gives `|mjoint| <= sqrt(c3 c4)`.  Since the rank-one
   acceleration costs `p3,p4` are strictly positive when both physical
   columns are nonzero, the full-cost gain bound (M2.8) is strictly below
   one.  At a zero physical column, the note correctly returns to the
   `h_j v_j` formulation instead of using a singular radial parameter.
8. The concrete conflicting-sign diamond family is within the theorem's
   scope.  The row-sum bounds are sufficient for strict diagonal dominance
   of the lower Schur complement, and the upper Schur complement is easier
   for `0<r<=1/2` because the coefficients are at most one.

## Scope

This certifies the restricted simultaneous radial-column family, including
moving the central `2 x 2` block.  It does not prove arbitrary nonradial
connection-column directions, non-diagonal leaf blocks, moving `vj` or `dj`,
or unrestricted N4 concavity.  Section 8 correctly leaves the nonradial
budget inequality (M2.9)/(M2.10) as a remaining obligation.

