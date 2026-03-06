from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import check_db

app = FastAPI(title="Vibe Platform API")
router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/image")
def health():
    # https://picsum.photos/200/200
    # return {"url": "https://fastly.picsum.photos/id/477/1920/1080.jpg?hmac=8V4fJHSP89AfrwJxObukCzN7UvUriZ6QbXAC6lL-zDs"}
    return {"url": "https://fastly.picsum.photos/id/867/200/200.jpg?hmac=o_T4KIW6jPbGySRv8Em8TaP9PH_tgegfmPaYJJ394Y4"}
    return {"url": "https://fastly.picsum.photos/id/118/1920/1080.jpg?hmac=d42KrCka0ICF4up1cFKNNipUmKDdTx_tqasvhTEmGvM"}

@router.get("/db")
def db_health():
    return {"db": check_db()}


app.include_router(router)
