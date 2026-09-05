import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATE_SCRIPT = REPO_ROOT / "scripts" / "validate-workflows.py"
PINNED_CHECKOUT = "actions/checkout@" + ("a" * 40)


class ValidateWorkflowsTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.scripts_dir = self.temp_path / "scripts"
        self.scripts_dir.mkdir()
        self.script_path = self.scripts_dir / "validate-workflows.py"
        shutil.copyfile(VALIDATE_SCRIPT, self.script_path)
        self.workflows_dir = self.temp_path / ".github" / "workflows"
        self.workflows_dir.mkdir(parents=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_workflow(self, name: str, content: str) -> Path:
        path = self.workflows_dir / name
        path.write_text(content, encoding="utf-8")
        return path

    def run_validator(self):
        return subprocess.run(
            [sys.executable, str(self.script_path)],
            cwd=self.temp_path,
            capture_output=True,
            text=True,
        )

    def test_accepts_pinned_unquoted_uses(self):
        self.write_workflow(
            "ok.yml",
            f"""\
name: OK
on: push
jobs:
  build:
    permissions:
      contents: read
    steps:
      - uses: {PINNED_CHECKOUT}
""",
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_mutable_ref_behind_a_quoted_uses_key(self):
        self.write_workflow(
            "bad.yml",
            """\
name: Bad
on: push
jobs:
  build:
    permissions:
      contents: read
    steps:
      - 'uses': attacker/action@main
""",
        )
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("attacker/action@main", result.stderr)

    def test_rejects_write_permission_behind_a_quoted_permissions_key(self):
        self.write_workflow(
            "bad-permissions.yml",
            f"""\
name: Bad permissions
on: push
jobs:
  build:
    'permissions':
      'pull-requests': 'write'
    steps:
      - uses: {PINNED_CHECKOUT}
""",
        )
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("pull-requests", result.stderr)

    def test_accepts_quoted_pinned_uses_value(self):
        self.write_workflow(
            "quoted-value.yml",
            f"""\
name: Quoted value
on: push
jobs:
  build:
    permissions:
      contents: read
    steps:
      - uses: '{PINNED_CHECKOUT}'
""",
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_mutable_ref_with_whitespace_before_the_uses_colon(self):
        # YAML permits separation whitespace before a mapping colon, so
        # `uses : x` is the same key as `uses: x`. A validator that only
        # recognizes the no-space form would let this bypass SHA pinning.
        self.write_workflow(
            "spaced-colon.yml",
            """\
name: Bad
on: push
jobs:
  build:
    permissions:
      contents: read
    steps:
      - uses : attacker/action@main
""",
        )
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("attacker/action@main", result.stderr)

    def test_rejects_write_permission_with_whitespace_before_the_permissions_colon(self):
        self.write_workflow(
            "spaced-permissions.yml",
            f"""\
name: Bad
on: push
jobs:
  build:
    permissions :
      pull-requests: write
    steps:
      - uses: {PINNED_CHECKOUT}
""",
        )
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("pull-requests", result.stderr)

    def test_ignores_a_permissions_named_action_input(self):
        # A step's `with:` inputs are arbitrary action-defined keys and may
        # happen to be named "permissions" — that is not a workflow/job
        # permissions block and must not be scanned as one.
        self.write_workflow(
            "action-input.yml",
            f"""\
name: OK
on: push
jobs:
  build:
    permissions:
      contents: read
    steps:
      - uses: {PINNED_CHECKOUT}
        with:
          permissions: write-all
""",
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
