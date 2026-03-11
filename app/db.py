import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import Generator
from sqlalchemy.orm import Session
from app.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 检查数据库是否存活
def check_db() -> str:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return "ok"
    except Exception as exc:  # pragma: no cover - runtime check
        return f"error: {exc.__class__.__name__}"

# 获取数据库会话的依赖项
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db  # 将 session 提供给 FastAPI 路由
    finally:
        db.close()  # 请求结束后自动关闭连接，释放回连接池