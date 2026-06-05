# 01 Intake — WhatsApp 群友 Persona 基礎資料

## 目的

收集建立 WhatsApp 群友 Persona 所需的最低資料，讓後續 6 個 prompt 可以穩定分析同一個目標成員。這一步只負責定義「要分析誰、在哪個群、已知背景是甚麼、輸出要避開甚麼」，不直接分析聊天內容。

## 輸入

請向使用者收集以下欄位：

1. `member_name`：目標群友暱稱或代號，例如 `Mika`、`Leo`、`Nora`。
2. `member_slug`：檔案用 slug，例如 `mika`、`leo`、`nora`。
3. `group_name`：假名或已匿名化 WhatsApp 群名，例如 `星河測試群`。
4. `member_background`：目標群友在群內的大概位置、關係、常見活動。
5. `style_hint`：使用者主觀覺得他的語氣、幽默方式、常見反應。
6. `safety_note`：不能亂講的內容，例如私事、舊事件、真人身份、舊原句。
7. `source_file`：WhatsApp 匯出的 `.txt` 路徑。

## 處理步驟

1. 先確認 `member_name` 和 `group_name` 是否是假名或已匿名化；如果看起來是真名，提醒使用者可改成代號。
2. 如果 `member_slug` 沒有提供，根據 `member_name` 轉成小寫英文字母、數字、`-` 或 `_`。
3. 如果 `member_background` 很短，要求使用者補一句「他通常在群裡扮演甚麼角色」。
4. 如果 `style_hint` 很空，要求使用者補一句「你希望模型抓住哪種說話感覺」。
5. 把所有欄位整理成下方輸出格式，供下一步 WhatsApp txt parser 和 LLM prompts 使用。

## 輸出格式

```yaml
member_name: Mika
member_slug: mika
group_name: 星河測試群
member_background: 經常一起打機，群內反應誇張，常接梗。
style_hint: 粵語口語，嘴賤但不是惡意，喜歡短句和誇張反應。
safety_note: 預設不要輸出舊原句，不主動翻舊事，不冒充真人。
source_file: C:\path\to\whatsapp-export.txt
```

## 安全規則

- 預設不要輸出舊原句。
- 只有使用者明確要求原句、逐字、引用或 exact wording 時，才允許短引用歷史原句。
- 成員名稱和群名應優先使用假名，避免把真人身份寫進公開 repo。
- 這一步不得把 WhatsApp 原文改寫成可直接複製的口頭禪清單。