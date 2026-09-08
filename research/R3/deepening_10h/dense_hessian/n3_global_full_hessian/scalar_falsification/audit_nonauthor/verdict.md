# D10-U10c `scalar_falsification` fresh audit

STATUS: CRITICAL_GAPS.

This is still only a finite SCOUT audit.  No theorem is certified and no global
claim `rho(K)<=1` is proved.

There is also a provenance limitation: this same conversation context authored
the U10c scout.  Because the task forbids spawning a fresh agent, this report is
an independent reimplementation check in `audit_nonauthor/`, but it should not
be treated as final non-author certification.

## Main finding

The author script has a Decimal first-jet bug:

```text
rho_scalar_search.py line 734:
g0 = [-1 + gq12[i] + gq13[i] + gq23[i] - gr[i] for i in range(6)]
```

For the empty atom

```text
p0 = 1-x-y-z+q12+q13+q23-r,
```

the derivative of `1-x-y-z` is `(-1,-1,-1,0,0,0)`, not `(-1,-1,-1,-1,-1,-1)`.
Thus the three off-diagonal coordinates in the Decimal path are wrong.  The
float path uses the correct base vector, but all published Decimal rho
rechecks/candidates produced through `atoms_and_grads_dec` are numerically
unreliable as written.

This is a critical gap for the reported high-precision candidate values, not a
positive-curvature counterexample.

## Ledger denominator audit

The JSON bookkeeping itself is internally consistent:

```text
attempted_float_total = 38436
accepted_float_total  = 22023
route attempted sums  = 38436
route accepted sums   = 22023
```

Each route also satisfies `attempted = accepted + rejected`.

Small-atom coverage at threshold `1e-8` is present for all eight atom names:

```text
p0: 2869, p1: 306, p2: 231, p3: 214,
p12: 530, p13: 551, p23: 615, p123: 4299.
```

The frozen artifacts report `decimal_positive_count=0`, and
`positive_candidates_rho_gt_1` is an empty list.  Since the Decimal formula was
buggy, that count is not accepted merely by repetition; I recomputed the
reconstructible Decimal families below with the corrected first jets.

## Independent corrected high-precision recomputations

The audit script independently reconstructs:

- exact atoms by Möbius/principal-minor formulas;
- correct first jets in `(11,22,33,12,13,23)`;
- Fisher, `N`, `A`, `eta`, and `rho=det(N)eta^T A^{-1}eta`;
- Decimal LDL pivots for `K`, `I-K`, and `N`.

### Best equal-rate point

Author stored:

```text
theta=0.99, epsilon=10^-96, rates=[1,1], complement=False
author rho = 0.99854837056755878367556202099985504244...
```

Corrected fresh recomputation:

```text
rho       = 0.99509994460201969229112579538559592802...
1-rho     = 0.00490005539798030770887420461440407197...
min atom  = p123 = 9.9e-193
K>0       = PASS
I-K>0     = PASS
N>0       = PASS
```

So the point remains subunit, but the published Decimal value is off by about
`-0.00344842596553909`.

### Best unequal-rate point from author near-threshold list

Author stored:

```text
theta=0.5, epsilon=10^-96, rates=[2,3], complement=False
author rho = 0.99557538648114883622794165905473993436...
```

Corrected fresh recomputation:

```text
rho       = 0.99325250311940130939025336008385825478...
1-rho     = 0.00674749688059869060974663991614174521...
min atom  = p123 = 5e-481
K>0       = PASS
I-K>0     = PASS
N>0       = PASS
```

Again subunit, but the author Decimal value is materially wrong.

The full corrected reconstruction of the 280 rank-one/rate Decimal grid finds
no `rho>1`.  Its best value is the corrected equal-rate point above:

```text
best corrected boundary rho = 0.99509994460201969229112579538559592802...
```

The best corrected unequal-rate grid value is also subunit:

```text
best corrected unequal rho = 0.99325250311940130939025336008385825478...
```

### Float pseudo-near-threshold point

The author float stage reported:

```text
rho_float = 0.9999999999875521
```

and the author Decimal recheck recorded:

```text
rho = 0.54173713302972814995716038831335082062...
```

Corrected fresh recomputation of the stored `K` gives:

```text
rho       = 0.50000000000000000000041666666666666662...
1-rho     = 0.49999999999999999999958333333333333337...
min atom  = p1 = 0.0072
K>0       = PASS
I-K>0     = PASS
N>0       = PASS
```

The qualitative diagnosis remains correct: this is a near `Lambda=0` /
near-disconnected conditioning hazard, not a candidate.  The smallest `N` LDL
pivot is about `1e-20`, so ordinary float rho is not a reliable gate there.

### Corrected `Lambda≈0` path grid

The audit reconstructed all `150` Decimal-only near-disconnected path probes.
No `rho>1` occurred.  The best corrected path value is only

```text
rho = 0.50005480933937654719295834657720265461...
```

## Credible positive-candidate count

Corrected recomputation covered:

```text
280 rank-one/rate Decimal boundary probes
150 Lambda≈0 path probes
the required best equal-rate, best unequal-rate, and float pseudo-threshold points
```

Credible `rho>1` count in this corrected/reconstructible set:

```text
0
```

The published float ledger has no stored `rho>1` and the positive-candidate
list is empty.  However, because the author Decimal implementation is wrong,
the original high-precision values and “best Decimal” rankings should be
replaced or regenerated before any later audit relies on them.

## Layered conclusion

- Formula target and finite-SCOUT framing: CORRECT.
- Route count bookkeeping and small-atom coverage bookkeeping: CORRECT.
- Author Decimal first jets: CRITICAL GAP at `rho_scalar_search.py:734`.
- Published Decimal best equal/unequal/pseudo-threshold rho values: INCORRECT.
- Corrected reconstructible Decimal scout: no credible `rho>1` found.
- Global `rho(K)<=1`: still OPEN / INCOMPLETE.

Recommended repair: patch the Decimal `p0` gradient to use
`[-1,-1,-1,0,0,0]`, rerun the U10c scout ledger, preserve the old ledger as
failed-version evidence, and then send the regenerated artifacts to a truly
fresh non-author reviewer.
