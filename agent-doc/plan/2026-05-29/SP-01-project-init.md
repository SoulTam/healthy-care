# SP-01: 项目基础设施搭建

## 元信息

| 属性 | 值 |
|------|-----|
| 子计划编号 | SP-01 |
| 对应全局任务 | T-01 |
| 对应结果蓝图章节 | 技术架构/部署/配置管理 |
| 前置依赖子计划 | 无 |
| 输出产物 | `main.py`, `app/core/`, `requirements.txt`, 项目骨架, `admin_operation_logs` / `index_maintenance_logs` 表模型 |
| 执行Agent | PM/DevOps |
| 预估复杂度 | 低 |

## 最终结果（来自结果蓝图）

### 要实现的内容

创建项目骨架，包含：
- `app/` - 应用主包
  - `core/` - 核心模块（config, database, auth, exceptions, schemas, dependencies）
  - `user/` - 用户模块（初始空）
  - `constitution/` - 体质模块
  - `diet/` - 食补方案模块
  - `content/` - 内容模块
  - `feedback/` - 反馈模块
  - `community/` - 社区模块
  - `notification/` - 通知模块
  - `favorite/` - 收藏模块
  - `search/` - 搜索模块
  - `family/` - 家庭模块
  - `admin/` - 管理后台
- `engine/` - AI 引擎
  - `llm/` - LLM 服务
  - `embedding/` - 嵌入服务
  - `retrieval/` - 检索服务
- `data/` - 数据目录（SQLite, Chroma）
- `tests/` - 测试目录
- `scripts/` - 工具脚本

**日志表定义**（蓝图 §3.2）：

**admin_operation_logs** - 管理员操作日志
| 列名 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 主键 |
| admin_id | INT | NOT NULL | 操作管理员ID |
| action | VARCHAR(100) | NOT NULL | 操作类型（如 update_recipe, delete_user） |
| target_type | VARCHAR(50) | NOT NULL | 操作对象类型 |
| target_id | INT |  | 操作对象ID |
| detail | TEXT |  | 操作详情（JSON） |
| ip_address | VARCHAR(45) |  | 操作者IP |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 操作时间 |

**index_maintenance_logs** - 索引维护日志
| 列名 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 主键 |
| index_type | VARCHAR(50) | NOT NULL | 索引类型（chroma, postgres_fts, materialized_view） |
| action | VARCHAR(50) | NOT NULL | 操作（full_rebuild, incremental_update, cleanup） |
| status | VARCHAR(20) | NOT NULL | 状态（running, success, failed） |
| started_at | DATETIME | NOT NULL | 开始时间 |
| finished_at | DATETIME |  | 结束时间 |
| records_processed | INT | DEFAULT 0 | 处理记录数 |
| error_message | TEXT |  | 错误信息 |
| triggered_by | VARCHAR(50) |  | 触发方式（manual, scheduled, hook） |

### 验收标准

| 蓝图项 | 验收条件 | 状态 |
|--------|---------|------|
| FastAPI 项目 | `uvicorn main:app` 可启动，访问 `/health` 返回 200 | ⬜ |
| 数据库连接 | SQLAlchemy 引擎配置完成，可建表 | ⬜ |
| JWT 鉴权 | token 生成/验证/刷新函数可用 | ⬜ |
| 配置管理 | 环境变量 `.env` 加载，敏感信息无硬编码 | ⬜ |
| CORS | 配置允许跨域 | ⬜ |
| 全局异常处理 | 统一异常响应格式 `{"code","message","detail"}` | ⬜ |
| admin_operation_logs 表 | SQLAlchemy 模型定义 + alembic 迁移可生成 | ⬜ |
| index_maintenance_logs 表 | SQLAlchemy 模型定义 + alembic 迁移可生成 | ⬜ |

## 上下文信息

### 输入依赖

| 输入项 | 来源 | 说明 |
|--------|------|------|
| 架构设计 | `agent-doc/architecture/system-architecture.md` | 分层结构和模块划分 |
| 终态描述 | `agent-doc/result-first/project-final-state.md` | 完整项目终态 |

### 相关设计文档引用

| 文档 | 相关章节 |
|------|---------|
| `system-architecture.md` | 2.系统分层架构, 5.安全架构, 6.部署架构, 7.配置管理 |

## 执行步骤

| 步骤 | 操作描述 | 预期中间产物 | 参考蓝图项 |
|------|---------|-------------|-----------|
| 1 | 创建目录结构：`app/`(含各模块子包+`__init__.py`)、`engine/`、`data/`、`tests/`、`scripts/` | 目录骨架 | 架构-分层 |
| 2 | 创建 `main.py`：FastAPI app 实例、CORS 中间件、路由注册入口、`/health` 端点 | 可启动的 FastAPI | 架构-应用层 |
| 3 | 创建 `app/core/config.py`：pydantic-settings 加载 `.env`，所有敏感信息来自环境变量 | 配置模块 | 架构-配置管理 |
| 4 | 创建 `app/core/database.py`：SQLAlchemy async engine + sessionmaker + Base + get_db 依赖 | 数据库会话 | 数据层 |
| 5 | 创建 `app/core/auth.py`：JWT 生成/验证/刷新函数、密码 bcrypt 哈希 | 鉴权模块 | 架构-安全 |
| 6 | 创建 `app/core/dependencies.py`：get_current_user 依赖注入 | 依赖注入 | 架构-鉴权 |
| 7 | 创建 `app/core/exceptions.py`：全局异常定义 + 异常处理器 | 异常模块 | 架构-异常处理 |
| 8 | 创建 `app/core/schemas.py`：通用响应模型 `ResponseModel`、分页模型 | 通用响应 | 架构 |
| 9 | 创建 `requirements.txt`：fastapi, uvicorn, sqlalchemy, alembic, pyjwt, bcrypt, pydantic-settings, python-multipart | 依赖清单 | — |
| 10 | 创建 `app/admin/models.py`：admin_operation_logs + index_maintenance_logs 表模型 | 日志表模型 | 3.2 日志表 |

## 完成标志

- [ ] 所有验收标准已达成
- [ ] `uvicorn main:app` 可正常启动并响应 `/health`
- [ ] 目录结构符合架构设计
- [ ] admin_operation_logs 模型 + 迁移文件已生成
- [ ] index_maintenance_logs 模型 + 迁移文件已生成
- [ ] 逐项验证报告 `plan/2026-05-29/verification-sp-01-report.md` 已生成并填写

---

> 本子计划依据结果蓝图 `agent-doc/result-first/project-final-state.md` 制定。
> 如有任何偏差，以结果蓝图为最终判断标准。
> 对齐 `.opencode/AGENTS.md` v2：计划驱动 — 独立子计划文件 + 结果蓝图直引 + 逐项验证
