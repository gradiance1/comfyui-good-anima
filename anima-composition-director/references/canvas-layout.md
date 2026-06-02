# 画布、布局与镜头参考

只在需要非默认画布、特殊镜头、空间落地、光影层次、遮挡、脸手可读性或关系可读性时读取。不要把本文件当通用构图教材。

## 画布选择

这些是当前 Anima base1.0 工作流的构图适配，不是预览版固定分辨率规则。

| 画布 | 使用场景 |
| --- | --- |
| `1536x1024` | 多人互动、横向动作、宽背景、左右空间关系 |
| `1024x1536` | 单人全身、竖图插画、手机壁纸、竖向姿势 |
| `1536x864` | 宽银幕、远景、横向环境叙事、桌面壁纸 |
| `1536x1152` | 室内中景、互动场景、人物占比较高且带环境 |
| `1152x1536` | 角色为主、轻环境叙事，比 2:3 更稳的竖图 |
| `1536x768` | 超宽场景、横向队列、压迫性风景；必须保护脸部可读性 |
| `1024x1024` | 头像、半身、中心主体、简单稳定构图 |
| `1536x1536` | 高细节中心构图、复杂服装、道具围绕、丰富背景 |

## 镜头语法

每组只选一个核心词，不要堆互斥镜头。

- 景别：`extreme close-up`、`close-up`、`medium close-up`、`upper body`、`medium shot`、`cowboy shot`、`full body`、`wide shot`、`establishing shot`。
- 角度：`eye-level`、`low front angle`、`high angle`、`side view`、`three-quarter view`、`over-shoulder view`、`top-down view`、`bird's-eye view`、`aerial view`、`pov`、`first-person view`。
- 透视：默认 `normal perspective`；只有动作、空间压迫、POV 需要时才用 `wide-angle`。
- 焦点：`shallow depth of field`、`deep focus`、`soft background blur`。

避免冲突：`pov/first-person view` 不写观众全身；`close-up` 不和 `full body` 同用；`from above` 不和 `from below` 同用；脸部是重点时不要 wide shot；没有明确要求不要用 fisheye。

## 景别用途

| 景别 | 适合 | 必须保护 |
| --- | --- | --- |
| `close-up` | 表情、脸部身份、观众连接 | 眼睛、脸型、简单背景 |
| `upper body` | 脸 + 手/道具/上半身服装 | 手部接触、肩线 |
| `medium shot` | 腰部以上动作、道具互动 | 手、腰线、道具轮廓 |
| `full body` | 服装、站姿、舞蹈、动作剪影 | 脚、四肢、外轮廓 |
| `wide shot` | 人物 + 场景、群体间距 | 主体分离、脸部仍可读 |
| `establishing shot` | 场地规模先于角色细节 | 一个焦点主体或地标 |

## 特殊镜头转换

- POV / 第一人称：前景可有观众的手、持物或身体边缘；目标角色在前方且脸可读；不要显示观众全身。
- 过肩：前景肩/头作为框架，目标脸部仍可读。
- 俯视 / 鸟瞰 / 航拍：地面、桌面、屋顶、道路、河流、阴影或人群要解释空间；不要期待细微表情。
- 透视夸张：最近的手、腿、道具或布料可更大，但关节连接、脸和身份锚点必须可信。
- 低角度：主体更高大；保护下巴和脸型。
- 插入镜头：只强调一个道具、手、徽章或物件细节。

视频术语要转成静帧：

- tracking shot → 主体偏置 + 背景引导线。
- push-in → 更近景别 + 更强脸部焦点。
- orbit → 三分之四视角 + 弧形背景线索。
- crane shot → 高角度 + 地面布局或人群图案。
- sky looking down at ground → 鸟瞰/航拍，优先地形和一个焦点地标。

## 局部聚焦与透视夸张

局部聚焦只选一个主焦点，不要同时强调脸、手、脚、服装细节和道具。

