# PR136 S2 independent finite-evidence audit contract

- Frozen author head: `39098dac760cea2d27f2955bed31f80c87913810`.
- Public claim: issue 65 comment `5622666752`.
- Cumulative clock: `2026-09-10T17:20:35.0178305Z` through `2026-09-10T19:20:35.0178305Z`.
- Limits: at most 4 CPU threads, 16 GiB RAM, no GPU; no job expected to exceed 60 minutes.
- Scope: the eight files in `certificate/`, `RESULT.md`, and the arithmetic interface to formulas (11)–(17) in `ENTROPY_KL_C2_TAIL.md`.
- Required fresh production command: `g++ -O3 -std=c++17 -ffp-contract=off -fno-fast-math -fopenmp certify_nodes.cpp -o certify_nodes`, then `certify_nodes nodes.tsv fresh_output.tsv 4 -1 1800`.
- Stop gate: missing compiler, resource/deadline breach, incomplete 128-node evidence, failed normalization, failed exact audit, or any static outward-rounding defect.
- No PR112 work, no analytic C2 correctness verdict, no novelty verdict, no merge.

