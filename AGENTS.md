# Vibe Backend 项目上下文

## 项目概览

这个目录是 `Vibe Platform` 的后端工程，目前还处于非常早期的搭建阶段。

当前技术栈：
- FastAPI
- SQLAlchemy 2.x ORM
- PostgreSQL
- psycopg
- Alembic

依赖定义见 [requirements.txt](/home/owen/vibe-plt/vibe-backend/requirements.txt)。

## 当前进度

后端基础骨架已经搭好：
- 应用入口在 [main.py](/home/owen/vibe-plt/vibe-backend/app/main.py)
- 配置读取在 [config.py](/home/owen/vibe-plt/vibe-backend/app/config.py)
- 数据库引擎、会话和 `Base` 在 [database.py](/home/owen/vibe-plt/vibe-backend/app/database.py)
- 路由聚合在 [router.py](/home/owen/vibe-plt/vibe-backend/app/router.py)
- `note` 模块已经建立，但还没有完整落地

目前最主要的业务代码在 [db.py](/home/owen/vibe-plt/vibe-backend/app/note/db.py)：
- `Book`
- `Note`
- `NoteAsset`

它们表达的关系是：
- 一个 `Book` 对应多个 `Note`
- 一个 `Note` 对应多个 `NoteAsset`

最近一轮补充：
- `Book` 新增了 `is_pinned`
- `Note` 新增了 `description`
- `/api/note/image` 现在已经改成最小可用的 multipart 上传占位接口
  - 会接收 `UploadFile`
  - 会把文件流读完
  - 然后仍然返回一个写死的图片 URL

## 当前数据库状态

笔记相关 ORM 模型已经写在代码里，但数据库还没有真正建表。

根据最近一次真实数据库检查，`vibe_plt` 这个库里目前只有：
- `alembic_version`

这意味着：
- 模型已经存在
- PostgreSQL 中还没有 `books / notes / note_assets` 这些业务表
- 当前没有任何业务数据

## 当前数据模型

### `Book`
- `id`
- `name`，当前是唯一约束
- `description`
- `is_pinned`
- `created_at`
- `updated_at`

### `Note`
- `id`
- `book_id`
- `description`
- `title`
- `json_url`
- `is_pinned`
- `created_at`
- `updated_at`

说明：
- 更早的设计讨论里，曾考虑把整份笔记 JSON 直接存进数据库。
- 当前代码不是这个方案。
- 现在的实现是存 `json_url`，也就是默认笔记 JSON 文件本体放在外部存储里，数据库只记录地址。

### `NoteAsset`
- `id`
- `note_id`
- `asset_url`
- `asset_type`
- `display_name`
- `created_at`
- `updated_at`

说明：
- `asset_url` 目前带有 `unique=True` 且建了索引
- `asset_type` 当前被限制为：
  - `svg`
  - `png`
  - `jpg`
  - `jpeg`
  - `excalidraw`

## 路由状态

当前路由挂载关系：
- `app.main` 把总路由挂在 `/api`
- `app.router` 把 note 路由挂在 `/note`

因此当前 note 模块的前缀是：
- `/api/note`

但 note 模块目前还只是占位状态。

当前实际存在的接口在 [router.py](/home/owen/vibe-plt/vibe-backend/app/note/router.py)：
- `POST /api/note/image`

当前行为：
- 已经按 `multipart/form-data` 接收上传文件
- 当前会先把上传文件读完，再返回一个写死的 Picsum 图片地址
- 没有接数据库
- 没有接上传逻辑
- 没有接对象存储

## Alembic 状态

Alembic 配置相关文件：
- [alembic.ini](/home/owen/vibe-plt/vibe-backend/alembic.ini)
- [env.py](/home/owen/vibe-plt/vibe-backend/alembic/env.py)

当前迁移状态：
- 只有一个迁移文件：[b28d57267979_初始化.py](/home/owen/vibe-plt/vibe-backend/alembic/versions/b28d57267979_初始化.py)
- 这个文件当前是空的 `pass`
- 这个文件已经被视为历史迁移记录，不应该继续拿来追加新表

重要约束：
- 不要修改现有的 `b28d...` 迁移文件去加入新表
- 后续如果要建 `books / notes / note_assets`，应该新建一个新的 Alembic migration

## 配置与环境说明

[config.py](/home/owen/vibe-plt/vibe-backend/app/config.py) 里的默认配置：
- `PROJECT_NAME = "Vibe Platform"`
- `API_V1_STR = "/api"`
- 回退数据库地址是 `postgresql+psycopg://postgres:postgres@localhost:5432/test`

但本地实际已经验证成功可用的 PostgreSQL 连接是：
- 数据库名：`vibe_plt`
- 用户：`postgres`
- 主机：`127.0.0.1`
- 端口：`5432`

另外，Codex 使用的 `dev-postgres-mcp` 也已经验证过，MCP 链路和真实 SQL 查询都能成功执行。

## 当前已知问题

- [README.md](/home/owen/vibe-plt/vibe-backend/README.md) 里的启动说明是旧的
- `README` 里写的是 `conda activate vibe-code`
- `README` 里路径写的是 `/home/owen/vibe-plt/backend`
- 实际目录是 `/home/owen/vibe-plt/vibe-backend`
- `/api/note/image` 现在虽然能正确消费 multipart 上传，但仍然只是占位接口
- [env.py](/home/owen/vibe-plt/vibe-backend/alembic/env.py) 当前只导入了 `Base`，如果后面要用 Alembic 自动生成迁移，记得确保模型模块被导入
- 还没有 Pydantic schema
- 还没有 CRUD service 层
- 还没有真正的 book / note API
- 还没有测试

## 推荐的下一步顺序

1. 先明确 `Note` 到底要存什么：
   - 存整份 JSON
   - 只存 `json_url`
   - 或者两者都存
2. 新建 Alembic migration，正式创建：
   - `books`
   - `notes`
   - `note_assets`
3. 补充 Book / Note / Asset 的 Pydantic 请求响应模型
4. 实现 CRUD 接口
5. 把占位的 `/api/note/image` 改成真实上传或资源登记逻辑
6. 更新 [README.md](/home/owen/vibe-plt/vibe-backend/README.md)，让启动方式和真实项目一致

## 方便下次继续的简短记忆

如果后面开新聊天，最关键的上下文是：

- `vibe-backend` 是一个早期 FastAPI 后端，技术栈是 SQLAlchemy + Alembic + PostgreSQL
- 笔记相关模型已经写在 [db.py](/home/owen/vibe-plt/vibe-backend/app/note/db.py)
- `Book` 现在额外有 `is_pinned`，`Note` 现在额外有 `description`
- 数据库当前只有 `alembic_version`，业务表还没有真正创建
- `b28d...` 这个旧迁移文件不要再改
- PostgreSQL 连通性和 `dev-postgres-mcp` 都已经验证通过
- note 模块当前只有一个最小占位上传接口：
  - 路径是 `POST /api/note/image`
  - 可以接收 multipart 上传
  - 但仍然只返回假图片地址
