#!/usr/bin/env python3
"""
从 danbooru-tags Rust CLI 批量校验本 skill 的静态随机标签池。

用法:
    python build_pools.py
"""

import json
from pathlib import Path

from danbooru_utils import CLI_PATH, run_danbooru_tags

HERE = Path(__file__).resolve().parent
OUTPUT_PATH = HERE / "tag_pools.json"


def validate_pool_tags(pools, checks):
    queries = []
    lookup = {}
    for key, group in checks.items():
        for index, tag in enumerate(pools.get(key, [])):
            query_id = f"{key}_{index}"
            lookup[query_id] = (key, tag)
            queries.append({
                "id": query_id,
                "group": group,
                "keyword": tag.replace("_", " "),
                "limit": 1,
            })

    payload = run_danbooru_tags([
        "--batch-workers", "8",
        "--batch-json", json.dumps({"queries": queries}, ensure_ascii=False, separators=(",", ":")),
        "--for-prompt",
    ])

    valid = {key: [] for key in checks}
    for query_id, result in payload.get("results", {}).items():
        key, tag = lookup[query_id]
        if result.get("found"):
            valid[key].append(tag)
    return valid


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
        "scene": "scene",
        "lighting": "lighting",
        "character_features": "appearance",
    }

    validated = validate_pool_tags(pools, checks)
    for key in checks:
        valid = validated.get(key, [])
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
