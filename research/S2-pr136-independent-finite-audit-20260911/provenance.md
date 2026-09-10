# Provenance and execution record

- Public claim: issue 65 comment `5622666752`.
- Clock: `2026-09-10T17:20:35.0178305Z` to fixed deadline
  `2026-09-10T19:20:35.0178305Z`.
- Host: Windows 11 `10.0.26200`; Python `3.12.14` at the bundled workspace
  interpreter; four-thread environment ceiling, no GPU.
- Git transport to the frozen commit failed before checkout. The exact tarball
  was then streamed through the authenticated GitHub API and only the ten
  authorized files were extracted. Their eight certificate Git blob hashes
  were independently recomputed and match PR136.
- Input generation: PID 31632, exit 0, wall 14.005 seconds, empty stderr;
  generated 65 cosine bounds and 128 nodes.
- Frozen saved-data checker: PID 52596, exit 0, wall 0.218 seconds, empty
  stderr. A local module shim supplied only `resource.getrusage` telemetry,
  absent on Windows; the frozen checker bytes and every mathematical value and
  predicate were unchanged.
- Independent audit attempt 1 is retained. It stopped before DCT at the
  independent checker's invalid monotonic treatment of the `cos(pi)` endpoint.
- Independent audit attempt 2: exit 0, 126.618 seconds, empty stderr.
- Compiler probes `where.exe g++`, `clang++`, `c++`, and `cl.exe` all returned
  absent. No dependency was installed and no production output was fabricated.

