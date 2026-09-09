# PR51: accepted half-filled theorem and scoped continuation

Final head: `184535756f5ed92f2f5c47804bdc8466a7d15041`. Merge commit: `ed10e23134d5dd8350f1cd9636204143c62ebc40`. All five source files are under [research/I05-22-missing-edge-20260909](../../research/I05-22-missing-edge-20260909/README.md). [Independent reports and exact checks](pr51/README.md) distinguish the original and continuation review units.

## Half-filled missing-edge centers

For the real symmetric center

`K=[[1/2,0,b],[0,1/2,c],[b,c,1/2]]`, `bc!=0`, `4(b^2+c^2)<1`,

every nonzero real symmetric three-point direction `D` has `H''(K;D)<0` for full complete-configuration Shannon entropy. The nonzero edge-strength ratio is arbitrary. The proof retains all eight atoms, the full Fisher and acceleration, a symmetry-derived 2+4 decomposition, and a positive rational derivative matrix proved by determinant, seed minors and inertia continuation. Integration from singular `G_0` is justified. No coordinate direction is removed.

Both independent reviewers accepted frozen original head `4baebc317896278dcb8f0947d308fdce037c87cf`. The independent first checker reconstructed the exact identities and the illustrative negative Jensen interval; finite examples do not prove the theorem. The second reviewer used only the public source and ran no arithmetic for this unit.

The theorem is about Hessians at these centers. It does not establish arbitrary unequal-diagonal missing-edge centers or arbitrary long chords leaving this center family. On `bc=0`, only the stated nonstrict continuity limit is retained. Strictness at singular boundaries is not asserted.

## General connected missing-edge identities and positive elimination block

For `K=[[x,0,b],[0,y,c],[b,c,z]]`, `bc!=0`, define `v=x(1-x)`, `w=y(1-y)`, `A=b^2/v`, `B=c^2/w`, and `q=z-A(1-x)-B(1-y)`. Strict legality is equivalent to `0<x,y<1`, `A,B>0`, `q>0`, `q+A+B<1`; signs of the nonzero edges are restored by sign conjugation.

Accepted continuation results are:

- Product-law conditional coordinates `t_ij=q+A(1-i)+B(1-j)` and an invertible map from all six physical symmetric directions to `(d,e,m,f,g,h)`.
- The exact complete Fisher and acceleration collected into a 2+4 block form. The marginal Fisher `diag(1/v,1/w)` remains present.
- Strict positive definiteness of the eliminable two-dimensional log block `L` throughout that product domain, proved by strict convexity and rectangle trapezoid bounds.
- Exact Schur-complement equivalence and face-acceleration identity, including both residual mixed terms. Facewise two-point arguments cannot omit those terms or count the same Fisher twice.
- The Lambda=0 subfamily condition `q=(1-A-B)/2`, its four-parameter coordinates and fixed-physical-direction derivative identity `M=F'(u)+Q` as an exact handoff formulation. The global sign of this matrix is not proved.
- The exact conditional marginal-Hessian subtraction in README: at the independent leaf center, `-H(X1,X2)''=d^2/v+e^2/w`, including cancellation of missing-edge acceleration against the additive marginal log law.

The continuation first review covers `2e4b8754ad4af2fe055ebeeef1159877773372a3`; a separate README first delta and fresh second review cover `8b078ab834c46ce0c0e81967e3ada3fbbf542f1a`. The two global four-dimensional Schur PSD statements (29) and (30) remain **INCOMPLETE**. Positive `L` alone does not settle either.

## Two method obstructions

The auxiliary conditional resolvent `Phi=sum P_ij^2/p_ij1` has an exact strict legal rational example with `Phi''=-53670727895896612562246875/14117659525214393686902<0`. Its actual entropy curvature and the displayed legal Jensen triple have the concave sign. This rules out universal convexity of the auxiliary resolvent only.

The half-filled direction `D_s=[[1/4,-1/4,0],[-1/4,1/4,0],[0,0,s/6]]` is PSD rank two for `0<s<1` and has harmful log acceleration. Its rescaled full curvature expansion has `s^4` coefficient `-1/18`, disproving the proposed coefficientwise PSD route. Because the test direction varies with `s`, it does not disprove the fixed-direction radial matrix conjecture in issue52.

Neither result is a DPP entropy counterexample. No general real three-point concavity, global radial derivative sign, new entropy-rate theorem, novelty, CI pass or proof-assistant certification is asserted.

## Version and publication binding

The original three source files are unchanged through `8b078ab8`. The final `18453575` successor only replaces private verifier/packet access locators and account metadata in README and verification entrypoints with the public reproduction boundary and independent-check link. The three mathematical source files and every displayed code/output block are unchanged; private originals and historical review line references remain tied to their frozen heads. C3 checked the exact two-file delta before merging. No private author file was retrieved or republished.
