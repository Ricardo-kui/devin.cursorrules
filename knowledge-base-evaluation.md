# 学术研究知识库全面评估报告

## 基于 Karpathy LLM Wiki 理念的 Claude + Obsidian + Zotero 体系诊断与改造路线

---

**评估对象：** 商学院战略管理与市场营销系教授个人研究知识库  
**研究方向：** CEO特征、公司治理、企业风险、产品召回、高阶理论、战略决策、市场响应机制  
**已激活专题：** 产品召回、竞业协议、共同所有权（3个专题）  
**目标期刊：** AMJ、SMJ、JM、JMR  
**技术栈：** Claude（AI引擎）+ Obsidian（知识库载体）+ Zotero（文献管理）  
**评估基准：** Karpathy LLM Wiki 三层架构（2026年4月）  

---

## 一、当前体系完善度评估

### 1.1 三大组件各自能力评分

| 组件 | 当前角色 | Karpathy框架要求 | 差距评级 |
|------|---------|------------------|---------|
| **Claude** | 对话式问答、单次文献分析 | 持久化wiki维护者：自动摄入、交叉引用、矛盾标记、lint健检 | ⚠️ 高差距 |
| **Obsidian** | 笔记存储与浏览 | 结构化wiki的IDE：graph view导航、Dataview查询、wikilink知识网络 | ⚠️ 中高差距 |
| **Zotero** | 文献元数据管理与PDF存储 | raw/层：不可变原始文献档案库 | ✅ 低差距（需桥接） |

### 1.2 体系整体诊断

**核心问题：三大组件之间缺乏"编译层"（Compilation Layer）。**

Karpathy LLM Wiki 的核心洞察是：知识应该被**编译一次、持续维护**，而非每次查询时**重新从原始文档检索合成**。当前体系的根本问题是：

```
当前状态：
  Zotero(文献PDF) ──手动摘录──→ Word笔记(散落) ──手动搬运──→ Obsidian(存储)
                                                                    ↓
                                                              Claude(单次对话问答)

Karpathy目标状态：
  raw/(不可变原始文献) ──LLM自动编译──→ wiki/(结构化知识网络) ──LLM持续维护──→ 对话问答
       ↑                                    ↑                                    ↓
    Zotero导出                         Obsidian呈现                      答案回写为wiki页面
```

**当前体系存在的是"存储系统"，缺失的是"编译系统"。**

### 1.3 按 Karpathy 三层架构对标

| 层级 | Karpathy定义 | 您的当前状态 | 缺失项 |
|------|-------------|-------------|--------|
| **Layer 1: Raw Sources** | 不可变的原始文献档案 | Zotero中的PDF + 散落的Word笔记 | Word笔记未统一转为Markdown进入raw/；Zotero与Obsidian间缺乏自动同步管道 |
| **Layer 2: The Wiki** | LLM生成并维护的结构化Markdown网络 | 三个专题的Obsidian笔记（手动整理） | 无LLM自动编译流程；无index.md总目录；无log.md变更日志；无标准化frontmatter；交叉引用不系统 |
| **Layer 3: The Schema** | 指导LLM行为的schema配置文件 | 不存在 | 无CLAUDE.md或等效文件；无摄入/查询/lint工作流定义；无学术领域特定规范 |

---

## 二、六大流程堵点诊断

### 堵点1：Word → Obsidian 的格式断裂

**问题：** 多年积累的Word文献笔记是"高工整度"的，但Word格式(.docx)无法被LLM直接读取和编译。每篇笔记需要手动转换，这是最大的迁移瓶颈。

**影响：** 数十甚至上百篇文献笔记的知识被"锁死"在Word格式中，无法参与语义化、链接化、LLM编译。

**解决路径：**
- 使用 Pandoc 批量转换：`pandoc input.docx -o output.md --wrap=none`
- 转换后进入 `raw/word-notes/` 目录作为不可变原始笔记
- LLM再将其编译为wiki页面

### 堵点2：Zotero → Obsidian 的元数据断链

