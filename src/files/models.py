import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from db.database import Base
from src.users.models import User


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    uploaded_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    downloads = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    uploader = relationship(User, back_populates="uploaded_files")
    permissions = relationship("FilePermission", back_populates="file", cascade="all, delete-orphan")


class FilePermission(Base):
    __tablename__ = "file_permissions"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey('files.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    granted_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    granted_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)

    user = relationship(User, foreign_keys=[user_id])

    granted_by = relationship(User, foreign_keys=[granted_by_id])

    file = relationship("File", back_populates="permissions")
