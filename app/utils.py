from __future__ import annotations

import shutil
from pathlib import Path

from fastapi import UploadFile

from app.config import settings


class PlatformFileStorage:
    _instance: PlatformFileStorage | None = None

    def __new__(cls, root: str | Path | None = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, root: str | Path | None = None):
        configured_root = root or settings.FILE_STORAGE_ROOT
        root_path = Path(configured_root).expanduser()
        if not root_path.is_absolute():
            root_path = Path(__file__).resolve().parent.parent / root_path
        root_path = root_path.resolve()

        if getattr(self, '_initialized', False):
            if root_path != self.root:
                raise ValueError('PlatformFileStorage 单例已经初始化，不能切换存储根目录')
            return

        self.root = root_path
        self.root.mkdir(parents=True, exist_ok=True)
        self._initialized = True

    def resolve_path(self, relative_path: str | Path) -> Path:
        normalized_path = Path(str(relative_path).lstrip('/'))
        if normalized_path.is_absolute() or not normalized_path.parts or '..' in normalized_path.parts:
            raise ValueError('文件路径无效')
        return self.root / normalized_path

    def save_binary_content(self, content: bytes, destination: str | Path) -> str:
        target_path = self.resolve_path(destination)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_bytes(content)
        return str(target_path)

    def read_binary_content(self, source: str | Path) -> bytes:
        target_path = self.resolve_path(source)
        return target_path.read_bytes()

    async def save_upload_file(
        self,
        file: UploadFile,
        destination: str | Path,
        chunk_size: int = 1024 * 1024,
    ) -> str:
        target_path = self.resolve_path(destination)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with target_path.open('wb') as buffer:
            while chunk := await file.read(chunk_size):
                buffer.write(chunk)

        return str(target_path)

    def delete(self, target: str | Path, missing_ok: bool = True, recursive: bool = False) -> bool:
        target_path = self.resolve_path(target)
        if not target_path.exists():
            if missing_ok:
                return False
            raise FileNotFoundError(str(target_path))

        if target_path.is_dir():
            if recursive:
                shutil.rmtree(target_path)
            else:
                target_path.rmdir()
        else:
            target_path.unlink()

        self._cleanup_empty_parents(target_path.parent)
        return True

    def stat(self, target: str | Path) -> dict[str, str | int | float | bool | None]:
        target_path = self.resolve_path(target)
        if not target_path.exists():
            return {
                'exists': False,
                'path': str(target_path),
                'relative_path': str(target_path.relative_to(self.root)),
                'is_file': False,
                'is_dir': False,
                'size': 0,
                'modified_at': None,
            }

        stats = target_path.stat()
        return {
            'exists': True,
            'path': str(target_path),
            'relative_path': str(target_path.relative_to(self.root)),
            'is_file': target_path.is_file(),
            'is_dir': target_path.is_dir(),
            'size': stats.st_size,
            'modified_at': stats.st_mtime,
        }

    def summary(self, target: str | Path = '.') -> dict[str, str | int]:
        target_path = self.root if str(target) in {'', '.'} else self.resolve_path(target)
        if not target_path.exists():
            return {
                'path': str(target_path),
                'files': 0,
                'directories': 0,
                'total_bytes': 0,
            }

        file_count = 0
        directory_count = 0
        total_bytes = 0

        for child in target_path.rglob('*'):
            if child.is_dir():
                directory_count += 1
                continue
            file_count += 1
            total_bytes += child.stat().st_size

        return {
            'path': str(target_path),
            'files': file_count,
            'directories': directory_count,
            'total_bytes': total_bytes,
        }

    def _cleanup_empty_parents(self, start_path: Path) -> None:
        current = start_path
        while current != self.root and current.is_relative_to(self.root):
            try:
                current.rmdir()
            except OSError:
                break
            current = current.parent


def save_binary_content(content: bytes, destination: str | Path) -> str:
    storage = PlatformFileStorage()
    return storage.save_binary_content(content, destination)


def read_binary_content(source: str | Path) -> bytes:
    storage = PlatformFileStorage()
    return storage.read_binary_content(source)


async def save_upload_file(
    file: UploadFile,
    destination: str | Path,
    chunk_size: int = 1024 * 1024,
) -> str:
    storage = PlatformFileStorage()
    return await storage.save_upload_file(file, destination, chunk_size=chunk_size)