**问题：** Zotero中的文献元数据（作者、年份、期刊、DOI、标签）与Obsidian中的笔记内容之间缺乏结构化桥接。

**影响：** 无法实现"从理论概念 → 追溯到具体文献 → 定位到PDF原文"的两跳溯源。

**解决路径：**
- 安装 Zotero Integration 插件（Obsidian社区插件）
- 配置文献导入模板，自动生成带标准frontmatter的Markdown文献卡片
- 每篇文献卡片应包含：citekey、作者、年份、期刊、DOI、摘要、关键发现、理论贡献

### 堵点3：缺乏统一的YAML Frontmatter标准

**问题：** 现有笔记可能没有统一的元数据头，导致Dataview无法查询、LLM无法系统性导航。

**影响：** 无法执行"列出所有关于CEO过度自信的文献"、"按发表年份排序产品召回研究"等结构化查询。

**建议的学术笔记frontmatter标准：**

```yaml
---
title: "CEO过度自信与企业风险承担"
type: concept | source-summary | theory | variable | method | evidence-chain
domain: [CEO特征, 企业风险, 高阶理论]
authors: [Malmendier & Tate]
year: 2005
journal: JF
citekey: malmendier2005ceo
sources: [raw/papers/malmendier2005.pdf]
related: [[高阶理论]], [[CEO特征]], [[风险承担]]
theories: [Upper Echelons Theory, Behavioral Decision Theory]
variables: [IV: CEO过度自信, DV: 企业投资, Moderator: 董事会独立性]
methodology: [Panel regression, Fixed effects]
sample: "S&P 1500, 1980-1994"
key_findings: "过度自信CEO更可能进行价值损毁的并购"
confidence: high
created: 2026-05-06
updated: 2026-05-06
---
```

### 堵点4：无交叉引用系统（Wikilink网络未建立）

**问题：** 三个已激活专题可能缺乏系统性的 `[[wikilink]]` 互联。

**影响：** 
- 无法通过Obsidian Graph View看到知识网络的全貌
- LLM无法通过链接追踪相关概念
- 理论与理论之间、变量与测量之间、研究与研究之间的关联未被编码

**学术知识库应建立的链接类型：**
1. **理论链接：** `[[高阶理论]]` → `[[CEO认知特征]]` → `[[过度自信]]`
2. **变量链接：** `[[产品召回]]`（DV）← `[[CEO特征]]`（IV）← `[[高阶理论]]`（理论基础）
3. **方法链接：** `[[事件研究法]]` → 用于测量 `[[市场响应]]`
4. **证据链链接：** `[[Malmendier2005]]` 支持 → `[[CEO过度自信假说]]`
5. **缺口链接：** `[[研究缺口：CEO特征与产品召回]]` → 连接多个理论和实证文献

### 堵点5：Claude使用方式未达"wiki维护者"级别

**问题：** Claude当前可能被用作"对话问答工具"（类似RAG模式），而非Karpathy所描述的"知识编译器"。

**Karpathy的关键区分：**
> "大多数人使用LLM和文档的体验是RAG模式：上传文件，LLM在查询时检索相关片段，生成答案。这可行，但LLM每次都在从零开始重新发现知识。没有积累。"

**当前模式 vs 目标模式：**

| 维度 | 当前（对话模式） | 目标（wiki维护者模式） |
|------|-----------------|---------------------|
| 知识处理时机 | 每次提问时临时合成 | 摄入时一次性编译，持续维护 |
| 交叉引用 | 每次临时发现 | 预先建立并维护 |
| 矛盾检测 | 可能被忽略 | 摄入时自动标记 |
| 知识积累 | 无——每次从零开始 | 每次摄入和查询后持续增长 |
| 输出形式 | 聊天回复（临时性） | 持久化Markdown文件（持久性） |

### 堵点6：缺乏Schema（编辑规范文件）

**问题：** 没有一个告诉Claude"你是谁、知识库怎么组织、如何处理新文献、如何回答问题"的系统性指令文件。

