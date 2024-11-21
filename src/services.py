from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from pathlib import Path
import shutil

from src.files.models import File

FILE_STORAGE = Path("files")

if not FILE_STORAGE.exists():
    FILE_STORAGE.mkdir()


async def list_all_files(db: AsyncSession):
    """Отримати список усіх файлів."""
    query = await db.execute(select(File))
    return query.scalars().all()


async def upload_file_to_storage(file, db: AsyncSession):
    """Завантажити файл до сховища та додати запис у базу даних."""
    file_path = FILE_STORAGE / file.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        new_file = File(
            filename=file.filename,
            filepath=str(file_path),
            downloads=0,
        )
        db.add(new_file)
        await db.commit()
        return {"message": "File uploaded successfully."}
    except Exception:
        raise HTTPException(status_code=500, detail="File upload failed.")


async def download_file_by_id(file_id: int, db: AsyncSession) -> Path:
    """Отримати шлях до файлу за ідентифікатором."""
    query = await db.execute(select(File).where(File.id == file_id))
    file = query.scalar_one_or_none()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file.downloads += 1
    db.add(file)
    await db.commit()

    return Path(file.filepath)
