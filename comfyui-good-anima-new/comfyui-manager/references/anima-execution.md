# Anima Workflow 执行

> ⚠️ 核心规则已回流至 SKILL.md。本文件仅提供扩展细节与边界情况。如内容与 SKILL.md 冲突，以 SKILL.md 为准。

只在执行已确认 Anima args、处理批量提交、缓存结果或选择 Anima workflow 时读取本文件。

## Args 格式

Args 文件必须是纯参数对象：

```json
{
  "prompt_11": "...positive...",
  "prompt_12": "...negative...",
  "width": 1024,
  "height": 1536,
  "batch_size": 1,
  "steps": 30,
  "rtx_vsr_quality": "ULTRA",
  "filename_prefix": "anima/%year%-%month%-%day%/anima_base_v1_0-artist_tag-character_tag"
}
```

## Workflow 选择

- 默认：`local/anima-txt2img-aesthetic-lora`
- Artist Mixer：`local/anima-txt2img-aesthetic-lora-artist-mixer`，仅在 args 已包含 `artist_chain` 且需求明确为融合/混合/artist mixer 时使用。
- 基础版：`local/anima-txt2img-base`，仅在用户明确要求基础版、禁用 LoRA、对比测试或排障时使用。

## 输出命名

`filename_prefix` 必须使用：

```text
anima/%year%-%month%-%day%/<model_tag>-<artist_tag>-<character_tag>
```

规则：

- `model_tag` 来自 UNet 模型名，去掉扩展名后转安全名。
- 默认工作流的 `artist_tag` 来自单画师标签，去掉 `@`。
- Artist Mixer 的 `artist_tag` 来自 `artist_chain`，按主次取 1-3 个画师名拼接。
- `character_tag` 来自主要角色标签。
- 三者都转小写，并把空格或特殊符号替换成 `_`。
- 不要手写序号，ComfyUI 会自动追加。

## 批量执行

批量策略由 `comfyui-animatool` 决定，本 skill 只执行已确认 args。

| 需求                             | 执行方式                                       |
| -------------------------------- | ---------------------------------------------- |
| 同一个 prompt 出 N 张变体        | 设置 `batch_size=N`，只提交 1 个 workflow      |
| 同一个 prompt 分几批出           | 提交多个 job，每个 job 可设置 `batch_size`     |
| 每张图不同 prompt / 不同随机 tag | 每个 prompt 单独构造 args 并 `submit` 一个 job |

## PowerShell JSON 写入

JSON 编码规则与 `Write-JsonForCli` 函数见 `comfyui-manager/SKILL.md` 的「PowerShell 与 JSON 编码」章节。批量提交时确保已有该函数可用。

多 prompt 推荐非阻塞提交，再用 `status` 汇总。脚本必须记录每个 job 的 args 文件和 `prompt_id`，不能只调用 `submit` 后结束：

```powershell
cd "$WORKSPACE"
$RUNTIME = if ($env:COMFYUI_MANAGER_RUNTIME_DIR) {
  $env:COMFYUI_MANAGER_RUNTIME_DIR
} elseif ($env:SKILL_RUNTIME_ROOT) {
  Join-Path $env:SKILL_RUNTIME_ROOT "comfyui-manager"
} else {
  $config = Get-Content -LiteralPath (Join-Path $WORKSPACE "config.json") -Raw | ConvertFrom-Json
  $outputDir = $config.servers[0].output_dir
  if ($outputDir) {
    Split-Path ([System.IO.Path]::GetFullPath((Join-Path $WORKSPACE $outputDir))) -Parent
  } else {
    Join-Path (Resolve-Path (Join-Path $WORKSPACE "..\..")).Path "runtime\comfyui-manager"
  }
}
New-Item -ItemType Directory -Force -Path $RUNTIME | Out-Null
$jobs = Get-Content -LiteralPath .\batch_jobs.json -Raw | ConvertFrom-Json
$ids = @()
foreach ($job in $jobs) {
  $argsDir = Join-Path $RUNTIME "batch_args"
  New-Item -ItemType Directory -Force -Path $argsDir | Out-Null
  $argsFile = Join-Path $argsDir "$($job.id).json"
  Write-JsonForCli $argsFile $job.args
  $result = node ./run_workflow_args.js submit local/anima-txt2img-aesthetic-lora $argsFile | ConvertFrom-Json
  $ids += $result.prompt_id
}
$ids
```

## 本地缓存

每次成功执行 Anima 生图后，除了返回 `outputs[].local_path`，必须在 `$RUNTIME/cache/anima/YYYY-MM-DD/` 保留缓存元数据或可访问副本，供远程云端客户端复用。`$RUNTIME` 优先来自 `COMFYUI_MANAGER_RUNTIME_DIR`，其次是 `SKILL_RUNTIME_ROOT/comfyui-manager`，再其次从 `workspace/config.json` 的 `output_dir` 父目录推导；不要写死平台特定的环境变量名。

缓存图片优先使用 NTFS hardlink 指向正式输出，避免 `outputs` 和 `cache` 双倍占用；硬链接失败时才复制。manifest 必须记录 `cache_mode`。

`workspace/outputs` 和 `workspace/cache` 应作为 Windows junction 指向 `$RUNTIME/outputs` 与 `$RUNTIME/cache`。这样 GUI 客户端可继续从 workspace 路径读取本地图像，但物理文件只保留在 runtime 中。

缓存日期优先来自输出的 `subfolder` 或 `source_local_path` 中的 `anima/YYYY-MM-DD`，其次才使用本地时区日期。不要用 UTC `toISOString().slice(0, 10)`。

缓存内容：

- 输出图片副本
- 最终 args JSON
- manifest JSON

manifest 至少记录：

- `workflow_id`
- `prompt_id`
- `source_local_path`
- `cache_local_path`
- `args_path`
- `filename_prefix`
- `created_at`
- `cache_mode`

缓存失败不应伪装生图失败，但必须在结果中说明原因。

## 提交脚本要求

- 串行/并行提交脚本必须记录每个 job 的 args 文件和 `prompt_id`。
- 任务完成后用 `comfyui-skill --json --dir "$WORKSPACE" status <prompt_id>` 读取 `outputs[].local_path`。
- `run_workflow_args.js` 会把 CLI 写入 `workspace/data/*/*/history` 的 history JSON 迁到 `$RUNTIME/history/<workflow_name>/`；不要再手动把 history 放回 skill 目录。
- `cache_anima_outputs.js` 优先读取 `$RUNTIME/history/<workflow_name>/` 中的本地 history，并从 `outputs[].local_path` 重建缓存；只有本地 history 不存在时才 fallback 到 server history。非默认 Anima workflow 必须传 `--workflow-id <workflow_id>`，与执行时的 workflow id 保持一致。
- 不要把 ComfyUI 队列返回的 `prompt_id` 传给 `history show`；`history show` 使用 workflow id + run_id。
- 如果脚本只入队不等待完成，必须同时生成后处理脚本或清单，说明如何根据 `prompt_id` 补建缓存。
- 远程 GUI 或云端客户端展示图片时，优先读取 runtime 缓存副本。
