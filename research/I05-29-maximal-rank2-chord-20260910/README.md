# I05-29 maximal-chord successor to PR80

Read `RESULT.md` for the self-contained fixed-input and explicit-neighborhood theorem. Status is PROVED at the author-proof/exact-finite-certificate level, PENDING_REVIEW; novelty NOT_ASSESSED. The actual full 64-event law and affine K parameter are retained.

The main claim is `H(K(t))+t^4/24` concave on the **entire maximal legal chord** of the accepted PR58 s=9/10 obstruction fixture and of every member of its coefficient radius 10^-6 and explicit matrix-factor entry box radius 10^-12. Legal endpoints move with the parameters. This is not merely the fixed s=9/10 calculation or a fixed compact subchord.

Run from any directory:

```sh
python3 code/verify_maximal_chord.py
```

Python standard library only. The script finds its input relative to its own file, checks exact Mobius and Schur reconstructions, all three interval bounds and all perturbation margins, and regenerates `output/rational_certificate.json` and `output/complete_event_coefficients.csv`. The saved `output/verify_maximal_chord.stdout.txt` is literal stdout of the retained author execution, not an edited PASS summary. Only runtime depends on the machine.

`SOURCES_AND_FAILURES.md` keeps primary-source hypotheses, two method comparisons, failed relaxations, prior scope corrections, and the distinction between author computation and independent review. No checksum files are used.

After the first local checkpoint, `ADDENDUM_MOVING_ENDPOINT_STABILITY.md` proves uniform simple-endpoint stability and nonempty fully active correlated open classes in every fixed pair of dimensions m,n>=3, on each member's own maximal chord. Those higher-dimensional radii are existential, not the 3+3 numerical radius.

Publication retry succeeded on 2026-09-10: this packet is published on branch `research/I05-29-maximal-rank2-chord-20260910` based on then-current `main` `d5fe8e2d50c45b5f67d29ff3ca82e5e56cf12f3b`. The earlier failed branch-creation attempt is retained as provenance in `REVIEW_HANDOFF.md`; publication itself does not imply independent review, arithmetic certification, or novelty. A review job counts as started only after an explicit issue claim.
