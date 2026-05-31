# SP-22: CI/CD 与部署

## 元信息

| 属性 | 值 |
|------|-----|
| 子计划编号 | SP-22 |
| 对应全局任务 | T-22 |
| 对应结果蓝图章节 | 非功能终态-部署 |
| 前置依赖子计划 | SP-01~SP-21 |
| 输出产物 | Docker 镜像 + CI 配置 + 部署文档 |
| 执行Agent | DevOps |
| 预估复杂度 | 中 |

## 最终结果（来自结果蓝图）

### 要实现的内容

**Docker 化**：
- `Dockerfile`：FastAPI + AI 引擎（Embedding 模型 + Chroma）
- `docker-compose.yml`：FastAPI + Chroma + Redis + Ollama

**CI 流程（GitHub Actions）**：
- push → lint → typecheck → pytest → build image

**部署文档**：
- 开发环境启动指南（本机）
- 生产环境部署步骤（Nginx + systemd）

### 验收标准

| 蓝图项 | 验收条件 | 状态 |
|--------|---------|------|
| Dockerfile | `docker build` 成功，镜像可运行 | ⬜ |
| docker-compose | `docker-compose up` 一键启动全部服务 | ⬜ |
| CI 流程 | push 触发，lint+typecheck+test+build 全通过 | ⬜ |
| 部署文档 | 开发/生产环境部署步骤完整 | ⬜ |

## 上下文信息

### 输入依赖

| 输入项 | 来源 | 说明 |
|--------|------|------|
| 全部项目代码 | SP-01~SP-20 | 打包部署 |
| 测试 | SP-21 | CI 中运行 |

## 执行步骤

| 步骤 | 操作描述 | 预期中间产物 | 参考蓝图项 |
|------|---------|-------------|-----------|
| 1 | 创建 Dockerfile（多阶段构建：依赖安装→代码→启动） | Dockerfile | 6.1 部署架构 |
| 2 | 创建 docker-compose.yml（app + chroma + redis + ollama） | docker-compose.yml | 6.1 |
| 3 | 创建 .dockerignore | .dockerignore | — |
| 4 | 创建 GitHub Actions CI 配置（.github/workflows/ci.yml） | CI 配置 | 6.2 CI/CD |
| 5 | 编写开发环境启动指南（README.md 或 deploy-guide.md） | 开发指南 | — |
| 6 | 编写生产环境部署文档（Nginx + systemd + 环境变量） | 生产指南 | — |

## 完成标志

- [ ] Docker 镜像构建成功
- [ ] docker-compose 一键启动正常
- [ ] CI 流程 push 后自动运行
- [ ] 逐项验证报告 `plan/2026-05-29/verification-sp-22-report.md` 已生成并填写

---

> 本子计划依据结果蓝图 `agent-doc/result-first/project-final-state.md` 制定。
> 对齐 `.opencode/AGENTS.md` v2：计划驱动 — 独立子计划文件 + 结果蓝图直引 + 逐项验证
