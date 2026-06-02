#!/usr/bin/env python3
"""Anima 随机标签采样。"""

import random
from typing import Any, Dict, List

REQUIRED_POOLS = {
    "hair_color", "hair_style", "eye_color", "expression", "clothing_onepiece",
    "clothing_top", "clothing_bottom", "swimwear", "accessories", "pose",
    "scene", "lighting", "character_features",
}

SWIMWEAR_ROLL_MAX = 0.15
ONEPIECE_ROLL_MAX = 0.45


def validate_pools(pools: Dict[str, Any]) -> None:
    """确认随机池完整且非空。"""
    missing = sorted(name for name in REQUIRED_POOLS if not pools.get(name))
    if missing:
        raise ValueError("随机标签池缺失或为空: " + ", ".join(missing))


def limit_tags(tags: List[str], max_items: int) -> List[str]:
    """按顺序去重并限制标签数量。"""
    result: List[str] = []
    seen = set()
    for tag in tags:
        key = tag.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(tag)
        if len(result) >= max_items:
            break
    return result


def random_hair(pools: Dict[str, Any]) -> List[str]:
    color = random.choice(pools["hair_color"])
    style = random.sample(pools["hair_style"], k=random.randint(1, 2))
    return [color] + style


def random_eyes(pools: Dict[str, Any]) -> List[str]:
    eyes = random.choice(pools["eye_color"])
    if eyes == "heterochromia" or random.random() < 0.5:
        return [eyes]
    second = random.choice(pools["eye_color"])
    if second == eyes or second == "heterochromia":
        return [eyes]
    return [eyes, second]


def random_expression(pools: Dict[str, Any]) -> List[str]:
    """随机1-2个表情，自动排除互斥组（张嘴/闭嘴、😛/严肃/无表情/困、眼泪/笑/微笑/吐舌）。"""
    mutex_groups = [
        {"open_mouth", "closed_mouth"},
        {":d", "serious", "expressionless", "sleepy"},
        {"tears", "grin", "light_smile", "tongue_out"},
    ]
    candidates = pools["expression"][:]
    chosen: List[str] = []

    for _ in range(random.randint(1, 2)):
        if not candidates:
            break
        expr = random.choice(candidates)
        chosen.append(expr)
        for group in mutex_groups:
            group_norm = {g.lower() for g in group}
            if expr.lower() in group_norm:
                candidates = [c for c in candidates if c.lower() not in group_norm]
                break
        candidates = [c for c in candidates if c.lower() != expr.lower()]
    return chosen


def random_clothing(pools: Dict[str, Any]) -> List[str]:
    """随机服装：泳装15% / 连衣裙45% / 上下分体40%。"""
    roll = random.random()
    if roll < SWIMWEAR_ROLL_MAX:
        return [random.choice(pools["swimwear"])]
    if roll < ONEPIECE_ROLL_MAX:
        return [random.choice(pools["clothing_onepiece"])]
    return [random.choice(pools["clothing_top"]), random.choice(pools["clothing_bottom"])]


def random_accessories(pools: Dict[str, Any]) -> List[str]:
    k = random.randint(0, min(3, len(pools["accessories"])))
    return random.sample(pools["accessories"], k=k) if k else []


def random_pose(pools: Dict[str, Any]) -> str:
    return random.choice(pools["pose"])


def random_scene(pools: Dict[str, Any], clothing_tags: List[str]) -> str:
    """随机场景；穿泳装时偏好海滩/水/户外/天空。"""
    scenes = pools["scene"][:]
    if any("swimsuit" in tag or "bikini" in tag for tag in clothing_tags):
        preferred = [s for s in scenes if s in {"beach", "water", "outdoor", "blue_sky", "sky"}]
        if preferred:
            return random.choice(preferred)
    return random.choice(scenes)


def random_lighting(pools: Dict[str, Any]) -> str:
    return random.choice(pools["lighting"])


def random_character_features(pools: Dict[str, Any]) -> List[str]:
    k = random.randint(0, min(2, len(pools["character_features"])))
    return random.sample(pools["character_features"], k=k) if k else []
