# 中医食补应用 — 终态描述（结果先行）

> 版本：v1.0
> 状态：待确认
> 本文档定义项目达成交付时的完整终态，用户确认后方可进入设计和开发阶段。

---

## 1. 前端终态

### 1.1 页面结构与导航

```
App Shell（底部 Tab 导航）
├── 首页（Home）
│   ├── 当季推荐卡片
│   ├── 今日养生知识卡片
│   ├── 体质状态卡片（快捷入口→体质评估）
│   └── 快捷入口：体质评估 / 方案查看 / 食材百科
├── 食补方案（Plans）
│   ├── 方案列表（历史方案/当前方案）
│   ├── 方案详情（一日三餐/一周计划）
│   │   ├── 每餐卡片（含工笔食材插画）
│   │   └── 单餐替换操作
│   └── 食谱详情
│       ├── 食材清单 + 用量
│       ├── 烹饪步骤（竖线时间轴）
│       ├── 中医功效（性味归经）
│       ├── 营养数据
│       └── 禁忌提示
├── 社区（Community）— 二期
│   ├── 瀑布流卡片列表
│   ├── 分享发布
│   └── 评论互动
└── 我的（Profile）
    ├── 个人信息
    ├── 家庭成员管理（二期）
    ├── 体质变化趋势
    ├── 反馈记录
    └── 设置（大字体、离线、隐私）
```

### 1.2 核心页面 ASCII 线框图

```
=== 首页 ===
┌─────────────────────────────┐
│ [状态栏]         [⚙️]      │
│                            │
│  ☀️ 早上好，[用户名]        │
│  今日：秋分 · 宜滋阴润肺    │
│                            │
│ ┌─────────────────────┐    │
│ │ 🌿 今日体质状态      │    │
│ │ 阴虚质 (轻度偏颇)    │    │
│ │ ████████░░ 78分      │    │
│ │ [重新评估]           │    │
│ └─────────────────────┘    │
│                            │
│ ┌─────────────────────┐    │
│ │ 🍵 当季推荐          │    │
│ │ 百合莲子银耳羹       │    │
│ │ "滋阴润肺，秋季宜食" │    │
│ └─────────────────────┘    │
│                            │
│ ┌─────────────────────┐    │
│ │ 📖 今日养生知识       │    │
│ │ "秋燥时节，宜多食    │    │
│ │  梨、百合、银耳..."  │    │
│ └─────────────────────┘    │
│                            │
│ [首页] [方案] [社区] [我的] │
└─────────────────────────────┘
```

```
=== 体质评估 ===
┌─────────────────────────────┐
│ 体质评估           [✕]     │
│ ████████░░░░░ 进度 60%      │
│                            │
│ ┌─────────────────────┐    │
│ │                      │    │
│ │ 您最近是否经常感到    │    │
│ │ 口干舌燥？            │    │
│ │                      │    │
│ │ [○] 从不              │    │
│ │ [○] 偶尔              │    │
│ │ [○] 经常              │    │
│ │ [○] 总是              │    │
│ │                      │    │
│ └─────────────────────┘    │
│                            │
│         [←上一步] [下一步→] │
└─────────────────────────────┘
```

```
=== 食补方案（一日三餐）===
┌─────────────────────────────┐
│ < 今日方案          [🌐]    │
│ 2026-05-29 · 秋季 · 阴虚质  │
│                            │
│ ☀️ 早餐                      │
│ ┌─────────────────────┐    │
│ │ 🖼️ ［工笔插画］       │    │
│ │ 山药红枣粥            │    │
│ │ 功效：健脾益气滋阴     │    │
│ └─────────────────────┘    │
│                            │
│ 🌤️ 午餐                      │
│ ┌─────────────────────┐    │
│ │ 🖼️ ［工笔插画］       │    │
│ │ 枸杞百合炒西芹        │    │
│ │ + 米饭                │    │
│ └─────────────────────┘    │
│                            │
│ 🌙 晚餐                      │
│ ┌─────────────────────┐    │
│ │ 🖼️ ［工笔插画］       │    │
│ │ 莲子银耳羹            │    │
│ │ 功效：清心安神        │    │
│ │         [换一换 🔄]   │    │
│ └─────────────────────┘    │
│                            │
│ [首页] [方案] [社区] [我的] │
└─────────────────────────────┘
```

