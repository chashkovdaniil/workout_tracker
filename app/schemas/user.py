from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """
    Базовая схема пользователя.
    
    Атрибуты:
        email (str): Email пользователя
        username (str): Имя пользователя
    """
    email: EmailStr
    username: str

class UserCreate(UserBase):
    """
    Схема для создания пользователя.
    
    Атрибуты:
        password (str): Пароль пользователя
    """
    password: str

class UserResponse(UserBase):
    """
    Схема пользователя с дополнительными полями.
    
    Атрибуты:
        id (int): Уникальный идентификатор
        is_active (bool): Статус активности
        created_at (datetime): Дата и время создания
    """
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserInDB(UserResponse):
    """
    Схема пользователя с хешированным паролем.
    
    Атрибуты:
        hashed_password (str): Хешированный пароль
    """
    hashed_password: str
 