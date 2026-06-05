# WhatsApp Group Persona Skill 安裝說明

## Claude Code

```bash
mkdir -p .claude/skills
git clone <repo-url> .claude/skills/create-group-persona
```

## OpenClaw

```bash
git clone <repo-url> ~/.openclaw/workspace/skills/create-group-persona
```

## 依賴

```bash
pip3 install -r requirements.txt
```

## 使用

```text
/create-group-persona
```

## WhatsApp txt parser

```bash
python3 tools/whatsapp_txt_parser.py \
  --file chat.txt \
  --group "群名" \
  --member "Mika" \
  --output /tmp/group_persona_input.txt
```

## 安全規則

預設不要輸出舊原句。
只有使用者明確要求原句、逐字、引用或 exact wording 時，才允許短引用歷史原句。