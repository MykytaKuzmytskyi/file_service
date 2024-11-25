from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import relationship

from db.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'

    uploaded_files = relationship("File", back_populates="uploader", cascade="all, delete-orphan")
    file_permissions = relationship("FilePermission", foreign_keys="FilePermission.user_id")
    granted_permissions = relationship("FilePermission", foreign_keys="FilePermission.granted_by_id")
