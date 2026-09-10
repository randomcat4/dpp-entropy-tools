# I05-35: fresh Möbius audit of the half-leaf pointwise resolvent route

Status: **DISPROVED** for the old universal pointwise claim
`Phi_r''(K;D)>0` for every strict half-leaf, every `r>0`, and every nonzero
real-symmetric physical direction. The disproof is an exact rational,
fully interior, true `K+tD` example reconstructed from all eight complete
events.

Status: **PROVED BY AUTHOR / PENDING EXTERNAL REVIEW** for the exact
eight-event reconstruction, the independent Schur-jet cross-check, and the
lossless two-side-plus-marginal identity recorded in `proof.md`.

This is not a Shannon-entropy counterexample. At the same exact
center/direction the occupied one-sided Hessian, the vacant one-sided
Hessian, and the full negative Shannon Hessian are all rigorously positive.

The branch starts from
`main@bcbf7016e2abc6401b66f39ac9202d235ee32fad`. It does not import or
execute the PR81 or PR104 checkers and does not change either source packet.
PR104 remains author work pending review. This packet is a fresh
same-author reconstruction, not an independent reviewer disposition.

## Exact obstruction

Use

```text
A=1/4, B=16/25, q=109/1000, qbar=1/1000,
K=[[1/2,0,1/4],
   [0,1/2,2/5],
   [1/4,2/5,277/500]],
D=[[-18,146,108],
   [146,-72,5],
   [108,5,40]],
r=1/50000.
```

All four parameters `A,B,q,qbar` are positive and sum to one, so both `K`
and `I-K` are strict. The checker constructs, for each
`x in {0,1}^3`,

```text
p_x(t)=(-1)^|Z_x| det(K+tD-I_Zx)
```

as an exact cubic polynomial. It sums the two third-bit outcomes to form
the four leaf marginals and then differentiates

```text
Phi_r(t)=sum_ij P_ij(t)^2/[p_ij1(t)+r P_ij(t)]
```

by exact rational quotient rules. The result is

```text
Phi_r''(0)=
-47488558049748267993080620088778228551027375300000000000
/2044542058422113103788725284171055940635901533282467
<0.
```

A second derivation obtains the four conditional jets from the actual
two-by-two Schur complements and checks exact equality with the Möbius
quotient jets. Thus the sign is not caused by a conditional-coordinate
or event-index convention.

## Entropy classification

For the four leaf states write `P_s=P(X_1,X_2=s)` and
`q_s=P(X_3=1|s)`. Exactly,

```text
H(K)=H(P)-G1-G0,
G1=sum_s P_s q_s log q_s,
G0=sum_s P_s(1-q_s)log(1-q_s).
```

At a half-leaf center `P_s=1/4`, and the complete leaf marginal contributes

```text
-H(P)''=4(D11^2+D22^2).
```

Consequently

```text
-H(K;D)''=4(D11^2+D22^2)+G1''+G0''.
```

The included fixed-term rational logarithm enclosures certify at the exact
witness:

```text
G1'' in
[46683.17721786154700699835814744593173463571879333569184,
 46683.17721786154700699835814744623988180436540262275381],

G0'' in
[12761038.58546859680575582197721374037172415087157141600,
 12761038.58546859680575582197721374329993214533615628276],

-H'' in
[12829753.76268645835276282033536118630345878659036475169,
 12829753.76268645835276282033536118953981394970155890552].
```

Therefore the exact result is a counterexample to the proposed
pointwise-in-`r` certificate only. It does not disprove integrated
one-sided convexity, conditional-entropy concavity, or full Shannon
concavity.

## Files

- `proof.md`: direct event derivation, exact formulas, and scope.
- `code/verify_mobius_obstruction.py`: standard-library-only exact
  reconstruction and rational log certificate.
- `output/verify_mobius_obstruction.txt`: literal output of the recorded run.
- `failure_ledger.md`: method and evidence boundaries.

Recorded run: Python 3.13.5, Linux x86_64, one process, no GPU, 32 fixed
atanh terms, about 0.66 seconds wall time and 93,608 KiB peak RSS. There
was one successful mathematical run after the output was expanded to print
all eight event polynomials. No search, interval subdivision, precision
escalation, PR81/104 replay, or computation budget was used.

## Continuing target

The pointwise resolvent route is abandoned. Work continues in this same
task on the exact one-sided power-perspective family and on direct
two-side-plus-marginal Schur control. No universal half-leaf theorem,
unequal-leaf theorem, general real three-point theorem, or novelty claim is
made by this checkpoint.
