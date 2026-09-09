# C2 issue52 computation attempt ledger

## Scope

This compute subtree implements the frozen issue52 Lambda=0 six-direction
radial derivative contract.  It reconstructs the eight DPP atom jets from
inclusion determinants, verifies the literal formula

```text
M = derivative_u(Fmat) + Q
```

and then uses the four-variable Schur-complement reduction before any raw
six-by-six determinant attempt.

## Launch record

- Arithmetic process PID: 172454.
- Wrapper PID: 172441.
- Timeout guard PID: 172453.
- Authoritative wrapper start: 2026-09-09T11:22:28Z.
- Authoritative outer deadline: 2026-09-09T12:07:28Z.
- Outer wall ceiling: 2700 seconds.
- Internal script wall budget: 2640 seconds.
- r=0 target slice: about 600 seconds, reached only if the derivation gate
  finishes first.
- Resource limits: one Python arithmetic process, one-thread numerical
  environment variables, 16 GiB virtual-memory limit, CPU affinity requested
  where available, no GPU.

## Source provenance

The executed server source was copied at launch time.  The current public
`verify_i05_22_lambda_zero.py` differs from that executed source by one privacy
sanitation line only:

```text
cwd=os.getcwd()  ->  cwd_record="present but not stored"
```

Raw run JSON from the launched process may contain the private runner working
directory and must remain private or be sanitized before publication.  The
public script is the portable version to keep future outputs path-clean.

## Final observed state

The wrapper exited with code 0 at 2026-09-09T11:54:46Z.  The derivation gate
completed successfully and wrote `lambda_zero_M.json` with
`all_derivation_checks_ok=true`.

Both factor stages then failed with:

```text
TypeError('Object of type Integer is not JSON serializable')
```

The error occurred after `minor_1_det.txt` and `minor_1_factored.txt` were saved
for each case.  No second, third or fourth leading principal minor was reached,
and no global sign certificate or exact rational obstruction was produced.

Sanitized copies of the completed outputs are in `outputs_sanitized/`.  The raw
run copy remains private because the launch-time JSON contains private runner
path fields.