| 主焦点 | 镜头选择 | 保护点 |
| --- | --- | --- |
| 脸/眼睛 | close-up 或 upper body | 眼睛清晰，头发和前景不遮关键身份 |
| 手/道具 | medium shot 或 insert shot | 手指数量、握持关系、道具轮廓 |
| 服装/剪影 | cowboy shot 或 full body | 轮廓干净，脸后背景简化 |
| 足部/地面接触 | full body 或 low angle | 脚接触地面，避免漂浮 |
| 身体姿态 | full body 或 wide shot | 关节连接可信，动作方向有留白 |

透视夸张只在用户要求冲击感、POV、广角或近大远小时使用。最近的手、腿、道具可以变大，但 `nltags` 必须保护关节连接、脸部可读性和主体身份。

## 布局与焦点

先选一个主优先级，再加细节。身份与用户指定主体冲突时，优先保护身份。

| 优先级 | 构图选择 |
| --- | --- |
| 脸/身份 | close-up 或 upper body；简单背景；眼睛附近最高对比 |
| 服装/剪影 | full body 或 cowboy shot；轮廓干净；身体后方背景简化 |
| 道具/手部互动 | medium shot；手部接触可见；道具有负空间 |
| 角色关系 | two-shot、三角站位或过肩；视线和距离可读 |
| 环境尺度 | wide shot；主体在中景；前中后景有尺度参照 |
| 动作峰值 | 对角线动势；运动方向留白；道具剪影清楚 |

可选构图模式：中心、三分法、对角线、动作线、S 曲线、前中后景层次、负空间、对称、填满画面、框中框。只选一个主模式。

## 空间落地与密度

- 前景只用于增加深度或上下文，不遮脸、眼、手和身份徽记。
- 角色与环境都重要时，主体通常放中景。
- 背景解释地点、尺度或天气；脸后方保持安静。
- 站立/行走必须有落地线索：脚接触地面、路面、草地、接触阴影、投影、脚印或地面重叠。
- 非飞行、跳跃、游泳、失重时，不要让主体漂浮。
- 用道路、走廊、栏杆、河流、光束或人群方向引导视线。
- 多个视觉故事同时出现时，只保留一个主故事，其他降对比或放背景。

## 光影与明暗分离

把光写成可见几何：

- 主光方向：左、右、上、下、背后、窗边。
- 轮廓光只在需要分离剪影时使用。
- 补光只在阴影遮住脸或服装身份时使用。
- 背景光不能压过脸。
- 实际光源要符合场景：窗、灯、灯笼、霓虹、火、屏幕、月亮、路灯。
- 宽画幅或 2:1 画面必须明确保护脸部可读性。
- 后期词最多 1 个：bloom、vignette、lens flare、film grain、chromatic aberration。

光影选择：

- 高调：明亮、柔影、温和情绪、低威胁。
- 低调：暗场景、小面积脸/手受光、紧张或秘密。
- 分割光：脸/身体一侧亮一侧暗；眼睛仍要可读。
- 逆光剪影：先保轮廓；身份细节不重要时才用。

## 表情、视线与遮挡

- 表情必须匹配动作：用力、冷静、惊讶、恐惧、喜悦、紧张、害羞。
- 视线决定关系：看观众、看另一个角色、看道具、看画外。
- 睡眠、昏迷、背身或专注别处时，不写 `looking at viewer`。
- 多角色场景说明谁看谁或看什么。
- 近景承载细微眼神；远景需要更大的身体姿态。
- 脸、眼、手、身份徽记默认清晰；只有用户要求遮掩时才遮。
- 头发、烟、袖子、前景物先遮非关键区域。

## nltags 示例

```text
Keep her eyes visible while the sleeve covers only her shoulder.
Make her look toward the umbrella, not directly at the viewer.
Keep the hand and sword grip clear in front of her body.
Use soft window light from the left.
Add a thin rim light around the silhouette.
Keep the face sharp; blur the background softly.
Keep foreground objects out of the face area.
Keep the strongest contrast around the face and upper body.
Place the subject slightly right of center, with the corridor receding to the left.
Use a first-person view with the viewer's hands in the foreground.
Frame the target character in front, keeping their face readable.
Use perspective distortion deliberately; keep joints, hands, face, and body connection believable.
```
