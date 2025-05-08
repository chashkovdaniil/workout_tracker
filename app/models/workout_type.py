from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base
from datetime import datetime

class WorkoutType(Base):
    """
    Модель типа тренировки.
    
    Атрибуты:
        id (int): Уникальный идентификатор типа тренировки
        name (str): Название типа тренировки (например, "ноги + плечи")
        description (str): Описание типа тренировки (опционально)
        icon_url (str): URL иконки типа тренировки (опционально)
        created_at (datetime): Дата и время создания записи
        user_id (int): ID пользователя, создавшего тип тренировки
        workouts (relationship): Связь с тренировками этого типа
        user (relationship): Связь с пользователем
    """
    __tablename__ = "workout_types"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    icon_url: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    workouts = relationship("Workout", back_populates="workout_type")
    user = relationship("User", back_populates="workout_types") 