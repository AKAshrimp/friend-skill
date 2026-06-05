---
name: create-group-persona
description: "Generate a safe WhatsApp group persona skill from exported group chat txt and user descriptions. | 从 WhatsApp 群聊 txt 和描述生成安全的群友 Persona Skill。"
argument-hint: "[member-name-or-slug]"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# WhatsApp 群友 Persona Skill 建立器

## 觸發条件

当使用者说以下任意內容時啟動：
- `/create-group-persona`
- "帮我建立群友 persona"
- "用 WhatsApp 群聊 txt 分析某個群友"
- "給 Mika / Leo / Nora 做一個群友 Persona"

当使用者对已有 Persona 说以下內容時，進入更新模式：
- `/update-group-persona {slug}`
- "我有新的 WhatsApp export txt"
- "這個群友不會這樣说"
- "Mika 應該更誇張一點"

当使用者说 `/list-group-personas` 時列出所有已生成的群友 Persona。

## 核心安全規則

預設不要輸出舊原句、舊事件細節、私密資訊或成員口頭禪。
只有使用者明確要求原句、逐字、引用或 exact wording 時，才允許短引用歷史原句。
普通聊天只模仿節奏、語氣強弱、幽默方式、語言習慣和互動模式。
不要冒充真人，不要聲稱自己就是目標群友本人。

## 工具使用規則

| 任务 | 使用工具 |
| --- | --- |
| 讀取 WhatsApp exported txt | `Read` 或 `Bash` |
| 解析 WhatsApp txt | `Bash` -> `python3 ${CLAUDE_SKILL_DIR}/tools/whatsapp_txt_parser.py` |
| 寫入/更新 Persona Skill | `Write` / `Edit` 或 `tools/skill_writer.py` |
| 版本管理 | `Bash` -> `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |

基礎目錄：Skill 檔案寫入 `./exes/{slug}/`。

## 主流程

### Step 1：基礎資訊录入

参考 `${CLAUDE_SKILL_DIR}/prompts/intake.md`，收集：
1. 成員暱稱/代號
2. WhatsApp 群組名稱
3. 成員背景
4. 說話風格和禁區

### Step 2：匯入 WhatsApp txt

使用者提供 WhatsApp 群聊匯出的 `.txt` 檔案后執行：

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/whatsapp_txt_parser.py \
  --file {path_to_export_txt} \
  --group "{group_name}" \
  --member "{member_name}" \
  --output /tmp/group_persona_input.txt
```

然后讀取 `/tmp/group_persona_input.txt`。

### Step 3：分析原材料

使用：
- `${CLAUDE_SKILL_DIR}/prompts/memories_analyzer.md`
- `${CLAUDE_SKILL_DIR}/prompts/persona_analyzer.md`

輸出群組背景、成員關係、目標群友表達風格、幽默方式、互動邊界和安全規則。

### Step 4：生成檔案

生成以下內容：
- `memories.md`：群組背景與成員互動记忆
- `persona.md`：目標群友 Persona
- `style_rules.md`：安全風格規則
- `meta.json`：元数据

### Step 5：寫入 Skill

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py \
  --action create \
  --slug {slug} \
  --meta /tmp/meta.json \
  --memories /tmp/memories.md \
  --persona /tmp/persona.md \
  --style-rules /tmp/style_rules.md \
  --base-dir ./exes
```

## 輸出行為

生成的 Persona 可以用於理解一個 WhatsApp 群友的表達風格，但不能預設複述舊訊息。
預設不要輸出舊原句；只有使用者明確要求原句時才允許短引用。