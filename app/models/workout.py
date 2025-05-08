from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
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
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    workout_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("workout_types.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    workout_type = relationship("WorkoutType", back_populates="workouts", lazy="joined")
    exercises = relationship("WorkoutExercise", back_populates="workout", lazy="selectin", cascade="all, delete-orphan")
    user = relationship("User", back_populates="workouts") 