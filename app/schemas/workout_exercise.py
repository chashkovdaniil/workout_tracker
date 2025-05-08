from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.exercise import ExerciseBase
from app.schemas.workout_set import WorkoutSet, WorkoutSetCreate, WorkoutSetUpdate

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
    sets: List[WorkoutSetCreate] = Field(default_factory=list) 

class WorkoutExerciseCreate(WorkoutExerciseBase):
    """Схема для создания упражнения в тренировке."""
    pass

class WorkoutExerciseUpdate(WorkoutExerciseBase):
    """Схема для обновления упражнения в тренировке."""
    exercise_id: Optional[int] = None
    sets: Optional[List[WorkoutSetUpdate]] = Field(default_factory=list)

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
    sets: List[WorkoutSet] = Field(default_factory=list)
    exercise: ExerciseBase
    class Config:
        from_attributes = True 