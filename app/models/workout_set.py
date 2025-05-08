from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base

class WorkoutSet(Base):
    """
    Модель подхода в упражнении.
    
    Атрибуты:
        id (int): Уникальный идентификатор подхода
        workout_exercise_id (int): ID упражнения в тренировке
        set_number (int): Номер подхода
        weight (int): Вес в килограммах
        reps (int): Количество повторений
        workout_exercise (relationship): Связь с упражнением в тренировке
    """
    __tablename__ = "workout_sets"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    workout_exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey("workout_exercises.id"))
    set_number: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)
    reps: Mapped[int] = mapped_column(Integer, nullable=False)
    
    workout_exercise = relationship("WorkoutExercise", back_populates="sets") 