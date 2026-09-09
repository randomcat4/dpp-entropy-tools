# C2 issue52 computation report

## Verdict

This original arithmetic attempt produced a scoped successful derivation check
but no global sign certificate and no rational negative obstruction.

The run exited cleanly at the wrapper level, but both factor stages stopped
early with the same implementation error:

```text
TypeError('Object of type Integer is not JSON serializable')
```

That error happened after the first leading minor of the four-variable
`Rstar` matrix was computed and factored.  It is not a mathematical sign
failure.

## Launch

- Arithmetic PID: 172454.
- Wrapper start: 2026-09-09T11:22:28Z.
- Wrapper finish: 2026-09-09T11:54:46Z.
- Wrapper exit code: 0.
- Total script elapsed time: 1938.017 seconds.
- Limits: one arithmetic Python process, one-thread environment, 16 GiB
  virtual-memory cap, no GPU, one 2700-second outer deadline.

The executed source was the copy launched at 2026-09-09T11:22:10Z.  The current
public script differs from that executed source by one privacy sanitation line:

```text
cwd=os.getcwd()  ->  cwd_record="present but not stored"
```

## Completed Derivation Gate

`lambda_zero_M.json` reports `all_derivation_checks_ok=true` after
1827.455 seconds.  The completed exact checks were:

- all eight atom probabilities from inclusion determinants;
- all eight first jets;
- pair Fisher split;
- complete Fisher identity;
- formal log-acceleration coefficient identity;
- `Q` from the sparse log-derivative matrix using the stated `n1,n2,n3`;
- initial negative Hessian `diag(v,w,4,0,0,0)`;
- common denominator clearing by `8*(1-u^4)^2*(1-r^2*u^4)^2`.

Scope limitation: the launched machine check used the stated `n1,n2,n3`
formulas when assembling `Q`.  It did not independently differentiate the
Lambda-zero log products from the atom probabilities.  The separate formula
review covers that algebra, so this run should be cited as a scoped machine
check, not as a standalone complete derivation of every log-product derivative.

## Factor Stages

The script used the structure reduction before determinant work.  It saved
raw six-by-six cleared-matrix checkpoints, then formed `Rstar` and its
pre-minor checkpoint for both `r=0` and full `r`.

For `r=0`, it saved only:

```text
minor_1_det.txt
minor_1_factored.txt
r0_Rstar_pre_minors.json
```

For full `r`, it saved only:

```text
minor_1_det.txt
minor_1_factored.txt
full_Rstar_pre_minors.json
```

No second, third, or fourth leading principal minor was attempted in this
original run after the JSON serialization error.  Therefore there is no
Sylvester certificate for `Rstar`, no determinant nonvanishing certificate, and
no inertia-continuation result from this attempt.

## Sanitized Artifacts

The public sanitized outputs are under:

```text
research/C2/lambda_zero52/compute/outputs_sanitized/
```

The raw copied run is retained only in the private compute area because the
launch-time JSON includes private runner path fields.
