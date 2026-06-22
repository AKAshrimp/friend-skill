import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from context_persona_extractor import summarize, context_windows


class ContextPersonaExtractorTest(unittest.TestCase):
    def test_context_windows_captures_surrounding_messages(self):
        messages = [
            {"sender": "A", "text": "one"},
            {"sender": "B", "text": "two"},
            {"sender": "Mika", "text": "hello"},
            {"sender": "C", "text": "four"},
            {"sender": "D", "text": "five"},
        ]

        windows = context_windows(messages, "Mika", before=2, after=1)

        self.assertEqual(len(windows), 1)
        self.assertEqual([m["sender"] for m in windows[0]["context"]], ["A", "B", "Mika", "C"])

    def test_summarize_keeps_english_words_and_traditional_hint(self):
        messages = [
            {"sender": "Mika", "text": "ok la, 唔該 thanks", "timestamp": "1"},
            {"sender": "Mika", "text": "let's go haha", "timestamp": "2"},
        ]

        summary = summarize(messages, "Mika", "group")

        self.assertEqual(summary["member_name"], "Mika")
        self.assertIn(summary["traditional_hint"], ["繁體傾向", "未能明確判定"])
        self.assertGreaterEqual(summary["language_mix"].get("mixed", 0), 1)
        self.assertTrue(any(word == "thanks" for word, _ in summary["top_english_words"]))

    def test_summarize_excludes_member_names_from_english_word_stats(self):
        messages = [
            {"sender": "Mika", "text": "ok alex blake casey need go", "timestamp": "1"},
            {"sender": "Mika", "text": "devon ellis flynn gray can come", "timestamp": "2"},
        ]

        summary = summarize(
            messages,
            "Mika",
            "group",
            excluded_english_words=["alex", "blake", "casey", "devon", "ellis", "flynn", "gray"],
        )
        words = [word for word, _ in summary["top_english_words"]]

        self.assertNotIn("alex", words)
        self.assertNotIn("blake", words)
        self.assertNotIn("casey", words)
        self.assertIn("need", words)
        self.assertIn("can", words)


if __name__ == "__main__":
    unittest.main()
