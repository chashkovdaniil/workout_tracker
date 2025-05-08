from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base
from datetime import datetime

class Exercise(Base):
    """
    Модель упражнения.
    
    Атрибуты:
        id (int): Уникальный идентификатор упражнения
        name (str): Название упражнения
        description (str): Описание упражнения (опционально)
        muscle_groups (list[str]): Группы мышц, задействованные в упражнении
        created_at (datetime): Дата и время создания записи
        user_id (int): ID пользователя, создавшего упражнение
        workout_exercises (relationship): Связь с упражнениями в тренировках
        user (relationship): Связь с пользователем
    """
    __tablename__ = "exercises"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    muscle_groups: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    workout_exercises = relationship("WorkoutExercise", back_populates="exercise")
    user = relationship("User", back_populates="exercises") 