**影响：** 每次与Claude对话都是从零开始，无法保证一致性、系统性和学术严谨性。

---

## 三、三大已激活专题深度评估

### 3.1 产品召回（Product Recall）

**学术价值评估：**
- 产品召回是战略管理与市场营销的交叉领域，发表于AMJ、SMJ、JM、JMR均有路径
- 核心理论基础：信号理论、利益相关者理论、声誉理论、高阶理论
- 关键变量：召回频率、召回规模、召回响应速度、CEO特征、市场反应（CAR）

**LLM Wiki改造需求：**
- [ ] 建立 `wiki/concepts/product-recall.md` 总览页面
- [ ] 建立变量页面：`wiki/variables/recall-severity.md`、`wiki/variables/market-reaction-car.md`
- [ ] 建立理论页面：`wiki/theories/signaling-theory.md`（关联到产品召回情境）
- [ ] 建立方法页面：`wiki/methods/event-study.md`
- [ ] 建立证据链页面：`wiki/evidence/recall-ceo-link.md`
- [ ] 所有现有Word笔记 → `raw/word-notes/product-recall/` → LLM编译为wiki页面

### 3.2 竞业协议（Non-Compete Agreements）

**学术价值评估：**
- 劳动力市场制度研究的热门话题，SMJ、JM发表路径清晰
- 核心理论基础：人力资本理论、知识溢出理论、制度理论、代理理论
- 关键变量：竞业协议可执行性（州级差异）、员工流动率、创新产出

**LLM Wiki改造需求：**
- [ ] 建立 `wiki/concepts/non-compete-agreements.md` 总览页面
- [ ] 建立制度背景页面：`wiki/context/us-state-nca-laws.md`
- [ ] 建立理论页面：`wiki/theories/human-capital-theory.md`
- [ ] 建立实证设计页面：`wiki/methods/diff-in-diff-nca.md`（利用州法律变化的自然实验）
- [ ] 建立文献地图：`wiki/literature-maps/nca-research-landscape.md`

### 3.3 共同所有权（Common Ownership）

**学术价值评估：**
- 公司治理前沿议题，SMJ、JF发表路径明确
- 核心理论基础：代理理论、公司治理理论、产业组织理论
- 关键变量：机构投资者重叠持股、产品市场竞争、企业战略决策

**LLM Wiki改造需求：**
- [ ] 建立 `wiki/concepts/common-ownership.md` 总览页面
- [ ] 建立理论页面：`wiki/theories/agency-theory-common-ownership.md`
- [ ] 建立争议页面：`wiki/debates/common-ownership-anticompetitive.md`
- [ ] 建立测量页面：`wiki/variables/common-ownership-measures.md`（MHHI等指标）
- [ ] 建立文献综述页面：`wiki/reviews/common-ownership-literature.md`

### 3.4 三大专题交叉链接分析

三个专题并非孤立，应建立以下交叉链接：

```
产品召回 ←→ CEO特征 ←→ 共同所有权
   ↓              ↓              ↓
市场反应      高阶理论      公司治理
   ↓              ↓              ↓
信号理论    行为决策理论    代理理论
   ↓              ↓              ↓
事件研究法   面板回归      工具变量法
```

**潜在研究问题（三专题交叉）：**
- "共同所有权是否影响企业产品召回决策？"（common ownership → product recall → AMJ/SMJ）
- "竞业协议如何影响CEO战略决策风格？"（NCA → CEO特征 → 风险承担 → SMJ）
- "共同所有权对竞业协议条款设计的影响？"（common ownership → NCA → 劳动力市场 → SMJ）

---

## 四、距离 Karpathy LLM Wiki 闭环的差距判断

### 4.1 闭环五要素评估

