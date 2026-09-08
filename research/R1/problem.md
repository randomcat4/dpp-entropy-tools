# R1 problem

Status: RUNNING.

R1 studies the real-symmetric restriction of finite DPP entropy concavity.
The ambient space is the open convex set of real symmetric positive
contractions:

```text
K = K^T,        0 < K < I.
```

For every subset S of [n], the exact event probability is computed from the
inclusion probabilities by Mobius inversion:

```text
p_K(S) = sum_{T superset S} (-1)^(|T|-|S|) det K[T]
       = (-1)^|S^c| det(K - I[S^c]).
```

The entropy under test is the full event entropy

```text
H(K) = - sum_S p_K(S) log p_K(S).
```

Principal minors det K[S] are inclusion probabilities, not event
probabilities, and are not used as entropy atoms.

R1 success criterion is one of:

1. DISPROVED: produce explicit rational real symmetric matrices K0,V and a
   rational t > 0 such that 0 < K0 +- tV < I and
   `(H(K0-tV)+H(K0+tV))/2 - H(K0) > 0`, with a strict rational interval
   certificate.
2. PROVED_FOR_FAMILY: prove nonpositive curvature or nonpositive chord gap
   for a stated real-symmetric family with explicit quantifiers.
3. INCOMPLETE/NO_HIT: report only the finite searched denominator, seeds,
   filters, and verifier coverage. No finite no-hit is promoted to a theorem.
