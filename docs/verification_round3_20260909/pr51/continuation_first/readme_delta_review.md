# PR51 README delta first review

Reviewed head: `8b078ab834c46ce0c0e81967e3ada3fbbf542f1a`.

Reviewed source: `research/I05-22-missing-edge-20260909/README.md` only. This is an explicitly frozen README-only delta; I relied on the supplied exact compare that the four earlier PR51 source files are byte-unchanged from the previously reviewed head. I did not fetch private Drive material, run author scripts, rerun existing checks, or use private author code.

Verdict: `ACCEPTED_SCOPED_README_DELTA`, with one non-mathematical hygiene note. I found no unsupported enlarged mathematical claim in the README. The README keeps the main half-filled result scoped to centers

`K=[[1/2,0,b],[0,1/2,c],[b,c,1/2]]`, `bc!=0`, `4(b^2+c^2)<1`,

and directions `D` at those centers (`README.md:7-11`), preserves the continuation/open-boundary split (`README.md:13-15`), and explicitly says `PROVED` is an author status rather than accepted theorem/review/CI/proof-assistant status (`README.md:17`).

## Claims and delta verdicts

| README claim | Lines | Delta verdict | Notes |
|---|---:|---|---|
| Half-filled theorem summary | `README.md:7-11`, `README.md:17` | `ACCEPTED_SCOPED_AS_SUMMARY` | The wording matches the prior first-review scope: strict half-filled missing-edge centers only, all nonzero real symmetric three-point directions at those centers, arbitrary edge-strength ratio, and no extension to arbitrary centers. The line-17 qualifier prevents accidental upgrade to an accepted main theorem. |
| Continuation identities/obstructions summary | `README.md:13-15`, `README.md:17` | `ACCEPTED_SCOPED_AS_SUMMARY` | This matches the prior continuation first-review result: identities/reductions/method obstructions are separated from the still-open four-dimensional Schur inequality, Lambda radial-derivative conjecture, general real three-point concavity, positive Jensen counterexample, and novelty. |
| Access/reproduction packet | `README.md:19-38` | `INCOMPLETE_AS_INDEPENDENT_EVIDENCE`; nonblocking | I did not fetch the private packet or independently verify the archive contents, metadata, or author-script reproduction commands. The README represents the packet as private and as a reproduction aid, not as public mathematical evidence. It therefore does not enlarge the theorem claim. Hygiene note: lines `README.md:21-23` contain a private storage locator and metadata; if public artifacts must avoid private locators, the integrator should handle that as a publication-policy issue rather than a proof blocker. |
| Actual post-checkpoint output summary | `README.md:40-54` | `ACCEPTED_SCOPED_AS_OUTPUT_SUMMARY`, except author-only packet transport details | The signs and exact values listed for the auxiliary-resolvent obstruction, entropy/Jensen intervals, and coefficientwise PSD failure agree with the previously reviewed continuation evidence. The README correctly states that the negative auxiliary value is not an entropy counterexample (`README.md:54`). I did not rerun the author packet or independently verify the ZIP/JSON transport packaging claim. |
| Conditional Schur complement clarification | `README.md:56-62` | `ACCEPTED_SCOPED` | The subtraction is the actual marginal entropy Hessian. At the independent leaf center, the marginal law of `(X1,X2)` is a product, and the first score is `d(i-x)/v + e(j-y)/w`. Missing-edge second derivatives have zero row and column sums, while `log Pij` splits as a row term plus a column term, so their log-acceleration contribution cancels. Thus `-H(X1,X2)'' = d^2/v + e^2/w`. The README also correctly leaves positivity of the conditional form unproved and identifies the complete-entropy Schur target as the intended one. |
| PSD rank-two direction `D_s` and harmful acceleration | `README.md:64` | `ACCEPTED_SCOPED` | In continuation equation (37), `D_s` has the displayed block form with `2 x 2` eigenvalues `0` and `1/2`, and third eigenvalue `s/6`; hence it is PSD of rank two for `0<s<1`. Since `log((1+s)/(1-s))>0` on this interval, the acceleration term `-s log((1+s)/(1-s))/6` is strictly negative. This supports the README's point that the Fisher term is essential even for this concrete semidefinite direction. |
| C2 exact-computation input/status | `README.md:66-74` | `ACCEPTED_AS_STATUS_BOUNDARY`; `INCOMPLETE` for global sign | The README points back to continuation equations (32)-(35), says the matrix transport check is only four exact fixtures, and says issue52 is requested rather than completed. It therefore does not claim the open global sign certificate. |

## Limitations preserved

This delta review does not certify the private reproduction packet, author scripts, ZIP contents, JSON transport beyond the public statements already reviewed, the global `4 x 4` Schur PSD inequality, global positivity of the Lambda radial-derivative matrix, general unequal-diagonal three-point concavity, any strict positive complete-entropy Jensen counterexample, or novelty.

No precise critical gap was found in the README delta. The only integration question I see is whether a public README should carry a private storage locator; that is a publication-hygiene decision, not an unsupported mathematical claim.
