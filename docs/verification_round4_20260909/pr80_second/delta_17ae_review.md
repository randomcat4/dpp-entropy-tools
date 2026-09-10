# PR80 delta 17ae independent SECOND review

## Verdict summary

The delivered delta files support several analytic or conditional conclusions, but they do not supply an independent finite certificate. The strongest closed conclusions in this review are: the negative-fiber construction is a real complete-reference fiber obstruction as written; the legality/equality/endpoint discussion is coherent; and the compensation and neighborhood arguments are valid conditional derivations once their stated finite symbolic constants are accepted.

The quantitative existence conclusions are not independently certified here. The special 2+2 complete-interval theorem still depends on event enumeration, Gram sums, q-window constants, and logarithmic comparisons that were not reconstructed by an independent C2 implementation. The coefficient radius `1/40000`, explicit correlated member, original `s=9/10` pair counts/signs/window bounds, and fixture equality remain author-side evidence only.

## Binding and redaction check

`delta_17ae_input_binding.json` fixes PR80 at head `17ae62c23aad387fbd9b445e5436aa9ad245185d` from previous head `1a322ace19fd8ccc679f849780850dde31deb3d2`. All seven delivered files match their delivered SHA-256 values. The binding also records public paths, original blob IDs, and original SHA-256 values. The local package is not a git repository, so original blob contents could not be independently fetched or hashed. I therefore accept the delivered file binding but mark public original blob mapping as `INCOMPLETE` for local verification.

The three placeholders are visible only as review-status references in the delivered files: `README.md:25` and `ADDENDUM_CROSS_FIBER_OBSTRUCTION.md:3,27`. Their placement is nonmathematical in the delivered packet. The stronger claim that no original mathematical line was altered remains binding-level metadata because the original blobs are unavailable locally.

## Negative full-reference fiber obstruction

`ADDENDUM_CROSS_FIBER_OBSTRUCTION.md:9-13` defines `C_S` as the complete `p_C`-reference fiber contribution to `t^2 I''`; it explicitly warns that this is not, in general, minus the second derivative of conditional Shannon entropy alone. This is the right object for the advertised obstruction.

For the first family `A=I/2`, `C=I/2+rX`, `B=sqrt(r/2)R`, `0<r<=1/8`, the note gives Schur-complement legality on `|t|<=1` at lines 47-53, derives the mask-1 conditional kernel at lines 55-63, and obtains

`C_{mask 1}(1/2)=-16r^2 log((1+4r^2)/(1-4r^2))<0`

at lines 65-71. As a static analytic construction, this gate is `CORRECT`: it is a genuine obstruction to universal positivity of every complete conditional fiber. It is not an entropy counterexample, and the note says so at lines 71-73.

The correlated-family variant at lines 91-107 is also structurally coherent: it supplies both correlated marginal blocks and a rank-two nonzero cross block. The decimal enclosures and the single-point full-curvature positivity at lines 75-89 and 107 are still author numerical evidence and are not independently certified here.

## Legality, equality, and the endpoint

The correction of strictness at lines 15-35 is accepted. Under the cone hypothesis at `s>0`, equality forces `u=y=0` on every complete event; the note then uses two-coordinate DPP probabilities to conclude `B=0`. The endpoint `t=0` is handled separately by analyticity and no division by `t^2` is used. This is `CORRECT` as a finite strict-DPP equality and endpoint statement.

## Special 2+2 complete-interval compensation

The theorem at lines 109-180 claims that the first family satisfies

`H''(t) <= -(700/19) r^2 t^2`

on all `|t|<=1`. The sign convention is consistent: lines 170-180 lower-bound `C_tot=t^2 I''`, then divide by `t^2=s` for `t!=0` and use `I''=-H''`; the endpoint is supplied by the earlier analytic argument.

The derivation is `CORRECT_CONDITIONAL`: if the grouped event probabilities in lines 121-128, the likelihood window in lines 130-140, the Gram identities in lines 142-150, and the logarithmic constants in lines 164-168 are accepted, the lower-bound chain in lines 170-178 follows with the advertised sign.

As an independently certified existence theorem, this gate is `INCOMPLETE`. The event grouping, all sixteen event coefficients, the Gram sums, and the log constants are exactly the kind of finite symbolic/arithmetic content that this review was forbidden to reconstruct and that no new C2 certificate supplies.

## Original `s=9/10` finite recheck

The original PR80 context already stated that the old output summaries and PASS labels are not independent numerical certificates (`input/README.md:9-15`). The delta README repeats that the new outputs are literal author stdout but still author evidence, not independent C2 (`delta_17ae_input/README.md:21-23`).

The recheck claims in `ADDENDUM_CROSS_FIBER_OBSTRUCTION.md:182-189` therefore remain `INCOMPLETE`: the 75/66 pair counts, negative event list, window lower bounds, full value, and equality to the intended PR58 fixture are not independently certified. The delta also states that the complete interval of the original 3+3 fixture is not newly certified (`README.md:27`).

## Normalized Gamma and coefficient neighborhood

`ADDENDUM_CORRELATED_NEIGHBORHOOD.md:7-23` removes the apparent endpoint singularity by defining

`Gamma(s)=E_mu phi_s(a,b)`

with continuous value `Gamma(0)=6E_mu a^2`. This is a sound normalization of the curvature object and is `CORRECT` at the level of the displayed identity.

The coefficient-space theorem at lines 25-113 is `CORRECT_CONDITIONAL`. The proof is a perturbative estimate around the `r=1/8` reference point; it explicitly says the radius is in coefficient space, not matrix-entry norm, at lines 33-41. The Lipschitz constants, lambda derivative bounds, base lower margin `Gamma0>=175/304`, and bad-fiber upper bound are coherently chained in lines 55-111 if their constants are accepted.

The quantitative radius and explicit existence conclusion are `INCOMPLETE` as independent certification. The base positive margin comes from the preceding interval theorem, whose event/Gram/log constants are not independently rebuilt here. The explicit kernel membership at lines 115-139 depends on rational reconstruction and coefficient differences checked only by the author script.

## Direct-sum, compactness, and open classes

The arbitrary-dimensional extension at lines 141-149 is a valid conditional topological argument. Independent spectators make the block-diagonal law additive in Shannon entropy, and fixed finite-dimensional continuity plus compactness gives a relative-open neighborhood once there is a verified strict base margin and a selected negative active fiber. The note correctly limits this to existential, dimension-dependent neighborhoods and does not claim a uniform radius, all rank-two coverage, or a whole-chord result for the original 3+3 fixture.

This gate is therefore `CORRECT_CONDITIONAL`, not a new independently certified global theorem.

## Final delta verdict

`CORRECT`: delivered SHA binding; negative complete-reference fiber obstruction as a static construction; legality/equality/endpoint handling; Gamma endpoint normalization.

`CORRECT_CONDITIONAL`: special 2+2 complete-interval compensation derivation; coefficient-neighborhood perturbation estimate; direct-sum/compactness/open-class extension.

`INCOMPLETE`: public original blob verification in this local package; redacted-original comparison; event enumeration; Gram sums; log constants; rational bounds; base positive margin as an independent certificate; explicit correlated-kernel coefficient membership; original `s=9/10` fixture equality, counts, signs, and numerical bounds; general dense correlated rank-two whole chord.

`SOURCE_ONLY`: all author scripts and saved outputs.

`NOT_ASSESSED`: novelty. `NOT_PERFORMED`: formal proof.
