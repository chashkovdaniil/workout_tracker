from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
import re
from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Rate limiting
limiter = Limiter(key_func=get_remote_address)

def rate_limit_exceeded_handler(request: Request, exc: Exception):
    raise HTTPException(status_code=429, detail="Too many requests")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверка пароля.
    
    Args:
        plain_password (str): Обычный пароль
        hashed_password (str): Хешированный пароль
    
    Returns:
        bool: True если пароль верный, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Хеширование пароля.
    
    Args:
        password (str): Пароль для хеширования
    
    Returns:
        str: Хешированный пароль
    """
    return pwd_context.hash(password)

def validate_password(password: str) -> None:
    """
    Валидация пароля.
    
    Требования:
    - Минимум 8 символов
    - Минимум 1 заглавная буква
    - Минимум 1 строчная буква
    - Минимум 1 цифра
    - Минимум 1 специальный символ
    """
    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Пароль должен содержать минимум 8 символов"
        )
    
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=400,
            detail="Пароль должен содержать минимум 1 заглавную букву"
        )
    
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=400,
            detail="Пароль должен содержать минимум 1 строчную букву"
        )
    
    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=400,
            detail="Пароль должен содержать минимум 1 цифру"
        )
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(
            status_code=400,
            detail="Пароль должен содержать минимум 1 специальный символ"
        )

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создание JWT токена.
    
    Args:
        data: Данные для кодирования в токен
        expires_delta: Время жизни токена
    
    Returns:
        str: JWT токен
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """
    Верификация JWT токена.
    
    Args:
        token: JWT токен
    
    Returns:
        dict: Данные из токена
    
    Raises:
        HTTPException: Если токен невалидный
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Невалидный токен",
            headers={"WWW-Authenticate": "Bearer"},
        ) 