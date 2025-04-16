from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
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
    
    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    notes = Column(Text, nullable=True)
    
    workout = relationship("Workout", back_populates="exercises")
    exercise = relationship("Exercise", back_populates="workout_exercises")
    sets = relationship("WorkoutSet", back_populates="workout_exercise", cascade="all, delete-orphan") 