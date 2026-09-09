# Route registry

## ROUTE-COVARIANCE

- Frozen target: v1; conditional determinant-score projections Q_k.
- Method: exact conditional Fisher decomposition and covariance squares.
- 最快证伪测试: compare Q_k against the cofactor at the true A optimizer.
- 工作单元: U1-U3, then U5-U6; two exact rational shortcut counterexamples.
- Status: projection identities PROVED; proposed closure DISPROVED, including
  all convex combinations at one exact stationary point.
- 共同瓶颈: discarded conditional-score residuals cannot be removed.

## ROUTE-PAIR-SCORE

- Method: retain all degree <=2 observable scores; isolate the triple-log
  derivative as one positive rank-one correction.
- 最快证伪测试: a nonexchangeable rank-two boundary with one rare full atom.
- 工作单元: U4 plus one analytic child unit and one exact point check.
- Status: all-direction projected closure DISPROVED; stationary version is
  an unproved stronger sufficient target.
- 共同瓶颈: actual DPP alignment of the retained triple score with the trace
  functional in the projected metric remains uncontrolled.

## ROUTE-OPTIMIZER

- Method: Sherman-Morrison on the exact omitted triple-score direction.
- 最快证伪测试: verify whether the proposed suppression bound supplies a
  lower bound on trace alignment; it does not.
- 工作单元: one separate analytic optimization unit.
- Status: general finite-dimensional formulas established; SM-close is
  EQUIVALENT_BLOCKER, not a new DPP inequality.
- 共同瓶颈: the same missing alignment condition. No independent third proof
  route remains after this reduction; no expanded scan is authorized here.
