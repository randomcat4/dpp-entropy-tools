# PR62 Second Mathematical Review

## Overall Verdict

The analytic moving rank-one endpoint theorem and its sufficiently small common independent-bit-flip lift are CORRECT within the frozen scope. I found no critical mathematical gap in the endpoint atom formula, midpoint atom formula, mass-transfer derivative, strict active-pair inequality, equality analysis, or bit-flip continuity margin.

The finite scripts and stored numerical outputs were not rerun and are not promoted. The `3+3` multiring line, formal verification, and novelty remain INCOMPLETE.

## Analytic Proof

STATUS: CORRECT

The proof begins from the complete DPP atom law, not inclusion marginals: `p_K(S)=sum_{T superset S}(-1)^{|T|-|S|} det K_T`, with entropy over all complete atoms (`input/moving_rank1_theorem.md` lines 5-13). For a rank-one kernel `a xx^T`, the atom law has empty mass `1-a`, singleton masses `a x_i^2`, and no larger atoms (lines 34-45). Averaging the two endpoint laws therefore gives the law `q` in lines 46-60 with the same empty and singleton masses as the arithmetic matrix midpoint before rank-two pair atoms open.

The midpoint law in lines 66-103 is correct. For the nonzero spectral representation `K_0 = alpha uu^T + beta ww^T`, Cauchy-Binet gives the pair weights `b_ij=(u_iw_j-u_jw_i)^2`, with sums recorded in lines 82-87. Mobius inversion for rank at most two gives the complete atoms in lines 89-98: empty mass `(1-alpha)(1-beta)`, singleton mass `(alpha-m)u_i^2+(beta-m)w_i^2`, pair mass `m b_ij`, and no atoms of size at least three.

The bridge `p_r` in lines 105-123 is a valid probability law for `0<=r<=m`. Nonnegativity follows from `m=alpha beta <= min(alpha,beta)` and the endpoint identities are exactly `p_0=q`, `p_m=p_{K_0}`. The entropy derivative in lines 125-132 follows by differentiating all empty, singleton, and pair atoms; the identity `sum_{j != i} b_ij = u_i^2+w_i^2` converts the singleton derivative terms into the pairwise logarithm sum.

The strictness step in lines 134-155 closes the main proof. Lagrange's identity gives
`p_i(r)p_j(r) = (A_r u_i u_j + B_r w_i w_j)^2 + A_r B_r b_ij`, and the scalar identity `A_rB_r-rp_empty(r)=m-r` is positive for `0<r<m`. Hence every active pair has logarithm ratio strictly greater than one, inactive pairs have zero weight, and since the `b_ij` weights sum to one the derivative is strictly positive on the open bridge. Continuity at endpoints justifies integrating the strict increase to obtain `H(p_m)>H(p_0)` when `m>0` (lines 155-160).

The collinearity and equality cases are also covered. When `m=0`, the midpoint rank is one, so the two endpoint ranges are collinear, `p_{K_0}=q`, and strict concavity of Shannon entropy gives equality only if the endpoint laws coincide. In the collinear rank-one setting, the endpoint laws coincide exactly when `a=b`, equivalent to `K_-=K_+` (lines 162-165). Zero coordinates do not create a missing case because any coordinate with no spectral support has zero `c_i` and no active pair weight, while every pair with `b_ij>0` has positive singleton masses for `0<r<m`.

Legal-kernel conditions are sufficient: the endpoint eigenvalues are `a,b in (0,1)`, and the midpoint is positive semidefinite with trace `(a+b)/2<1`, so every midpoint eigenvalue is below one. This supports the legality assertion in lines 24-32.

## Bit-Flip Lift

STATUS: CORRECT

The affine lift `K^(epsilon)=epsilon I+(1-2epsilon)K` is exact for independent bit flips. Conditional on an original bit, the output bit has generating factor `(1-epsilon)+epsilon z_i` if absent and `epsilon+(1-epsilon)z_i` if present; substituting these diagonal factors into the DPP probability generating polynomial gives the determinant identity in `input/moving_rank1_theorem.md` lines 223-244. The map is affine, so it preserves the arithmetic midpoint as stated in lines 169-181.

