# PR55 structure delta closure

New frozen head: `4bd0d615f6cfc44aea537ccfdc62cd8420b2d3ea`

Reviewed source file:

- `research/C2/lambda_zero52/structure/STRUCTURE.md`

New source file hash:

- Git blob SHA-1: `36735e3a3d49f4c7ef732303e7615c943cc56175`
- SHA-256: `08E83B179646A969C031597D23A2B66457996FB35B4074768317DE382AF60DDC`

Delta verdict: `ACCEPTED_SCOPED`.

I compared this file against the previously reviewed PR55 snapshot at head `de802933899b6a02e7c4fb8afc79e0b15564caba`. The textual delta is limited to:

1. A clarification of the verified Gram statement:
   - old: `Fmat = 4*T^T G T` at the quadratic-form level;
   - new: `zeta^T Fmat zeta = 4*y^T G y`;
   - source: `STRUCTURE.md:293-302`.

2. A new determinant-bookkeeping supplement:
   - defines `T` as the six-by-six forward map from `zeta=(alpha,beta,gamma,eta,xi,omega)` to `x=(alpha,beta,m,p,q,h)`;
   - states the orientation `M_red = T^{-T} M T^{-1}` and `M = T^T M_red T`;
   - gives `det T = 8*u^4*a^2*b^2`;
   - gives `det M = 16*n1*n2*u^12*a^5*b^5*v*w*det Rstar`;
   - states that all prefactors are positive on the open domain and that this does not prove `det Rstar` is nonzero;
   - source: `STRUCTURE.md:312-343`.

No other formula, scope, algorithm, or status text in `structure/STRUCTURE.md` changed relative to the reviewed `de802933899b6a02e7c4fb8afc79e0b15564caba` snapshot.

The new paragraph implements the requested correction from the second audit. The orientation is correct: reduced coordinates satisfy `x=T zeta`, so the reduced matrix is `M_red=T^{-T}MT^{-1}` and therefore `det M=(det T)^2 det M_red`. The determinant factor then follows from `det M_red=d_alpha*d_beta*det Rstar`, `d_alpha=n2*a*u^2*v/2`, and `d_beta=n1*b*u^2*w/2`.

I did not inspect or rely on any linked prior review or first-review artifact. No arithmetic, symbolic elimination, scout computation, or C2 job was run.
