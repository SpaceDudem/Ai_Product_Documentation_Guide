\
import re
import sys
from pathlib import Path

ID_REGEX = re.compile(r'^(MPD|TDS|TEST|SOP|ACS)-(SYS|HW|FW|SW|SEC|OPS|REG|SAF|QA|AUD)-[A-Z0-9]+-[A-Z0-9]+-[0-9]{3}$')

def extract_ids_from_md(path: Path):
    ids = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = line.strip()
        if line.startswith("[") and line.endswith("]") and len(line) > 2:
            section_id = line[1:-1].strip()
            ids.append((section_id, lineno))
    return ids

def main():
    docs_root = Path("docs")
    if not docs_root.exists():
        print("ID lint skipped: docs/ not found")
        return 0

    seen = {}
    errors = []

    for path in docs_root.rglob("*.md"):
        for section_id, lineno in extract_ids_from_md(path):
            if not ID_REGEX.match(section_id):
                errors.append(f"{path}:{lineno} Invalid ID format: {section_id}")
                continue
            if section_id in seen:
                errors.append(f"{path}:{lineno} Duplicate ID: {section_id} (first seen at {seen[section_id]})")
            else:
                seen[section_id] = f"{path}:{lineno}"

    if errors:
        print("ID LINT FAILED:\n" + "\n".join(errors))
        return 1

    print(f"ID LINT PASSED: {len(seen)} IDs validated")
    return 0

if __name__ == "__main__":
    sys.exit(main())
