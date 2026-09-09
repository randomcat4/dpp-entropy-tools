# Reproducing the bounded computations

Use the frozen upstream sources listed in README.md. The source directories below mean the author packet at those exact commits, not a moving branch. Use a fresh output directory for each replay so the original published evidence is preserved.

The symbolic/event verifiers use Python 3.12.3 and SymPy 1.14.0. The flow certificate checker uses only the Python standard library; rerunning LP discovery is unnecessary for checking the certificate. The supplied shell wrappers record invocation, process identifiers, exit status and resource bounds for a server run. Do not relaunch an existing job without first checking its recorded PID.

From this packet's directory, with the two source placeholders replaced by the corresponding frozen packet directories:

```sh
python pr41/verify_pr41_independent.py --source-round2 /path/to/PR41/research/N3/round3/I05-W4-20260909/round2 --out replay_pr41/evidence.json

python pr43_events/standalone_pr43_events.py --source-root /path/to/PR43/research/I05-W1-20260909-R2 --out-dir replay_pr43_events

python pr43_flow/verify_pr43_flow.py --certificate pr43_flow/flow_certificate.json --write-summary replay_flow_summary.json

python pr43_flow_review/verify_pr43_flow_independent.py --certificate pr43_flow/flow_certificate.json --instance pr43_flow/instance.json --output-dir replay_flow_independent
```

The first two commands replay the relevant author verifiers as well as their independent reconstruction. PR43's root verifier is intentionally outside this packet because C1 owns that fixture. The full PR43 event evidence retains all three 256-event tables, conditional tables and strict-legality certificates. A completed checker is evidence within its declared domain, not certification of unrelated analytic or novelty claims.

See each unit's report for the actual recorded run, failures and exact source-line checklist. The fourth command uses the fresh review's separate implementation to reconstruct the generator directly from the rational certificate.
