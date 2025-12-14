#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

DOC_ID_RE = re.compile(r'^(MPD|TDS|TEST|SOP|ACS)-(SYS|HW|FW|SW|SEC|OPS|REG|SAF|QA|AUD)-[A-Z0-9]+-[A-Z0-9]+-[0-9]{3}$')
TICKET_ID_RE = re.compile(r'^TKT-[0-9]{4}$')

REQUIRED_FIELDS = [
    "id", "title", "status", "priority", "doc", "scope", "acceptance_criteria", "tests", "change_control"
]

TICKET_DIRS = [
    Path("tickets/backlog"),
    Path("tickets/done"),
]

def parse_ticket(path):
    data = {}
    with path.open(encoding="utf-8") as f:
        lines = f.readlines()

    current_key = None
    current_indent = 0
    for line in lines:
        raw = line.rstrip("\n")
        if not raw.strip() or raw.strip().startswith("#"):
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        content = raw.strip()

        if ": " in content:
            k, v = content.split(": ", 1)
            data[k.strip()] = v.strip()
            current_key = k.strip()
        elif content.endswith(":"):
            current_key = content[:-1].strip()
            if current_key not in data:
                data[current_key] = []
        elif content.startswith("- "):
            if isinstance(data.get(current_key), list):
                data[current_key].append(content[2:].strip())

    return data

def lint_ticket_file(path):
    errors = []
    data = parse_ticket(path)

    # ID check
    tid = data.get("id", "")
    if not TICKET_ID_RE.match(tid):
        errors.append(f"{path}: invalid or missing ticket ID '{tid}'")

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"{path}: missing required field '{field}'")

    # Doc references
    doc = data.get("doc", {})
    if not isinstance(doc, dict):
        errors.append(f"{path}: 'doc' should be a dictionary")
    else:
        for key in ["tds_section_ids", "mpd_section_ids"]:
            ids = doc.get(key, [])
            if not isinstance(ids, list) or not ids:
                errors.append(f"{path}: 'doc.{key}' should be a non-empty list")
            else:
                for sid in ids:
                    if not DOC_ID_RE.match(sid):
                        errors.append(f"{path}: invalid doc section ID in {key}: {sid}")

    # Acceptance criteria
    ac = data.get("acceptance_criteria", [])
    if not isinstance(ac, list) or not all(ac):
        errors.append(f"{path}: invalid or empty 'acceptance_criteria'")

    # Tests
    tests = data.get("tests", [])
    if not isinstance(tests, list) or not tests:
        errors.append(f"{path}: 'tests' should be a non-empty list")

    return errors

def main():
    all_errors = []
    seen_ids = set()

    for tdir in TICKET_DIRS:
        if not tdir.exists():
            continue
        for file in tdir.glob("TKT-*.yaml"):
            errors = lint_ticket_file(file)
            all_errors.extend(errors)

            ticket_id = parse_ticket(file).get("id", "").strip()
            if ticket_id:
                if ticket_id in seen_ids:
                    all_errors.append(f"{file}: duplicate ticket ID {ticket_id}")
                else:
                    seen_ids.add(ticket_id)

    if all_errors:
        print("TICKET LINT FAILED:\n" + "\n".join(all_errors))
        sys.exit(1)
    else:
        print("TICKET LINT PASSED")
        sys.exit(0)

if __name__ == "__main__":
    main()