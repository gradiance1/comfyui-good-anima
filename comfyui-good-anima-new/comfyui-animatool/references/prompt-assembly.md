# Anima Prompt 组装细则

> ⚠️ 核心规则已回流至 SKILL.md。本文件仅提供扩展细节与边界情况。如内容与 SKILL.md 冲突，以 SKILL.md 为准。

只在需要处理画师时代、槽位冲突、权重、自然语言控制或复杂 prompt 规则时读取本文件。

## period 与 dataset tag

`newest / recent / mid / early / old` 是风格时期控制，不是固定装饰。

- 默认现代二次元风格：保留 `newest, year 2025`。
- 指定年份：优先使用 `year xxxx`，必要时配合最接近 period；不要同时放冲突 period。
- 旧画风/赛璐璐/早期代表作：优先考虑 `old` 或 `early`，并让年份、代表作/IP 和画师时期一致。
- `retro_artstyle`、`faux_retro_artstyle`、`heisei_retro`、`traditional_media` 可用 `danbooru-tags` 校验后放入 tags。
- `ye-pop`、`deviantart` 等 dataset tag 只在用户明确要求对应数据域质感时使用。

## 画师字段

`artist` 是当前工具 schema 的必填字段，画师 tag 必须以 `@` 开头。

### 画师称呼解析

用户给出的画师名可能是中文圈称呼、昵称、社交平台名、画集名或社团名，不一定是 Danbooru/Anima 的 artist tag。不要维护本地固定别名表，也不要把中文昵称按字面直接丢给 tag 检索器。

1. 如果画师输入不是明确 Danbooru artist tag，先进行网络搜索确认 canonical artist name、常见别名和公开资料来源。
2. 优先采用官方主页、Pixiv/X/微博资料、百科条目、画集/作品页等互相印证的信息。
3. 将确认出的英文/罗马字画师名转为候选 `@artist`，再用 `danbooru-tags --group artist` 校验。
4. 只有 `danbooru-tags` 返回 confirmed artist 后才写入 prompt；查不到时说明无法确认 tag，或改用最接近的 confirmed artist 候选。
5. 网络搜索只用于解析称呼和别名，不替代 Anima CSV / Danbooru tag 校验。

### 角色外貌与服装确认

命名角色的默认服装、原作服装、某版本/形态、活动服、制服或特殊配饰不应让模型凭印象补全。不要用角色名反查 `appearance/clothing` 来推断设定。

1. 优先依据用户参考图；没有参考图时，用官方资料、角色页、百科或轻量网络搜索确认关键外观和服装来源。
2. 只把可被 Danbooru 稳定锚定的部分交给 `danbooru-tags` 检索，例如发色、瞳色、发型、制服、巫女服、帽子、武器或明确道具。
3. 查不到的复杂服装结构、材质组合、版本差异和装饰细节写入 `nltags`，不要伪造 Danbooru tag。
4. 多角色时逐个确认外观/服装归属，避免把 A 的服装、发色或配饰写到 B 身上。
5. 网络搜索只用于确认外观/服装事实，不替代 Danbooru tag 校验。

- 用户指定画师：先用 `danbooru-tags --group artist` 校验。
- 用户要求随机画师：用 `danbooru-tags --random 5 --for-prompt --json --compact` 取 1 个。
- 用户未指定画师：按风格意图从少量候选中选 1 个再校验，不要用抽象气质词查 artist。
- 默认普通生图只选 1 个画师。
- 用户明确不要画师：如果 schema 允许可传 `artist: ""`；若工具拒绝，说明 AnimaTool 当前 schema 要求画师字段。

## 质量前缀

本地默认使用美学 LoRA 增强工作流：

```text
masterpiece, very aesthetic, best quality, score_9, score_8, highres, absurdres, newest, year 2025, nsfw
```

只有用户明确指定基础工作流、禁用 LoRA 或做对比测试时，才使用基础质量前缀：

```text
masterpiece, best quality, score_7, newest, year 2025, nsfw
```

常用候选：

- 日系本子 / 成年向：`@pija`, `@okara`, `@mignon`
- 肉感 / 黑丝白丝：`@rhasta`, `@mignon`, `@yom`
- 中性通用 / 清爽二次元：`@mignon`, `@fkey`, `@hiroichi`

## 画师时代与代表作

- 用户指定年份、年代、旧画风、新画风、赛璐璐、某时期或某代表作时，把 `year` 视为风格控制参数。
- 用户指定代表作/IP 风格时，可把该代表作/IP 作为 `series` 或 style anchor；先用 `danbooru-tags --group series` 校验。
- 查不到代表作 tag 时写入 `nltags`，不要伪造 Danbooru tag。
- 画师/代表作/年份三者不能冲突。

## hard anchors 与 nltags

hard anchors 放可被 Danbooru 稳定控制的内容：

- 人数、角色、作品、画师
- 发色、瞳色、发型、体型
- 已确认的服装、道具、姿势、表情、视角、光影、场景

`nltags` 放难以用单个 tag 表达的内容：

- 动作连续性、神态细节、叙事关系
- 镜头结构、前景/中景/背景、景深落点、主体脸部可读性
- tag 库缺失的服装/配饰/材质组合
- 光影、空间、氛围的完整描述

同一语义不要在 tags 和 `nltags` 中冲突。

## 冲突检查

- `solo` 不能和多人互动标签混用。
- 睡眠、昏迷、闭眼时不要写 `looking at viewer`。
- `close-up` 与 `full body` 不混用。
- `from above` 与 `from below` 不混用。
- `completely nude` 不和具体服装同用。
- 连续动作或复杂角色关系写入 `nltags`。
- 同一 tag 不重复写；强调靠顺序和更准确的词。
- 普通单人核心 tag 控制在 16-30 个；复杂主题最多约 40 个。
- 正面单人图默认保留 `looking at viewer` 或 `facing viewer`，并在 `nltags` 中保护脸部清晰，除非用户明确要求背影、侧脸、远景或遮脸。
- 多人图必须明确每个角色的关键外观、相对位置、主动作和视线归属，不要只写一组外观后接多个角色名。
- 命名角色外观或服装不确定时，不要用 `appearance/clothing` 盲查反推设定；先依据参考图、官方资料或轻量网络搜索确认关键外观和服装，不确定细节写入 `nltags`。

## 权重控制

Anima 支持 prompt weighting，官方示例为 `(chibi:2)`。

- 默认不要加权，先靠准确 tag、槽位顺序和短句控制。
- 只有用户明确要求强化/弱化，或某元素多次不稳定时才加权。
- 从 `(tag:2)` 级别开始测试；不要默认使用 `1.1-1.3` 小权重。
- 不要给角色名、安全标签、质量前缀或整段 `nltags` 默认加权。
- 同一 prompt 最多处理 1-3 个关键视觉元素。

## nltags 写法

- 默认 2-4 句；复杂构图最多 5 句。
- 单句尽量 8-18 个英文词，最多约 25 个词。
- 每句只控制一个画面要素：动作、姿势、镜头、构图、光源、背景层级、脸部质量。
- 禁止文学修辞、比喻、世界观解释、剧情说明、营销式形容词堆叠。
- 写法优先使用直接控制句：`Place her full body slightly right of center.`
