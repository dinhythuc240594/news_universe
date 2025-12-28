
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, TypeDecorator
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship


class Base(DeclarativeBase):
    pass


# Database connection
_engine = None
_SessionLocal = None

def get_database_url():
    """Lấy URL kết nối database từ config"""
    from flask import current_app
    try:
        return current_app.config.get('DATABASE_URL', 'postgresql://postgres:123456789@localhost:5432/newsdb')
    except RuntimeError:
        # Nếu không có Flask app context, dùng giá trị mặc định
        import os
        return os.environ.get('DATABASE_URL', 'postgresql://postgres:123456789@localhost:5432/newsdb')

def create_engine_instance():
    """Tạo engine kết nối database"""
    global _engine
    if _engine is None:
        _engine = create_engine(get_database_url(), pool_size=20, max_overflow=20, pool_recycle=3600)
    return _engine

def get_session():
    global _SessionLocal
    if _SessionLocal is None:
        engine = create_engine_instance()
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _SessionLocal()

def init_db():
    engine = create_engine_instance()
    Base.metadata.create_all(engine)