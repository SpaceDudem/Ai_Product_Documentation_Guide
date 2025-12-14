Document: AI
Version: v0.1.0
Status: DRAFT
Change Summary:
- Initial MCP tool allowlist template

Allowed MCP tools (allowlist):
- filesystem: read/write within repo only; must log changes in PR
- git: status/diff/log; commits allowed; no force-push
- build: run tests/build locally in CI environment
- web: read-only for official docs (if enabled in your MCP stack)

Forbidden by default:
- Any tool that can modify external systems (cloud accounts, production, vendor portals)
- Any tool that can exfiltrate secrets or scrape private systems
- Any tool that writes outside this repo

Tool contracts are documented under: mcp/tool-contracts/
