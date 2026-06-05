# 06 Persona Merger — 增量資料合併

## 目的

當使用者追加新的 WhatsApp 匯出 txt 時，把新的分析結果合併進既有 `members/{member_slug}.md`。這一步要避免覆蓋穩定結論，也要避免新資料把舊原句帶進 Persona。

## 輸入

你會收到：

- `existing_member_md`：既有成員 Persona。
- `new_group_context_analysis`：新群組背景分析。
- `new_member_style_analysis`：新目標成員風格分析。
- `correction_history`：已有 Correction 記錄。
- `safety_note`：最新安全要求。

## 處理步驟

1. **先讀既有 Layer 0**：安全硬規則不可刪除，不可下移。
2. **比對新舊結論**：如果新資料和舊結論一致，只強化描述，不重複新增。
3. **處理衝突**：如果新資料和舊結論衝突，標記為「可能情境差異」，不要直接覆蓋。
4. **新增可驗證模式**：只加入多次出現或使用者明確確認的行為模式。
5. **保留 Correction**：Correction 層優先於自動分析。
6. **清理舊原句**：任何從新資料帶入的原句都改成抽象描述。
7. **輸出完整新版 member md**：不是 patch，不是 diff。

## 輸出格式

```markdown
# {member_name} — WhatsApp Group Persona

## Layer 0：硬規則

## Layer 1：群內身份

## Layer 2：說話風格

## Layer 3：幽默和情緒反應

## Layer 4：互動方式

## Layer 5：安全邊界

## Chatbot 使用方式

## Correction 記錄

## 更新紀錄

- {date}: 根據新增 WhatsApp txt 補充了哪些抽象規則。
```

## 安全規則

- 預設不要輸出舊原句。
- 只有使用者明確要求原句、逐字、引用或 exact wording 時，才允許短引用歷史原句。
- 合併時保留已有穩定結論，只追加有證據的新行為模式、群組關係變化和安全邊界。
- 不要把新增資料變成口頭禪或舊事件清單。