```
=== 一周计划 ===
┌─────────────────────────────┐
│ < 一周方案          [🌐]    │
│                            │
│ 周一 │ 周二 │ 周三 │ ...  │
│ ┌──┐ ┌──┐ ┌──┐           │
│ │🌅│ │🌅│ │🌅│           │
│ │🍚│ │🥣│ │🥗│           │
│ └──┘ └──┘ └──┘           │
│ ┌──┐ ┌──┐ ┌──┐           │
│ │🌤│ │🌤│ │🌤│           │
│ │🥘│ │🍲│ │🥟│           │
│ └──┘ └──┘ └──┘           │
│ ┌──┐ ┌──┐ ┌──┐           │
│ │🌙│ │🌙│ │🌙│           │
│ │🥣│ │🍜│ │🥗│           │
│ └──┘ └──┘ └──┘           │
│                            │
│ [单餐可点击替换]           │
└─────────────────────────────┘
```

```
=== 食谱详情 ===
┌─────────────────────────────┐
│ < 百合莲子银耳羹    [❤️]     │
│                            │
│ 🖼️ ［工笔食材插画］         │
│                            │
│ ┌─────────────────────┐    │
│ │ 📋 食材              │    │
│ │ 百合 15g · 莲子 20g  │    │
│ │ 银耳 10g · 冰糖 10g  │    │
│ └─────────────────────┘    │
│                            │
│ 📝 步骤                      │
│ │ 1. 银耳泡发撕小朵         │
│ │ 2. 百合莲子洗净          │
│ │ 3. 加水炖煮1小时          │
│ │ 4. 加冰糖调味            │
│                            │
│ 🌿 中医功效                  │
│ 滋阴润肺 · 清心安神         │
│ 性味：甘平，归肺胃心经      │
│                            │
│ 📊 营养数据                  │
│ 热量 120kcal · 蛋白 3g     │
│ 脂肪 0.5g · 碳水 28g       │
│                            │
│ ⚠️ 禁忌                      │
│ 风寒咳嗽 · 脾胃虚寒泄泻     │
│                            │
│ 📖 出处：《随息居饮食谱》    │
└─────────────────────────────┘
```

### 1.3 交互规则

| 页面 | 交互行为 |
|------|----------|
| 全局 | 页面切换淡入淡出，卡片浮现缓慢上移 |
| 首页 | 下拉刷新；点击体质状态卡→体质评估；点击推荐卡→食谱详情 |
| 体质评估 | 每步一题大卡片；选项选后自动进入下一步；支持后退修改 |
| 方案页 | 切换一日三餐/一周计划视图；一周计划中点击任意餐→替换弹窗 |
| 单餐替换 | 弹窗列出候补食谱（同季同体质）；点选后即时替换 |
| 食谱详情 | 收藏按钮→收藏列表；食材名点击→百科浮窗 |
| 反馈 | 结构化评分（1-5星）+ 文本输入框；提交后 AI 即时反馈 |

---

## 2. 后端终态

### 2.1 服务架构

```
┌─────────────┐   ┌─────────────┐   ┌──────────────┐
│  FastAPI     │   │  FastAPI     │   │  FastAPI      │
│  用户服务     │   │  食补方案服务 │   │  内容服务      │
│  /api/v1/user│   │  /api/v1/diet│   │  /api/v1/content
└──────┬──────┘   └──────┬──────┘   └───────┬───────┘
       │                  │                   │
       └──────────────────┼───────────────────┘
                          │
              ┌───────────┴───────────┐
              │    AI 检索引擎服务     │
              │  /api/v1/retrieval    │
              │  （语义检索+元数据过滤） │
              └───────────┬───────────┘
                          │
              ┌───────────┴───────────┐
              │    Chroma 向量数据库    │
              │    SQLite 业务数据库    │
              └───────────────────────┘
```

### 2.2 API 接口清单

| 模块 | 接口 | 方法 | 说明 |
|------|------|------|------|
| 用户服务 | `/api/v1/user/register` | POST | 用户注册 |
| | `/api/v1/user/login` | POST | 登录 |
| | `/api/v1/user/profile` | GET/PUT | 用户信息 |
| | `/api/v1/user/dietary-restrictions` | GET/PUT | 饮食禁忌 |
| 体质评估 | `/api/v1/constitution/assess` | POST | 提交问卷答案，返回评估结果 |
| | `/api/v1/constitution/result/{id}` | GET | 获取评估报告 |
| | `/api/v1/constitution/history` | GET | 体质变化历史 |
| | `/api/v1/constitution/chat` | POST | AI对话式问诊（流式） |
| 食补方案 | `/api/v1/diet/plan/generate` | POST | 生成食补方案（参数：维度条件） |
| | `/api/v1/diet/plan/{id}` | GET | 获取方案详情 |
| | `/api/v1/diet/plan/{id}/replace/{meal}` | POST | 替换单餐 |
| | `/api/v1/diet/recipe/{id}` | GET | 获取食谱详情 |
| | `/api/v1/diet/recipe/search` | GET | 搜索食谱（多维筛选） |
| 反馈 | `/api/v1/feedback/submit` | POST | 提交反馈 |
| | `/api/v1/feedback/history` | GET | 反馈历史 |
| 内容 | `/api/v1/content/daily-tip` | GET | 每日养生知识 |
| | `/api/v1/content/ingredient/{id}` | GET | 食材百科 |
| | `/api/v1/content/education-cards` | GET | 科普卡片列表 |
| 检索引擎 | `/api/v1/retrieval/search` | POST | 多维检索（元数据过滤+语义检索） |
| | `/api/v1/retrieval/ingest` | POST | 资料入库 |

