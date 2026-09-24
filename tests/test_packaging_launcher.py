"""Regression guards for the packaged app's first-launch bootstrap."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "packaging" / "build_app.sh"


class PackagedLauncherTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = BUILD_SCRIPT.read_text(encoding="utf-8")

    def test_partial_venv_is_not_treated_as_ready(self):
        self.assertIn('READY_MARKER="$VENV/.jev-ready"', self.script)
        self.assertIn('import objc, AppKit, Quartz, Vision', self.script)
        self.assertIn('environment_ready() {', self.script)
        self.assertIn('write_ready_marker()', self.script)

    def test_concurrent_first_launches_share_an_install_lock(self):
        self.assertIn('INSTALL_LOCK="$SUPPORT/venv-install.lock"', self.script)
        self.assertIn('if mkdir "$INSTALL_LOCK" 2>/dev/null; then', self.script)
        self.assertIn('lock_owner_is_running()', self.script)
        self.assertIn('install_lock_is_stale()', self.script)
        self.assertIn('本次不重复启动', self.script)


if __name__ == "__main__":
    unittest.main()
