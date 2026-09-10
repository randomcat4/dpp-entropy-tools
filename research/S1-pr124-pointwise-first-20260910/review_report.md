# PR124 pointwise-resolvent obstruction: narrow FIRST

## Verdict

**ACCEPTED_SCOPED** at exact PR124 head
`344723af6affab240c9f87c395d4e8c1b7b19f6d`.

## Analytic reconstruction

At the witness,

`A=1/4`, `B=16/25`, `q=109/1000`, `qbar=1/1000`.

These quantities are positive and sum to one.  With `b^2=A/4` and
`c^2=B/4`, the leaf block is `(1/2)I`.  Its Schur complement in `K` is `q`,
while the corresponding Schur complement in `I-K` is `qbar`.  Hence
`0<K<I` strictly.  Openness of this condition makes every real symmetric
matrix direction, including the displayed six-coordinate `D`, a legal local
physical tangent.

For leaf signs `s1,s2`, direct two-point complete-event algebra gives

`P_s=1/4`,

`P'_s=(s1 d11+s2 d22)/2`,

`P''_s=2s1s2(d11 d22-d12^2)`.

The occupied-center conditional is the exact complete-event Schur complement

`q_s(t)=K33(t)-v(t)^T M_s(t)^(-1)v(t)`.

At the half-leaf, `M_s^(-1)=2 diag(s1,s2)`.  Differentiating this identity
reproduces the submitted `q'_s` and
`q''_s=-4(s1 e1^2+s2 e2^2)`.  These are conditional coordinates of the full
complete law, not a replacement for that law.

Since `p_s=P_s q_s`,

`Phi_r=sum_s P_s^2/(p_s+rP_s)=sum_s P_s/(q_s+r)`.

Twice differentiating each quotient gives exactly

`P''/R-2P'q'/R^2-(1/4)q''/R^2+(1/2)(q')^2/R^3`,

where `R=q_s+r`.  All denominators are positive at the strict witness.

Substitution of

`r=1/50000`, `D=(-18,-72,40,146,108,5)`,

with `sqrt(A)=1/2`, `sqrt(B)=4/5`, and `sqrt(AB)=2/5`, yields the exact value

`-47488558049748267993080620088778228551027375300000000000`

divided by

`2044542058422113103788725284171055940635901533282467`.

The denominator is positive and the numerator is negative, so
`Phi_r''<0`.

## Independent exact-event check

The short checker was read line by line and rerun once with exact rational
arithmetic.  It constructs `K+tD`, computes every inclusion principal minor,
performs Möbius inversion to all eight complete atoms, verifies total mass one
and positive base masses, groups the four leaf marginals, and differentiates
`P(t)^2/(p_1(t)+rP(t))` directly.  It neither imports the longer checker nor
uses floating-point arithmetic.  The rerun reproduced the exact fraction
above.

## Logical boundary

One negative value at one `r` disproves the old universal pointwise statement
`Phi_r''>=0` and invalidates any purported all-positive certificate for that
statement on the claimed domain.  It does not determine the sign of

`G1''=integral_0^infinity r Phi_r'' dr`,

because other `r` values can dominate the integral.  It therefore supplies
neither an integrated counterexample nor a complete-Shannon entropy
counterexample.  The stronger positive theorems elsewhere in PR124 remain
outside this narrow verdict.

