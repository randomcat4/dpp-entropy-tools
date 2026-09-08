# D10-U7 frozen problem

Author research; no self-certification.

Fix any finite n>=2, any x in (0,1)^n, X=diag(x), and any real symmetric zero-diagonal matrix A whose support graph G is connected. Every supported edge has nonzero weight, of arbitrary sign and magnitude. No equality or symmetry among the x_i is assumed. Set K_epsilon=X+epsilon A.

Primary target A: there exists epsilon_0>0, depending on this fixed (n,x,A), such that for every real epsilon with 0<|epsilon|<epsilon_0, K_epsilon is strictly between 0 and I and the full Shannon entropy Hessian is strictly negative definite on all Sym(n).

Secondary target B: the same statement for every tree support, with all the same parameter quantifiers. Target C if these do not close: a strict connected counterexample or an explicit mathematical obstruction, not a floating sign or finite non-hit.

Exact event probabilities are p_S=sum_{T superset S}(-1)^{|T|-|S|}det(K_T). Inclusion minors are not exact atoms. Entropy uses natural logarithms. Off-diagonal observation coordinates are z_ij with direction E_ij+E_ji; all diagonal directions are included.

The proposed distance scaling is I on diagonal coordinates and |epsilon|^-d_G(i,j) on each off-diagonal coordinate. Its limit, including all mixed entries, must be proved. A negative diagonal or a finite matrix scout does not suffice.

Excluded interpretations: a threshold uniform in n, x approaching the boundary, or weights approaching zero; negativity at epsilon=0; a global Hessian statement for all strict DPP kernels; any conjecture certified by finite numerical evaluations.

Only this new directory is writable for this unit. No shared index or existing U4/U5/S8c file is modified. No submission or external computation is part of this task.
