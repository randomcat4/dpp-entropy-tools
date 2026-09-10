# DPP32: the fixed macroscopic true-entropy-rate interval

Date: 2026-09-10. Status: **AUTHOR_PROOF / AUTHOR_CERTIFICATE_PASS / PENDING_INDEPENDENT_REVIEW**. No independent reviewer acceptance, merge, novelty or formal verification is claimed.

## Theorem

For the stationary Toeplitz DPP with

    f_t(theta)=1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8,
    1/2 <= t <= 3/2,

let h(t) be the COMPLETE-CONFIGURATION Shannon entropy rate, with natural logarithms, per ORIGINAL lattice coordinate. Then the author's proof and executed certificate establish

    h''(t) < -1/3000                                      (T)

on the entire closed parameter interval. The correlation kernel K_t is affine in t. No spectral entropy, affine L-kernel substitution, omitted vacancy event, fixed-state-only Fisher information, or deleted acceleration is used.

This resolves the specified interval at the AUTHOR level only. It does not prove convexity of parity mutual information in s=t^2/256, the entire maximal legal parameter interval, general scalar entropy-rate concavity, or general finite real-kernel concavity.

## The new analytic bridge that makes the computation finite

The main proof is [ENTROPY_KL_C2_TAIL.md](ENTROPY_KL_C2_TAIL.md). It depends on the scoped accepted PR91 complete-event representation and explicit coding-jet bounds, not on PR112's failed wide-interval certificate or on PR115's unreviewed finite-window signs.

Write Y_j=(X_(2j),X_(2j+1)) and h_r=(1/2)H(Y_0|Y_1,...,Y_r). The complete KL increment delta_n=2(h_(n-1)-h_n) satisfies the exact differentiated identity

    delta_n'' = sum_w [p_n F_w'' + 2 p_n' F_w' + p_n'' F_w],
    F_w = KL(g_n(w) || g_(n-1)(w)).                       (1)

