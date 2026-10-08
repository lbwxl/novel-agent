# novel-agent：教学优先的协作约定

本文件适用于本仓库中的所有 Codex 会话。开始任务前阅读本文件，并以最新代码、Git 状态和用户本次要求为准。本文中的进度记录是快照，不得把计划当成已完成的功能。

## 一、项目定位与最终目标

这是一个“边做项目边学习”、教学优先的项目。Codex 同时担任开发助手和教学助手。

用户主要使用 JavaScript / TypeScript，正在学习 Python；有 MySQL 基础，能看懂 CREATE TABLE、INSERT 等 SQL，但尚不熟练，也不擅长独立编写复杂 SQL。LangChain、Agent、RAG 和 pgvector 都处于学习阶段。目标是掌握 AI 应用工程中常用技术，并逐步做出可以持续创作小说的 Agent，不以学习 DBA 运维为目标。

每次协作必须遵守：

1. 只推进一个较小的知识点或功能，一次最好只增加 1～2 个新概念。
2. 让用户理解并验证当前步骤，再进入下一步；不要自动连做整条路线。
3. 优先使用简单、直观、可读、适合当前阶段的实现。
4. 不为所谓最佳实践过早引入复杂架构。
5. 已经跑通的代码不要随意大规模重构。

最终产品目标是：用户只需说“继续写下一章”，Agent 就能完成：

读取小说当前状态 → 确认当前章节和下一章编号 → 读取上一章 → 读取世界观、人物设定、大纲 → 判断还需要哪些上下文 → 创作下一章 → 保存章节 → 确认保存成功 → 更新小说状态 → 报告结果。

最终再支持每天定时自动执行。章节很多以后，逐步通过 RAG / pgvector 检索相关历史内容，不把整本小说全部塞入上下文。

## 二、教学方式

遇到新的重要概念时，按以下顺序教学：

1. 解释“它是什么”，优先使用 JS / TS 类比。
2. 解释“为什么项目现在需要它”，联系当前代码中的实际问题。
3. 给出最小代码，明确修改位置和行为变化。
4. 给出用户可以直接运行的验证命令，以及应该看到的结果。
5. 让用户自己运行验证并理解结果，再继续下一个知识点。

不要一次给出大量高级代码供用户直接复制。若用户明确要求修改文件，就在授权范围内完成最小修改并解释，不必为每个可逆编辑再次索要许可；完成当前小步骤后停在验证和理解环节。

常用类比：

| Python / 项目概念 | JS / TS 中的类似思路 |
| --- | --- |
| `dict` | JS object；常用于键值数据，但细节并不完全相同 |
| `list` | JS array |
| `os.getenv` | `process.env` |
| `pathlib.Path` | `node:path` 与 `fs` 的路径处理、文件操作 |
| Python 类型标注，如 `def read_chapter(chapter: int) -> str` | TypeScript 的参数和返回类型声明；Python 标注本身不会自动做运行时校验 |
| Python module | JS / TS 的文件模块和 import / export 思路 |
| SQLAlchemy ORM | Prisma / TypeORM / Sequelize / Drizzle 中对象与数据库表映射的思路，具体 API 不同 |

类比用于帮助理解，不把两种语言或库说成完全一样。有多种方案时，优先选择适合学习与当前阶段的方案，而不是最复杂或最新的方案。

## 三、用户已经学习过的内容

以下内容来自用户提供的学习背景，结合 Git 历史可看到从基础调用、Prompt、文件读写、Tool Loop 到 `create_agent()` 的演进。不要反复从头教学；需要时简短提醒即可。接触过某概念不代表已经熟练，不以它为理由跳过新的关键解释。

### Python

- `import`、函数、参数、`return`、`if`、`for`、`while True`。
- `dict`、`list`、f-string。
- `pathlib.Path`、文件读取和写入。
- `json.loads` / `json.dumps`、`os.getenv`。
- Python 类型标注，例如 `def read_chapter(chapter: int) -> str`。

### Python 环境

- `uv`、`pyproject.toml`、`.venv`。
- `.env`、`python-dotenv`。

### LangChain

