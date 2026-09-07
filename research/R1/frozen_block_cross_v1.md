# Frozen block-cross midpoint statement (v1)

Let `[n]=B_1 sqcup ... sqcup B_m` be a partition into at least two nonempty
blocks. Let `K_0` be a real symmetric strict contraction that is block
diagonal for this partition. Let `V` be a nonzero real symmetric matrix with

```text
V[B_a,B_a] = 0  for every a.
```

Take `t>0` and assume `K_-=K_0-tV` and `K_+=K_0+tV` are strict contraction
kernels. If `H(K)` denotes the Shannon entropy of the complete DPP event law,
where complete events are defined from `P(A subseteq Y)=det(K_A)` by Mobius
inversion, then

```text
(H(K_-)+H(K_+))/2-H(K_0) < 0.
```

Permitted standard facts are Shannon entropy subadditivity and its equality
condition, the DPP inclusion formula, and the product rule for independent
Bernoulli indicators. The claim is limited to this block-cross family.
