---
name: comfyui-anima-master
description: |
  用户要通过 ComfyUI 生成 Anima 二次元图片时加载。负责把普通生图、批量、随机、画师融合、tag 查询和执行路由到正确 skill，同时保留用户原始意图。
  触发词：anima、comfyui、generate、draw、生图、画图、出图、生成、来一张、roll、抽卡、画师融合。
  不用于纯服务器运维（交给 comfyui-manager）、独立 tag 查询（交给 danbooru-tags）、或用户未明确要求的非 Anima 工作流。
---

# ComfyUI-Anima 主控

本 skill 是路由和最小事实层。不要替代模型自身的构图常识；只锁住 Anima、LoRA、Artist Mixer、workflow args、CLI 执行这些模型不知道或容易乱调用的事实。

## 路由

| 用户意图 | 处理 |
| --- | --- |
| 普通 Anima 生图 | 本 skill 组织流程；需要细节时读 `comfyui-animatool` |
| 随机 / roll / 抽卡 | `anima-random-gen` 产出语义参数 → 回到 `comfyui-animatool` 复核 |
| 明确构图/镜头/多人/参考图/大场景/象征隐喻/暗示表达 | `anima-composition-director` 给视觉计划 |
| 仅查 tag/画师/角色/作品 | `danbooru-tags`，不执行生图 |
| 执行已组装 args / 查队列 / 运维 | `comfyui-manager` |

进入本 skill 后先做轻量意图识别：判断用户到底要生成什么、哪些要素已锁定、哪些缺口会影响画面成立。只有用户已经给出主体、场景、关系/动作、镜头或构图、风格/光影等足够完整的画面方案时，才跳过意图展开和构图 skill；否则先把模糊需求具体化，再进入 tag 校验与 prompt 组装。

## 不可丢事实

- 默认工作流：`local/anima-txt2img-aesthetic-lora`。
- 对比/禁用 LoRA 才用：`local/anima-txt2img-base`。
- 明确多画师融合才用：`local/anima-txt2img-aesthetic-lora-artist-mixer`。
- args 是纯参数对象；正向 `prompt_11`、负向 `prompt_12` 必填。
- 普通画师写进 `prompt_11`，格式 `@artist name`；Artist Mixer 写 `artist_chain`，不带 `@`，且不要在 `prompt_11` 重复画师。
- 默认 LoRA 质量前缀与 LoRA 栈绑定：`masterpiece, very aesthetic, best quality, score_9, score_8, highres, absurdres, newest, year 2025, nsfw`。
- 裸模型对照前缀：`masterpiece, best quality, score_7, safe`。
- 默认负向：`worst quality, low quality, score_1, score_2, score_3, blurry, bad anatomy, bad hands, bad feet, extra fingers, missing fingers, distorted face, text, watermark, logo`。
- `submit` 非阻塞：提交后返回 `prompt_id` / manifest，不主动轮询；用户要求看结果时才查状态或补缓存。

## 标准流程

1. 先做意图识别 gate：用一句话确认用户真正想生成的画面，并记录已锁定的主体、场景容器、关系/动作、风格锚点和拒绝项。
2. 判断是否需要意图展开：如果用户已经给出完整画面方案，只保留轻量 brief，不扩写成另一张图；如果输入仍然稀疏、只给场景/关系/氛围、或缺少动作、空间、时间、光影等会影响画面成立的信息，则在 tag 校验前把需求具体化为“确认 → 补全 → 创作组合”。需要更完整意图解析时读取 `anima-composition-director`。
3. 判断是否需要规则层收缩：多人归属、复杂镜头、参考图迁移、强光影叙事、大场景空间关系或 Anima 已知崩点，才按症状读取 `composition-case-studies/`；不要把规则层当意图层。
4. 解析并校验 hard anchors：用户给中文名、外号、圈名、社交账号、CP 简称或同名角色时，先按 `comfyui-animatool` 的名称解析规则做网络 canonical 解析，再调用 `danbooru-tags` 校验角色、作品、用户指定画师和关键服装/外观。模型已知或用户未要求的普通描述，不必强查。
5. 组装 prompt：把意图 brief 拆成 hard anchors、environment 与 `nltags`，再按 `quality → count → character → series → artist/style → appearance → tags/environment → nltags` 组装，避免 tag 与自然语言重复。
6. 写 args：只传 workflow schema 支持的字段。
7. 交给 `comfyui-manager` 执行。

## Prompt 边界

- Anima prompt 是 Danbooru tags + short natural language，不是纯 tag 堆砌，也不是文学段落。
- `nltags` 只写可见控制：位置、动作、镜头、光源、景深、脸部可读性。一般 1-4 句足够；复杂图可以更多，但每句都要服务画面。
- 不要重复：同一语义要么在 tag，要么在 `nltags`。
- 冲突必须解决：`solo` vs 多人、`close-up` vs `full body`、`from above` vs `from below`、`closed eyes` vs `looking at viewer`、裸体状态 vs 服装。
- 标签用空格：`red hair`，不要 `red_hair`；`score_9` 这类质量 token 保留下划线。
- 没有用户画师偏好时，不强制套默认画师；可留空或按用户风格需求轻量选择一个已验证画师。

## 画师融合

只在用户明确说融合、混合、多画师合一、artist mixer、artist_chain 时启用。

- “允许多个画师”不是融合指令；默认从候选里为每个非融合 job 选 1 个画师。
- `artist_chain`: `wlop, (sakimichan:1.2), (krenz:0.7)`。
- 不带 `@`。
- `prompt_11` 不重复画师。
- 默认 mixer 参数由 workflow 提供；用户没要求不要传高级 mixer 字段。
- “分别用 A/B 各出图”是多个普通 job，不是 Artist Mixer。

## 批量

- 同 prompt 多变体：一个 args，`batch_size=N`。
- 不同角色/画师/构图/随机内容：多个 args，分别 `submit`。
- 每个 job 都必须有自己的 `filename_prefix`，命名格式见 `shared/conventions.md`。
- 不要为了等待图片完成而把 `submit` 变成阻塞流程。

## 需要继续读取

- Prompt 组装细节与冲突矩阵：`comfyui-animatool/SKILL.md`。
- 意图解析与构图计划：`anima-composition-director/SKILL.md`。
- Tag 查询：`danbooru-tags/SKILL.md`。
- 执行命令和 workflow args：`comfyui-manager/SKILL.md`。
- 共享模型、LoRA、节点、CLI、脚本、文件命名规则：`shared/conventions.md`。
