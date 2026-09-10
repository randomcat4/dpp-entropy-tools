# I05-31 local contract — exact joint Fisher/acceleration certificate at alpha=1/10

Status: **FROZEN COMPUTATION CONTRACT; NOT YET A CERTIFICATE.** This contract does not reuse any PR95/PR97/PR102 or earlier PR116 computation budget. It is written because a naive global common-denominator expansion plus adaptive three-variable Bernstein subdivision may exceed one hour. The analytic work continues separately in the same task.

## Mathematical input

Use only the thirteen exact generic likelihood types and original complete-event weights in `TWO_PARAMETER_ALPHA01_CHECKPOINT.md`. Set

`alpha=1/10`, `0<=beta<=1`, `s=t^2`, `0<=s<=1`, `0<=u<=1`,

`q_i=1-a_i s+b_i s^2`,

`v_i=a_i-2s b_i`, `z_i=(a_i-sb_i)(a_i-6sb_i)`,

`d_i=(1-u)+u q_i`.

The target is the pointwise joint integrand

`J(beta,s,u)=sum_i W_i [4v_i^2/d_i^2+2z_i/d_i]`.

On the strict physical domain all `d_i` are positive. A negative `J` point would not by itself be an entropy counterexample; it would next require the `u` integral and the full curvature to be evaluated.

## Exact algorithm

1. Parse the thirteen rational `W_i,q_i` expressions literally from the frozen table. Reconstruct `a_i,b_i` by coefficient extraction and check `sum W_i=1`, `sum W_i a_i=sum W_i b_i=0`.
2. Independently reconstruct the 64 signed complete-event determinants for three exact interior beta values and compare their grouped `(W,a,b)` data with the table. This is an input guard, not a replacement for independent review.
3. Prove every factor used to clear denominators is positive on the requested open domain. Do not insert a numerical probability floor.
4. Put `delta=1-s`, `eta=1-u`. Form the exact reduced numerator after multiplication by the product of the distinct positive `d_i^2` and by the positive marginal denominator factors. Remove only polynomial factors proved nonnegative by exact division.
5. Cover the regular region by exact tensor Bernstein form. The initial regular boxes are
   - `eta in [1/16,1]`, already covered more strongly by the existing positive-acceleration certificate and used only as a cross-check;
   - `eta in [0,1/16]`, split adaptively in `(beta,delta,eta)`.
6. Resolve the singular corner with two projective charts rather than arbitrarily deep dyadic subdivision:
   - chart A, `eta<=delta`: substitute `eta=delta y`, `0<=y<=1`;
   - chart B, `delta<=eta`: substitute `delta=eta y`, `0<=y<=1`;
   and, if the double-root scale remains unresolved, split chart A once more into `eta=delta^2 y` and `delta^2=eta y`.
7. On every rational box, convert the exact multivariate polynomial to its full tensor Bernstein basis. A box is certified only if every coefficient is nonnegative and at least one coefficient or a separately proved factor gives strict positivity on the physical interior.
8. If a box has a negative Bernstein coefficient, subdivide its longest normalized side. A negative coefficient is not a counterexample. Stop with a candidate only after exact rational evaluation of the original un-cleared `J` gives `J<0` at a rational interior point.
9. For any exact negative `J` point, immediately evaluate
   `Gamma=int_0^1 J du`
   by directed rational logarithm enclosures and separately reconstruct the complete Fisher and acceleration sums before assigning any entropy status.

## Arithmetic and error certificate

All polynomial, determinant, subdivision and Bernstein arithmetic is over exact integers/rationals. Logarithms are needed only after an exact negative joint-integrand witness and must use a directed `atanh` expansion with an explicit geometric tail. Floating point may be printed for navigation but may not decide a sign.

The retained certificate must contain: the exact input table; reduced numerator multidegree and term count; every terminal rational box; its multidegree and minimum Bernstein coefficient; removed factors and exact quotients; any projective-chart factors; total check count; and literal stdout/stderr.

## Resource envelope

- one process and one CPU thread;
- no GPU;
- at most 8 GiB address space;
- absolute wall limit 7200 seconds;
- Python 3 with SymPy allowed, but no optimization-disabled assertions for sign gates.

## Stop and recovery contract

Stop at the first of: an input mismatch, failed exact division, a rational point with original `J<0`, address-space exhaustion, nonzero exit, or the absolute deadline. Do not alter inputs and rerun under the same record. Persist the pending-box priority queue, exact chart identifier, completed terminal boxes and command line every 300 seconds. A resumed run starts from that immutable queue under a new run identifier and reports cumulative CPU, peak memory and wall time. No earlier budget is reset or silently enlarged.

A completed run remains author machine evidence pending independent source/arithmetic review.