| 闭环要素 | Karpathy要求 | 当前状态 | 完成度 |
|---------|-------------|---------|--------|
| **raw → wiki 自动编译** | LLM读取原始文献，自动生成/更新wiki页面 | 手动摘录、手动整理 | 10% |
| **自然语言对话 → 带引用回答** | 读取index.md定位相关页面，综合回答并引用wiki页面 | Claude单次对话，无持久化索引 | 15% |
| **答案回写 → wiki持续增长** | 有价值的查询结果自动归档为新wiki页面 | 不存在 | 0% |
| **lint健康检查** | 定期检测矛盾、孤立页面、缺失概念 | 不存在 | 0% |
| **Schema持续进化** | CLAUDE.md随使用持续优化 | 不存在 | 0% |

**总体评估：当前距离Karpathy LLM Wiki闭环约完成5-10%，主要完成了"内容存在"，但"编译系统"和"维护系统"基本为零。**

### 4.2 好消息

1. **内容基础扎实：** 多年积累的Word笔记代表了大量高质量、已经过学术筛选的知识
2. **三个专题已激活：** 产品召回、竞业协议、共同所有权提供了足够的初始内容来建立wiki原型
3. **工具选型正确：** Claude + Obsidian + Zotero 的组合完全覆盖了Karpathy所需的能力
4. **领域聚焦：** 战略管理与市场营销的交叉领域，知识体量在LLM Wiki的最佳规模区间（50-200篇文献 ≈ 5万-10万token的wiki）

---

## 五、从当前状态到成熟LLM Wiki的最短路径

### 5.1 优先级排序（按投入产出比）

| 优先级 | 任务 | 投入产出比 | 理由 |
|--------|-----|-----------|------|
| **P0** | 创建Schema（CLAUDE.md） | ★★★★★ | 零成本高回报，立即改变Claude的行为模式 |
| **P1** | 建立wiki目录结构 + index.md + log.md | ★★★★★ | 骨架搭建，后续所有操作的基础 |
| **P2** | Word笔记批量转Markdown → raw/ | ★★★★☆ | 激活沉睡资产，是编译的前提 |
| **P3** | 第一个专题完整编译（产品召回） | ★★★★☆ | 端到端验证流程，建立模板 |
| **P4** | Zotero-Obsidian桥接配置 | ★★★☆☆ | 文献元数据流通的基础设施 |
| **P5** | 第二、三专题编译 | ★★★☆☆ | 复用P3模板，边际成本递减 |
| **P6** | 建立跨专题交叉链接与研究问题页面 | ★★★☆☆ | 真正发挥wiki相对于RAG的优势 |
| **P7** | lint工作流建立 | ★★☆☆☆ | wiki达到一定规模后才有必要 |

### 5.2 七天执行清单

#### Day 1：建立骨架与Schema（约3小时）

**任务1.1：创建目录结构**
```
D:\OneDrive\Obsidian Vault\
├── raw/                          # Layer 1: 不可变原始文献
│   ├── papers/                   # Zotero导出的PDF/BibTeX
│   ├── word-notes/               # 转换后的Word笔记Markdown
│   │   ├── product-recall/
│   │   ├── non-compete/
│   │   └── common-ownership/
│   └── web-clips/                # Obsidian Web Clipper剪藏
├── wiki/                         # Layer 2: LLM编译的知识网络
│   ├── index.md                  # 总目录
│   ├── log.md                    # 变更日志
│   ├── overview.md               # 研究全景概览
│   ├── concepts/                 # 概念页面
│   ├── theories/                 # 理论页面
│   ├── variables/                # 变量与测量页面
│   ├── methods/                  # 方法与研究设计页面
│   ├── sources/                  # 文献摘要页面
│   ├── evidence/                 # 证据链页面
│   ├── debates/                  # 学术争议页面
│   ├── literature-maps/          # 文献地图页面
│   ├── research-gaps/            # 研究缺口页面
│   └── research-questions/       # 研究问题页面
├── templates/                    # Obsidian模板
│   ├── source-summary.md         # 文献摘要模板
│   ├── concept-page.md           # 概念页面模板
│   ├── theory-page.md            # 理论页面模板
│   └── variable-page.md          # 变量页面模板
└── CLAUDE.md                     # Layer 3: Schema（LLM行为规范）
```

