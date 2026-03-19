# app/note/router.py
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from .model import Book
from .schema import BookCreate, BookListResponse, BookRead

router = APIRouter()


@router.post("/books", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    normalized_name = payload.name
    existing_book_id = db.execute(
        select(Book.id)
        .where(func.lower(func.trim(Book.name)) == normalized_name.lower())
        .limit(1)
    ).scalar_one_or_none()

    if existing_book_id is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="知识库名称已存在",
        )

    book = Book(
        name=normalized_name,
        description=payload.description,
        is_pinned=payload.is_pinned,
    )
    db.add(book)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="知识库名称已存在",
        ) from exc

    db.refresh(book)
    return book


@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    await file.read()
    # https://picsum.photos/200/200
    # return {"url": "https://fastly.picsum.photos/id/477/1920/1080.jpg?hmac=8V4fJHSP89AfrwJxObukCzN7UvUriZ6QbXAC6lL-zDs"}
    return {"url": "https://fastly.picsum.photos/id/867/200/200.jpg?hmac=o_T4KIW6jPbGySRv8Em8TaP9PH_tgegfmPaYJJ394Y4"}
    # return {"url": "http://localhost:9090/test.png"}


@router.get("/books", response_model=BookListResponse)
async def get_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total = db.execute(select(func.count()).select_from(Book)).scalar_one()
    offset = (page - 1) * page_size
    books = db.execute(
        select(Book).order_by(Book.id).offset(offset).limit(page_size)
    ).scalars().all()
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0

    return BookListResponse(
        items=books,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )
