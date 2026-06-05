import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from skill_writer import create_skill, load_json_file, slugify


class GroupPersonaWriterTest(unittest.TestCase):
    def test_create_skill_writes_group_member_persona_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = create_skill(
                base_dir=Path(tmp),
                slug="mika",
                meta={
                    "name": "Mika",
                    "group_name": "星河測試群",
                    "role": "group member",
                    "style_tags": ["嘴賤", "誇張反應"],
                },
                memories_content="# Group Context\n\nMika is active in the group.",
                persona_content="# Mika Persona\n\nUse lively Cantonese.",
                style_rules_content="# Style Rules\n\nDefault: do not quote old messages.",
            )

            self.assertTrue((skill_dir / "style_rules.md").exists())
            skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("name: member_mika", skill_text)
            self.assertIn("PART C：安全風格規則", skill_text)
            self.assertIn("Default: do not quote old messages.", skill_text)
            self.assertNotIn("\u524d\u4efb", skill_text)
            self.assertNotIn("\u5206\u624b", skill_text)

            meta = json.loads((skill_dir / "meta.json").read_text(encoding="utf-8"))
            self.assertEqual(meta["group_name"], "星河測試群")

    def test_slugify_empty_defaults_to_member(self):
        self.assertEqual(slugify(""), "member")

    def test_load_json_file_accepts_utf8_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "meta.json"
            path.write_text('\ufeff{"name":"Mika"}', encoding="utf-8")

            self.assertEqual(load_json_file(path), {"name": "Mika"})


if __name__ == "__main__":
    unittest.main()
