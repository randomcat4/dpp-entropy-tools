# Non-Author Review: Coarse Event Identity

Status: CORRECT_IDENTITY_ONLY.

Reviewed source: main-authored `research/N4/round2/coarse_event_candidate.md`
at commit `3eabd9ba71ff24569a7d22ded4c3f159ef2ed89a`, blob
`4c550633176ecd709e48a27a9b73212c6458c5b7`.

Executable artifact: `coarse_identity_check.py`.

Run artifact: `coarse_identity_check.json`.

Run metadata: PID `12864`, exit status `0`, script SHA-256
`3eabceb17c1cacb567e8e2b82849d1a365987a3b9f23063ac5e2c61737901fc5`,
Python `3.12.14`.

## Verdict

No critical gaps found for the stated identity. The check uses the independent
Householder fixture `z=(1,2,2,4)/5` with rational noncommuting `A,V`. For all
16 events, the candidate's low-degree formulas match the independent signed
determinant event polynomials exactly; the full event polynomial is exactly
zero.

The triple merge also preserves Fisher exactly:

```text
original triple Fisher = -82391929/82652202360
grouped triple Fisher  = -82391929/82652202360
```

Thus the decomposition

```text
H_face(A;U)=H_12(A;U)+det(A) H(z^2)
```

is correct in the scoped rank-three four-point face.

This review makes no concavity claim. The coarse 12-symbol vector is a
constrained polynomial function of the six entries of `A`; it is not an affine
free-simplex chord under `A -> A+sV`, so Shannon concavity of an unconstrained
simplex law cannot be used to conclude face concavity.
