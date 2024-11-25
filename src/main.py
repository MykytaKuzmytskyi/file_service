from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.users.routes import user_routers

app = FastAPI()

app.include_router(user_routers)

app.mount("/static", StaticFiles(directory="src/static"), name="static")
