# ComfyUI 运维命令

> ⚠️ 核心规则已回流至 SKILL.md。本文件仅提供扩展细节与边界情况。如内容与 SKILL.md 冲突，以 SKILL.md 为准。

只在用户要求管理服务器、模型、workflow、节点、队列、依赖、日志，或执行已准备好的非 Anima workflow 时读取本文件。

## 命令约定

- Workflow ID 使用 `provider/name`，例如 `local/anima-txt2img-aesthetic-lora`。
- 默认使用 `--json`，输出通常是 JSON 对象；先检查 `success` / `error` / `data` / `outputs` / `jobs` 字段，不要只看文本。
- 执行 workflow 时优先用 `run_workflow_args.js` 读取 args 文件，避免 PowerShell 内联 `--args` 破坏引号、反斜杠、换行和空格。
- 只有非常简单、无中文、无换行、无反斜杠的临时测试，才考虑官方 `--args '{"prompt":"..."}'` 形式。
- 能确认 PowerShell 7.x / `pwsh` 可用时，示例使用 `./script.js` 和正斜杠路径；只有确认是 Windows PowerShell 5.x 时才用 BOM fallback 写法。

常见 JSON 形状：

```json
{
  "success": true,
  "data": {},
  "outputs": [],
  "jobs": []
}
```

## 服务器

```powershell
comfyui-skill --json --dir "$WORKSPACE" server status
comfyui-skill --json --dir "$WORKSPACE" server stats
comfyui-skill --json --dir "$WORKSPACE" server list
```

## 模型

```powershell
comfyui-skill --json --dir "$WORKSPACE" models list
comfyui-skill --json --dir "$WORKSPACE" models list checkpoints
comfyui-skill --json --dir "$WORKSPACE" models list loras
comfyui-skill --json --dir "$WORKSPACE" models list vae
comfyui-skill --json --dir "$WORKSPACE" models list controlnet
comfyui-skill --json --dir "$WORKSPACE" models list diffusion_models
comfyui-skill --json --dir "$WORKSPACE" models list text_encoders
```

释放资源：

```powershell
comfyui-skill --dir "$WORKSPACE" free
comfyui-skill --dir "$WORKSPACE" free --models
comfyui-skill --dir "$WORKSPACE" free --memory
```

## Workflow

```powershell
comfyui-skill --json --dir "$WORKSPACE" list
comfyui-skill --json --dir "$WORKSPACE" info local/workflow_id
comfyui-skill --json --dir "$WORKSPACE" workflow import "<path-to-workflow.json>" --check-deps
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
```

## 执行与队列

```powershell
cd "$WORKSPACE"
node ./run_workflow_args.js run local/workflow_id ./args.json
node ./run_workflow_args.js submit local/workflow_id ./args.json
comfyui-skill --json --dir "$WORKSPACE" status <prompt_id>
comfyui-skill --json --dir "$WORKSPACE" cancel <prompt_id>
comfyui-skill --json --dir "$WORKSPACE" queue list
comfyui-skill --json --dir "$WORKSPACE" queue clear
comfyui-skill --json --dir "$WORKSPACE" queue delete <prompt_id>
```

## 上传与链式执行

```powershell
comfyui-skill --json --dir "$WORKSPACE" upload "<path-to-image.png>"
comfyui-skill --json --dir "$WORKSPACE" upload --from-output <prompt_id>
```

## 节点、依赖、日志

```powershell
comfyui-skill --json --dir "$WORKSPACE" nodes list
comfyui-skill --json --dir "$WORKSPACE" nodes info <node_class_name>
comfyui-skill --json --dir "$WORKSPACE" nodes search <keyword>
comfyui-skill --json --dir "$WORKSPACE" deps check local/workflow_id
comfyui-skill --json --dir "$WORKSPACE" deps install local/workflow_id --all
comfyui-skill --json --dir "$WORKSPACE" logs show
comfyui-skill --json --dir "$WORKSPACE" history list local/workflow_id
comfyui-skill --json --dir "$WORKSPACE" history show local/workflow_id <run_id>
```

## 协作示例

- 用户说“显存满了/清一下”：先 `server stats`，再 `free --models` 或 `free --memory`，不要改 prompt。
- 用户说“换 LoRA/看有哪些 LoRA”：用 `models list loras`；选择和 prompt 策略仍交给对应生图 skill。
- 用户说“导入这个 FLUX/SDXL workflow”：用 `workflow import "<path-to-workflow.json>" --check-deps`，再按提示执行 `deps check/install`。
- 用户说“跑这个 SDXL/FLUX workflow”：确认 workflow 已导入且 args 已准备好；先 `info local/workflow_id` / `deps check local/workflow_id`，再用 `node ./run_workflow_args.js run|submit local/workflow_id ./args.json` 执行。
