from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from database.database import Base
from src.files.models import File, FileAccessLog


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=True)

    uploaded_files = relationship(File, back_populates="uploader")
    access_logs = relationship(FileAccessLog, back_populates="user")