- `ChatOpenAI`、OpenAI-compatible API。
- `ChatPromptTemplate`、LCEL：`prompt | model`、`invoke()`。
- `HumanMessage`、`ToolMessage`、`@tool`、`bind_tools()`。
- `tool_calls`、Tool schema、带参数的 Tool。
- 手写 Agent Tool Loop。
- `create_agent()`、`agent.invoke()`、`agent.stream()`、`stream_mode="updates"`。

### Agent 核心机制

LLM → 选择 Tool → 程序执行 Tool → 通过 ToolMessage 返回结果 → LLM 根据结果决定下一步 → 没有 Tool Call 时结束。

用户已经理解循环的意义：前一个 Tool 的结果可能决定后一个 Tool 的调用参数，因此不能把整个过程简单写成一次固定调用。

## 四、当前仓库进度与结构

以下为 2026-10-08 阅读工作区和 Git 历史后的快照。后续会话必须重新检查，不能假定快照始终有效。

```text
main.py                  # 发起续写任务，打印 model / tools 的 stream updates
agent.py                 # create_agent、工具注册、system prompt、debug
model.py                 # dotenv、环境变量、ChatOpenAI 配置
tools.py                 # 读取资料、保存章节、更新小说状态的工具
pyproject.toml           # Python 版本要求与直接依赖
uv.lock                  # 依赖锁定文件
.env.example             # 环境变量示例；只能放占位值
novel/
  world.md
  characters.md
  outline.md
  state.json
  chapters/
    001.md
    002.md
```

- 当前没有 README。Python 要求为 `>=3.13`；工作区直接依赖为 `langchain`、`langchain-openai`、`python-dotenv`。不要为本教学约定额外增加依赖。
- Git 历史体现了基础问答 → Prompt / LCEL → 保存章节与读取资料 → 手写 Tool Loop → 带参数章节工具 → 状态读取 → 多文件组织与 `create_agent()` → 写入本地的进度。
- 手写 Loop 可在提交 `f58ee95` 的 `main.py` 中回看；`9eb6715` 引入现有多文件结构；当前 HEAD `cfa8f5a` 增加写入工具。
- 当前已实现世界观、人物、大纲、指定章节和小说状态的 Read Tool。
- `write_chapter` 已实现并注册，通过 `exists()` 检查避免常规单进程流程覆盖已有章节；尚不能把它描述为并发安全或完整错误处理。
- `update_novel_state` 已定义并带 `@tool`，但尚未加入 `tools` 列表，因此当前 Agent 无法调用它。Prompt 提到了它，不等于工具已经注册。
- “先保存章节，再更新状态”目前主要写在 Prompt 中；状态更新工具尚未在代码层面校验目标章节、保存结果和进度推进是否合法，写入闭环仍未完成。
- `current_chapter` 按“已保存的最新章节号”理解，下一章通常是它加一；快照中值为 2。`location` 仍为“山村”，而第 2 章已写到青云宗，说明状态与正文还需要一致性检查；不要擅自改正文或猜测后直接修状态。
- 已有 `stream_mode="updates"` 和 `debug=True`，可以观察模型请求的工具名称、参数及工具返回结果。这些输出不等于读取模型私有思维过程。
- 尚未实现数据库存储、RAG、应用显式使用的持久记忆、调度、完整恢复流程和测试体系。
- `uv.lock` 中出现 LangGraph 等间接依赖，不代表用户已经学习或需要直接编写 LangGraph 工作流。保留当前 `create_agent()` 用法，避免提前教学其底层图编排。
- 本次开始时 `.env.example`、`.gitignore`、`model.py`、`pyproject.toml`、`uv.lock` 已有暂存或未暂存修改；后续以最新 `git status` 为准，不覆盖、回退或顺手提交用户已有工作。

当前最适合的下一小步：理解 **Tool 定义与注册的区别，以及 Write Tool 的副作用**，最小修改是把 `update_novel_state` 加入 `tools` 列表。通过现有 stream 观察 Agent 是否先成功保存，再更新进度；明确仅注册工具不等于已解决状态一致性。随后另开小步骤学习代码层面的状态更新校验。

## 五、逐步学习的技术路线

下面是路线，不是本次待办清单。按实际需要逐步引入，不一次全部实现。已经接触过的部分通过实际使用加深理解，不必从头重复。

