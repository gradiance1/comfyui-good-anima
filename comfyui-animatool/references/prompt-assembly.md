# Prompt 组装参考

本文件只补 prompt 组装的边界情况。标准槽位顺序、质量前缀、模型/LoRA/节点事实见 `shared/conventions.md`。

## 场景决策树

拿到需求后先判类型，再组装 prompt。不要先翻标签库。

| 场景类型                 | 处理                                                             |
| ------------------------ | ---------------------------------------------------------------- |
| 用户粘贴完整 prompt      | 只检查安全标签、明显冲突、尺寸和 workflow args，不重写风格       |
| 简单单人角色图           | `comfyui-animatool` 直接组装；按需校验角色、作品、画师           |
| 多角色/互动关系          | 先让 `anima-composition-director` 绑定位置、外观、动作和视线关系 |
| 大场景/特殊镜头/强光影   | 先做构图计划，再把空间、光源、脸部保护写成 `nltags`              |
| 候选池批量               | 先抽候选、筛选 K 个方案；每个方案独立 prompt、画布、args         |
| 参考图迁移               | 先确定只迁移构图，还是迁移完整视觉；构图迁移交给 composition     |
| 画师/角色/作品名称不确定 | 先解析 canonical name，再用 `danbooru-tags` 校验，不凭空造 tag   |

## 内容槽位细化

在共享顺序 `quality_meta_year_safe → count → character → series → artist/style → appearance → tags → environment → nltags` 下，内容部分按这个内部顺序整理：

```text
count/identity → appearance → clothing/state → pose/action → expression/reaction → camera/shot → scene/environment → detail/mood → nltags
```

- `appearance`: 发色、瞳色、发型、体型、身份特征；IP 角色要补防混淆锚点。
- `clothing/state`: 服装大类 + 穿着状态 + 1-2 个关键材质/配饰，不要堆满衣物词。
- `pose/action`: 一个主动作 + 一个辅助姿势；连续动作和角色关系写进 `nltags`。
- `expression/reaction`: 表情、视线和身体状态必须匹配动作；不要跨情绪硬堆。
- `camera/shot`: 只选一个核心景别和一个核心角度；复杂镜头转 `nltags`。
- `scene/environment`: 一个主场所 + 少量能解释尺度、天气或故事的道具。
- `detail/mood`: 只选能改变画面的 1-2 个质感/后期/氛围词。

## 年代与数据集标签

`newest / recent / mid / early / old` 控制风格年代，不是装饰词。

| 触发                         | 处理                                                    |
| ---------------------------- | ------------------------------------------------------- |
| 默认现代二次元               | 保留 `newest, year 2025`                                |
| 用户指定年份                 | 使用 `year XXXX` 和最接近的 period，移除冲突的 `newest` |
| 旧番、复古、赛璐璐           | 使用 `old` 或 `early`，并让年份、作品、画师年代一致     |
| 平成复古、传统媒介           | 用 `danbooru-tags` 校验，可确认才放 tag                 |
| 西方/DeviantArt/非二次元艺术 | 只有用户明确要求时才考虑 `ye-pop` / `deviantart`        |

冲突规则：`old` + `newest`、年份与 period 不匹配，必须先修正。作品 tag 不确定时，保留画师和年份，把作品描述放进 `nltags`，不要伪造 Danbooru tag。

## 名称解析：网络别名 → 本地 tag 校验

用户给的可能是中文名、外号、圈名、社交账号、社团名、简称或 CP 俗称，不一定是 Danbooru canonical tag。

执行规则：

1. 明确是常见 canonical tag 时，可直接用 `danbooru-tags` 校验。
2. 输入不像 canonical tag，或本地查询 miss / 候选明显不对时，先网络搜索解析 canonical name、别名和所属作品。
3. 网络只负责“人类叫法 → 候选 canonical name”；不要把网页描述直接当 Anima tag。
4. 解析后必须回到 `danbooru-tags` 校验 artist / character / series category。
5. 只有 confirmed 且符合用户意图的 tag 回填；无法确认时用短英文自然语言保留用户意图，不伪造 hard anchor。
6. 角色外观设定需要时可网络确认，但外观 tag 仍要单独校验；不要把 aliases 当外观设定。
7. 角色 tag confirmed 只证明角色锚点有效，不保证默认服装、发色、道具一定正确；模型可先基于自身知识补少量身份锚点。
8. 当角色小众、同名/多皮肤/跨作品、用户要求高还原、模型自己不确定，或历史生成出现服装/人设漂移时，先网络/官方资料确认 3-5 个身份锚点，再用 `danbooru-tags` 校验可标签化部分。
9. 随机候选池不逐个网络搜索；最终选中的命名/IP 角色也不强制默认搜索。先让模型判断是否有把握，不确定再查。画师只有在用户要求画风、时期、代表作或名称有歧义时才查。

常见触发：

- 画师：中文圈名、昵称、社团名、Pixiv/X/微博名、用户说“某某老师/太太”。
- 角色：中文译名、外号、CP 简称、同名角色、跨作品重名。
- 作品：中文译名、缩写、旧译名、系列别称。

