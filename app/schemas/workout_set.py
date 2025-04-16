from pydantic import BaseModel
from typing import Optional

class WorkoutSetBase(BaseModel):
    """
    Базовая схема подхода в упражнении.
    
    Атрибуты:
        set_number (int): Номер подхода
        weight (int): Вес в килограммах
        reps (int): Количество повторений
    """
    set_number: int
    weight: int
    reps: int

class WorkoutSetCreate(WorkoutSetBase):
    """Схема для создания подхода."""
    pass

class WorkoutSet(WorkoutSetBase):
    """
    Схема подхода с дополнительными полями.
    
    Атрибуты:
        id (int): Уникальный идентификатор
        workout_exercise_id (int): ID упражнения в тренировке
    """
    id: int
    workout_exercise_id: int

    class Config:
        from_attributes = True 