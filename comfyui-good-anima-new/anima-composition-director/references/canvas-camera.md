# Canvas 与 Camera 细则

> ⚠️ 核心规则已回流至 SKILL.md。本文件仅提供扩展细节与边界情况。如内容与 SKILL.md 冲突，以 SKILL.md 为准。

只在需要更精细的画布选择、镜头距离、镜头角度或参考图构图迁移时读取本文件。

## Canvas fit

| Canvas          | Use when                                           |
| --------------- | -------------------------------------------------- |
| `1536x1024` 3:2 | 多人互动、横向动作、宽景背景、左右空间关系         |
| `1024x1536` 2:3 | 单人全身、立绘、手机壁纸、纵向姿态                 |
| `1536x864` 16:9 | 电影感宽银幕、远景、横向环境叙事、桌面壁纸预览     |
| `1536x1152` 4:3 | 室内中景、互动场景、人物占比高但仍保留环境         |
| `1152x1536` 3:4 | 角色为主、少量环境叙事、比 2:3 更稳的竖图          |
| `1536x768` 2:1  | 超宽场景、横向队列、压迫感风景；必须保护脸部可读性 |
| `1024x1024` 1:1 | 头像、半身、中心主体、简单稳定构图                 |
| `1536x1536` 1:1 | 高信息量中心构图、复杂服装、道具环绕、丰富背景     |

## Camera grammar

Pick one value from each row unless the user explicitly needs a special shot:

- Distance: `close-up`, `upper body`, `cowboy shot`, `full body`, `wide shot`.
- Angle: `eye-level`, `low front angle`, `high angle`, `side view`, `three-quarter view`, `over-shoulder view`, `top-down view`.
- Lens feel: `normal perspective` by default; use `wide-angle` only for strong space or action.
- Focus: `shallow depth of field`, `deep focus`, `rack focus look`, or `soft background blur`.

Avoid contradictions:

- no `close-up` with `full body`
- no `from above` with `from below`
- no wide shot if the face must dominate
- avoid fisheye unless requested

## Video term conversion

- `tracking shot` -> subject offset with background leading lines.
- `push-in` -> close framing and stronger face emphasis.
- `orbit` -> three-quarter view with curved background cues.
- Describe peak pose and motion direction, not a sequence of events.
