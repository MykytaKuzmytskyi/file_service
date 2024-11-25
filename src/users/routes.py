from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies import get_db
from .auth import auth_backend, fastapi_users
from .models import User
from .schemas import UserRead, UserCreate, UserUpdate

user_routes = APIRouter()

user_routes.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

user_routes.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

user_routes.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@user_routes.get("/users", tags=["users"])
async def read_users(db: AsyncSession = Depends(get_db)):
    query = select(User)
    users = await db.execute(query)
    users = [user for user in users.scalars()]
    return users
