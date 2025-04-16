from pydantic import BaseModel

class WorkoutBase(BaseModel):
    """
    Базовая схема для тренировки.
    
    Атрибуты:
        name (str): Название тренировки
        description (str | None): Описание тренировки
        workout_type_id (int): ID типа тренировки
    """
    name: str
    description: str | None = None
    workout_type_id: int

class WorkoutCreate(WorkoutBase):
    """Схема для создания тренировки."""
    pass

class WorkoutResponse(WorkoutBase):
    """
    Схема для ответа с тренировкой.
    
    Атрибуты:
        id (int): ID тренировки
        user_id (int): ID пользователя
    """
    id: int
    user_id: int

    class Config:
        """Настройки схемы."""
        from_attributes = True 