# Review provenance

C1 acts as finite-kernel verifier and review publisher in this round.
The author material is obtained from the public PRs and identified by
immutable commit. No private conversation or connection information is
distributed. Earlier author files and other lines' checkouts are unchanged.

Three fresh, isolated GPT-5.5 xhigh contexts own the W1, W4 and C3 checks.
They are nonauthors of those submitted results and are instructed to judge
the frozen author proof before reading prior reviewers' opinions. They do
not spawn descendants. Main integrates review files and resolves version
scope, but does not self-certify the C1-authored PR30.

The mathematical review, independent implementation check, rerun of author
code, and universal theorem claim must stay distinct in each report.
Neither a majority of reviews nor a large sample count is a proof.

If a material corrected proof is authored during this round, its authorship
will be recorded and it must receive a different nonauthor review before
being called accepted. Archiving a still-unverified claim in a draft is
permitted only with its unverified status explicit.

C3 alone decides main integration. A READY message includes exact accepted
scope, frozen source commit, our review commit, independent runtime evidence,
and any unresolved obligations. Receiving a new author version triggers a
content delta check, not automatic acceptance or abandonment of earlier work.
