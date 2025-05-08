from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class WorkoutExercise(Base):
    """
    Модель упражнения в тренировке.
    
    Атрибуты:
        id (int): Уникальный идентификатор упражнения в тренировке
        workout_id (int): ID тренировки
        exercise_id (int): ID упражнения
        notes (str, опционально): Заметки
        workout (relationship): Связь с тренировкой
        exercise (relationship): Связь с упражнением
        sets (relationship): Связь с подходами
    """
    __tablename__ = "workout_exercises"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    workout_id: Mapped[int] = mapped_column(Integer, ForeignKey("workouts.id"))
    exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey("exercises.id"))
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    workout = relationship("Workout", back_populates="exercises")
    exercise = relationship("Exercise")
    sets = relationship("WorkoutSet", back_populates="workout_exercise", cascade="all, delete-orphan") 