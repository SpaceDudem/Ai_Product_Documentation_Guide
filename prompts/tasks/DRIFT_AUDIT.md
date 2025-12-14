Task: Drift Audit

Purpose:
Verify that a change set has not drifted from documented intent, scope, or requirements.

Inputs:
- Ticket ID(s) referenced by the PR
- Referenced MPD section IDs
- Referenced TDS section IDs
- Git diff for the change set

Audit Checklist (must all pass):
1) Every code change maps to at least one acceptance criterion.
2) No code exists that is not traceable to a ticket ID.
3) No functionality exceeds scope.in_scope.
4) No scope.out_of_scope items are implemented.
5) No undocumented dependencies were added.
6) No undocumented configuration or environment assumptions were introduced.
7) Security posture unchanged or improved (no new attack surface without docs).
8) Tests required by acceptance criteria exist and pass.

Output (mandatory):
- PASS or FAIL
- If FAIL: list exact drift points with file paths and line numbers.
- Required corrective action or escalation.
