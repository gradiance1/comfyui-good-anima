#!/usr/bin/env python3
"""随机图英文自然语言片段。"""

import random
from typing import Dict, List

POSE_NARRATIVES: Dict[str, List[str]] = {
    "sitting": [
        "She sits with a relaxed posture.",
        "She is seated with a balanced pose.",
    ],
    "standing": [
        "She stands with a confident posture.",
        "She is standing with a readable silhouette.",
    ],
    "lying": [
        "She lies in a relaxed pose.",
        "She is lying down comfortably.",
    ],
    "looking_at_viewer": [
        "She looks directly at the viewer.",
        "Her gaze meets the viewer clearly.",
    ],
    "full_body": [
        "Show her full body clearly.",
    ],
    "upper_body": [
        "Use upper-body framing.",
    ],
}

SCENE_NARRATIVES: Dict[str, List[str]] = {
    "beach": ["Place her on a beach with soft waves in the background."],
    "water": ["Place calm water around her in the background."],
    "bedroom": ["Place her inside a cozy bedroom."],
    "classroom": ["Place her inside a quiet classroom."],
    "cafe": ["Place her inside a relaxed cafe setting."],
    "forest": ["Place tall trees behind her."],
    "street": ["Place her on a casual urban street."],
    "rooftop": ["Place her on a rooftop."],
    "night": ["Set the scene at night."],
    "sunset": ["Use warm sunset colors across the scene."],
    "simple_background": ["The clean background keeps attention on the character."],
    "white_background": ["The white background creates a minimal illustration-like presentation."],
}

LIGHT_NARRATIVES: Dict[str, List[str]] = {
    "sunlight": ["Use warm sunlight on the subject."],
    "bokeh": ["Use soft bokeh behind the subject."],
    "lens_flare": ["Add a subtle lens flare away from the face."],
    "dappled_sunlight": ["Use dappled sunlight across the scene."],
    "shadow": ["Use soft shadows to add depth."],
}

EXPRESSION_NARRATIVES: Dict[str, List[str]] = {
    "embarrassed": ["Give her an embarrassed reaction."],
    "grin": ["Give her a playful grin."],
    "expressionless": ["Keep her expression quiet and unreadable."],
    "serious": ["Give her a serious expression."],
    "surprised": ["Give her a surprised expression."],
    "pout": ["Give her a mild pout."],
    "sleepy": ["Give her a sleepy expression."],
    "tears": ["Her tears make the scene emotionally fragile."],
}

def pick_narrative(pose: str, scene: str, lighting: str, expressions: List[str] | None = None) -> str:
    """按 pose → scene → lighting 组合英文描述，避免单句互相冲突。"""
    sentences = []
    expression_sentence = ""
    for expression in expressions or []:
        choices = EXPRESSION_NARRATIVES.get(expression, [])
        if choices:
            expression_sentence = random.choice(choices)
            break
    for mapping, key in ((POSE_NARRATIVES, pose), (SCENE_NARRATIVES, scene), (LIGHT_NARRATIVES, lighting)):
        choices = mapping.get(key, [])
        if choices:
            sentences.append(random.choice(choices))
    if expression_sentence:
        sentences = [
            sentence
            for sentence in sentences
            if not any(word in sentence.lower() for word in ("calm", "relaxed", "composed", "restful", "quiet"))
        ]
        sentences.insert(0, expression_sentence)
    return " ".join(sentences[:3])
