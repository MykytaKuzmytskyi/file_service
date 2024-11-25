from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

pages_routers = APIRouter()

templates = Jinja2Templates(directory="src/pages/templates")


@pages_routers.get("/", response_class=HTMLResponse, tags=["pages"])
async def file_manager_page(
        request: Request,
):
    """Display the file management page."""
    return templates.TemplateResponse(
        "file_manager/file_manager.html",
        {"request": request}
    )


@pages_routers.get("/login", response_class=HTMLResponse, tags=["pages"])
async def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@pages_routers.get("/register", response_class=HTMLResponse, tags=["pages"])
async def register(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})
