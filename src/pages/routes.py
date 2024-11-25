from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from db.database import get_async_session
from src.users.auth import current_user
from src.users.models import User

pages_routers = APIRouter()

templates = Jinja2Templates(directory="src/pages/templates")


@pages_routers.get("/", response_class=HTMLResponse)
async def file_manager_page(
        request: Request,
):
    """Display the file management page."""
    return templates.TemplateResponse(
        "file_manager/file_manager.html",
        {"request": request}
    )
