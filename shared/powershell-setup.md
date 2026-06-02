# PowerShell 共享配置

供 `comfyui-anima-master` 和 `comfyui-manager` 引用。只记录执行时必须复用的 PowerShell 写法。

## 工作目录

```powershell
Set-Location -LiteralPath "<comfyui-manager skill 目录>/workspace"
$WORKSPACE = (Get-Location).Path
$RUNTIME = Join-Path (Resolve-Path (Join-Path $WORKSPACE "../..")).Path "runtime/comfyui-manager"
$env:COMFYUI_MANAGER_RUNTIME_DIR = $RUNTIME
New-Item -ItemType Directory -Force -Path $RUNTIME | Out-Null
```

## 写无 BOM UTF-8 JSON

Windows PowerShell 5.x 的 `Set-Content -Encoding utf8` 会写入 BOM，容易破坏 CLI JSON 解析。写 args 文件必须用这个函数：

```powershell
function Write-JsonForCli($Path, $Value) {
  $json = $Value | ConvertTo-Json -Depth 30
  $fullPath = [System.IO.Path]::GetFullPath($Path)
  [System.IO.File]::WriteAllText($fullPath, $json, [System.Text.UTF8Encoding]::new($false))
}
```

## 默认提交

```powershell
Write-JsonForCli (Join-Path $RUNTIME "args/args_anima.json") $argsObj
Push-Location "$WORKSPACE"
node ./run_workflow_args.js submit local/anima-txt2img-aesthetic-lora "$RUNTIME/args/args_anima.json"
Pop-Location
```

只有用户明确要求等待结果时，才把 `submit` 换成 `run`。