**任务1.2：撰写CLAUDE.md（学术研究版Schema）**

```markdown
# 学术研究知识库 — Schema

## 身份与使命
你是一位商学院战略管理与市场营销领域的研究知识库维护者。
你的使命是帮助教授维护一个面向顶刊发表（AMJ、SMJ、JM、JMR）的结构化知识库。
你负责所有知识编译工作：摘要、交叉引用、矛盾标记、证据链构建。
教授负责文献选择、研究方向判断和学术洞察。

## 研究领域
- CEO特征与高阶理论（Upper Echelons Theory）
- 公司治理（Corporate Governance）
- 企业风险（Corporate Risk-Taking）
- 产品召回（Product Recalls）
- 竞业协议（Non-Compete Agreements）
- 共同所有权（Common Ownership）
- 战略决策（Strategic Decision-Making）
- 市场响应机制（Market Response）

## 目录结构
- `raw/` — 不可变原始文献。绝不修改。
- `wiki/` — LLM生成并维护的知识网络。你完全拥有此层。
- `wiki/index.md` — 全部页面的主目录。每次摄入后必须更新。
- `wiki/log.md` — 仅追加的活动日志。

## 页面类型与frontmatter规范

### 文献摘要页面（source-summary）
---
title: "文献标题"
type: source-summary
authors: [作者列表]
year: 发表年份
journal: 期刊简称
citekey: Zotero citekey
domain: [所属领域标签]
theories: [涉及的理论]
variables:
  IV: [自变量]
  DV: [因变量]
  moderator: [调节变量]
  mediator: [中介变量]
  control: [控制变量]
methodology: [研究方法]
sample: "样本描述"
key_findings: "核心发现一句话"
contribution: "理论贡献一句话"
limitations: "主要局限"
future_directions: "未来研究方向"
related: [[相关wiki页面]]
confidence: high | medium | low
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

### 理论页面（theory）
包含：理论起源、核心命题、关键假设、代表性文献、在本领域的应用、
与其他理论的关系、理论缺口

### 概念页面（concept）
包含：定义、操作化方式、测量方法、相关理论、关键文献、研究缺口

### 变量页面（variable）
包含：概念定义、操作化定义、常用测量方法（含具体量表/指标）、
数据来源、在顶刊中的使用案例

### 证据链页面（evidence-chain）
包含：主张/假说 → 支持文献列表（含效应量和显著性）→ 
反对文献列表 → 边界条件 → 证据强度评估

### 研究缺口页面（research-gap）
包含：已有研究概述 → 未解决的问题 → 为什么重要 → 
可能的理论框架 → 可能的研究设计 → 目标期刊

## 摄入工作流（Ingest）
当教授说"摄入 [文件名]"时：
1. 完整阅读 raw/ 中的源文件
2. 与教授讨论关键发现和理论贡献
3. 创建/更新 wiki/sources/ 中的文献摘要页面
4. 更新所有相关的理论、概念、变量、方法页面
5. 检查新文献是否与已有wiki内容存在矛盾，明确标记
6. 添加/更新所有 [[wikilink]] 交叉引用
7. 更新 wiki/index.md
8. 追加条目到 wiki/log.md
9. 评估是否需要新建研究缺口页面

## 查询工作流（Query）
当教授提出研究问题时：
1. 首先阅读 wiki/index.md 定位相关页面
2. 阅读相关页面
3. 综合回答，必须带 [[wiki页面]] 引用
4. 如果回答涉及多文献综合，提供证据链
5. 如果回答有价值，建议归档为新的wiki页面
6. 回答格式应适配顶刊写作需求：
   - 研究动机（motivation）→ 引用研究缺口页面
   - 理论基础（theoretical foundation）→ 引用理论页面
   - 变量测量（measurement）→ 引用变量页面
   - 实证支持（empirical evidence）→ 引用证据链页面

## lint工作流（Lint）
当教授说"lint"或"健康检查"时：
1. 检查页面间的理论矛盾（同一变量在不同页面的定义是否一致）
2. 查找孤立页面（无入链的页面）
3. 列出被提及但没有独立页面的重要概念
4. 检查证据链页面是否有新文献可以补充
5. 检查frontmatter完整性
6. 建议下一步应该摄入的文献
7. 建议应该探索的研究问题

## 学术严谨性规则
- 所有主张必须可追溯到raw/中的原始文献
- 效应量和统计显著性必须注明
- 不同文献间的矛盾必须明确标记，不得静默覆盖
- 区分"已确认发现"和"初步证据"
- 样本、方法、时间范围差异必须注明
- 研究缺口的识别必须基于系统性文献回顾，不可臆造
```

