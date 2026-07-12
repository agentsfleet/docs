#!/usr/bin/env python3
"""Check published MDX pages against the agentsfleet documentation rules."""

from __future__ import annotations

import re
import sys
from pathlib import Path

PAGE_FIELDS = {
    "type",
    "audience",
    "verified",
    "product_version",
    "executable",
}
FIELD_VALUES = {
    "type": {"tutorial", "how-to", "reference", "explanation", "troubleshooting"},
    "audience": {"user", "operator", "contributor"},
    "executable": {"true", "false"},
}
PAGE_SECTIONS = {
    "tutorial": [
        "What you will build",
        "Before you begin",
        "Steps",
        "Verify it works",
        "What you learned",
        "Related pages",
    ],
    "how-to": [
        "What this does",
        "Before you begin",
        "Steps",
        "Verify it works",
        "Common problems",
        "Remove or undo",
        "Related pages",
    ],
    "reference": ["Synopsis", "Example with output", "Options", "Errors", "Related pages"],
    "explanation": ["What it is", "Why it exists", "How it behaves", "Limits", "Related pages"],
    "troubleshooting": ["Symptom", "Why it happened", "How to fix it", "How to prevent it"],
}
BANNED_PATTERNS = {
    "utilise": re.compile(r"\butilis(?:e|es|ed|ing)\b", re.IGNORECASE),
    "facilitate": re.compile(r"\bfacilitat(?:e|es|ed|ing)\b", re.IGNORECASE),
    "leverage": re.compile(r"\bleverag(?:e|es|ed|ing)\b", re.IGNORECASE),
    "orchestrate": re.compile(r"\borchestrat(?:e|es|ed|ing|ion)\b", re.IGNORECASE),
    "instantiate": re.compile(r"\binstantiat(?:e|es|ed|ing|ion)\b", re.IGNORECASE),
    "terminate": re.compile(r"\bterminat(?:e|es|ed|ing|ion|al)\b", re.IGNORECASE),
    "provision": re.compile(r"\bprovision(?:s|ed|ing)?\b", re.IGNORECASE),
    "execute": re.compile(r"\bexecut(?:e|es|ed|ing|ion)\b", re.IGNORECASE),
    "persist": re.compile(r"\bpersist(?:s|ed|ing|ent|ence)?\b", re.IGNORECASE),
    "hydrate": re.compile(r"\bhydrat(?:e|es|ed|ing|ion)\b", re.IGNORECASE),
    "artifact": re.compile(r"\bartifacts?\b", re.IGNORECASE),
    **{
        word: re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE)
        for word in (
            "powerful",
            "revolutionary",
            "enterprise-grade",
            "seamless",
            "cutting-edge",
            "robust",
            "next-generation",
            "world-class",
            "intelligent",
        )
    },
}
MARKETING_WORDS = {
    "powerful",
    "revolutionary",
    "enterprise-grade",
    "seamless",
    "cutting-edge",
    "robust",
    "next-generation",
    "world-class",
    "intelligent",
}
ACRONYM_ALLOWLIST = {
    "API",
    "CSS",
    "DELETE",
    "DNS",
    "GET",
    "HEAD",
    "HTML",
    "HTTP",
    "IP",
    "JSON",
    "OPTIONS",
    "OS",
    "PATCH",
    "POST",
    "PUT",
    "SQL",
    "TCP",
    "UDP",
    "URL",
}
EXPECTED_VERSION = "0.17.0"
NON_PAGE_CODE_SNIPPETS = {Path("snippets/rates.mdx")}
ERROR_REFERENCE_PRIVATE_TERMS = {
    "API_MAX_",
    "DATABASE_URL",
    "MEMORY_RUNTIME_URL",
    "Postgres memory schema",
    "REDIS_URL_API",
    "SSE_MAX_",
    "config_json",
    "core.model_library",
    "core.platform_provider_defaults",
    "core.tenant_model_entries",
    "err= field",
}
FRONTMATTER_BOUNDARY = "---"
FENCE_PATTERN = re.compile(r"^```([^\s]*)\s*$")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
WORD_PATTERN = re.compile(r"\b[\w'-]+\b")
SENTENCE_PATTERN = re.compile(r"(?<=[.!?])(?:[\s]+|$)")
ACRONYM_PATTERN = re.compile(r"(?<![-_`])\b[A-Z][A-Z0-9]{1,5}\b(?![-_`])")


