# Problem

## Original problem

For a finite real-symmetric positive contraction `K`, let `H(K)` be the
Shannon entropy of its full-subset DPP law.  Find a feasible real-symmetric
chord `K_-`, `K_+` with

```text
Delta = (H(K_-) + H(K_+))/2 - H((K_-+K_+)/2) > 0,
```

or prove a rigorous obstruction for a clearly quantified structural family.

## First bounded objective

Freeze and analyze one balanced, transverse, near-projection family.  Compute
the exact feasibility interval, all leading zero-event scales, and the
coefficient of `epsilon log(1/epsilon)` in `Delta`.

## Intent contract

- Exact event probabilities are obtained by Mobius inversion of inclusion
  minors; principal minors alone are not event probabilities.
- The displayed `Delta` is the counterexample sign.  The opposite Jensen gap
  is not a counterexample.
- A pointwise or finite numerical non-hit is not a universal theorem.
- A result for the frozen family must not be promoted to all real directions,
  all centers, or all dimensions.
- Fixed-`epsilon` chord data and the varying outer family must remain distinct.

## Acceptable outcomes

- a rigorously certified strict counterexample in the frozen family;
- a proof excluding the entire frozen asymptotic family;
- `INCOMPLETE` with an exact coefficient or remainder blocker.