Strict spectral legality is correct for `0<epsilon<1/2`: an eigenvalue `lambda in [0,1]` maps to `epsilon+(1-2epsilon)lambda`, which lies between `epsilon` and `1-epsilon`; for the accepted strict endpoint and midpoint kernels it lies in `(0,1)`, matching lines 182-187.

The continuity margin is valid. Under the natural coupling, at least one bit changes with probability at most `delta_n(epsilon)=1-(1-epsilon)^n`, so total variation distance is bounded by this value (lines 246-248). Audenaert's primary source states the sharp continuity bound for dimension `d` as `T log_2(d-1)+H((T,1-T))`, and defines the classical total variation parameter as `T=(1/2) sum_i |p_i-q_i|`; see the arXiv HTML version of `quant-ph/0610146`, lines 75-82 and 108-113. The source uses base-2 logarithms (lines 53-60), while this packet uses `log`; the bound is unchanged after replacing all logarithms by any fixed common base. With `d=2^n`, this is exactly the packet's `omega_n(epsilon)` in lines 198-220. Because `omega_n(epsilon)` tends to zero as `epsilon` tends to zero, every strict boundary gap `G>0` has an explicit sufficiently small accepted range defined by `2 omega_n(epsilon)<G`.

## Static Code Inspection

STATUS: CORRECT

I inspected the code and stored outputs only for interface coherence. I did not run Python, SymPy, entropy arithmetic, interval arithmetic, or remote/formal tools.

The rank-one fixture script states that the symbolic proof is in the markdown and that the script checks one six-coordinate rational fixture (`input/code/verify_rank1_midpoint.py` lines 1-9). Its assertions reconstruct complete atoms, check the mass-transfer bridge for that fixture, check the exact bit-flip identity, and evaluate the displayed margin (lines 107-191). The output reports a single fixture pass and numerical margins (`input/output/verify_rank1_midpoint.txt` lines 1-21). These are coherent with the theorem file's claim that the proof decision uses the analytic continuity bound, not the displayed decimal (`input/moving_rank1_theorem.md` lines 277-299).

The multiring script explicitly labels itself a motivated high-precision probe, not an interval certificate (`input/code/probe_multiring_fixture.py` lines 1-9). Its output repeats the same nonclaim (`input/output/probe_multiring_fixture.txt` lines 1-2 and 89-91). This matches the multiring markdown's status and exclusions (`input/multiring_fixture.md` lines 3-4 and 165-176).

## Finite Execution

STATUS: INCOMPLETE

No independent finite execution was performed. The six-coordinate fixture and dense `3+3` multiring diagnostics remain author-provided illustrations or setup checks only. They are excluded from independent finite certification by instruction and by the packet's own scope (`input/README.md` lines 37-51; `input/multiring_fixture.md` lines 142-176).

## Formal Verification

STATUS: INCOMPLETE

No formal proof assistant, Lean project, interval proof, or machine-checkable formal certificate was inspected or run. No formal correctness claim is accepted.

## Novelty

STATUS: INCOMPLETE

Novelty is not certified. The packet itself labels `prior_art.md` as a literature/scope audit, not a novelty certificate (`input/prior_art.md` lines 1-4), and says correctness and novelty require separate review (`input/moving_rank1_theorem.md` lines 308-310). I used the prior-art file only to understand claimed scope separation, especially lines 8-35 and 74-94.

## Source Use

I used only the frozen author packet in `input/`, the adjacent `input_binding.json`, and Audenaert's primary arXiv page for the Fannes-Audenaert continuity bound. I did not read any C1 first-review report, C2 artifact, other reviewer folder, or `[excluded private directory]`.

Primary external source checked: [Audenaert, "A Sharp Fannes-type Inequality for the von Neumann Entropy", arXiv:quant-ph/0610146](https://arxiv.org/html/quant-ph/0610146).
