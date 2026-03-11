# app/api/router.py
from fastapi import APIRouter
from app.note.router import router as note_router

api_router = APIRouter()

# 统一管理各模块的路径前缀和标签
api_router.include_router(note_router, prefix="/note", tags=["笔记模块"])