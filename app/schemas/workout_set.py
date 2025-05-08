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

class WorkoutSetUpdate(BaseModel):
    """Схема для обновления подхода, включая его ID. Все поля опциональны."""
    id: Optional[int] = None       # ID существующего подхода для обновления
    set_number: Optional[int] = None
    weight: Optional[int] = None
    reps: Optional[int] = None
    # Если есть другие поля в WorkoutSetBase, которые могут обновляться, добавьте их сюда как Optional

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