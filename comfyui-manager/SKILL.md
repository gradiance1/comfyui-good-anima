---
name: comfyui-manager
description: |
  当需要执行已组装好的 ComfyUI workflow、提交/查询队列、检查模型/节点依赖、查看服务器状态或排查执行错误时加载。
  不用于决定画面内容、画师、构图或 prompt 策略；这些交给 comfyui-anima-master / comfyui-animatool。
---

# ComfyUI Manager

本 skill 只负责执行和排障。不要自动生成 prompt、steps、画布、模型选择或文件名；这些必须来自上游 skill 已经组装好的 args。

## 工作目录

所有 `comfyui-skill` 命令都从 `comfyui-manager/workspace` 执行：

```powershell
Set-Location -LiteralPath "<当前 comfyui-manager skill 目录>/workspace"
$WORKSPACE = (Get-Location).Path
$RUNTIME = Join-Path (Resolve-Path (Join-Path $WORKSPACE "../..")).Path "runtime/comfyui-manager"
$env:COMFYUI_MANAGER_RUNTIME_DIR = $RUNTIME
New-Item -ItemType Directory -Force -Path $RUNTIME | Out-Null
```

统一命令前缀：`comfyui-skill --json --dir "$WORKSPACE"`。运行产物写入 `$RUNTIME`，不要写回 skill 目录。

无法确定 workspace 时停止，并说明：`无法确定 comfyui-manager/workspace 目录`。

写 JSON 文件必须使用无 BOM UTF-8；PowerShell 写法见 `shared/powershell-setup.md`。

## 可用工作流

- `local/anima-txt2img-aesthetic-lora`：默认双 LoRA 文生图。
- `local/anima-txt2img-aesthetic-lora-artist-mixer`：仅用于用户明确要求多画师融合 / artist_chain。
- `local/anima-txt2img-base`：裸模型、禁用 LoRA、对比测试或排障。

不要根据文件名猜 workflow；用上游传来的 workflow id。

## 执行模式

默认不要用阻塞 `run`。

- 用户只要求生成图片：用 `submit`，返回 `prompt_id` 后停止。
- 用户明确要求等待、看结果、确认完成：才用 `run` 或显式 `status` 查询。
- 多个不同 prompt / 不同画师 / 不同构图：每个 args 单独 `submit`，返回 manifest。
- 同一个 prompt 要 N 个变体：设置 `batch_size=N`，提交 1 个 workflow。

`submit` 是非阻塞。提交后不要 `Start-Sleep`、不要轮询、不要自动缓存，除非用户明确要求看结果。

## Args 格式

Args 文件必须是纯参数对象，不包 workflow 外壳。标准工作流要求 `prompt_11` 和 `prompt_12` 非空。

```json
{
  "prompt_11": "...positive...",
  "prompt_12": "...negative...",
  "width": 1024,
  "height": 1536,
  "batch_size": 1,
  "steps": 30,
  "rtx_vsr_quality": "ULTRA",
  "filename_prefix": "anima/%year%-%month%-%day%/anima_base_1_masterpiece_v51-none-character"
}
```

参数边界：

- 普通画师写在 `prompt_11`，格式 `@artist name`。
- `artist_chain` 只给 Artist Mixer workflow，且不带 `@`。
- 默认不传 `rtx_vsr_scale`；2x 倍率在 workflow 固定。
- `rtx_vsr_quality` 只能是 `LOW / MEDIUM / HIGH / ULTRA`。
- FLSampler、TeaCache、AnimaBoosterLoader、Artist Mixer 高级字段只有用户明确调参或排障时传。
- `teacache_version` 必须是 `v1 (Legacy Fast)` 或 `v2 (Standard Precise)`，不能写短 `v1` / `v2`。

## 默认提交

```powershell
Push-Location "$WORKSPACE"
$result = node ./run_workflow_args.js submit local/anima-txt2img-aesthetic-lora "$RUNTIME/args/args_anima.json" | ConvertFrom-Json
Pop-Location
```

返回给用户：`prompt_id`、args 路径、`filename_prefix`、简短 prompt/构图摘要。不要主动查询完成状态。

## 用户要求等待结果时

```powershell
Push-Location "$WORKSPACE"
node ./run_workflow_args.js run local/anima-txt2img-aesthetic-lora "$RUNTIME/args/args_anima.json"
Pop-Location
```

`run_workflow_args.js run` 会先 submit 再轮询；只有用户明确等待时使用。

## 验证

首次使用、改 workflow/schema、改节点参数或排障前先验证：

```powershell
node ./run_workflow_args.js validate local/anima-txt2img-aesthetic-lora "$RUNTIME/args/args_anima.json"
```

验证失败时停止，不要继续提交批量任务。

## 本地脚本边界

`run_workflow_args.js`：项目默认执行入口，负责读取 args 文件、处理 BOM、调用 `comfyui-skill`。不要改用内联 `--args`。

`cache_anima_outputs.js`：用户要求查看图片、补缓存、批量任务完成后整理输出时使用。不要在 `submit` 后自动调用。

`runtime_utils.js`：共享 runtime / JSON / BOM 工具。新脚本不要重复实现路径解析。

## 排障

连接失败、`connection refused`、`timeout`、端口错误：

```powershell
comfyui-skill --json --dir "$WORKSPACE" server status
```

`400`、`Bad Request`、`invalid prompt`：

1. 先运行 `validate`。
2. 再运行 `deps check`。
3. 检查错误 JSON 里的 `node_errors`。
4. 核对 enum：尤其 `teacache_version`、`rtx_vsr_quality`。
5. 核对核心字段：`prompt_11`、`prompt_12`、`width`、`height`、`batch_size`、`steps`。

缺模型或 `value_not_in_list`：

```powershell
comfyui-skill --json --dir "$WORKSPACE" models list diffusion_models
comfyui-skill --json --dir "$WORKSPACE" models list text_encoders
comfyui-skill --json --dir "$WORKSPACE" models list vae
comfyui-skill --json --dir "$WORKSPACE" models list loras
```

需要匹配的 workflow 节点：

- `AnimaBoosterLoader.model_name`
- `CLIPLoader.clip_name`
- `VAELoader.vae_name`
- `LoraLoaderModelOnly.lora_name`

缺自定义节点或依赖：

```powershell
comfyui-skill --json --dir "$WORKSPACE" deps check local/anima-txt2img-aesthetic-lora
```

不要猜路径或手工改安装目录。

## 缓存输出

只有用户要求看图、补缓存或整理批量结果时运行：

```powershell
node cache_anima_outputs.js --workflow-id local/anima-txt2img-aesthetic-lora
```

批量任务使用 manifest：

```powershell
node cache_anima_outputs.js --manifest "$RUNTIME/manifests/batch.json"
```

不要把 ComfyUI 队列 `prompt_id` 传给 `history show`；需要历史时使用 workflow id + run_id，或使用本地 runtime history。
