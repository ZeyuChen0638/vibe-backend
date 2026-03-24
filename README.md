# Backend

FastAPI + PostgreSQL backend for Vibe Platform.

## Setup

```bash
cd /home/owen/CURA/CURA-Backend
uv sync
```

## Commands

```bash
# 开发模式，执行 fastapi dev app
uv run dev

# 生产模式启动
uv run start

# 使用 FastAPI 官方 CLI
uv run fastapi dev
uv run fastapi run

# 数据库迁移
uv run db upgrade head
uv run db revision --autogenerate -m "message"
uv run db downgrade -1
```

## Endpoints

- `GET /api/health`
- `GET /api/db`
