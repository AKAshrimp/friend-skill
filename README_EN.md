# WhatsApp Group Persona Skill

Generate safe group persona skills from WhatsApp exported `.txt` files, member descriptions, and interaction patterns.

The goal is to capture rhythm, tone, humor, and interaction style without quoting old messages by default or impersonating a real person.

## Usage

```text
/create-group-persona
```

## Main data source

WhatsApp exported txt:

```text
05/06/2026, 10:01 - Mika: haha
05/06/2026, 10:02 - Leo: ok
```

## Outputs

- `memories.md`
- `persona.md`
- `style_rules.md`
- `meta.json`

## Safety

預設不要輸出舊原句。
只有使用者明確要求原句、逐字、引用或 exact wording 時，才允許短引用歷史原句。
Normal chats should imitate style, not copy historical messages.