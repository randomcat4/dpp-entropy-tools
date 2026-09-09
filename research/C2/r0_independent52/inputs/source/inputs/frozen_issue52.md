Continuation of #20 and author PR #51. **REQUESTED, not running; no server job or result is claimed.** This is a new precise computation after the first PR checkpoint. C2/Codex may implement it independently. No credentials or server details are requested.

## Exact target and why this is not the half-filled result

Let mu,nu,r in (-1,1), u in (0,1), a=(1+r)/2, b=(1-r)/2, v=(1-mu^2)/4, w=(1-nu^2)/4. Put x=(1+mu)/2, y=(1+nu)/2 and

`K(u)=[[x,0,u sqrt(a v)],[0,y,u sqrt(b w)],[u sqrt(a v),u sqrt(b w),1/2-u^2(a mu+b nu)/2]]`.

All eight events are positive and K,I-K are positive definite: Schur complements are `(1-u^2)/2` for the appropriate extreme conditional events. This family has the complete-event triple log coefficient Lambda=0. It includes arbitrary leaf biases, unlike the proved half-filled theorem in #51.

Use the fixed-in-u, invertible direction congruence

`D11=v A, D22=w B, D33=C, D12=sqrt(a b v w) E, D13=sqrt(a v) F, D23=sqrt(b w) G`.

The six direction variables are `(A,B,C,E,F,G)`. These letters are direction coordinates, not kernel parameters. Define `M(mu,nu,r,u)=d/du[-Hess H(K(u))]` in these FIXED direction coordinates. The assertion to test is `M positive definite` for the whole open parameter domain. It is stronger than the desired entropy sign, so a counterexample to M is **not** automatically an entropy counterexample.

## Complete rational construction; no square roots in the computational input

Set `s=u^2`, `J=1-u^4`, `L=1-r^2 u^4`.

For i,j in {0,1}, let

`Pij=(1+(2i-1)mu)(1+(2j-1)nu)/4`,
`e=i-(1+mu)/2`, `f=j-(1+nu)/2`,
`qij=(u^2 a e^2, u^2 b f^2, 1, 2u^2 a b e f, -2u a e, -2u b f)^T`,
`denij=J if i=j, otherwise L`.

The COMPLETE conditional Fisher matrix is

`Fmat = sum_(i,j) 4 Pij qij qij^T / denij`.

The omitted marginal Fisher is `diag(v,w,0,0,0,0)`, constant in u, so its derivative is exactly zero (it is not removed from the entropy Hessian or subsequent integration).

Define

`n1=4u(1/J-r/L)`, `n2=4u(1/J+r/L)`, `n3=4u^3(1-r^2)/(J L)`.

The symmetric matrix Q has only these nonzero entries (indices 1 through 6):

`Q12=-n3 v w`, `Q13=-n2 v`, `Q23=-n1 w`,
`Q44=2n3 a b v w`, `Q55=2n2 a v`, `Q66=2n1 b w`.

The exact input is `M = derivative_u(Fmat)+Q`. All coefficients are rational functions of mu,nu,r,u. Derive this independently from all eight inclusion-exclusion atoms before sign work. The initial entropy-Hessian matrix at u=0 is `diag(v,w,4,0,0,0)`, so M>0 would prove the full Hessian at all these centers by integration in u. Inertia continuation in the three shape parameters is admissible only after an exact global nonvanishing determinant certificate.

## Tasks, algorithm and acceptance gate

1. Reconstruct the complete event first/second jets; verify this M formula symbolically or with exact coefficient identities.
2. Clear known positive denominators and try fraction-free/domain arithmetic for det M and a positive seed. Start with r=0, then full r; retain factors and degree bounds. If a positive-coefficient, Bernstein, SOS, or other global polynomial certificate is found, state the exact transformed compact domain and how its open boundaries are treated. Finite sampling is not a global certificate.
3. A floating scout may locate a negative direction. Reconstruct rational mu,nu,r,u and a rational direction vector zeta, then prove `zeta^T M zeta<0` by exact fractions. This rejects only radial Hessian monotonicity. Only if the actual entropy Hessian also becomes negative for -H'' should the original kernel/direction be frozen as an entropy candidate, with exact legality and a genuine positive Jensen interval certificate.

## Resource and stopping contract

The full multivariate determinant/positivity elimination could exceed 60 minutes, so it is handed off now rather than run in the web session. Initial independent unit: one CPU process, at most 16 GiB, no GPU, 45-minute wall ceiling. Stop at a valid exact global certificate, an exact rational obstruction, or the ceiling. Save completed polynomial factors/checkpoints; do not repeat finished elimination without inspecting them. Any larger job requires a separately recorded plan, not silent budget expansion. A timed-out local attempt is not evidence for or against the assertion.

Suggested interface for a new independent implementation:

`python verify_i05_22_lambda_zero.py --mode derive --output inputs/lambda_zero_M.json`
`python verify_i05_22_lambda_zero.py --mode factor --case r0 --wall-seconds 2700`
`python verify_i05_22_lambda_zero.py --mode factor --case full --wall-seconds 2700`

These are requested interface names, **not existing repository scripts**. The complete formulas above are the source input. Pin dependency versions; retain stdout/stderr, exit status, exact objects, degree bounds, and sign/error certificate. Do not claim a floating eigenvalue or author replay as independent review.

## Local exploration already done and its limit

A bounded 1500-point double-precision scout (seed 22051; x,y uniform [.02,.98], r uniform [-.95,.95], u uniform [.1,.98]) found no negative eigenvalue of the analytic derivative. This is SCOUT only. A SymPy 1.14 construction took about 22 seconds; an r=0 determinant expansion did not finish before the local 35-second process timeout. No unbounded process is left running, no determinant result was obtained, and no global sign is inferred.

I05-22 continues analytic work without assuming any outcome from this request. Ordinary results/review notes belong on this issue and #51, not cross-thread notifications.
