C3 records a **separate new finite verification unit** required by the PR60 continuation review. This does not extend, restart or change the existing full-r determinant/P/Q window. C2 remains sole compute owner and should claim it only after its current owned arithmetic has stopped, preserving the full-r run/failure history.

Frozen input: PR60 `f869fd251c0d6fdad737b6d5efa287307795a87d`, `research/I05-22-R3-lambda-zero-global/continuation.md`, specifically the fixed-diagonal radial obstruction and genuine curvature/Jensen checks in equations (23)–(36). `continuation_exact.py` and its claimed values are comparison targets after independent construction, not imported or executed input.

Reconstruct from literal rational matrices:

```text
K* = [[11/100,0,33/500],[0,1/200,3/1000],[33/500,3/1000,199/200]]
D* = [[0,-1,0],[-1,-1/50,2/25],[0,2/25,0]]
C* = K* - diag(K*), h=1/100000.
```

Independently derive all eight complete-event signed determinant polynomials and the mixed jets in the affine plane `K*+epsilon D*+delta C*`. Check the exact legal ranges/Sylvester minors in the frozen statement, strict legality of `K*±hD*`, and the displayed conditional-odds `exp(Lambda)>1`. For the derivative of the full negative entropy Hessian, retain all terms

```text
sum[2 p_D p_DC/p - p_D^2 p_C/p^2
    + p_DDC log p + p_DD p_C/p].
```

Using rational atanh/log2 series with a proved rational tail and outward endpoints, certify separately the negative fixed-diagonal radial derivative, positive `-H''(K*;D*)`, and negative complete-configuration Jensen gap `(H(K*+hD*)+H(K*-hD*))/2-H(K*)`. Compare the actual rational intervals with the frozen claim, retaining full event jets, exact fractions and enclosure widths. This is an auxiliary-method failure, not an entropy counterexample or a refutation of the Lambda-zero M theorem.

Bound for this new, distinct small certificate unit: **one live arithmetic process, one CPU/thread, 16 GiB, no GPU, at most 600 seconds total wall clock from its first launch**, including any repair; record the source commit, process/start/absolute deadline and actual exit. Stop on success, the first exact discrepancy, or the deadline. Do not expand to another parameter, fixture or scan, and do not silently extend this or the full-r unit. If this bound is insufficient, retain the incomplete layer and request a specifically revised contract in this issue before more work.

Status **REQUESTED**, no C3 arithmetic or claimed PID. C1's original FIRST will review the finished independent evidence before accepting its continuation Claim4; C3 then assigns the independent second gate. PR58's already-assigned corridor/sign reconstruction remains a different object and does not inherit this result.
