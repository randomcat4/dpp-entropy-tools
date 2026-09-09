# Reproduction and artifact scope

Use fresh output directories; do not overwrite retained research evidence.
Scouts require Python, NumPy, SciPy and mpmath; reviewer scripts use the
standard library. Versions, commands, hashes and PIDs are in the manifests.

From the corresponding script directory:

```text
python face_search.py --out F1_replay
python face5_search.py --out F2_replay
```

Scouts fix frame/spectrum sets and seeds in source. Set OMP_NUM_THREADS,
OPENBLAS_NUM_THREADS, MKL_NUM_THREADS and NUMEXPR_NUM_THREADS to 1.
Postprocessing uses its named retained directories; inspect output names
before replaying. The pilot writes under its own results directory, so copy
that directory to a fresh location before replay. Its original manifest
has a documented entropy-call accounting correction.

Reviewer scripts accept output arguments. The coarsening checker additionally
takes a source repository and frozen main commit. Read review/run_ledger.md
for actual calls. A history-preserving author checkout is needed for that
commit. Public API transport has different commit history but the same full
tree; verify frozen blobs in proofs/index.md when author commits are absent.

Exact rational support and PD checks certify finite algebraic claims.
Logarithm interval comparisons certify only the stated finite signs.
Scouts and structural validation do not establish a general theorem.
Original certificate decimals are approximate; use the presentation
supplement for outward rational enclosures.

No automatic job or larger batch is part of reproduction. The checkpoint
specifies the mathematical obstruction a new unit must attack.

