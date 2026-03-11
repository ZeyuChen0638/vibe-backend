from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# 优先级: 系统环境 > .env > 默认值
class Settings(BaseSettings):
    # 1. 基本项目配置
    PROJECT_NAME: str = "Vibe Platform"
    API_V1_STR: str = "/api"
    
    # 2. 数据库配置
    # 默认值，但实际运行中应通过环境变量覆盖
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/test"
    
    # 3. 跨域配置 (支持字符串解析为列表)
    # 给出一个默认值以免报错
    BACKEND_CORS_ORIGINS: List[Union[AnyHttpUrl, str]] = []

    # V2 风格的 field_validator
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        return []

    # 4. 读取配置
    model_config = SettingsConfigDict(
        extra="allow",  # 允许 .env 中有未定义的字段，并且加载进来
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True # 环境变量名需与字段名完全一致
    )

# 实例化
settings = Settings()