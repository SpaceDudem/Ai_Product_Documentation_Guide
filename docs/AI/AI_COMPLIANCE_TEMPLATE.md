Document: AI Compliance Spec (ACS)
Version: v0.1.0
Status: TEMPLATE
Change Summary:
- Initial AI compliance template

[ACS-SYS-PURPOSE-001]
Title: Purpose
Define agent/tool guardrails to prevent drift, preserve scope, and require evidence.

[ACS-SYS-TOOLS-ALLOWLIST-001]
Title: Tooling Policy
- Allowed tools: (see MCP_TOOLS_ALLOWLIST.md)
- Forbidden tools:
- Logging requirements:

[ACS-SYS-AGENTS-ROLES-001]
Title: Agent Roles & Handoffs
- Planner:
- Coder:
- Reviewer:
- Tester:
- Scribe:

[ACS-SYS-STOP-CONDITIONS-001]
Title: Stop Conditions (Must Halt)
- Unclear requirements or missing ticket references
- Missing access to required MCP tools
- Any request to add features not listed in scope.in_scope
- Any change that breaks tests without a documented plan and rollback
- Any secret/credential request not explicitly provided and scoped

[ACS-SYS-EVIDENCE-REQUIREMENTS-001]
Title: Evidence Requirements
- Tests required by ticket must pass
- Provide diff summary mapped to ticket acceptance criteria
- Provide rollback note

[ACS-SYS-DRIFT-AUDIT-001]
Title: Drift Audit Procedure
- Run drift checklist
- Validate ticket↔doc IDs
- Validate PR metadata contains ticket IDs

