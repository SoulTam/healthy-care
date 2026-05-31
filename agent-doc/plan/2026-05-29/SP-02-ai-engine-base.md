# SP-02: AI 引擎基础设施

## 元信息

| 属性 | 值 |
|------|-----|
| 子计划编号 | SP-02 |
| 对应全局任务 | T-02 |
| 对应结果蓝图章节 | 技术选型-AI引擎层 |
| 前置依赖子计划 | SP-01 |
| 输出产物 | `engine/llm/`, `engine/embedding/`, `engine/retrieval/` 基础客户端 |
| 执行Agent | 后端Dev |
| 预估复杂度 | 中 |

## 最终结果（来自结果蓝图）

### 要实现的内容

LLM 服务（`engine/llm/client.py`）：
- Ollama HTTP API 封装
- 同步/异步调用
- SSE 流式响应支持
- 提示词模板管理
- 统一错误处理+重试

Embedding 服务（`engine/embedding/client.py`）：
- sentence-transformers 封装 BGE-small-zh
- 单文本/批量向量化
- CPU 推理配置

Chroma 客户端（`engine/retrieval/base.py`）：
- Chroma 持久化客户端
- collection 管理（食谱库/知识库）
- metadata 过滤搜索
- 向量相似度搜索

### 验收标准

| 蓝图项 | 验收条件 | 状态 |
|--------|---------|------|
| LLM 客户端 | 可调用 Ollama Qwen2.5 生成文本 | ⬜ |
| SSE 流式 | 支持 `StreamingResponse` 流式输出 | ⬜ |
| Embedding 客户端 | BGE-small-zh 加载成功，文本→向量(384维) | ⬜ |
| Chroma 客户端 | 创建/查询/删除 collection，支持 metadata 过滤 | ⬜ |
| 统一错误处理 | LLM/Ollama 不可用时优雅降级 | ⬜ |

## 上下文信息

### 输入依赖

| 输入项 | 来源 | 说明 |
|--------|------|------|
| 项目骨架 | SP-01 | `main.py`、配置模块 |
| 系统架构 | `agent-doc/architecture/system-architecture.md` | AI引擎层架构 |

## 执行步骤

| 步骤 | 操作描述 | 预期中间产物 | 参考蓝图项 |
|------|---------|-------------|-----------|
| 1 | 创建 `engine/llm/client.py`：封装 Ollama `/api/generate` 和 `/api/chat`，支持 `generate()` 和 `generate_stream()` 方法 | LLM客户端 | 5.4.1 LLM选型 |
| 2 | 创建 `engine/llm/prompts.py`：提示词模板（意图理解、反馈解读、报告生成、审核），使用 Jinja2 模板 | 提示词模板 | 5.1 AI引擎 |
| 3 | 创建 `engine/embedding/client.py`：sentence-transformers 加载 BGE-small-zh，`embed()` 单条 + `embed_batch()` 批量 | Embedding客户端 | 5.4.1 Embedding选型 |
| 4 | 创建 `engine/retrieval/base.py`：chromadb 持久化客户端，`get_or_create_collection()`，`similarity_search()` 支持 metadata filter | Chroma客户端 | 5.4.1 向量数据库 |
| 5 | 三项客户端注册到 `app/core/config.py` 作为 FastAPI 生命周期事件（startup/shutdown） | 引擎初始化 | 架构 |

## 完成标志

- [ ] LLM 调用正常，流式 SSE 工作
- [ ] Embedding 向量化正常（BGE-small-zh）
- [ ] Chroma 可创建 collection 并搜索
- [ ] 逐项验证报告 `plan/2026-05-29/verification-sp-02-report.md` 已生成并填写

---

> 本子计划依据结果蓝图 `agent-doc/result-first/project-final-state.md` 制定。
> 对齐 `.opencode/AGENTS.md` v2：计划驱动 — 独立子计划文件 + 结果蓝图直引 + 逐项验证
