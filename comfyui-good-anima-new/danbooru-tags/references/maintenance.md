# Danbooru 检索器维护

> ⚠️ 核心规则已回流至 SKILL.md。本文件仅提供扩展细节与边界情况。如内容与 SKILL.md 冲突，以 SKILL.md 为准。

只在维护 Rust CLI、SQLite 索引、CSV 数据源或排查检索器本身时读取本文件。普通查询和生图不要读取大数据文件。

## 数据文件边界

- 默认主索引只使用 `anima-1.0.csv`。
- `Anima-preview.csv`、`Anima-preview-alternate.csv` 等历史 CSV 只用于维护或兼容排查。
- `artists_extended.txt` 和外部画师表不参与默认生图回填。
- `tags_index.sqlite` 存在时优先查 SQLite，不预读 JSON。
- `tags_index.json` 是索引产物，不要在普通任务中加载到上下文。

## 维护命令

更新 CSV 或白名单后重建索引：

```powershell
python .\build_index.py
```

如需要检查 SQLite 构建逻辑，再读取：

- `build_index.py`
- `sqlite_index.py`
- `tag_groups.py`
- `rust-cli/src/*.rs`

## 普通任务禁止

- 不要读取 `Typora_Hook_Log.txt`。
- 不要读取 `_tmp_*`、`batch_*`、`random_*` 等历史运行样例，除非用户明确要求分析这些文件。
- 不要进入 `rust-cli/target` 或 `__pycache__`。
