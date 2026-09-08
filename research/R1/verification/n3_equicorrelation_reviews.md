# Non-author reviews: three-dimensional equicorrelation results

## Reviewed private candidates

The proof was developed as three separately hashed candidate files:

```text
standard block
7FBAECC946BF5ECD9A5B9A485F0AC4D3F2F2E030A69AB3F6CB93B23D7C694B23

trivial block
9D93B8A0A17E1DD458618B3F2EDE48CE10A0030A3FC60BDB00219A5478AC450E

strict family-chord corollary
F9F1DF0CFBBC07DA1993F03B82A1E14C9EBB812E613CCFFC14BE04C5A83C196D
```

The public proof `proofs/n3_equicorrelation_hessian.md` consolidates those
three reviewed arguments.  A separate commit-bound review of that consolidated
blob is recorded below after the freeze commit is created.

## First independent review

Reviewer context: `param_opt`, which did not author the candidate proofs.

```text
STANDARD: CORRECT
TRIVIAL:  CORRECT
```

The reviewer independently checked the complete-event and Fisher formulas,
the standard mixed term, complementation, monotonicity in `W`, the `q0,q1`
factorizations, the fixed-odds determinant substitution, the quartic Bernstein
reduction, every inequality direction, boundary equalities, and the final
two-by-two inertia arguments.  The dependency-free exact certificate was only
an auxiliary check.  Both candidate hashes were unchanged by the review.

The same reviewer then separately checked the family-chord corollary and
returned:

```text
COROLLARY: CORRECT
```

It verified convexity of the parameter domain, affinity and injectivity of the
kernel map, the single intersection with the degenerate line, the strictly
negative `(u,u)` curvature for a chord contained in that line, and the weighted
second-derivative integration.  The corollary hash was unchanged.

## Second independent review

Reviewer context: `certificate`, which did not author the candidates and was
instructed not to use the first verdict.

```text
STANDARD:  CORRECT
TRIVIAL:   CORRECT
COROLLARY: CORRECT
OVERALL:   CORRECT
```

This reviewer reread all three candidates and their reduction dependencies,
checked the exact replay with exit code `0`, and manually audited the same
algebraic and analytic boundary points.  It noted that the standard proof's
compressed `sigma=1` strictness is explicitly
`F=9(1-lambda)^2>0` for `lambda<1`.

Neither review promotes the still-open arbitrary-direction finite-midpoint
claim at an equicorrelation center, nor general connected `3 x 3` concavity.

## Infrastructure failures retained

A low-frequency text-only Codex OAuth review attempt timed out after 600
seconds without a verdict.  One reviewer-context wakeup initially met model
capacity and was retried later.  Neither event is a mathematical decision, and
neither changed a reviewed file.

## Commit-bound consolidated review

Pending the freeze commit.  This section is updated only after reviewers read
the fixed Git objects rather than the working tree.
