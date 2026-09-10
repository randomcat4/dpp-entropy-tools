# Independent audit of the pointwise resolvent obstruction

For

```text
A=1/4, B=16/25, q=109/1000, qbar=1/1000,
K=[[1/2,0,1/4],[0,1/2,2/5],[1/4,2/5,277/500]],
D=[[-18,146,108],[146,-72,5],[108,5,40]],
r=1/50000,
```

all eight complete atoms were reconstructed afresh as

```text
p_x(t)=(-1)^|Z_x| det(K+tD-I_Zx).
```

Summing over the third bit and differentiating the exact rational functions reproduced, for leaf signs `s1,s2 in {+1,-1}`,

```text
P'_s=(s1 D11+s2 D22)/2,
P''_s=2s1s2(D11 D22-D12^2),
q'_s=D33+A D11+B D22+2s1s2 sqrt(AB)D12
     -2s1 sqrt(A)D13-2s2 sqrt(B)D23,
q''_s=-4(s1 e1^2+s2 e2^2),
e1=D13-(s1 sqrt(A)D11+s2 sqrt(B)D12),
e2=D23-(s1 sqrt(A)D12+s2 sqrt(B)D22).
```

Direct differentiation of

```text
Phi_r=sum_s P_s/(r+q_s)
```

gives the exact value

```text
-47488558049748267993080620088778228551027375300000000000
/2044542058422113103788725284171055940635901533282467
```

which is approximately `-23226.9900509641905987`.

The same independent event jets give

```text
G1'' = 46683.177217861547006998358147446...,
G0'' = 12761038.5854685968057558219772137...,
-H(P)''=22032,
-H''  = 12829753.7626864583527628203353612... .
```

Thus the pointwise-in-`r` positivity claim is false, while the integrated occupied side, vacant side, and complete entropy all have the concave sign at this witness. The exact classification is **method/certificate obstruction only**.
