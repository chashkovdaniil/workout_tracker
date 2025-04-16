from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ExerciseBase(BaseModel):
    """
    Базовая схема упражнения.
    
    Атрибуты:
        name (str): Название упражнения
        description (str, опционально): Описание упражнения
        muscle_groups (list[str], опционально): Группы мышц
    """
    name: str
    description: Optional[str] = None
    muscle_groups: Optional[List[str]] = None

class ExerciseCreate(ExerciseBase):
    """Схема для создания упражнения."""
    pass

class ExerciseUpdate(ExerciseBase):
    """
    Схема для обновления упражнения.
    Все поля опциональны, так как можно обновлять только часть полей.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    muscle_groups: Optional[List[str]] = None

class ExerciseResponse(ExerciseBase):
    """
    Схема упражнения с дополнительными полями.
    
    Атрибуты:
        id (int): Уникальный идентификатор
        created_at (datetime): Дата и время создания
        user_id (int): ID пользователя, создавшего упражнение
    """
    id: int
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True 