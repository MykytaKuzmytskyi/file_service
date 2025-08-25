from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.files.routers import router as file_routers
from src.user.routers import router as user_routers

app = FastAPI()

# Маршрути для файлів
app.include_router(user_routers)
app.include_router(file_routers, prefix="/files", tags=["File Management"])

# Статичні файли
app.mount("/static", StaticFiles(directory="src/static"), name="static")