## 画师解析细则

用户可能给中文圈名、昵称、社交账号或社团名，不一定是 Danbooru artist tag。

解析流程：

1. 输入不像明确 Danbooru 画师 tag 时，先网络搜索 canonical name、常见别名和公开来源。
2. 交叉参考官网、Pixiv、X、微博、百科或画集页。
3. 把确认的英文/罗马音转成 `@artist` 候选。
4. 用 `danbooru-tags --group artist` 验证。
5. 只有确认过的画师进入 prompt；无法确认时告知用户并给最接近候选。
6. 网络只用于解析别名；Anima CSV / Danbooru tag 校验才是最终入口。

用户没有画师偏好时：

- 不强制默认画师。
- workflow 允许时，画师槽位可留空。
- 具体风格确实需要画师锚点时，只选 1 个合理画师并校验。
- 不要用“dark / dramatic / corruption”这类抽象风格词搜索画师。

多画师判断：

- “允许使用多个画师 / 可参考多个画师” → 候选许可；默认每个非融合 job 选 1 个 `@artist`。
- “分别用 A/B 画师各 N 张” → 多个普通 job，每个 job 一个 `@artist`。
- “A+B 混合 / A 和 B 融合” → Artist Mixer，`artist_chain` 不带 `@`。
- 随机画师候选池 → 使用 `danbooru-tags --random N --group artist --json`；默认加速 + 美学 LoRA 工作流每个非融合 job 使用 1 个已确认 `@artist`。

画师、年代、作品必须对齐。用户强调某一时期风格时，优先调整 `year`/period 和 Artist Mixer 权重，不要用 prompt 权重硬压整个画师名。

## Hard anchors 与 nltags

适合放 hard anchors：

- 人数、角色、作品、画师。
- 基础外观：发色、瞳色、发型、体型。
- 已确认的服装、道具、姿势、表情、稳定场景/光影 tag。

适合放 `nltags`：

- 连续动作、表情细微差别、叙事关系。
- 镜头结构、前景/中景/背景、景深焦点、光源方向。
- tag 库无法稳定表达的服装/配饰/材质组合。
- 完整空间关系、氛围、脸部可读性保护。

黄金规则：同一语义同时出现在 tag 和 `nltags` 就是冲突。Anima 有 tag dropout 训练，少量硬锚点 + 清晰 `nltags` 通常比塞满 tag 更稳。

## 冲突检查矩阵

每个最终 prompt 前都检查：

身份与人数：

- `solo` 与 `2girls` / `multiple girls` 互斥。
- 睡眠、昏迷、闭眼 与 `looking at viewer` 互斥。
- 单人数量与多人互动 tag 互斥。

镜头与景别：

- `close-up` / `face focus` 与 `full body` / `wide shot` 互斥。
- `from above` 与 `from below` 互斥。
- `from front` 与 `from behind` 互斥。
- 复杂镜头转成 `nltags`，tag 里只留一个简单视角锚点。

服装与状态：

- `completely nude` 与任何具体服装互斥。
- 内衣套装（`cat lingerie`, `lace lingerie`, `babydoll`, `negligee`, `chemise` 等）与 `no panties` / `bottomless` 通常冲突——内衣套装隐含包含内裤，模型优先解析套装忽略暴露标签。需暴露时拆为单件（`cat bra` + `no panties`）。
- 外衣/制服（`maid outfit`, `school uniform`, `bunny suit` 等）与 `no panties` / `bottomless` 兼容——穿制服不穿内裤属于合理场景。
- `pantyhose` 与 `barefoot` 互斥（除非 `torn pantyhose`，脚部撕开例外）。
- `blindfold` 与任何需要眼睛可见的标签互斥（`heart-shaped pupils`, `rolling eyes`, `looking at viewer`）。
- 暴露状态要拆清上半身、下半身、是否穿着，不要模糊堆 tag。

细节过度：

- 同一身体部位最多 2 个细节标签，且不能互斥。
- `spread toes` + `toe scrunch` / `toes curling`：舒展 vs 蜷缩，互斥。
- `spread fingers` + `clenched fist` / `gripping`：张开 vs 握拳，互斥。
- `bouncing breasts` + `breasts squeeze together`：弹跳 vs 挤压，动态矛盾。
- `open mouth` + `clenched teeth` / `closed mouth`：张嘴 vs 闭嘴。
- `rolling eyes` + `looking at viewer`：翻白眼 vs 直视。
- `spread legs` + `legs together`：分开 vs 并拢。
- 足部 3 个以上细节标签容易导致脚趾/脚掌畸形。

动作与姿势：

- 一个主动作 + 一个辅助姿势即可。
- 连续动作和角色互动写进 `nltags`。

重复：

- 重复 tag 只保留最准确的一个。
- 强调靠顺序、准确 tag、必要权重，不靠堆叠同义词。

数量：

- 普通单人约 16-30 个核心 tag。
- 复杂多人可更多，但不要让 tag 接管构图职责。
- 超限时先删弱环境、弱氛围、弱细节。

