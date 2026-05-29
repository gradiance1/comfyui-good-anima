#!/usr/bin/env python3
"""
Anima 随机图生成器。

用法:
    python random_generator.py --count 5
    python random_generator.py --artist-count 2
    python random_generator.py --safe sensitive
    python random_generator.py --json
"""

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, List

from artist_utils import load_random_artists
from prompt_builder import generate_prompt

HERE = Path(__file__).resolve().parent
TAG_POOLS_PATH = HERE / "tag_pools.json"
MAX_ARTIST_COUNT = 2


def load_tag_pools() -> Dict[str, Any]:
    """读取随机标签池。"""
    if not TAG_POOLS_PATH.exists():
        raise FileNotFoundError(f"缺少随机标签池: {TAG_POOLS_PATH}，请先运行 build_pools.py")
    with TAG_POOLS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_artist_count(value: int) -> int:
    """限制随机图画师数量，避免多画师风格漂移。"""
    if value < 1:
        raise ValueError("--artist-count 必须大于等于 1")
    if value > MAX_ARTIST_COUNT:
        raise ValueError(f"--artist-count 最大为 {MAX_ARTIST_COUNT}，随机图默认不使用长画师串")
    return value


def format_output(params: Dict[str, Any], index: int = 1) -> str:
    """格式化人类可读输出。"""
    lines = [
        f"=== 随机生成 #{index} ===",
        f"正向预览: {params['positive_prompt_preview']}",
        f"画师: {params['artist']}",
        f"人数: {params['count']}",
        f"外观: {params['appearance']}",
        f"标签: {params['tags']}",
        f"环境: {params['environment']}",
        f"自然语言: {params['nltags']}",
        f"比例: {params['aspect_ratio']}",
        f"尺寸: {params['width']}x{params['height']}",
        "",
        "--- CLI 工作流参数 ---",
        json.dumps(params, ensure_ascii=False, indent=2),
        "",
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Anima 随机图生成器")
    parser.add_argument("--count", "-n", type=int, default=1, help="生成几组参数（默认1）")
    parser.add_argument("--artist-count", "-a", type=int, default=1, help="每组随机画师数量（默认1，最大2）")
    parser.add_argument("--safe", "-s", default="safe", choices=["safe", "sensitive", "nsfw", "explicit"], help="安全标签级别")
    parser.add_argument("--json", "-j", action="store_true", help="仅输出JSON数组")
    parser.add_argument("--seed", type=int, default=None, help="随机种子（用于复现）")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        if args.count < 1:
            raise ValueError("--count 必须大于等于 1")
        artist_count = validate_artist_count(args.artist_count)
        if args.seed is not None:
            random.seed(args.seed)

        pools = load_tag_pools()
        artists_pool = load_random_artists(artist_count * args.count)
        results: List[Dict[str, Any]] = [
            generate_prompt(pools, artists_pool, artist_count=artist_count, safety=args.safe)
            for _ in range(args.count)
        ]

        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for i, params in enumerate(results, 1):
                print(format_output(params, index=i))
        return 0
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