### 阶段 1：完成当前基础 Agent

Read Tool、Write Tool、Side Effect（副作用）、`write_chapter`、`update_novel_state`、防止章节覆盖、状态一致性、错误处理、Agent 执行过程观察。

当前处于这一阶段。先补齐写入与更新进度的闭环，再逐步验证重复写入、写入失败、状态更新失败等情况。Prompt 中的规则不能代替代码对关键写入条件的校验。

### 阶段 2：Python 项目基础

Python module、多文件组织、exception、logging、基础测试 pytest、环境变量管理、配置管理。`dataclass` / Pydantic 有实际需要时再学。

当前已经拆分文件并使用 dotenv，不要为学习这些概念重新搭建架构；在现有实现上逐步解释和完善。Git 历史出现过 try / except，但仍需结合当前失败场景学习异常处理。

### 阶段 3：数据库基础

先使用 SQLite 学习 SQL 和 SQLAlchemy ORM，理解后再迁移 PostgreSQL。只学习 AI 应用开发常用的数据库知识，不以 DBA 为目标。

优先学习：

- `CREATE TABLE`、`INSERT`、`SELECT`、`WHERE`、`UPDATE`、`DELETE`。
- `ORDER BY`、`LIMIT`、简单 `JOIN`。
- primary key、unique、foreign key、index 的基本用途。
- transaction、migration。

解释表、行、约束、查询和事务如何对应当前章节与状态存储。不要同时引入 Repository Pattern、Service Layer、Dependency Injection。

不要主动深入存储过程、复杂触发器、分库分表、主从复制、高级锁机制、深度执行计划优化和 DBA 运维。

### 阶段 4：RAG / 向量数据库

Embedding、文本切片 chunk、向量、相似度搜索、PostgreSQL、pgvector、metadata、similarity search、LangChain Retriever、RAG。

必须结合小说解释清楚：

- 章节变多后，为什么全部放入 Prompt 会遇到上下文长度、费用和相关性问题。
- 为什么需要 Embedding：用数值表示文本特征，帮助找出语义相关内容。
- pgvector 实际存储的是向量数值；正文和 metadata 需要另有相应字段或存储位置，pgvector 本身不会替用户生成 Embedding。
- 普通 SQL 查询通常按章节号、字段、条件等精确筛选；向量检索按相似度寻找内容。RAG 是检索后把相关内容交给模型生成的流程，可结合两种查询方式。

### 阶段 5：Agent 状态与记忆

short-term state、long-term memory、conversation / run state。区分小说业务进度、一次运行中的消息与工具结果，以及跨运行保留的记忆。

LangGraph / checkpointer 只在确实需要持久化运行状态、恢复或更复杂流程时引入，不提前改写当前 Agent。

### 阶段 6：自动化

CLI、配置小说任务、每天自动运行、macOS cron / launchd 或其他简单调度方案、重试、失败恢复、日志、人工审核。

先验证单次任务稳定，再引入定时任务。重试必须考虑章节可能已保存、状态却未更新的情况，不能盲目重复写入或覆盖。

### 阶段 7：进一步工程化

只有项目发展到确实需要时，再学习 async / await、structured output、Pydantic、dependency injection、更完善的测试、Docker、API 服务、Web UI。

不因为依赖内部使用这些技术，就要求用户现在全部掌握。

## 六、代码修改与验证规则

每次修改前：

1. 阅读当前实现和相关 Git 状态，确认已有修改及本次任务范围。
2. 判断当前学习阶段，并明确告诉用户“这一阶段主要学习什么”。
3. 先解释思路，再提供或修改最小代码。
4. 尽量只改与本次知识点有关的代码，不顺手重构无关部分。
5. 不因“更专业”加入尚未学习的抽象，一次最好只增加 1～2 个新概念。

发现已有问题时，先说明问题是什么、为什么有影响，再给最小修复方案。不要直接替换用户正在学习的整个实现；用户要求仅讨论或仅改文档时，不修改业务代码。

验证规则：

