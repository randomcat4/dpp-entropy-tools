# PR51 second independent proof review — frozen scope

Review status: **FROZEN / NOT YET REVIEWED**.

Frozen PR51 head: `4baebc317896278dcb8f0947d308fdce037c87cf`.

Source directory:

`research/I05-22-missing-edge-20260909/`

Files in scope:

1. `proof_half_filled.md`
2. `sources_and_routes.md`
3. `verification.md`

The later PR51 successor head `2e4b8754ad4af2fe055ebeeef1159877773372a3` reportedly adds only `continuation.md`; that continuation is out of scope for this review.

Target theorem to review:

For the real symmetric half-filled three-point DPP kernel

\[
K=\begin{pmatrix}
1/2&0&b\\
0&1/2&c\\
b&c&1/2
\end{pmatrix},
\qquad bc\ne0,\qquad 4(b^2+c^2)<1,
\]

the complete-configuration Shannon entropy has strictly negative Hessian in every nonzero real symmetric direction.

Review boundaries:

- This is a fresh second nonauthor proof review, independent of any first review/report/code/conclusions.
- I will not fetch or use any private Drive verifier.
- I will not use PR41/PR43 theorem black boxes.
- I will read all three source files in scope and cite source lines.
- I will not execute heavy mathematics. If a narrow doubt requires a targeted check, it is limited to one local thread, 4 GiB RAM, no GPU, and 15 minutes, with a frozen plan first.
- I will not modify author files, publish to GitHub, or merge anything.
