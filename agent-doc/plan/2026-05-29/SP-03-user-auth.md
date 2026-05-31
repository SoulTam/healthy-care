# SP-03: 用户认证系统

## 元信息

| 属性 | 值 |
|------|-----|
| 子计划编号 | SP-03 |
| 对应全局任务 | T-03 |
| 对应结果蓝图章节 | 后端API-认证鉴权, 数据表-users/user_sessions |
| 前置依赖子计划 | SP-01 |
| 输出产物 | `app/user/models.py`, `app/user/schemas.py`, `app/user/router.py`, `app/user/service.py` |
| 执行Agent | 后端Dev |
| 预估复杂度 | 中 |

## 最终结果（来自结果蓝图）

### 要实现的内容

**数据表 `users`**：
| 字段 | 类型 | 约束 |
|------|------|------|
| id | UUID | PK, default gen_random_uuid() |
| phone | VARCHAR(20) | UNIQUE NOT NULL |
| password_hash | VARCHAR(256) | |
| nickname | VARCHAR(50) | |
| avatar_url | VARCHAR(500) | |
| gender | ENUM('male','female','other') | DEFAULT 'other' |
| birthday | DATE | |
| region | VARCHAR(100) | |
| wechat_openid | VARCHAR(100) | UNIQUE |
| font_size | ENUM('normal','large') | DEFAULT 'normal' |
| status | ENUM('active','disabled','deleted') | DEFAULT 'active' |
| last_login_at | TIMESTAMP | |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | |
| deleted_at | TIMESTAMP | |

**数据表 `user_sessions`**：
| 字段 | 类型 | 约束 |
|------|------|------|
| id | UUID | PK |
| user_id | UUID | FK→users, ON DELETE CASCADE |
| token | VARCHAR(500) | NOT NULL |
| refresh_token | VARCHAR(500) | NOT NULL |
| expires_at | TIMESTAMP | NOT NULL |
| created_at | TIMESTAMP | |

**API**：
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/auth/send-code` | POST | 发送短信验证码（开发阶段直接返回验证码） |
| `/api/v1/auth/login` | POST | 验证码登录 |
| `/api/v1/auth/login-password` | POST | 密码登录 |
| `/api/v1/auth/register` | POST | 注册 |
| `/api/v1/auth/reset-password` | POST | 重置密码 |
| `/api/v1/auth/refresh` | POST | 刷新 token |
| `/api/v1/auth/logout` | POST | 退出登录 |
| `/api/v1/auth/wechat-login` | POST | 微信登录 |

### 验收标准

| 蓝图项 | 验收条件 | 状态 |
|--------|---------|------|
| users 表 | 创建成功，唯一约束正常 | ⬜ |
| user_sessions 表 | 创建成功，外键正常 | ⬜ |
| 注册 | 手机号+验证码+密码 → 创建用户 → 返回 token | ⬜ |
| 登录 | 验证码登录和密码登录均正常 | ⬜ |
| Token 鉴权 | 请求带 token 正常，不带返回 401 | ⬜ |
| Token 刷新 | refresh_token 可换取新 token | ⬜ |
| 退出登录 | token 失效 | ⬜ |
| 密码加密 | bcrypt 哈希，不存明文 | ⬜ |

## 上下文信息

### 输入依赖

| 输入项 | 来源 | 说明 |
|--------|------|------|
| 数据库会话 | SP-01 | `app/core/database.py` |
| JWT 工具 | SP-01 | `app/core/auth.py` |
| 依赖注入 | SP-01 | `app/core/dependencies.py` |

### 相关设计文档引用

| 文档 | 相关章节 |
|------|---------|
| `project-final-state.md` | 2.2 API-认证鉴权, 3.2 表-users/user_sessions |

## 执行步骤

| 步骤 | 操作描述 | 预期中间产物 | 参考蓝图项 |
|------|---------|-------------|-----------|
| 1 | 定义 User + UserSession SQLAlchemy 模型 | `models.py` | 3.2 users/user_sessions |
| 2 | 定义 Pydantic schema（RegisterRequest, LoginRequest, TokenResponse 等） | `schemas.py` | — |
| 3 | 实现 UserService：register, login, send_code, refresh_token, logout | `service.py` | — |
| 4 | 实现 Auth router 注册所有认证端点 | `router.py` | 2.2 认证鉴权 |
| 5 | 在 `main.py` 中注册 `app/user/router.py` | 路由注册 | — |
| 6 | pytest 测试：注册→登录→访问受保护接口→refresh→logout | 测试用例 | — |

## 完成标志

- [ ] 8 个认证接口全部实现且可用
- [ ] 注册→登录→鉴权→退出的端到端流程正常
- [ ] 测试通过
- [ ] 逐项验证报告 `plan/2026-05-29/verification-sp-03-report.md` 已生成并填写

---

> 本子计划依据结果蓝图 `agent-doc/result-first/project-final-state.md` 制定。
> 对齐 `.opencode/AGENTS.md` v2：计划驱动 — 独立子计划文件 + 结果蓝图直引 + 逐项验证
