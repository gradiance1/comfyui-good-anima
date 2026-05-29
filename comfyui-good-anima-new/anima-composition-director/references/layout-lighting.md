# Layout 与 Lighting 细则

> ⚠️ 核心规则已回流至 SKILL.md。本文件仅提供扩展细节与边界情况。如内容与 SKILL.md 冲突，以 SKILL.md 为准。

只在需要构图模式、光影、景深、主体层级或复杂场景取舍时读取本文件。

## Layout modes

| Mode                                   | Use when               | Priority                                                      |
| -------------------------------------- | ---------------------- | ------------------------------------------------------------- |
| Character illustration                 | 单人或角色展示         | readable face, outfit silhouette, clean background separation |
| Key visual / poster                    | 主视觉、宣传图、封面感 | strong focal point, silhouette, controlled negative space     |
| Event CG / visual novel CG             | 剧情事件图、角色互动   | relationship, gaze, hands, props, motivated light             |
| Manga single panel                     | 单格漫画感、动作峰值   | peak action, diagonal flow, expression and hand readability   |
| Cinematic still                        | 电影定格、强镜头感     | shot distance, camera angle, depth layers                     |
| Concept art / environment illustration | 场景设定、环境叙事     | scale, foreground/midground/background                        |
| Card / splash art                      | 卡面、必杀技、强冲击图 | dynamic pose, prop silhouette, effects not over face          |
| Character sheet                        | 设定展示、服装细节     | neutral pose, clean lighting, readable details                |

## Composition patterns

Use one clear pattern:

- Center: stable portrait, icon, square image, character focus.
- Rule of thirds: character plus readable environment.
- Diagonal: action, weapons, movement, falling, chase.
- Layered depth: foreground object, midground subject, background scene.
- Negative space: title area, sky, empty corridor, breathing room.
- Symmetry: ritual, shrine, throne, formal scene, stillness.

State subject placement and background direction:

```text
Place the subject slightly right of center, with the corridor receding to the left.
```

## Visual quality rules

- Establish one focal point first; secondary props and background must support it.
- Use either negative space or controlled density, not both.
- Use overlap to show depth, but keep overlaps away from the face and hands.
- Put the most readable silhouette against the simplest background area.
- If the prompt has many tags, reduce background complexity before reducing identity tags.
- Prefer clear value separation: bright subject on darker background, or dark subject on bright background.
- Use edge control: sharp face and hands; softer hair ends, clothing edges, and background.
- Use one dominant palette plus one accent color; avoid naming many unrelated colors.
- When clothing is complex, simplify the background and use a medium shot or full body with clean silhouette.

## Lighting and depth

Define light as visible geometry:

- Key light direction: left / right / above / below / behind / window side.
- Rim light only when it helps silhouette separation.
- Fill light only when shadows hide the face or outfit identity.
- Background light should not overpower the face.
- Use background blur when scene detail competes with identity.
- For 2:1 or wide shots, explicitly protect face readability.
- Pick one post-process word at most: bloom, vignette, lens flare, film grain, or chromatic aberration.

Useful controls:

```text
Use soft window light from the left.
Add a thin rim light around the silhouette.
Keep the face sharp; blur the background softly.
Keep foreground objects out of the face area.
Keep the strongest contrast around the face and upper body.
```
