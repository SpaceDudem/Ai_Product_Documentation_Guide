\
import os
import re
import sys
import subprocess
from pathlib import Path

DOC_ID_REGEX = re.compile(r'^(MPD|TDS|TEST|SOP|ACS)-(SYS|HW|FW|SW|SEC|OPS|REG|SAF|QA|AUD)-[A-Z0-9]+-[A-Z0-9]+-[0-9]{3}$')
TICKET_ID_REGEX = re.compile(r'^TKT-[0-9]{4}$')

def run(cmd):
    return subprocess.check_output(cmd, text=True).strip()

def extract_doc_ids():
    ids = set()
    for path in Path("docs").rglob("*.md"):
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                sid = line[1:-1].strip()
                if DOC_ID_REGEX.match(sid):
                    ids.add(sid)
    return ids

def parse_ticket_yaml_minimal(path: Path):
    # Minimal YAML reader for the repo's fixed schema; avoids external deps.
    data = {}
    stack = [(0, data)]
    key_stack = []

    lines = [ln.rstrip("\n") for ln in path.read_text(encoding="utf-8", errors="replace").splitlines()]
    for raw in lines:
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()

        while stack and indent < stack[-1][0]:
            stack.pop()
            if key_stack:
                key_stack.pop()

        cur = stack[-1][1]

        if line.startswith("- "):
            item = line[2:].strip()
            if not isinstance(cur, list):
                # convert last mapping key into list
                parent_indent, parent = stack[-2]
                last_key = key_stack[-1] if key_stack else None
                if last_key is None:
                    raise ValueError(f"List item without parent key at: {raw}")
                if not isinstance(parent.get(last_key), list):
                    parent[last_key] = []
                stack[-1] = (stack[-1][0], parent[last_key])
                cur = stack[-1][1]
            cur.append(item)
            continue

        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip()
            if v == "":
                # nested map
                new_obj = {}
                cur[k] = new_obj
                stack.append((indent + 2, new_obj))
                key_stack.append(k)
            else:
                if v.lower() in ("true", "false"):
                    v = (v.lower() == "true")
                cur[k] = v
                key_stack.append(k)
            continue

    return data

def load_tickets():
    tickets = {}
    tdir = Path("tickets/backlog")
    if not tdir.exists():
        return tickets
    for path in tdir.rglob("*.yaml"):
        data = parse_ticket_yaml_minimal(path)
        tid = str(data.get("id", "")).strip()
        tickets[tid] = (path, data)
    return tickets

def list_changed_files():
    base = os.getenv("AI_LINT_BASE_SHA", "").strip()
    head = os.getenv("AI_LINT_HEAD_SHA", "").strip()
    if not base or not head:
        # fallback to last commit
        out = run(["git", "diff", "--name-only", "HEAD~1", "HEAD"])
        return [x for x in out.splitlines() if x.strip()]
    out = run(["git", "diff", "--name-only", base, head])
    return [x for x in out.splitlines() if x.strip()]

def main():
    errors = []

    doc_ids = extract_doc_ids()
    if not doc_ids:
        errors.append("No doc IDs found under docs/. Did you forget to include [ID] headers?")

    tickets = load_tickets()

    # Validate each ticket's doc IDs exist
    for tid, (path, data) in tickets.items():
        if not TICKET_ID_REGEX.match(tid):
            errors.append(f"{path}: Invalid ticket id: {tid}")
            continue

        doc = data.get("doc", {})
        # minimal parser may keep nested dicts but lists are sometimes strings; normalize
        tds_ids = doc.get("tds_section_ids", [])
        mpd_ids = doc.get("mpd_section_ids", [])

        if not isinstance(tds_ids, list) or not tds_ids:
            errors.append(f"{path}: doc.tds_section_ids must be a non-empty list")
        if not isinstance(mpd_ids, list) or not mpd_ids:
            errors.append(f"{path}: doc.mpd_section_ids must be a non-empty list")

        for sid in (tds_ids if isinstance(tds_ids, list) else []):
            if not DOC_ID_REGEX.match(str(sid)):
                errors.append(f"{path}: Invalid TDS section ID format: {sid}")
            elif str(sid) not in doc_ids:
                errors.append(f"{path}: Ticket references missing doc ID: {sid}")

        for sid in (mpd_ids if isinstance(mpd_ids, list) else []):
            if not DOC_ID_REGEX.match(str(sid)):
                errors.append(f"{path}: Invalid MPD section ID format: {sid}")
            elif str(sid) not in doc_ids:
                errors.append(f"{path}: Ticket references missing doc ID: {sid}")

        # Gate: acceptance criteria must exist
        ac = data.get("acceptance_criteria", [])
        if not isinstance(ac, list) or not ac or any(not str(x).strip() for x in ac):
            errors.append(f"{path}: acceptance_criteria must be a non-empty list of non-empty strings")

    # Source-change gating
    changed = list_changed_files()
    src_changed = any(
        p.startswith("src/") or p.startswith("firmware/") or p.startswith("hardware/") or p.startswith("app/")
        for p in changed
    )

    referenced_ticket_ids = os.getenv("AI_LINT_PR_TICKETS", "").strip()
    pr_ticket_ids = [t.strip() for t in referenced_ticket_ids.split(",") if t.strip()]
    pr_ticket_ids = [t for t in pr_ticket_ids if TICKET_ID_REGEX.match(t)]

    if src_changed and not pr_ticket_ids:
        errors.append("PR changes source paths (src/|firmware/|hardware/|app/) but PR title/body references no TKT-#### IDs.")

    # If PR references tickets, ensure they exist in backlog or done folders
    if pr_ticket_ids:
        all_ticket_files = set()
        for d in (Path("tickets/backlog"), Path("tickets/done")):
            if d.exists():
                for p in d.rglob("*.yaml"):
                    try:
                        tid = parse_ticket_yaml_minimal(p).get("id", "")
                        all_ticket_files.add(str(tid).strip())
                    except Exception:
                        pass
        for tid in pr_ticket_ids:
            if tid not in all_ticket_files:
                errors.append(f"PR references ticket {tid} but no matching ticket file found under tickets/backlog or tickets/done.")

    if errors:
        print("AI COMPLIANCE LINT FAILED:\n" + "\n".join(errors))
        print("\nChanged files detected:")
        for p in changed:
            print(f"- {p}")
        return 1

    print("AI COMPLIANCE LINT PASSED")
    return 0

if __name__ == "__main__":
    sys.exit(main())
