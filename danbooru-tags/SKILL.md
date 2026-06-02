---
name: danbooru-tags
description: |
  当 Anima 生图或独立查询需要验证 Danbooru 锚点时加载：画师、角色、作品/IP、外观、服装、道具、姿势、表情、场景或随机候选。
  不用于决定构图、撰写完整 prompt 或执行 ComfyUI workflow。
---

# Danbooru Tags 查询

本 skill 只做数据检索和确认。是否生图、如何构图、如何组装 prompt，交给 `comfyui-anima-master` / `comfyui-animatool`。

## 权威边界

- 默认数据源是 Anima CSV / 本地索引。
- Artist tag 必须来自 artist category，并保留 `@`。
- Character / series / general tag 不带 `@`，不能当画师。
- 角色查询只返回 tag、aliases、count；aliases 不是外观设定。
- 本 skill 不做网络别名解析；中文名、外号、社交账号、CP 简称或本地 miss 时，先回到 `comfyui-animatool` 做 canonical 解析，再来校验。
- `confirmed_tags` 仍需按用户意图筛选；`candidate_tags` 不能批量塞进 prompt。
- 查不到的复合概念交给 `nltags`；不要伪造 Danbooru tag。
- 抽象构图、光源方向、情绪叙事、镜头关系通常不是检索任务。
- Rust CLI 不可用、非 0、非 JSON、字段缺失时停止报告，不切换旧实现。

## CLI

从当前 `danbooru-tags` skill 目录执行：

```powershell
Set-Location -LiteralPath "<current danbooru-tags skill directory>"
$exe = if ($env:OS -eq "Windows_NT") { "danbooru-tags.exe" } else { "danbooru-tags" }
$cli = Join-Path "bin" $exe
```

单查示例：

```powershell
& $cli --group artist --prefix "@mignon" --limit 5 --for-prompt --json --compact
& $cli --group character --keyword "hakurei reimu" --limit 5 --for-prompt --json --compact
```

批量校验优先用 `--batch-file`，JSON 写 UTF-8 without BOM：

```powershell
$batch = @{
  queries = @(
    @{ id = "character"; group = "character"; keyword = "kanade tachibana"; limit = 5 },
    @{ id = "series"; group = "series"; keyword = "angel beats"; limit = 5 },
    @{ id = "artist"; group = "artist"; prefix = "@mignon"; limit = 5 }
  )
}
$json = $batch | ConvertTo-Json -Depth 20
$file = Join-Path $env:TEMP "danbooru_batch.json"
[System.IO.File]::WriteAllText($file, $json, [System.Text.UTF8Encoding]::new($false))
& $cli --batch-file $file --batch-workers 8 --for-prompt --json --compact
```

## 什么时候查

- 用户指定或任务依赖准确的角色、作品/IP、画师。
- 用户给出已解析的中文/俗称/别名候选，需要确认 canonical tag。
- 关键外观、服装、道具、姿势必须稳定落到 Danbooru tag。
- 随机候选需要来自有效 tag 池。

不必查：

- 模型常识足够的普通自然语言描述。
- 光从左来、前景/中景/背景、脸部清晰、故事关系等构图控制。
- 每一个普通形容词。

## 分组

| 分组 | 覆盖内容 |
| --- | --- |
| `artist` | 画师，保留 `@` |
| `character` | 角色 |
| `series` / `ip` / `copyright` | 作品/IP |
| `appearance` / `body` | 发色、瞳色、发型、耳、角、体型 |
| `expression` | 表情 |
| `pose` / `action` | 姿势、动作 |
| `clothing` / `outfit` | 服装 |
| `accessory` / `prop` | 配饰、道具 |
| `scene` / `background` | 场景、天气、背景 tag |
| `lighting` | 稳定 Danbooru 光影 tag；不是抽象光位设计 |
| `meta` | highres 等元信息 |

## 随机

- `--random N --json`: 候选列表。
- `--random N --group <group> --json`: 指定 group 候选。
- `--random N --for-prompt --json --compact`: 生图回填模式，通常只返回 1 个 artist。
- `N` 是候选规模；普通建议 10-50，用户要求大量候选时可更高。不要循环调用来模拟候选池。

## 输出读取

`--for-prompt --json --compact` 关注：

- `confirmed_tags`: 可回填但仍需筛选。
- `candidate_tags`: 候选，必须人工/模型按意图筛选。
- `missing`: 交给 `nltags`。

详细批量策略和维护说明见 `references/query-patterns.md`。