### 2.3 关键调用链路

```
链路1：生成食补方案
[用户] → POST /diet/plan/generate
  → 读取用户档案（体质/禁忌/地域）
  → 获取当前季节
  → 调用 /retrieval/search
    → LLM 理解自然语言 → 提取查询条件
    → 元数据过滤（体质+季节+禁忌）
    → 语义检索（症状匹配）
    → 组合引擎排序
  → 拼装三餐/周方案
  → 返回方案

链路2：单餐替换
[用户] → POST /diet/plan/{id}/replace/{meal}
  → 获取原方案上下文（体质/季节）
  → 同条件检索候补食谱池
  → 排除已用食材（去重）
  → 排序取 top 5
  → 返回候补列表
  → 用户选择 → 替换 → 返回新方案

链路3：资料入库
[管理员] → POST /retrieval/ingest
  → 解析食谱/文本
  → LLM 辅助打标（结构化标签）
  → 存入向量库（embedding）
  → 存入业务库（元数据）
  → 更新索引
```

---

## 3. 数据层终态

### 3.1 数据库表设计

```
-- 用户表
users
├── id (UUID, PK)
├── phone (VARCHAR, 登录标识)
├── password_hash (VARCHAR)
├── nickname (VARCHAR)
├── avatar_url (VARCHAR)
├── region (VARCHAR, 地域)
├── dietary_restrictions (JSON, 饮食禁忌)
├── font_size (ENUM: normal/large)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

-- 体质评估记录
constitution_assessments
├── id (UUID, PK)
├── user_id (UUID, FK→users)
├── constitution_type (ENUM: 九种体质)
├── scores (JSON, 各维度分数)
├── trend (VARCHAR, 变化趋势)
├── assessment_date (DATE)
├── source (ENUM: questionnaire/chat)
├── report (TEXT, 评估报告)
├── created_at (TIMESTAMP)
└── ai_adjusted (BOOLEAN, 是否AI动态调整)

-- 食谱库（结构化）
recipes
├── id (UUID, PK)
├── name (VARCHAR, 食谱名称)
├── category (ENUM: 主食/菜肴/汤羹/甜品/饮品)
├── meal_type (JSON, 适配餐类 [早餐/午餐/晚餐])
├── ingredients (JSON, 食材清单+用量)
├── steps (JSON, 烹饪步骤)
├── efficacy (JSON, 中医功效列表)
├── nature_flavor (JSON, 性味归经)
├── nutrition (JSON, 营养成分)
├── contraindications (JSON, 禁忌)
├── source (VARCHAR, 古籍出处)
├── image_url (VARCHAR)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

-- 食谱多维索引标签
recipe_tags
├── id (UUID, PK)
├── recipe_id (UUID, FK→recipes)
├── dimension (ENUM: constitution/season/ingredient/efficacy/symptom/contraindication/meal_type)
├── tag_value (VARCHAR)
├── created_at (TIMESTAMP)
└── INDEX(recipe_id, dimension, tag_value)

-- 知识片段（名著切片）
knowledge_chunks
├── id (UUID, PK)
├── content (TEXT, 文本内容)
├── source (VARCHAR, 出处)
├── chunk_index (INT)
├── embedding_id (VARCHAR, 向量ID)
├── tags (JSON, 标签: 食材/功效/体质/季节)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

-- 食补方案
diet_plans
├── id (UUID, PK)
├── user_id (UUID, FK→users)
├── plan_type (ENUM: daily/weekly)
├── plan_date (DATE)
├── constitution_type (VARCHAR)
├── season (VARCHAR)
├── meals (JSON, 三餐/周具体内容 {meal_type, recipe_id, recipe_name})
├── status (ENUM: active/history)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

-- 用户反馈
user_feedback
├── id (UUID, PK)
├── user_id (UUID, FK→users)
├── plan_id (UUID, FK→diet_plans)
├── recipe_id (UUID, FK→recipes)
├── rating (INT, 1-5)
├── symptoms (JSON, 症状改善反馈)
├── text_content (TEXT)
├── ai_response (TEXT, AI反馈解读)
├── created_at (TIMESTAMP)
└── is_read (BOOLEAN)

-- 用户权重偏好
user_preferences
├── id (UUID, PK)
├── user_id (UUID, FK→users)
├── dimension (VARCHAR, 权重维度)
├── value (VARCHAR, 标签值)
├── weight (DECIMAL, 权重)
├── reason (VARCHAR, 调整原因)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

-- 食材百科（二期扩展）
ingredients_library
├── id (UUID, PK)
├── name (VARCHAR)
├── nature (VARCHAR, 性)
├── flavor (VARCHAR, 味)
├── meridian (VARCHAR, 归经)
├── efficacy (TEXT, 功效)
├── applicable_constitutions (JSON, 适用体质)
├── contraindications (TEXT, 禁忌)
├── nutrition (JSON, 营养成分)
├── season (VARCHAR, 时令)
└── image_url (VARCHAR)
```

