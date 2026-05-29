# 解析 DANBOORU_TAGS_DIR 和 RUNTIME 路径
function Test-DanbooruTagsDir($Path) {
  return (Test-Path (Join-Path $Path "SKILL.md")) -and (
    (Test-Path (Join-Path $Path "tags_index.sqlite")) -or
    (Test-Path (Join-Path $Path "anima-1.0.csv"))
  )
}

function Test-DanbooruTagsCli($Path) {
  return Test-Path (Join-Path $Path "bin/danbooru-tags.exe")
}

function Find-DanbooruTagsDirFromSkills($Start) {
  $cursor = (Resolve-Path $Start).Path
  while ($cursor) {
    $skillsDirs = Get-ChildItem -LiteralPath $cursor -Directory -Recurse -Depth 2 -Filter "skills" -ErrorAction SilentlyContinue
    foreach ($skillsDir in $skillsDirs) {
      $candidate = Join-Path $skillsDir.FullName "danbooru-tags"
      if (Test-DanbooruTagsDir $candidate) { return (Resolve-Path $candidate).Path }
      $nestedCandidate = Join-Path $skillsDir.FullName "comfyui-good-anima\danbooru-tags"
      if (Test-DanbooruTagsDir $nestedCandidate) { return (Resolve-Path $nestedCandidate).Path }
    }
    $flatCandidate = Join-Path $cursor "danbooru-tags"
    if (Test-DanbooruTagsDir $flatCandidate) { return (Resolve-Path $flatCandidate).Path }
    $bundleCandidate = Join-Path $cursor "comfyui-good-anima\danbooru-tags"
    if (Test-DanbooruTagsDir $bundleCandidate) { return (Resolve-Path $bundleCandidate).Path }
    $parent = Split-Path $cursor -Parent
    if ($parent -eq $cursor) { break }
    $cursor = $parent
  }
  return $null
}

$DANBOORU_TAGS_DIR = if ($env:DANBOORU_TAGS_DIR) {
  $env:DANBOORU_TAGS_DIR
} elseif (Test-DanbooruTagsDir ".") {
  (Get-Location).Path
} elseif (Test-DanbooruTagsDir "./danbooru-tags") {
  (Resolve-Path "./danbooru-tags").Path
} elseif ($found = Find-DanbooruTagsDirFromSkills ".") {
  $found
} else {
  throw "Set DANBOORU_TAGS_DIR or run from a directory that can discover skills/danbooru-tags"
}
Push-Location "$DANBOORU_TAGS_DIR"

if (-not (Test-DanbooruTagsCli $DANBOORU_TAGS_DIR)) {
  throw "Found danbooru-tags at $DANBOORU_TAGS_DIR, but bin/danbooru-tags.exe is missing. Restore the packaged CLI or rebuild it before running tag queries."
}

$DANBOORU_RUNTIME_DIR = if ($env:DANBOORU_TAGS_RUNTIME_DIR) {
  $env:DANBOORU_TAGS_RUNTIME_DIR
} elseif ($env:SKILL_RUNTIME_ROOT) {
  Join-Path $env:SKILL_RUNTIME_ROOT "danbooru-tags"
} else {
  $cursor = (Resolve-Path $DANBOORU_TAGS_DIR).Path
  $runtimeRoot = $null
  while ($cursor) {
    $candidate = Join-Path $cursor "runtime"
    if (Test-Path -LiteralPath $candidate) { $runtimeRoot = $candidate; break }
    $parent = Split-Path $cursor -Parent
    if ($parent -eq $cursor) { break }
    $cursor = $parent
  }
  if ($runtimeRoot) {
    Join-Path $runtimeRoot "danbooru-tags"
  } else {
    $repoRoot = Resolve-Path (Join-Path $DANBOORU_TAGS_DIR "..")
    if (Test-Path -LiteralPath (Join-Path $repoRoot.Path "comfyui-manager")) {
      Join-Path $repoRoot.Path "runtime\danbooru-tags"
    } else {
      Join-Path (Resolve-Path (Join-Path $DANBOORU_TAGS_DIR "..\..")).Path "runtime\danbooru-tags"
    }
  }
}
New-Item -ItemType Directory -Force -Path $DANBOORU_RUNTIME_DIR | Out-Null
