# 批量策略参考

供 `comfyui-anima-master` 判断多图任务。所有批量决策必须在交给 `comfyui-manager` 之前完成。

## 默认单图

用户没有明确要求多张时，只生成 1 张：`batch_size=1`，1 个 job。

## 类型 1：同 prompt 多种子

触发：同角色、同构图、同 prompt，只要不同 seed。

执行：一个 args，设置 `batch_size=N`。

例子：“出 5 张同款不同种子” → 1 个 job，`batch_size=5`。

例外：用户要求逐张记录 seed 时，拆成 N 个 job，每个 `seed` 显式、`batch_size=1`。

## 类型 2：多 prompt 任务

触发：不同角色、服装、构图、画师、随机 tag 或每张图内容不同。

执行：每张图单独组装 prompt + args，分别 `submit`。

例子：“第一张 A 画师，第二张 B 画师” → 2 个 job，各自一个 `@artist`。

## 类型 3：候选池筛选批量

触发：用户要求“随机抽 N 个候选，选 K 个出图”，候选可以是画师、角色、作品、服装、姿势、男女组合或其他 tag group。

执行：

1. 用 `danbooru-tags --random N --group <group> --json` 抽候选池。
2. 按用户约束筛选 K 个方案，例如画师、角色、男女组合、题材分布、风格差异。
3. 只对选中的 K 个方案做网络搜索、背景确认或风格摘要；不要搜索完整候选池。
4. 每个方案独立生成 prompt、画布、steps、filename_prefix。
5. 每个方案独立 `submit`，返回 K 个 `prompt_id`。

不要把候选池数量 `N` 或选中数量 `K` 写死；按用户本次要求执行。

## 常见误判

| 用户说法 | 正确处理 | 错误处理 |
| --- | --- | --- |
| “分别用 A/B 画师各出 N 张” | 每个画师 N 个普通 job，各自一个 `@artist` | Artist Mixer / `artist_chain` |
| “随机 tag 抽卡出 N 张” | N 个 job，每个有自己的随机语义参数 | 一个 job 塞进所有 tag |
| “抽 N 个角色选 K 个出图” | 候选池筛选后生成 K 个 job | 把 N 个角色都写进 prompt |
| “抽男女角色组合” | 按组合约束筛选后，每组一个 job | 把男女候选池混成 loose list |
| “A 和 B 画师融合出图” | Artist Mixer，使用 `artist_chain` | 拆成多个普通 job |

## 批量自检

批量里每个 job 仍需要自己的 prompt/args 自检。只在 job 需要时调用构图计划或 tag 校验；不要为了速度跳过身份、工作流字段或冲突检查。

## Artist Mixer 批量

- Artist Mixer 是一个 workflow + 一个 `artist_chain`，不是 N 个普通画师 job。
- 用户说“分别用 A+B、C+D 两组融合各出 N 张”：这是 2 组 Artist Mixer job，每组自己的 `artist_chain`。
- `combine_mode`、`fusion_mode`、`artist_mixer_strength` 等参数按 job 生效；只有用户明确指定时才覆盖 workflow 默认。

## 批量约束

- `steps`：默认 30；只有用户要求高质量、复杂背景、多人互动或强光影时用 40。
- 脚本：批量提交脚本只读取并提交已确认 args，不能自行决定 prompt、steps、画布、模型或 `filename_prefix`。
- 输出：向用户返回每张图的编号、简短主题、`prompt_id`、args 路径；不要倾倒完整 prompt 或原始 JSON。
- 随机：不要循环调用 `anima-random-gen` N 次制造随机批量；随机批量应先抽候选池，再由 random-gen/animatool 产出 K 个已选方案并复核。
