# Main-instance replay of the phase-2 numerical self-test

The committed `param_opt/phase2/selftest.py` was replayed with the bundled
workspace Python after the formal run ended. It returned exit code 0 and:

```json
{"status":"PASS","primary_hessian_calls":43,"max_alternate_error":1.4432899320127035e-15,"stratum_cases":32}
```

The replay regenerated the detailed JSON with platform-level floating-point
differences in some last digits. That regenerated file was not substituted for
the frozen run artifact; the original committed detailed result is retained.
