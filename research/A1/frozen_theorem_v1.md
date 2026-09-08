# Frozen research target v1

Status: INCOMPLETE. Definitions and quantifiers are frozen by the lane owner.
Proof and verification instances may not change or supplement premises.

## Objects and definitions

Let K be a real symmetric 3 by 3 matrix with 0<K<I. For S subset {1,2,3},

    p_K(S) = sum_{T superset S} (-1)^(|T|-|S|) det(K[T]),
    H(K) = -sum_S p_K(S) log p_K(S).

The empty principal determinant is 1. All logarithms are natural. A center
is connected if its graph of nonzero off-diagonal entries is connected.

## Intended question

Determine whether there exist rational K0,V,t, with t>0, K0 connected,
V real symmetric and 0<K0 +/- tV<I, such that

    Delta = (H(K0-tV)+H(K0+tV))/2-H(K0) > 0.

Probe the full six-dimensional entropy Hessian on general connected centers;
triangle cycles are the first priority. An exact reduction or subclass result
does not settle this existential target. The owner must freeze any proposed
subclass theorem separately before its final proof and verification.

## Information and boundaries

Public baseline: R1 PR #8 at ba1227931521fa663f0d5b3f15906a985866877c.
Use only finite full-event entropy. Do not substitute inclusion probabilities,
eigenvalue entropy, a stationary rate, or complex directions. Do not repeat
the excluded 1 by 1 / 2 by 2 block midpoint families.

## Success criteria

1. A strict counterexample requires rational feasibility plus rigorous log
   bounds and an independent non-author fixed-object review.
2. A subclass theorem requires explicit quantifiers, full proof and a fresh
   non-author review. It must be labeled with its actual scope.
3. An incomplete result must identify exact checked identities and the
   smallest remaining inequality; equivalent reformulations are labeled so.

Finite floating positives only nominate candidates. Finite non-hits establish
only their recorded denominators. No novelty claim is authorized by this file.
