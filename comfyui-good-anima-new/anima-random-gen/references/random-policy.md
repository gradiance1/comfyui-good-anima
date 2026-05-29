# Anima 随机策略

> ⚠️ 核心规则已回流至 SKILL.md。本文件仅提供扩展细节与边界情况。如内容与 SKILL.md 冲突，以 SKILL.md 为准。

## 参数默认值

- 质量前缀：`masterpiece, very aesthetic, best quality, score_9, score_8, highres, absurdres, newest, year 2025, [safe/sensitive/nsfw/explicit]`
- `steps=30`
- `cfg=4.5`
- `sampler_name=dpmpp_2m_sde_gpu`
- `scheduler=beta57`
- 默认 1 个画师，最多 2 个。
- 默认本地执行链路包含 TeaCache 与 RTX VSR 2x 放大。

## 画布

画布尺寸选择见 `anima-composition-director/SKILL.md` 的「Fast canvas choices」表。不要随机图固定套默认竖图；默认不主动推荐任一边超过 1536。

## 完整画面约束

- `environment` 放 2-6 个已确认的场景/光影 tag。
- `nltags` 补动作、空间、光影、材质和氛围，且不能和 tags 冲突。
- 背景不是主体时，用轻微背景虚化或景深分离主体。
- 单人、头像、半身或角色表现图必须保护脸部可读性。

## 脚本入口

当前目录包含随机辅助脚本：

```powershell
python .\random_generator.py --count 5
python .\random_generator.py --artist-count 2
python .\random_generator.py --safe sensitive
python .\random_generator.py --json
```

脚本输出仍需交给 `comfyui-animatool` 复核，不要直接执行 ComfyUI。

## 权重规则

- 默认不要加权。
- 只有用户明确要求强化/弱化，或某元素多次不稳定时才加权。
- 从 `(tag:2)` 开始测试。
- 不要给角色名、画师名、安全标签和整段 `nltags` 默认加权。

## 禁止组合

- `lying` + `sitting`
- `open mouth` + `closed mouth`
- `close-up` + `full body`
- 单人图但使用多人互动描述
- 服装和裸体状态冲突