def issue(rule: str, path: Path, line: int, message: str) -> str:
    return f"{rule} {path}:{line}: {message}"


def split_frontmatter(text: str) -> tuple[dict[str, str], str, int]:
    lines = text.splitlines()
    if not lines or lines[0] != FRONTMATTER_BOUNDARY:
        return {}, text, 1
    try:
        end = lines.index(FRONTMATTER_BOUNDARY, 1)
    except ValueError:
        return {}, text, 1
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" in line and not line.startswith((" ", "-")):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip("\"'")
    return fields, "\n".join(lines[end + 1 :]), end + 2


def visible_lines(body: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    in_fence = False
    for number, line in enumerate(body.splitlines(), 1):
        if FENCE_PATTERN.match(line.strip()):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        stripped = line.lstrip()
        if stripped.startswith("{") or stripped in {"*/", "*/}"}:
            continue
        heading = HEADING_PATTERN.match(line)
        if heading:
            result.append((number, heading.group(2)))
            result.append((number, ""))
            continue
        if stripped.startswith("|"):
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                continue
            for cell in cells:
                cleaned_cell = re.sub(r"`[^`]+`", "", cell)
                cleaned_cell = re.sub(r"<[^>]+>", "", cleaned_cell)
                cleaned_cell = re.sub(r"\[([^]]+)]\([^)]+\)", r"\1", cleaned_cell)
                cleaned_cell = re.sub(r"\*\*|__", "", cleaned_cell).strip()
                if cleaned_cell:
                    result.append((number, cleaned_cell))
                    result.append((number, ""))
            continue
        is_list_item = bool(re.match(r"^(?:[-*+]\s+|\d+[.)]\s+)", stripped))
        cleaned = re.sub(r"^(?:[-*+]\s+|\d+[.)]\s+|>\s*)", "", stripped)
        cleaned = re.sub(r"<[^>]+>", "", cleaned)
        cleaned = re.sub(r"`[^`]+`", "", cleaned)
        cleaned = re.sub(r"\[([^]]+)]\([^)]+\)", r"\1", cleaned)
        cleaned = re.sub(r"\*\*|__", "", cleaned).strip()
        result.append((number, cleaned))
        if is_list_item:
            result.append((number, ""))
    return result


def lint_language(path: Path, body: str, line_offset: int) -> list[str]:
    errors: list[str] = []
    visible = visible_lines(body)
    for word, pattern in sorted(BANNED_PATTERNS.items()):
        for number, line in visible:
            if pattern.search(line):
                rule = "DOC-07" if word in MARKETING_WORDS else "DOC-05"
                errors.append(issue(rule, path, number + line_offset - 1, f"banned word '{word}'"))
                break

    expanded: set[str] = set()
    reported: set[str] = set()
    for number, line in visible:
        expanded_here = set(re.findall(r"\(([A-Z][A-Z0-9]{1,5})\)", line))
        for acronym in ACRONYM_PATTERN.findall(line):
            if acronym in ACRONYM_ALLOWLIST:
                continue
            if acronym in expanded_here:
                expanded.add(acronym)
                continue
            if acronym not in expanded and acronym not in reported:
                errors.append(issue("DOC-10", path, number + line_offset - 1, f"expand '{acronym}' once"))
                reported.add(acronym)

    paragraph: list[tuple[int, str]] = []
    for number, line in visible + [(len(body.splitlines()) + 1, "")]:
        if line:
            paragraph.append((number, line))
            continue
        if not paragraph:
            continue
        paragraph_text = " ".join(value for _, value in paragraph)
        sentences = [value for value in SENTENCE_PATTERN.split(paragraph_text) if value.strip()]
        if len(sentences) > 3:
            errors.append(issue("DOC-03", path, paragraph[0][0] + line_offset - 1, "paragraph has more than 3 sentences"))
        for sentence in sentences:
            word_count = len(WORD_PATTERN.findall(sentence))
            if word_count > 25:
                errors.append(issue("DOC-02", path, paragraph[0][0] + line_offset - 1, f"sentence has {word_count} words"))
        paragraph = []
    return errors


def parse_headings(body: str) -> list[tuple[int, int, str]]:
    headings: list[tuple[int, int, str]] = []
    in_fence = False
    for number, line in enumerate(body.splitlines(), 1):
        if FENCE_PATTERN.match(line.strip()):
            in_fence = not in_fence
            continue
        match = None if in_fence else HEADING_PATTERN.match(line)
        if match:
            headings.append((number, len(match.group(1)), match.group(2).strip("`")))
    return headings


def lint_fences(path: Path, body: str, line_offset: int) -> list[str]:
    errors: list[str] = []
    fences: list[tuple[str, int]] = []
    open_language: str | None = None
    for number, line in enumerate(body.splitlines(), 1):
        match = FENCE_PATTERN.match(line.strip())
        if not match:
            continue
        if open_language is None:
            open_language = match.group(1)
            fences.append((open_language, number))
        else:
            open_language = None
    for index, (language, number) in enumerate(fences):
        if language == "bash" and (index + 1 >= len(fences) or fences[index + 1][0] != "text"):
            errors.append(issue("DOC-15", path, number + line_offset - 1, "bash command needs a following text output block"))
    return errors


def lint_page(path: Path, text: str) -> list[str]:
    fields, body, line_offset = split_frontmatter(text)
    errors: list[str] = []
    if not fields:
        return [issue("DOC-F1", path, 1, "missing front matter")]
    for field in sorted(PAGE_FIELDS):
        if not fields.get(field):
            errors.append(issue("DOC-F1", path, 1, f"missing '{field}'"))
    for field, values in FIELD_VALUES.items():
        if fields.get(field) and fields[field] not in values:
            errors.append(issue("DOC-F1", path, 1, f"invalid '{field}' value"))
    if fields.get("product_version") != EXPECTED_VERSION:
        errors.append(issue("DOC-F2", path, 1, f"product_version must be {EXPECTED_VERSION}"))
    if fields.get("verified") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fields["verified"]):
        errors.append(issue("DOC-F2", path, 1, "verified must use YYYY-MM-DD"))

    ignores = [line for line in text.splitlines() if "lint-ignore:" in line]
    if len(ignores) > 3:
        errors.append(issue("DOC-35", path, 1, "more than 3 lint-ignore entries"))

    headings = parse_headings(body)
    h1_count = sum(level == 1 for _, level, _ in headings)
    if h1_count != 1:
        errors.append(issue("DOC-25", path, line_offset, f"expected 1 H1, found {h1_count}"))
    for previous, current in zip(headings, headings[1:]):
        if current[1] > previous[1] + 1:
            errors.append(issue("DOC-25", path, current[0] + line_offset - 1, "heading level is skipped"))

    page_type = fields.get("type")
    required = PAGE_SECTIONS.get(page_type, [])
    level_two = [title for _, level, title in headings if level == 2]
    positions = [level_two.index(title) if title in level_two else -1 for title in required]
    missing = [title for title, position in zip(required, positions) if position < 0]
    if missing:
        errors.append(issue("DOC-P1", path, line_offset, f"missing sections: {', '.join(missing)}"))
    elif positions != sorted(positions):
        errors.append(issue("DOC-P1", path, line_offset, "required sections are out of order"))

    lines = body.splitlines()
    for number, line in enumerate(lines, 1):
        if line.startswith("|") and re.search(r"\bOption\b", line, re.IGNORECASE) and "Default" not in line:
            errors.append(issue("DOC-19", path, number + line_offset - 1, "option table needs a Default column"))
        if line.startswith("|"):
            cells = [cell.strip().lower() for cell in line.strip("|").split("|")]
            if any(cell in {"action", "instruction", "procedure", "step"} for cell in cells):
                errors.append(issue("DOC-27", path, number + line_offset - 1, "procedure must not use a table"))
    errors.extend(lint_language(path, body, line_offset))
    errors.extend(lint_fences(path, body, line_offset))
    if path == Path("api-reference/error-codes.mdx"):
        for term in sorted(ERROR_REFERENCE_PRIVATE_TERMS):
            if term in body:
                errors.append(issue("DOC-22", path, line_offset, f"customer error text exposes '{term}'"))
    return errors


def lint_tree(root: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(root.rglob("*.mdx")):
        relative = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        if relative == Path("changelog.mdx"):
            continue
        if relative in NON_PAGE_CODE_SNIPPETS:
            continue
        if relative.parts[0] == "snippets":
            errors.extend(lint_language(relative, text, 1))
            continue
        errors.extend(lint_page(relative, text))
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = lint_tree(root)
    if errors:
        print("Documentation check failed:")
        print("\n".join(f"  {error}" for error in errors))
        return 1
    print("Documentation check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
