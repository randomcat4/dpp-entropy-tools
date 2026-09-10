# Local run metadata

| Stage | Exit | Wall seconds | CPU seconds | Peak working set | Threads / affinity |
|---|---:|---:|---:|---:|---|
| Build attempt 1 | 1 | 3.177 | not sampled | not sampled | compile only |
| Build attempt 2 | 0 | 2.934 | not sampled | not sampled | compile only |
| Node-0 pilot | 0 | 0.955 | 0.516 | 5,877,760 bytes | 1 / `0x3` process mask |
| Full 128-node production | 0 | 66.315 | 109.359 | 5,799,936 bytes | 2 / `0x3` |
| Frozen author fresh check | 0 | 0.184 | not sampled | not sampled | Python library threads 1 |
| Independent exact fresh audit | 0 | 145.013 | 122.391 | 20,987,904 bytes | 1 / `0x1` |

Production environment controls included `OMP_NUM_THREADS=2`,
`OMP_THREAD_LIMIT=2`, `OMP_DYNAMIC=FALSE`, and one thread for BLAS-family
libraries.  `CUDA_VISIBLE_DEVICES=-1`; no GPU was used.  The full production
process ran at `BelowNormal` priority.  The independent audit used one logical
CPU at the same priority.

The author-program summary reports `max_rss_kib=0` because the Windows-only
compatibility header intentionally stubs POSIX telemetry.  The table uses
external `PeakWorkingSet64` samples instead.
