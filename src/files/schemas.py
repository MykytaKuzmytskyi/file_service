from pydantic import BaseModel
from datetime import datetime


class FileBase(BaseModel):
    filename: str
    downloads: int

    class Config:
        orm_mode = True


class FileCreate(BaseModel):
    filename: str
    filepath: str


class FileResponse(FileBase):
    id: int
    uploaded_at: datetime
