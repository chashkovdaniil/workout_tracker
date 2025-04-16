from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WorkoutTypeBase(BaseModel):
    """
    Базовая схема типа тренировки.
    
    Атрибуты:
        name (str): Название типа тренировки
        description (str, опционально): Описание типа тренировки
        icon_url (str, опционально): URL иконки типа тренировки
    """
    name: str
    description: Optional[str] = None
    icon_url: Optional[str] = None

class WorkoutTypeCreate(WorkoutTypeBase):
    """Схема для создания типа тренировки."""
    pass

class WorkoutTypeResponse(WorkoutTypeBase):
    """
    Схема типа тренировки с дополнительными полями.
    
    Атрибуты:
        id (int): Уникальный идентификатор
        created_at (datetime): Дата и время создания
    """
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 