# WhatsApp 群友 Persona 生成器計劃

目標：把專案改成只處理 WhatsApp 匯出的 `.txt` 群聊資料，產生安全的群友 Persona 框架。

## 範圍

- 保留 `tools/whatsapp_txt_parser.py` 解析 WhatsApp txt。
- 保留 `tools/skill_writer.py` 產生本地 Persona Skill。
- 使用假名示例：`Mika`、`Leo`、`Nora`、`Chris`。
- 使用假群名示例：`星河測試群`。
- 預設不要輸出舊原句；只有使用者明確要求原句、逐字、引用或 exact wording 時才允許短引用。

## 不包含

- 不包含真實 WhatsApp 匯出檔。
- 不包含真實成員名字、群名或私密聊天內容。
- 不保留微信、iMessage、SMS、照片或社交媒體 parser。
