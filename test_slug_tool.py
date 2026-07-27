import unittest

from slug_tool import slugify


class SlugifyTests(unittest.TestCase):
    def test_normalizes_spaces_and_punctuation(self):
        self.assertEqual(slugify("Harness Review: Common2!"), "harness-review-common2")

    def test_collapses_repeated_separators(self):
        self.assertEqual(slugify("  API___delivery---demo  "), "api-delivery-demo")

    def test_returns_empty_for_non_ascii_only_input(self):
        self.assertEqual(slugify("中文"), "")


if __name__ == "__main__":
    unittest.main()
