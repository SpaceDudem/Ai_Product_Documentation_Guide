# Product Repo (MPD/TDS + AI Compliance)

This repository provides a documentation-first structure for building hardware/software products with:
- MPD (Master Product Definition)
- TDS (Technical Design Specification)
- AI Compliance Spec (agent/tool guardrails)
- Ticket-driven implementation with stable section IDs
- CI linting to prevent drift, broken references, and scope creep

Primary conventions:
- Docs embed stable IDs in bracket headers: [TDS-SW-CONFIG-PERSISTENCE-001]
- Tickets reference doc version + section IDs
- CI enforces ID format/uniqueness and ticket↔doc cross-checks
- PRs that change source code must reference at least one ticket ID in PR title/body (e.g., "Implements: TKT-0001")
