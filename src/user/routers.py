from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi_users.exceptions import UserAlreadyExists
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from database.dependencies import get_db
from . import schemas
from .auth import auth_backend, fastapi_users, get_jwt_strategy, current_user
from .manager import create_user, UserManager
from .models import User
from .schemas import UserRead, UserCreate, UserUpdate
from ..files.routers import templates

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@router.get("/login", response_class=HTMLResponse, tags=["auth"])
async def login(request: Request, user=None):
    return templates.TemplateResponse("auth/login.html", {"request": request, "user": user})


@router.post("/login", response_class=RedirectResponse, tags=["auth"])
async def login_post(
        email: str = Form(...),
        password: str = Form(...),
        user_manager: UserManager = Depends(fastapi_users.get_user_manager),
        request: Request = None,
):
    """Обработка логина."""
    user = await user_manager.authenticate(email=email, password=password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Генерация JWT токена
    strategy = get_jwt_strategy()
    token = await strategy.write_token(user)

    # Установка cookie с токеном
    response = RedirectResponse(url="/files", status_code=303)
    response.set_cookie(
        "access_token", token, httponly=True, max_age=3600, expires=3600
    )

    return response


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request, "user": None})


@router.post("/register", response_class=RedirectResponse, tags=["auth"])
async def register_post(
        email: str = Form(...),
        password: str = Form(...),
        user_manager: UserManager = Depends(fastapi_users.get_user_manager),
):
    try:
        user_create = UserCreate(email=email, password=password)
        user = await user_manager.create(user_create)
    except UserAlreadyExists:
        raise HTTPException(status_code=400, detail="User already exists")

    # Генерация JWT токена с использованием JWTStrategy
    strategy = get_jwt_strategy()  # Получаем стратегию
    token = await strategy.write_token(user)  # Генерация токена

    # Устанавливаем cookie с токеном
    response = RedirectResponse(url="/files", status_code=303)
    return response


@router.get("/users", tags=["users"])
async def read_users(db: AsyncSession = Depends(get_db)):
    query = select(User)
    users = await db.execute(query)
    users = [user for user in users.scalars()]
    return users
