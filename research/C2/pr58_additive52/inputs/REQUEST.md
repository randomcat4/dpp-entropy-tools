C3 records a **separate finite witness unit** for the new PR58 joint-additive addendum. This does not extend either the original PR58 compact-corridor contract or the closed PR60 full-r contract. C2 remains the only arithmetic owner; execute serially after existing owned arithmetic stops.

Frozen numerical source: PR58 head `a4f05cc962985015b71635bf633acce9dfe76866`, `research/I05-23-middle-20260909/ADDENDUM_JOINT_ADDITIVE.md`, section 3, with the code/output treated only as later comparison targets. Current descendant `5ab3cae1c49da8334057596f46a4bd8fc449b98c` retains every fixture and numeric statement byte-for-byte; its changes are the two original prose repairs and the single normal-operator domain correction. Never import or execute the author checker.

Exact input matrices and point:

```text
A = [[219/500,-47/1000,73/1000],[-47/1000,461/1000,23/1000],[73/1000,23/1000,43/100]]
C = [[231/500,1/50,-49/1000],[1/50,43/100,11/200],[-49/1000,11/200,3/5]]
U = [[7/40,-22/125],[339/1000,13/250],[229/500,-231/500]]
V = [[141/200,981/1000],[-343/1000,113/250],[187/250,577/1000]]
B = U V^T; s=t^2=9/10.
dual table c_ST, rows/columns in the author's mask order 0,...,7:
[[-20,-14,-10,9,-26,-9,15,55],
 [-15,-8,-9,3,-13,4,8,30],
 [-11,-5,35,16,-21,-23,28,-19],
 [2,1,20,7,-7,-17,9,-15],
 [-10,9,-13,-10,14,44,-17,-17],
 [-8,7,-10,-8,12,33,-13,-13],
 [36,6,-7,-10,24,-18,-17,-14],
 [26,4,-6,-7,17,-14,-13,-7]]
```

Independently reconstruct all 64 complete events, product marginals, and the quadratic likelihood `q_s=1-sa+s^2b`. Check strict legality using exact Schur/complement inequalities at rational s (no floating square root), strict marginal kernels, dense rank-two B, total probability, and both fixed marginals. Verify the exact conditional a/b cancellations and every dual row/column sum. Keep all 64 rows in the output.

Compute `u=q-1`, `y=s^2 b`, `Phi=4u^2/q+2u log q`, `psi=8u/q+10log q`, `P0=E_mu Phi`, `A2=4E_mu[y^2/q]`, `W=E_mu[y psi]`, the dual bound `L=(sum c psi)^2/(sum c^2/P_s)`, and threshold `T=4(P0+A2)^2/A2`. Retain full Fisher/acceleration terms and independently compare direct differentiated entropy/MI to `t^2 I''=P0+A2+W`.

Use exact rational atanh/log2 series with proved rational tails, outward fraction endpoints, and target enclosure width below `1e-18` for the reported scalars; refine within the same deadline only if necessary for the displayed inequalities. Check both qualitative signs `L>T`, `W<0`, `t^2 I''>0` and the **literal decimal bounds** in equations (3.4)-(3.7). A rounded display can fail even if the qualitative theorem survives: report the first exact mismatch and preserve it; do not silently replace a failed decimal or infer strictness from a floating printout. A finite witness here would refute necessity of this sufficient condition while retaining negative actual entropy curvature. It is not an entropy-concavity counterexample.

New resource contract: **at most 600 seconds total wall clock from this unit's first arithmetic launch, one live process/CPU/thread, 16 GiB, no GPU**, including repairs. Freeze the new independent code before launch; record PID, start, absolute deadline, source hash, outputs, and actual exit. Stop on success, first exact mismatch or deadline. No parameter scan, original-corridor expansion, issue63 whole-chord computation, overlap or silent extension. If the budget is insufficient, return the last completed layer and request a new explicit contract before restarting.

Status: **REQUESTED**. No arithmetic has been launched by C3. C1 must read the completed raw evidence before closing this finite-witness FIRST; C3 then applies its own second gate. The analytical projection and normal equations have separate source-review gates.
