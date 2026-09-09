# Independent r=0 chain: frozen contract

Source main: `9dcb6e9079ca57f94e0e30d63161cda89ca61fae`.
Request: issue52 comment `5602242678`. This is a new authorized allocation,
not a continuation of the expired PR55 execution window.

Prove or strictly refute the recorded chain for every
`|mu|<1, |nu|<1, 0<u<1`, with `r=0`. Begin from the displayed four-by-four
Schur formula in the frozen STRUCTURE source. Preserve all six original
fixed physical directions in the resulting M assertion. General r and
Lambda-nonzero work are outside this unit.

The new implementation must construct Rstar from its analytic ingredients,
compute its determinant in exact rational/polynomial arithmetic, extract P
using the proposed identity
`det Rstar=(1-mu^2)^2(1-nu^2)^2 P/[2(1-u^4)^5]`, and build the integer
positive-orthant polynomial Q using
`mu=(X-1)/(X+1), nu=(Y-1)/(Y+1), u=U/(1+U)`.
Save and verify every identity and every coefficient. The archived P and Q
are comparison targets only after independent construction; importing an old
checker or using old matrix strings to construct the new matrix is excluded.

A successful certificate also needs all domain and denominator signs, the
positive seed, nonvanishing, continuity, connectedness and inertia argument.
The old FIRST INCOMPLETE record stays unchanged. A new first acceptance must
come from a fresh nonauthor reviewer; C3 alone schedules the independent
second after the first passes and alone integrates main.

The initial budget is one live arithmetic process, one CPU thread, at most
16 GiB, no GPU, and one total 2700-second wall window from the first new
arithmetic launch. Author and any first-review arithmetic share that absolute
window; preparation and purely analytic review are recorded separately.
Do not spend the window replaying the old eight-event derivation. Save
checkpoints after every completed layer and enforce the deadline externally.
Stop arithmetic on successful completion, a strict mismatch or the deadline.
No automatic full-r expansion, resource increase or second window.

The exact source, command, PID, start, absolute deadline, environment,
stdout/stderr and exit status must be preserved without publishing private
connection data. Before launching or resuming, check that prior owned PIDs
have exited. No global software changes and no access to `C:\canglan\`.
