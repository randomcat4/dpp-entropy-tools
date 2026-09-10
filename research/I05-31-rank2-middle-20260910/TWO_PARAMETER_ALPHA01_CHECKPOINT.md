# I05-31 continuation — alpha=1/10, variable beta exact 13-type checkpoint

Status: **AUTHOR DERIVATION / PENDING_REVIEW; novelty NOT_ASSESSED.** This is a checkpoint before the sign proof is completed. It concerns complete-configuration Shannon entropy of the true physical affine kernel and retains every event, Fisher term and acceleration term. It does not inherit PR94/95/97/102 review and does not use endpoint asymptotics to infer a middle sign.

Put

`Q=11^T/3`, `P=I_3-Q`, `alpha=1/10`, `rho=sqrt(alpha(1-alpha))=3/10`,

`A=alpha P+beta Q`, `C=I-A`, `B=rho P`, `0<beta<1`,

and

`K_beta(t)=[[A,tB],[tB,C]]`.

On each of the two P modes the physical 2-by-2 block is `[[1/10,3t/10],[3t/10,9/10]]`; on the Q mode the two blocks are the uncoupled scalars `beta,1-beta`. Therefore the exact maximal legal chord is `[-1,1]` for every `0<beta<1`; at either endpoint both `K` and `I-K` have nullity two. Spectral coordinates are used only for legality, not entropy.

For every one of the 64 observed complete events, with `s=t^2`,

`p_E(t)=mu_E q_E(s)`, `q_E=1-a_E s+b_E s^2`.

Symbolic signed-determinant reconstruction gives **13** generic likelihood types. The 11 types in `RESULT_EXCHANGEABLE.md` are the specialization `beta=1/3`, where two pairs coincide. The generic type table is:

| mult | total decoupled weight `W` | `q(s)` |
|---:|---|---|
| 6 | `(17 beta+1)^2/15000` | `[729 beta^2 s^2-18 beta^2 s+289 beta^2-486 beta s^2+252 beta s+34 beta+81 s^2+18 s+1]/(17 beta+1)^2` |
| 6 | `27(7 beta+2)^2/5000` | `[81 beta^2 s^2+478 beta^2 s+441 beta^2-108 beta s^2-344 beta s+252 beta+36 s^2+28 s+36]/[9(7 beta+2)^2]` |
| 3 | `(17 beta+1)^2/30000` | `(9s+1)[81 beta^2 s+289 beta^2-54 beta s+34 beta+9s+1]/(17 beta+1)^2` |
| 1 | `beta^2/10000` | `(9s+1)^2` |
| 6 | `729(1-beta)(7 beta+2)/5000` | `(s+9)[3 beta s+7 beta-2s+2]/[9(7 beta+2)]` |
| 3 | `27(7 beta+2)^2/10000` | `(s+9)[81 beta^2 s+49 beta^2-108 beta s+28 beta+36s+4]/[9(7 beta+2)^2]` |
| 1 | `6561(1-beta)^2/10000` | `(s+9)^2/81` |
| 6 | `9 beta(7 beta+2)/5000` | `(s-1)[27 beta s-7 beta-18s-2]/(7 beta+2)` |
| 2 | `81 beta(1-beta)/5000` | `(s-1)^2` |
| 12 | `3(7 beta+2)(17 beta+1)/2500` | `-[81 beta^2 s^2+338 beta^2 s-119 beta^2-81 beta s^2-178 beta s-41 beta+18s^2-16s-2]/[(7 beta+2)(17 beta+1)]` |
| 6 | `beta(17 beta+1)/5000` | `-(9s+1)[27 beta s-17 beta-9s-1]/(17 beta+1)` |
| 6 | `81(1-beta)(17 beta+1)/5000` | `-(s-1)[3 beta s+17 beta-s+1]/(17 beta+1)` |
| 6 | `3(7 beta+2)(17 beta+1)/5000` | `-(s-1)[81 beta^2 s+119 beta^2-81 beta s+41 beta+18s+2]/[(7 beta+2)(17 beta+1)]` |

The weights sum to one. Direct coefficient extraction also gives the complete normalization cancellations `sum W a=0` and `sum W b=0` identically in beta.

Hence the normalized exact curvature is still

`Gamma_beta(s)=-H''(t)/t^2=sum W[4(a-2sb)^2/q+2(a-sb)(a-6sb) lambda(q)]`,

`lambda(q)=log(q)/(q-1)` with `lambda(1)=1`.

A preliminary mechanism scan of this **new** beta family found no adverse total-acceleration point on a coarse compact grid; its observed minimum was positive and internal, near `beta≈0.35, s≈0.47`. This is explicitly **not a theorem or finite certificate** and is recorded only to choose the next analytic branch. The next step is an exact beta-uniform sign decomposition of the 13 acceleration types, followed by full Fisher if aggregate acceleration can become negative.