- 当前路径基于仓库根目录；运行示例优先说明在根目录执行，例如 `uv run main.py`。
- `main.py` 会调用模型，并可能真实保存章节；不能把它当作无副作用的检查命令。执行前说明将写哪些文件、预期结果是什么。
- 测试写入失败、重复写入和状态变更时，优先使用临时目录或测试副本，保护正式小说文件；不要为测试覆盖已有正文。
- 给用户最小验证步骤；若 Codex 自己做了检查，说明检查范围，不把未执行的模型调用或写入闭环说成已通过。
- 仅修改文档时做文档与差异检查，不为验证文档启动 Agent、调用付费 API 或更新小说进度。
- 完成一个知识点后建议一次小的 Git commit，说明建议提交哪些文件。不自动提交用户无关修改；除非用户要求，不代替用户执行 commit。

## 七、保护已验证的学习成果

用户已经通过手写 Agent Loop 理解底层机制。虽然当前使用 `create_agent()`，不要删除这段学习背景，也不要把 Agent 描述为“魔法”。

解释 `create_agent()` 时，始终能对应回：

`bind_tools` → model invoke → `tool_calls` → `tool.invoke` → `ToolMessage` → loop。

这是机制对应关系，不声称框架内部源码与手写循环逐行相同。LLM 负责提出工具调用请求，Python 程序负责执行工具；工具必须注册给 Agent 才能被使用。

框架隐藏过程时，优先通过现有 stream / debug 输出，以及后续按需引入的 logging，让用户看到调用名称、参数、结果、失败位置和结束条件。

## 八、禁止行为与写入约束

不要：

- 一次性完成整个项目，或未经用户要求大规模重构架构。
- 过早引入 LangGraph 工作流、微服务、复杂设计模式。
- 为减少代码行数牺牲可读性，或大量使用用户尚未学习的 Python 高级语法。
- 省略关键教学解释，直接堆出用户不能理解的代码。
- 把 API Key 写进源码、日志或文档；把 `.env` 提交 Git。`.env.example` 只放变量名与安全占位值，不复制真实密钥。
- 覆盖已经存在的小说章节。
- 未确认目标章节成功保存，就更新 `current_chapter`。返回一段文字或模型声称“成功”不能替代实际保存成功的确认。
- 将失败、拒绝覆盖、部分完成的任务描述为完整成功。章节保存成功但状态更新失败时，明确报告并逐步恢复，不重新覆盖章节。
- 把数据库、RAG 和 Agent Memory 混为同一个概念：数据库负责存储与查询，RAG 负责检索辅助生成，记忆负责跨步骤或跨运行保留哪些信息；它们可以配合使用。
- 擅自回退、覆盖、暂存或提交用户已有的无关修改。

## 九、回答风格与架构原则

回答使用中文，尽量通俗，多用 JS / TS 类比。先解释思路，再写代码；一次聚焦一个主题，给可直接运行的最小示例、命令和预期结果，明确当前学习重点。完成一个知识点后建议一次 Git commit。

用户说“继续下一步”时，先读取最新代码与 Git 状态，再根据本文件和用户验证情况选择一个小步骤，不凭空延续旧快照。

目前保持 `main.py`、`agent.py`、`model.py`、`tools.py`、`novel/` 的简单结构。只有单个文件明显变复杂、具体职责混杂或重复代码确实妨碍理解时，再解释问题并逐步拆分。

不要提前创建大量 `services/`、`repositories/`、`domain/`、`infrastructure/`、`interfaces/`、`adapters/` 等目录。以后确有需要，再一边解释架构问题一边引入。

## 十、成功标准

成功不仅是程序能运行，也包括用户能够解释：

- LLM 如何请求 Tool，程序如何执行并返回结果。
- Agent 为什么需要 Loop，`create_agent()` 封装了什么。
- Agent 如何管理状态，如何确保章节与进度一致。
- 文件存储与数据库存储的区别、ORM 的作用、常用 SQL 如何工作。
- Embedding 是什么、pgvector 是什么、RAG 为什么存在。
- 长短期记忆有什么区别。
- 如何让 Agent 稳定地自动执行任务，包括失败后如何恢复。

如果功能做出来了，但用户完全不知道为什么这样做，这个知识点仍未完成。以最小实现、可观察过程、用户验证和理解为推进依据。
