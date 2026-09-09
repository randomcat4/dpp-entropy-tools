# C2 directed weak-low-layer unit

Status: PARTIAL / STOPPED_SUBSTANTIVE. This unit is complete and no further search is scheduled. General real DPP entropy concavity remains unresolved. No positive candidate was found, and a finite set of negative Hessians is not a universal theorem. Novelty is unverified. Author self-check only; not independently reviewed.

The fixed five-point rational U from the task was used with all 26 positive events of sizes 0,1,2,3 and all six real symmetric directions. The mechanism tested was whether a weak direction of the low-event Jacobian or Fisher matrix could retain positive top geometric acceleration while suppressing compensation.

The budget was frozen at 24 center records (22 distinct matrices: the scalar center occurs under all three rotations), 129 selected directions. At every center the full six-dimensional Hessian was numerically negative definite. The largest Euclidean/Frobenius-normalized curvature was -0.4287830801381278. This is numerical evidence at those centers, not an interval certificate for every direction.

## Mechanism evidence

All V below have Frobenius norm one. The geometric term means c(det A)'', not the entire top log-acceleration term.

|Direction selection|Count|Largest total curvature|Range of geometric acceleration|
|---|---:|---:|---:|
|Weakest low Fisher mode|24|-0.4512355983|[-1.648763660,-0.491769678]|
|Weakest unweighted low Jacobian mode|24|-0.5287487897|[-1.323526755,-0.559120272]|
|Largest full Hessian eigenvector|24|-0.4287830801|[-1.568693313,-0.471721670]|
|Largest full curvature / low Fisher generalized eigenvector|24|-2.7562758752|[-1.304895694,0.592454346]|
|Largest geometric acceleration / low Fisher generalized eigenvector|24|-3.4065517214|[1.339305957,2.470210439]|
|Exact pair-null formula at trace A=2|9|-4.0348032188|[2.386014344,2.519066013]|

Weak low-event modes lost positive determinant acceleration in every tested center. Directions that retained positive geometry incurred larger low-event Fisher cost and, more decisively, negative two-point log acceleration. A noncommuting representative has geometry/top-Fisher = 1.2186632189, but full curvature -4.0425292455.

|Layer size|Fisher cost|Log acceleration|Total curvature|
|---|---:|---:|---:|
|0|0.9237349678|2.0679681582|1.1442331905|
|1|1.5206284560|0.1775743029|-1.3430541532|
|2|0.0050585744|-5.8813669255|-5.8864254999|
|3|2.0237515414|4.0664687586|2.0427172171|

Its center spectrum is (0.58,0.67,0.75), trace 2; the commutator norm is 0.0043779948. Thus pair-score suppression does occur and survives noncommuting perturbation, but it does not suppress pair logarithmic acceleration. `representative_noncommuting_top_excess.json` records the nearby exact rational input and all exact probabilities and interval layer values.

## Exact negative fixtures

Both use the rational step h=1/100, all 26 rational endpoint/center probabilities, exact Sylvester minors for A-hV, A, A+hV and their complements, and 70-decimal interval logarithms. The following wider displayed intervals contain the saved interval output:

* `representative_best_full.json`: H'' lies in (-0.428783069797,-0.428783069795); chord difference lies in (-0.000021452578304,-0.000021452578303).
* `representative_noncommuting_top_excess.json`: H'' lies in (-4.042529348722,-4.042529348720); chord difference lies in (-0.000202134709853,-0.000202134709851).

The old scalar fixture `representative_top_excess.json` is retained as a version-1 artifact; it is not the final noncommuting representative. `results_v1.json` is also retained, so failed-wrapper history is not overwritten.

## Remaining obstacle

Numerical suppression of low first derivatives gives no sign control over -sum p'' log p. In particular the pair-null direction can have nonzero pair acceleration. The minimum remaining mathematical obligation is a quantitative bound coupling these second derivatives to the full Fisher costs, or an explicit direction violating that bound. Injectivity of the low-event derivative map alone does not supply such a bound. No additional scanning is justified by this unit.

See `proof_and_methods.md` for formulas and valid-domain derivation, `results.json` for every center and direction, and `verification.md` for calibration and execution history.
