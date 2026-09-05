import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RENDER_SCRIPT = REPO_ROOT / "scripts" / "render-audit-pdf.py"


class RenderAuditPdfCliTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.browser_path = self.temp_path / "google-chrome"
        self.args_path = self.temp_path / "browser-args.txt"
        self.profile_path = self.temp_path / "browser-profile.txt"
        self.report_path = self.temp_path / "sample-report.md"
        self.pdf_path = self.temp_path / "sample-report.pdf"

        self.browser_path.write_text(
            """#!/bin/sh
printf '%s\\n' "$@" > "$BROWSER_ARGS_FILE"
for arg do
    case "$arg" in
        --user-data-dir=*)
            profile="${arg#*=}"
            test -d "$profile" || exit 2
            printf '%s' "$profile" > "$BROWSER_PROFILE_FILE"
            test "$BROWSER_EXIT_AFTER_PROFILE" != "1" || exit 3
            ;;
        --print-to-pdf=*)
            printf '%%PDF-1.4' > "${arg#*=}"
            ;;
    esac
done
""",
            encoding="utf-8",
        )
        self.browser_path.chmod(0o755)
        self.report_path.write_text("# Sample audit\n", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_renderer(self, no_sandbox: bool = False, browser_failure: bool = False):
        env = os.environ.copy()
        env["PATH"] = f"{self.temp_path}{os.pathsep}{env['PATH']}"
        env["BROWSER_ARGS_FILE"] = str(self.args_path)
        env["BROWSER_PROFILE_FILE"] = str(self.profile_path)
        if no_sandbox:
            env["AI_VISIBILITY_PDF_NO_SANDBOX"] = "1"
        else:
            env.pop("AI_VISIBILITY_PDF_NO_SANDBOX", None)
        if browser_failure:
            env["BROWSER_EXIT_AFTER_PROFILE"] = "1"
        else:
            env.pop("BROWSER_EXIT_AFTER_PROFILE", None)

        return subprocess.run(
            [
                sys.executable,
                str(RENDER_SCRIPT),
                str(self.report_path),
                str(self.pdf_path),
            ],
            capture_output=True,
            text=True,
            env=env,
            timeout=30,
        )

    def test_browser_runs_with_an_isolated_profile_and_sandbox(self):
        result = self.run_renderer()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertGreater(self.pdf_path.stat().st_size, 0)

        browser_args = self.args_path.read_text(encoding="utf-8").splitlines()
        self.assertNotIn("--no-sandbox", browser_args)
        self.assertIn("--disable-extensions", browser_args)
        self.assertIn("--disable-dev-shm-usage", browser_args)

        user_data_args = [
            arg for arg in browser_args if arg.startswith("--user-data-dir=")
        ]
        self.assertEqual(len(user_data_args), 1)
        self.assertFalse(Path(self.profile_path.read_text(encoding="utf-8")).exists())

    def test_no_sandbox_requires_explicit_opt_in_and_warns(self):
        result = self.run_renderer(no_sandbox=True)

        self.assertEqual(result.returncode, 0, result.stderr)
        browser_args = self.args_path.read_text(encoding="utf-8").splitlines()
        self.assertIn("--no-sandbox", browser_args)
        self.assertIn("[WARNING] Browser sandbox disabled", result.stderr)

    def test_isolated_profile_is_removed_when_browser_fails(self):
        result = self.run_renderer(browser_failure=True)

        self.assertEqual(result.returncode, 1)
        self.assertFalse(Path(self.profile_path.read_text(encoding="utf-8")).exists())


if __name__ == "__main__":
    unittest.main()
