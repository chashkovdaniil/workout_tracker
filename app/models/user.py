from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.database.base import Base
from datetime import datetime

class User(Base):
    """
    Модель пользователя.
    
    Атрибуты:
        id (int): Уникальный идентификатор пользователя
        email (str): Email пользователя (уникальный)
        username (str): Имя пользователя (уникальное)
        hashed_password (str): Хешированный пароль
        is_active (bool): Статус активности пользователя
        created_at (datetime): Дата и время создания пользователя
        workout_types (relationship): Связь с типами тренировок пользователя
        exercises (relationship): Связь с упражнениями пользователя
        workouts (relationship): Связь с тренировками пользователя
    """
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    workout_types = relationship("WorkoutType", back_populates="user", cascade="all, delete-orphan")
    exercises = relationship("Exercise", back_populates="user", cascade="all, delete-orphan")
    workouts = relationship("Workout", back_populates="user", cascade="all, delete-orphan") 