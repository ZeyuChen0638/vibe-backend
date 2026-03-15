from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.router import api_router  # 导入聚合后的总路由
from app.database import check_db

# 初始化应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="API for Vibe Platform"
)

# --- 1. 全局中间件配置 ---
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# --- 2. 路由挂载 ---
# 这一行代码就接入了所有的业务模块（User, Video, Resource 等）
app.include_router(api_router, prefix=settings.API_V1_STR)
# --- 3. 基础监控接口 ---
@app.get("/api/health", tags=["Infrastructure"])
def health_check():
    """
    用于 K8s 或云平台的健康检查接口
    """
    return {
        "status": "up",
        "database": check_db(),
        "project_name": settings.PROJECT_NAME
    }

@app.get("/db")
def db_health():
    return {"db": check_db()}
