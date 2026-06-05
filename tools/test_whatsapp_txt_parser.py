import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from whatsapp_txt_parser import extract_member_messages, format_group_persona_input, parse_whatsapp_txt


class WhatsAppTxtParserTest(unittest.TestCase):
    def test_parse_whatsapp_export_groups_multiline_messages(self):
        content = "\n".join(
            [
                "05/06/2026, 10:01 - Mika: 哈哈",
                "呢句係第二行",
                "05/06/2026, 10:02 - Leo: ok",
                "05/06/2026, 10:03 - Mika: <Media omitted>",
                "05/06/2026, 10:04 - Messages and calls are end-to-end encrypted.",
            ]
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chat.txt"
            path.write_text(content, encoding="utf-8")

            messages = parse_whatsapp_txt(path)

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["sender"], "Mika")
        self.assertEqual(messages[0]["text"], "哈哈\n呢句係第二行")
        self.assertEqual(messages[1]["sender"], "Leo")

    def test_extract_member_messages_filters_target_member(self):
        messages = [
            {"sender": "Mika", "text": "救命笑死", "timestamp": "05/06/2026, 10:01"},
            {"sender": "Leo", "text": "ok", "timestamp": "05/06/2026, 10:02"},
        ]

        result = extract_member_messages(messages, "Mika")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["text"], "救命笑死")

    def test_format_group_persona_input_does_not_request_old_quotes_by_default(self):
        messages = [
            {"sender": "Mika", "text": "救命笑死", "timestamp": "05/06/2026, 10:01"},
        ]

        output = format_group_persona_input("星河測試群", "Mika", messages)

        self.assertIn("WhatsApp 群聊 Persona 原材料", output)
        self.assertIn("目標群友：Mika", output)
        self.assertIn("預設不要輸出舊原句", output)
        self.assertIn("只有使用者明確要求原句", output)


if __name__ == "__main__":
    unittest.main()
