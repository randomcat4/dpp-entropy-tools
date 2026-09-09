# Main review of W4 certificate interval arithmetic

This note concerns the independent checker implementation, not the
author's universal proof or the theorem verdict.

The first minimized checker run returned PASS numerically, but its
`d_div_pos` formed reciprocal endpoints using the default Decimal context.
The main reviewer identified this as an enclosure failure: ordinary
rounded division does not guarantee an outward interval. That run and
script are rejected as strict certificate evidence and are retained in
`children/w4/rejected_interval_attempt_default_reciprocal/`.

The corrected code computes `1/b_upper` in a 90-digit local context with
`ROUND_FLOOR`, and `1/b_lower` in a separate 90-digit local context with
`ROUND_CEILING`, before interval multiplication. The main reviewer checked
the actual corrected implementation. Rational atanh-series log bounds are
converted outward to Decimal intervals; interval addition, subtraction,
multiplication and squaring also use explicit outward rounding. Positive
interval LDL pivots then certify the selected residual matrix is positive
definite. Where the graph is disconnected, excluded null rows are checked
symbolically rather than inferred from small floating eigenvalues.

The same seven fixed centers were rerun after the fix, with PID 169057,
exit 0, one thread, 8 GiB memory limit, and 240-second timeout. Each passed.
The report stores complete Decimal lower endpoints; rounded scientific
notation and floating eigenvalues are explicitly diagnostic. No new
centers were added to obtain a favorable result.

This supplies strict finite-center certificate evidence only. Universal
W4 acceptance must rest on the separate analytic proof review. The earlier
full computation timeout, exit 124, is also retained and does not count as
a mathematical counterexample or a completed certificate.
