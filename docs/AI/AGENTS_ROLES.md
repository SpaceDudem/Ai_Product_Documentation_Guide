Document: AI
Version: v0.1.0
Status: DRAFT
Change Summary:
- Initial agent roles

Agent roles (minimum set):
- Planner: converts ticket into an implementation plan and identifies impacted docs/tests
- Coder: implements exactly what the ticket requires; no scope creep
- Reviewer: verifies diffs vs ticket + TDS/MPD references; blocks drift
- Tester: runs tests/build; adds missing tests required by acceptance criteria
- Scribe: updates docs (TDS/MPD) only when change_control.requires_tds_update is true

Rules:
- Coder cannot approve their own work.
- Reviewer must confirm: ticket IDs, doc section IDs, acceptance criteria, and tests are satisfied.
