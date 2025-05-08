from typing import Optional
from pydantic import BaseModel

from app.schemas.workout_exercise import WorkoutExercise, WorkoutExerciseUpdate
from app.schemas.workout_type import WorkoutTypeResponse

class WorkoutBase(BaseModel):
    """
    Базовая схема для тренировки.
    
    Атрибуты:
        name (str): Название тренировки
        description (str | None): Описание тренировки
        workout_type_id (int): ID типа тренировки
    """
    name: str
    description: Optional[str] = None
    workout_type_id: int
    exercises: list[WorkoutExercise] = []

class WorkoutCreate(WorkoutBase):
    """Схема для создания тренировки."""
    pass

class WorkoutUpdate(WorkoutBase):
    """Схема для обновления тренировки."""
    name: Optional[str] = None
    description: Optional[str] = None
    workout_type_id: Optional[int] = None
    exercises: Optional[list[WorkoutExerciseUpdate]] = None

class WorkoutResponse(WorkoutBase):
    """
    Схема для ответа с тренировкой.
    
    Атрибуты:
        id (int): ID тренировки
        user_id (int): ID пользователя
    """
    id: int
    user_id: int
    workout_type: WorkoutTypeResponse
    exercises: list[WorkoutExercise] = []

    class Config:
        """Настройки схемы."""
        from_attributes = True 