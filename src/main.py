from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.users.routes import user_routes
from src.pages.routes import pages_routers

app = FastAPI()

app.include_router(user_routes)
app.include_router(pages_routers)

app.mount("/static", StaticFiles(directory="src/static"), name="static")
