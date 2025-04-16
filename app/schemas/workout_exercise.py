from pydantic import BaseModel
from typing import Optional, List
from app.schemas.exercise import Exercise
from app.schemas.workout_set import WorkoutSet, WorkoutSetCreate

class WorkoutExerciseBase(BaseModel):
    """
    Базовая схема упражнения в тренировке.
    
    Атрибуты:
        exercise_id (int): ID упражнения
        notes (str, опционально): Заметки
        sets (List[WorkoutSetCreate]): Список подходов
    """
    exercise_id: int
    notes: Optional[str] = None
    sets: List[WorkoutSetCreate]

class WorkoutExerciseCreate(WorkoutExerciseBase):
    """Схема для создания упражнения в тренировке."""
    pass

class WorkoutExercise(WorkoutExerciseBase):
    """
    Схема упражнения в тренировке с дополнительными полями.
    
    Атрибуты:
        id (int): Уникальный идентификатор
        workout_id (int): ID тренировки
        sets (List[WorkoutSet]): Список подходов
    """
    id: int
    workout_id: int
    sets: List[WorkoutSet]

    class Config:
        from_attributes = True 