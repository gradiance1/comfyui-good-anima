#!/usr/bin/env python3
"""Anima 随机图 prompt 组装。"""

import random
import json
from typing import Any, Dict, List

from artist_utils import run_danbooru_tags
from narratives import pick_narrative
from sampler import (
    limit_tags,
    random_accessories,
    random_character_features,
    random_clothing,
    random_expression,
    random_eyes,
    random_hair,
    random_lighting,
    random_pose,
    random_scene,
    validate_pools,
)

QUALITY_TAGS = ["masterpiece", "very aesthetic", "best quality", "score_9", "score_8", "highres", "absurdres", "newest", "year 2025"]
NEGATIVE_PROMPT = "worst quality, low quality, score_1, score_2, score_3, blurry, bad anatomy, bad hands, bad feet, extra fingers, missing fingers, distorted face, text, watermark, logo, artist name"


def format_prompt_tag(raw: str) -> str:
    """转换为 Anima prompt 常用空格 tag。"""
    return str(raw or "").strip().replace("_", " ")


def fmt(tags: List[str]) -> str:
    """将 tag 列表转成 Anima prompt 片段。"""
    return ", ".join(format_prompt_tag(t) for t in tags if t)


def first_confirmed_prompt_tag(result: Dict[str, Any], fallback: str) -> str:
    """取第一个已确认 prompt_tag，查不到时回退到原 tag 格式。"""
    for items in result.get("confirmed_tags", {}).values():
        if items:
            return items[0].get("prompt_tag") or format_prompt_tag(fallback)
    return format_prompt_tag(fallback)


def validate_random_tags(groups: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """用 danbooru-tags Rust CLI 批量确认随机抽出的 hard anchors。"""
    queries: List[Dict[str, Any]] = []
    lookup: Dict[str, str] = {}

    for group, tags in groups.items():
        for index, tag in enumerate(tags):
            query_id = f"{group}_{index}"
            lookup[query_id] = tag
            queries.append({
                "id": query_id,
                "group": group,
                "keyword": format_prompt_tag(tag),
                "limit": 1,
            })

    if not queries:
        return {group: [] for group in groups}

    payload = run_danbooru_tags([
        "--batch-workers", "8",
        "--batch-json", json.dumps({"queries": queries}, ensure_ascii=False, separators=(",", ":")),
        "--for-prompt",
    ])

    validated: Dict[str, List[str]] = {group: [] for group in groups}
    for query_id, result in payload.get("results", {}).items():
        group = query_id.rsplit("_", 1)[0]
        validated[group].append(first_confirmed_prompt_tag(result, lookup[query_id]))
    return validated


def random_artists(artists_pool: List[str], count: int = 1) -> str:
    """随机抽取不重复画师，默认用于稳定单画师锚定。"""
    if not artists_pool:
        raise ValueError("画师池为空，无法生成随机图")
    count = min(max(count, 1), 2, len(artists_pool))
    chosen = random.sample(artists_pool, k=count)
    return ", ".join(a for a in chosen)


def build_quality_prefix(safety: str) -> str:
    """字段化组装质量、年份与安全标签。"""
    return ", ".join(QUALITY_TAGS + [safety])


def build_positive_preview(parts: Dict[str, str]) -> str:
    """按 Anima 顺序组装最终正向提示词预览。"""
    ordered = [
        parts["quality_meta_year_safe"],
        parts["count"],
        parts["artist"],
        parts["appearance"],
        parts["tags"],
        parts["environment"],
        parts["nltags"],
    ]
    return ", ".join(part for part in ordered if part)


def generate_prompt(
    pools: Dict[str, Any],
    artists_pool: List[str],
    artist_count: int = 1,
    safety: str = "safe",
) -> Dict[str, Any]:
    """生成一组完整的 Anima 生图参数。"""
    validate_pools(pools)

    count_tag = "1girl"
    hair_tags = random_hair(pools)
    eye_tags = random_eyes(pools)
    feature_tags = random_character_features(pools)
    appearance_tags = limit_tags(hair_tags + eye_tags + feature_tags, 4)

    expr_tags = random_expression(pools)
    clothing_tags = random_clothing(pools)
    acc_tags = random_accessories(pools)
    body_tags = limit_tags(clothing_tags + acc_tags + expr_tags, 6)

    pose = random_pose(pools)
    scene = random_scene(pools, clothing_tags)
    lighting = random_lighting(pools)
    env_tags = limit_tags([pose, scene, lighting], 4)
    narrative = pick_narrative(pose, scene, lighting)

    checked = validate_random_tags({
        "appearance": appearance_tags,
        "clothing": body_tags,
        "scene": env_tags,
    })
    appearance = ", ".join(checked["appearance"])
    tags = ", ".join(checked["clothing"])
    environment = ", ".join(checked["scene"])

    artist = random_artists(artists_pool, count=artist_count)
    quality = build_quality_prefix(safety)

    params = {
        "aspect_ratio": "2:3",
        "width": 1024,
        "height": 1536,
        "quality_meta_year_safe": quality,
        "count": count_tag,
        "artist": artist,
        "appearance": appearance,
        "tags": tags,
        "environment": environment,
        "nltags": narrative,
        "neg": NEGATIVE_PROMPT,
        "steps": 30,
        "sampler_name": "dpmpp_2m_sde_gpu",
        "scheduler": "beta57",
        "cfg": 4.5,
        "batch_size": 1,
        "rtx_vsr_quality": "ULTRA",
        "filename_prefix": "AnimaTool_random",
    }
    params["positive_prompt_preview"] = build_positive_preview(params)
    return params
