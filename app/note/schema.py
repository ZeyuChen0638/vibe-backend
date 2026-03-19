# app/note/schema.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class BookCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    is_pinned: bool = Field(default=False, alias="isPinned")

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("知识库名称不能为空")
        return value


class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    is_pinned: bool
    created_at: datetime
    updated_at: datetime


class BookListResponse(BaseModel):
    items: list[BookRead]
    total: int
    page: int
    page_size: int
    total_pages: int
