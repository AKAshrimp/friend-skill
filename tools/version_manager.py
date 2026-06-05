#!/usr/bin/env python3
"""
版本管理器

负责 Skill 檔案的版本存档和回滚。

用法：
    python version_manager.py --action list --slug xiaomei --base-dir ./exes
    python version_manager.py --action rollback --slug xiaomei --version v2 --base-dir ./exes
"""

from __future__ import annotations

import json
import shutil
import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone

MAX_VERSIONS = 10  # 最多保留的版本数


def list_versions(skill_dir: Path) -> list:
    """列出所有歷史版本"""
    versions_dir = skill_dir / "versions"
    if not versions_dir.exists():
        return []

    versions = []
    for v_dir in sorted(versions_dir.iterdir()):
        if not v_dir.is_dir():
            continue

        version_name = v_dir.name
        mtime = v_dir.stat().st_mtime
        archived_at = datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
        files = [f.name for f in v_dir.iterdir() if f.is_file()]

        versions.append({
            "version": version_name,
            "archived_at": archived_at,
            "files": files,
            "path": str(v_dir),
        })

    return versions


def rollback(skill_dir: Path, target_version: str) -> bool:
    """回滚到指定版本"""
    version_dir = skill_dir / "versions" / target_version

    if not version_dir.exists():
        print(f"错误：版本 {target_version} 不存在", file=sys.stderr)
        return False

    # 先存档当前版本
    meta_path = skill_dir / "meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        current_version = meta.get("version", "v?")
        backup_dir = skill_dir / "versions" / f"{current_version}_before_rollback"
        backup_dir.mkdir(parents=True, exist_ok=True)
        for fname in ("SKILL.md", "memories.md", "persona.md"):
            src = skill_dir / fname
            if src.exists():
                shutil.copy2(src, backup_dir / fname)

    # 从目標版本恢复檔案
    restored_files = []
    for fname in ("SKILL.md", "memories.md", "persona.md"):
        src = version_dir / fname
        if src.exists():
            shutil.copy2(src, skill_dir / fname)
            restored_files.append(fname)

    # 更新 meta
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        meta["version"] = target_version + "_restored"
        meta["updated_at"] = datetime.now(timezone.utc).isoformat()
        meta["rollback_from"] = current_version
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"已回滚到 {target_version}，恢复檔案：{', '.join(restored_files)}")
    return True


def cleanup_old_versions(skill_dir: Path, max_versions: int = MAX_VERSIONS):
    """清理超出限制的舊版本"""
    versions_dir = skill_dir / "versions"
    if not versions_dir.exists():
        return

    version_dirs = sorted(
        [d for d in versions_dir.iterdir() if d.is_dir()],
        key=lambda d: d.stat().st_mtime,
    )

    to_delete = version_dirs[:-max_versions] if len(version_dirs) > max_versions else []

    for old_dir in to_delete:
        shutil.rmtree(old_dir)
        print(f"已清理舊版本：{old_dir.name}")


def main():
    parser = argparse.ArgumentParser(description="Skill 版本管理器")
    parser.add_argument("--action", required=True, choices=["list", "rollback", "cleanup"])
    parser.add_argument("--slug", required=True, help="群友 Persona slug")
    parser.add_argument("--version", help="目標版本號（rollback 時使用）")
    parser.add_argument(
        "--base-dir",
        default="./exes",
        help="群友 Persona Skill 根目錄（預設：./exes）",
    )

    args = parser.parse_args()
    base_dir = Path(args.base_dir).expanduser()
    skill_dir = base_dir / args.slug

    if not skill_dir.exists():
        print(f"错误：找不到 Skill 目錄 {skill_dir}", file=sys.stderr)
        sys.exit(1)

    if args.action == "list":
        versions = list_versions(skill_dir)
        if not versions:
            print(f"{args.slug} 暫無歷史版本")
        else:
            print(f"{args.slug} 的歷史版本：\n")
            for v in versions:
                print(f"  {v['version']}  存档時间: {v['archived_at']}  檔案: {', '.join(v['files'])}")

    elif args.action == "rollback":
        if not args.version:
            print("错误：rollback 操作需要 --version", file=sys.stderr)
            sys.exit(1)
        rollback(skill_dir, args.version)

    elif args.action == "cleanup":
        cleanup_old_versions(skill_dir)
        print("清理完成")


if __name__ == "__main__":
    main()
