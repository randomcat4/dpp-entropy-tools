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

## Full-dimensional neighborhood corollary

The exact reviewed corollary text has SHA-256

```text
8774578DFF6EF846A725FEE598C7247D0EFA0AB0BF05FFEA26430544D99BA679
```

and is published as
`proofs/equicorrelation_open_neighborhood_corollary.md`.  Two independent
nonauthor contexts returned `CORRECT`; both hashes were unchanged before and
after review.  They checked positive L-ensemble event probabilities,
analyticity on `0<K<I`, openness of negative definiteness, existence of a
convex ball inside the strict domain, strict chord integration, and every
stated exclusion.  This proves an existential full-dimensional neighborhood
around each non-product equicorrelation kernel, not a uniform radius or global
`n=3` concavity.

The reviewed corollary was then frozen without content changes in:

```text
commit 941556fb754134c25d1b53e52500ff509d02626e
tree   dc02d4a272580810015e7244d42b6c93301812a4
blob   6a4aa765d046ed1ebe382f67d56bd89a0ea47cdd
```

Both reviewers independently read that blob with `git show` and recomputed
SHA-256 `8774578D...BA679`; both returned `MATCH/CORRECT`.  Thus their original
mathematical reviews apply byte-for-byte to the public fixed object.

## Infrastructure failures retained

A low-frequency text-only Codex OAuth review attempt timed out after 600
seconds without a verdict.  One reviewer-context wakeup initially met model
capacity and was retried later.  Neither event is a mathematical decision, and
neither changed a reviewed file.

## Commit-bound consolidated review

The consolidated public proof and dependency-free certificate were frozen in:

```text
commit c5aca64cc85c57113db0ea79ebaf65908cedbe90
tree   fff31fdf785675b5c95e5f77628c120af30e000b

proof blob      a0299cc6ec5a7777876007d6561f5dc0e343021c
certificate blob 20356c6590884ef2a1c738874f4cef4724ac2f29
```

Two independent reviewer contexts were instructed to use `git show` on those
fixed objects, not the working tree.  Both returned:

```text
STATUS: CORRECT
```

Both reviewers confirmed that the public consolidation faithfully proves the
two stated results, preserves every parameter and strictness boundary, and
does not claim either general connected `n=3` concavity or the finite chord
that leaves the equicorrelation family.  Each piped the certificate blob
directly from `git show`; both replays returned

```text
PASS: exact rational determinant reduction and positivity rewrites verified
```

with exit code `0`.  Neither reviewer read a same-named working-tree file or
modified repository contents.  One first attempt to query the tree omitted
PowerShell quoting and failed at the shell layer; the reviewer corrected the
query and recorded the tree above.  This did not affect a Git object or the
mathematical verdict.
