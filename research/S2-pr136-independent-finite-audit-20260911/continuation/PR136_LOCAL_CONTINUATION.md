# PR136 finite certificate: local production continuation

## Frozen object and scope

- Exact author head: `39098dac760cea2d27f2955bed31f80c87913810`.
- Scope remains only the eight certificate files plus `RESULT.md` and their
  arithmetic interface to formulas (11)--(17) in `ENTROPY_KL_C2_TAIL.md`.
- This continuation does not review the analytic C2 proof, novelty, or merge
  suitability.
- The first PR139 commit remains the historical saved-data audit and records
  the then-missing local compiler.  This second phase adds a fresh production
  run; it does not rewrite that history.

## Local toolchain and portability boundary

The previously available remote compute endpoint was unavailable, so the run
was performed locally after a single-node pilot.  A task-local, portable
WinLibs GCC was used without administrator privileges or a global `PATH`
change:

- compiler: GCC 16.2.0, MinGW-w64 UCRT POSIX SEH, WinLibs r1;
- release: `16.2.0posix-14.0.0-ucrt-r1`;
- downloaded archive SHA-256:
  `C1F52294597C0B73786B2A78EB5D176D89226D2F21875EAB75E783A8B1CEFCC4`;
- author source SHA-256:
  `4D50597FA934852E5C2ED309D7C94379970FF1692E7FC55A8F397B0D6AD94208`;
- compiled executable SHA-256:
  `4142A18A68CD69C0858E331DFA1DCC85CB7F529B916968448B9FED46FEE57FF3`.

The frozen author source includes POSIX `sys/resource.h` only to print peak
RSS.  The first unmodified Windows build therefore failed at that missing
header, as retained in `logs/compile_attempt1.stderr.log`.  The successful
build left the author source byte-identical and added an include path with the
committed `portability/sys/resource.h`.  That compatibility header supplies
only `getrusage`/`ru_maxrss=0`; external process monitoring records memory.
No interval arithmetic, input, predicate, or production control flow is
changed.

Successful build flags were:

```text
-O3 -std=c++17 -ffp-contract=off -fno-fast-math -fopenmp -I portability
```

## Resource-bounded production

Both production processes ran at Windows `BelowNormal` priority with explicit
processor affinity.  GPU use was disabled and unrelated library thread counts
were set to one.

The node-0 pilot used one thread and one of the allowed cores.  It exited 0 in
0.955 seconds wall / 0.516 seconds CPU with a 5,877,760-byte peak working set,
one complete row, `stopped=0`, and `failed=0`.

The fresh full run used exactly two threads and affinity mask `0x3`.  It ran
from `2026-09-10T17:54:11.9953948Z` to
`2026-09-10T17:55:18.3099312Z`, exiting 0 after 66.315 seconds wall and
109.359 seconds total CPU.  External peak working set was 5,799,936 bytes.
The output contains all 128 unique node IDs and has SHA-256
`9F35777945F45EF205DD8B1297F3126DC1902F064163D680C87BE9E0709508F4`.
The program reported `threads=2 stopped=0 failed=0`.

Each row certifies all `4^9 = 262144` future words and all four current
outcomes, hence `4^10 = 1048576` complete current/future atoms per node.

## Exact author audit of fresh output

The frozen `check_certificate.py` and `certificate_inputs.json` were copied
byte-for-byte into an isolated check directory.  A Windows Python `resource`
shim again changed only unavailable process telemetry.  The checker exited 0,
verified 128 nodes and returned these four exact-gate decimal upper bounds:

```text
[-0.0003746944028546811,
 -0.0010306469749631383,
 -0.0019577212125145367,
 -0.0031712104741915452]
```

All are strictly below `-1/3000`.  The exact tail was

```text
589387328229019964285617091244680106481903343765504 /
5143466080331011979778316775380842071512247021978203125
```

which is approximately `0.0001145895236838209 < 115e-6`.

## Independent exact audit

`independent_fresh_audit.py` does not import the author checker.  It reuses the
previously published S2 independent primitives to regenerate exact rational
Machin/atan and cosine enclosures, validate all 65 cosine intervals, validate
`log(2)` and all 128 Chebyshev nodes, parse the fresh output, reconstruct the
tail, and propagate all four DCT cells.

It also parsed the four saved author parts and made 512 explicit interval
intersection checks: one curvature interval and three normalization-jet
intervals at each of 128 nodes.  Every fresh interval intersects its saved
counterpart.  The independent process ran on one core at `BelowNormal`
priority and exited 0 after 145.013 seconds wall / 122.391 seconds CPU, with a
20,987,904-byte external peak working set.

## Verdict

**PASS within the frozen finite-evidence scope.**  Fresh input generation,
fresh full 128-node production, the frozen author exact checker, the separate
exact Fraction audit, saved/fresh interval correspondence, tail propagation,
and all four continuum gates pass.  This closes the compiler/reproduction
gap recorded in the first PR139 commit.  It makes no claim about the analytic
C2 argument or novelty.
