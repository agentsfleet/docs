#!/usr/bin/env python3
"""Regression tests for the documentation checker."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

CHECKER_PATH = Path(__file__).with_name("check-documentation.py")
ROOT = Path(__file__).resolve().parents[1]
MODULE_SPEC = importlib.util.spec_from_file_location("documentation_checker", CHECKER_PATH)
assert MODULE_SPEC and MODULE_SPEC.loader
CHECKER = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(CHECKER)

VALID_PAGE = """---
title: Test page
description: A small test page.
type: explanation
audience: user
verified: 2026-07-12
product_version: 0.17.0
executable: false
---

# Test page

## What it is

This page explains a fleet.

## Why it exists

A fleet handles events for you.

## How it behaves

You create the fleet. `agentsfleet` receives each event.

## Limits

The workspace limit comes from its configured policy.

## Related pages

No related page applies.
"""


class DocumentationCheckerTests(unittest.TestCase):
    def lint(self, content: str, relative: str = "page.mdx") -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return CHECKER.lint_tree(root)

    def test_should_accept_valid_page(self) -> None:
        self.assertEqual([], self.lint(VALID_PAGE))

    def test_should_accept_fragment_without_page_fields(self) -> None:
        self.assertEqual([], self.lint("Contact support.\n", "snippets/contact.mdx"))

    def test_should_ignore_historical_changelog(self) -> None:
        self.assertEqual([], self.lint("Old powerful launch copy.\n", "changelog.mdx"))

    def test_should_ignore_non_page_rate_source_fragment(self) -> None:
        self.assertEqual([], self.lint("Old powerful TS and JS copy.\n", "snippets/rates.mdx"))

    def test_should_reject_private_terms_in_customer_error_text(self) -> None:
        errors = self.lint(VALID_PAGE.replace("This page explains a fleet.", "Check DATABASE_URL."), "api-reference/error-codes.mdx")
        self.assertTrue(any("DOC-22" in error for error in errors))

    def test_should_reject_missing_frontmatter(self) -> None:
        errors = self.lint("# Missing fields\n")
        self.assertTrue(any("DOC-F1" in error for error in errors))

    def test_should_reject_missing_required_section(self) -> None:
        errors = self.lint(VALID_PAGE.replace("## Limits\n", ""))
        self.assertTrue(any("DOC-P1" in error for error in errors))

    def test_should_reject_banned_word(self) -> None:
        content = VALID_PAGE.replace("handles events", "orchestrates events")
        expected_line = next(number for number, line in enumerate(content.splitlines(), 1) if "orchestrates" in line)
        errors = self.lint(content)
        self.assertTrue(any(f"DOC-05 page.mdx:{expected_line}:" in error for error in errors))

    def test_should_reject_banned_word_in_list(self) -> None:
        errors = self.lint(VALID_PAGE.replace("A fleet handles events for you.", "- A fleet orchestrates events for you."))
        self.assertTrue(any("DOC-05" in error for error in errors))

    def test_should_reject_banned_word_inflection(self) -> None:
        errors = self.lint(VALID_PAGE.replace("handles events", "provisioned events"))
        self.assertTrue(any("DOC-05" in error for error in errors))

    def test_should_check_inline_callout_text(self) -> None:
        replacement = "<Note>A powerful fleet handles events.</Note>"
        errors = self.lint(VALID_PAGE.replace("A fleet handles events for you.", replacement))
        self.assertTrue(any("DOC-07" in error for error in errors))

    def test_should_reject_long_sentence(self) -> None:
        long_text = "This sentence contains more than twenty five words because it keeps adding unnecessary details that a first day reader cannot use during one simple task today."
        errors = self.lint(VALID_PAGE.replace("This page explains a fleet.", long_text))
        self.assertTrue(any("DOC-02" in error for error in errors))

    def test_should_reject_long_paragraph(self) -> None:
        paragraph = "One sentence. Two sentences. Three sentences. Four sentences."
        errors = self.lint(VALID_PAGE.replace("This page explains a fleet.", paragraph))
        self.assertTrue(any("DOC-03" in error for error in errors))

    def test_should_reject_unexpanded_acronym(self) -> None:
        errors = self.lint(VALID_PAGE.replace("explains a fleet", "explains the CLI"))
        self.assertTrue(any("DOC-10" in error for error in errors))

    def test_should_accept_expanded_acronym_and_http_method(self) -> None:
        content = VALID_PAGE.replace("explains a fleet", "explains the command-line interface (CLI) POST command")
        self.assertEqual([], self.lint(content))

    def test_should_reject_command_without_output(self) -> None:
        command = """```bash
agentsfleet --version
```"""
        errors = self.lint(VALID_PAGE.replace("This page explains a fleet.", command))
        self.assertTrue(any("DOC-15" in error for error in errors))

    def test_should_reject_multiple_h1_headings(self) -> None:
        errors = self.lint(VALID_PAGE + "\n# Another title\n")
        self.assertTrue(any("DOC-25" in error for error in errors))

    def test_should_reject_option_table_without_default(self) -> None:
        table = "| Option | Effect |\n| --- | --- |\n| `--force` | Skips the prompt. |"
        errors = self.lint(VALID_PAGE.replace("No related page applies.", table))
        self.assertTrue(any("DOC-19" in error for error in errors))

    def test_should_reject_procedure_table(self) -> None:
        table = "| Step | Result |\n| --- | --- |\n| Sign in | You receive a token. |"
        errors = self.lint(VALID_PAGE.replace("No related page applies.", table))
        self.assertTrue(any("DOC-27" in error for error in errors))

    def test_should_reject_sections_out_of_order(self) -> None:
        content = VALID_PAGE.replace(
            "## How it behaves\n\nYou create the fleet. `agentsfleet` receives each event.\n\n## Limits",
            "## Limits\n\nThe workspace limit comes from its configured policy.\n\n## How it behaves\n\nYou create the fleet. `agentsfleet` receives each event.\n\n## Limits",
        )
        errors = self.lint(content)
        self.assertTrue(any("DOC-P1" in error for error in errors))

    def test_should_reject_more_than_three_ignores(self) -> None:
        ignores = "\n".join(f"lint-ignore: DOC-0{number} — test" for number in range(1, 5))
        errors = self.lint(VALID_PAGE.replace("type: explanation", f"type: explanation\n{ignores}"))
        self.assertTrue(any("DOC-35" in error for error in errors))

    def test_should_check_api_drift_before_commit(self) -> None:
        hook = (ROOT / ".githooks/pre-commit").read_text(encoding="utf-8")
        self.assertIn("make test", hook)
        self.assertIn("api-reference/endpoint/*.mdx", hook)
        self.assertIn("make _lint-openapi-drift", hook)
        self.assertNotIn("skipping openapi drift check", (ROOT / "Makefile").read_text(encoding="utf-8"))
        self.assertIn("--max-time 10", (ROOT / "Makefile").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
