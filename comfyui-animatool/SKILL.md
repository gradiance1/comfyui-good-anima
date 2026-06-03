---
name: comfyui-animatool
description: |
  当 Anima prompt 组装需要更细规则时加载：槽位顺序、tag/nltags 分工、冲突检查、画师解析、文件命名 args、Artist Mixer prompt 约束。
  不用于执行 workflow（交给 comfyui-manager）、纯 tag 查询（交给 danbooru-tags）、或通用构图教学。
---

# ComfyUI-AnimaTool — Prompt 组装守门

本 skill 不替模型强行设计画面。它只做 Anima 特定的 prompt 组装、冲突消解和 workflow args 准备。

## 意图 brief 接入

组装 prompt 前必须接住主控的轻量意图识别结果：用户想要什么、哪些要素已锁定、是否需要展开。用户已有完整画面方案时保留原意并最小组装；需求仍然稀疏或缺少画面成立条件时，先补意图 brief 再组装。不要把意图 brief 变成固定模板，也不要直接把用户原句字面翻译成 tag。

意图 brief 来自 `comfyui-anima-master` 的轻量解析，或来自 `anima-composition-director` 的完整解析。它只回答“为了让需求变清楚还缺什么”，通常包括：

- 用户明确锁定了什么：主体、场景容器、关系、风格锚点、拒绝项。
- 画面成立需要补什么：季节/天气/时间、服装状态、空间层次、身体动作。
- 当前图最有张力的瞬间是什么：故事节拍、手势、概念锚点、视线关系。

组装时按下面方式消费，不把 brief 原样塞进 prompt：

| brief 内容 | 回填位置 |
| --- | --- |
| 主体、作品、画师、稳定外观 | hard anchors；需要时用 `danbooru-tags` 校验 |
| 场景容器、少量天气/光影 tag | `environment` 或 tags |
| 手势、关系、故事节拍、复杂空间、脸部保护 | `nltags` |
| 查不到的复合概念、隐喻关系 | `nltags`，不要伪造 Danbooru tag |

如果 brief 与用户硬约束冲突，保留用户硬约束；如果 brief 与 Anima 规则层冲突，优先调整 brief 的表达方式，不改写用户意图。

## 组装顺序

```text
quality_meta_year_safe → count → character → series → artist/style → appearance → tags → environment → nltags
```

- `prompt_11`: 正向 prompt。
- `prompt_12`: 负向 prompt。
- `width` / `height` / `batch_size` / `steps` / `rtx_vsr_quality` / `filename_prefix`: 写入 args。
- 不传 workflow schema 未暴露的字段。
- 不把 LoRA 文件名写进 prompt；workflow 已加载 LoRA。

## 质量前缀

默认双 LoRA 工作流：

```text
masterpiece, very aesthetic, best quality, score_9, score_8, highres, absurdres, newest, year 2025, nsfw
```

裸模型/对比测试：

```text
masterpiece, best quality, score_7, safe
```

安全标签必须是 `safe / sensitive / nsfw / explicit` 之一。用户未指定时默认工作流用 `nsfw`。

## Hard anchors 与 nltags

Hard anchors 适合放：

- 人数、角色、作品、用户指定或已选定画师。
- 稳定外观：发色、瞳色、发型、基础服装、道具、姿势、表情、简单场景。

`nltags` 适合放：

- 镜头结构、前景/中景/背景、人物相对位置、光源方向、景深落点、脸部可读性。
- 连续动作、情感关系、复杂服饰组合、难以确认的自然语言描述。

规则：同一语义不要同时写 tag 和 `nltags`。查不到的复合概念不要伪造 tag，改写成短自然语言。

## Tag 查询策略

- 用户指定角色/作品/画师，或 hard anchor 不确定时，用 `danbooru-tags` 校验。
- 模型常识能处理的普通构图、光源方向、氛围、故事关系，不要拿去查 tag。
- 典型生图查询 2-4 个语义锚点即可；不是硬上限。复杂命名角色/多角色可以多查，但不要反复补查。
- 画师中文名、圈名、社交 handle 不确定时，可先网络搜索 canonical name，再用 `danbooru-tags` 确认 `@artist`。
- 只把符合意图的 `confirmed_tags` 回填；`candidate_tags` 必须筛选。

## 画师规则

- 普通 prompt 的画师必须写 `@artist name`。
- 用户没指定画师时，不强制套预设画师；可以留空，或根据用户明确风格选 1 个并校验。
- 默认加速 + 美学 LoRA 工作流推荐单画师；除非用户明确要求，否则不要在同一张图里堆多个画师。
- 用户说“允许多个画师”时，把它理解为候选许可；单个非融合 job 仍选 1 个画师。
- “分别用 A/B”是多个普通 job。
- “融合 A+B / artist mixer / artist_chain”才用 Artist Mixer。

Artist Mixer：

- `artist_chain` 不带 `@`。
- `prompt_11` 不重复画师名。
- 默认 mixer 参数由 workflow 维持；用户没要求不要传 `artist_mixer_*`。
- 可用 `(name:1.2)` 表达相对权重。

## 冲突检查

组装前必须消解：

- `solo` vs 多人。
- `close-up` vs `full body`。
- `from above` vs `from below`，`from front` vs `from behind`。
- `closed eyes` / 睡眠 / 昏迷 vs `looking at viewer`。
- `completely nude` vs 具体服装。
- 多角色 loose appearance list：必须给每个角色绑定位置和关键外观。
- tag 与 `nltags` 语义重复。

标签数量按画面需要控制。普通单人约 16-30 个核心 tag；复杂图可更多，但不要用 tag 填满构图职责。

## nltags 规范

- 通常 1-4 句；复杂构图、强叙事或多角色图可以更多，但每句都必须服务画面。
- 每句 8-18 个英文词为宜；这只是可读性建议，不是截断规则。
- 一句只控制一个可见要素：位置、动作、镜头、光源、景深、脸部质量。
- 使用 `Place / Use / Keep / Frame / Light / Blur` 这类直接控制动词。
- 不写文学比喻、世界观说明、营销形容词或多镜头视频动作。

## 参数建议

- 默认画布由画面决定；简单单人可用 `1024x1536` 或 `1024x1024`，多人/横向场景常用 `1536x1024`。
- 默认 `steps=30`；用户要求高质量、复杂背景、多人互动、强光影时用 `40`。
- `rtx_vsr_quality` 默认 `ULTRA`。
- `filename_prefix`: `anima/%year%-%month%-%day%/<model>-<artist|none>-<subject>`。

## 按需参考

- 共享模型、LoRA、CLI、脚本、命名事实：`shared/conventions.md`。
- 中文需求太抽象，需要补东方幻想、服饰、光影、材质等可见细节时：`references/chinese-visual-brief.md`。
- 复杂 prompt 组装、画师解析、年代标签、冲突矩阵：`references/prompt-assembly.md`。
- 批量任务分类：`references/batch-strategy.md`。
- 模糊输入缺少场景动作、天气、手势或叙事节拍时：`../anima-composition-director/references/intent-expansion-patterns.md`。
