Task: Review Diff

Purpose:
Perform a structured review of a proposed diff against documentation and tickets.

Inputs:
- Git diff
- Ticket file(s)
- Referenced MPD/TDS sections

Review Steps:
1) Confirm ticket ID(s) are valid and present.
2) Confirm MPD/TDS section IDs exist and are correct.
3) Review diff file-by-file.
4) For each file, map changes to acceptance criteria.
5) Identify unrelated or speculative changes (flag as drift).
6) Confirm tests cover all behavioral changes.
7) Confirm no forbidden tools or paths were used.

Output (mandatory):
- APPROVE or REQUEST_CHANGES
- Bullet list of findings
- Explicit statement on scope compliance
