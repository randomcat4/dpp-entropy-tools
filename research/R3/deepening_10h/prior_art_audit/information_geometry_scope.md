# D10-Prior audit: Hino--Yano information geometry versus R3 Shannon curvature

STATUS: CORRECT

Assessment: the T1 prior-art branch correctly warns that Hino--Yano information-geometric curvature does not directly control this project's Shannon entropy Hessian along affine marginal-kernel \(K\)-paths. Any proof that cites Hino--Yano as a direct sign theorem for \(d^2H(K_0+tD)/dt^2\) has a critical gap.

## Sources checked

Local author material, read-only from `origin/research/T1-curvature-structure`:

- `research/T1/prior_art.md`
- `research/T1/audits/prior_art_conditions.md`

Primary external source:

- Hideitsu Hino and Keisuke Yano, *Duality induced by an embedding structure of determinantal point process*, arXiv:2404.11024, <https://arxiv.org/abs/2404.11024>.

The T1 prior-art branch states that Hino--Yano studies DPP embeddings into log-linear/exponential-family geometry and warns not to confuse those curvature objects with Shannon entropy curvature on marginal-kernel affine paths. That warning is correct.

## What Hino--Yano supplies

The paper is directly relevant prior art for finite DPP information geometry. It studies an embedding of DPPs into log-linear models / exponential-family geometry, describes dual coordinate structures, and gives Fisher-information and \(e\)-curvature calculations for the embedded DPP model.

This supports the following safe implications:

1. DPPs have established information-geometric structure; Fisher and curvature language is not new by itself.
2. In the strict finite real setting, a DPP kernel \(K\) can be related to an \(L\)-ensemble representation \(L=K(I-K)^{-1}\), so Hino--Yano's real finite-DPP geometry is relevant background.
3. Fisher information describes local second-order KL geometry of the statistical model in the chosen coordinates.
4. \(e\)-curvature describes how the embedded DPP model bends inside an ambient exponential family.

These are useful tools and prior-art constraints.

## What Hino--Yano does not directly supply

It does not directly prove a sign for
\[
\frac{d^2}{dt^2}H(K_0+tD)
\]
where \(H\) is the full-subset Shannon entropy of the exact DPP atom law and \(K_0+tD\) is affine in the marginal kernel.

There are three separate mismatches.

### 1. Functional mismatch

Hino--Yano's Fisher and \(e\)-curvature objects are geometric properties of a statistical model embedded in a log-linear/exponential-family ambient space. R3 asks about the scalar Shannon entropy
\[
H(P_K)=-\sum_S p_K(S)\log p_K(S).
\]
For a smooth probability curve \(p(t)\),
\[
H''(t)
=-\sum_S\frac{(p'_S(t))^2}{p_S(t)}
-\sum_S p''_S(t)\log p_S(t),
\]
using \(\sum_Sp''_S(t)=0\). Fisher information controls the first negative square term. It does not, by itself, control the acceleration term
\[
-\sum_S p''_S(t)\log p_S(t).
\]

### 2. Coordinate mismatch

The R3 path is affine in marginal kernel coordinates:
\[
K(t)=K_0+tD.
\]
Hino--Yano's embedding uses log-linear / \(L\)-ensemble / information-geometric coordinates. A \(K\)-affine line is generally nonlinear in those coordinates.

Even in expectation-like inclusion coordinates, \(\det K_T(t)\) is generally a nonlinear polynomial in \(t\) for \(|T|\ge2\). It is affine only in special cases such as rank-one \(D\), which is exactly why Gu's rank-one route is a special occupied route.

### 3. Curvature-sign mismatch

Nonzero or bounded \(e\)-curvature is not the same object as concavity or convexity of Shannon entropy along an arbitrary coordinate path. To turn Hino--Yano into an R3 Hessian sign theorem, one would need an extra theorem proving that their curvature tensors, under the specific \(K\)-affine pullback, dominate or cancel the atom-acceleration term above. The T1 prior-art files do not claim such a theorem, and I did not find it in the Hino--Yano source checked here.

## Correct implication direction

Safe direction:

\[
\text{Hino--Yano}
\Rightarrow
\text{prior art for DPP information geometry, Fisher tensors, embeddings, and curvature terminology}.
\]

Unsafe direction:

\[
\text{Hino--Yano \(e\)-curvature}
\nRightarrow
\operatorname{sign}\!\left(\frac{d^2}{dt^2}H(K_0+tD)\right)
\text{ for marginal-kernel affine R3 paths}.
\]

Conditional future direction:

\[
\text{Hino--Yano tools}
+\text{ explicit pullback to \(K\)-affine paths}
+\text{ control of }-\sum_Sp''_S\log p_S
\Rightarrow
\text{possible R3-relevant curvature criterion}.
\]

The missing middle step is substantial and cannot be skipped.

## Verdict for T1 prior-art branch

The T1 branch's prior-art framing is correct: Hino--Yano is strong prior art for DPP information geometry and a warning against novelty overclaim, but it does not directly certify the Shannon entropy Hessian sign problem in R3 coordinates.

If a T1 proof later uses Hino--Yano, it must explicitly state which coordinates are used, whether the path is \(K\)-affine or information-geometric affine, and where the atom-acceleration term is controlled.
