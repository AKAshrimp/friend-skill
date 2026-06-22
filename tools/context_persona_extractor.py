#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from whatsapp_txt_parser import parse_whatsapp_txt, extract_member_messages


EN_WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
TRAD_ONLY_HINTS = ("嘅", "喺", "咩", "唔", "佢", "咁", "呢", "冇", "俾", "緊", "啲")
SIMPLIFIED_HINTS = ("吗", "吗", "吗", "吗", "吗", "这", "们", "为", "个", "还", "说", "爱")
DEFAULT_EXCLUDED_ENGLISH_WORDS = {
    "http",
    "https",
    "www",
    "com",
}
EMOJI_RE = re.compile(
    "[" 
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "]+",
    re.UNICODE,
)


def classify_language(text: str) -> str:
    has_cjk = bool(CJK_RE.search(text))
    has_en = bool(EN_WORD_RE.search(text))
    if has_cjk and has_en:
        return "mixed"
    if has_en:
        return "english"
    if has_cjk:
        return "cjk"
    return "other"


def detect_traditional_hint(text: str) -> str:
    trad = sum(text.count(ch) for ch in TRAD_ONLY_HINTS)
    simp = sum(text.count(ch) for ch in SIMPLIFIED_HINTS)
    if trad > simp:
        return "繁體傾向"
    if simp > trad:
        return "簡體傾向"
    return "未能明確判定"


def sentence_length(text: str) -> int:
    return len(text.split())


def build_excluded_english_words(member_name: str, extra_words: list[str] | None = None) -> set[str]:
    words = set(DEFAULT_EXCLUDED_ENGLISH_WORDS)
    words.update(w.lower() for w in EN_WORD_RE.findall(member_name))
    if extra_words:
        words.update(w.strip().lower() for w in extra_words if w.strip())
    return words


def extract_style_english_words(text: str, excluded_words: set[str]) -> list[str]:
    return [
        word
        for word in (w.lower() for w in EN_WORD_RE.findall(text))
        if word and word not in excluded_words
    ]


def context_windows(messages: list[dict], member_name: str, before: int = 3, after: int = 2) -> list[dict]:
    out: list[dict] = []
    for i, msg in enumerate(messages):
        if member_name.casefold() not in str(msg.get("sender", "")).casefold():
            continue
        start = max(0, i - before)
        end = min(len(messages), i + after + 1)
        window = messages[start:end]
        out.append(
            {
                "target": msg,
                "context": window,
            }
        )
    return out


def summarize(
    messages: list[dict],
    member_name: str,
    group_name: str,
    excluded_english_words: list[str] | None = None,
) -> dict:
    texts = [m.get("text", "") for m in messages if m.get("text")]
    excluded_words = build_excluded_english_words(member_name, excluded_english_words)
    lang_counts = Counter(classify_language(t) for t in texts)
    emoji_count = sum(len(EMOJI_RE.findall(t)) for t in texts)
    q_count = sum(1 for t in texts if "?" in t or "？" in t)
    ex_count = sum(1 for t in texts if "!" in t or "！" in t)
    avg_len = round(sum(sentence_length(t) for t in texts) / max(1, len(texts)), 2)
    trad_hint = detect_traditional_hint(" ".join(texts[:5000]))
    short_count = sum(1 for t in texts if len(t.strip()) <= 8)
    medium_count = sum(1 for t in texts if 9 <= len(t.strip()) <= 24)
    long_count = sum(1 for t in texts if len(t.strip()) > 24)
    at_count = sum(1 for t in texts if "@" in t or "＠" in t)
    ellipsis_count = sum(1 for t in texts if "..." in t or "…" in t)
    capsish_count = sum(1 for t in texts if any(ch.isupper() for ch in t) and any(ch.islower() for ch in t))
    cantonese_hint = sum(1 for t in texts if any(marker in t for marker in TRAD_ONLY_HINTS))

    word_counter = Counter()
    for t in texts:
        word_counter.update(extract_style_english_words(t, excluded_words))

    def sample_texts(predicate, limit=12):
        out = []
        for t in texts:
            if predicate(t):
                out.append(t)
            if len(out) >= limit:
                break
        return out

    return {
        "group_name": group_name,
        "member_name": member_name,
        "message_count": len(texts),
        "language_mix": dict(lang_counts),
        "traditional_hint": trad_hint,
        "avg_word_count": avg_len,
        "length_profile": {
            "short": short_count,
            "medium": medium_count,
            "long": long_count,
        },
        "emoji_usage": emoji_count,
        "question_messages": q_count,
        "exclamation_messages": ex_count,
        "mention_messages": at_count,
        "ellipsis_messages": ellipsis_count,
        "mixed_case_messages": capsish_count,
        "cantonese_marker_messages": cantonese_hint,
        "excluded_english_words": sorted(excluded_words),
        "top_english_words": word_counter.most_common(30),
        "samples_by_signal": {
            "short": sample_texts(lambda t: len(t.strip()) <= 8),
            "mixed": sample_texts(lambda t: classify_language(t) == "mixed"),
            "question": sample_texts(lambda t: "?" in t or "？" in t),
            "exclamation": sample_texts(lambda t: "!" in t or "！" in t),
            "mention": sample_texts(lambda t: "@" in t or "＠" in t),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract first-layer persona stats from WhatsApp export")
    parser.add_argument("--file", required=True)
    parser.add_argument("--member", required=True)
    parser.add_argument("--group", default="")
    parser.add_argument("--output", required=True)
    parser.add_argument("--before", type=int, default=3)
    parser.add_argument("--after", type=int, default=2)
    parser.add_argument("--sample", type=int, default=40)
    parser.add_argument(
        "--exclude-word",
        action="append",
        default=[],
        help="English token to exclude from style word statistics, useful for names and URLs.",
    )
    args = parser.parse_args()

    file_path = Path(args.file)
    all_messages = parse_whatsapp_txt(file_path)
    member_messages = extract_member_messages(all_messages, args.member)
    windows = context_windows(all_messages, args.member, before=args.before, after=args.after)

    summary = summarize(member_messages, args.member, args.group, args.exclude_word)
    summary["context_window_count"] = len(windows)
    summary["samples"] = []

    seen = 0
    for item in windows[: args.sample]:
        target = item["target"]
        context = item["context"]
        summary["samples"].append(
            {
                "target": {
                    "timestamp": target.get("timestamp", ""),
                    "sender": target.get("sender", ""),
                    "text": target.get("text", ""),
                },
                "context_senders": [m.get("sender", "") for m in context],
                "context_texts": [m.get("text", "") for m in context],
            }
        )
        seen += 1

    out_path = Path(args.output)
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