**任务1.3：创建初始 index.md 和 log.md**

#### Day 2：Word笔记批量转换（约4小时）

**任务2.1：安装Pandoc**
```bash
# Windows
winget install JohnMacFarlane.Pandoc
```

**任务2.2：批量转换脚本**
```powershell
# PowerShell批量转换脚本
$wordFolder = "D:\原始Word笔记文件夹"
$outputFolder = "D:\OneDrive\Obsidian Vault\raw\word-notes"

Get-ChildItem -Path $wordFolder -Filter "*.docx" | ForEach-Object {
    $outputFile = Join-Path $outputFolder ($_.BaseName + ".md")
    pandoc $_.FullName -o $outputFile --wrap=none --extract-media="$outputFolder/assets"
    Write-Host "Converted: $($_.Name) -> $($_.BaseName).md"
}
```

**任务2.3：转换后质量检查**
- 检查表格是否正确转换
- 检查引用格式是否保留
- 检查特殊字符是否正确
- 将笔记按专题分入对应子文件夹

#### Day 3：第一个专题完整编译 — 产品召回（约5小时）

**任务3.1：与Claude进行首次摄入会话**

打开Claude，粘贴CLAUDE.md内容，然后逐篇摄入产品召回相关笔记：

```
请阅读以下文献笔记并按照Schema执行摄入工作流：

[粘贴第一篇产品召回文献笔记的Markdown内容]
```

**任务3.2：每篇文献期望产出**
- 1个文献摘要页面（wiki/sources/）
- 更新或创建相关概念页面
- 更新或创建相关理论页面
- 更新或创建相关变量页面
- 更新index.md
- 追加log.md

**任务3.3：摄入完所有产品召回文献后**
- 创建 `wiki/literature-maps/product-recall-landscape.md`（文献全景图）
- 创建 `wiki/evidence/recall-market-response.md`（证据链）
- 创建 `wiki/research-gaps/recall-ceo-governance.md`（研究缺口）

#### Day 4：Zotero-Obsidian桥接 + 第二专题编译开始（约4小时）

**任务4.1：配置Zotero Integration**
- Obsidian社区插件搜索"Zotero Integration"，安装
- 配置导入模板，使用Day 1定义的frontmatter标准
- 测试导入一篇文献，验证元数据完整性

**任务4.2：开始编译竞业协议专题**
- 复用Day 3的流程和模板
- 注意建立与产品召回专题的交叉链接（如共享理论页面）

#### Day 5：完成第二、三专题编译（约5小时）

**任务5.1：完成竞业协议专题**
**任务5.2：开始并完成共同所有权专题**
**任务5.3：建立三专题交叉链接**
- 共享理论页面（如代理理论同时服务于共同所有权和产品召回）
- 共享方法页面（如事件研究法）
- 共享变量页面（如CEO特征变量）

#### Day 6：跨专题综合与研究问题生成（约4小时）

**任务6.1：创建overview.md**
- 三大专题的全景综述
- 专题间的理论交叉点
- 方法论共性与差异

**任务6.2：生成研究问题页面**
- 基于三专题的交叉，向Claude提问：
  "基于整个wiki的内容，识别三个专题交叉处最有发表潜力的研究问题，
   每个问题需要包含：理论基础、研究缺口、变量关系、可能的研究设计、
   目标期刊。"
- 将结果归档为wiki页面

