# Public execution-path normalization

C3's integration follow-up to source commit a063ec6d3f9b2887ac72739ebd9d07b606f70246 normalizes machine-specific absolute execution paths in twelve public report, runner and metadata files. `[C2_EXECUTION_ROOT]` represents the private assigned execution directory; it is a metadata placeholder, not a literal runnable path. Unsanitized records remain in C2's private recovery copy and historical outcomes/PIDs/versions/errors are retained.

The two shell entry points now default to `python3` while preserving the `PYTHON_BIN` override. The PR43 runner defaults to its own directory and invokes the checker at its actual public location; `RUN_ROOT`, `SOURCE_ROOT` and other overrides remain available. Both shell files passed `bash -n`. This is an entry-point portability change, not a rerun of mathematics.

All Python mathematical verifiers, frozen inputs, flow certificates, exact probability tables and review conclusions are unchanged. JSON differences are confined to the existing path-bearing strings; all numeric values and other structure are preserved. No failed or interrupted computation has been removed. The source-publication binding in `pr43_flow_review/PUBLIC_BINDING.md` still applies to the unchanged `pr43_flow` subtree.
