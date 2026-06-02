---
name: anima-composition-director
description: |
  当 Anima 生图需要把模糊意图解析成清楚视觉计划时加载：场景容器补全、关系/手势/叙事节拍、多人站位、非默认画布/镜头、参考图构图迁移、大场景、强光影、空间深度、脸部可读性保护。
  不用于已经说明主体、风格和场景的简单单人 prompt。
---

# Anima 构图导演

本 skill 把模糊用户意图变成清楚视觉计划，并在需要时给出 Anima 容易出错的边界条件和可交接字段。

## 意图解析

拿到用户需求后，先判断它是否已经足够清楚；如果仍然模糊，就把它拆成三层，再落回构图。意图层的目标是把模糊需求变成清楚需求，不是替用户强加固定设定。不要字面翻译用户语句：用户说“花海”不等于只写 `flower field`；用户没说“手势”也不等于人物一定要站着。意图层负责展开，规则层负责收缩；不要在这里写 Anima 崩点案例。

### 第一层：确认

先提取用户已经明确的部分，暂不延伸：

- 主体是谁：命名角色、原创角色、人数、CP/组合。
- 场景容器是什么：花海、教室、街道、神社、抽象空间等。
- 关系是什么：CP、对峙、守护、擦肩、回避、独处。
- 风格锚点是什么：画师、年代、光影、材质、用途。
- 用户明确拒绝什么：不加角色、不改场景、不写文字、不要某风格。

场景容器一旦锁定不可改写。用户说花海就保留花海，不偷换成花田、花园或室内花房。

### 第二层：补全

从场景容器的物理属性反推画面成立所需上下文。补全不是猜用户偏好，也不是套默认模板，而是避免画面空洞、静止、字面化。

下表是思考样例，不是默认填充项。优先选择当前画面确实需要的内容。

| 已知 | 可推导的画面条件 |
| --- | --- |
| 花海 | 春季或初夏，户外空气，花瓣、花茎、自然地面层次 |
| 花海 + 户外 | 微风或晴朗光线；否则花瓣不动，画面像静物 |
| 风 | 发丝微扬、袖口/裙摆轻动、花瓣落在衣褶或道具上 |
| 教室窗边 | 窗光、窗帘、桌椅或黑板作为空间锚点 |
| 雨夜街道 | 湿地反光、伞、路灯/霓虹、水痕、衣料湿润 |
| 神社夜景 | 石阶、鸟居、灯笼/月光、御札或袖摆的轻微动作 |
| 两人同框 | 位置、距离、视线、手势或道具通常需要帮助表达关系 |

用户已经指定天气、时间、季节、服装状态或镜头时，保留用户版本，不再自动推导同类项。

### 第三层：创作组合

在确认和补全之后，收敛出一个能让需求更清楚的画面瞬间。尽量选择当前最合理方向，不穷举，也不把示例当作固定默认。

- 故事节拍：触碰前、触碰刹那、刚离开、回头一瞬、递出未接。选择最贴合用户关系的一种；“触碰前一秒”只是高张力关系的可选解，不是默认规则。
- 手势叙事：主动方伸手、递出、前倾、掌心向上；被动方后退、侧身、手指缩回、用伞/书/怀表隔开距离。
- 概念锚点：用一个可见物件承载关系，例如花瓣落到对方道具上、影子跨过边界、共用道具被花缠绕。
- 视线关系：看向对方、看向对方手中物、避开视线、看向画外。按关系温度选择，不把对视当固定默认。

隐喻尽量落成可见物件和动作，不写解释性说明。若某个构图手法会改写用户给定的场景、关系或象征物，保留用户意图，换一种表达方式。若用户需求已经足够清楚，只做最小补全。

### 意图 brief 输出

输出给 `comfyui-animatool` 的 brief 保持短，不向用户复述完整推理：

