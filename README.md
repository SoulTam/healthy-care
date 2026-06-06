# 中医食补健康助手 (HealthyCare)

基于 **中医体质辨证** 与 **AI 智能推荐** 的个性化食补方案应用。用户通过体质评估获取中医体质类型，系统结合体质、季节、症状等信息智能推荐匹配的食疗食谱，并支持多轮对话问诊、方案替换、反馈闭环等完整功能。

---

## 功能特性

### 🩺 体质评估
- **问卷模式**：10 道标准化问题，覆盖九种中医体质（平和/气虚/阳虚/阴虚/痰湿/湿热/血瘀/气郁/特禀）
- **AI 对话问诊**：与 AI 中医师多轮对话，系统收集症状后自动汇总评估
- **体质趋势追踪**：历次评估记录可视化，趋势变化一目了然

### 🍲 智能食补方案
- **体质匹配**：根据体质+季节+症状多维匹配，生成每日食补方案（早/午/晚餐+加餐）
- **方案替换**：不满意可替换单道食谱，AI 推荐同类替代
- **食谱搜索**：支持关键词、体质、季节、症状等多维度语义搜索

### 📚 内容百科
- **食材百科**：性味归经、功效、禁忌、营养成分全面展示
- **养生课堂**：按主题分类的养生知识卡片
- **古籍出处**：食谱均引用《金匮要略》《随息居饮食谱》等中医典籍

### 🔄 反馈闭环
- **方案评价**：对食补方案评分 + 症状变化记录
- **AI 解读**：分析反馈内容，评估改善效果
- **体质动态调整**：根据反馈证据微调体质评估

### 👤 用户中心
- 个人信息管理（头像/昵称/性别/生日/地域）
- 饮食禁忌设置（过敏/宗教/孕期）
- 收藏管理（食谱/知识）
- 大字体模式

---

## 技术架构

```
healthy-care/
├── app/                    # 后端应用模块
│   ├── core/               #   核心：配置/数据库/鉴权/异常/依赖
│   ├── user/               #   用户认证 + 资料管理
│   ├── constitution/       #   体质评估 + AI 对话
│   ├── diet/               #   食谱模型 + 方案生成
│   ├── content/            #   内容百科 + 知识库
│   ├── feedback/           #   反馈闭环
│   ├── search/             #   食谱搜索
│   ├── favorite/           #   收藏服务
│   └── admin/              #   管理后台日志
├── engine/                 # AI 引擎
│   ├── llm/                #   LLM 客户端 (Ollama)
│   ├── embedding/          #   向量化 (BGE-small-zh)
│   └── retrieval/          #   向量检索 (ChromaDB)
├── src/                    # v0.2 语义检索引擎 (Whoosh + BM25 + BGE)
├── tests/                  # pytest 测试
├── data/                   # 数据目录 (Chroma 等运行时数据)
├── scripts/                # 脚本 + 部署文档
├── main.py                 # FastAPI 入口
├── Dockerfile              # Docker 构建
└── docker-compose.yml      # 容器编排
```

### 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI (Python 3.12+) |
| 数据库 | PostgreSQL (开发/生产统一) |
| ORM | SQLAlchemy 2.0 (async) |
| 向量数据库 | ChromaDB |
| AI 引擎 | Ollama + Qwen2.5 / BGE-small-zh |
| 前端 | React Native (骨架) |
| 测试 | pytest + httpx |
| 部署 | Docker + GitHub Actions CI |

### API 一览

| 模块 | 端点 | 说明 |
|------|------|------|
| 认证 | `/api/v1/auth/*` | 注册/登录/刷新/退出/重置密码 (8 个) |
| 用户 | `/api/v1/user/*` | 资料/饮食禁忌/注销 (5 个) |
| 体质 | `/api/v1/constitution/*` | 问卷/评估/报告/趋势/对话 (8 个) |
| 方案 | `/api/v1/diet/plan/*` | 生成/替换 (2 个) |
| 搜索 | `/api/v1/search/*` | 食谱搜索/全局搜索/热门 (3 个) |
| 收藏 | `/api/v1/favorite/*` | 列表/切换/检查 (3 个) |
| 入库 | `/api/v1/retrieval/*` | 食谱入库/知识入库/批量/统计 (4 个) |
| 反馈 | `/api/v1/feedback/*` | 提交/历史/AI 解读 (3 个) |

---

## 快速开始

### 环境要求

- Python 3.12+
- pip
- PostgreSQL 16+（本机运行）或 Docker & Docker Compose（推荐）
- （可选）Ollama（本地 LLM 推理，AI 对话/反馈解读等功能需要）

### 安装 Ollama（本地 LLM）

```bash
# 方式一：直接安装（Windows / macOS / Linux）
# 访问 https://ollama.com/download 下载安装包

# 方式二：Docker 安装
docker run -d -p 11434:11434 --name ollama ollama/ollama

# 拉取 Qwen2.5 7B 模型
docker exec ollama ollama pull qwen2.5:7b
# 或直接安装时拉取：
ollama pull qwen2.5:7b

# 验证模型可用
ollama run qwen2.5:7b "你好，请用一句话介绍中医食疗"
```

Ollama 默认监听 `http://localhost:11434`，在 `.env` 中配置即可被应用识别。

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，按需修改配置
```

开发和生产统一使用 PostgreSQL。默认 `.env` 连接本机 PostgreSQL：

```env
DATABASE_URL=postgresql+asyncpg://healthy_care:healthy_care@localhost:5432/healthy_care
```

如使用 Docker Compose 启动，应用容器会自动覆盖为 `postgres` 服务地址。

### 3. 启动 PostgreSQL

```bash
# 推荐：仅启动开发数据库
docker-compose up -d postgres

