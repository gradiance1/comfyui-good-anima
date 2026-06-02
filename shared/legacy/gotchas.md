# Anima V3 常见陷阱

编辑或审查 Anima skills 时读本文件。这里不重复完整规则，只记录最容易导致模型误操作的边界。

## 画师必须加 @

普通 prompt 里的画师写 `@artist name`。没有 `@` 时 Anima 对画师的响应很弱。

```text
@mignon    正确
mignon     错误
```

例外：Artist Mixer 的 `artist_chain` 不写 `@`，因为 `AnimaArtistPack` 已经把它当画师链处理。

## tag 用空格，不用下划线

Danbooru prompt tag 使用小写和空格。

```text
red hair     正确
red_hair     错误
```

`score_7`、`score_8`、`score_9` 这类质量 token 保留下划线。

## Artist Mixer 不要重复画师

使用 `artist_chain` 时，`prompt_11` 不再写画师名。否则画师会被双重强调，容易过拟合或出伪影。

## 画布不是固定 1024x1536

按人数、主体关系、横竖构图、脸部可读性选择画布。不要所有图都默认竖图。

## tag 与 nltags 不要重复

同一语义要么放 tag，要么放 `nltags`。tag 负责 Danbooru hard anchors，`nltags` 负责镜头、位置、光源、景深、脸部可读性。

## 不要查询抽象构图

光从左来、前中后景、人物情感关系、故事性动作通常写进 `nltags`。`danbooru-tags` 只用于稳定 tag 锚点。

## 不要过度检索

普通生图通常校验角色、作品、画师和少量关键锚点即可。查不到就转自然语言，不要反复补查。

## 质量前缀跟 workflow 绑定

默认双 LoRA 用 `masterpiece, very aesthetic, best quality, score_9, score_8...`。用户要求裸模型或对比测试时，改用裸模型前缀，不要混用。

## Artist Mixer 不是分别出图

“A 和 B 分别出一张”是两个普通 job；“A+B 融合成一张”才是 Artist Mixer。

## batch_size 与多个 job

同 prompt 多变体用 `batch_size=N`。不同角色、画师、构图、prompt 使用多个 args 分别 `submit`。

## submit 后立即返回

`submit` 的意义是非阻塞。提交后返回 `prompt_id` / manifest；只有用户要求看结果时才查询状态或缓存图片。
