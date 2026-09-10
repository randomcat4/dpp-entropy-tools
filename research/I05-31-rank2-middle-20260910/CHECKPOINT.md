# I05-31 checkpoint — compact-middle rank-two curvature

Status: **AUTHOR DERIVATION / PENDING_REVIEW**. This checkpoint is intentionally small and is uploaded before continuing the same research task. It does not alter PR94/95/97/102 and does not inherit their pending reviews.

All statements concern complete-configuration Shannon entropy of a real DPP under a genuinely affine physical-kernel path

`K(t)=[[A,tB],[tB^T,C]]`,

with fixed strict marginal blocks `0<A<I`, `0<C<I`, real `rank(B)<=2`, and natural logarithms. No spectral entropy, observed-coordinate rotation, affine-L path, event deletion, or Fisher-only proxy is used.

## 1. Frozen prior boundary

The working comparison set is PR94, PR95, PR97 and PR102.

- PR94 gives an exact local-channel lift of the accepted `m x 2` radial theorem to a structured higher-dimensional family; it does not cover arbitrary dense rank-two cross blocks.
- PR95 closes one dense correlated 3+3 maximal chord and an open moving-simple-endpoint class; its independent finite/source reconstruction is reported separately, while mathematical SECOND remains pending.
- PR97 exhibits a strong rank-four physical direction with positive complete acceleration in the middle, but proves full Fisher dominance on one chord and a one-parameter strength family.
- PR102 proves author-side endpoint Fisher dominance for arbitrary finite affine DPP boundary approach, including repeated and simultaneous 0/1 activity, and gives two dense rank-two whole chords. Therefore the unresolved place is a compact strict interior away from all legal endpoints.

## 2. Exact rank-two event formula retained

For a complete left/right event pair `(S,T)` let

`mu_ST=p_A(S)p_C(T)>0`, `s=t^2`,

and write the exact complete-event likelihood ratio

`q_ST(s)=p_{K(t)}(S,T)/mu_ST=1-a_ST s+b_ST s^2`.

For rank at most two this follows from the 2x2 Schur determinant identity and is an identity for every complete event. The normalization identities are

`E_mu a=E_mu b=0`.

Define

`v=a-2sb`, `z=(a-sb)(a-6sb)`,

`lambda(q)=log(q)/(q-1)` with `lambda(1)=1`.

On every strict legal point,

`Gamma(s):=-H''(t)/t^2 = E_mu[4 v^2/q + 2 z lambda(q)]`.

This is the full complete-law curvature: the first term is the complete Fisher contribution and the second is the full affine-acceleration contribution after the exact cancellation identities. In particular `lambda(q)>0` for every `q>0`.

## 3. New checkpoint lemma: an eventwise six-slope cone is a whole-interval certificate

**Lemma (author proof, pending review).** Fix a squared-parameter interval `0<=s<=S` contained in the strict legal region. If every complete event satisfies

`(a_ST-s b_ST)(a_ST-6s b_ST) >= 0` for every `s in [0,S]`,

then

`H''(t)<=0` for every `|t|<=sqrt(S)`.

No likelihood lower bound is required and no acceleration term is discarded.

**Proof.** In the exact formula above, `4v^2/q>=0`, `lambda(q)>0`, and the hypothesis makes every logarithmic acceleration summand `2 z lambda(q)` nonnegative. Hence `Gamma(s)>=0`, i.e. `H''(t)<=0` for `t!=0`. At `t=0`, the analytic limit is `Gamma(0)=6 E_mu a^2>=0`, so the conclusion extends through zero. QED.

For exact coefficient checking on a whole interval, no temporal mesh is needed. Since

`z(s)=(a-bs)(a-6bs)`,

the hypothesis is guaranteed event-by-event by the following finite coefficient test:

- `ab<=0`; or
- `ab>0` and `S <= a/(6b)`.

Indeed, when `ab<=0` both affine factors retain the same sign for `s>=0`; when `ab>0`, the first possible sign separation begins at the smaller positive root `a/(6b)`.

This criterion is only sufficient. Failure of the cone is a method failure, not an entropy counterexample. PR97 already shows that positive/adverse acceleration can occur while the full curvature remains negative.

## 4. Immediate research target after this checkpoint

The next step is not to search near an endpoint. It is to test whether a natural, fully dense correlated rank-two family outside PR94's grouped-channel image can be proved to stay in the six-slope cone on its complete maximal chord, or, failing that, to identify the smallest exact collection of cone-violating event types and prove a compensating Fisher inequality for them.

The primary analytic candidate is the simultaneous-permutation 3+3 family

`A=alpha P+beta Q`, `C=gamma P+delta Q`, `B=u P`,

where `Q=11^T/3`, `P=I-Q`, with strict scalar parameters and `u!=0`. Here `B` is rank two and dense in the observed coordinates, both marginal blocks are internally correlated when `alpha!=beta` and `gamma!=delta`, and no pair of rows or columns of `B` is proportional. The family contains substantial parameter freedom, not merely a coefficient box around the PR102 displayed example. The continuation will derive its complete-event types symbolically and determine whether a parameter region admits a closed whole-chord proof.

No computation was started for this checkpoint.