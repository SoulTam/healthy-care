# 阶段路由器 + 强制输出模板

**每次收到消息，按以下步骤执行：**
1. 读取 `agent-doc/workflow-status.md`，找到 `当前阶段`
2. 找到下面与该阶段对应的模板，输出完整内容（填充所有字段），不得添加模板外的内容
3. 将模板完整内容保存到对应文件（路径见各阶段输出规范）
4. 更新 `agent-doc/workflow-status.md`
5. 回复结束后自动执行 Git 提交（`git add . && git commit -m "类型(范围): 描述"`）

> 所有模板均为强制。禁止用"..."、"略"、"同上"等省略。聊天窗口输出 + 文件保存两者缺一不可。

---

## 仓库速查

### 核心命令
```bash
pip install -r requirements.txt         # 安装依赖
python -m pytest tests/ -v              # 运行全部测试
python -m pytest tests/test_algorithm.py -v  # 单文件测试（无需 DB）
python -m uvicorn main:app --reload --port 8000  # 开发服务器
python run_server.py                    # 启动脚本
docker-compose up -d postgres chroma    # 仅启动基础设施
docker-compose up -d                    # 启动全部服务（app + postgres + chroma + ollama）
```

### 架构要点
- **入口**: `main.py` — FastAPI 应用，路由在 `startup` 事件中注册，`app/core/config.py` 的 `Settings` 类从 `.env` 读取配置
- **双代引擎**: `app/` (v1.0, FastAPI + SQLAlchemy async + PostgreSQL) 和 `src/` (v0.2, Whoosh BM25 + BGE 混合检索)
- **测试**: pytest + httpx `AsyncClient` + `ASGITransport`（无需启动服务器）；`conftest.py` 导入了 `main` 模块（会初始化搜索引擎和 Chroma），使用 `sys.path.insert(0, ...)` 保证导入路径
- **数据库**: PostgreSQL 16+，SQLAlchemy 2.0 async，无 `Base.metadata.create_all` 调用；alembic 在 requirements.txt 中但未初始化（无 `alembic.ini` 或 `alembic/` 目录）
- **AI 引擎**: Ollama LLM (qwen2.5:7b) + ChromaDB + BGE-small-zh 嵌入

### 测试注意事项
- `test_api.py` 需要 PostgreSQL 运行中且数据库已创建（否则 500 错误）
- `test_algorithm.py` 和 `test_combine.py` 是纯逻辑测试，无需数据库
- 手动调试脚本: `test_api.py` (requests，需要服务器运行中)、`test_phase2.py` (直接导入，无需服务器)
- 必要数据文件: `data/recipes.json` (18道食谱)、`index/` (Whoosh 索引目录)

### 代码约定
- `from __future__ import annotations` 在所有文件开头
- 所有服务类都带 `from pydantic_settings import BaseSettings`
- 配置文件: `app/core/config.py`，所有配置项大写
- 认证: bcrypt 密码哈希 + python-jose JWT

---

## 阶段：未开始 / 提示词增强

输出 `提示词工程师 Agent — 请求增强` 模板，分析意图、模糊点、结构化需求。用户确认后 → 更新状态至 `结果先行定义`。

**输出规范**：仅聊天窗口展示，无需保存文件。用户确认后将结构化请求保存到 `agent-doc/user-request/{日期}-{简述}.md`。

---

## 阶段：结果先行定义

依次调用 4 个 Agent（需求分析、架构设计、功能设计、技术设计）产出各自维度终态，最后做交叉校验 + 15项自检 + 覆盖矩阵。

**输出规范**：完整结果蓝图保存到 `agent-doc/result-first/{yyyy-MM-dd}-{seq}-{需求简述}-result-blueprint.md`。

用户确认后 → 更新状态至 `计划拆分`。

---

## 阶段：计划拆分

产出架构设计、技术设计、功能设计、开发规范 4 份文档 + 里程碑排期 + 子计划文件 + 进度表。

**输出规范**：
- 架构设计 → `agent-doc/architecture/{yyyy-MM-dd}-{seq}-{项目}-architecture.md`
- 技术设计 → `agent-doc/technical-design/{yyyy-MM-dd}-{seq}-{项目}-technical-design.md`
- 功能设计 → `agent-doc/feature-design/{yyyy-MM-dd}-{seq}-{项目}-feature-design.md`
- 开发规范 → `agent-doc/dev-plan/{yyyy-MM-dd}-{seq}-{项目}-dev-standards.md`
- 全局执行计划概览 → `agent-doc/plan/{yyyy-MM-dd}-global-execution-plan.md`
- 子计划文件 → `agent-doc/plan/{确认日期}/SP-XX-{名称}.md`（每个任务独立文件）
- 进度追踪 → `agent-doc/plan/{确认日期}/progress.md`

更新状态至 `覆盖核查`。

---

## 阶段：覆盖核查

核查 Agent 执行蓝图→子计划覆盖核查。核查报告保存到 `agent-doc/plan/{当前日期}/verification-coverage-report.md`。

通过 → 更新状态至 `子计划执行`。有遗漏 → 通知 PM Agent 修正后重新核查。

---

## 阶段：子计划执行

执行经理模式，逐个子计划执行。每完成 3 个子计划自动 Git 提交（`auto: SP-{起始} to SP-{结束} 子计划完成`）。产出物保存到 `agent-doc/code/`。

全部完成 → 更新状态至 `终态校验`。

---

## 阶段：子计划核查

逐行核查子计划产出。核查报告保存到 `agent-doc/plan/{当前日期}/verification-sp-xx-report.md`。

---

## 阶段：终态校验

重新读取蓝图，逐项检查所有内容是否被子计划涵盖。报告保存到 `agent-doc/result-first/{yyyy-MM-dd}-{seq}-verification-final-report.md`。

无遗漏 → 通知用户终态检查。有遗漏 → 通知 PM Agent 修复后重新检查。全部完成 → 更新状态至 `已完成`。

---

## 阶段：合规稽查

子计划执行后触发，稽查报告保存到 `agent-doc/audit/{日期}-{阶段}-audit-report.md`。

## 输出规范（所有阶段适用）

- 每条回复必须使用模板格式，不得自由发挥
- 禁止使用"..."、"略"、"同上"、"参考XX"等省略表述
- 每次回复结束后，更新 `agent-doc/workflow-status.md`
- 每个模板填充完毕后，必须将完整内容保存到对应文件
- 每次回复结束后，必须执行 Git 提交（Conventional Commits 格式）
