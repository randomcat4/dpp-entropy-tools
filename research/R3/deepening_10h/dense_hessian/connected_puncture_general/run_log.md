# U7 bounded research and exact sanity log

Date: 2026-09-08. All computation was local, standard-library only, with no random sampling, server, GPU, dependency installation, or spawned agent. Only this new directory was written.

Command from the repository root:

```text
& 'C:/Users/UIO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' research/R3/deepening_10h/dense_hessian/connected_puncture_general/general_sanity.py
```

Two script executions completed with exit 0. The first checked the cycle and graph identities; the final added the separate exact-event Mobius gate. Final elapsed time: 0.2434694766998291 seconds. No finite test failed.

Frozen finite denominator/scope accounting:

- Eight cycle lengths m=3,...,10: the squarefree full-product coefficient of -M log M was extracted with exact fractions and found to be -1. Every power contribution is retained; adding the independently derived oriented-cycle contribution -2 gives -3.
- Five cycle lengths m=3,...,7: all m! determinant permutations were compared with the matching-plus-two-orientations formula.
- Five n=6 marked-coordinate jets: P6 endpoint distance 5; P6 mixed distances 5 and 3; C6 opposite vertices with two shortest paths; C6 distinct distance-3 coordinates; C6 mixed distances 3 and 2. Diagonal parameters remain arbitrary through formal independent vertex moments. Support weights are the fixed rationals (-1)^i*(i+1)/(2i+3), i=0,...,4, and C6 adds A_16=6/13. Each retained coefficient and its full denominator is in JSON. These are finite SCOUT identities, not the arbitrary-weight proof.
- One deliberately dangerous residual-support configuration: two disconnected support edges with weights 2/3 and -3/5, and two connecting marked chords. Every mixed-Hessian coefficient through residual degree 6 cancels, although a monomial with degree four at each vertex is combinatorially possible. This demonstrates why the minimum-degree rule alone is insufficient.
- One dense n=4 direct-Mobius gate: all 16 exact atoms equal the likelihood-character reconstruction, sum to one and remain positive. Exact diagonals, perturbation variables and every atom fraction are retained.

An initially contemplated proof shortcut was rejected before drafting the candidate: the minimum-degree-four rule alone does not force the residual graph to contain either marked pair's long path. Two chords can link disconnected remote pieces. The repaired route explicitly proves full Hessian block locality before extracting residual-support constraints. This is a failed argument, not a counterexample to the frozen claim.

Source SHA256:

`46e075f8dc25814bbe5ab5571bc671552ecd740f8fb87bc93644b5837e5e0970`

sanity_results.json SHA256:

`c288bc03bf9d63ec17e382d4ae61fc2c2cb851d259718407d2b04d7c637bd16d`

The JSON includes elapsed time, so its raw file hash can change on rerun even when all exact witness fields agree. No author or verifier module from another research directory is imported. The prior U5 materials informed the question, but the candidate proof reproduces its required exact-event and disconnected lemmas self-containedly.

Skill usage: math-theorem research/proof workflow, with the parent retaining claim ownership and independent certification. No Lean or proof-assistant certification is claimed.