**任务6.3：首次lint健康检查**
- 执行完整lint流程
- 修复发现的问题
- 补充缺失的页面

#### Day 7：验收与优化（约3小时）

**任务7.1：端到端测试**
向Claude提出以下学术研究问题，验证回答质量：

1. "产品召回后企业的市场反应受哪些CEO特征调节？请给出完整的理论基础和实证证据链。"
2. "请为'共同所有权对产品安全决策的影响'这一研究问题构建理论框架，包含研究动机、理论基础、假设推导依据。"
3. "竞业协议的可执行性如何影响CEO的风险承担行为？请综合相关文献给出分析。"
4. "为一篇目标AMJ的论文，请基于知识库生成文献综述框架，主题为CEO特征与产品召回。"

**任务7.2：评估回答质量**
- 是否引用了具体的wiki页面？
- 是否综合了多篇文献的发现？
- 是否识别了矛盾和边界条件？
- 是否适配顶刊的写作标准？

**任务7.3：Schema迭代**
- 根据测试结果修改CLAUDE.md
- 记录学到的经验

---

## 六、让Claude真正理解全部研究笔记的配置方案

### 6.1 方案选型

| 方案 | 适用规模 | 复杂度 | 推荐度 |
|------|---------|--------|--------|
| **A: Claude Projects（推荐）** | 3万-20万token | 低 | ★★★★★ |
| B: Claude Code + 本地文件 | 无限制 | 中高 | ★★★★☆ |
| C: Obsidian插件（Copilot/Smart Connections） | 5万-50万token | 低 | ★★★☆☆ |
| D: 自建RAG（混合方案） | 50万token以上 | 高 | ★★☆☆☆ |

### 6.2 推荐方案A：Claude Projects 配置

**为什么选Claude Projects：**
- 支持最多200K token的Project Knowledge
- wiki编译后的所有页面（预计100-200个页面 × 500 token = 5万-10万token）完全可以放入
- 每次对话自动加载全部项目知识，无需手动粘贴
- 支持自定义System Prompt（= Karpathy的Schema）

**配置步骤：**

1. **创建Claude Project：** 登录claude.ai → Projects → 新建"学术研究知识库"

2. **上传Project Knowledge：**
   - 上传 wiki/ 目录下的所有Markdown文件
   - 上传 CLAUDE.md 作为 Custom Instructions
   - 不要上传raw/（保持在本地Obsidian Vault中）

3. **设置Custom Instructions（粘贴CLAUDE.md的内容）**

4. **工作流程：**
   ```
   摄入新文献：
   1. 在Claude Project对话中粘贴新文献内容
   2. Claude按Schema编译
   3. 将Claude生成的wiki页面复制回Obsidian Vault
   4. 更新Claude Project的Knowledge文件
   
   查询研究问题：
   1. 在Claude Project对话中提问
   2. Claude基于全部wiki内容回答（带引用）
   3. 有价值的回答归档为新wiki页面
   ```

5. **同步策略：**
   - 每次在Obsidian中修改wiki页面后，重新上传到Claude Project
   - 每次Claude生成新页面后，下载到Obsidian Vault
   - 建议每周进行一次全量同步

### 6.3 进阶方案B：Claude Code + 本地文件操作

**适用场景：** 当wiki规模超过200K token，或需要更自动化的工作流时。

```bash
# 安装Claude Code（如尚未安装）
npm install -g @anthropic-ai/claude-code

# 在Obsidian Vault目录下初始化
cd "D:\OneDrive\Obsidian Vault"
claude

# Claude Code可以直接读写本地文件，实现完全自动化的摄入/查询/lint
```

### 6.4 Obsidian插件辅助方案

**推荐安装的插件：**

| 插件 | 用途 | 优先级 |
|------|------|--------|
| **Zotero Integration** | 文献元数据自动导入 | P0 |
| **Dataview** | frontmatter结构化查询 | P0 |
| **Templater** | 标准化页面模板 | P1 |
| **Smart Connections** | 基于语义的笔记关联推荐 | P2 |
| **Obsidian Copilot** | Vault内AI问答 | P2 |
| **Graph Analysis** | 知识网络分析 | P2 |
| **Obsidian Web Clipper** | 浏览器文章剪藏 | P2 |
| **Marp Slides** | 从wiki内容生成学术报告幻灯片 | P3 |

