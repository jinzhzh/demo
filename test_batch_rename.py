#!/usr/bin/env python3
"""
test_batch_rename.py — Unit tests for batch_rename.py

Covers three scenarios:
  1. Dry-run mode (no files modified)
  2. Empty manifest handling
  3. Illegal characters in filenames
"""

import csv
import os
import sys
import tempfile
import unittest

# Import the module under test
sys.path.insert(0, os.path.dirname(__file__))
import batch_rename


class TestDryRun(unittest.TestCase):
    """Scenario 1: Dry-run should not modify any files."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        # Create a real file that will appear in the manifest
        self.src = os.path.join(self.tmpdir, "old_file.txt")
        with open(self.src, "w") as f:
            f.write("hello")

        self.manifest = os.path.join(self.tmpdir, "manifest.csv")
        with open(self.manifest, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["old_name", "new_name"])
            writer.writerow(["old_file.txt", "new_file.txt"])

    def test_dry_run_does_not_rename(self):
        entries = batch_rename.load_manifest(self.manifest)
        plan, _ = batch_rename.build_plan(entries, root=self.tmpdir)

        # In dry-run mode we simply inspect the plan — no os.rename is called
        self.assertEqual(plan[0]["status"], "ready")
        # Verify the original file still exists
        self.assertTrue(os.path.exists(os.path.join(self.tmpdir, "old_file.txt")))
        # Verify the new file does NOT exist (dry-run didn't create it)
        self.assertFalse(os.path.exists(os.path.join(self.tmpdir, "new_file.txt")))


class TestEmptyManifest(unittest.TestCase):
    """Scenario 2: Empty manifest should raise ValueError."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def test_empty_manifest_raises(self):
        manifest = os.path.join(self.tmpdir, "empty.csv")
        with open(manifest, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["old_name", "new_name"])
            # No data rows

        with self.assertRaises(ValueError) as ctx:
            batch_rename.load_manifest(manifest)
        self.assertIn("empty", str(ctx.exception).lower())

    def test_missing_columns_raises(self):
        manifest = os.path.join(self.tmpdir, "bad.csv")
        with open(manifest, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["wrong_col", "another_col"])
            writer.writerow(["a", "b"])

        with self.assertRaises(ValueError) as ctx:
            batch_rename.load_manifest(manifest)
        self.assertIn("columns", str(ctx.exception).lower())


class TestIllegalCharacters(unittest.TestCase):
    """Scenario 3: Filenames with illegal characters should be skipped."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def test_illegal_chars_detected(self):
        err = batch_rename.validate_name('file<bad>.txt')
        self.assertIsNotNone(err)
        self.assertIn("illegal", err.lower())

    def test_plan_skips_illegal_names(self):
        manifest = os.path.join(self.tmpdir, "manifest.csv")
        with open(manifest, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["old_name", "new_name"])
            writer.writerow(["good.txt", 'bad<file>.txt'])

        entries = batch_rename.load_manifest(manifest)
        plan, warnings = batch_rename.build_plan(entries, root=self.tmpdir)

        # The entry with illegal characters should be skipped
        self.assertEqual(plan[0]["status"], "skipped")
        self.assertIn("illegal", plan[0]["reason"].lower())

    def test_clean_names_pass_validation(self):
        self.assertIsNone(batch_rename.validate_name("valid-file_name (1).txt"))
        self.assertIsNone(batch_rename.validate_name("UPPERCASE.TXT"))


class TestExecutePlan(unittest.TestCase):
    """Bonus: Verify actual rename works."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.src = os.path.join(self.tmpdir, "rename_me.txt")
        with open(self.src, "w") as f:
            f.write("data")

    def test_rename_succeeds(self):
        plan = [{
            "old_name": "rename_me.txt",
            "new_name": "renamed.txt",
            "old_path": self.src,
            "new_path": os.path.join(self.tmpdir, "renamed.txt"),
            "status": "ready",
            "reason": None,
        }]
        results = batch_rename.execute_plan(plan)
        self.assertEqual(results[0]["status"], "renamed")
        self.assertTrue(os.path.exists(os.path.join(self.tmpdir, "renamed.txt")))
        self.assertFalse(os.path.exists(self.src))


if __name__ == "__main__":
    unittest.main()