```json
{
  "intent_summary": "what the image should express",
  "locked": {
    "subject": "characters or subject",
    "scene_container": "fixed container",
    "relationship": "relationship or mood",
    "style_anchor": "artist / era / lighting / material"
  },
  "inferred_context": [
    "only context required for the scene to work"
  ],
  "creative_anchor": {
    "story_moment": "one selected moment",
    "gesture": "one visible relationship action",
    "object": "one visible symbolic prop if useful",
    "gaze": "one gaze relation"
  },
  "nltags_sentences": [
    "short English visual control sentence"
  ]
}
```

## 何时使用

使用：

- 多角色同框，需要位置、属性归属或互动关系。
- 用户指定镜头、画布、参考图构图、POV、俯视、广角、大场景。
- 强光影、叙事场景、空间层次会影响主体可读性。
- 生成结果容易脸小、漂浮、背景抢主体、肢体互相粘连。

跳过：

- 简单单人、半身/头像、用户已有完整 prompt。
- 只需要 tag 校验、画师解析或工作流执行。

## Anima 边界

- 不默认 `1920x1080`；初始生成通常不推荐单边超过 `1536`，大图交给放大节点。
- 复杂衣装或身份优先时，先简化背景，不要删身份锚点。
- 多角色必须绑定“位置 + 角色 + 关键外观/服装 + 动作”，不要写 loose hair/color/outfit list。
- 极端俯视、低角度、POV、广角会增加脸部和肢体崩坏风险；需要时明确前景、中景、背景和脸部可读性。
- 光源方向保持一致；背光时补一句保护脸部或轮廓。
- 大背景/宽画幅必须说明主体占比、地面接触、尺度参照或前中后景，否则容易漂浮或主体过小。

## 画布参考

| 画布        | 用途                            |
| ----------- | ------------------------------- |
| `1024x1536` | 单人全身、竖图、手机壁纸        |
| `1024x1024` | 头像、半身、中心主体            |
| `1152x1536` | 角色为主，带少量环境            |
| `1536x1024` | 多人互动、横向动作、宽背景      |
| `1536x1152` | 室内中景、人物占比较高的环境    |
| `1536x864`  | 宽银幕、远景、桌面壁纸          |
| `1536x1536` | 高信息量中心构图、道具/服装复杂 |

用户给定尺寸时保留尺寸，但要调整主体大小、留白和背景方向。

## nltags 句式

- 通常 1-4 句就够；复杂图可以更多，但每句都要能改变画面。
- 每句一个可见控制：位置、动作、镜头、光源、景深、脸部质量。
- 使用具体动词：`Place`, `Use`, `Keep`, `Frame`, `Light`, `Blur`。
- 不写文学比喻、世界观解释、连续视频动作。

示例：

```text
Place the main subject slightly right of center.
Use soft window light from the left side.
Keep her face sharp and readable, with a softly blurred background.
```

多人示例：

```text
Place Reimu on the front left, with brown hair and a red shrine outfit.
Place Marisa on the front right, with blonde hair and a black witch dress.
Keep their hands separated and both faces readable.
```

## 输出契约

返回或传给 `comfyui-animatool`：

```json
{
  "canvas": {
    "width": 1536,
    "height": 1024,
    "reason": "horizontal interaction scene"
  },
  "camera": "upper body, eye-level, normal perspective",
  "composition": "two characters share the midground with clear spacing",
  "lighting": "soft window light from the left",
  "focus": "faces sharp and readable, background softly blurred",
  "nltags_sentences": [
    "Place the two characters in the center midground with clear spacing.",
    "Use soft window light from the left side.",
    "Keep both faces sharp and readable, with a softly blurred background."
  ]
}
```

## 按需参考

用户输入稀疏、场景容器明确但缺少天气、动作、道具或叙事节拍时，读 `references/intent-expansion-patterns.md`。

只有遇到具体失败模式时才读 `references/composition-case-studies/_index.md`，不要默认加载整套案例库。
