# Verification and claim boundaries

Global B0: NOT PROVED. No counterexample is certified.

## Authorship

Main rebuilt the structural formulas and derived the exact tilt equations.
Geometry authored both asymptotic proofs. Main independently identified the
missing common-event cross in the first sparse model and checked the corrected
scalar algebra, so main is an author-side participant and is NOT counted as
an independent reviewer of sparse sharpness. Mechanism authored the finite
rational certificate. Their own diagnostics are labelled author checks in
their original files.

## Independent mathematical reviews

| Claim | Nonauthor context | Verdict and report |
|---|---|---|
| Complete event/Fisher/N reconstruction and tilt stationarity | audit | CORRECT within formula scope; verifications/audit/FORMULA_AUDIT.md |
| Full-support uniform beta-negative collar | audit | CORRECT within restricted scope; verifications/audit/GEOMETRY_REVIEW.md |
| Sparse exact zeros, localization and d alpha approaching one from below | audit | CORRECT; verifications/audit/SPARSE_REVIEW.md |
| Same frozen sparse theorem | fresh_review | CORRECT; verifications/fresh_review/review.md |
| Finite rational exact-zero certificate | audit | CORRECT; verifications/audit/SPARSE_CERTIFICATE_REVIEW.md |
| Explicit interval soundness explanation | audit | CORRECT; verifications/audit/INTERVAL_SOUNDNESS_REVIEW.md |

The sparse reviews bind to the UNCHANGED author file
geometry/sparse_proof.md, SHA256
b096a9986d123652849704ed001439b63373591153f4bbd321f8023d9ab98e9f,
frozen at author commit 0ff950c685228a9c76be0aa6dbbed77f077899a1.
The full-support proof binding is
7c7082a59d695ef87c9549337f8722d98513d401aa872a9e86eaca3df766717e.
Neither sparse reviewer authored the proof or saw the other review verdict
before returning its own. The fresh context inherited no preceding dialogue.
Four child contexts were used sequentially, never more than three active
children, with no descendant agents.

Both sparse reviewers explicitly checked the full six-direction optimizer,
the common-event U,V term, rare log terms, uniform Schur bounds for Q/T/W,
positive scaled V/Z0 inverse, and the passage from endpoint signs to exact
zeros for EVERY sufficiently small epsilon. The fresh review notes that the
proof summarizes a finite coefficient table rather than printing each
coefficient; it found this sufficient for the stated uniform remainder and
did not classify it as a critical gap. These are nonauthor AI mathematical
reviews, not a human expert or machine proof-checker certification.

## Independent diagnostic execution

All listed substantive runs used the authorized isolated server and exited
successfully. Each retained script and complete output is distributed.

| Context and script | PID | Runtime | Scope |
|---|---:|---|---|
| audit/formula_rebuild_audit.py | 164000 | Python 3.12.3, NumPy 2.1.2 | Independent eight-event/covariance/Hessian/tilt checks |
| audit/geometry_asymptotic_audit.py | 164365 | Python 3.12.3, NumPy 2.1.2 | Fixed full-support collar diagnostics |
| audit/sparse_asymptotic_audit.py | 165270 | Python 3.12.3, mpmath 1.3.0, 100 digits | Full optimizer, endpoints and common/rare split |
| fresh_review/independent_sparse_check.py | 165426 | Python 3.12.3, mpmath 1.3.0 | Separate full-event sparse reconstruction |
| fresh_review/endpoint_check.py | see exit_records.txt | Same | Endpoint coefficient checks |
| audit/mechanism_rerun/scripts/sparse_rational_certificate.py | 165603 | Python 3.12.3, mpmath 1.3.0 | Independent rerun with explicit 60 bisections |
| audit/sparse_certificate_audit.py | 165764 | Python 3.12.3, mpmath 1.3.0, 120 digits | Separate reconstruction of certificate endpoints, optimizer and H'' |

The numeric computations supplement the independently inspected analytic
proof. They are not its endpoint-sign premise or a replacement for uniform
error control. Their tiny floating beta values are not called exact zeros.
Exact zeros in the theorem follow by continuity and the uniform analytic
signs. The separate finite certificate uses outward interval arithmetic.

## Finite certificate review

The author certificate, exact rational endpoints and enclosures, script,
and failure history are included in mechanism/. Its finite kernel uses
u=(3/5,4/5,q/10000), not the normalized analytic sparse family. The audit
context reviewed the interval implementation, reran it in its isolated
directory, checked its exact rational enclosures, and separately rebuilt
the full six-coordinate formulas without importing the author evaluator.
Its CORRECT verdict is limited to this finite certificate. The rerun and
independent audit output are under verifications/audit/.

The rerun confirms the material command caveat: the historical default
--cert-steps 24 fails by interval overestimation; explicit --cert-steps 60
reproduces the frozen 2^-62 bracket. README.md and reproduce.py record that
successful input. The original script bytes and failed rerun are preserved.
No change to a frozen source is hidden behind the review's source hash.

The interval explanation in main/interval_soundness.md was separately
reviewed at SHA256
28474b6a781255e762661eddaec6f6406d53ac99cb24d163331f845363b45899.
All child-owned mathematical processes had ended at substantive stop.

## Formal and publication validation

Formal status is L0 only: Lean/Lake availability was checked, but no C1
theorem was submitted to Lean and no B0 formal proof is claimed. The local
archive checks validate required files, Python syntax, JSON readability,
proof/review hashes, manifest coverage and ZIP round-trip bytes. These
structural checks cannot establish mathematical correctness or novelty.
Full publication and substantive-stop metadata are in checkpoint.json;
the external final commit/tree mapping is reported with the Draft PR.
