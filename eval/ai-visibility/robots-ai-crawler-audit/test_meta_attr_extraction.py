"""Extracts the meta/data-nosnippet extraction snippet embedded in
skills/ai-visibility/robots-ai-crawler-audit/references/checks.md (the
`python3 - "$PAGE" <<'PY' ... PY` heredoc) and runs it directly against
representative HTML, so a regression in that snippet's regex/parsing logic
fails a PR instead of only being caught by hand-authored golden reports that
never actually execute it (run_eval.py checks report *shape*, not that the
skill's own extraction command produces the claimed finding from the input)."""
import re
import subprocess
import sys
import unittest
from pathlib import Path

CHECKS_MD = (
    Path(__file__).resolve().parents[3]
    / "skills"
    / "ai-visibility"
    / "robots-ai-crawler-audit"
    / "references"
    / "checks.md"
)


def extract_snippet() -> str:
    text = CHECKS_MD.read_text(encoding="utf-8")
    match = re.search(r"python3 - \"\$PAGE\" <<'PY'\n(.*?)\nPY", text, re.DOTALL)
    if not match:
        raise AssertionError("could not find the meta/data-nosnippet extraction heredoc in checks.md")
    return match.group(1)


def run_snippet(html: str) -> list[str]:
    snippet = extract_snippet()
    with subprocess.Popen(
        [sys.executable, "-c", snippet, "/dev/stdin"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ) as proc:
        out, err = proc.communicate(html)
    assert proc.returncode == 0, err
    return [line for line in out.splitlines() if line.strip()]


class MetaAttrExtractionTest(unittest.TestCase):
    def test_attribute_order_independent(self):
        html = '<meta content="max-snippet:0" name="robots">'
        self.assertEqual(run_snippet(html), ['name="robots" content="max-snippet:0"'])

    def test_unquoted_attribute_values_are_recognized(self):
        html = "<meta name=robots content=max-snippet:0>"
        self.assertEqual(run_snippet(html), ['name="robots" content="max-snippet:0"'])

    def test_google_specific_meta_name(self):
        html = '<meta content="nosnippet" name="googlebot">'
        self.assertEqual(run_snippet(html), ['name="googlebot" content="nosnippet"'])

    def test_bare_boolean_data_nosnippet_on_span_is_active(self):
        html = "<span data-nosnippet>excluded text</span>"
        self.assertEqual(
            run_snippet(html), ["data-nosnippet on <span>: active snippet exclusion"]
        )

    def test_data_nosnippet_on_unsupported_element_is_invalid(self):
        html = "<p data-nosnippet>excluded text</p>"
        self.assertEqual(
            run_snippet(html),
            ["data-nosnippet on <p>: invalid markup, not honored by Google"],
        )

    def test_class_containing_the_substring_is_not_a_false_positive(self):
        html = '<div class="data-nosnippet-caption">caption text</div>'
        self.assertEqual(run_snippet(html), [])

    def test_unrelated_data_attribute_prefix_is_not_a_false_positive(self):
        html = "<span data-nosnippet-extra>text</span>"
        self.assertEqual(run_snippet(html), [])


if __name__ == "__main__":
    unittest.main()
