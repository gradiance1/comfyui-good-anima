#!/usr/bin/env python3
"""随机图英文自然语言片段。"""

import random
from typing import Dict, List

POSE_NARRATIVES: Dict[str, List[str]] = {
    "sitting": [
        "She sits calmly with a relaxed posture, looking naturally composed.",
        "She is seated gracefully, her pose quiet and balanced.",
    ],
    "standing": [
        "She stands with a confident posture, framed clearly in the composition.",
        "She is standing naturally, her silhouette easy to read.",
    ],
    "lying": [
        "She lies comfortably with a soft, restful expression.",
        "She is lying down in a relaxed pose, creating a gentle atmosphere.",
    ],
    "looking_at_viewer": [
        "She looks directly at the viewer with a clear focal presence.",
        "Her gaze meets the viewer, making the image feel immediate and expressive.",
    ],
    "full_body": [
        "The composition shows her full body with a clear readable silhouette.",
    ],
    "upper_body": [
        "The upper-body framing emphasizes her expression and outfit details.",
    ],
}

SCENE_NARRATIVES: Dict[str, List[str]] = {
    "beach": ["The scene is set on a bright beach with soft waves in the background."],
    "water": ["Calm water reflects the light around her, adding a quiet shimmer."],
    "bedroom": ["The room feels cozy, with soft interior light and warm details."],
    "classroom": ["A quiet classroom surrounds her with gentle afternoon light."],
    "cafe": ["The cafe setting adds warm ambient light and a relaxed daily-life mood."],
    "forest": ["Tall trees and natural greenery create a peaceful outdoor backdrop."],
    "street": ["The street background gives the image a casual urban atmosphere."],
    "rooftop": ["The rooftop setting opens toward the skyline and a wide sky."],
    "night": ["The night setting adds a calm, slightly cinematic mood."],
    "sunset": ["The sunset colors wrap the scene in warm orange light."],
    "simple_background": ["The clean background keeps attention on the character."],
    "white_background": ["The white background creates a minimal illustration-like presentation."],
}

LIGHT_NARRATIVES: Dict[str, List[str]] = {
    "sunlight": ["Warm sunlight softly defines the shapes and colors."],
    "bokeh": ["Soft bokeh separates her from the background with a dreamy depth."],
    "lens_flare": ["A subtle lens flare adds a photographic sparkle without overpowering the subject."],
    "dappled_sunlight": ["Dappled sunlight creates gentle patches of light and shadow."],
    "shadow": ["Soft shadows add depth while keeping the character readable."],
}


def pick_narrative(pose: str, scene: str, lighting: str) -> str:
    """按 pose → scene → lighting 组合英文描述，避免单句互相冲突。"""
    sentences = []
    for mapping, key in ((POSE_NARRATIVES, pose), (SCENE_NARRATIVES, scene), (LIGHT_NARRATIVES, lighting)):
        choices = mapping.get(key, [])
        if choices:
            sentences.append(random.choice(choices))
    return " ".join(sentences[:3])
