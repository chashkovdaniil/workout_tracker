from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    """
    Схема JWT токена.
    
    Атрибуты:
        access_token (str): JWT токен
        token_type (str): Тип токена (bearer)
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Схема данных токена.
    
    Атрибуты:
        username (str): Имя пользователя
        exp (int, опционально): Время истечения токена
    """
    username: str
    exp: Optional[int] = None 