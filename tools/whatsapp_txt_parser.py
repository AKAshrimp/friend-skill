#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import io
from pathlib import Path


MESSAGE_RE = re.compile(
    r"^(?P<timestamp>\d{1,2}/\d{1,2}/\d{2,4}(?:,\s+|\s+)\d{1,2}:\d{2}(?:\s?[AP]M)?)\s+-\s+(?P<sender>[^:：]+)[:：]\s*(?P<text>.*)$",
    re.IGNORECASE,
)

SKIP_TEXTS = (
    "<Media omitted>",
    "Messages and calls are end-to-end encrypted.",
    "This message was deleted",
    "You deleted this message",
)


def parse_whatsapp_txt(path: str | Path) -> list[dict]:
    messages: list[dict] = []
    current: dict | None = None

    path = Path(path)
    with io.open(str(path), mode="r", encoding="utf-8", errors="replace") as fh:
        for raw_line in fh:
            line = raw_line.strip("\ufeff\u200e\r\n")
            match = MESSAGE_RE.match(line)
            if match:
                if current and _is_useful_text(current["text"]):
                    messages.append(current)
                current = {
                    "timestamp": match.group("timestamp").strip(),
                    "sender": match.group("sender").strip(),
                    "text": match.group("text").strip(),
                }
                continue

            if current and line.strip():
                current["text"] += "\n" + line.strip()

    if current and _is_useful_text(current["text"]):
        messages.append(current)

    return messages


def extract_member_messages(messages: list[dict], member_name: str) -> list[dict]:
    target = member_name.casefold()
    return [
        message
        for message in messages
        if target in str(message.get("sender", "")).casefold()
    ]


def format_group_persona_input(
    group_name: str,
    member_name: str,
    messages: list[dict],
    limit: int = 200,
) -> str:
    selected = messages[-limit:]
    lines = [
        "# WhatsApp 群聊 Persona 原材料",
        f"群組名稱：{group_name}",
        f"目標群友：{member_name}",
        f"訊息数量：{len(selected)}",
        "",
        "安全規則：預設不要輸出舊原句；只有使用者明確要求原句、逐字、引用或 exact wording 時，才允許短引用。",
        "",
        "## 目標群友訊息",
    ]
    for index, message in enumerate(selected, 1):
        lines.append(
            f"{index}. [{message.get('timestamp', '')}] {message.get('sender', '')}: {message.get('text', '')}"
        )
    return "\n".join(lines)


def _is_useful_text(text: str) -> bool:
    value = str(text).strip()
    return bool(value) and not any(skip in value for skip in SKIP_TEXTS)


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse WhatsApp exported txt for group persona generation")
    parser.add_argument("--file", required=True)
    parser.add_argument("--member", required=True)
    parser.add_argument("--group", default="")
    parser.add_argument("--output", required=True)
    parser.add_argument("--limit", type=int, default=200)
    args = parser.parse_args()

    messages = extract_member_messages(parse_whatsapp_txt(args.file), args.member)
    output = format_group_persona_input(args.group, args.member, messages, args.limit)
    Path(args.output).write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
