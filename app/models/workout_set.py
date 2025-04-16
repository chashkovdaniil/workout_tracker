from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
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
    
    id = Column(Integer, primary_key=True, index=True)
    workout_exercise_id = Column(Integer, ForeignKey("workout_exercises.id"))
    set_number = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    
    workout_exercise = relationship("WorkoutExercise", back_populates="sets") 