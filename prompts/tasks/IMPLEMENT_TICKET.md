Task: Implement exactly one ticket from tickets/backlog.

Inputs you must use:
- Ticket file path: tickets/backlog/TKT-####.yaml
- Referenced TDS version and section IDs in ticket.doc.tds_section_ids
- Referenced MPD section IDs in ticket.doc.mpd_section_ids

Output format (mandatory):
1) Ticket recap (id + title)
2) Plan (numbered steps)
3) Files changed (list)
4) Implementation notes mapped to acceptance_criteria (one-by-one)
5) Test evidence (commands + results)
6) Drift audit (confirm nothing outside scope.in_scope was implemented)
7) Rollback plan (how to revert cleanly)

Rules:
- Do not implement anything listed under scope.out_of_scope.
- If a required TDS/MPD section is missing, stop and report it.
- If acceptance criteria are not testable, add tests or tighten the criteria by updating the ticket (only if permitted).
