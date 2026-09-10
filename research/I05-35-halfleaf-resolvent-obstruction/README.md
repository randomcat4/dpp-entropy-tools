# I05-35: exact half-leaf resolvent obstruction and lossless curvature repair

Status: **PROVED BY AUTHOR / PENDING INDEPENDENT REVIEW** for the exact pointwise-resolvent counterexample and the complete-event decomposition in `proof.md`. This packet is an independent-from-PR104-code reconstruction, not an independent reviewer verdict. General half-leaf Shannon concavity, one-sided integrated convexity, unequal leaf diagonals, and general real three-point concavity remain **INCOMPLETE**. Novelty is **NOT_ASSESSED**.

This successor starts from `main@b3ada9f6bb23e3efd2e1a4d2a2977d50b61fb4d7`. It does not modify PR81, PR104, their review records, or any accepted file. No existing computation is rerun.

## Exact result

For the strict half-leaf

```text
A=1/4, B=16/25, q=109/1000, qbar=1/1000,
K=[[1/2,0,1/4],[0,1/2,2/5],[1/4,2/5,277/500]],
```

at

```text
r=1/50000,
D=(d11,d22,d33,d12,d13,d23)=(-18,-72,40,146,108,5),
```

the true six-direction affine line `K+tD` satisfies

```text
Phi_r''(K;D)
=-47488558049748267993080620088778228551027375300000000000
 /2044542058422113103788725284171055940635901533282467
<0.
```

Here

```text
Phi_r=sum_ij P_ij^2/(p_ij1+r P_ij).
```

Therefore the old-chat assertion that `Phi_r''` is positive definite for every `r>0` and every strict half-leaf is false. This is a **method/certificate counterexample**, not an entropy counterexample and not a counterexample to the integrated one-sided quantity `G1''`.

## Lossless repair

With `q_ij=p_ij1/P_ij`,

```text
G1=sum_ij P_ij q_ij log q_ij,
G0=sum_ij P_ij (1-q_ij) log(1-q_ij),
H=H(P)-G1-G0.
```

At the half-leaf center `P_ij=1/4`, so every physical direction obeys the exact identity

```text
-H''=4(d11^2+d22^2)+G1''+G0''.
```

It retains all eight complete events, both emitted states, the leaf marginal, complete Fisher information, and every acceleration term. On the displayed resolvent witness the checker rigorously encloses all three terms and proves the full entropy curvature has the concave sign. Thus no Shannon counterexample is inferred from the negative pointwise resolvent.

## Reproduction

Run

```text
python code/verify_resolvent_obstruction.py
```

The checker is Python-standard-library only. It:

1. reconstructs all eight complete-event polynomials from principal-minor Möbius inversion on the true `K+tD`;
2. independently checks each against the signed shifted determinant formula;
3. groups leaf marginals and verifies the exact conditional Schur jets;
4. differentiates `P(t)^2/[p_1(t)+rP(t)]` directly and obtains the printed negative rational;
5. encloses logarithms by a 60-term rational atanh series with an explicit tail; and
6. compares the two-side-plus-marginal curvature with a direct eight-event Shannon calculation.

The retained run used one local Python process and completed far below one minute. There was no search, parameter scan, precision escalation, retry, or external computation contract.

## Files

- `proof.md`: complete derivation, exact witness, repair, and scope.
- `code/verify_resolvent_obstruction.py`: self-contained exact checker.
- `output/verify_resolvent_obstruction.txt`: literal successful output.

The next analytic target is the integrated logarithmic Hessian itself, preferably after complement pairing, rather than pointwise positivity in the auxiliary parameter `r`.
