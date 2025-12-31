
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, TypeDecorator
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
import enum

from config import envConfig as ecf


class Base(DeclarativeBase):
    pass


class NewsStatus(enum.Enum):
    
    DRAFT = "draft"           # Bản nháp
    PENDING = "pending"       # Chờ duyệt
    PUBLISHED = "published"   # Đã xuất bản
    HIDDEN = "hidden"         # Đã ẩn
    REJECTED = "rejected"     # Đã từ chối

    def __str__(self):
        return self.value
    
    @classmethod
    def from_string(cls, value):
        """Convert string to NewsStatus enum"""
        if value is None:
            return None
        if isinstance(value, cls):
            return value
        try:
            # Try to get enum by value
            for status in cls:
                if status.value == value:
                    return status
        except (ValueError, AttributeError):
            pass
        return None


class NewsStatusType(TypeDecorator):
    """Custom type decorator for NewsStatus enum"""
    impl = String(20)
    cache_ok = True
    
    def __init__(self):
        super(NewsStatusType, self).__init__(length=20)
    
    def process_bind_param(self, value, dialect):
        """Convert enum to string when saving to database"""
        if value is None:
            return None
        if isinstance(value, NewsStatus):
            return value.value
        if isinstance(value, str):
            return value
        return str(value)
    
    def process_result_value(self, value, dialect):
        """Convert string to enum when reading from database"""
        if value is None:
            return None
        if isinstance(value, NewsStatus):
            return value
        # Convert string to enum
        if isinstance(value, str):
            # Try to find enum by value
            value_lower = value.lower()
            for status in NewsStatus:
                if status.value.lower() == value_lower:
                    return status
            # If not found, try NewsStatus.from_string
            result = NewsStatus.from_string(value)
            if result:
                return result
        # If all else fails, return None or raise error
        return None


class UserRole(enum.Enum):
    
    ADMIN = "admin"           # Quản trị viên
    EDITOR = "editor"         # Biên tập viên
    USER = "user"             # Người dùng thường

    def __str__(self):
        return self.value
    
    @classmethod
    def from_string(cls, value):
        """Convert string to UserRole enum"""
        if value is None:
            return None
        if isinstance(value, cls):
            return value
        try:
            # Try to get enum by value
            for role in cls:
                if role.value == value:
                    return role
        except (ValueError, AttributeError):
            pass
        return None


class UserRoleType(TypeDecorator):
    """Custom type decorator for UserRole enum"""
    impl = String(20)
    cache_ok = True
    
    def __init__(self):
        super(UserRoleType, self).__init__(length=20)
    
    def process_bind_param(self, value, dialect):
        """Convert enum to string when saving to database"""
        if value is None:
            return None
        if isinstance(value, UserRole):
            return value.value
        if isinstance(value, str):
            return value
        return str(value)
    
    def process_result_value(self, value, dialect):
        """Convert string to enum when reading from database"""
        if value is None:
            return None
        if isinstance(value, UserRole):
            return value
        # Convert string to enum
        if isinstance(value, str):
            # Try to find enum by value
            value_lower = value.lower()
            for role in UserRole:
                if role.value.lower() == value_lower:
                    return role
            # If not found, try UserRole.from_string
            result = UserRole.from_string(value)
            if result:
                return result
        # If all else fails, return None or raise error
        return None


# Database connection
_engine = None
_SessionLocal = None

def get_database_url():
    """Lấy URL kết nối database từ config"""
    from flask import current_app
    try:
        return current_app.config.get('DATABASE_URL', ecf.DATABASE_URL)
    except RuntimeError:
        # Nếu không có Flask app context, dùng giá trị mặc định
        import os
        return os.environ.get('DATABASE_URL', ecf.DATABASE_URL)

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