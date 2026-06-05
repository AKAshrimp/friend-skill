import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GroupPersonaDomainTest(unittest.TestCase):
    def test_skill_and_prompts_use_whatsapp_group_persona_domain(self):
        files = [
            "SKILL.md",
            "README.md",
            "README_EN.md",
            "INSTALL.md",
            "prompts/intake.md",
            "prompts/memories_analyzer.md",
            "prompts/persona_analyzer.md",
            "prompts/memories_builder.md",
            "prompts/persona_builder.md",
        ]
        for filename in files:
            with self.subTest(filename=filename):
                text = (ROOT / filename).read_text(encoding="utf-8")
                self.assertIn("WhatsApp", text)
                self.assertRegex(text.lower(), r"group persona|群友 persona|群組 persona|群聊 persona")
                self.assertIn("預設不要輸出舊原句", text)
                self.assertIn("只有使用者明確要求原句", text)
                self.assertNotIn("\u524d\u4efb", text)
                self.assertNotIn("\u5206\u624b", text)

    def test_prompt_pipeline_files_are_detailed(self):
        files = [
            "prompts/intake.md",
            "prompts/memories_analyzer.md",
            "prompts/persona_analyzer.md",
            "prompts/memories_builder.md",
            "prompts/persona_builder.md",
            "prompts/merger.md",
            "prompts/correction_handler.md",
        ]
        required_sections = ["## 目的", "## 輸入", "## 處理步驟", "## 輸出格式", "## 安全規則"]
        for filename in files:
            with self.subTest(filename=filename):
                text = (ROOT / filename).read_text(encoding="utf-8")
                for section in required_sections:
                    self.assertIn(section, text)
                self.assertIn("預設不要輸出舊原句", text)
                self.assertIn("只有使用者明確要求原句", text)


if __name__ == "__main__":
    unittest.main()
