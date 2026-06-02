# Keyword Match Scoring — Resolved

Status: resolved in bundled `bin/danbooru-tags.exe`.

## Fixed cases

```powershell
.\bin\danbooru-tags.exe --group character --keyword "fumizuki kai ni" --limit 5 --for-prompt --json --compact
.\bin\danbooru-tags.exe --group character --keyword "kako kai ni" --limit 5 --for-prompt --json --compact
```

Expected confirmed tags:

- `fumizuki_kai_ni_(kancolle)`
- `kako_kai_ni_(kancolle)`

## Cause

Structured character queries used a count-sorted SQL prefilter that was too small for low-count suffix variants such as `kai ni`.

## Fix

For `characters` and `series` keyword queries, the Rust CLI now reads a larger candidate pool before final text scoring. V3 also uses the corrected Danbooru category mapping: `3=series`, `4=characters`.
