# SP-05: 食谱与知识库数据模型

## 元信息

| 属性 | 值 |
|------|-----|
| 子计划编号 | SP-05 |
| 对应全局任务 | T-05 |
| 对应结果蓝图章节 | 数据表-recipes/recipe_tags/recipe_ingredients/knowledge_chunks/chunk_tags |
| 前置依赖子计划 | SP-01 |
| 输出产物 | `app/diet/models.py`, `app/content/models.py` |
| 执行Agent | 后端Dev |
| 预估复杂度 | 低 |

## 最终结果（来自结果蓝图）

### 要实现的内容

**`recipes` 表**：

| 字段 | 类型 | 约束 |
|------|------|------|
| id | UUID | PK |
| name | VARCHAR(200) | NOT NULL |
| category | ENUM(主食/菜肴/汤羹/甜品/饮品) | NOT NULL |
| meal_type | JSON | ["早餐","午餐","晚餐"] |
| ingredients | JSON | [{"name":"百合","amount":"15g"}] |
| steps | JSON | [{"step":1,"content":"..."}] |
| efficacy | JSON | ["滋阴润肺"] |
| nature_flavor | JSON | {"百合":"甘微寒，归心肺经"} |
| nutrition | JSON | {"calories":120} |
| contraindications | JSON | ["风寒咳嗽"] |
| source | VARCHAR(200) | 古籍出处 |
| source_detail | VARCHAR(500) | 原文引用 |
| image_url | VARCHAR(500) | |
| status | ENUM(draft/published/disabled) | DEFAULT 'published' |
| created_at, updated_at | TIMESTAMP | |

**`recipe_tags` 表**：recipe_id + dimension(constitution/season/ingredient/efficacy/ symptom/contraindication/meal_type/source) + tag_value

**`recipe_ingredients` 表**：recipe_id + ingredient_name + amount + note + sort_order

**`knowledge_chunks` 表**：id + content + source + source_chapter + chunk_index + embedding_id + status

**`chunk_tags` 表**：chunk_id + dimension + tag_value

### 验收标准

| 蓝图项 | 验收条件 | 状态 |
|--------|---------|------|
| 5 张表模型 | 定义正确，类型/约束/索引完整 | ⬜ |
| 表关系 | recipes↔recipe_tags, recipes↔recipe_ingredients 外键正确 | ⬜ |

## 上下文信息

### 输入依赖

| 输入项 | 来源 | 说明 |
|--------|------|------|
| database.py | SP-01 | SQLAlchemy Base, 会话管理 |

## 执行步骤

| 步骤 | 操作描述 | 预期中间产物 | 参考蓝图项 |
|------|---------|-------------|-----------|
| 1 | 定义 Recipe + RecipeTag + RecipeIngredient SQLAlchemy 模型 | `app/diet/models.py` | 3.2 食谱表 |
| 2 | 定义 KnowledgeChunk + ChunkTag SQLAlchemy 模型 | `app/content/models.py` | 3.2 知识库表 |
| 3 | 定义各模型对应的 Pydantic schemas | `app/diet/schemas.py`, `app/content/schemas.py` | — |

## 完成标志

- [ ] 5 张表模型定义完整
- [ ] Alembic 迁移可生成
- [ ] 逐项验证报告 `plan/2026-05-29/verification-sp-05-report.md` 已生成并填写

---

> 本子计划依据结果蓝图 `agent-doc/result-first/project-final-state.md` 制定。
> 对齐 `.opencode/AGENTS.md` v2：计划驱动 — 独立子计划文件 + 结果蓝图直引 + 逐项验证
