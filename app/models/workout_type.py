from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
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
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    icon_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    workouts = relationship("Workout", back_populates="workout_type")
    user = relationship("User", back_populates="workout_types") 