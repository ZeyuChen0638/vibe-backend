# app/note/schema.py
from datetime import datetime
from typing import Any

from fastapi import Form
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


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


class BookUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    is_pinned: bool | None = Field(default=None, alias="isPinned")

    @field_validator("name")
    @classmethod
    def normalize_name_for_update(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()
        if not value:
            raise ValueError("知识库名称不能为空")
        return value

    @model_validator(mode="after")
    def validate_has_updates(self):
        if len(self.model_fields_set - {"id"}) == 0:
            raise ValueError("至少提供一个需要更新的字段")
        return self


class BookListResponse(BaseModel):
    items: list[BookRead]
    total: int
    page: int
    page_size: int
    total_pages: int


class NoteCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    book_id: int = Field(alias="bookId")
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    is_pinned: bool = Field(default=False, alias="isPinned")

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("笔记标题不能为空")
        return value


class NoteUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    is_pinned: bool | None = Field(default=None, alias="isPinned")

    @field_validator("title")
    @classmethod
    def normalize_title_for_update(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()
        if not value:
            raise ValueError("笔记标题不能为空")
        return value

    @classmethod
    def as_form(
        cls,
        id: int = Form(...),
        title: str | None = Form(default=None),
        description: str | None = Form(default=None),
        is_pinned: bool | None = Form(default=None, alias="isPinned"),
    ) -> "NoteUpdate":
        data = {"id": id}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if is_pinned is not None:
            data["isPinned"] = is_pinned
        return cls(**data)


class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int
    title: str
    description: str | None
    json_url: str
    is_pinned: bool
    created_at: datetime
    updated_at: datetime


class NotePageRead(NoteRead):
    content: Any | None = None


class NoteListQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    book_id: int = Field(alias="bookId")


class NoteListResponse(BaseModel):
    items: list[NoteRead]


class NoteDelete(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
