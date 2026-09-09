# PR53 second independent review — frozen scope

Review status: **FROZEN / NOT YET REVIEWED**.

Frozen author head: `e0688fbb713e55f93acf791b83437ddf2cc06b7f`.

Source directory:

`research/I05-DPP-21-20260909/`

Files in scope:

1. `proof.md`
2. `README.md`
3. `sources.md`
4. `code/probe_balanced_beamsplitter.py`
5. `output/balanced_beamsplitter_probe.json`

Review focus:

- parity reordering and exact mutual-information rate normalization;
- complete-event likelihood and the full `J' + 2sJ''` sign obligation;
- configuration-uniform finite-range inverse and exponential decay under strict spectral margin, not only Wiener smallness;
- balanced fermionic beam-splitter reduction and the distinction between quantum von Neumann entropy and occupation Shannon entropy;
- open boundaries: global rate concavity, remaining volume-uniform signed-curvature/occupation inequality, general nonconstant centers, endpoints, phase loss under measurement, and finite floating diagnostics.

Rules:

- Do not read C1's first review/report/code/conclusions.
- Do not use other author private code.
- Do not use PR54 or C2 issue #52 work.
- Do not run broad scans.
- Do not access excluded private workspaces.
- Do not write to GitHub or publish.
- Analytic review is preferred. If a narrow exact check becomes essential, write a frozen object/plan first and keep it to one local thread, no GPU, target 4 GiB RAM, and 15 minutes.

Output:

Write `review_report.md` in this directory with source-line references, actual checks, verdict, and precise limits.
