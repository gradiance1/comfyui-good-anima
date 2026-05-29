# ComfyUI 执行排障

> ⚠️ 核心规则已回流至 SKILL.md。本文件仅提供扩展细节与边界情况。如内容与 SKILL.md 冲突，以 SKILL.md 为准。

只在执行失败或用户明确要求排查时读取本文件。

## 分流规则

- 连接失败：先确认 ComfyUI 是否启动、端口是否和 `workspace/config.json` 一致。
- 400 / invalid prompt：检查 args 字段、workflow schema、节点枚举值。
- `value_not_in_list`：检查模型、CLIP、VAE、LoRA 文件名是否和当前 ComfyUI 扫描结果一致。
- 依赖缺失：运行 `deps check`，不要直接猜模型路径。

## 环境适配检查

首次在新机器、迁移后的 ComfyUI、重装模型目录后使用 Anima 默认工作流前，检查：

```powershell
comfyui-skill --json --dir "$WORKSPACE" models list diffusion_models
comfyui-skill --json --dir "$WORKSPACE" models list text_encoders
comfyui-skill --json --dir "$WORKSPACE" models list vae
comfyui-skill --json --dir "$WORKSPACE" models list loras
```

重点匹配：

- AnimaBoosterLoader 的 `model_name`
- CLIPLoader 的 `clip_name`
- VAELoader 的 `vae_name`
- LoraLoaderModelOnly 的 `lora_name`

如果 workflow JSON 里的值不在扫描结果中，需要修正 workflow JSON 后重新导入。

## 400 Bad Request

处理顺序：

1. 对同一 args 先跑 validate 或等效 schema 检查，确认不是参数文件格式错误。
2. 跑 `deps check`，确认不是缺节点或缺模型。
3. 读取错误 JSON 中的 `node_errors`、节点名、输入名和 expected choices。
4. 检查 args 是否传了 workflow schema 不接受的字段。
5. 检查枚举值是否完整，例如 `teacache_version` 不能写短值 `v1`。
6. 检查 prompt 字段是否为空或类型不符。
7. 只有确认 ComfyUI 在线且 args 格式正确后，才查看 workflow info。

常用命令：

```powershell
comfyui-skill --json --dir "$WORKSPACE" deps check local/workflow_id
comfyui-skill --json --dir "$WORKSPACE" info local/workflow_id
```

如果 CLI 抽象隐藏了详细错误，可直接向 ComfyUI `/prompt` 端点提交同一 prompt JSON 查看原始 `node_errors`；只在本地开发/排障时使用，不替代正常执行链路。

不要反复枚举 help、templates、目录结构或随机改 workflow。