### 6.5 Dataview查询示例（配合frontmatter使用）

```dataview
TABLE authors, year, journal, key_findings
FROM "wiki/sources"
WHERE contains(domain, "产品召回")
SORT year DESC
```

```dataview
TABLE title, type, length(related) AS "链接数"
FROM "wiki"
WHERE length(related) < 2
SORT file.name ASC
```

```dataview
LIST
FROM "wiki/research-gaps"
WHERE contains(domain, "CEO特征")
```

---

## 七、成熟度评估矩阵与目标里程碑

### 7.1 LLM Wiki成熟度模型

| 级别 | 名称 | 特征 | 您的当前位置 |
|------|------|------|-------------|
| **L0** | 散落存储 | Word/PDF文件散落在文件夹中 | ← 大部分笔记在此 |
| **L1** | 集中存储 | 文件迁入Obsidian，但无结构 | ← 三个专题部分在此 |
| **L2** | 结构化存储 | frontmatter + wikilink + 目录结构 | 目标：Day 1-2达到 |
| **L3** | LLM辅助编译 | LLM参与摄入和编译，但人工主导 | 目标：Day 3-5达到 |
| **L4** | LLM Wiki运行 | 完整的摄入/查询/lint循环，知识持续积累 | 目标：Day 6-7达到 |
| **L5** | 自进化知识库 | 100+文档、40万词，自动发现研究缺口，直接支撑论文写作 | 目标：30天后评估 |

### 7.2 关键度量指标

| 指标 | 当前值（估） | 7天目标 | 30天目标 |
|------|------------|---------|---------|
| wiki页面总数 | 0 | 60-80 | 200+ |
| 交叉引用链接数 | ~少量 | 200+ | 1000+ |
| 理论页面数 | 0 | 8-12 | 20+ |
| 证据链页面数 | 0 | 3-5 | 15+ |
| 研究缺口页面数 | 0 | 3-5 | 10+ |
| index.md完整性 | 不存在 | 100% | 100% |
| frontmatter覆盖率 | ~0% | 100% | 100% |
| Claude可检索率 | ~0% | 80% | 95%+ |

---

## 八、总结与核心建议

### 一句话诊断
> **您拥有优质的学术内容资产，但缺失Karpathy所描述的"编译系统"——即将散落的文献笔记自动编译为结构化、交叉引用、持续维护的知识网络的能力。**

### 三个最高优先级行动

1. **今天就写CLAUDE.md**——这是零成本、最高回报的行动。一旦Schema存在，Claude就从"通用聊天机器人"变为"专业知识编译器"。

2. **本周完成Word → Markdown转换**——您多年的学术积累被锁在.docx格式中。Pandoc批量转换是解锁这些资产的钥匙。

3. **选一个专题做端到端验证**——不要试图一次性完成所有专题。选择产品召回，完整走一遍"raw → LLM编译 → wiki页面 → 交叉引用 → 查询验证"的全流程，建立信心和模板。

### 长期愿景
当知识库达到100+文档、200+wiki页面规模后，您将能够：
- 在Claude中用自然语言提问："为什么CEO的军旅经历会影响产品召回决策？请构建完整的理论论证链。"
- Claude回答时自动引用知识库中的理论页面、变量测量页面、实证证据页面
- 回答质量足以直接嵌入顶刊论文的理论发展部分
- 这就是Karpathy所说的："wiki是持久的、持续积累的产物。交叉引用已经在那里了。矛盾已经被标记了。综合已经反映了你读过的一切。"

---

*评估完成日期：2026-05-06*  
*基准框架：Karpathy LLM Wiki (2026-04-03)*  
*评估范围：产品召回、竞业协议、共同所有权三大专题*
