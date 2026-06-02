# ComfyUI 运维参考

仅在管理服务器、模型、工作流、节点、队列、依赖、日志，或执行非 Anima 工作流时读取。普通 Anima 生图不要加载本文件。

## 命令约定

- 工作流 ID 使用 `provider/name`，例如 `local/anima-txt2img-aesthetic-lora`。
- 默认加 `--json --dir "$WORKSPACE"`，按 JSON 字段判断结果，不解析终端表格。
- 非 0 退出码表示失败；脚本必须保留 stderr。
- 优先使用 `run_workflow_args.js` + args 文件，避免内联 `--args` 被 PowerShell 引号、反斜杠、换行破坏。
- 只有无中文、无换行、无反斜杠的临时测试才考虑内联 `--args`。

## 服务器

```powershell
comfyui-skill --json --dir "$WORKSPACE" server status
comfyui-skill --json --dir "$WORKSPACE" server stats
comfyui-skill --json --dir "$WORKSPACE" server stats --all
comfyui-skill --json --dir "$WORKSPACE" server list
comfyui-skill --json --dir "$WORKSPACE" server add --id <server_id> --url <url>
comfyui-skill --json --dir "$WORKSPACE" server enable <server_id>
comfyui-skill --json --dir "$WORKSPACE" server disable <server_id>
comfyui-skill --json --dir "$WORKSPACE" server remove <server_id>
```

## 模型

```powershell
comfyui-skill --json --dir "$WORKSPACE" models list
comfyui-skill --json --dir "$WORKSPACE" models list diffusion_models
comfyui-skill --json --dir "$WORKSPACE" models list text_encoders
comfyui-skill --json --dir "$WORKSPACE" models list vae
comfyui-skill --json --dir "$WORKSPACE" models list loras
comfyui-skill --json --dir "$WORKSPACE" models list checkpoints
comfyui-skill --json --dir "$WORKSPACE" models list controlnet
```

显存处理：

```powershell
comfyui-skill --dir "$WORKSPACE" free
comfyui-skill --dir "$WORKSPACE" free --models
comfyui-skill --dir "$WORKSPACE" free --memory
```

## 工作流管理

```powershell
comfyui-skill --json --dir "$WORKSPACE" list
comfyui-skill --json --dir "$WORKSPACE" info local/workflow_id
comfyui-skill --json --dir "$WORKSPACE" workflow import "<path-to-workflow.json>" --check-deps
comfyui-skill --json --dir "$WORKSPACE" workflow import --from-server --preview
comfyui-skill --json --dir "$WORKSPACE" workflow import --from-server --name <keyword>
comfyui-skill --json --dir "$WORKSPACE" workflow enable local/workflow_id
comfyui-skill --json --dir "$WORKSPACE" workflow disable local/workflow_id
comfyui-skill --json --dir "$WORKSPACE" workflow delete local/workflow_id
```

模板与配置：

```powershell
comfyui-skill --json --dir "$WORKSPACE" templates list
comfyui-skill --json --dir "$WORKSPACE" templates subgraphs
comfyui-skill --json --dir "$WORKSPACE" config export --output "<backup.zip>"
comfyui-skill --json --dir "$WORKSPACE" config import "<backup.zip>"
comfyui-skill --json --dir "$WORKSPACE" config import "<backup.zip>" --dry-run
```

## 执行与队列

普通提交默认用 `submit`：

```powershell
cd "$WORKSPACE"
node ./run_workflow_args.js submit local/workflow_id ./args.json
```

等待结果才用 `run`：

```powershell
node ./run_workflow_args.js run local/workflow_id ./args.json
```

验证和队列：

```powershell
node ./run_workflow_args.js validate local/workflow_id ./args.json
comfyui-skill --json --dir "$WORKSPACE" status <prompt_id>
comfyui-skill --json --dir "$WORKSPACE" cancel <prompt_id>
comfyui-skill --json --dir "$WORKSPACE" queue list
comfyui-skill --json --dir "$WORKSPACE" queue clear
comfyui-skill --json --dir "$WORKSPACE" queue delete <prompt_id>
```

## 上传

```powershell
comfyui-skill --json --dir "$WORKSPACE" upload "<path-to-image.png>"
comfyui-skill --json --dir "$WORKSPACE" upload "<path-to-mask.png>" --mask
comfyui-skill --json --dir "$WORKSPACE" upload --from-output <prompt_id>
```

## 节点、依赖、日志

```powershell
comfyui-skill --json --dir "$WORKSPACE" nodes list
comfyui-skill --json --dir "$WORKSPACE" nodes info <node_class_name>
comfyui-skill --json --dir "$WORKSPACE" nodes search <keyword>
comfyui-skill --json --dir "$WORKSPACE" deps check local/workflow_id
comfyui-skill --json --dir "$WORKSPACE" deps install local/workflow_id --all
comfyui-skill --json --dir "$WORKSPACE" deps install local/workflow_id --repos '["repo-url"]'
comfyui-skill --json --dir "$WORKSPACE" deps install local/workflow_id --models
comfyui-skill --json --dir "$WORKSPACE" logs show
comfyui-skill --json --dir "$WORKSPACE" history list local/workflow_id
comfyui-skill --json --dir "$WORKSPACE" history show local/workflow_id <run_id>
```

## 任务历史

```powershell
comfyui-skill --json --dir "$WORKSPACE" jobs list
comfyui-skill --json --dir "$WORKSPACE" jobs list --status <status>
comfyui-skill --json --dir "$WORKSPACE" jobs show <job_id>
```

## 快速排障

```powershell
comfyui-skill --json --dir "$WORKSPACE" server status
comfyui-skill --json --dir "$WORKSPACE" deps check local/workflow_id
comfyui-skill --json --dir "$WORKSPACE" info local/workflow_id
comfyui-skill --json --dir "$WORKSPACE" models list diffusion_models
comfyui-skill --json --dir "$WORKSPACE" models list text_encoders
comfyui-skill --json --dir "$WORKSPACE" models list vae
comfyui-skill --json --dir "$WORKSPACE" models list loras
```

## 协作场景

- 显存满：先 `server stats`，再 `free --models` 或 `free --memory`。
- 列 LoRA：用 `models list loras`；是否写入 prompt 仍由生图 skill 决定。
- 导入非 Anima workflow：`workflow import "<path>" --check-deps` 后再 `deps check/install`。
- 运行非 Anima workflow：先 `info` / `deps check`，再按用户要求选 `submit` 或 `run`。

## 后处理

只有用户要求看图、检查完成或整理批量输出时才查询状态和缓存。不要把下面流程接在普通 `submit` 后自动执行。

```powershell
$manifest = Get-Content -LiteralPath (Join-Path $RUNTIME "batch_manifest.json") -Raw | ConvertFrom-Json
$failed = @()
foreach ($job in $manifest) {
  do {
    Start-Sleep -Seconds 10
    $status = comfyui-skill --json --dir "$WORKSPACE" status $job.prompt_id | ConvertFrom-Json
    $state = if ($status.data.status) { $status.data.status } else { $status.status }
  } while ($state -notin @("completed","success","error","failed","cancelled","canceled"))
  if ($state -notin @("completed","success")) { $failed += $job.prompt_id }
}
if ($failed.Count -gt 0) { throw "jobs failed: $($failed -join ', ')" }
node ./cache_anima_outputs.js --workflow-id $manifest[0].workflow_id --manifest (Join-Path $RUNTIME "batch_manifest.json")
```

轮询间隔建议 10-30 秒。缓存目录是 `$RUNTIME/cache/anima/YYYY-MM-DD/`。
