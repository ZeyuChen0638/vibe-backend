from fastapi import APIRouter, FastAPI

from .db import check_db

app = FastAPI(title="Vibe Platform API")
router = APIRouter(prefix="/api")


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/db")
def db_health():
    return {"db": check_db()}


app.include_router(router)