# 或使用本机 PostgreSQL，自行创建数据库与用户：
# database: healthy_care
# user/password: healthy_care/healthy_care
```

### 4. 启动服务

```bash
# 开发模式（热重载）
python -m uvicorn main:app --reload --port 8000

# 或使用启动脚本
python run_server.py
```

访问 http://localhost:8000/docs 查看 Swagger API 文档。

### 5. 验证服务

```bash
curl http://localhost:8000/health
# 返回: {"status":"ok","app":"HealthyCare","version":"1.0.0"}
```

### 启动 Ollama（可选，LLM 功能需要）

```bash
docker run -d -p 11434:11434 --name ollama ollama/ollama
docker exec ollama ollama pull qwen2.5:7b
```

---

## Docker 部署

### 环境要求

- [Docker](https://docs.docker.com/get-docker/) 24+
- [Docker Compose](https://docs.docker.com/compose/install/) v2.24+（通常随 Docker Desktop 一同安装）

> **Windows**：通过 PowerShell 安装 Docker Desktop：
> ```powershell
> # 使用 winget 安装 Docker Desktop
> winget install Docker.DockerDesktop
> 
> # 安装后启动 Docker Desktop
> Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
> 
> # 验证安装
> docker --version
> docker compose version
> ```
> 安装完成后在 Docker Desktop → Settings → Resources → WSL Integration 中启用你的 WSL 发行版。
>
> **Linux**：安装 Docker Engine 后，需额外安装 docker-compose-plugin：
> ```bash
> sudo apt-get install docker-compose-plugin
> ```
>
> **macOS**：安装 [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/) 即可。

### 1. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，如需修改数据库密码等配置
```

Docker Compose 会自动用 `postgres` 服务地址覆盖 `DATABASE_URL`，无需手动修改。

### 2. 一键启动全部服务

```bash
docker-compose up -d
```

这会同时启动以下容器：

| 服务 | 端口 | 说明 |
|------|------|------|
| app | `8000` | FastAPI 应用 |
| postgres | `5432` | PostgreSQL 数据库 |
| chroma | `8001` | ChromaDB 向量数据库 |
| ollama | `11434` | Ollama LLM 引擎（可选，拉取模型后生效） |

### 3. 初始化数据库（首次启动）

```bash
# 创建数据库表
docker-compose exec app alembic upgrade head

# 导入初始食谱数据
docker-compose exec app python scripts/seed_recipes.py
```

### 4. 拉取 LLM 模型（可选，AI 功能需要）

```bash
docker-compose exec ollama ollama pull qwen2.5:7b
```

### 5. 验证服务

```bash
curl http://localhost:8000/health
# 返回: {"status":"ok","app":"HealthyCare","version":"1.0.0"}
```

访问 http://localhost:8000/docs 查看 Swagger API 文档。

### 仅启动数据库（开发模式）

如果只需在本地开发时使用 Docker 运行数据库：

```bash
docker-compose up -d postgres chroma
```

### 常用命令

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看应用日志
docker-compose logs -f app

# 重启应用（代码变更后）
docker-compose restart app

# 停止所有服务
docker-compose down

# 停止并删除数据卷（⚠️ 会清空数据库）
docker-compose down -v

# 重新构建镜像（依赖变更时）
docker-compose build app
```

---

## 运行测试

```bash
python -m pytest tests/ -v
```

---

## API 使用示例

### 注册用户

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138000","code":"123456","password":"mypassword","nickname":"测试用户"}'
```

### 体质评估

```bash
# 获取问卷
curl http://localhost:8000/api/v1/constitution/questions

# 提交评估
curl -X POST http://localhost:8000/api/v1/constitution/assess \
  -H "Content-Type: application/json" \
  -d '{"answers":{"1":0,"2":0,"3":3,"4":3,"5":0,"6":0,"7":0,"8":0,"9":0,"10":0}}'
```

### 生成食补方案

```bash
curl -X POST http://localhost:8000/api/v1/diet/plan/generate \
  -H "Content-Type: application/json" \
  -d '{"query":"阴虚体质秋季调理","days":3}'
```

### 搜索食谱

```bash
curl "http://localhost:8000/api/v1/search/recipes?q=阴虚失眠&top_k=5"
```

---

## 项目结构

| 目录/文件 | 说明 |
|-----------|------|
| `main.py` | FastAPI 应用入口，路由注册 |
| `app/core/` | 核心模块（配置/数据库/鉴权/异常/依赖） |
| `app/user/` | 用户认证 + 资料管理 |
| `app/constitution/` | 体质评估（问卷/对话/算法/报告/趋势） |
| `app/diet/` | 食谱模型 + 方案生成 |
| `app/content/` | 内容百科 + 知识库 |
| `app/feedback/` | 反馈闭环 |
| `app/favorite/` | 收藏服务 |
| `app/search/` | 食谱搜索 |
| `app/admin/` | 管理日志 |
| `engine/llm/` | LLM 客户端（Ollama API 封装 + 提示词模板） |
| `engine/embedding/` | 文本向量化（BGE-small-zh） |
| `engine/retrieval/` | 向量检索（ChromaDB 封装） |
| `src/` | 语义检索引擎（Whoosh BM25 + BGE 混合检索） |
| `tests/` | 自动化测试 |
| `data/recipes.json` | 初始食谱数据（18 道） |
| `data/` | 运行时数据（Chroma 持久化等） |
| `agent-doc/` | 项目文档（蓝图/计划/验证报告） |

---

## 版本历史

- **v0.2** — 原型：BM25 + BGE 嵌入 + 元数据过滤检索引擎
- **v1.0** — 完整版：用户系统 + 体质评估 + AI 对话 + 食补方案 + 反馈闭环 + 部署就绪
