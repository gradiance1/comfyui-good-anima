# Danbooru 查询模式

只在生成前批量校验、候选筛选、回填 prompt hard anchors 或维护索引时读取。

## 批量与多变体

- `--batch-workers N`：建议 4-8。
- 批量 JSON 是带 `queries` 数组的对象；每个 query 必须有唯一 `id`。
- Shell 入口优先用 `--batch-file`，JSON 文件写无 BOM UTF-8。
- 同一个锚点的多个写法放进同一个 `queries` 数组；不要多次调用 CLI。
- 中文/日文俗称先转 Danbooru 英文或罗马音；同批放主词、别名、拆分词。
- group 过滤可能漏掉的概念，可同时加 `category=general` 变体。
- 精确画师/角色/作品查询默认 `limit 5`；服装/动作/场景/俗称可用 `limit 10-20`，最终仍只回填少量锚点。
- 典型生图校验 2-4 个语义锚点；每个锚点 2-3 个变体即可。
- 默认每次生图最多 1 次批量查询；只有必需锚点缺失时才加 1 次小补查，不要反复重查。
- `--compact` 结果只供 JSON 筛选，不要向用户复述完整搜索过程。
- group 未命中但 general 命中时，结果只当 `candidate_tags`。

## 查询例子：巫女服

不要只查 `group=clothing keyword=miko`。同批覆盖服装词、general 词和组成部件：

```json
{
  "queries": [
    { "id": "miko_clothing", "group": "clothing", "keyword": "miko", "limit": 5 },
    { "id": "miko_general", "category": "general", "keyword": "miko", "limit": 5 },
    { "id": "miko_hakama", "group": "clothing", "keyword": "hakama", "limit": 5 },
    { "id": "miko_sleeves", "group": "clothing", "keyword": "wide sleeves", "limit": 5 },
    { "id": "miko_detached", "group": "clothing", "keyword": "detached sleeves", "limit": 5 },
    { "id": "miko_jp", "group": "clothing", "keyword": "japanese clothes", "limit": 5 }
  ]
}
```

## 输出筛选

- `confirmed_tags`：高置信候选，仍必须符合用户意图。
- `candidate_tags`：只有语义明显匹配时才用。
- `missing`：直接交给自然语言，不要无限补查。
- 生图回填一律用 `--for-prompt --json --compact`。

## 关键词匹配评分

`--keyword` 使用模糊评分，不是严格子串匹配。带变体后缀的 tag 可能比基础 tag 得分低。

已知模式：角色服装/季节/改二变体，例如 `fumizuki_kai_ni_(kancolle)`、`kako_kai_ni_(kancolle)`，可能比 `fumizuki_(kancolle)`、`kako_(kancolle)` 得分低。

出现这种情况时：

- 变体会落入 `candidate_tags`，不一定进入 `confirmed_tags`。
- `--random` 仍可能抽到该变体，因为随机选择不依赖关键词评分。
- 精确搜索变体名可能 `found: false`，原因是评分低于阈值。

处理：

1. 先查基础角色名，例如 `fumizuki`，不要先查 `fumizuki kai ni`。
2. 检查 `candidate_tags` 中是否有目标变体。
3. 如果变体来自 `--random`，且语义符合用户意图，可信任 random 输出。

这不是两套索引；`--random` 和 `--keyword` 读的是同一份 CSV，差异来自匹配评分阈值。

## 随机规则

- `--random N`：`N` 是候选数量，建议 10-50，硬上限 1-300。
- `--random N --for-prompt`：返回可直接用于生图的少量结果，不是候选池。
- “抽 N 个候选再挑一个”：只调用一次 `--random N --json`。
- 随机角色/服装/姿势/场景：`--random N --group <group> --json`，不要加 `--for-prompt`。
- 随机画师候选池：用 `--random N --group artist --json`；选中数 `K` 由用户要求决定。
- 默认加速 + 美学 LoRA 工作流推荐单画师；批量任务可为每个非融合 job 分配 1 个画师。
- 用户明确要求画师融合时，才把多个已选画师交给 Artist Mixer。
- 随机男女/组合角色时，先抽候选池，再按用户组合约束筛选；不要把所有候选塞进一个 prompt。
- `count` 是训练覆盖和稳定性参考，不是默认硬阈值；不要默认加 `--min-count`。
- 候选池只用于内部筛选；最终展示数量按用户选中数 `K`，不复述完整 JSON。

## 索引维护

默认主索引使用 `anima-1.0.csv`。历史 CSV 只用于维护或兼容。`artists_extended.txt` 和外部画师表不参与默认生图回填。

存在 `tags_index.sqlite` 时优先 SQLite；普通任务不要把 `tags_index.json` 读进上下文。

更新 CSV 或白名单后重建索引：

```powershell
python .\build_index.py
```

需要检查 SQLite 构建逻辑时再读：`build_index.py`、`sqlite_index.py`、`tag_groups.py`、`rust-cli/src/*.rs`。
