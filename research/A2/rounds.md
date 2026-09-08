# Rounds and coverage

## Round 0: initialization and scope audit

- Read public AGENTS, COMMON protocol, PR #11 frozen hierarchy and two C2
  reviews. User's later real-domain and model authorization controls scope.
- Created an isolated A2 branch and checked existing local/remote state.
- Remote resources were ample; other processes were left untouched.
- Local authenticated public-repository access worked after process-local
  removal of stale proxy settings. Remote HTTPS clone failed its CA check;
  a public git bundle will supply the isolated remote checkout.
- No mathematical computation or search has started yet.
