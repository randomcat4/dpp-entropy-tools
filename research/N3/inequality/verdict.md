# First-unit verdict

## Status

`INCOMPLETE` for the frozen N3 inequality.

`PROVED_HERE` for the slice Fisher covariance lemma.

## What was proved

The new lemma proves an unconditional exact decomposition

```text
F(D,D) = Q_k(D) + R_k(D),        R_k(D) >= 0,
```

and therefore the lower bound

```text
F(D,D) >= Q_k(D)
```

for every strict real symmetric three-point kernel `K`, every real symmetric
direction `D`, and every coordinate `k`.  The lower bound keeps only:

1. the Fisher information of the marginal `X_k`;
2. the centered determinant score in the slice `X_k=0`;
3. the centered determinant score in the slice `X_k=1`.

The two slice determinants are exactly the two DPP conditional covariance
squares from the frozen theorem.  Thus the lemma uses the actual eight-event
map and not an artificial independent choice of `F` and `N`.

The lemma is strictly weaker than the full Fisher form because each two by
two slice discards all conditional score components orthogonal to the
centered determinant gradient.  Equality in a slice would require the
centered score to be proportional to that one gradient; generic directions
do not satisfy this.

## Failed closure

Under the frozen trace normalisation,

```text
tr(N^-1 D)=1,
```

the target is equivalent to

```text
F(D,D) >= 2 tr(N adj D).
```

The first hoped-for closure was

```text
max_k Q_k(D) >= 2 tr(N adj D)
```

for all directions.  This is false.  The main instance reported a strict
certificate; this route locally rechecked the same clean rational point in
floating arithmetic:

```text
K = (1/100) [[30,29,15],[29,33,10],[15,10,16]],
D = diag(1,1,1/3).
```

The local one-thread check gave:

```text
eig(K) = (0.00861822, 0.11469543, 0.66668635),
eig(I-K) = (0.33331365, 0.88530457, 0.99138178),
F = 37.94861242536174,
2 tr(N adj D) = 6.953325064724251,
B = F - 2 tr(N adj D) = 30.995287360637487,
Q_k = (5.041626538797038, 4.697085044513301, 0.9020682098293722),
max_k Q_k - 2 tr(N adj D) = -1.9116985259272132.
```

The rigorous interval certificate belongs to the main instance's frozen
artifact at commit `424b4efcec0052ad8d79ac71c69b334dcfb03bb8`; this author
unit only records an independent floating recheck and does not certify that
counterexample.

## Minimal remaining gap

The viable next statement is narrower:

```text
At a true trace-constrained minimising direction for
F(D,D)+det(N) tr(N^-1 D N^-1 D),
the slice scores Q_k must couple to the N-cofactor term strongly enough
to recover F(D,D) >= 2 tr(N adj D).
```

Equivalently, one needs either:

1. a proof only at the stationary optimal direction, using the linear system
   defining that direction; or
2. a kernel-dependent convex combination of the three `Q_k` that dominates
   the cofactor expression on the relevant constrained optimiser, not on all
   symmetric directions; or
3. a way to use the positive residual `R_k` from the exact decomposition when
   the covariance-score part `Q_k` is too small.

The present unit does not close either statement.  It supplies the exact
Fisher lower-bound lemma and identifies the false unrestricted closure.

## Boundary and premise checks

The proof assumes only strict positivity of the eight event probabilities,
which follows from `0<K<I`.  It covers noncommuting and indefinite symmetric
directions because the argument is a first-order Fisher metric statement on
the exact event probabilities.  It does not use disconnected limits or
`N^-1`, so singularity of `N` at disconnected points is irrelevant to the
lemma.

No stronger pointwise nonpositivity of individual cofactor pieces is used.
No artificial independent `F,N` pair is introduced.
