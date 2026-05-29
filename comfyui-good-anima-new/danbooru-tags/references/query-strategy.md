# Danbooru 查询与回填策略

> ⚠️ 核心规则已回流至 SKILL.md。本文件仅提供扩展细节与边界情况。如内容与 SKILL.md 冲突，以 SKILL.md 为准。

只在生图前批量校验、候选筛选、回填 prompt hard anchors 时读取本文件。

## 批量并发与多变体

- `--batch-workers N` 控制批量查询并发，建议 4-8；过高会增加 SQLite 连接竞争。
- `--batch-file` 必须是 JSON 对象，包含 `queries` 数组；每条 query 必须有唯一 `id`。
- 提升准确度时，不要多次调用 CLI；在同一个 `queries` 里放同一锚点的多个变体。
- 普通生图最多 4 个语义锚点；每个锚点最多 2-3 个变体；总 query 控制在 12-16 内。
- `--compact` 结果只读 JSON 并筛选，不向用户复述完整检索过程。
- group 精确过滤无命中时返回的 general 候选只作为 `candidate_tags`。

## 查询示例

用户说“巫女服”，不要只查 `group=clothing keyword=巫女服`。一次 batch 覆盖：

```json
{
  "queries": [
    {
      "id": "miko_clothing",
      "group": "clothing",
      "keyword": "miko",
      "limit": 5
    },
    {
      "id": "miko_general",
      "category": "general",
      "keyword": "miko",
      "limit": 5
    },
    {
      "id": "miko_hakama",
      "group": "clothing",
      "keyword": "hakama",
      "limit": 5
    },
    {
      "id": "miko_sleeves",
      "group": "clothing",
      "keyword": "wide sleeves",
      "limit": 5
    },
    {
      "id": "miko_detached_sleeves",
      "group": "clothing",
      "keyword": "detached sleeves",
      "limit": 5
    },
    {
      "id": "miko_japanese_clothes",
      "group": "clothing",
      "keyword": "japanese clothes",
      "limit": 5
    }
  ]
}
```

## 回填策略

采用“Danbooru 锚点确认 + nltags 补足”：

1. 角色、作品、画师、基础外观优先查到并回填。
2. 服装/配饰/动作/场景/光影先查可确认 tag，再筛选。
3. 由 `comfyui-animatool` 生图调用时，以它的最多 4 项批量查询限制为准。
4. 复合短语拆成可确认锚点，例如 `fur-trimmed hooded cape` 拆成 `fur trim`、`hood`、`cape`。
5. 查不到完整组合时不要编 tag，交给 `nltags`。
6. 不要把 `candidate_tags` 整组塞进 prompt。
7. 不要堆 30+ 个松散 tag；少量硬锚点更稳。

## 输出筛选

- `confirmed_tags` 可作为高置信候选，但仍要和用户意图一致。
- `candidate_tags` 只在语义明显匹配时使用。
- `missing` 直接交给自然语言，不无限补查。
- 生图回填默认使用 `--for-prompt --json --compact`。
- 随机画师候选最多选 1 个；用户明确要求混合风格时最多 2 个。
- `count` 是训练覆盖与稳定性参考，不是默认硬门槛；不要默认加 `--min-count`。
- 不要为了给随机画师补 `count` 反复二次查询。
