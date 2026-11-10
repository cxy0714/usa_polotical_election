# 双语排版规范 / Bilingual formatting specification

Binding for every Markdown deliverable converted to bilingual format.
适用于所有转为双语格式的 Markdown 交付物，具有约束力。

---

## 1. Layout rule / 排版规则

Each **English block is followed immediately by its Chinese counterpart**.
每一段英文之后紧跟对应的中文译文。

```markdown
### 4. Documented visual identity / 有据可查的视觉识别

English paragraph text…

中文段落文本……

| Metric | 指标 | Median | 中位数 |
|---|---|---|---|
| Aspect ratio | 宽高比 | 1.500 | 1.500 |
```

Rules / 规则:

1. **Headings are bilingual on one line** — `English / 中文`. Never duplicate a
   heading as two separate headings.
   标题单行双语，用 ` / ` 分隔；不得拆成两个标题。
2. **Body paragraphs alternate EN → ZH.** One English paragraph, then its Chinese
   paragraph. A reader must be able to stop after either one.
   正文段落按「英 → 中」交替；读者读完任一段落即获得完整信息。
3. **Tables**: either one bilingual table (English cell then Chinese in the same
   cell separated by `<br>`), or a bilingual header row where the column name is
   `English | 中文`. Prefer adding a Chinese column label and translating only
   prose cells; keep numeric cells single-valued.
   表格：优先双语表头（`English / 中文`）；数字单元格只写一次，不重复。
4. **Lists**: translate each list item, English line then Chinese line, same
   bullet grouping. Do not merge or reorder items.
   列表：逐条对应翻译，顺序与条目不得增删。
5. **Front matter** gains a bilingual title and a `language:` field:

```yaml
---
title: "English title"
title_zh: "中文标题"
language: en+zh
...
---
```

---

## 2. Traceability rules — NON-NEGOTIABLE / 溯源规则（不可违反）

These exist because the whole archive is judged on traceability. Breaking them
invalidates the deliverable.
整个档案以可溯源性为评判标准，违反以下任一条即判定交付物失效。

1. **Never alter a URL, `SRC-####` id, dataset row id, date, percentage, dollar
   figure, vote count or person's name.** Copy them byte-for-byte.
   不得改动任何 URL、`SRC-####` 编号、数据集行 ID、日期、百分比、金额、票数或人名，必须逐字复制。
2. **Quotations stay in the original English**, followed by a Chinese rendering in
   parentheses marked `（译）`. Never translate *instead of* quoting; never
   paraphrase inside quotation marks.
   引语保留英文原文，其后以 `（译：……）` 给出中文译文；不得以译文替代原文，不得在引号内改写。
   ```markdown
   He said "we can never quite work out the details"（译：我们始终无法把细节谈拢）。
   ```
3. **Controlled vocabulary values, CSV field names, and file names stay in
   English.** Translations of these belong only in the bilingual data dictionary,
   never inside a code span or a CSV.
   受控词表值、CSV 字段名与文件名保持英文；其中文对照只出现在双语数据字典中。
4. **`unknown` stays `unknown`**, with the Chinese explanation in prose only
   (`unknown（未查明）` is acceptable in body text, but the literal cell value in
   any CSV remains `unknown`).
   `unknown` 保持原样；正文可写作 `unknown（未查明）`，CSV 单元格仍须为 `unknown`。
5. **Hedge and uncertainty language must be translated faithfully.** Where the
   English says "not verified" or "`⚠ unknown`", the Chinese must not soften it
   into a confident statement. Translation must not add certainty.
   不确定表述必须如实翻译；英文写"未核实"或"`⚠ unknown`"，中文不得改写成肯定判断。翻译不得增加确定性。
6. **Do not add new facts, sources, interpretations or evaluative judgements while
   translating.** This is a rendering task, not a rewriting task. If a sentence is
   hard to translate because the underlying fact is unclear, keep it unclear in
   Chinese too.
   翻译过程中不得新增事实、来源、解读或评价。这是转换任务，不是重写任务；原文含糊处译文亦须含糊。
7. **Preserve every Markdown link exactly** (`[text](path)` → keep path; Chinese
   link text may be added after the English, e.g. `[README](README.md)（[中文](README.md)）` is
   unnecessary — simply keep the link and translate surrounding prose).
   所有 Markdown 链接原样保留；仅翻译链接外的说明文字。
8. **Do not delete content to save space.** If a file is long, translate all of it.
   Length is acceptable; omission is not.
   不得为压缩篇幅删减内容；篇幅长可接受，漏译不可接受。

---

## 3. Tone / 语气要求

- Chinese should read as **research prose for an analyst**, not as machine
  translation. Prefer 书面语, precise connectives (因为／但是／然而／此外), and
  avoid Chinglish word order.
  中文应为面向研究者的书面语，避免机器翻译腔与英文语序直搬。
- Keep the archive's **non-evaluative stance** in Chinese: no words like
  "更成功""更有说服力""显然优于".
  中文必须保持非评价立场，不得出现"更成功""更有说服力""明显更优"等判断词。
- Proper nouns: first mention `English（中文）`, then Chinese thereafter.
  专有名词首次出现用 `English（中文）`，其后用中文。
- Use 「」or Chinese quotation marks for translated speech, not English quotes.
  译文引语使用中文引号「」，不使用英文引号。

---

## 4. Self-check before finishing / 完成前自检

- [ ] Every heading bilingual, no duplicate headings 每个标题均双语且未重复
- [ ] Every English paragraph has a Chinese counterpart 每段英文均有中文对应
- [ ] All `SRC-####`, URLs, dates, numbers unchanged 编号、链接、日期、数字未变
- [ ] Quotes: English original + `（译）` rendering 引语保留原文并附译文
- [ ] No new facts or judgements 无新增事实或判断
- [ ] Front matter has `title_zh` and `language: en+zh` 前置元数据含双语标题与语言字段
- [ ] File name unchanged 文件名未改
