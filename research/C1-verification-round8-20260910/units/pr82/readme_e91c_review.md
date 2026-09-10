# PR82 README e91c delta-FIRST review

Verdict: **ACCEPTED_SCOPED for the README-only textual corrections**, with the original `p>4` theorem still **INCOMPLETE** and the unchanged successor p>8 material not upgraded by this patch.

## 1. Dobrushin source dependency and inherited-claim wording

README lines 17--25 now say the primary Dobrushin text is available, identify the applicability defect, and point directly to the printed-page locations for A1/A2, perturbation hypotheses, and the Banach formulation. This is the right source posture for a method checkpoint: the text no longer relies on an internal review addendum as evidence for the primary hypotheses.

README line 47 also fixes a scope problem. It says the internal inverse/two-leg/equilibrium/parity lemmas of PR66 are separate source claims and that this checkpoint neither repairs the external import nor enlarges their scope. That is acceptable: it preserves the source-only boundary and avoids converting prior review context into a proof premise.

Status: **ACCEPTED_SCOPED**.

## 2. Hamiltonian sign and Boolean Möbius convention

README lines 63--74 set up the finite positive definite L-ensemble identity
`\log det L_S=|S|\log gamma - sum_{k>=1} k^{-1} Tr(R_S^k)` with `rho<1`, so the trace expansion is available for each finite `S`.

README line 76 defines the Hamiltonian convention `H(S)=-log det L_S` and defines
`J_A=sum_{B subseteq A} (-1)^(|A|-|B|) H(B)`. Under the usual Boolean zeta/Möbius convention `H(S)=sum_{A subseteq S} J_A`, this means `J_A` is the coefficient in the Hamiltonian, not in the log weight.

For `|A|>=2`, the linear `|S| log gamma` part cancels under Möbius inversion. Since `H=-log det`, the remaining trace-series part enters with positive sign in `H`. The displayed expression in README lines 79--85 is therefore correct for the Hamiltonian coefficient, and README line 87 correctly says the corresponding coefficient of `log det L_S` is `-J_A`.

Status: **ACCEPTED_SCOPED**.

## 3. Grouped closed-walk convergence and what it does not prove

README lines 76--87 now use the right convergence level. The equality is not being used as an absolutely summable expansion over individual closed walks across all supports. Instead, for each finite `A`, the walks at each fixed `k` are grouped first, and the resulting scalar series is a finite Boolean Möbius combination of the absolutely convergent finite trace series.

This wording also preserves the key unresolved point. README line 87 explicitly declines to claim absolute summability after taking absolute values of individual walks or all supports, and README lines 91--96 state that Dobrushin A2 still needs an absolute weighted sum of `|J_A|`. That is the correct distinction: the finite determinant algebra avoids a naive literal Boolean expansion loss, but it does not yet give the infinite-volume Dobrushin norm.

Status: **ACCEPTED_SCOPED**, with the A2 bridge still **INCOMPLETE**.

## 4. Corrected quartic target

README lines 188--200 replace the old informal concavity target with the corrected functional
`F(t)=h(c+tg)+alpha t^4` and `H(t)=h(c+tg)`. The stated assumptions are exactly the conditional ones needed for this local calculus step: `H` is even and `C^4` near zero, `H''(0)=0`, and the strict corrected quartic inequality is
`H^{(4)}(0)/24 + alpha < 0`.

Under those assumptions, `H''(t)=(1/2)H^{(4)}(0)t^2+o(t^2)`, while the added `alpha t^4` term contributes `12 alpha t^2` to `F''(t)`. README line 197 therefore has the correct coefficient,
`F''(t)=((1/2)H^{(4)}(0)+12 alpha)t^2+o(t^2)`.
The strict inequality above makes that coefficient negative, so line 200 correctly concludes strict concavity for sufficiently small nonzero `t`, with `F''(0)=0`, conditional on the stated response hypotheses.

This is only a calculus correction. It does not supply the missing `C^4` response theorem or uniform remainder; README lines 202--210 and 224--228 still mark that gap as pending.

Status: **ACCEPTED_SCOPED**.

## 5. Original `p>4` theorem and relation to successor p>8 files

The README continues to state the right nonclaim. Lines 3 and 214 say the original `p>4` theorem is not repaired. Lines 91--96 keep the finite determinant route as a candidate rather than a theorem. Lines 210 and 224--228 keep the response theorem and A1/A2 bridges open.

This e91c delta changes only the old README. It does not change `c4_response_p8.md` or `c4_response_p8_correction.md`, and it cannot by itself close the successor p>8 theorem. Acceptance here is limited to the README's corrected wording and local algebra/calculus statements.

Status: **ACCEPTED_SCOPED for README text; INCOMPLETE for the original theorem and unchanged bridges**.

## Final status buckets

### ACCEPTED_SCOPED

* Direct primary-source wording for Dobrushin hypotheses: README lines 17--25.
* Separation of PR66 internal claims from the external import: README line 47.
* Hamiltonian sign and Boolean Möbius convention: README lines 76--87.
* Grouped closed-walk convergence caveat: README line 87, with the unresolved norm issue at lines 91--96.
* Corrected quartic target for `F(t)=h(c+tg)+alpha t^4`: README lines 188--200.
* Preservation of the open `p>4` status: README lines 3, 210, and 214--228.

### INCOMPLETE

* Original arbitrary-center `p>4` PR66 theorem.
* Infinite-volume DPP null-state interaction and Dobrushin A2 absolute weighted norm.
* A genuinely applicable `C^4` response theorem with the needed uniform remainder.
* Any theorem-level acceptance of the unchanged successor p>8 files.

### NEEDS_FIX

None for this exact README-only delta.

### PENDING_C2

None. No finite numerical comparison or arithmetic execution is needed for this delta.
