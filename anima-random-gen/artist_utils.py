#!/usr/bin/env python3
"""Anima 画师检索。

随机图的画师锚点以 danbooru-tags Rust CLI 为准，避免直接读取旧索引。
"""

from typing import List

from danbooru_utils import run_danbooru_tags

BLOCKED_ARTIST_HINTS = {
    "voice_actor", "voice actor", "company", "circle", "official", "studio",
    "sample", "wildcard", "copyright", "bot", "ai_generated", "anonymous",
}

def format_artist_for_anima(raw: str) -> str:
    """格式化 Anima 画师标签。"""
    value = str(raw or "").strip()
    if not value:
        return value
    if value.startswith("@"):
        value = value[1:]
    return "@" + value.replace("_", " ")


def is_trusted_artist(raw: str) -> bool:
    """过滤疑似非画师或弱风格锚点。"""
    value = str(raw or "").strip().lower()
    if not value.startswith("@"):
        return False
    normalized = value.replace("_", " ")
    return not any(hint in value or hint in normalized for hint in BLOCKED_ARTIST_HINTS)


def load_random_artists(count: int = 1) -> List[str]:
    """通过 Rust CLI 读取可直接用于 prompt 的随机画师。"""
    if count <= 0:
        return []

    artists: List[str] = []
    max_attempts = max(count * 3, 3)

    for _ in range(max_attempts):
        if len(artists) >= count:
            break
        payload = run_danbooru_tags(["--random", "5", "--for-prompt"])
        for artist in payload.get("random_artists_for_prompt", []):
            formatted = format_artist_for_anima(artist)
            if is_trusted_artist(formatted) and formatted not in artists:
                artists.append(formatted)
                break

    if not artists:
        raise ValueError("画师池为空，请检查 danbooru-tags Rust CLI 与 Anima CSV 索引")
    return artists
