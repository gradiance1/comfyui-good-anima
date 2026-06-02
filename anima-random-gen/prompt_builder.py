#!/usr/bin/env python3
"""Anima 随机图 prompt 组装。"""

import random
import json
import math
import re
from typing import Any, Dict, List, Optional

from danbooru_utils import run_danbooru_tags
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
NEGATIVE_PROMPT = "worst quality, low quality, score_1, score_2, score_3, blurry, bad anatomy, bad hands, bad feet, extra fingers, missing fingers, distorted face, text, watermark, logo"
DEFAULT_CANVAS = {"aspect_ratio": "2:3", "width": 1024, "height": 1536, "reason": "random single-character vertical composition"}
WORKFLOW_SEED_MAX = 2**32 - 1


def format_prompt_tag(raw: str) -> str:
    """转换为 Anima prompt 常用空格 tag。"""
    return str(raw or "").strip().replace("_", " ")


def first_confirmed_prompt_tag(result: Dict[str, Any]) -> Optional[str]:
    """取第一个已确认 prompt_tag；查不到就交给下游 nltags 处理。"""
    for items in result.get("confirmed_tags", {}).values():
        if items:
            item = items[0]
            return item.get("prompt_tag") or format_prompt_tag(item.get("tag", ""))
    return None


def validate_random_tags(groups: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """用 danbooru-tags Rust CLI 批量确认随机抽出的 hard anchors。"""
    queries: List[Dict[str, Any]] = []

    for group, tags in groups.items():
        for index, tag in enumerate(tags):
            query_id = f"{group}_{index}"
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
        prompt_tag = first_confirmed_prompt_tag(result)
        if prompt_tag:
            validated[group].append(prompt_tag)
    return validated


def random_artists(artists_pool: List[str], count: int = 0) -> str:
    """随机抽取 1 个画师；默认不强加画师。"""
    if count <= 0:
        return ""
    if not artists_pool:
        raise ValueError("画师池为空，无法生成随机图")
    count = min(count, 1, len(artists_pool))
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
        parts.get("character", ""),
        parts.get("series", ""),
        parts.get("artist", ""),
        parts.get("style", ""),
        parts["appearance"],
        parts["tags"],
        parts["environment"],
        parts["nltags"],
    ]
    return ", ".join(part for part in ordered if part)


def split_nltags_sentences(text: str) -> List[str]:
    """把随机叙事文本拆成下游可直接合并的控制句。"""
    return [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", text or "") if sentence.strip()]


def aspect_ratio_for(width: int, height: int) -> str:
    """把画布尺寸转成简短比例。"""
    divisor = math.gcd(width, height)
    return f"{width // divisor}:{height // divisor}"


def generate_prompt(
    pools: Dict[str, Any],
    artists_pool: List[str],
    artist_count: int = 0,
    safety: str = "nsfw",
    width: int = DEFAULT_CANVAS["width"],
    height: int = DEFAULT_CANVAS["height"],
) -> Dict[str, Any]:
    """生成一组给 comfyui-anima-master 复核的语义交接参数。"""
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
    narrative = pick_narrative(pose, scene, lighting, expressions=expr_tags)

    checked = validate_random_tags({
        "appearance": appearance_tags,
        "clothing": clothing_tags,
        "accessory": acc_tags,
        "expression": expr_tags,
        "pose": [pose],
        "scene": [scene],
        "lighting": [lighting],
    })
    appearance = ", ".join(checked["appearance"])
    tags = ", ".join(limit_tags(checked["clothing"] + checked["accessory"] + checked["expression"], len(body_tags)))
    environment = ", ".join(limit_tags(checked["pose"] + checked["scene"] + checked["lighting"], 4))

    artist = random_artists(artists_pool, count=artist_count)
    quality = build_quality_prefix(safety)
    workflow_seed = random.randint(0, WORKFLOW_SEED_MAX)

    params = {
        "aspect_ratio": aspect_ratio_for(width, height),
        "width": width,
        "height": height,
        "quality_meta_year_safe": quality,
        "count": count_tag,
        "artist": artist,
        "appearance": appearance,
        "tags": tags,
        "environment": environment,
        "nltags": narrative,
        "nltags_sentences": split_nltags_sentences(narrative),
        "canvas_reason": DEFAULT_CANVAS["reason"] if (width, height) == (DEFAULT_CANVAS["width"], DEFAULT_CANVAS["height"]) else "user-specified random canvas",
        "neg": NEGATIVE_PROMPT,
        "seed": workflow_seed,
        "steps": 30,
        "batch_size": 1,
        "rtx_vsr_quality": "ULTRA",
    }
    params["positive_prompt_preview"] = build_positive_preview(params)
    return params
