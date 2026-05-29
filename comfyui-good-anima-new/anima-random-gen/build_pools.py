#!/usr/bin/env python3
"""
从 danbooru-tags Rust CLI 批量校验本 skill 的静态随机标签池。

用法:
    python build_pools.py
"""

import json
import os
import subprocess
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(HERE, "tag_pools.json")
DANBOORU_DIR = Path(HERE).resolve().parent / "danbooru-tags"
CLI_PATH = DANBOORU_DIR / "bin" / "danbooru-tags.exe"


def run_query(group: str, keyword: str) -> bool:
    command = [
        str(CLI_PATH),
        "--group", group,
        "--keyword", keyword.replace("_", " "),
        "--limit", "1",
        "--for-prompt",
        "--json",
        "--compact",
    ]
    result = subprocess.run(
        command,
        cwd=str(DANBOORU_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        return False
    try:
        return bool(json.loads(result.stdout).get("found"))
    except json.JSONDecodeError:
        return False


def build_pools():
    if not CLI_PATH.exists():
        raise FileNotFoundError(f"缺少 danbooru-tags CLI: {CLI_PATH}")

    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        pools = json.load(f)

    checks = {
        "hair_color": "appearance",
        "hair_style": "appearance",
        "eye_color": "appearance",
        "expression": "expression",
        "clothing_onepiece": "clothing",
        "clothing_top": "clothing",
        "clothing_bottom": "clothing",
        "swimwear": "clothing",
        "accessories": "accessory",
        "pose": "pose",
        "composition": "scene",
        "lighting": "lighting",
        "character_features": "appearance",
    }

    for key, group in checks.items():
        valid = [tag for tag in pools.get(key, []) if run_query(group, tag)]
        if not valid:
            raise ValueError(f"标签池校验后为空: {key}")
        pools[key] = valid

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(pools, f, ensure_ascii=False, indent=2)

    print(f"Validated {OUTPUT_PATH}")
    for k, v in pools.items():
        if isinstance(v, list):
            print(f"  {k}: {len(v)} tags")


if __name__ == "__main__":
    build_pools()
