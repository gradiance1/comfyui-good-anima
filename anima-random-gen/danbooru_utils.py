#!/usr/bin/env python3
"""Shared danbooru-tags CLI helpers."""

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List

HERE = Path(__file__).resolve().parent


def is_danbooru_tags_dir(path: Path) -> bool:
    return (
        (path / "SKILL.md").exists()
        and ((path / "tags_index.sqlite").exists() or (path / "anima-1.0.csv").exists())
    )


def resolve_danbooru_tags_dir() -> Path:
    env_dir = os.environ.get("DANBOORU_TAGS_DIR")
    if env_dir:
        return Path(env_dir).expanduser().resolve()

    for base in (HERE, *HERE.parents):
        candidates = [
            base / "danbooru-tags",
            base / "skills" / "danbooru-tags",
        ]
        try:
            candidates.extend(child / "danbooru-tags" for child in base.iterdir() if child.is_dir())
        except OSError:
            pass

        for candidate in candidates:
            if is_danbooru_tags_dir(candidate):
                return candidate.resolve()

    raise FileNotFoundError("缺少 danbooru-tags skill；请设置 DANBOORU_TAGS_DIR")


DANBOORU_TAGS_DIR = resolve_danbooru_tags_dir()
CLI_NAME = "danbooru-tags.exe" if os.name == "nt" else "danbooru-tags"
CLI_PATH = DANBOORU_TAGS_DIR / "bin" / CLI_NAME


def run_danbooru_tags(args: List[str]) -> Dict[str, Any]:
    """执行 danbooru-tags Rust CLI 并返回 JSON。"""
    if not CLI_PATH.exists():
        raise FileNotFoundError(f"缺少 danbooru-tags CLI: {CLI_PATH}")

    command = [str(CLI_PATH), *args, "--json", "--compact"]
    result = subprocess.run(
        command,
        cwd=str(DANBOORU_TAGS_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"danbooru-tags 执行失败: {detail}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("danbooru-tags 输出不是有效 JSON") from exc