### 3.2 数据流图

```
[资料入库]
食谱JSON/名著MD → 解析 → LLM打标 → Embedding → Chroma(向量)
                                              → SQLite(元数据)

[食补方案生成]
用户条件 → LLM意图提取 → 多维查询条件
    → 元数据过滤(SQLite) → 候选ID列表
    → 语义检索(Chroma) → 排序
    → 组合引擎 → 方案JSON → 返回用户

[反馈闭环]
用户反馈 → 存储 → AI反馈解读 → 更新user_preferences权重
    → 定期分析汇总 → 更新组合引擎规则
```

---

## 4. 业务逻辑终态

### 4.1 用户生命周期

```
注册 → 首次体质评估 → 生成首份方案
    ↓
执行方案 (使用/调整/替换)
    ↓
提交反馈 (每日/定时提醒)
    ↓
AI动态调整 (基于反馈微调体质判定+索引权重)
    ↓
周期性重新评估 (月度/季度)
    ↓
查看体质变化趋势 → 调整调养方向
```

### 4.2 业务规则

| 规则 | 说明 |
|------|------|
| 数据边界 | AI 严格基于已索引资料回答，不做超越资料的推理 |
| 免责声明 | 所有食补方案标注"仅供养生参考，不替代医疗诊断和治疗" |
| 隐私保护 | 健康数据加密存储，不共享给第三方 |
| 兜底策略 | 无完全匹配食谱时放宽症状条件；仍无则推荐同体质通用食谱 |
| 排序优先级 | 体质匹配 > 季节匹配 > 症状匹配 > 功效匹配 |
| 换餐原则 | 替换餐保持同季同体质，食材去重，性味平衡 |
| 展示限制 | 一次推荐≤7天（一周计划），超期重新生成 |
| 审核机制 | 用户分享食谱需 AI 审核标签"AI食补审核"或"仅供参考" |

### 4.3 维度体系

| 维度 | 取值空间 |
|------|----------|
| 体质 | 平和质、气虚质、阳虚质、阴虚质、痰湿质、湿热质、血瘀质、气郁质、特禀质 |
| 季节 | 春、夏、秋、冬 + 长夏（根据节气动态调整） |
| 餐类 | 早餐、午餐、晚餐、加餐 |
| 食谱类别 | 主食、菜肴、汤羹、甜品、饮品 |
| 功效 | 滋阴润肺、清热解毒、健脾益气、温补肾阳、活血化瘀等 |
| 症状 | 口干、失眠、乏力、便秘、上火、消化不良等 |
| 来源典籍 | 《随息居饮食谱》《本草纲目》《食疗本草》等 |

---

## 5. 技术架构终态

| 层级 | 选型 | 说明 |
|------|------|------|
| 前端 App | React Native | iOS + Android 跨平台 |
| 前端 小程序 | 微信原生 | 独立代码库 |
| 后端框架 | Python FastAPI | RESTful API |
| 向量数据库 | Chroma（开发）/ Milvus（生产） | 元数据过滤+语义检索 |
| 业务数据库 | SQLite（开发）/ PostgreSQL（生产） | 用户数据+业务数据 |
| Embedding | BGE-small-zh（开发）/ BGE-base-zh（生产） | CPU可运行 |
| LLM | Ollama + Qwen2.5-7B-Instruct-Q4_K_M | 仅意图理解+格式化输出 |
| 缓存 | Redis（生产可选） | 高频查询缓存 |
| 部署 | 本机开发 → 云服务器生产 | NVIDIA GPU 可选 |

---

## 6. 非功能性终态

| 指标 | 目标值 |
|------|--------|
| 方案生成响应 | < 5 秒 |
| 页面加载 | < 2 秒 |
| 离线支持 | 基础百科+已生成方案离线可读 |
| 大字体模式 | 支持系统字体缩放 |
| 隐私合规 | 健康数据加密，明确用户协议+隐私政策 |
| 可追溯 | 每条资料标注古籍出处，每份方案可溯源 |
