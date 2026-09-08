# Provenance

- Problem selection and scope: human instruction; A1 owns frozen statements.
- Main A1: GPT-6 Astra, xhigh; coordination, history/scope audit, integration.
- Direct analytic author: GPT-6 Astra, high; exact 3D structure and standard
  mode proof, authored commit e5a099d127d3471e4d88a75e8b530a5d578431d4.
- Direct falsifier: GPT-6 Astra, high; asymmetric bounded probes and a
  separate conditional-acceleration shortcut counterexample.
- Direct independent verifier: GPT-5.5, xhigh; fresh context with no proof
  authorship. Original review commit e787ad086a8be98335933ca5f8b99f5dd921983c,
  integrated as a35ad53. All three restricted objects received CORRECT.
- Direct agents do not spawn descendants. Maximum active contexts: four.
- Each participant owns a separate writable checkout and disjoint outputs.
- Proof and verification authorship will be bound to commits at integration.
- No novelty certification or attribution to external authors is implied.

Main A1 authored the radial-slice proof. It is therefore subject to the same
non-author review rule as the analytic and falsification results; integration
by A1 is not a correctness certificate. The standard-mode author's proof
was integrated without a mathematical rewrite as commit 8558362.

The probe author fixed the explicit acceleration witness, rigorous log bounds
and complete proof in commit 19574e7848bc3689d6495becd05629a3a42f690d,
integrated unchanged as e9e188d. A1 supplied the conditional acceleration
identity and requested the bounded transverse diagnostic; that contribution
is disclosed in probe/provenance.md. Neither contributor verified this proof.
