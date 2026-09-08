# Reproduction and source binding

Use a fresh checkout and private environment: Python3.12.3, NumPy2.5.3,
SciPy1.18.1, mpmath1.4.1. Set OMP_NUM_THREADS, OPENBLAS_NUM_THREADS,
MKL_NUM_THREADS, NUMEXPR_NUM_THREADS to 1. No GPU; at most two concurrent
single-thread jobs were used. From the repository root:

```
python research/N4/pilot.py --out <new-output-directory>
python research/N4/search/bounded_search.py --out <new-output-directory>
python research/N4/search/diamond_gain.py
python research/N4/search/diamond_interior.py
python research/N4/review/rational_dpp_review.py --out <new-smoke-json> smoke
python research/N4/review/rational_dpp_review.py --out <new-benchmark-json> p2-benchmark --p2-terms 120
```

Some scripts use fixed output paths: run in a fresh disposable checkout and
preserve delivered evidence. Child ledgers give precision replay and JSON
rationalization commands. A changed seed/precision is a new run.

The following four compute-manifest source hashes were compared directly to
immutable Git blob bytes on 2026-09-09; all matched exactly:

| Script | SHA256 |
| --- | --- |
| pilot.py | a0f97256a985f71ffedecf2c0fdeb09ad7d9e5b712d25c6391d61946fe69489e |
| search/bounded_search.py | fb5a5239d1ec0e3ce06d294d9d954d41beb535d8d3dd3c3a497c3456179f5da1 |
| search/diamond_gain.py | 0d92e541fab0ffdc8e5a9d80ff7f78ddc36e05ec3e34da50f155f965bb602fce |
| search/diamond_interior.py | bcda670a9bc9080159660724f41305da523b0b313f4be98f845fdc9e8fdb07bb |

The P1 imported baseline source hash is in pilot_results/manifest.json.
The independent reviewer imported neither author implementation. Its early
script bytes were not saved separately before the P2 extension; the exact
limitation and interrupted attempt are in review/run_ledger.md.

Direct Git HTTPS transport was unavailable. Publication used GitHub's Git Data
API and checked equality of the complete remote/local source tree. Publication
commits reference the local source commit; immutable proof blobs are preserved.
TLS verification was not disabled. Private transport files are not public artifacts.
