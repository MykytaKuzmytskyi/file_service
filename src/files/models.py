import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.database import Base


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    uploaded_by = Column(Integer, ForeignKey('users.id'))
    downloads = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    uploader = relationship("User", back_populates="uploaded_files")
    access_logs = relationship("FileAccessLog", back_populates="file")


class FileAccessLog(Base):
    __tablename__ = "access_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    file_id = Column(Integer, ForeignKey('files.id'))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # Связь с пользователем и файлом на уровне Python
    user = relationship("User", back_populates="access_logs")
    file = relationship(File, back_populates="access_logs")
