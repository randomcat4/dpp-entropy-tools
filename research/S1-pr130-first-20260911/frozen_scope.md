# Frozen scope

Repository: `randomcat4/dpp-entropy-tools`

Pull request: PR130

Reviewed author head: `4cae5c29effcf01b1fadc7452780b73a58ec94e7`

Author base: `1d440702b16b8e65954edde076686dba8f1901ae`

## Frozen objects

Let real `c,g in L^infinity(T)` satisfy

`delta<=c<=1-delta`,

`c(theta+1/2)=c(theta)`,

`g(theta+1/2)=-g(theta)`, `g!=0`,

with `delta>0`.  Let `h(c+t g)` be the complete-configuration Shannon entropy
rate of the Toeplitz DPP, with natural logarithms and normalization per
original lattice coordinate.

## Accepted conclusions

1. For sufficiently small legal real `t` satisfying
   `t^2 delta^(-2)||g||_infinity^2<=1/4`,

   `0<=h(c)-h(c+t g)`

   `<= (4/3)delta^(-4)||g||_infinity^2||g||_2^2 t^4`.
2. With the accepted parity matching floor, the deficit is `Theta(t^4)` for
   every nonzero `g` in this class.
3. The symmetric second Peano quotient at zero is zero, and the quartic
   quotient stays between positive finite constants for sufficiently small
   nonzero `t`.
4. If a measurable direction admits a nonempty two-sided legal affine interval
   around a strict center, its `L^infinity` boundedness follows from legality;
   hence the theorem applies to such half-period-odd directions.

## Authorized dependency

Only the accepted regularity-free parity matching lower bound from PR53 is
imported.  No analytic response regularity from PR53 or PR117 is imported.

## Exclusions

- existence or continuity of ordinary second or fourth entropy-rate
  derivatives outside `A_0`;
- any off-center curvature sign;
- local concavity on a punctured neighborhood;
- concavity on a whole legal interval;
- general real finite-kernel concavity;
- quantum or spectral entropy substitution;
- novelty, computation, or merge.