Full finite-word Fisher and acceleration estimates give

    sum_w (p_n')^2/p_n <=3n,
    sum_w |p_n'|<=sqrt(3n),
    sum_w |p_n''|<=9n.                                  (2)

Differentiating the quadratic Bregman representation of KL, rather than differentiating a value bound, yields

    |delta_n''| <= lambda^(n-1) P(n-1),
    lambda=(34/81)^2,
    P(m)=(1809918/180625)m^2
          +(154889893499/5135349375)m
          +342449808326286961/15178486401000000.          (3)

The zeroth, first and second derivative series are uniformly absolutely summable. Thus the limit is genuinely C2, and

    |h_r''-h''| <= E_r=(1/2)sum_(m=r)^infinity lambda^m P(m). (4)

The rational geometric-sum expression in the proof gives E_9<115/10^6. This is a uniform rate-derivative tail theorem for all depths, not an extrapolation of a sequence of finite curvature samples. PR91 supplies an actual C2 physical response on a neighborhood of the closed target interval; alternatively the strict coding estimates extend with slightly perturbed constants. Hence endpoint derivatives are covered, not only open-cell limits.

The initial Neumann work in [HIGH_ORDER_CLOSURE.md](HIGH_ORDER_CLOSURE.md) separately closes the previously missing state bounds uniformly in m, giving |D_Q A_m|<1153. Its literal depth-120 scalar evaluation is not needed for (T): the entropy-specific bridge (1)-(4) reduces the proof to one fixed memory r=9.

## Finite computation plus analytic coverage, not a grid claim

At r=9, h_9=(H_20-H_18)/2. Four closed cells cover the interval:

    [1/2,3/4], [3/4,1], [1,5/4], [5/4,3/2].

For each cell, 32 first-kind Chebyshev nodes were enclosed using exact rational pi/cosine constructions. At each node the production source enumerated all 4^9 complete future words and all four current-cell outcomes, propagating full second-order jets of both the state and its changing probability law. There are 4^10 complete current/future entropy contributions per node.

For each cell the proof supplies a zero-free complex event-determinant neighborhood containing the Bernstein ellipse rho=3, and the bound |h_9''(z)|<40000000. The degree-31 interpolation error is therefore at most

    6*40000000/3^32 = 80000000/617673396283947.             (5)

This bound follows from analytic Chebyshev coefficient estimates and exact aliasing. It covers the endpoints and every point between the nodes.

The exact rational DCT audit bounds each interpolation polynomial by upper(c0)+sum_(j>=1)maxabs(cj), then adds (5) and E_9. The resulting true-rate upper bounds, rounded UPWARD for this table, are

| Closed cell | Rigorous upper bound on h'' |
| --- | ---: |
| [1/2,3/4] | -37469/100000000 |
| [3/4,1] | -103064/100000000 |
| [1,5/4] | -195772/100000000 |
| [5/4,3/2] | -317121/100000000 |

Every table entry is strictly below -1/3000. The unrounded weakest bound is approximately -0.0003746944028546811. The exact original result JSON and all coefficient intervals can be reconstructed from the public raw data by the public audit source; no unprovided production program is needed.

## Public production source and evidence

All paths below are under certificate/.

- `make_inputs.py`: the actually executed rational input generator. Machin pi bounds, cosine Taylor remainders, outward dyadic conversion, rational verification of log(2) and the atanh remainder. It reconstructs all canonical input values; elapsed-time metadata naturally changes on another run.
- `certify_nodes.cpp`: the actually executed production source, not a replacement scout. Binary64 endpoints are padded outward after arithmetic operations. It uses no library logarithm or trigonometric evaluation: log is a rationally bounded atanh series with an explicit tail. Jets are ordinary Taylor coefficients, so the t^2 coefficient is half the second derivative. The per-original-coordinate factor 1/2 is explicitly handled in the leaf formula.
- `node_output.part0.tsv` through `node_output.part3.tsv`: lossless consecutive byte pieces of the literal saved output after the publication corrections documented below. Concatenation produces all 128 original rows, in actual completion order. Each row includes both curvature endpoints, zeroth/first/second normalization-jet enclosures, its measured time and leaf count.
- `check_certificate.py`: the actually executed exact-Fraction audit, reconstructing the KL tail polynomial, infinite tail, complex bound and DCT coefficient intervals. It verifies complete node IDs, all leaf counts, normalization jets, and the four strict inequalities against -1/3000.
- `certificate_summary.json`: a derived short-rational summary, NOT literal stdout. Full exact coefficient/result fractions are reconstructed by the audit. The original input/output JSON, TSV and literal execution logs are also retained in the chat evidence ZIP.

The three executed sources and four final public raw-data parts were matched to the original local files using their native Git blob identities. Local concatenation of the four parts is byte-for-byte the original 25414-byte raw output. This is source binding, not an independent mathematical review.

### Audit from saved data, without re-enumerating DPP events

From the certificate directory:

    python make_inputs.py
    cat node_output.part0.tsv node_output.part1.tsv node_output.part2.tsv node_output.part3.tsv > node_output.tsv
    python check_certificate.py

The last command writes the full `certificate_result.json`, including every exact coefficient enclosure. With the supplied ZIP inputs already present, the first command is unnecessary. This audit does not repeat the production computation.

### Optional independently authorized production reproduction

    g++ -O3 -std=c++17 -ffp-contract=off -fno-fast-math -fopenmp certify_nodes.cpp -o certify_nodes
    ./certify_nodes nodes.tsv NEW_output.tsv 4 -1 1800

Use a NEW output path for a genuinely independent run. The program skips node IDs already saved in its output. It flushes after each completed node, stops starting new nodes after the specified wall cap, and returns distinct failure/stopped codes. Any resumed run must keep the exact source/input and use only its authorized remaining budget. No old issue74/PR112 budget is assigned by these reproduction instructions, and no outside execution is claimed to have started.

## Actual resource record and failures

The new author production had a one-node pilot (ID31) followed by the remaining127 nodes; ID31 was not repeated. The pilot used 1 thread, wall 0.708781524 seconds, CPU 0.708747 seconds, max RSS 1960 KiB. The remaining batch used 4 threads, wall 21.92962432 seconds, CPU 86.285293 seconds, max RSS 2088 KiB. Both reported stopped=0, failed=0. Measured production totals are wall 22.638405844 seconds and CPU 86.994040 seconds, excluding compilation and input generation.

The rational input generator recorded wall 25.557354703 seconds; its CPU and memory were not separately recorded. The successful rational audit recorded wall 0.047477772 seconds, CPU 0.047479484 seconds, max RSS 92968 KiB. Small exploratory scalar-constant calculations and compilation were not separately timed. Do not mistake the measured production totals for total interactive research time.

Environment: x86_64, g++ 14.2.0 (Debian 14.2.0-19), Python 3.13.5. Production used IEEE binary64, round-to-nearest, no fast-math or fused contraction, at most4 CPU threads, no GPU. No >60-minute job was needed or initiated, and no previous finite-window/scout computation was rerun. The production process was confirmed no longer running.

Preserved failures: an interactive terminal request failed before execution because streaming sessions were unavailable; the normal invocation succeeded. The first audit source had `ndef p_scale` and stopped with SyntaxError before arithmetic; deleting the extra `n` repaired it, and no production node was rerun. A direct raw-GitHub download for byte comparison failed at DNS; connector/native-Git source binding was used instead.

Publication corrections, retained in Git history: initial part1 ID59 and part3 ID97 normalization fields each acquired one extra zero during text transfer. The first part1 restoration also introduced a one-character ID48 curvature-endpoint copy error. All three fields were restored from the unchanged original output, and final source/data bindings match. The initial long-fraction summary also had a mistyped intermediate denominator; it was replaced with independently exact-compared short rational UPPER bounds. Neither the original production files nor the executed rational audit/result was changed by these publication errors. None is concealed as a successful first upload.

## Review boundary

Suggested independent review units are: (i) complete KL identity and two differentiated future-law terms; (ii) quantitative finite jet/Fisher/acceleration tail and actual C2 convergence; (iii) event-determinant analytic continuation, ellipse coverage and aliasing error; (iv) the binary64 enclosure kernel, exact input generation and full finite evidence. The higher-order Neumann lemma is separable and not a premise of the final interval certificate.

This file supersedes checkpoint statements that the new scalar gate had not yet been computed; it does not retroactively upgrade PR112, PR115, PR98 or any old output. The entire new theorem remains pending independent review.
