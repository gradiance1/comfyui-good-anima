# 解析 WORKSPACE 目录和 RUNTIME 路径
function Test-ComfyManagerWorkspace($Path) {
  return (Test-Path (Join-Path $Path "config.json")) -and (Test-Path (Join-Path $Path "data"))
}

function Find-ComfyManagerWorkspaceFromSkills($Start) {
  $cursor = (Resolve-Path $Start).Path
  while ($cursor) {
    $skillsDirs = Get-ChildItem -LiteralPath $cursor -Directory -Recurse -Depth 2 -Filter "skills" -ErrorAction SilentlyContinue
    foreach ($skillsDir in $skillsDirs) {
      $candidate = Join-Path $skillsDir.FullName "comfyui-manager\workspace"
      if (Test-ComfyManagerWorkspace $candidate) { return (Resolve-Path $candidate).Path }
      $nestedCandidate = Join-Path $skillsDir.FullName "comfyui-good-anima\comfyui-manager\workspace"
      if (Test-ComfyManagerWorkspace $nestedCandidate) { return (Resolve-Path $nestedCandidate).Path }
    }
    $flatCandidate = Join-Path $cursor "comfyui-manager\workspace"
    if (Test-ComfyManagerWorkspace $flatCandidate) { return (Resolve-Path $flatCandidate).Path }
    $bundleCandidate = Join-Path $cursor "comfyui-good-anima\comfyui-manager\workspace"
    if (Test-ComfyManagerWorkspace $bundleCandidate) { return (Resolve-Path $bundleCandidate).Path }
    $parent = Split-Path $cursor -Parent
    if ($parent -eq $cursor) { break }
    $cursor = $parent
  }
  return $null
}

$WORKSPACE = if ($env:COMFYUI_MANAGER_WORKSPACE) {
  $env:COMFYUI_MANAGER_WORKSPACE
} elseif (Test-ComfyManagerWorkspace ".\workspace") {
  (Resolve-Path ".\workspace").Path
} elseif (Test-ComfyManagerWorkspace ".") {
  (Get-Location).Path
} elseif ($found = Find-ComfyManagerWorkspaceFromSkills ".") {
  $found
} else {
  throw "Set COMFYUI_MANAGER_WORKSPACE or run from a directory that can discover skills/comfyui-manager"
}

$RUNTIME = if ($env:COMFYUI_MANAGER_RUNTIME_DIR) {
  $env:COMFYUI_MANAGER_RUNTIME_DIR
} elseif ($env:SKILL_RUNTIME_ROOT) {
  Join-Path $env:SKILL_RUNTIME_ROOT "comfyui-manager"
} else {
  try {
    $config = Get-Content -LiteralPath (Join-Path $WORKSPACE "config.json") -Raw | ConvertFrom-Json
    $outputDir = $config.servers[0].output_dir
    if ($outputDir) {
      $resolvedOutput = [System.IO.Path]::GetFullPath((Join-Path $WORKSPACE $outputDir))
      if ((Split-Path $resolvedOutput -Parent) -eq (Resolve-Path $WORKSPACE).Path) {
        Join-Path (Resolve-Path (Join-Path $WORKSPACE "..\..")).Path "runtime\comfyui-manager"
      } else {
        Split-Path $resolvedOutput -Parent
      }
    } else {
      Join-Path (Resolve-Path (Join-Path $WORKSPACE "..\..")).Path "runtime\comfyui-manager"
    }
  } catch {
    Join-Path (Resolve-Path (Join-Path $WORKSPACE "..\..")).Path "runtime\comfyui-manager"
  }
}
New-Item -ItemType Directory -Force -Path $RUNTIME | Out-Null
