# 04 Context Builder — WhatsApp Group Persona 群組背景區塊生成

## 目的

把 `02 Group Context Analyzer` 的分析結果整理成 WhatsApp group persona 最終 `members/{member_slug}.md` 裡的「群組背景」區塊。這不是每個成員各自一份散亂記憶，而是把與目標成員有關的群組語境壓縮成乾淨、可讀、可給 chatbot 使用的 Markdown。

## 輸入

你會收到：

- `member_name`
- `group_name`
- `group_context_analysis`
- `member_relationship_notes`
- `safety_note`

## 處理步驟

1. 只保留對 chatbot 生成回覆有用的群組背景。
2. 把成員關係寫成抽象描述，不寫真實私事。
3. 把互動模式寫成「可使用的上下文」，不要寫成可直接複製的句子。
4. 把禁區寫清楚，讓後續 Persona 不會主動翻舊事。
5. 如果資訊不足，明確標記「資料不足」，不要腦補。

## 輸出格式

```markdown
## 群組背景

- 群組代號：{group_name}
- 常見主題：
- 整體氣氛：
- 回覆節奏：

## {member_name} 的群內位置

- 互動角色：
- 常一起接話的人：
- 常見觸發情境：

## 可用上下文

- 可以用來理解語氣的背景：
- 可以用來判斷關係的背景：

## 不應主動提及

- 私密資訊：
- 舊事件：
- 容易造成誤會的內容：
```

## 安全規則

- 預設不要輸出舊原句。
- 只有使用者明確要求原句、逐字、引用或 exact wording 時，才允許短引用歷史原句。
- 預設只概述群組事實、成員關係和互動傾向。
- 不要把群組背景寫成八卦紀錄。