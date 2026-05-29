# Anima 多图、批量与 Artist Mixer

> ⚠️ 核心规则已回流至 SKILL.md。本文件仅提供扩展细节与边界情况。如内容与 SKILL.md 冲突，以 SKILL.md 为准。

只在用户明确要求多张、几批、抽卡、多方案、每张不同内容、画师串或多画师融合时读取本文件。

## 批量分类

默认只生成 1 张。先区分两类需求：

1. 同 prompt 多变体：同角色、同构图、同提示词，只想要不同随机结果。使用同一个 args，设置 `batch_size=N`。
2. 多 prompt 多任务：每张图的角色、服装、随机 tag、构图或画布不同。每张分别组装 args，通过 `comfyui-manager` 提交多个 job。

规则：

- 用户没说数量：`batch_size=1`，只提交 1 个 job。
- “出 N 张同类型不同种子”：优先 `batch_size=N`。
- “第一张 A，第二张 B”：不能用 `batch_size`；必须分别写 prompt 和 filename。
- “分别用 A/B 画师各出 N 张”：不是画师串；每个 job 只写一个 `@artist`，仍用默认工作流。
- “随机 tag 抽卡出 N 张”：每张先抽/筛一组兼容 tag，再分别组 prompt。
- 普通批量默认 `steps=30`；用户明确高质量或精修时可用 `steps=40`。

## Artist Mixer

用户明确要求画师串、多画师融合、artist mixer 或多画师权重混合时，使用：

```text
local/anima-txt2img-aesthetic-lora-artist-mixer
```

规则：

- 画师写入 `artist_chain`，不要带 `@`。
- `prompt_11` 不包含多画师 tag。
- 默认参数由 `comfyui-manager` 工作流提供：`combine_mode=output_avg`、`fusion_mode=interpolate`、`artist_mixer_strength=0.7`、`artist_mixer_normalize_weights=true`、`artist_mixer_apply_to_uncond=false`。
- 非用户要求不要改这些参数。
- 默认保持 `artist_mixer_normalize_weights=true`。
- 关闭 `artist_mixer_normalize_weights` 后，2-3 个画师可能过曝，4 个以上可能被节点拒绝。
- 需要主辅关系时，主画师从 `1.0`、辅画师从 `0.2-0.4` 开始。
- 画师越多速度和风格可控性越差；用户未指定数量时不要追求长串。
- 画师组合优先选风格相近者；差异很大的画师容易折中退化。
- 用户未指定数量时优先 2-4 个。

示例：

```json
{
  "artist_chain": "wlop, (sakimichan:1.2), (krenz:0.7)",
  "prompt_11": "masterpiece, very aesthetic, best quality, 1girl, ...",
  "prompt_12": "worst quality, low quality, ...",
  "width": 1024,
  "height": 1536,
  "batch_size": 1,
  "steps": 30
}
```

## 脚本约束

临时脚本、辅助脚本或一次性批量提交脚本只能读取/提交本 skill 已确认的 args，不得自行决定：

- prompt
- `steps`
- 画布
- 模型
- `filename_prefix`

批量输出时只汇总每张编号、简短主题、`local_path`；不要复述完整 prompt 和检索 JSON。
