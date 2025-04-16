from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime

class Workout(Base):
    """
    Модель тренировки.
    
    Атрибуты:
        id (int): Уникальный идентификатор тренировки
        name (str): Название тренировки
        description (str): Описание тренировки (опционально)
        workout_type_id (int): ID типа тренировки
        user_id (int): ID пользователя, создавшего тренировку
        created_at (datetime): Дата и время создания записи
        workout_type (relationship): Связь с типом тренировки
        exercises (relationship): Связь с упражнениями в тренировке
        user (relationship): Связь с пользователем
    """
    __tablename__ = "workouts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    workout_type_id = Column(Integer, ForeignKey("workout_types.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workout_type = relationship("WorkoutType", back_populates="workouts")
    exercises = relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")
    user = relationship("User", back_populates="workouts") 