from fastapi import APIRouter, Depends, UploadFile, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse, RedirectResponse, FileResponse
from starlette.templating import Jinja2Templates

from src.services import list_all_files, upload_file_to_storage, download_file_by_id
from database.database import get_async_session
from src.user.auth import current_user
from src.user.models import User

router = APIRouter()

templates = Jinja2Templates(directory="src/templates")


@router.get("/", response_class=HTMLResponse)
async def file_manager_page(
    request: Request,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Відобразити сторінку управління файлами."""
    files = await list_all_files(db)
    return templates.TemplateResponse(
        "file_manager/file_manager.html",
        {"request": request, "files": files, "user": user}
    )


@router.post("/upload")
async def upload_file(file: UploadFile, db: AsyncSession = Depends(get_async_session)):
    """Завантажити файл."""
    await upload_file_to_storage(file, db)
    return RedirectResponse(url="/files/", status_code=303)


@router.get("/download/{file_id}")
async def download_file(file_id: int, db: AsyncSession = Depends(get_async_session)):
    """Завантажити файл за ідентифікатором."""
    file_path = await download_file_by_id(file_id, db)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on server")
    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/octet-stream",
    )


