from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import check_db

app = FastAPI(title="Vibe Platform API")
router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/db")
def db_health():
    return {"db": check_db()}


app.include_router(router)
