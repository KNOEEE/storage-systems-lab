#!/usr/bin/env python3
"""Validate course coverage and local Markdown links using only stdlib."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PHASE_WEEKS = {
    "phase-01-local-storage": range(1, 5),
    "phase-02-storage-engines": range(5, 9),
    "phase-03-replication": range(9, 13),
    "phase-04-distributed-filesystems": range(13, 16),
    "phase-05-placement": range(16, 19),
    "phase-06-transactions": range(19, 23),
    "phase-07-capstone": range(23, 25),
}
WEEK_NAME = re.compile(r"w(\d{2})-[a-z0-9-]+\.md")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def without_code(text):
    return re.sub(r"^```[^\n]*\n.*?^```\s*$", "", text, flags=re.M | re.S)


def main():
    errors = []
    found = {}
    for path in sorted((ROOT / "curriculum").glob("phase-*/w*.md")):
        relative = path.relative_to(ROOT)
        match = WEEK_NAME.fullmatch(path.name)
        if not match:
            errors.append("Invalid week filename: {}".format(relative))
            continue
        week = int(match.group(1))
        if week in found:
            errors.append("Duplicate week {:02d}: {} / {}".format(week, found[week], relative))
        found[week] = relative
        if week not in PHASE_WEEKS.get(path.parent.name, ()):
            errors.append("Wrong phase for week {:02d}: {}".format(week, relative))
        text = path.read_text(encoding="utf-8")
        fields = dict(re.findall(r"^(week|phase|estimated_hours|status):\s*(.+)$", text, re.M))
        if not text.startswith("---\n") or text.count("\n---\n") < 1:
            errors.append("Missing front matter: {}".format(relative))
        if fields.get("week") != str(week):
            errors.append("Week metadata mismatch: {}".format(relative))
        if not fields.get("phase") or fields.get("estimated_hours") != "5":
            errors.append("Missing phase or non-5-hour estimate: {}".format(relative))
        if fields.get("status") not in {"planned", "in-progress", "completed"}:
            errors.append("Invalid status: {}".format(relative))
        for section in ("## 目标", "## 交付物", "## 验收标准", "## 复盘"):
            if section not in text:
                errors.append("{} missing {}".format(relative, section))
        if "- [ ]" not in text and "- [x]" not in text:
            errors.append("No acceptance checklist: {}".format(relative))

    expected = set(range(1, 25))
    if set(found) != expected:
        errors.append("Week coverage mismatch; missing={}, extra={}".format(
            sorted(expected - set(found)), sorted(set(found) - expected)))
    for phase in PHASE_WEEKS:
        if not (ROOT / "curriculum" / phase / "README.md").is_file():
            errors.append("Missing phase README: {}".format(phase))

    checked = 0
    for path in sorted(ROOT.rglob("*.md")):
        relative = path.relative_to(ROOT)
        if any(part in {".git", "checkouts", "__pycache__"} for part in relative.parts):
            continue
        if relative.parts[0] == "artifacts" and path.name != "README.md":
            continue
        text = without_code(path.read_text(encoding="utf-8"))
        for match in LINK.finditer(text):
            target = urlsplit(match.group(1).strip("<>"))
            if target.scheme or target.netloc or not target.path:
                continue
            link = unquote(target.path)
            destination = ROOT / link.lstrip("/") if link.startswith("/") else path.parent / link
            checked += 1
            if not destination.exists():
                errors.append("Broken link in {}: {}".format(relative, match.group(1)))

    if errors:
        for error in errors:
            print("- " + error, file=sys.stderr)
        return 1
    print("Course check passed: 24 weeks, 7 phases, {} local links.".format(checked))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
