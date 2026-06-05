# WhatsApp Group Persona Framework

這是一個用來把 **WhatsApp 群聊匯出 `.txt`** 轉成「群友 Persona」的框架。

它不是 LoRA，也不是模型微調。它的用途是：

```text
WhatsApp export txt
→ 7 個 prompt 框架分析
→ 產生單一成員 Persona Markdown
→ 給 chatbot / RAG / n8n 使用
```

核心目標是模仿群友的 **說話節奏、語氣強弱、幽默方式、互動模式**，但預設不輸出舊原句、不翻舊事、不冒充真人。

## 專案結構

```text
prompts/
  intake.md                  # 01 收集成員、群組、風格、禁區
  memories_analyzer.md        # 02 分析群組背景
  persona_analyzer.md         # 03 分析目標群友風格
  memories_builder.md         # 04 整理群組背景區塊
  persona_builder.md          # 05 產生單一 member markdown
  merger.md                   # 06 追加新聊天記錄後合併
  correction_handler.md       # 07 人手修正 Persona

tools/
  whatsapp_txt_parser.py      # 解析 WhatsApp 匯出 txt
  skill_writer.py             # 產生本地 Persona Skill 檔案
  version_manager.py          # 版本回滾工具
```

## 資料來源

主要使用 WhatsApp 匯出的 `.txt`：

```text
05/06/2026, 10:01 - Mika: 哈哈
05/06/2026, 10:02 - Leo: ok
```

示例名稱和群名都是假的，例如：

```text
Mika
Leo
Nora
Chris
星河測試群
```

請不要把真實 WhatsApp 匯出檔、真實成員名、真實群名 push 到公開 repo。

## 使用方式

### 1. 解析 WhatsApp txt

```powershell
python tools/whatsapp_txt_parser.py `
  --file chat.txt `
  --group "星河測試群" `
  --member "Mika" `
  --output output.md
```

### 2. 用 LLM 依序跑 7 個 prompt

把 `output.md` 和手動補充資料交給 LLM，按以下順序處理：

```text
01 intake
02 memories_analyzer
03 persona_analyzer
04 memories_builder
05 persona_builder
06 merger       # 有新資料時才用
07 correction   # 需要人手修正時才用
```

理想最終輸出是：

```text
members/mika.md
members/leo.md
members/nora.md
```

每個成員只需要一個 Markdown，方便之後 merge 到 chatbot。

## 安全規則

- 預設不要輸出舊原句。
- 只有使用者明確要求原句，才允許短引用歷史原句。
- 只有使用者明確要求「原句 / 逐字 / 引用 / exact wording」時，才允許短引用歷史原句。
- 普通聊天只模仿風格，不複製歷史訊息。
- 不主動翻舊事。
- 不冒充真人。
- 不把私密資訊當玩笑素材。

## 測試

```powershell
python -m unittest discover -s tools -p "test_*.py" -v
```

目前測試覆蓋：

- WhatsApp txt parser
- Persona writer
- 7 個 prompt 是否保留必要安全規則
- 假名 / 匿名化範例

## Push 前提醒

建議只 push 框架：

```text
prompts/
tools/
README.md
SKILL.md
INSTALL.md
```

不要 push：

```text
真實 WhatsApp export txt
真實 members/*.md
真實群友名字
真實群名
```