物理兼容：

- 场景、动作和道具必须能同时成立，例如水下、强风、拥挤空间、坐姿、站姿都要影响服装、头发和动作选择。
- 同一身体部位不要堆互斥状态；强调靠一个准确状态，而不是多个近义词。
- 服装套装隐含的部件不要和暴露/缺失状态冲突；需要特殊穿着状态时拆成上装、下装、配饰分别描述。

脸部可读性：

- 默认保留 `looking at viewer` / `facing viewer`，除非用户明确要求背影、侧脸、远景或遮脸。

多人归属：

- 不要先列多个角色，再列一串未归属的发色、瞳色、衣服。
- 用短英文 `nltags` 说明谁在什么位置、什么外观、什么服装、做什么动作、看向谁。

## 生成前自检

提交给 `comfyui-manager` 前，至少检查：

1. 人数与身份一致：`count`、角色数量、`solo` / 多人关系没有矛盾。
2. 槽位顺序一致：质量、安全、人数、身份、画师、外观、动作、环境、`nltags` 没乱序。
3. 画师规则一致：普通 job 最多 1 个 `@artist`；Artist Mixer 不在 `prompt_11` 重复画师。
4. 冲突矩阵通过：镜头、服装、动作、视线、睡眠/闭眼没有互斥。
5. tag 与 `nltags` 不重复：同一语义只保留在最适合的位置。
6. tag 数量合理：普通图不靠堆标签，复杂图也要优先保身份、脸、手和主体关系。
7. 画布匹配画面：多人/横向关系不要硬用竖图，头像/半身不要硬用大宽景。
8. 高风险主题不作为通用配方保留；只处理合规成人、用户明确且可执行的视觉需求。

## 权重控制

- 默认不加权重；准确 tag、槽位顺序和 `nltags` 优先。
- 只有用户明确要求，或同一元素连续 3 次以上失败，才考虑权重。
- 起步用 `(tag:2)`，不要用 `1.1-1.3` 这类对 Anima 太弱的权重。
- 每个 prompt 最多 1-3 个加权元素。
- 不给角色名、安全标签、质量前缀、整段 `nltags` 加权。
- 画师主导用 `artist_chain` 权重，不用 prompt 权重。
- 抽象氛围改写成光影、构图、表情，不用权重硬压。

## nltags 句式

写直接可见控制句，通常 2-4 句就够；复杂图可以更多，但每句都要服务画面。每句 8-18 个英文词为宜，只控制一个可见元素。

可用模式：

```text
Place her full body slightly right of center.
Use a low front camera angle looking up.
Keep her face sharp and undistorted.
Soft backlight from the window, mild bokeh on background.
She looks at the viewer with a slight smile.
```

不要写：

```text
The mysterious fallen angel descends through shards of broken light,
her eyes holding the weight of a thousand forgotten promises...
debut volume cover, title text placement area at top
cinematic, breathtaking, masterpiece quality, stunning
```

背景规则：

- 背景不是主体：用轻微虚化或景深分离。
- 背景是主体：说明空间层次和景深焦点，不要列满背景物件。
- 不描述每个背景小物。

## 参考图迁移

用户提供参考图时：

1. 先确定迁移范围。“参考构图/视角/景深”只迁移构图，不迁移角色、服装、发型、道具、场景。
2. 拆解构图：景别、角度强度、前景/中景/背景、景深焦点、脸部可读性、是否允许鱼眼/广角。
3. 稳定元素转 hard anchors，复杂空间结构转 `nltags`。
4. 用户说“像这张图一样”这类完整参考迁移时，交给 `anima-composition-director` 做结构化拆解。

## 示例 1：普通单人

```text
quality: aesthetic-lora + safe | count: 1girl | char: kanade tachibana
series: angel beats! | artist: @mignon
appearance: silver hair, yellow eyes, long hair, school uniform
tags: solo, expressionless, looking at viewer, face focus, depth of field
environment: classroom, window, soft light, backlighting, blurry background
nltags: Place her beside the classroom window, facing the viewer. Use soft daylight from the left side. Keep her face centered, sharp, and undistorted. Blur the classroom background gently.
neg: worst quality, low quality, score_1, score_2, score_3, blurry, bad anatomy, bad hands, bad feet, extra fingers, missing fingers, distorted face, text, watermark
```

## 示例 2：Artist Mixer

```text
artist_chain: "wlop, (sakimichan:1.2), (krenz:0.7)"
prompt_11: 不写画师 tag，画师只由 artist_chain 处理
quality: aesthetic-lora + nsfw | count: 1girl | char: remilia scarlet
series: touhou | appearance: short blue hair, red eyes, gothic dress, bat wings
tags: solo, looking at viewer, face focus, night, moon, vampire
nltags: Place her centered against a moonlit sky. Use a low camera angle. Keep her face sharp and detailed.
```

## 示例 3：保留用户意图

```text
用户粘贴完整 prompt → 只检查安全标签、冲突、尺寸、steps、batch_size → 执行。不要重写成另一张图。
```
